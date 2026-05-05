from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import (
    DealProbabilityRecord,
    LeadSpendPlan,
    MarketScalingScore,
    RevenueForecastRecord,
)
from app.serializers import model_to_dict


FORECAST_UNSAFE_PATTERNS = {
    "guaranteed_revenue": ["guaranteed revenue", "guaranteed profit", "guaranteed assignment fee"],
    "unsupported_roi": ["guaranteed roi", "risk-free return", "unsupported roi"],
    "invented_probability": ["made-up probability", "invented close probability"],
}


def validate_forecast_language(content: str) -> dict[str, object]:
    text = content.lower()
    risk_flags = sorted(
        {
            category
            for category, phrases in FORECAST_UNSAFE_PATTERNS.items()
            if any(phrase in text for phrase in phrases)
        }
    )
    return {
        "allowed": not risk_flags,
        "risk_flags": risk_flags,
        "forecasts_are_estimates": True,
        "guaranteed_revenue_allowed": False,
        "unsupported_roi_allowed": False,
    }


def calculate_deal_probability(record: DealProbabilityRecord) -> float:
    positive = (
        record.seller_readiness * 0.16
        + record.buyer_demand * 0.16
        + record.underwriting_confidence * 0.14
        + record.compliance_status_score * 0.14
        + record.title_review_readiness * 0.12
        + record.buyer_pof_strength * 0.14
        + record.communication_momentum * 0.10
    )
    penalty = record.blocker_severity * 0.10
    record.probability_score = round(max(0, min(100, positive - penalty)), 2)
    if record.probability_score >= 80:
        record.probability_band = "high_estimate"
    elif record.probability_score >= 60:
        record.probability_band = "base_estimate"
    else:
        record.probability_band = "conservative_estimate"
    record.estimate_only = True
    return record.probability_score


def calculate_market_scaling(record: MarketScalingScore) -> float:
    score = (
        min(record.lead_volume * 2, 100) * 0.12
        + record.hot_lead_percentage * 0.18
        + record.buyer_demand * 0.20
        + min(record.average_spread / 280, 100) * 0.18
        + min(record.conversion_rate * 2, 100) * 0.14
        + (100 - record.title_compliance_friction) * 0.10
        + (100 - record.competition_risk) * 0.08
    )
    record.scaling_score = round(max(0, min(100, score)), 2)
    if record.scaling_score >= 70 and record.source_record_ids:
        record.recommended_spend_level = "increase_selectively"
    elif record.scaling_score >= 65:
        record.recommended_spend_level = "hold_or_test"
    else:
        record.recommended_spend_level = "avoid_or_research"
    record.estimate_only = True
    return record.scaling_score


def validate_lead_spend_plan(plan: LeadSpendPlan) -> dict[str, object]:
    reasons: list[str] = []
    if not plan.evidence_basis:
        reasons.append("evidence_basis_required")
    if plan.unsupported_spend_recommended:
        reasons.append("unsupported_spend_recommended")
    if plan.max_monthly_spend > 0 and plan.break_even_assignment_target <= 0:
        reasons.append("break_even_assignment_target_required")
    return {
        "allowed": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "estimate_only": True,
        "owner_review_required": True,
    }


def sync_revenue_forecast(record: RevenueForecastRecord) -> None:
    record.conservative_forecast = int(record.probability_adjusted_revenue * 0.75)
    record.base_forecast = record.probability_adjusted_revenue
    record.aggressive_forecast = int(record.probability_adjusted_revenue * 1.18)
    record.estimate_label = "Estimate only; not guaranteed revenue."
    record.guaranteed_revenue_claim_allowed = False
    record.unsupported_roi_claim_allowed = False


def revenue_forecast_dashboard(session: Session) -> dict[str, object]:
    forecasts = session.query(RevenueForecastRecord).all()
    probabilities = session.query(DealProbabilityRecord).all()
    markets = session.query(MarketScalingScore).all()
    spend_plans = session.query(LeadSpendPlan).all()
    for forecast in forecasts:
        sync_revenue_forecast(forecast)
    for probability in probabilities:
        calculate_deal_probability(probability)
    for market in markets:
        calculate_market_scaling(market)
    spend_gates = {plan.id: validate_lead_spend_plan(plan) for plan in spend_plans}
    return {
        "revenue_forecasts": [model_to_dict(forecast) for forecast in forecasts],
        "deal_probabilities": [
            model_to_dict(probability)
            for probability in sorted(probabilities, key=lambda item: item.probability_score, reverse=True)
        ],
        "market_scaling_scores": [
            model_to_dict(market)
            for market in sorted(markets, key=lambda item: item.scaling_score, reverse=True)
        ],
        "lead_spend_plans": [
            {**model_to_dict(plan), "gate": spend_gates[plan.id]}
            for plan in spend_plans
        ],
        "pipeline_value": {
            "projected_monthly_revenue": sum(forecast.projected_assignment_fees for forecast in forecasts),
            "probability_adjusted_revenue": sum(
                forecast.probability_adjusted_revenue for forecast in forecasts
            ),
            "verified_assignment_fees": sum(forecast.verified_assignment_fees for forecast in forecasts),
            "revenue_at_risk": sum(
                forecast.projected_assignment_fees - forecast.probability_adjusted_revenue
                for forecast in forecasts
            ),
            "forecasts_are_estimates": True,
            "guaranteed_profit_allowed": False,
        },
        "ten_k_likely_deals": [
            model_to_dict(probability)
            for probability in probabilities
            if probability.probability_score >= 70
        ],
        "forecasts_are_estimates": True,
        "guaranteed_revenue_allowed": False,
        "unsupported_roi_allowed": False,
    }
