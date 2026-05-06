from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.domain.field_testing import apply_call_outcome, outreach_eligibility_for_lead
from app.domains.mobile_operator.safety import mobile_approval_gate, mobile_capture_safety
from app.domains.mobile_operator.sanitizer import sanitize_mobile_record
from app.models import (
    Buyer,
    Deal,
    DocumentIntelligenceFile,
    FieldCallOutcome,
    Lead,
    MobileApprovalAttempt,
    MobileOfflineDraft,
    MobileOperatorNote,
    OwnerApprovalItem,
)
from app.serializers import model_to_dict


def _source_present(session: Session, source_record_type: str, source_record_id: str) -> bool:
    model_by_type = {
        "lead": Lead,
        "deal": Deal,
        "owner_approval": OwnerApprovalItem,
        "field_call_outcome": FieldCallOutcome,
        "document": DocumentIntelligenceFile,
    }
    model = model_by_type.get(source_record_type)
    return bool(source_record_id and (model is None or session.get(model, source_record_id) is not None))


def _lead_card(lead: Lead) -> dict[str, object]:
    return {
        "id": lead.id,
        "seller_name": lead.seller_name,
        "property": f"{lead.address}, {lead.city}, {lead.state} {lead.zip_code}",
        "stage": lead.stage,
        "opportunity_score": lead.opportunity_score,
        "motivation_score": lead.motivation_score,
        "contactability_score": lead.contactability_score,
        "next_best_action": lead.next_best_action,
    }


def _deal_card(deal: Deal) -> dict[str, object]:
    buyer_margin = (
        deal.arv - deal.repairs - deal.buyer_costs - deal.buyer_purchase_price
    )
    return {
        "id": deal.id,
        "status": deal.status,
        "projected_assignment_fee": deal.projected_assignment_fee,
        "buyer_margin": buyer_margin,
        "risk_score": deal.risk_score,
        "hot": deal.is_hot_opportunity,
        "under_contract": deal.is_under_contract,
        "next_action": "Review mobile-safe owner queue; no field execution from mobile.",
    }


def mobile_overview(session: Session) -> dict[str, object]:
    leads = session.query(Lead).order_by(desc(Lead.opportunity_score)).limit(10).all()
    deals = session.query(Deal).order_by(desc(Deal.projected_assignment_fee)).limit(10).all()
    approvals = (
        session.query(OwnerApprovalItem)
        .filter(OwnerApprovalItem.approval_status == "pending_owner")
        .order_by(desc(OwnerApprovalItem.high_risk_action), OwnerApprovalItem.created_at)
        .limit(10)
        .all()
    )
    call_outcomes = (
        session.query(FieldCallOutcome)
        .order_by(desc(FieldCallOutcome.call_datetime))
        .limit(10)
        .all()
    )
    notes = (
        session.query(MobileOperatorNote)
        .order_by(desc(MobileOperatorNote.created_at))
        .limit(10)
        .all()
    )
    return {
        "top_money_actions_today": [_deal_card(deal) for deal in deals[:5]],
        "top_risk_actions_today": [
            _deal_card(deal) for deal in sorted(deals, key=lambda item: item.risk_score, reverse=True)[:5]
        ],
        "call_queue": [_lead_card(lead) for lead in leads],
        "approval_queue": [model_to_dict(item) for item in approvals],
        "recent_call_outcomes": [model_to_dict(outcome) for outcome in call_outcomes],
        "recent_mobile_notes": [sanitize_mobile_record(note) for note in notes],
        "field_briefing": field_briefing(session),
        "mobile_safety": {
            "field_capture_only": True,
            "live_outreach_from_mobile_allowed": False,
            "contract_execution_allowed": False,
            "portal_publish_allowed": False,
        },
    }


def today_actions(session: Session) -> dict[str, object]:
    overview = mobile_overview(session)
    return {
        "top_money_actions_today": overview["top_money_actions_today"],
        "top_risk_actions_today": overview["top_risk_actions_today"],
        "next_best_owner_focus": "Work approvals, call outcomes, DNC marks, and evidence gaps from mobile.",
    }


def call_queue(session: Session) -> dict[str, object]:
    leads = session.query(Lead).order_by(desc(Lead.opportunity_score)).limit(15).all()
    return {
        "call_queue": [
            {**_lead_card(lead), "outreach_eligibility": outreach_eligibility_for_lead(session, lead.id)}
            for lead in leads
        ],
        "system_calling_enabled": False,
    }


