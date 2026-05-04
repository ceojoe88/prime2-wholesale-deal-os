from __future__ import annotations

from datetime import UTC, datetime

from app.models import Buyer, BuyerDealPublication, Deal


SANITIZED_DEAL_FIELDS = {
    "deal_id",
    "city",
    "state",
    "zip_code",
    "property_type",
    "beds",
    "baths",
    "sqft",
    "arv_range",
    "repair_estimate_range",
    "asking_price",
    "estimated_buyer_margin",
    "photos_placeholder",
    "access_instructions_placeholder",
    "proof_of_funds_status",
    "availability_status",
    "offer_interest_action",
}

FORBIDDEN_BUYER_KEYS = {
    "seller_name",
    "seller_contact",
    "seller_phone",
    "seller_email",
    "seller_motivation",
    "motivation_score",
    "seller_temperature",
    "seller_contract_price",
    "projected_assignment_fee",
    "target_assignment_fee",
    "max_seller_offer",
    "max_buyer_purchase_price",
    "source_category",
    "lead_source",
    "internal_notes",
    "notes",
    "underwriting_notes",
    "seller_fairness_notes",
    "buyer_margin_notes",
    "risk_flags",
    "compliance_records",
    "compliance_risk",
    "compliance_risk_details",
    "wholesale_prime_recommendations",
    "agent_queues",
    "manager_queues",
    "spread_confidence_score",
    "offer_reasonableness_score",
}

WEAK_MARGIN_MINIMUM = 25_000
HIGH_RISK_THRESHOLD = 45


def estimated_buyer_margin(deal: Deal, publication: BuyerDealPublication) -> int | None:
    if publication.asking_price is None:
        return None
    return deal.arv - deal.repairs - deal.buyer_costs - publication.asking_price


def portal_publish_gate(
    deal: Deal,
    publication: BuyerDealPublication | None,
) -> dict[str, object]:
    reasons: list[str] = []
    if publication is None:
        reasons.append("missing_publication_record")
        return {"can_publish": False, "blocked_reasons": reasons}

    if not publication.operator_marked_visible:
        reasons.append("operator_has_not_marked_buyer_visible")
    if deal.arv <= 0 or publication.arv_low is None or publication.arv_high is None:
        reasons.append("missing_arv")
    if deal.repairs <= 0 or publication.repair_low is None or publication.repair_high is None:
        reasons.append("missing_repair_estimate")
    if publication.asking_price is None or publication.asking_price <= 0:
        reasons.append("missing_asking_price")
    if not publication.compliance_reviewed:
        reasons.append("missing_compliance_review")
    if not publication.seller_contract_controlled:
        reasons.append("seller_contract_not_marked_controlled")
    if publication.risk_status == "high" or deal.risk_score >= HIGH_RISK_THRESHOLD:
        reasons.append("risk_status_high")

    margin = publication.estimated_buyer_margin
    if margin is None:
        margin = estimated_buyer_margin(deal, publication)
    if margin is None or margin < WEAK_MARGIN_MINIMUM or publication.buyer_margin_status == "weak":
        reasons.append("buyer_margin_weak")

    return {"can_publish": not reasons, "blocked_reasons": sorted(set(reasons))}


def update_publication_gate(publication: BuyerDealPublication, deal: Deal) -> None:
    gate = portal_publish_gate(deal, publication)
    publication.blocked_reasons = gate["blocked_reasons"]
    if gate["can_publish"]:
        publication.availability_status = (
            publication.availability_status
            if publication.availability_status in {"available", "under_review", "reserved"}
            else "available"
        )
        publication.published_at = publication.published_at or datetime.now(UTC)
    else:
        publication.availability_status = "blocked"
        publication.published_at = None


def sanitize_buyer_deal(
    deal: Deal,
    publication: BuyerDealPublication,
    buyer: Buyer | None = None,
) -> dict[str, object]:
    gate = portal_publish_gate(deal, publication)
    if not gate["can_publish"]:
        raise ValueError("Deal is not buyer-visible.")

    sanitized = {
        "deal_id": deal.id,
        "city": deal.lead.city,
        "state": deal.lead.state,
        "zip_code": deal.lead.zip_code,
        "property_type": deal.lead.property_type,
        "beds": publication.beds,
        "baths": publication.baths,
        "sqft": publication.sqft,
        "arv_range": {
            "low": publication.arv_low,
            "high": publication.arv_high,
        },
        "repair_estimate_range": {
            "low": publication.repair_low,
            "high": publication.repair_high,
        },
        "asking_price": publication.asking_price,
        "estimated_buyer_margin": publication.estimated_buyer_margin,
        "photos_placeholder": publication.photos_placeholder,
        "access_instructions_placeholder": publication.access_instructions_placeholder,
        "proof_of_funds_status": buyer.proof_of_funds_status if buyer else "invite_required",
        "availability_status": publication.availability_status,
        "offer_interest_action": {
            "type": "draft_intent_only",
            "contract_execution_allowed": False,
            "payment_collection_allowed": False,
        },
    }
    assert_no_buyer_leaks(sanitized)
    return sanitized


def assert_no_buyer_leaks(payload: dict[str, object]) -> None:
    leaked_keys = FORBIDDEN_BUYER_KEYS.intersection(payload.keys())
    if leaked_keys:
        raise ValueError(f"Buyer sanitizer leaked forbidden fields: {sorted(leaked_keys)}")
    if not set(payload.keys()).issubset(SANITIZED_DEAL_FIELDS):
        extras = sorted(set(payload.keys()) - SANITIZED_DEAL_FIELDS)
        raise ValueError(f"Buyer sanitizer emitted unexpected fields: {extras}")


def buyer_portal_rules() -> dict[str, object]:
    return {
        "source_of_truth": "private_operator_system",
        "invite_gated_only": True,
        "public_signup": False,
        "seller_portal": False,
        "live_buyer_blasts": False,
        "payment_collection": False,
        "contract_execution": False,
        "legal_advice": False,
        "sanitized_fields": sorted(SANITIZED_DEAL_FIELDS),
        "forbidden_fields": sorted(FORBIDDEN_BUYER_KEYS),
    }
