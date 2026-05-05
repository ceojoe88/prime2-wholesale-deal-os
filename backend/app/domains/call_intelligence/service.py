from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.domain.field_testing import apply_call_outcome, outreach_eligibility_for_lead
from app.domains.ai_gateway.ai_router import handle_ai_request
from app.domains.call_intelligence.extractor import OBJECTION_PATTERNS, extract_call_intelligence
from app.domains.call_intelligence.sanitizer import (
    sanitize_call_text,
    sanitize_follow_up,
    sanitize_input,
    sanitize_objection,
    sanitize_session,
    sanitize_signal,
)
from app.models import (
    AIRequestLog,
    AutonomousAgentTask,
    CallFollowUpRecommendation,
    CallIntelligenceSession,
    CallObjectionRecord,
    CallTranscriptInput,
    Deal,
    FieldCallOutcome,
    Lead,
    OperatorExceptionRecord,
    SellerSignalExtraction,
)


def _next_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:10]}"


def safe_response_for_objection(objection_type: str) -> tuple[str, str, list[str], str]:
    responses = {
        "price_too_low": (
            "Draft only: I understand price matters. The owner can review the documented condition, timeline, and available comparable evidence before deciding whether the number should be adjusted.",
            "medium",
            ["ARV range", "repair estimate", "safe offer range"],
            "review price alignment inside approved range",
        ),
        "wants_legal_title_explanation": (
            "Draft only: Those questions should be reviewed with the title company or a qualified professional before anyone relies on the explanation.",
            "high",
            ["attorney/title review reminder"],
            "route to compliance/title review reminder",
        ),
        "confused_about_assignment": (
            "Draft only: The owner should clearly explain the operator role and assignment process without hiding fees or making unsupported commitments.",
            "high",
            ["role disclosure checklist", "assignment disclosure review"],
            "escalate disclosure review",
        ),
        "wants_proof_buyer_can_close": (
            "Draft only: The owner can review buyer proof-of-funds status and decide what can be shared after sanitization and approval.",
            "medium",
            ["buyer POF status", "sanitized buyer info boundary"],
            "verify POF before response",
        ),
        "call_back_later": (
            "Draft only: Acknowledge the requested timing and place an owner-reviewed follow-up task on the queue.",
            "low",
            ["requested follow-up timing"],
            "create follow-up task",
        ),
    }
    return responses.get(
        objection_type,
        (
            "Draft only: Acknowledge the concern, confirm the operator will review the facts, and avoid pressure or unsupported promises.",
            "medium",
            ["source notes", "owner review"],
            "owner review required",
        ),
    )


def _create_exception(
    session: Session,
    *,
    session_id: str,
    exception_type: str,
    severity: str,
    reason: str,
    recommended_action: str,
) -> None:
    record_id = f"call-intel-exception-{session_id}-{exception_type}"
    if session.get(OperatorExceptionRecord, record_id):
        return
    session.add(
        OperatorExceptionRecord(
            id=record_id,
            exception_type=exception_type,
            severity=severity,
            source_record_type="call_intelligence_session",
            source_record_id=session_id,
            reason=reason,
            recommended_action=recommended_action,
            owner_action_required=True,
            status="open",
        )
    )


def _create_task(session: Session, *, session_id: str, lead_id: str, priority: str) -> None:
    task_id = f"call-intel-task-{session_id}"
    if session.get(AutonomousAgentTask, task_id):
        return
    session.add(
        AutonomousAgentTask(
            id=task_id,
            agent_name="Seller Temperature Agent",
            division="Seller Acquisition Division",
            task_type="call_intelligence_follow_up_review",
            source_record_type="call_intelligence_session",
            source_record_id=session_id,
            priority=priority,
            status="queued",
            recommendation="Review extracted seller signals and prepare draft-only follow-up. No live call, SMS, or email.",
            idempotency_key=f"{lead_id}:{session_id}:call-intel-task",
            owner_approval_required=True,
            draft_only=True,
            live_action_allowed=False,
        )
    )


def _maybe_ai_assist(
    session: Session,
    *,
    call_session_id: str,
    transcript_text: str,
    extracted: dict[str, object],
    use_ai_assist: bool,
) -> str | None:
    if not use_ai_assist:
        return None
    try:
        result = handle_ai_request(
            session,
            request_type="call_intelligence_extraction",
            prompt="Summarize extracted seller signals using transcript evidence only.",
            source_record_type="call_intelligence_session",
            source_record_id=call_session_id,
            source_data={
                "transcript_excerpt": transcript_text[:600],
                "extracted_signals": extracted,
                "next_best_action": "owner review",
            },
        )
    except Exception:
        return None
    return str(result["id"]) if result.get("allowed") else None