def lead_detail(session: Session, lead_id: str) -> dict[str, object]:
    lead = session.get(Lead, lead_id)
    if lead is None:
        raise ValueError(f"Lead not found: {lead_id}")
    outcomes = (
        session.query(FieldCallOutcome)
        .filter(FieldCallOutcome.lead_id == lead_id)
        .order_by(desc(FieldCallOutcome.call_datetime))
        .all()
    )
    return {
        "lead": model_to_dict(lead),
        "outreach_eligibility": outreach_eligibility_for_lead(session, lead_id),
        "call_outcomes": [model_to_dict(outcome) for outcome in outcomes],
        "quick_actions": {
            "note_capture_only": True,
            "dnc_mark_available": True,
            "live_outreach_allowed": False,
        },
    }


def deal_detail(session: Session, deal_id: str) -> dict[str, object]:
    deal = session.get(Deal, deal_id)
    if deal is None:
        raise ValueError(f"Deal not found: {deal_id}")
    lead = session.get(Lead, deal.lead_id)
    return {
        "deal": model_to_dict(deal),
        "lead_summary": model_to_dict(lead) if lead else None,
        "mobile_safety": {
            "numbers_source": "system_records_only",
            "no_terms_changed_from_mobile": True,
            "no_contract_execution": True,
        },
    }


def approval_queue(session: Session) -> dict[str, object]:
    approvals = (
        session.query(OwnerApprovalItem)
        .filter(OwnerApprovalItem.approval_status == "pending_owner")
        .order_by(desc(OwnerApprovalItem.ready_for_approval), desc(OwnerApprovalItem.high_risk_action))
        .all()
    )
    attempts = (
        session.query(MobileApprovalAttempt)
        .order_by(desc(MobileApprovalAttempt.created_at))
        .all()
    )
    return {
        "approval_queue": [model_to_dict(item) for item in approvals],
        "mobile_gate_attempts": [sanitize_mobile_record(attempt) for attempt in attempts],
        "quick_approval_cannot_execute": True,
    }


def field_briefing(session: Session) -> dict[str, object]:
    call_outcomes = session.query(FieldCallOutcome).all()
    dnc_count = len([outcome for outcome in call_outcomes if outcome.do_not_contact])
    motivated = [
        outcome
        for outcome in call_outcomes
        if outcome.contact_result in {"motivated", "offer_requested", "appointment_set"}
    ]
    return {
        "recent_imported_leads": session.query(Lead).filter(Lead.id.like("real-lead-%")).count(),
        "call_outcomes_recorded": len(call_outcomes),
        "motivated_sellers_found": len(motivated),
        "do_not_contact_records": dnc_count,
        "field_capture_mode": "offline_safe_draft_capture",
        "next_best_action": "Review call queue, add field notes, mark DNC when needed, and work owner approvals.",
    }


def buyers_snapshot(session: Session) -> dict[str, object]:
    buyers = session.query(Buyer).order_by(desc(Buyer.reliability_score)).all()
    return {
        "buyers": [model_to_dict(buyer) for buyer in buyers],
        "mobile_contact_enabled": False,
        "buyer_response_note_capture_only": True,
    }


def documents_snapshot(session: Session) -> dict[str, object]:
    documents = (
        session.query(DocumentIntelligenceFile)
        .order_by(desc(DocumentIntelligenceFile.created_at))
        .all()
    )
    return {
        "documents": [model_to_dict(document) for document in documents],
        "photo_metadata_placeholder_only": True,
        "portal_publish_allowed": False,
    }


def capture_mobile_note(session: Session, request) -> dict[str, object]:
    safety = mobile_capture_safety(request.body)
    note = MobileOperatorNote(
        id=f"mobile-note-{uuid4().hex[:10]}",
        note_type=request.note_type,
        source_record_type=request.source_record_type,
        source_record_id=request.source_record_id,
        body=request.body,
        offline_created=request.offline_created,
        sync_status="pending_sync" if request.offline_created else "synced",
        safety_status="safe_capture" if safety["allowed"] else "needs_owner_review",
        blocked_reasons=list(safety["blocked_reasons"]),
    )
    session.add(note)
    session.commit()
    return {**sanitize_mobile_record(note), "safety": safety}


