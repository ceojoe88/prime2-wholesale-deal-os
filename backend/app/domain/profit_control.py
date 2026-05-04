from __future__ import annotations

from dataclasses import dataclass

from app.domain.scoring import clamp_score


@dataclass(frozen=True)
class ProfitControlInput:
    arv: int
    estimated_repairs: int
    buyer_desired_profit: int
    buyer_closing_costs: int
    buyer_holding_costs: int
    target_assignment_fee: int = 10_000
    seller_contract_price: int | None = None
    buyer_purchase_price: int | None = None


def calculate_profit_control(payload: ProfitControlInput) -> dict[str, object]:
    buyer_costs = payload.buyer_closing_costs + payload.buyer_holding_costs
    max_buyer_purchase_price = (
        payload.arv
        - payload.estimated_repairs
        - buyer_costs
        - payload.buyer_desired_profit
    )
    max_seller_offer = max_buyer_purchase_price - payload.target_assignment_fee

    conservative_offer = round(max_seller_offer * 0.94)
    standard_offer = max_seller_offer
    aggressive_offer = min(
        max_buyer_purchase_price - round(payload.target_assignment_fee * 0.55),
        round(max_seller_offer * 1.04),
    )

    seller_contract_price = payload.seller_contract_price or standard_offer
    buyer_purchase_price = payload.buyer_purchase_price or min(
        max_buyer_purchase_price,
        seller_contract_price + payload.target_assignment_fee,
    )
    projected_assignment_fee = buyer_purchase_price - seller_contract_price
    buyer_margin_after_costs = (
        payload.arv
        - payload.estimated_repairs
        - buyer_costs
        - buyer_purchase_price
    )

    risk_flags: list[str] = []
    if projected_assignment_fee < payload.target_assignment_fee:
        risk_flags.append("projected_assignment_fee_below_target")
    if buyer_margin_after_costs < payload.buyer_desired_profit:
        risk_flags.append("buyer_margin_below_desired_profit")
    if seller_contract_price > max_seller_offer:
        risk_flags.append("seller_offer_exceeds_margin_safe_max")
    if seller_contract_price < max_seller_offer * 0.72:
        risk_flags.append("seller_offer_may_be_too_aggressive")
    if payload.estimated_repairs <= 0 or payload.arv <= 0:
        risk_flags.append("invalid_arv_or_repair_basis")

    offer_reasonableness_score = 92.0
    if "seller_offer_exceeds_margin_safe_max" in risk_flags:
        offer_reasonableness_score -= 28
    if "seller_offer_may_be_too_aggressive" in risk_flags:
        offer_reasonableness_score -= 18
    if "invalid_arv_or_repair_basis" in risk_flags:
        offer_reasonableness_score -= 35

    spread_confidence_score = 88.0
    if projected_assignment_fee < payload.target_assignment_fee:
        spread_confidence_score -= 26
    if buyer_margin_after_costs < payload.buyer_desired_profit:
        spread_confidence_score -= 32

    return {
        "arv": payload.arv,
        "estimated_repairs": payload.estimated_repairs,
        "buyer_costs": buyer_costs,
        "buyer_desired_profit": payload.buyer_desired_profit,
        "target_assignment_fee": payload.target_assignment_fee,
        "max_buyer_purchase_price": max_buyer_purchase_price,
        "max_seller_offer": max_seller_offer,
        "seller_contract_price": seller_contract_price,
        "buyer_purchase_price": buyer_purchase_price,
        "projected_assignment_fee": projected_assignment_fee,
        "buyer_margin_after_costs": buyer_margin_after_costs,
        "seller_fairness_notes": (
            "Offer range is defensible only when ARV, repair scope, and comparable sales "
            "are documented and presented without pressure."
        ),
        "buyer_margin_notes": (
            "Buyer margin is protected when purchase price stays at or below the computed "
            "max buyer purchase price."
        ),
        "offer_options": {
            "conservative": conservative_offer,
            "standard": standard_offer,
            "aggressive": aggressive_offer,
        },
        "offer_reasonableness_score": clamp_score(offer_reasonableness_score),
        "spread_confidence_score": clamp_score(spread_confidence_score),
        "risk_flags": risk_flags,
        "is_10k_opportunity": projected_assignment_fee >= 10_000,
        "owner_approval_required": True,
        "compliance_review_required": True,
    }


def calculate_mao(
    arv: int,
    repairs: int,
    buyer_costs: int,
    buyer_desired_profit: int,
    target_assignment_fee: int = 10_000,
) -> int:
    return arv - repairs - buyer_costs - buyer_desired_profit - target_assignment_fee
