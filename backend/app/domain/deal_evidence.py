from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.closing_coordination import sync_deal_room
from app.models import (
    AssignmentFeeAttribution,
    BuyerInterest,
    CommunicationDraft,
    DealEvidencePacket,
    SellerInteraction,
    UnifiedDealRoom,
)
from app.serializers import model_to_dict


UNSUPPORTED_PROFIT_PATTERNS = {
    "guaranteed profit": "fake_profit_claim",
    "guaranteed roi": "unsupported_roi_claim",
    "risk-free return": "unsupported_roi_claim",
    "guarantee closing": "legal_closing_guarantee",
    "guaranteed close": "legal_closing_guarantee",
    "guaranteed closing": "legal_closing_guarantee",
    "will close no matter what": "legal_closing_guarantee",
    "invented buyer price": "invented_buyer_seller_numbers",
    "invented seller price": "invented_buyer_seller_numbers",
    "fake buyer price": "invented_buyer_seller_numbers",
    "fake seller price": "invented_buyer_seller_numbers",
}

INTERNAL_NOTE_KEYS = {
    "call_notes",
    "motivation_answers",
    "pain_points",
    "objections",
    "internal_notes",
    "seller_temperature_score",
    "next_best_actions",
    "blocker_records",
    "wholesale_prime_recommendations",
}


def validate_profit_claims(content: str) -> dict[str, object]:
    lowered = content.lower()
    flags = sorted(
        {flag for pattern, flag in UNSUPPORTED_PROFIT_PATTERNS.items() if pattern in lowered}
    )
    return {
        "allowed": not flags,
        "risk_flags": flags,
        "blocked": bool(flags),
        "fake_profit_claims_blocked": "fake_profit_claim" in flags,
        "unsupported_roi_claims_blocked": "unsupported_roi_claim" in flags,
        "invented_numbers_blocked": "invented_buyer_seller_numbers" in flags,
        "legal_closing_guarantees_blocked": "legal_closing_guarantee" in flags,
    }


def _latest(records):
    return records[0] if records else None


def _seller_interaction(session: Session, room: UnifiedDealRoom) -> SellerInteraction | None:
    return (
        session.query(SellerInteraction)
        .filter(SellerInteraction.lead_id == room.deal.lead_id)
        .order_by(SellerInteraction.created_at.desc())
        .first()
    )


def _buyer_interest(room: UnifiedDealRoom) -> BuyerInterest | None:
    readiness = room.assignment_readiness_record or _latest(room.deal.assignment_readiness_records)
    if readiness and readiness.buyer_interest:
        return readiness.buyer_interest
    return _latest(room.deal.buyer_interests)


def communication_receipt_summary(session: Session, room: UnifiedDealRoom) -> list[dict[str, object]]:
    seller_interaction_ids = [
        interaction.id
        for interaction in session.query(SellerInteraction)
        .filter(SellerInteraction.lead_id == room.deal.lead_id)
        .all()
    ]
    buyer_interest_ids = [interest.id for interest in room.deal.buyer_interests]
    title_packet_ids = [packet.id for packet in room.deal.title_handoff_packets]
    drafts = [
        draft
        for draft in session.query(CommunicationDraft).all()
        if draft.seller_interaction_id in seller_interaction_ids
        or draft.buyer_interest_id in buyer_interest_ids
        or draft.title_handoff_packet_id in title_packet_ids
    ]
    return [
        {
            "draft_id": draft.id,
            "source_record_type": draft.source_record_type,
            "source_record_id": draft.source_record_id,
            "safety_passed": draft.safety_passed,
            "dry_run_receipts": [receipt.id for receipt in draft.dry_run_receipts],
            "provider_mode": "mock/dry_run",
            "live_send_count": draft.live_send_count,
        }
        for draft in drafts
    ]


