from __future__ import annotations

from app.models import ClientLeadProfile


REQUIRED_FIELDS = [
    "display_name",
    "property_address_summary",
    "property_city",
    "property_state",
    "property_zip",
    "property_type",
    "estimated_value",
    "estimated_equity",
]


def clamp(value: int) -> int:
    return max(0, min(100, int(value)))


def missing_fields(lead: ClientLeadProfile) -> list[str]:
    missing: list[str] = []
    for field in REQUIRED_FIELDS:
        value = getattr(lead, field)
        if value in (None, "", 0, []):
            missing.append(field)
    if not lead.contact_channels_present:
        missing.append("contact_channels_present")
    if not lead.motivation_signals:
        missing.append("motivation_signals")
    return missing


def score_client_lead(lead: ClientLeadProfile) -> dict[str, object]:
    motivation_score = clamp(25 + len(lead.motivation_signals or []) * 18)
    urgency_score = clamp(100 - max(0, lead.timeline_days - 7))
    equity_signal_score = clamp(max(lead.estimated_equity_percent, 0) + (20 if lead.estimated_equity >= 75000 else 0))
    distress_signal_score = clamp(20 + len(lead.distress_signals or []) * 16)
    contactability_score = clamp(20 + len(lead.contact_channels_present or []) * 30)
    missing = missing_fields(lead)
    missing_data_score = clamp(100 - len(missing) * 13)
    deal_probability_score = clamp(
        round(
            motivation_score * 0.22
            + urgency_score * 0.16
            + equity_signal_score * 0.22
            + distress_signal_score * 0.16
            + contactability_score * 0.14
            + lead.data_confidence * 0.10
        )
    )
    final_priority_score = clamp(round(deal_probability_score * 0.82 + missing_data_score * 0.18))

    if lead.dnc_flag or lead.legal_question_flag:
        recommended_next_action = "human_review_required"
    elif missing:
        recommended_next_action = "complete_missing_data"
    elif final_priority_score >= 78:
        recommended_next_action = "owner_review_hot_lead"
    elif final_priority_score >= 62:
        recommended_next_action = "research_and_prepare_call_plan"
    else:
        recommended_next_action = "nurture_or_skip_for_now"

    confidence_level = "high"
    if missing or lead.data_confidence < 65:
        confidence_level = "medium"
    if len(missing) >= 4 or lead.data_confidence < 45:
        confidence_level = "low"

    requires_human_review = (
        lead.dnc_flag
        or lead.legal_question_flag
        or final_priority_score >= 78
        or len(missing) >= 3
        or confidence_level == "low"
    )

    reasons = [
        f"{len(lead.motivation_signals or [])} motivation signals",
        f"{len(lead.distress_signals or [])} distress signals",
        f"{lead.estimated_equity_percent}% estimated equity",
        f"{len(missing)} missing data items",
    ]
    if lead.dnc_flag:
        reasons.append("DNC flag requires no outbound action")
    if lead.legal_question_flag:
        reasons.append("legal question requires human review")

    return {
        "motivation_score": motivation_score,
        "urgency_score": urgency_score,
        "equity_signal_score": equity_signal_score,
        "distress_signal_score": distress_signal_score,
        "contactability_score": contactability_score,
        "deal_probability_score": deal_probability_score,
        "missing_data_score": missing_data_score,
        "final_priority_score": final_priority_score,
        "recommended_next_action": recommended_next_action,
        "reason_summary": "; ".join(reasons),
        "confidence_level": confidence_level,
        "requires_human_review": requires_human_review,
        "missing_fields": missing,
        "raw_risk_logic": {
            "weights": {
                "motivation": 0.22,
                "urgency": 0.16,
                "equity": 0.22,
                "distress": 0.16,
                "contactability": 0.14,
                "data_confidence": 0.10,
            },
            "client_hidden": True,
        },
    }