def analyze_call_session(
    session: Session,
    *,
    lead_id: str,
    transcript_text: str,
    input_type: str = "manual_call_notes",
    call_outcome_id: str | None = None,
    source_metadata: dict[str, object] | None = None,
    use_ai_assist: bool = True,
) -> dict[str, object]:
    lead = session.get(Lead, lead_id)
    if lead is None:
        raise ValueError("lead_not_found")
    text = sanitize_call_text(transcript_text)
    if not text:
        raise ValueError("transcript_text_required")
    extracted = extract_call_intelligence(text)
    session_id = _next_id("call-intel")
    ai_request_id = _maybe_ai_assist(
        session,
        call_session_id=session_id,
        transcript_text=text,
        extracted=extracted,
        use_ai_assist=use_ai_assist,
    )

    next_best_action = "review seller response and prepare draft-only next step"
    if extracted["do_not_contact_detected"]:
        next_best_action = "do not contact; retain record for owner and compliance review"
    elif extracted["legal_compliance_red_flags"]:
        next_best_action = "route legal/title questions to compliance review reminder"
    elif extracted["motivation_score_delta"] >= 15:
        next_best_action = "escalate motivated seller for seller acquisition review"
    elif extracted["asking_price"] and lead.deals:
        next_best_action = "prepare draft-only offer explanation from existing underwriting"

    call_session = CallIntelligenceSession(
        id=session_id,
        lead_id=lead_id,
        call_outcome_id=call_outcome_id,
        input_type=input_type,
        seller_motivation_reason=str(extracted["seller_motivation_reason"]),
        urgency_timeline=str(extracted["urgency_timeline"]),
        asking_price=extracted["asking_price"],
        property_condition=str(extracted["property_condition"]),
        repair_clues=extracted["repair_clues"],
        occupancy_status=str(extracted["occupancy_status"]),
        decision_maker_status=str(extracted["decision_maker_status"]),
        trust_level=float(extracted["trust_level"]),
        price_flexibility=float(extracted["price_flexibility"]),
        follow_up_preference=str(extracted["follow_up_preference"]),
        do_not_contact_detected=bool(extracted["do_not_contact_detected"]),
        legal_compliance_red_flags=extracted["legal_compliance_red_flags"],
        next_best_action=next_best_action,
        call_quality_score=float(extracted["call_quality_score"]),
        confidence_score=float(extracted["confidence_score"]),
        motivation_score_delta=float(extracted["motivation_score_delta"]),
        contactability_score_delta=float(extracted["contactability_score_delta"]),
        seller_temperature_update=float(extracted["seller_temperature_update"]),
        contract_readiness_influence=float(extracted["contract_readiness_influence"]),
        risk_score_influence=float(extracted["risk_score_influence"]),
        score_update_explanation={
            "motivation": "Raised when the seller references urgency, cash/as-is interest, or strong motivation words.",
            "contactability": "Lowered sharply for do-not-contact, raised when a next contact preference is captured.",
            "readiness": "Influenced by motivation, price flexibility, and legal/compliance risk.",
            "deterministic": True,
        },
        transcript_basis=extracted["transcript_basis"],
        ai_request_id=ai_request_id,
        deterministic_fallback_used=True,
        live_response_generated=False,
    )
    session.add(call_session)
    session.flush()
    session.add(
        CallTranscriptInput(
            id=_next_id("call-input"),
            session_id=session_id,
            input_type=input_type,
            transcript_text=text,
            sanitized_text=text,
            source_metadata=source_metadata or {},
            raw_audio_processed=False,
            live_call_recording=False,
        )
    )
    signal_map = {
        "motivation": "seller_motivation_reason",
        "timeline": "urgency_timeline",
        "asking_price": "asking_price",
        "condition": "property_condition",
        "occupancy": "occupancy_status",
        "decision_maker": "decision_maker_status",
        "follow_up_preference": "follow_up_preference",
    }
    for signal_type, source_key in signal_map.items():
        value = extracted.get(source_key)
        session.add(
            SellerSignalExtraction(
                id=_next_id("seller-signal"),
                session_id=session_id,
                signal_type=signal_type,
                signal_value=str(value or ""),
                confidence_score=float(extracted["confidence_score"]),
                transcript_basis=str(extracted["transcript_basis"]),
            )
        )
    for objection in extracted["seller_objections"]:
        draft, risk, required_data, next_action = safe_response_for_objection(str(objection))
        session.add(
            CallObjectionRecord(
                id=_next_id("call-objection"),
                session_id=session_id,
                objection_type=str(objection),
                safe_response_draft=draft,
                risk_level=risk,
                required_data=required_data,
                next_action=next_action,
                owner_review_required=True,
                draft_only=True,
                live_response_allowed=False,
            )
        )
    session.add(
        CallFollowUpRecommendation(
            id=_next_id("call-follow-up"),
            session_id=session_id,
            follow_up_type=str(extracted["follow_up_preference"]),
            recommended_timing="owner review before next touchpoint",
            draft_message_summary="Draft-only follow-up may be prepared after owner review; no live response is generated.",
            owner_review_required=True,
            live_send_allowed=False,
        )
    )

    if extracted["do_not_contact_detected"]:
        outcome = FieldCallOutcome(
            id=f"call-intel-dnc-{session_id}",
            lead_id=lead_id,
            call_datetime=datetime.now(UTC),
            contact_result="do_not_contact",
            motivation_notes="DNC detected from call intelligence input.",
            asking_price=extracted["asking_price"],
            timeline=str(extracted["urgency_timeline"]),
            property_condition_notes=str(extracted["property_condition"]),
            seller_objections=extracted["seller_objections"],
            seller_temperature=0,
            operator_notes="Automatically created from transcript DNC detection; review-only.",
            prime2_next_recommendation=next_best_action,
            live_call_recorded=False,
            live_outreach_allowed=False,
        )
        session.add(outcome)
        session.flush()
        apply_call_outcome(session, outcome)
        call_session.call_outcome_id = outcome.id
    elif extracted["motivation_score_delta"] >= 15:
        _create_exception(
            session,
            session_id=session_id,
            exception_type="call_intelligence_motivated_seller",
            severity="high",
            reason="Transcript indicates strong motivation or offer readiness.",
            recommended_action="Review seller acquisition queue and prepare draft-only next step.",
        )
        call_session.prime2_escalation_created = True
        _create_task(session, session_id=session_id, lead_id=lead_id, priority="high")
        call_session.follow_up_task_created = True

    if extracted["legal_compliance_red_flags"]:
        _create_exception(
            session,
            session_id=session_id,
            exception_type="call_intelligence_compliance_review",
            severity="high",
            reason="Seller asked for legal, contract, attorney, or title meaning.",
            recommended_action="Route to attorney/title review reminder; do not answer as legal guidance.",
        )
        call_session.compliance_escalation_created = True

    if extracted["asking_price"] and session.query(Deal).filter(Deal.lead_id == lead_id).first():
        call_session.draft_offer_explanation_created = True

    lead.motivation_score = max(0, min(100, lead.motivation_score + call_session.motivation_score_delta))
    if not call_session.do_not_contact_detected:
        lead.contactability_score = max(0, min(100, lead.contactability_score + call_session.contactability_score_delta))
    lead.seller_temperature = max(lead.seller_temperature, call_session.seller_temperature_update)
    lead.next_best_action = next_best_action
    session.commit()
    return call_intelligence_detail(session, session_id)


