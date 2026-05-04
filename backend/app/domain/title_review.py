from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.offer_conversion import sync_contract_ready_state
from app.models import ReviewPacketPrep, TitleReviewCoordination
from app.serializers import model_to_dict


TITLE_REVIEW_UNSAFE_PATTERNS = {
    "legal_advice": [
        "this is legal advice",
        "you are legally required",
        "no attorney needed",
        "ignore title",
    ],
    "contract_execution": [
        "execute this contract",
        "ready to sign contract",
        "binding contract",
        "final legal contract",
    ],
    "document_submission": [
        "submit documents",
        "submit to title",
        "send documents to title",
        "open escrow now",
    ],
    "title_company_email_send": [
        "email title company",
        "send to title company",
        "send title email",
    ],
    "attorney_client_relationship_claim": [
        "we are your attorney",
        "attorney-client relationship",
        "our lawyer represents you",
    ],
    "closing_guarantee": [
        "guaranteed close",
        "guaranteed closing",
        "will definitely close",
    ],
}


def validate_title_review_language(content: str) -> dict[str, object]:
    text = content.lower()
    flags = sorted(
        {
            category
            for category, phrases in TITLE_REVIEW_UNSAFE_PATTERNS.items()
            if any(phrase in text for phrase in phrases)
        }
    )
    return {
        "allowed": not flags,
        "blocked": bool(flags),
        "risk_flags": flags,
        "legal_advice_blocked": "legal_advice" in flags,
        "contract_execution_blocked": "contract_execution" in flags,
        "document_submission_blocked": "document_submission" in flags,
        "title_company_email_send_blocked": "title_company_email_send" in flags,
        "attorney_client_relationship_claim_blocked": (
            "attorney_client_relationship_claim" in flags
        ),
        "closing_guarantee_blocked": "closing_guarantee" in flags,
    }


def title_review_gate(record: TitleReviewCoordination) -> dict[str, object]:
    state = record.contract_ready_state
    if state is not None:
        sync_contract_ready_state(state)
    negotiation = state.negotiation_record if state is not None else None
    reasons: list[str] = []

    if state is None or not state.contract_ready:
        reasons.append("v10_contract_ready_not_cleared")
    if state is None or not state.compliance_passed:
        reasons.append("compliance_not_passed")
    if (
        state is None
        or not state.owner_approval_recorded
        or record.owner_approval_status != "approved"
    ):
        reasons.append("owner_approval_not_recorded")
    if state is None or not state.numbers_locked:
        reasons.append("numbers_not_locked")
    if (
        negotiation is None
        or negotiation.readiness_level not in {"high readiness", "contract-ready"}
    ):
        reasons.append("seller_acceptance_readiness_not_high")
    if record.legal_advice_allowed:
        reasons.append("legal_advice_enabled")
    if record.contract_execution_allowed:
        reasons.append("contract_execution_enabled")
    if record.document_submission_allowed:
        reasons.append("document_submission_enabled")
    if record.title_company_email_send_allowed:
        reasons.append("title_company_email_send_enabled")
    if record.attorney_client_relationship_claimed:
        reasons.append("attorney_client_relationship_claimed")
    if record.closing_guarantee_allowed:
        reasons.append("closing_guarantee_enabled")

    return {
        "can_prepare_review_packet": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "v10_contract_ready": bool(state and state.contract_ready),
        "compliance_passed": bool(state and state.compliance_passed),
        "owner_approval_recorded": bool(
            state and state.owner_approval_recorded and record.owner_approval_status == "approved"
        ),
        "numbers_locked": bool(state and state.numbers_locked),
        "seller_acceptance_readiness": negotiation.readiness_level if negotiation else "missing",
        "draft_only": True,
        "legal_advice_allowed": False,
        "contract_execution_allowed": False,
        "document_submission_allowed": False,
        "title_company_email_send_allowed": False,
    }


def sync_title_review_coordination(record: TitleReviewCoordination) -> dict[str, object]:
    gate = title_review_gate(record)
    record.packet_prep_allowed = bool(gate["can_prepare_review_packet"])
    record.blocked_reasons = gate["blocked_reasons"]
    record.attorney_title_review_status = (
        "packet_ready" if record.packet_prep_allowed else "blocked"
    )
    record.draft_only = True
    record.legal_advice_allowed = False
    record.contract_execution_allowed = False
    record.document_submission_allowed = False
    record.title_company_email_send_allowed = False
    record.attorney_client_relationship_claimed = False
    record.closing_guarantee_allowed = False
    return gate


def sync_review_packet_prep(packet: ReviewPacketPrep) -> dict[str, object]:
    gate = sync_title_review_coordination(packet.title_review_coordination)
    packet.prep_allowed = bool(gate["can_prepare_review_packet"])
    packet.blocked_reasons = gate["blocked_reasons"]
    packet.packet_status = "draft_ready" if packet.prep_allowed else "blocked"
    packet.draft_only = True
    packet.legal_advice_allowed = False
    packet.contract_execution_allowed = False
    packet.document_submission_allowed = False
    packet.title_company_email_send_allowed = False
    packet.submitted_to_title = False
    packet.attorney_client_relationship_claimed = False
    packet.closing_guarantee_allowed = False
    return gate


def title_review_coordination_summary(record: TitleReviewCoordination) -> dict[str, object]:
    gate = sync_title_review_coordination(record)
    return {
        **model_to_dict(record),
        "gate": gate,
        "review_packet_prep_allowed": gate["can_prepare_review_packet"],
        "contract_execution_allowed": False,
        "document_submission_allowed": False,
        "title_company_email_send_allowed": False,
        "legal_advice_allowed": False,
    }


def review_packet_prep_summary(packet: ReviewPacketPrep) -> dict[str, object]:
    gate = sync_review_packet_prep(packet)
    return {
        **model_to_dict(packet),
        "gate": gate,
        "review_packet_note": "Draft-only title/attorney review packet; no document submission, email send, legal advice, or contract execution.",
        "contract_execution_allowed": False,
        "document_submission_allowed": False,
        "title_company_email_send_allowed": False,
        "legal_advice_allowed": False,
        "submitted_to_title": False,
    }


def title_review_dashboard(session: Session) -> dict[str, object]:
    records = session.query(TitleReviewCoordination).all()
    packets = session.query(ReviewPacketPrep).all()
    for record in records:
        sync_title_review_coordination(record)
    for packet in packets:
        sync_review_packet_prep(packet)

    return {
        "title_review_records": [
            title_review_coordination_summary(record) for record in records
        ],
        "review_packet_preps": [review_packet_prep_summary(packet) for packet in packets],
        "packet_prep_ready": [
            review_packet_prep_summary(packet) for packet in packets if packet.prep_allowed
        ],
        "blocked_title_reviews": [
            title_review_coordination_summary(record)
            for record in records
            if record.blocked_reasons
        ],
        "missing_items_queue": [
            {
                "review_id": record.id,
                "deal_id": record.deal_id,
                "missing_items": record.missing_items,
            }
            for record in records
            if record.missing_items
        ],
        "owner_approval_needed": [
            title_review_coordination_summary(record)
            for record in records
            if record.owner_approval_status != "approved"
        ],
        "draft_only": True,
        "legal_advice_allowed": False,
        "contract_execution_allowed": False,
        "document_submission_allowed": False,
        "title_company_email_send_allowed": False,
    }
