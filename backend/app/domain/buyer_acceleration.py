from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import (
    BuyerAccelerationRecord,
    BuyerResponseRoute,
    BuyerSequencePrep,
    BuyerVelocityProfile,
)
from app.serializers import model_to_dict


BUYER_SEQUENCE_UNSAFE_PATTERNS = {
    "bulk_blast": ["blast this to all buyers", "send to all buyers", "buyer blast"],
    "deceptive_scarcity": ["only chance", "last buyer slot", "this will sell today"],
    "fake_competition": ["we already have multiple offers", "fake offer", "bidding war"],
    "seller_private_data": ["seller name", "seller phone", "seller motivation"],
    "internal_profit_logic": ["assignment fee", "seller contract price", "internal spread"],
    "legal_guarantee": ["guaranteed close", "legal advice", "binding contract"],
}


def validate_buyer_sequence_text(content: str) -> dict[str, object]:
    text = content.lower()
    flags = sorted(
        {
            category
            for category, phrases in BUYER_SEQUENCE_UNSAFE_PATTERNS.items()
            if any(phrase in text for phrase in phrases)
        }
    )
    return {
        "allowed": not flags,
        "blocked": bool(flags),
        "risk_flags": flags,
    }


def buyer_velocity_score(profile: BuyerVelocityProfile) -> float:
    score = (
        profile.response_speed * 0.18
        + profile.pof_strength * 0.18
        + profile.close_history * 0.18
        + profile.price_fit * 0.14
        + profile.market_fit * 0.14
        + profile.reliability * 0.12
        + profile.previous_intent_quality * 0.06
    )
    profile.velocity_score = round(score, 2)
    if profile.velocity_score >= 88:
        profile.recommended_use = "fast_close_priority"
    elif profile.velocity_score >= 75:
        profile.recommended_use = "targeted_follow_up"
    else:
        profile.recommended_use = "pof_or_fit_review"
    return profile.velocity_score


def buyer_distribution_gate(record: BuyerAccelerationRecord) -> dict[str, object]:
    reasons: list[str] = []
    if not record.buyer_visible:
        reasons.append("deal_not_buyer_visible")
    if not record.sanitized_deal_sheet_ready:
        reasons.append("sanitized_deal_sheet_missing")
    if not record.buyer_match_approved:
        reasons.append("buyer_match_not_approved")
    if record.pof_status not in {"verified", "acceptable", "pof_request_allowed"}:
        reasons.append("pof_status_not_acceptable")
    if not record.compliance_passed:
        reasons.append("compliance_not_passed")
    if not record.v13_gate_passed:
        reasons.append("v13_gate_not_passed")
    if not record.v5_gate_passed:
        reasons.append("v5_gate_not_passed")
    if record.owner_approval_status != "approved":
        reasons.append("owner_approval_not_recorded")
    if record.bulk_blast_allowed:
        reasons.append("bulk_blast_enabled")
    if record.buyer_margin_strength < 70:
        reasons.append("buyer_margin_weak")

    record.blocked_reasons = sorted(set(reasons))
    record.controlled_send_allowed = not reasons
    record.distribution_readiness = "ready" if record.controlled_send_allowed else "blocked"
    return {
        "controlled_send_allowed": record.controlled_send_allowed,
        "blocked_reasons": record.blocked_reasons,
        "bulk_blast_allowed": False,
        "sanitized_deal_sheet_only": True,
        "owner_approval_required": True,
    }


def sync_buyer_sequence(sequence: BuyerSequencePrep) -> dict[str, object]:
    content = " ".join(
        [
            sequence.first_buyer_notice,
            sequence.buyer_detail_follow_up,
            sequence.pof_request,
            sequence.viewing_access_coordination,
            sequence.offer_intent_follow_up,
            sequence.deadline_reminder,
        ]
    )
    result = validate_buyer_sequence_text(content)
    sequence.safety_status = "approved" if result["allowed"] else "blocked"
    sequence.blocked_reasons = result["risk_flags"]
    sequence.draft_only = True
    sequence.live_send_allowed = False
    sequence.bulk_blast_allowed = False
    sequence.deceptive_scarcity_allowed = False
    sequence.seller_private_data_exposed = False
    sequence.internal_profit_logic_exposed = False
    return result


def buyer_acceleration_dashboard(session: Session) -> dict[str, object]:
    records = session.query(BuyerAccelerationRecord).all()
    sequences = session.query(BuyerSequencePrep).all()
    routes = session.query(BuyerResponseRoute).all()
    velocities = session.query(BuyerVelocityProfile).all()
    for record in records:
        buyer_distribution_gate(record)
    for sequence in sequences:
        sync_buyer_sequence(sequence)
    for profile in velocities:
        buyer_velocity_score(profile)
    return {
        "buyer_acceleration_records": [model_to_dict(record) for record in records],
        "buyer_sequence_preps": [model_to_dict(sequence) for sequence in sequences],
        "buyer_response_routes": [model_to_dict(route) for route in routes],
        "buyer_velocity_profiles": [model_to_dict(profile) for profile in velocities],
        "fastest_buyers": [
            model_to_dict(profile)
            for profile in sorted(velocities, key=lambda item: item.velocity_score, reverse=True)
        ],
        "deals_ready_for_controlled_distribution": [
            model_to_dict(record) for record in records if record.controlled_send_allowed
        ],
        "buyer_responses_needing_owner_action": [
            model_to_dict(route) for route in routes if route.owner_action_required
        ],
        "pof_gaps": [model_to_dict(route) for route in routes if route.pof_gap],
        "blocked_distribution_records": [
            model_to_dict(record) for record in records if record.blocked_reasons
        ],
        "bulk_blast_allowed": False,
        "seller_private_data_exposed": False,
        "internal_profit_logic_exposed": False,
    }