def underwriting_snapshot(room: UnifiedDealRoom) -> dict[str, object]:
    deal = room.deal
    return {
        "deal_id": deal.id,
        "arv": deal.arv,
        "repairs": deal.repairs,
        "buyer_costs": deal.buyer_costs,
        "buyer_desired_profit": deal.buyer_desired_profit,
        "target_assignment_fee": deal.target_assignment_fee,
        "seller_contract_price": deal.seller_contract_price,
        "buyer_purchase_price": deal.buyer_purchase_price,
        "projected_assignment_fee_source": "buyer_purchase_price_minus_seller_contract_price",
        "buyer_margin_source": "arv_minus_repairs_minus_buyer_costs_minus_buyer_purchase_price",
    }


def _source_records_present(
    room: UnifiedDealRoom,
    seller_interaction: SellerInteraction | None,
    buyer_interest: BuyerInterest | None,
) -> bool:
    snapshot = underwriting_snapshot(room)
    return all(
        [
            room.deal is not None,
            room.contract_control is not None,
            bool(room.deal.lead.source_category),
            seller_interaction is not None,
            buyer_interest is not None,
            bool(snapshot["arv"]),
            bool(snapshot["repairs"]),
            bool(snapshot["seller_contract_price"]),
            bool(snapshot["buyer_purchase_price"]),
        ]
    )


def evidence_review_gate(packet: DealEvidencePacket) -> dict[str, object]:
    reasons: list[str] = []
    if packet.contract_control_status == "missing":
        reasons.append("missing_contract_control")
    if not packet.buyer_interest_proof.get("buyer_interest_id"):
        reasons.append("missing_buyer_interest")
    if not packet.seller_interaction_proof.get("seller_acceptance_recorded"):
        reasons.append("missing_seller_acceptance")
    if packet.compliance_review_status != "approved":
        reasons.append("compliance_not_passed")
    if not packet.source_records_present:
        reasons.append("source_records_missing")
    if packet.unsupported_profit_claims:
        reasons.append("unsupported_profit_claims")
    if packet.client_facing_proof_allowed:
        reasons.append("client_facing_proof_enabled")
    if packet.legal_closing_guarantee_allowed:
        reasons.append("legal_closing_guarantee_enabled")
    return {
        "can_approve_evidence": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "client_facing_proof_allowed": False,
        "legal_closing_guarantee_allowed": False,
    }


def sanitize_evidence_packet(packet: DealEvidencePacket) -> dict[str, object]:
    summary = {
        "packet_id": packet.id,
        "deal_room_id": packet.deal_room_id,
        "deal_id": packet.deal_id,
        "lead_source": packet.lead_source,
        "seller_interaction_proof": packet.seller_interaction_proof,
        "underwriting_snapshot": packet.underwriting_snapshot,
        "buyer_interest_proof": packet.buyer_interest_proof,
        "pof_proof_status": packet.pof_proof_status,
        "contract_control_status": packet.contract_control_status,
        "title_handoff_status": packet.title_handoff_status,
        "communication_receipts": packet.communication_receipts,
        "blocker_history": packet.blocker_history,
        "compliance_review_status": packet.compliance_review_status,
        "evidence_status": packet.evidence_status,
        "owner_review_status": packet.owner_review_status,
        "approved": packet.approved,
        "client_facing_proof_allowed": False,
        "legal_closing_guarantee_allowed": False,
    }
    serialized = str(summary).lower()
    for key in INTERNAL_NOTE_KEYS:
        summary.pop(key, None)
        assert key not in serialized
    return summary