def quick_call_outcome(session: Session, request) -> dict[str, object]:
    lead = session.get(Lead, request.lead_id)
    if lead is None:
        raise ValueError(f"Lead not found: {request.lead_id}")
    outcome = FieldCallOutcome(
        id=f"mobile-call-{uuid4().hex[:10]}",
        lead_id=request.lead_id,
        call_datetime=datetime.now(UTC),
        contact_result=request.contact_result,
        motivation_notes=request.motivation_notes,
        asking_price=request.asking_price,
        timeline=request.timeline,
        property_condition_notes=request.property_condition_notes,
        seller_objections=request.seller_objections,
        seller_temperature=request.seller_temperature,
        next_follow_up_date=request.next_follow_up_date,
        operator_notes=request.operator_notes or "Mobile field outcome capture only.",
        prime2_next_recommendation="Prime 2 will route internally after owner review.",
    )
    session.add(outcome)
    session.flush()
    apply_call_outcome(session, outcome)
    session.commit()
    return {
        "call_outcome": model_to_dict(outcome),
        "lead": model_to_dict(outcome.lead),
        "live_call_recorded": False,
        "live_outreach_allowed": False,
    }


def quick_dnc_mark(session: Session, request) -> dict[str, object]:
    return quick_call_outcome(
        session,
        type(
            "MobileDncRequest",
            (),
            {
                "lead_id": request.lead_id,
                "contact_result": "do_not_contact",
                "motivation_notes": request.notes,
                "asking_price": None,
                "timeline": "",
                "property_condition_notes": "",
                "seller_objections": ["do_not_contact"],
                "seller_temperature": 0,
                "next_follow_up_date": None,
                "operator_notes": "Mobile DNC mark; future live outreach eligibility blocked.",
            },
        )(),
    )


def sync_offline_draft(session: Session, request) -> dict[str, object]:
    existing = (
        session.query(MobileOfflineDraft)
        .filter(MobileOfflineDraft.idempotency_key == request.idempotency_key)
        .one_or_none()
    )
    if existing is not None:
        return {
            **sanitize_mobile_record(existing),
            "idempotent_replay": True,
            "action_executed": False,
        }
    draft = MobileOfflineDraft(
        id=f"mobile-draft-{uuid4().hex[:10]}",
        draft_type=request.draft_type,
        source_record_type=request.source_record_type,
        source_record_id=request.source_record_id,
        payload=request.payload,
        idempotency_key=request.idempotency_key,
        sync_status="captured_for_owner_review",
    )
    session.add(draft)
    session.commit()
    return {
        **sanitize_mobile_record(draft),
        "idempotent_replay": False,
        "action_executed": False,
    }


def quick_approval_check(session: Session, request) -> dict[str, object]:
    existing = (
        session.query(MobileApprovalAttempt)
        .filter(MobileApprovalAttempt.idempotency_key == request.idempotency_key)
        .one_or_none()
    )
    if existing is not None:
        return {
            **sanitize_mobile_record(existing),
            "idempotent_replay": True,
            "duplicate_action_prevented": True,
        }
    source_present = _source_present(session, request.source_record_type, request.source_record_id)
    gate = mobile_approval_gate(
        source_record_present=source_present,
        safety_status=request.safety_status,
        dry_run_receipt_id=request.dry_run_receipt_id,
        provider_readiness_status=request.provider_readiness_status,
        idempotency_key=request.idempotency_key,
        owner_approval_recorded=request.owner_approval_recorded,
    )
    attempt = MobileApprovalAttempt(
        id=f"mobile-approval-{uuid4().hex[:10]}",
        approval_type=request.approval_type,
        source_record_type=request.source_record_type,
        source_record_id=request.source_record_id,
        approval_status="ready_for_owner_review"
        if gate["allowed_for_owner_review"]
        else "blocked",
        safety_status=request.safety_status,
        dry_run_receipt_id=request.dry_run_receipt_id,
        provider_readiness_status=request.provider_readiness_status,
        idempotency_key=request.idempotency_key,
        owner_approval_recorded=request.owner_approval_recorded,
        source_record_present=source_present,
        blocked_reasons=list(gate["blocked_reasons"]),
        approved=False,
        live_action_allowed=False,
    )
    session.add(attempt)
    session.commit()
    return {**sanitize_mobile_record(attempt), "gate": gate}
