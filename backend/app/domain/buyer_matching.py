from __future__ import annotations


def score_buyer_match(deal: dict, buyer: dict) -> dict[str, object]:
    score = 0.0
    reasons: list[str] = []
    risk_flags: list[str] = []

    if deal["zip_code"] in buyer["target_zip_codes"]:
        score += 30
        reasons.append("target_zip_match")
    if buyer["max_purchase_price"] >= deal["buyer_purchase_price"]:
        score += 24
        reasons.append("price_capacity_match")
    else:
        risk_flags.append("buyer_price_capacity_short")
    if buyer["property_type"] in {deal["property_type"], "any"}:
        score += 14
        reasons.append("property_type_match")

    score += min(18.0, buyer["reliability_score"] * 0.18)
    if buyer["proof_of_funds_status"] == "verified":
        score += 8
        reasons.append("proof_of_funds_verified")
    else:
        risk_flags.append("proof_of_funds_needs_review")
    if buyer["closing_speed_days"] <= 14:
        score += 6
        reasons.append("fast_close")

    return {
        "score": round(min(score, 100.0), 2),
        "match_reasons": reasons,
        "risk_flags": risk_flags,
        "draft_only": True,
    }


def rank_buyer_matches(deal: dict, buyers: list[dict]) -> list[dict[str, object]]:
    matches = []
    for buyer in buyers:
        if not buyer.get("active", True):
            continue
        result = score_buyer_match(deal, buyer)
        if result["score"] >= 55:
            matches.append({"buyer_id": buyer["id"], "deal_id": deal["id"], **result})
    return sorted(matches, key=lambda match: match["score"], reverse=True)