def sync_evidence_packet(session: Session, packet: DealEvidencePacket) -> dict[str, object]:
    room = packet.deal_room
    sync_deal_room(session, room)
    seller_interaction = _seller_interaction(session, room)
    buyer_interest = _buyer_interest(room)
    packet.lead_source = room.deal.lead.source_category
    packet.seller_interaction_proof = {
        "seller_interaction_id": seller_interaction.id if seller_interaction else None,
        "seller_acceptance_recorded": bool(room.contract_control.seller_accepted_terms),
        "accepted_terms_record_id": room.contract_control.id,
    }
    packet.underwriting_snapshot = underwriting_snapshot(room)
    packet.buyer_interest_proof = {
        "buyer_interest_id": buyer_interest.id if buyer_interest else None,
        "interest_status": buyer_interest.interest_status if buyer_interest else "missing",
        "intended_offer_amount": buyer_interest.intended_offer_amount if buyer_interest else None,
        "draft_only": buyer_interest.draft_only if buyer_interest else True,
        "contract_execution_allowed": False,
    }
    packet.pof_proof_status = buyer_interest.proof_of_funds_status if buyer_interest else "missing"
    packet.contract_control_status = room.contract_control.contract_status
    packet.title_handoff_status = room.title_handoff_status
    packet.communication_receipts = communication_receipt_summary(session, room)
    packet.blocker_history = [
        {
            "blocker_id": blocker.id,
            "blocker_type": blocker.blocker_type,
            "status": blocker.status,
            "resolved": blocker.resolved,
        }
        for blocker in room.blocker_records
    ]
    packet.compliance_review_status = room.contract_control.compliance_review_status
    packet.source_records_present = _source_records_present(room, seller_interaction, buyer_interest)
    packet.unsupported_profit_claims = validate_profit_claims(str(packet.sanitized_summary))[
        "risk_flags"
    ]
    gate = evidence_review_gate(packet)
    if gate["can_approve_evidence"] and packet.owner_review_status == "owner_approved":
        packet.evidence_status = "approved"
        packet.approved = True
    elif gate["can_approve_evidence"]:
        packet.evidence_status = "owner_review_needed"
        packet.approved = False
    else:
        packet.evidence_status = "blocked_missing_evidence"
        packet.approved = False
    packet.sanitized_summary = sanitize_evidence_packet(packet)
    packet.internal_notes_sanitized = True
    packet.draft_only = True
    packet.client_facing_proof_allowed = False
    packet.legal_closing_guarantee_allowed = False
    return gate


def _fee_basis(room: UnifiedDealRoom, packet: DealEvidencePacket | None) -> list[str]:
    basis = [
        f"deal:{room.deal_id}",
        f"deal_room:{room.id}",
        f"contract_control:{room.contract_control_id}",
        "seller_contract_price:deal.seller_contract_price",
        "buyer_purchase_price:deal.buyer_purchase_price",
        "buyer_margin:arv-repairs-buyer_costs-buyer_purchase_price",
    ]
    interest = _buyer_interest(room)
    if interest:
        basis.append(f"buyer_interest:{interest.id}")
    if packet:
        basis.append(f"evidence_packet:{packet.id}")
    return basis


def sync_assignment_fee_attribution(
    session: Session,
    attribution: AssignmentFeeAttribution,
) -> dict[str, object]:
    room = attribution.deal_room
    sync_deal_room(session, room)
    packet = attribution.evidence_packet or _latest(room.evidence_packets)
    if packet is not None:
        sync_evidence_packet(session, packet)
        attribution.evidence_packet_id = packet.id

    deal = room.deal
    calculated_fee = deal.buyer_purchase_price - deal.seller_contract_price
    buyer_margin = deal.arv - deal.repairs - deal.buyer_costs - deal.buyer_purchase_price
    attribution.projected_assignment_fee = calculated_fee
    attribution.target_assignment_fee = deal.target_assignment_fee
    attribution.seller_contract_price = deal.seller_contract_price
    attribution.buyer_purchase_price = deal.buyer_purchase_price
    attribution.buyer_margin = buyer_margin
    attribution.attribution_basis = _fee_basis(room, packet)
    attribution.source_records_present = bool(packet and packet.source_records_present)
    attribution.unsupported_profit_claims = packet.unsupported_profit_claims if packet else []
    if not attribution.source_records_present:
        attribution.verification_status = "missing_evidence"
    elif packet and packet.approved:
        attribution.verification_status = "verified"
    elif packet and evidence_review_gate(packet)["can_approve_evidence"]:
        attribution.verification_status = "owner_review_needed"
    else:
        attribution.verification_status = "blocked"
    blockers = len([blocker for blocker in room.blocker_records if not blocker.resolved])
    base_confidence = 92 if attribution.verification_status == "verified" else 72
    if attribution.verification_status in {"blocked", "missing_evidence"}:
        base_confidence = 45
    attribution.confidence_score = max(0, base_confidence - blockers * 4)
    attribution.verified_10k_opportunity = (
        attribution.verification_status == "verified"
        and calculated_fee >= attribution.target_assignment_fee
        and calculated_fee == deal.projected_assignment_fee
    )
    attribution.draft_only = True
    attribution.client_facing_proof_allowed = False
    attribution.legal_closing_guarantee_allowed = False
    return assignment_fee_gate(attribution)


