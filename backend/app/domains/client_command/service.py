from __future__ import annotations

from uuid import uuid4

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.domains.client_command.permissions import (
    CLIENT_COMMAND_PERMISSIONS,
    has_permission,
    member_permissions,
)
from app.domains.client_command.safety import (
    client_command_safety_rules,
    validate_client_safe_text,
)
from app.domains.client_command.sanitizer import (
    acquisition_brief_public,
    acquisition_event_public,
    action_public,
    appointment_readiness_public,
    evidence_item_public,
    evidence_packet_public,
    event_public,
    follow_up_draft_public,
    lead_public,
    member_public,
    missing_item_public,
    objection_draft_public,
    offer_readiness_public,
    offer_scenario_public,
    question_plan_public,
    role_public,
    score_public,
    seller_question_public,
    underwriting_event_public,
    underwriting_review_public,
    workspace_public,
)
from app.domains.client_command.scoring import missing_fields, score_client_lead
from app.models import (
    ClientLeadDivisionEvent,
    ClientLeadIntelligenceScore,
    ClientLeadMissingDataItem,
    ClientLeadNextBestAction,
    ClientLeadProfile,
    ClientWorkspace,
    ClientWorkspaceMember,
    ClientWorkspaceRole,
    ClientAcquisitionBrief,
    ClientSellerQuestionPlan,
    ClientSellerQuestion,
    ClientObjectionResponseDraft,
    ClientFollowUpDraft,
    ClientAppointmentReadinessReview,
    ClientAcquisitionDivisionEvent,
    ClientDealEvidencePacket,
    ClientDealEvidenceItem,
    ClientUnderwritingReview,
    ClientOfferScenario,
    ClientOfferReadinessGate,
    ClientUnderwritingDivisionEvent,
)


class ClientCommandPermissionError(ValueError):
    pass


def list_workspaces(session: Session) -> dict[str, object]:
    workspaces = session.query(ClientWorkspace).order_by(ClientWorkspace.workspace_name).all()
    return {
        "permissions": sorted(CLIENT_COMMAND_PERMISSIONS),
        "safety": client_command_safety_rules(),
        "workspaces": [workspace_public(workspace) for workspace in workspaces],
    }