def call_intelligence_detail(session: Session, session_id: str) -> dict[str, object]:
    record = session.get(CallIntelligenceSession, session_id)
    if record is None:
        raise ValueError("call_intelligence_session_not_found")
    inputs = session.query(CallTranscriptInput).filter(CallTranscriptInput.session_id == session_id).all()
    signals = session.query(SellerSignalExtraction).filter(SellerSignalExtraction.session_id == session_id).all()
    objections = session.query(CallObjectionRecord).filter(CallObjectionRecord.session_id == session_id).all()
    followups = session.query(CallFollowUpRecommendation).filter(CallFollowUpRecommendation.session_id == session_id).all()
    return {
        "session": sanitize_session(record),
        "inputs": [sanitize_input(item) for item in inputs],
        "signals": [sanitize_signal(signal) for signal in signals],
        "objections": [sanitize_objection(objection) for objection in objections],
        "follow_ups": [sanitize_follow_up(followup) for followup in followups],
        "outreach_eligibility": outreach_eligibility_for_lead(session, record.lead_id),
        "draft_only": True,
        "live_response_generated": False,
    }


def call_intelligence_dashboard(session: Session) -> dict[str, object]:
    sessions = (
        session.query(CallIntelligenceSession)
        .order_by(CallIntelligenceSession.created_at.desc())
        .all()
    )
    objections = session.query(CallObjectionRecord).all()
    followups = session.query(CallFollowUpRecommendation).all()
    return {
        "sessions": [sanitize_session(record) for record in sessions],
        "recent_analyzed_calls": [sanitize_session(record) for record in sessions[:10]],
        "high_motivation_sellers": [
            sanitize_session(record)
            for record in sessions
            if record.motivation_score_delta >= 15 or record.seller_temperature_update >= 75
        ],
        "dnc_detected": [sanitize_session(record) for record in sessions if record.do_not_contact_detected],
        "objections": [sanitize_objection(record) for record in objections],
        "follow_ups": [sanitize_follow_up(record) for record in followups],
        "legal_compliance_escalations": [
            sanitize_session(record)
            for record in sessions
            if record.legal_compliance_red_flags or record.compliance_escalation_created
        ],
        "call_quality_average": round(
            sum(record.call_quality_score for record in sessions) / max(len(sessions), 1),
            1,
        ),
        "next_best_seller_actions": [record.next_best_action for record in sessions],
        "live_calling_inside_system": False,
        "live_response_generation_allowed": False,
    }
