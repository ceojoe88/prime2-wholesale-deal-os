from __future__ import annotations


LEAD_SCORE_WEIGHTS = {
    "motivation": 0.18,
    "distress_signals": 0.14,
    "equity": 0.16,
    "urgency": 0.12,
    "contactability": 0.10,
    "seller_temperature": 0.10,
    "data_confidence": 0.08,
    "market_demand": 0.12,
}


def clamp_score(value: float) -> float:
    return max(0.0, min(100.0, round(value, 2)))


def weighted_score(values: dict[str, float], weights: dict[str, float]) -> float:
    return clamp_score(
        sum(clamp_score(values.get(key, 0.0)) * weight for key, weight in weights.items())
    )


def calculate_lead_opportunity(values: dict[str, float]) -> float:
    return weighted_score(values, LEAD_SCORE_WEIGHTS)


def deal_speed_score(
    motivation: float,
    equity: float,
    buyer_demand: float,
    contactability: float,
    compliance_risk: float,
) -> float:
    low_risk_multiplier = max(0.0, (100.0 - clamp_score(compliance_risk)) / 100.0)
    raw = (
        (clamp_score(motivation) / 100.0)
        * (clamp_score(equity) / 100.0)
        * (clamp_score(buyer_demand) / 100.0)
        * (clamp_score(contactability) / 100.0)
        * low_risk_multiplier
    )
    return clamp_score(raw * 100)