def workspace_detail(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    roles = (
        session.query(ClientWorkspaceRole)
        .filter(ClientWorkspaceRole.workspace_id == workspace_id)
        .order_by(ClientWorkspaceRole.role_name)
        .all()
    )
    members = (
        session.query(ClientWorkspaceMember)
        .filter(ClientWorkspaceMember.workspace_id == workspace_id)
        .order_by(ClientWorkspaceMember.member_name)
        .all()
    )
    leads = (
        session.query(ClientLeadProfile)
        .filter(ClientLeadProfile.workspace_id == workspace_id)
        .order_by(ClientLeadProfile.created_at)
        .all()
    )
    return {
        "workspace": workspace_public(workspace),
        "roles": [role_public(role) for role in roles],
        "members": [member_public(member) for member in members],
        "lead_count": len(leads),
        "hot_lead_count": len(
            [
                score
                for score in _scores_for_workspace(session, workspace_id)
                if score.final_priority_score >= 78
            ]
        ),
        "safety": client_command_safety_rules(),
    }


def leads_for_workspace(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    leads = (
        session.query(ClientLeadProfile)
        .filter(ClientLeadProfile.workspace_id == workspace_id)
        .order_by(ClientLeadProfile.created_at)
        .all()
    )
    return {
        "workspace_id": workspace_id,
        "leads": [lead_card(session, lead) for lead in leads],
        "safety": client_command_safety_rules(),
    }


def list_leads(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientLeadProfile)
    if workspace_id:
        query = query.filter(ClientLeadProfile.workspace_id == workspace_id)
    leads = query.order_by(ClientLeadProfile.workspace_id, ClientLeadProfile.created_at).all()
    return {
        "workspace_id": workspace_id,
        "leads": [lead_card(session, lead) for lead in leads],
        "safety": client_command_safety_rules(),
    }


def lead_detail(session: Session, lead_id: str, workspace_id: str | None = None) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    score = ensure_score(session, lead)
    brief = ensure_acquisition_brief(session, lead)
    plan = ensure_question_plan(session, lead)
    ensure_objection_drafts(session, lead)
    ensure_follow_up_drafts(session, lead)
    readiness = ensure_appointment_readiness(session, lead)
    packet = ensure_evidence_packet(session, lead)
    review = ensure_underwriting_review(session, lead, packet)
    gate = ensure_offer_readiness(session, lead, packet, review)
    return {
        "lead": lead_public(lead),
        "score": score_public(score),
        "missing_data": [
            missing_item_public(item)
            for item in _missing_items(session, lead.workspace_id, lead.id)
        ],
        "next_actions": [
            action_public(action)
            for action in _next_actions(session, lead.workspace_id, lead.id)
        ],
        "division_events": [
            event_public(event)
            for event in _division_events(session, lead.workspace_id, lead.id)
        ],
        "acquisition": {
            "brief": acquisition_brief_public(brief),
            "question_plan": question_plan_public(plan),
            "questions": [
                seller_question_public(question)
                for question in _seller_questions(session, lead.workspace_id, lead.id, plan.id)
            ],
            "objection_drafts": [
                objection_draft_public(draft)
                for draft in _objection_drafts(session, lead.workspace_id, lead.id)
            ],
            "follow_up_drafts": [
                follow_up_draft_public(draft)
                for draft in _follow_up_drafts(session, lead.workspace_id, lead.id)
            ],
            "appointment_readiness": appointment_readiness_public(readiness),
            "division_events": [
                acquisition_event_public(event)
                for event in _acquisition_events(session, lead.workspace_id, lead.id)
            ],
        },
        "underwriting": {
            "evidence_packet": evidence_packet_public(packet),
            "evidence_items": [
                evidence_item_public(item)
                for item in _evidence_items(session, lead.workspace_id, lead.id, packet.id)
            ],
            "underwriting_review": underwriting_review_public(review),
            "offer_scenarios": [
                offer_scenario_public(scenario)
                for scenario in _offer_scenarios(session, lead.workspace_id, lead.id, review.id)
            ],
            "offer_readiness": offer_readiness_public(gate),
            "division_events": [
                underwriting_event_public(event)
                for event in _underwriting_events(session, lead.workspace_id, lead.id)
            ],
        },
        "safety": client_command_safety_rules(),
    }


def score_lead(session: Session, lead_id: str, workspace_id: str | None = None) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    score = ensure_score(session, lead, refresh=True)
    return {
        "lead": lead_public(lead),
        "score": score_public(score),
        "missing_data": [
            missing_item_public(item)
            for item in _missing_items(session, lead.workspace_id, lead.id)
        ],
        "next_action": action_public(_ensure_next_action(session, lead, score)),
        "safety": client_command_safety_rules(),
    }


def hot_board(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientLeadIntelligenceScore)
    if workspace_id:
        query = query.filter(ClientLeadIntelligenceScore.workspace_id == workspace_id)
    scores = query.order_by(desc(ClientLeadIntelligenceScore.final_priority_score)).all()
    hot_scores = [score for score in scores if score.final_priority_score >= 70]
    return {
        "workspace_id": workspace_id,
        "hot_leads": [
            {
                "lead": lead_public(_lead_or_404(session, score.lead_id, score.workspace_id)),
                "score": score_public(score),
            }
            for score in hot_scores
        ],
        "safety": client_command_safety_rules(),
    }


def next_actions(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientLeadNextBestAction)
    if workspace_id:
        query = query.filter(ClientLeadNextBestAction.workspace_id == workspace_id)
    actions = query.order_by(desc(ClientLeadNextBestAction.priority)).all()
    return {
        "workspace_id": workspace_id,
        "next_actions": [action_public(action) for action in actions],
        "outbound_provider_actions_allowed": False,
        "safety": client_command_safety_rules(),
    }


def lead_card(session: Session, lead: ClientLeadProfile) -> dict[str, object]:
    score = ensure_score(session, lead)
    return {
        "lead": lead_public(lead),
        "score": score_public(score),
        "missing_data_count": len(missing_fields(lead)),
        "recommended_next_action": score.recommended_next_action,
        "requires_human_review": score.requires_human_review,
    }


def ensure_score(
    session: Session,
    lead: ClientLeadProfile,
    refresh: bool = False,
) -> ClientLeadIntelligenceScore:
    score = (
        session.query(ClientLeadIntelligenceScore)
        .filter(ClientLeadIntelligenceScore.lead_id == lead.id)
        .first()
    )
    values = score_client_lead(lead)
    if score is None:
        score = ClientLeadIntelligenceScore(
            id=f"client-score-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
        )
        session.add(score)
    if refresh or score.final_priority_score == 0:
        for key, value in values.items():
            if key != "missing_fields":
                setattr(score, key, value)
        score.client_safe = True
        _sync_missing_items(session, lead, values["missing_fields"])
        _ensure_next_action(session, lead, score)
        _ensure_division_event(session, lead, score)
        session.flush()
    return score


def acquisition_brief_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    brief = ensure_acquisition_brief(session, lead, refresh=refresh)
    return {"lead": lead_public(lead), "brief": acquisition_brief_public(brief), "safety": client_command_safety_rules()}


def question_plan_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    plan = ensure_question_plan(session, lead, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "question_plan": question_plan_public(plan),
        "questions": [
            seller_question_public(question)
            for question in _seller_questions(session, lead.workspace_id, lead.id, plan.id)
        ],
        "safety": client_command_safety_rules(),
    }


def objection_drafts_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    drafts = ensure_objection_drafts(session, lead, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "objection_drafts": [objection_draft_public(draft) for draft in drafts],
        "safety": client_command_safety_rules(),
    }


def follow_up_drafts_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    drafts = ensure_follow_up_drafts(session, lead, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "follow_up_drafts": [follow_up_draft_public(draft) for draft in drafts],
        "outbound_provider_actions_allowed": False,
        "safety": client_command_safety_rules(),
    }


def appointment_readiness_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    review = ensure_appointment_readiness(session, lead, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "appointment_readiness": appointment_readiness_public(review),
        "safety": client_command_safety_rules(),
    }


def acquisition_briefs(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientAcquisitionBrief)
    if workspace_id:
        query = query.filter(ClientAcquisitionBrief.workspace_id == workspace_id)
    briefs = query.order_by(desc(ClientAcquisitionBrief.updated_at)).all()
    return {
        "workspace_id": workspace_id,
        "briefs": [acquisition_brief_public(brief) for brief in briefs],
        "safety": client_command_safety_rules(),
    }


def acquisition_needs_review(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientAppointmentReadinessReview).filter(
        ClientAppointmentReadinessReview.requires_human_review.is_(True)
    )
    if workspace_id:
        query = query.filter(ClientAppointmentReadinessReview.workspace_id == workspace_id)
    reviews = query.order_by(ClientAppointmentReadinessReview.readiness_score).all()
    return {
        "workspace_id": workspace_id,
        "needs_review": [appointment_readiness_public(review) for review in reviews],
        "safety": client_command_safety_rules(),
    }


def evidence_packet_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    packet = ensure_evidence_packet(session, lead, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "evidence_packet": evidence_packet_public(packet),
        "evidence_items": [
            evidence_item_public(item)
            for item in _evidence_items(session, lead.workspace_id, lead.id, packet.id)
        ],
        "safety": client_command_safety_rules(),
    }


def evidence_items_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    packet = ensure_evidence_packet(session, lead, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "packet_id": packet.id,
        "evidence_items": [
            evidence_item_public(item)
            for item in _evidence_items(session, lead.workspace_id, lead.id, packet.id)
        ],
        "safety": client_command_safety_rules(),
    }


def underwriting_review_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    packet = ensure_evidence_packet(session, lead)
    review = ensure_underwriting_review(session, lead, packet, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "evidence_packet": evidence_packet_public(packet),
        "underwriting_review": underwriting_review_public(review),
        "offer_scenarios": [
            offer_scenario_public(scenario)
            for scenario in _offer_scenarios(session, lead.workspace_id, lead.id, review.id)
        ],
        "safety": client_command_safety_rules(),
    }


def offer_readiness_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    packet = ensure_evidence_packet(session, lead)
    review = ensure_underwriting_review(session, lead, packet)
    gate = ensure_offer_readiness(session, lead, packet, review, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "offer_readiness": offer_readiness_public(gate),
        "decision_support_only": True,
        "safety": client_command_safety_rules(),
    }


def underwriting_ready_review(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientOfferReadinessGate).filter(
        ClientOfferReadinessGate.readiness_status == "ready_for_client_review"
    )
    if workspace_id:
        query = query.filter(ClientOfferReadinessGate.workspace_id == workspace_id)
    gates = query.order_by(desc(ClientOfferReadinessGate.readiness_score)).all()
    return {
        "workspace_id": workspace_id,
        "ready_review": [offer_readiness_public(gate) for gate in gates],
        "safety": client_command_safety_rules(),
    }


def underwriting_blocked(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientOfferReadinessGate).filter(
        ClientOfferReadinessGate.readiness_status.in_(["blocked", "evidence_missing", "underwriting_review_needed"])
    )
    if workspace_id:
        query = query.filter(ClientOfferReadinessGate.workspace_id == workspace_id)
    gates = query.order_by(ClientOfferReadinessGate.readiness_score).all()
    return {
        "workspace_id": workspace_id,
        "blocked": [offer_readiness_public(gate) for gate in gates],
        "safety": client_command_safety_rules(),
    }


def underwriting_needs_human_review(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientOfferReadinessGate).filter(
        ClientOfferReadinessGate.requires_human_review.is_(True)
    )
    if workspace_id:
        query = query.filter(ClientOfferReadinessGate.workspace_id == workspace_id)
    gates = query.order_by(ClientOfferReadinessGate.readiness_score).all()
    return {
        "workspace_id": workspace_id,
        "needs_human_review": [offer_readiness_public(gate) for gate in gates],
        "safety": client_command_safety_rules(),
    }


def ensure_acquisition_brief(
    session: Session,
    lead: ClientLeadProfile,
    refresh: bool = False,
) -> ClientAcquisitionBrief:
    score = ensure_score(session, lead)
    missing = _missing_items(session, lead.workspace_id, lead.id)
    brief = (
        session.query(ClientAcquisitionBrief)
        .filter(ClientAcquisitionBrief.lead_id == lead.id)
        .first()
    )
    if brief is None:
        brief = ClientAcquisitionBrief(
            id=f"client-acq-brief-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
        )
        session.add(brief)
    if refresh or not brief.seller_summary:
        signals = ", ".join(lead.motivation_signals or []) or "motivation not confirmed"
        channels = ", ".join(lead.contact_channels_present or []) or "contact channel missing"
        brief.seller_summary = f"{lead.display_name} in {lead.property_city or 'unknown market'} with {signals}."
        brief.lead_priority_snapshot = {
            "final_priority_score": score.final_priority_score,
            "recommended_next_action": score.recommended_next_action,
            "missing_data_count": len([item for item in missing if item.resolution_status == "open"]),
        }
        brief.motivation_hypothesis = (
            "Likely motivated by " + signals
            if lead.motivation_signals
            else "Motivation is unconfirmed; ask open discovery questions first."
        )
        brief.urgency_hypothesis = (
            "Timeline signal is strong; confirm whether the seller has a specific date."
            if score.urgency_score >= 70
            else "Timeline is not yet strong enough for appointment pressure; keep tone exploratory."
        )
        brief.property_context_summary = (
            f"{lead.property_type or 'Property type unknown'} in {lead.property_address_summary or 'address missing'}; "
            f"estimated value signal {lead.estimated_value or 0} and equity signal {lead.estimated_equity_percent or 0}%."
        )
        brief.recommended_call_objective = _acquisition_objective(score, missing)
        brief.suggested_opening_angle = (
            "Open with a calm property check-in and ask what the seller would like to do next."
        )
        brief.top_questions_to_ask_summary = _question_summary(lead, missing)
        brief.sensitive_topics_to_avoid = [
            "Do not pressure the seller.",
            "Do not imply a legal conclusion.",
            "Do not claim buyer demand or pricing certainty without evidence.",
        ]
        brief.suggested_tone = "calm, curious, respectful"
        brief.confidence_level = score.confidence_level
        brief.requires_human_review = score.requires_human_review or len(missing) >= 3
        brief.manager_name = "Acquisition Manager"
        brief.source_basis_summary = "Built from CP2 lead score, lead profile fields, and missing-data checklist."
        brief.client_safe_summary = (
            f"Prepare a manual seller conversation using {channels}; no outbound action is performed."
        )
        _ensure_acquisition_event(session, lead, "acquisition_brief", "Acquisition Manager prepared a client-safe call brief.")
        session.flush()
    return brief


def ensure_question_plan(
    session: Session,
    lead: ClientLeadProfile,
    refresh: bool = False,
) -> ClientSellerQuestionPlan:
    missing = _missing_items(session, lead.workspace_id, lead.id)
    plan = (
        session.query(ClientSellerQuestionPlan)
        .filter(ClientSellerQuestionPlan.lead_id == lead.id)
        .first()
    )
    if plan is None:
        plan = ClientSellerQuestionPlan(
            id=f"client-question-plan-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
        )
        session.add(plan)
    existing = _seller_questions(session, lead.workspace_id, lead.id, plan.id)
    if refresh or not existing:
        if existing:
            session.query(ClientSellerQuestion).filter(
                ClientSellerQuestion.question_plan_id == plan.id
            ).delete(synchronize_session=False)
        questions = _build_questions(lead, missing)
        for question in questions:
            session.add(
                ClientSellerQuestion(
                    id=f"client-question-{uuid4().hex[:10]}",
                    question_plan_id=plan.id,
                    workspace_id=lead.workspace_id,
                    lead_id=lead.id,
                    **question,
                )
            )
        plan.total_questions = len(questions)
        plan.high_priority_count = len([question for question in questions if question["priority"] == "high"])
        plan.missing_data_focus_count = len([question for question in questions if question.get("tied_missing_data_key")])
        plan.plan_status = "needs_review" if plan.high_priority_count >= 4 else "ready_for_manual_use"
        plan.client_safe_summary = "Question plan is manual-use only and is based on CP2 missing-data signals."
        _ensure_acquisition_event(session, lead, "question_plan", "Acquisition Manager prepared seller discovery questions.")
        session.flush()
    return plan


def ensure_objection_drafts(
    session: Session,
    lead: ClientLeadProfile,
    refresh: bool = False,
) -> list[ClientObjectionResponseDraft]:
    existing = _objection_drafts(session, lead.workspace_id, lead.id)
    if refresh and existing:
        session.query(ClientObjectionResponseDraft).filter(
            ClientObjectionResponseDraft.lead_id == lead.id
        ).delete(synchronize_session=False)
        existing = []
    if not existing:
        drafts = [
            (
                "price_too_low",
                "The number feels lower than expected.",
                "I understand. My goal is to be transparent about the repairs, timeline, and as-is purchase assumptions. If your target number is different, I can note it and compare it against the property facts before any next step.",
                "medium",
            ),
            (
                "needs_time",
                "I need more time to think.",
                "That makes sense. I can summarize what we discussed and note a follow-up date that works for you. Nothing is final from this conversation.",
                "low",
            ),
            (
                "trust_concern",
                "How do I know this is legitimate?",
                "Fair question. You should review any paperwork with qualified title or legal professionals. I can keep the next step simple and provide a clear summary for manual review.",
                "medium",
            ),
        ]
        for objection_type, objection, response, risk_level in drafts:
            safety = validate_client_safe_text(response)
            existing.append(
                ClientObjectionResponseDraft(
                    id=f"client-objection-{uuid4().hex[:10]}",
                    workspace_id=lead.workspace_id,
                    lead_id=lead.id,
                    objection_type=objection_type,
                    seller_objection=objection,
                    suggested_response=response,
                    risk_level="high" if not safety["allowed"] else risk_level,
                    requires_human_review=not safety["allowed"] or risk_level != "low",
                    client_safe=bool(safety["allowed"]),
                    manual_use_only=True,
                )
            )
            session.add(existing[-1])
        _ensure_acquisition_event(session, lead, "objection_drafts", "Acquisition Manager prepared manual-use objection responses.")
        session.flush()
    return _objection_drafts(session, lead.workspace_id, lead.id)


def ensure_follow_up_drafts(
    session: Session,
    lead: ClientLeadProfile,
    refresh: bool = False,
) -> list[ClientFollowUpDraft]:
    existing = _follow_up_drafts(session, lead.workspace_id, lead.id)
    if refresh and existing:
        session.query(ClientFollowUpDraft).filter(ClientFollowUpDraft.lead_id == lead.id).delete(
            synchronize_session=False
        )
        existing = []
    if not existing:
        draft_values = [
            (
                "sms_draft",
                "Manual note: follow up about the property and ask whether the seller still wants to talk through options.",
                "simple seller check-in",
            ),
            (
                "email_draft",
                "Manual note: summarize the property questions, timeline, and next step for seller review.",
                "conversation recap",
            ),
            (
                "call_note",
                "Manual note: ask motivation, timeline, condition, price expectation, and decision-maker status before any offer review.",
                "call preparation",
            ),
        ]
        for channel_type, draft_body, purpose in draft_values:
            safety = validate_client_safe_text(draft_body)
            existing.append(
                ClientFollowUpDraft(
                    id=f"client-follow-up-{uuid4().hex[:10]}",
                    workspace_id=lead.workspace_id,
                    lead_id=lead.id,
                    channel_type=channel_type,
                    draft_body=draft_body,
                    purpose=purpose,
                    risk_level="high" if not safety["allowed"] else "low",
                    approval_status="needs_review" if not safety["allowed"] else "draft_only",
                    manual_use_only=True,
                    no_live_send=True,
                    unsafe_language_flag=not safety["allowed"],
                )
            )
            session.add(existing[-1])
        _ensure_acquisition_event(session, lead, "follow_up_drafts", "Acquisition Manager queued manual-use follow-up drafts.")
        session.flush()
    return _follow_up_drafts(session, lead.workspace_id, lead.id)


def ensure_appointment_readiness(
    session: Session,
    lead: ClientLeadProfile,
    refresh: bool = False,
) -> ClientAppointmentReadinessReview:
    score = ensure_score(session, lead)
    review = (
        session.query(ClientAppointmentReadinessReview)
        .filter(ClientAppointmentReadinessReview.lead_id == lead.id)
        .first()
    )
    if review is None:
        review = ClientAppointmentReadinessReview(
            id=f"client-appt-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
        )
        session.add(review)
    if refresh or review.readiness_score == 0:
        missing = _appointment_missing_requirements(lead, score)
        score_value = max(0, min(100, 100 - len(missing) * 14 - max(0, 70 - score.missing_data_score)))
        review.readiness_score = score_value
        review.appointment_ready = score_value >= 72 and not lead.dnc_flag
        review.missing_requirements = missing
        review.recommended_next_step = (
            "Use the manual call plan and confirm appointment logistics."
            if review.appointment_ready
            else "Complete missing seller context before appointment readiness."
        )
        review.reason_summary = f"{len(missing)} appointment requirements need review."
        review.confidence_level = "high" if score_value >= 80 else "medium" if score_value >= 55 else "low"
        review.requires_human_review = not review.appointment_ready or len(missing) > 0
        _ensure_acquisition_event(session, lead, "appointment_readiness", "Acquisition Manager reviewed appointment readiness.")
        session.flush()
    return review


def ensure_evidence_packet(
    session: Session,
    lead: ClientLeadProfile,
    refresh: bool = False,
) -> ClientDealEvidencePacket:
    packet = (
        session.query(ClientDealEvidencePacket)
        .filter(ClientDealEvidencePacket.lead_id == lead.id)
        .first()
    )
    if packet is None:
        packet = ClientDealEvidencePacket(
            id=f"client-evidence-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
        )
        session.add(packet)
    existing = _evidence_items(session, lead.workspace_id, lead.id, packet.id)
    if refresh and existing:
        session.query(ClientDealEvidenceItem).filter(ClientDealEvidenceItem.packet_id == packet.id).delete(
            synchronize_session=False
        )
        existing = []
    if not existing:
        for item in _default_evidence_items(lead):
            session.add(
                ClientDealEvidenceItem(
                    id=f"client-evidence-item-{uuid4().hex[:10]}",
                    workspace_id=lead.workspace_id,
                    lead_id=lead.id,
                    packet_id=packet.id,
                    **item,
                )
            )
    missing = _missing_evidence_types(_evidence_items(session, lead.workspace_id, lead.id, packet.id))
    packet.property_address = lead.property_address_summary
    packet.seller_motivation_summary = ", ".join(lead.motivation_signals or []) or "Seller motivation not confirmed."
    packet.property_condition_summary = _condition_summary(lead)
    packet.occupancy_status = "vacancy signal" if "vacant_signal" in (lead.distress_signals or []) else "occupancy not confirmed"
    packet.title_status_summary = "Title status not externally verified; client must use qualified review."
    packet.evidence_status = "ready_for_underwriting" if not missing else "missing_evidence"
    packet.missing_evidence_count = len(missing)
    packet.required_evidence_summary = missing
    packet.confidence_level = "high" if not missing else "medium" if len(missing) <= 2 else "low"
    packet.requires_human_review = bool(missing)
    packet.client_safe_summary = "Evidence packet uses manual/demo records only and does not call property, title, tax, or MLS providers."
    _ensure_underwriting_event(session, lead, "evidence_packet", "Underwriting Manager prepared a client-safe evidence packet.")
    session.flush()
    return packet


def ensure_underwriting_review(
    session: Session,
    lead: ClientLeadProfile,
    packet: ClientDealEvidencePacket,
    refresh: bool = False,
) -> ClientUnderwritingReview:
    review = (
        session.query(ClientUnderwritingReview)
        .filter(ClientUnderwritingReview.lead_id == lead.id)
        .first()
    )
    if review is None:
        review = ClientUnderwritingReview(
            id=f"client-underwriting-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
            packet_id=packet.id,
        )
        session.add(review)
    if refresh or (review.arv_estimate is None and review.repair_estimate is None):
        inputs = _manual_underwriting_inputs(lead)
        review.packet_id = packet.id
        review.arv_estimate = inputs.get("arv_estimate")
        review.repair_estimate = inputs.get("repair_estimate")
        review.holding_cost_estimate = inputs.get("holding_cost_estimate")
        review.desired_assignment_fee = inputs.get("desired_assignment_fee")
        missing = []
        if review.arv_estimate is None:
            missing.append("arv_estimate")
        if review.repair_estimate is None:
            missing.append("repair_estimate")
        if review.holding_cost_estimate is None:
            missing.append("holding_cost_estimate")
        if review.desired_assignment_fee is None:
            missing.append("desired_assignment_fee")
        review.missing_data_summary = missing
        if missing:
            review.max_allowable_offer = None
            review.conservative_offer = None
            review.standard_offer = None
            review.aggressive_offer = None
            review.margin_warning = True
            review.confidence_level = "low"
            review.assumptions_summary = "Missing underwriting inputs; no values are invented."
            review.requires_human_review = True
        else:
            mao = int(round((review.arv_estimate or 0) * 0.70 - (review.repair_estimate or 0) - (review.desired_assignment_fee or 0) - (review.holding_cost_estimate or 0)))
            review.max_allowable_offer = mao
            review.conservative_offer = int(round(mao * 0.90))
            review.standard_offer = mao
            review.aggressive_offer = int(round(mao * 1.05))
            review.margin_warning = mao <= 0 or packet.missing_evidence_count > 0
            review.confidence_level = "high" if not review.margin_warning and packet.confidence_level == "high" else "medium"
            review.assumptions_summary = (
                "Formula: ARV * 0.70 - repairs - desired assignment fee - holding costs. "
                "Inputs are manual/demo values and decision support only."
            )
            review.requires_human_review = review.margin_warning
        _sync_offer_scenarios(session, lead, review)
        _ensure_underwriting_event(session, lead, "underwriting_review", "Underwriting Manager completed deterministic offer math review.")
        session.flush()
    return review


def ensure_offer_readiness(
    session: Session,
    lead: ClientLeadProfile,
    packet: ClientDealEvidencePacket,
    review: ClientUnderwritingReview,
    refresh: bool = False,
) -> ClientOfferReadinessGate:
    gate = (
        session.query(ClientOfferReadinessGate)
        .filter(ClientOfferReadinessGate.lead_id == lead.id)
        .first()
    )
    if gate is None:
        gate = ClientOfferReadinessGate(
            id=f"client-offer-gate-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
            packet_id=packet.id,
        )
        session.add(gate)
    if refresh or not gate.recommended_next_step:
        block_reasons: list[str] = []
        risk_flags: list[str] = []
        if packet.missing_evidence_count > 0:
            block_reasons.append("evidence_missing")
        if review.arv_estimate is None:
            block_reasons.append("arv_estimate_missing")
        if review.repair_estimate is None:
            block_reasons.append("repair_estimate_missing")
        if review.max_allowable_offer is None:
            block_reasons.append("underwriting_review_needed")
        if review.max_allowable_offer is not None and review.max_allowable_offer <= 0:
            block_reasons.append("thin_or_negative_offer_margin")
        if lead.dnc_flag:
            risk_flags.append("do_not_contact")
        if lead.legal_question_flag:
            risk_flags.append("legal_review_needed")
        if review.margin_warning:
            risk_flags.append("margin_warning")

        gate.packet_id = packet.id
        gate.underwriting_review_id = review.id
        gate.block_reasons = block_reasons
        gate.risk_flags = risk_flags
        gate.readiness_score = max(0, 100 - len(block_reasons) * 22 - len(risk_flags) * 12)
        if block_reasons:
            gate.readiness_status = "evidence_missing" if "evidence_missing" in block_reasons else "underwriting_review_needed"
        elif risk_flags:
            gate.readiness_status = "blocked"
        else:
            gate.readiness_status = "ready_for_client_review"
        gate.can_present_offer = gate.readiness_status == "ready_for_client_review"
        gate.no_contract_generated = True
        gate.no_offer_sent = True
        gate.requires_human_review = True
        gate.recommended_next_step = (
            "Client can review the decision-support offer range manually."
            if gate.can_present_offer
            else "Resolve evidence, underwriting, or risk blockers before offer review."
        )
        _ensure_underwriting_event(session, lead, "offer_readiness", f"Underwriting Manager set offer readiness to {gate.readiness_status}.")
        session.flush()
    return gate


def require_member_permission(
    session: Session,
    workspace_id: str,
    member_email: str,
    permission: str,
) -> dict[str, object]:
    member = (
        session.query(ClientWorkspaceMember)
        .filter(
            ClientWorkspaceMember.workspace_id == workspace_id,
            ClientWorkspaceMember.member_email == member_email,
        )
        .first()
    )
    role = session.get(ClientWorkspaceRole, member.role_id) if member else None
    if not has_permission(member, role, permission):
        raise ClientCommandPermissionError("member_not_authorized_for_workspace")
    return {
        "member": member_public(member),
        "permissions": member_permissions(member, role),
    }


def _acquisition_objective(
    score: ClientLeadIntelligenceScore,
    missing: list[ClientLeadMissingDataItem],
) -> str:
    if score.recommended_next_action == "complete_missing_data" or missing:
        return "Confirm missing seller, property, and timeline facts before any offer discussion."
    if score.final_priority_score >= 75:
        return "Confirm motivation, timeline, condition, price expectation, and whether a manual appointment makes sense."
    return "Use a respectful discovery call to decide whether the lead should stay in the client queue."


def _question_summary(
    lead: ClientLeadProfile,
    missing: list[ClientLeadMissingDataItem],
) -> str:
    focus = [item.field_name for item in missing if item.resolution_status == "open"][:3]
    if focus:
        return f"Lead has missing data focus: {', '.join(focus)}."
    if lead.asking_price:
        return "Ask seller to explain timeline, property condition, and flexibility around the stated price expectation."
    return "Ask motivation, timeline, condition, price expectation, and decision-maker questions."


def _build_questions(
    lead: ClientLeadProfile,
    missing: list[ClientLeadMissingDataItem],
) -> list[dict[str, object]]:
    missing_fields_by_name = {item.field_name for item in missing if item.resolution_status == "open"}
    questions: list[dict[str, object]] = [
        {
            "question_text": "What has you thinking about selling this property now?",
            "question_category": "motivation",
            "priority": "high" if not lead.motivation_signals else "medium",
            "reason": "Motivation drives whether this lead belongs in the acquisition queue.",
            "tied_missing_data_key": "motivation_signals" if not lead.motivation_signals else None,
            "client_safe": True,
        },
        {
            "question_text": "Is there a specific timeline you are hoping to work around?",
            "question_category": "timeline",
            "priority": "high" if not lead.timeline_days or lead.timeline_days > 90 else "medium",
            "reason": "Timeline clarifies urgency without pressure.",
            "tied_missing_data_key": "timeline_days" if not lead.timeline_days else None,
            "client_safe": True,
        },
        {
            "question_text": "What condition is the property in today, and what repairs are you aware of?",
            "question_category": "condition",
            "priority": "high",
            "reason": "Condition is required before underwriting review.",
            "tied_missing_data_key": "property_condition" if "property_type" in missing_fields_by_name else None,
            "client_safe": True,
        },
        {
            "question_text": "Do you already have a price in mind, or are you looking for a clear as-is number?",
            "question_category": "price_expectation",
            "priority": "high" if not lead.asking_price else "medium",
            "reason": "Price expectation helps compare seller goals against underwriting inputs.",
            "tied_missing_data_key": "asking_price" if not lead.asking_price else None,
            "client_safe": True,
        },
        {
            "question_text": "Is the property currently occupied, vacant, or rented?",
            "question_category": "occupancy",
            "priority": "medium",
            "reason": "Occupancy affects access planning and client next steps.",
            "tied_missing_data_key": "occupancy_status",
            "client_safe": True,
        },
        {
            "question_text": "Are you the decision maker, or does anyone else need to review next steps with you?",
            "question_category": "decision_authority",
            "priority": "medium",
            "reason": "Decision authority reduces appointment and offer confusion.",
            "tied_missing_data_key": "decision_authority",
            "client_safe": True,
        },
        {
            "question_text": "Are there mortgage, lien, probate, or title questions that should be reviewed by qualified professionals?",
            "question_category": "mortgage_or_lien_context",
            "priority": "medium",
            "reason": "Title or legal questions should be routed to qualified review, not answered by the system.",
            "tied_missing_data_key": "title_status",
            "client_safe": True,
        },
    ]
    if "contact_channels_present" in missing_fields_by_name:
        questions.append(
            {
                "question_text": "What is the best way for you to receive a manual follow-up summary?",
                "question_category": "access_showing",
                "priority": "high",
                "reason": "Contactability is missing; no provider lookup is performed.",
                "tied_missing_data_key": "contact_channels_present",
                "client_safe": True,
            }
        )
    if "property_address_summary" in missing_fields_by_name:
        questions.append(
            {
                "question_text": "Can you confirm the property address before we review anything else?",
                "question_category": "access_showing",
                "priority": "high",
                "reason": "Property address is required for safe client review.",
                "tied_missing_data_key": "property_address_summary",
                "client_safe": True,
            }
        )
    return questions


def _appointment_missing_requirements(
    lead: ClientLeadProfile,
    score: ClientLeadIntelligenceScore,
) -> list[str]:
    missing: list[str] = []
    if not lead.motivation_signals:
        missing.append("seller_motivation")
    if not lead.contact_channels_present:
        missing.append("phone_or_email")
    if not lead.timeline_days or lead.timeline_days > 120:
        missing.append("timeline")
    if not lead.distress_signals and not lead.client_notes:
        missing.append("property_condition")
    if not lead.asking_price:
        missing.append("asking_price_or_expectation")
    if score.missing_data_score < 70:
        missing.append("cp2_missing_data_score")
    if lead.dnc_flag:
        missing.append("do_not_contact")
    return missing


def _default_evidence_items(lead: ClientLeadProfile) -> list[dict[str, object]]:
    if lead.id.startswith("client-lead-memphis-"):
        if lead.id == "client-lead-memphis-002":
            return [
                {
                    "item_type": "seller_note",
                    "item_summary": "High seller motivation is present, but ARV and repair evidence are still missing.",
                    "source_type": "manual",
                    "confidence_level": "medium",
                    "client_safe": True,
                    "internal_notes": "Memphis demo: keep evidence gap visible.",
                }
            ]
        return [
            {
                "item_type": item_type,
                "item_summary": "Memphis demo manual evidence item; no external provider call occurred.",
                "source_type": "manual",
                "confidence_level": "medium" if lead.id in {"client-lead-memphis-003", "client-lead-memphis-004"} else "high",
                "client_safe": True,
                "internal_notes": "Memphis demo support note.",
            }
            for item_type in ["seller_note", "repair_note", "comp_note", "occupancy_note", "title_note"]
        ]
    if lead.id == "client-lead-001":
        return [
            {
                "item_type": "seller_note",
                "item_summary": "Seller signals include absentee ownership, tired landlord context, and deferred-maintenance notes.",
                "source_type": "system_generated",
                "confidence_level": "high",
                "client_safe": True,
                "internal_notes": "Source: CP demo lead profile.",
            },
            {
                "item_type": "repair_note",
                "item_summary": "Manual demo repair note assumes visible deferred maintenance requires client review.",
                "source_type": "manual",
                "confidence_level": "medium",
                "client_safe": True,
                "internal_notes": "Internal estimate support hidden from client payload.",
            },
            {
                "item_type": "comp_note",
                "item_summary": "Manual comp note supports using the imported estimated value as a placeholder for review.",
                "source_type": "manual",
                "confidence_level": "medium",
                "client_safe": True,
                "internal_notes": "No live comp provider was called.",
            },
            {
                "item_type": "occupancy_note",
                "item_summary": "Vacancy signal requires seller confirmation before appointment planning.",
                "source_type": "system_generated",
                "confidence_level": "medium",
                "client_safe": True,
                "internal_notes": "Distress signal only.",
            },
            {
                "item_type": "title_note",
                "item_summary": "Title status is not verified; external review is required for any real file.",
                "source_type": "manual",
                "confidence_level": "low",
                "client_safe": True,
                "internal_notes": "Review reminder only.",
            },
        ]
    if lead.id == "client-lead-002":
        return [
            {
                "item_type": "seller_note",
                "item_summary": "Inherited/out-of-area signals are present, but property condition and valuation support are incomplete.",
                "source_type": "system_generated",
                "confidence_level": "medium",
                "client_safe": True,
                "internal_notes": "Needs manual data.",
            },
            {
                "item_type": "title_note",
                "item_summary": "Probate context needs external title or attorney review before any real paperwork.",
                "source_type": "manual",
                "confidence_level": "low",
                "client_safe": True,
                "internal_notes": "Review reminder only.",
            },
        ]
    if lead.id == "client-lead-004":
        return [
            {
                "item_type": "seller_note",
                "item_summary": "High-equity signal exists, but distress and seller motivation evidence are weak.",
                "source_type": "system_generated",
                "confidence_level": "low",
                "client_safe": True,
                "internal_notes": "Cross-workspace demo lead.",
            },
            {
                "item_type": "repair_note",
                "item_summary": "Manual review note expects high repair sensitivity and thin offer margin.",
                "source_type": "manual",
                "confidence_level": "low",
                "client_safe": True,
                "internal_notes": "Blocked example support.",
            },
            {
                "item_type": "comp_note",
                "item_summary": "Estimated value is a placeholder only and needs verification before client review.",
                "source_type": "manual",
                "confidence_level": "low",
                "client_safe": True,
                "internal_notes": "No live comp provider was called.",
            },
        ]
    return [
        {
            "item_type": "manual_note",
            "item_summary": "Lead requires manual evidence before underwriting can be reviewed.",
            "source_type": "system_generated",
            "confidence_level": "low",
            "client_safe": True,
            "internal_notes": "Incomplete demo lead.",
        }
    ]


def _missing_evidence_types(items: list[ClientDealEvidenceItem]) -> list[str]:
    present = {item.item_type for item in items}
    required = ["seller_note", "repair_note", "comp_note", "occupancy_note", "title_note"]
    return [item_type for item_type in required if item_type not in present]


def _condition_summary(lead: ClientLeadProfile) -> str:
    if "deferred_maintenance" in (lead.motivation_signals or []) or "property_condition_unknown" in (lead.distress_signals or []):
        return "Condition needs seller confirmation and repair evidence before final review."
    if lead.distress_signals:
        return f"Distress signals: {', '.join(lead.distress_signals)}."
    return "No condition evidence recorded yet."


def _manual_underwriting_inputs(lead: ClientLeadProfile) -> dict[str, int | None]:
    inputs: dict[str, dict[str, int | None]] = {
        "client-lead-001": {
            "arv_estimate": 238000,
            "repair_estimate": 42000,
            "holding_cost_estimate": 8000,
            "desired_assignment_fee": 10000,
        },
        "client-lead-004": {
            "arv_estimate": 210000,
            "repair_estimate": 120000,
            "holding_cost_estimate": 8000,
            "desired_assignment_fee": 10000,
        },
        "client-lead-memphis-001": {
            "arv_estimate": 165000,
            "repair_estimate": 32000,
            "holding_cost_estimate": 6000,
            "desired_assignment_fee": 10000,
        },
        "client-lead-memphis-003": {
            "arv_estimate": 210000,
            "repair_estimate": 36000,
            "holding_cost_estimate": 7000,
            "desired_assignment_fee": 10000,
        },
        "client-lead-memphis-004": {
            "arv_estimate": 135000,
            "repair_estimate": 76000,
            "holding_cost_estimate": 7000,
            "desired_assignment_fee": 10000,
        },
        "client-lead-memphis-005": {
            "arv_estimate": 240000,
            "repair_estimate": 50000,
            "holding_cost_estimate": 9000,
            "desired_assignment_fee": 15000,
        },
    }
    return inputs.get(
        lead.id,
        {
            "arv_estimate": None,
            "repair_estimate": None,
            "holding_cost_estimate": None,
            "desired_assignment_fee": 10000,
        },
    )


def _sync_offer_scenarios(
    session: Session,
    lead: ClientLeadProfile,
    review: ClientUnderwritingReview,
) -> None:
    session.query(ClientOfferScenario).filter(
        ClientOfferScenario.underwriting_review_id == review.id
    ).delete(synchronize_session=False)
    if review.max_allowable_offer is None:
        return
    scenario_values = [
        ("conservative", review.conservative_offer, "low"),
        ("standard", review.standard_offer, "medium"),
        ("aggressive", review.aggressive_offer, "high"),
    ]
    for name, amount, risk_level in scenario_values:
        amount_value = int(amount or 0)
        session.add(
            ClientOfferScenario(
                id=f"client-scenario-{uuid4().hex[:10]}",
                workspace_id=lead.workspace_id,
                lead_id=lead.id,
                underwriting_review_id=review.id,
                scenario_name=name,
                offer_amount=amount_value,
                projected_margin=max(0, int((review.max_allowable_offer or 0) - amount_value)),
                assumptions="Decision-support scenario from manual underwriting inputs only.",
                risk_level=risk_level if amount_value > 0 else "high",
                client_safe_explanation="No offer has been sent and no contract has been generated.",
            )
        )


def _ensure_acquisition_event(
    session: Session,
    lead: ClientLeadProfile,
    event_type: str,
    summary: str,
) -> None:
    event = (
        session.query(ClientAcquisitionDivisionEvent)
        .filter(
            ClientAcquisitionDivisionEvent.lead_id == lead.id,
            ClientAcquisitionDivisionEvent.event_type == event_type,
        )
        .first()
    )
    if event is None:
        event = ClientAcquisitionDivisionEvent(
            id=f"client-acq-event-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
            event_type=event_type,
        )
        session.add(event)
    event.event_summary = summary
    event.manager_name = "Acquisition Manager"
    event.client_visible = True


def _ensure_underwriting_event(
    session: Session,
    lead: ClientLeadProfile,
    event_type: str,
    summary: str,
) -> None:
    event = (
        session.query(ClientUnderwritingDivisionEvent)
        .filter(
            ClientUnderwritingDivisionEvent.lead_id == lead.id,
            ClientUnderwritingDivisionEvent.event_type == event_type,
        )
        .first()
    )
    if event is None:
        event = ClientUnderwritingDivisionEvent(
            id=f"client-underwriting-event-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
            event_type=event_type,
        )
        session.add(event)
    event.event_summary = summary
    event.manager_name = "Underwriting Manager"
    event.client_visible = True


def _workspace_or_404(session: Session, workspace_id: str) -> ClientWorkspace:
    workspace = session.get(ClientWorkspace, workspace_id)
    if workspace is None:
        raise ValueError(f"Client workspace not found: {workspace_id}")
    return workspace


def _lead_or_404(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
) -> ClientLeadProfile:
    query = session.query(ClientLeadProfile).filter(ClientLeadProfile.id == lead_id)
    if workspace_id is not None:
        query = query.filter(ClientLeadProfile.workspace_id == workspace_id)
    lead = query.first()
    if lead is None:
        raise ValueError(f"Client lead not found in requested workspace: {lead_id}")
    return lead


def _scores_for_workspace(session: Session, workspace_id: str) -> list[ClientLeadIntelligenceScore]:
    return (
        session.query(ClientLeadIntelligenceScore)
        .filter(ClientLeadIntelligenceScore.workspace_id == workspace_id)
        .all()
    )


def _missing_items(
    session: Session,
    workspace_id: str,
    lead_id: str,
) -> list[ClientLeadMissingDataItem]:
    return (
        session.query(ClientLeadMissingDataItem)
        .filter(
            ClientLeadMissingDataItem.workspace_id == workspace_id,
            ClientLeadMissingDataItem.lead_id == lead_id,
        )
        .order_by(ClientLeadMissingDataItem.severity.desc(), ClientLeadMissingDataItem.field_name)
        .all()
    )


def _next_actions(
    session: Session,
    workspace_id: str,
    lead_id: str,
) -> list[ClientLeadNextBestAction]:
    return (
        session.query(ClientLeadNextBestAction)
        .filter(
            ClientLeadNextBestAction.workspace_id == workspace_id,
            ClientLeadNextBestAction.lead_id == lead_id,
        )
        .order_by(desc(ClientLeadNextBestAction.priority))
        .all()
    )


def _division_events(
    session: Session,
    workspace_id: str,
    lead_id: str,
) -> list[ClientLeadDivisionEvent]:
    return (
        session.query(ClientLeadDivisionEvent)
        .filter(
            ClientLeadDivisionEvent.workspace_id == workspace_id,
            ClientLeadDivisionEvent.lead_id == lead_id,
        )
        .order_by(desc(ClientLeadDivisionEvent.created_at))
        .all()
    )


def _seller_questions(
    session: Session,
    workspace_id: str,
    lead_id: str,
    question_plan_id: str,
) -> list[ClientSellerQuestion]:
    return (
        session.query(ClientSellerQuestion)
        .filter(
            ClientSellerQuestion.workspace_id == workspace_id,
            ClientSellerQuestion.lead_id == lead_id,
            ClientSellerQuestion.question_plan_id == question_plan_id,
        )
        .order_by(ClientSellerQuestion.priority.desc(), ClientSellerQuestion.question_category)
        .all()
    )


def _objection_drafts(
    session: Session,
    workspace_id: str,
    lead_id: str,
) -> list[ClientObjectionResponseDraft]:
    return (
        session.query(ClientObjectionResponseDraft)
        .filter(
            ClientObjectionResponseDraft.workspace_id == workspace_id,
            ClientObjectionResponseDraft.lead_id == lead_id,
        )
        .order_by(ClientObjectionResponseDraft.objection_type)
        .all()
    )


def _follow_up_drafts(
    session: Session,
    workspace_id: str,
    lead_id: str,
) -> list[ClientFollowUpDraft]:
    return (
        session.query(ClientFollowUpDraft)
        .filter(
            ClientFollowUpDraft.workspace_id == workspace_id,
            ClientFollowUpDraft.lead_id == lead_id,
        )
        .order_by(ClientFollowUpDraft.channel_type)
        .all()
    )


def _acquisition_events(
    session: Session,
    workspace_id: str,
    lead_id: str,
) -> list[ClientAcquisitionDivisionEvent]:
    return (
        session.query(ClientAcquisitionDivisionEvent)
        .filter(
            ClientAcquisitionDivisionEvent.workspace_id == workspace_id,
            ClientAcquisitionDivisionEvent.lead_id == lead_id,
        )
        .order_by(desc(ClientAcquisitionDivisionEvent.created_at))
        .all()
    )


def _evidence_items(
    session: Session,
    workspace_id: str,
    lead_id: str,
    packet_id: str,
) -> list[ClientDealEvidenceItem]:
    return (
        session.query(ClientDealEvidenceItem)
        .filter(
            ClientDealEvidenceItem.workspace_id == workspace_id,
            ClientDealEvidenceItem.lead_id == lead_id,
            ClientDealEvidenceItem.packet_id == packet_id,
        )
        .order_by(ClientDealEvidenceItem.item_type)
        .all()
    )


def _offer_scenarios(
    session: Session,
    workspace_id: str,
    lead_id: str,
    underwriting_review_id: str,
) -> list[ClientOfferScenario]:
    return (
        session.query(ClientOfferScenario)
        .filter(
            ClientOfferScenario.workspace_id == workspace_id,
            ClientOfferScenario.lead_id == lead_id,
            ClientOfferScenario.underwriting_review_id == underwriting_review_id,
        )
        .order_by(ClientOfferScenario.scenario_name)
        .all()
    )


def _underwriting_events(
    session: Session,
    workspace_id: str,
    lead_id: str,
) -> list[ClientUnderwritingDivisionEvent]:
    return (
        session.query(ClientUnderwritingDivisionEvent)
        .filter(
            ClientUnderwritingDivisionEvent.workspace_id == workspace_id,
            ClientUnderwritingDivisionEvent.lead_id == lead_id,
        )
        .order_by(desc(ClientUnderwritingDivisionEvent.created_at))
        .all()
    )


def _sync_missing_items(
    session: Session,
    lead: ClientLeadProfile,
    fields: list[str],
) -> None:
    existing = {
        item.field_name: item
        for item in _missing_items(session, lead.workspace_id, lead.id)
    }
    for field in fields:
        if field not in existing:
            session.add(
                ClientLeadMissingDataItem(
                    id=f"client-missing-{uuid4().hex[:10]}",
                    workspace_id=lead.workspace_id,
                    lead_id=lead.id,
                    field_name=field,
                    reason=f"{field} is required before this lead is ready for client action.",
                    severity="high" if field in {"property_address_summary", "contact_channels_present"} else "medium",
                    blocks_readiness=True,
                )
            )
        else:
            existing[field].resolution_status = "open"
    for field, item in existing.items():
        if field not in fields:
            item.resolution_status = "resolved"
            item.blocks_readiness = False


def _ensure_next_action(
    session: Session,
    lead: ClientLeadProfile,
    score: ClientLeadIntelligenceScore,
) -> ClientLeadNextBestAction:
    action = (
        session.query(ClientLeadNextBestAction)
        .filter(ClientLeadNextBestAction.lead_id == lead.id)
        .first()
    )
    if action is None:
        action = ClientLeadNextBestAction(
            id=f"client-action-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
        )
        session.add(action)
    action.action_type = score.recommended_next_action
    action.action_label = _action_label(score.recommended_next_action)
    action.reason = score.reason_summary
    action.priority = score.final_priority_score
    action.status = "owner_review" if score.requires_human_review else "open"
    action.confidence_level = score.confidence_level
    action.requires_human_review = score.requires_human_review
    action.outbound_action_allowed = False
    action.provider_action_allowed = False
    action.client_safe = True
    return action


def _ensure_division_event(
    session: Session,
    lead: ClientLeadProfile,
    score: ClientLeadIntelligenceScore,
) -> None:
    event = (
        session.query(ClientLeadDivisionEvent)
        .filter(
            ClientLeadDivisionEvent.lead_id == lead.id,
            ClientLeadDivisionEvent.event_type == "lead_intelligence_score",
        )
        .first()
    )
    if event is None:
        event = ClientLeadDivisionEvent(
            id=f"client-event-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
            event_type="lead_intelligence_score",
        )
        session.add(event)
    event.division_name = "Lead Intelligence Division"
    event.manager_status = "human_review" if score.requires_human_review else "client_safe_queue"
    event.event_summary = f"Lead Intelligence Manager scored priority {score.final_priority_score} with {score.confidence_level} confidence."
    event.safe_for_client = True
    event.internal_prime_governance_visible = False
    event.raw_provider_payload_exposed = False


def _action_label(action_type: str) -> str:
    labels = {
        "human_review_required": "Review before any client action",
        "complete_missing_data": "Complete missing lead data",
        "owner_review_hot_lead": "Review hot lead with client-safe notes",
        "research_and_prepare_call_plan": "Research and prepare a call plan",
        "nurture_or_skip_for_now": "Nurture or skip for now",
        "manual_acquisition_ready": "Use acquisition brief for manual seller prep",
        "collect_repair_arv_evidence": "Collect repair and ARV evidence",
        "validate_buyer_demand_before_matching": "Validate buyer demand before matching",
        "hold_due_to_thin_offer_margin": "Hold until margin improves or evidence changes",
        "ready_for_buyer_matching_cp5": "Ready for buyer matching review",
    }
    return labels.get(action_type, "Review next best action")
