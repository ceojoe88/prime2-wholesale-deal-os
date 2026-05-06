from __future__ import annotations

from app.models import (
    AssignmentFeeAttribution,
    Buyer,
    BuyerDealPriority,
    ContractReadyState,
    Deal,
    DealEvidencePacket,
    OfferPacket,
)


def buyer_margin(deal: Deal) -> int:
    return deal.max_buyer_purchase_price - deal.buyer_purchase_price


def offer_decision_status(deal: Deal, packet: OfferPacket | None) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if deal.arv <= 0:
        reasons.append("missing_arv")
    if deal.repairs <= 0:
        reasons.append("missing_repair_estimate")
    if deal.max_seller_offer <= 0:
        reasons.append("missing_max_seller_offer")
    if buyer_margin(deal) < deal.buyer_desired_profit:
        reasons.append("buyer_margin_not_protected")
    if deal.projected_assignment_fee < deal.target_assignment_fee:
        reasons.append("target_assignment_fee_not_met")
    if deal.risk_score >= 80 or any("compliance" in flag for flag in (deal.risk_flags or [])):
        reasons.append("compliance_review_needed")
    if packet is None:
        reasons.append("offer_packet_missing")
    elif packet.packet_prep_allowed is False:
        reasons.extend(packet.blocked_reasons or ["offer_packet_gate_not_clear"])

    if "compliance_review_needed" in reasons:
        return "blocked_by_compliance", sorted(set(reasons))
    if reasons:
        return "needs_data", sorted(set(reasons))
    return "ready_for_owner_review", []


def buyer_validation_gate(
    deal: Deal,
    priority: BuyerDealPriority | None,
    buyer: Buyer | None,
) -> dict[str, object]:
    reasons: list[str] = []
    if priority is None or buyer is None:
        reasons.append("no_buyer_demand")
    else:
        if priority.buyer_margin_strength < 70:
            reasons.append("weak_buyer_margin")
        if buyer.proof_of_funds_status not in {"verified", "acceptable", "approved"}:
            reasons.append("pof_request_unresolved")
        if buyer.reliability_score < 70:
            reasons.append("buyer_reliability_low")
        if buyer.max_purchase_price < deal.buyer_purchase_price:
            reasons.append("buyer_price_below_needed_spread")
    return {
        "validated": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "contract_ready_recommendation_allowed": not reasons,
    }


def contract_ready_gate(state: ContractReadyState | None) -> dict[str, object]:
    reasons: list[str] = []
    if state is None:
        reasons.append("contract_ready_state_missing")
    else:
        checks = {
            "seller_motivation_confirmed": state.seller_readiness_high,
            "seller_terms_soft_accepted": state.seller_likely_to_sign,
            "underwriting_complete": state.underwriting_complete,
            "buyer_demand_validated": state.buyer_demand_confirmed,
            "offer_approved": state.owner_approval_recorded,
            "compliance_passed": state.compliance_passed,
            "assignment_readiness_checked": state.profit_control_validated,
            "title_attorney_review_prep_available": state.ready_for_external_drafting,
            "owner_approval_complete": state.owner_approval_recorded,
        }
        reasons.extend(key for key, passed in checks.items() if not passed)
    return {
        "contract_ready": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "external_process_only": True,
    }


def evidence_gate(
    deal: Deal,
    attribution: AssignmentFeeAttribution | None,
    packet: DealEvidencePacket | None,
) -> dict[str, object]:
    reasons: list[str] = []
    if attribution is None:
        reasons.append("assignment_fee_attribution_missing")
    else:
        if attribution.projected_assignment_fee < attribution.target_assignment_fee:
            reasons.append("unsupported_10k_opportunity")
        if attribution.buyer_purchase_price <= 0:
            reasons.append("buyer_price_missing")
        if attribution.seller_contract_price <= 0:
            reasons.append("seller_acceptance_missing")
        if not attribution.source_records_present:
            reasons.append("source_records_missing")
        if attribution.unsupported_profit_claims:
            reasons.append("unsupported_profit_claims")
    if packet is None or not packet.source_records_present:
        reasons.append("evidence_packet_source_missing")
    if deal.arv <= 0 or deal.repairs <= 0:
        reasons.append("underwriting_source_missing")
    return {
        "evidence_supported": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "client_facing_claim_allowed": False,
        "guarantee_language_allowed": False,
    }