def assignment_fee_gate(attribution: AssignmentFeeAttribution) -> dict[str, object]:
    reasons: list[str] = []
    if not attribution.source_records_present:
        reasons.append("source_records_missing")
    if attribution.unsupported_profit_claims:
        reasons.append("unsupported_profit_claims")
    if attribution.projected_assignment_fee != (
        attribution.buyer_purchase_price - attribution.seller_contract_price
    ):
        reasons.append("assignment_fee_not_source_calculated")
    if attribution.client_facing_proof_allowed:
        reasons.append("client_facing_proof_enabled")
    if attribution.legal_closing_guarantee_allowed:
        reasons.append("legal_closing_guarantee_enabled")
    return {
        "can_attribute_fee": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "uses_actual_source_numbers": True,
        "client_facing_proof_allowed": False,
        "legal_closing_guarantee_allowed": False,
    }


def evidence_packet_summary(packet: DealEvidencePacket) -> dict[str, object]:
    return {
        **model_to_dict(packet),
        "sanitized_summary": sanitize_evidence_packet(packet),
        "review_gate": evidence_review_gate(packet),
        "client_facing_proof_allowed": False,
        "legal_closing_guarantee_allowed": False,
    }


def assignment_fee_summary(attribution: AssignmentFeeAttribution) -> dict[str, object]:
    return {
        **model_to_dict(attribution),
        "fee_gate": assignment_fee_gate(attribution),
        "actual_formula": "buyer_purchase_price - seller_contract_price",
        "verified_10k_opportunity": attribution.verified_10k_opportunity,
        "client_facing_proof_allowed": False,
        "legal_closing_guarantee_allowed": False,
    }


def evidence_dashboard(session: Session) -> dict[str, object]:
    packets = session.query(DealEvidencePacket).all()
    attributions = session.query(AssignmentFeeAttribution).all()
    for packet in packets:
        sync_evidence_packet(session, packet)
    for attribution in attributions:
        sync_assignment_fee_attribution(session, attribution)

    verified = [item for item in attributions if item.verification_status == "verified"]
    missing_evidence = [
        packet
        for packet in packets
        if evidence_review_gate(packet)["blocked_reasons"]
    ]
    owner_review = [
        packet
        for packet in packets
        if packet.evidence_status == "owner_review_needed"
        or packet.owner_review_status != "owner_approved"
    ]
    fees_at_risk = [
        item
        for item in attributions
        if item.verification_status != "verified" and item.projected_assignment_fee > 0
    ]
    return {
        "evidence_packets": [evidence_packet_summary(packet) for packet in packets],
        "assignment_fee_attributions": [
            assignment_fee_summary(attribution) for attribution in attributions
        ],
        "projected_assignment_fees": sum(
            item.projected_assignment_fee for item in attributions
        ),
        "verified_assignment_fees": sum(item.projected_assignment_fee for item in verified),
        "fees_at_risk": sum(item.projected_assignment_fee for item in fees_at_risk),
        "missing_evidence": [packet.id for packet in missing_evidence],
        "deals_needing_owner_review": [packet.deal_id for packet in owner_review],
        "verified_10k_opportunities": [
            assignment_fee_summary(item) for item in attributions if item.verified_10k_opportunity
        ],
        "client_facing_proof_allowed": False,
        "legal_closing_guarantee_allowed": False,
    }
