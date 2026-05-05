from __future__ import annotations

import re
from typing import Any

from app.domain.scoring import clamp_score
from app.domains.call_intelligence.safety import detect_do_not_contact, detect_legal_request


OBJECTION_PATTERNS: dict[str, list[str]] = {
    "price_too_low": ["too low", "low offer", "need more money", "worth more"],
    "needs_more_time": ["need time", "think about it", "not ready"],
    "wants_repairs_considered": ["repairs", "roof", "foundation", "hvac", "condition"],
    "has_mortgage_concern": ["mortgage", "payoff", "loan balance"],
    "wants_family_input": ["family", "spouse", "children", "brother", "sister"],
    "wants_proof_buyer_can_close": ["proof", "funds", "can close"],
    "confused_about_assignment": ["assignment", "assign", "who is buying"],
    "wants_legal_title_explanation": ["attorney", "title", "contract mean", "legal meaning"],
    "not_interested": ["not interested", "no thanks"],
    "call_back_later": ["call me back", "follow up", "next week", "tomorrow"],
}


def _basis(text: str, patterns: list[str]) -> str:
    lowered = text.lower()
    for pattern in patterns:
        index = lowered.find(pattern)
        if index >= 0:
            start = max(0, index - 35)
            end = min(len(text), index + len(pattern) + 35)
            return text[start:end].strip()
    return ""


def _asking_price(text: str) -> int | None:
    money_matches = re.findall(r"\$?\s?(\d{2,3}(?:,\d{3})+|\d{5,6})", text)
    if not money_matches:
        return None
    values = [int(match.replace(",", "")) for match in money_matches]
    return max(values) if values else None


def extract_call_intelligence(text: str) -> dict[str, Any]:
    lowered = text.lower()
    asking_price = _asking_price(text)
    timeline = "soon" if any(term in lowered for term in ["soon", "asap", "quick", "this month"]) else ""
    if "next week" in lowered:
        timeline = "next week"
    elif "30 days" in lowered:
        timeline = "30 days"
    elif "no rush" in lowered:
        timeline = "no rush"

    condition_terms = [term for term in ["roof", "foundation", "hvac", "plumbing", "vacant", "repairs", "cleanout"] if term in lowered]
    condition = ", ".join(condition_terms) if condition_terms else "condition not fully captured"
    occupancy = "vacant" if "vacant" in lowered or "empty" in lowered else "occupied" if "tenant" in lowered or "living" in lowered else "unknown"
    decision_maker = "needs family input" if "family" in lowered or "spouse" in lowered else "owner_decision_maker" if "i own" in lowered or "my property" in lowered else "unknown"
    follow_up = "do_not_contact" if detect_do_not_contact(text) else "call_back_later" if "call me back" in lowered or "next week" in lowered else "owner_review"
    motivation_reason = "timeline or property condition pressure" if any(term in lowered for term in ["tired", "vacant", "repairs", "behind", "inherited", "tax"]) else "motivation not explicit"
    trust_level = 80 if any(term in lowered for term in ["thanks", "appreciate", "send me", "talk"]) else 55
    price_flexibility = 75 if any(term in lowered for term in ["flexible", "as-is", "cash", "quick"]) else 45
    objections = [
        objection
        for objection, patterns in OBJECTION_PATTERNS.items()
        if any(pattern in lowered for pattern in patterns)
    ]
    legal_flags = detect_legal_request(text)
    do_not_contact = detect_do_not_contact(text)
    motivation_delta = 18 if any(term in lowered for term in ["motivated", "asap", "quick", "offer", "cash", "tired"]) else 6 if timeline else 0
    contactability_delta = -60 if do_not_contact else 15 if any(term in lowered for term in ["call me back", "email", "text", "next week"]) else 5
    risk_delta = 30 if legal_flags else 5 if objections else 0
    quality_items = {
        "asked_motivation_questions": any(term in lowered for term in ["why", "timeline", "looking to sell"]),
        "captured_property_condition": bool(condition_terms),
        "captured_timeline": bool(timeline),
        "captured_asking_price": asking_price is not None,
        "captured_decision_maker": decision_maker != "unknown",
        "captured_next_step": follow_up != "owner_review",
        "avoided_pressure": not any(term in lowered for term in ["must sign", "last chance"]),
        "avoided_legal_advice": "this is legal advice" not in lowered,
        "avoided_fake_urgency": "this will sell today" not in lowered,
    }
    quality_score = clamp_score(
        sum(12 if value else 0 for value in quality_items.values())
        - (10 if do_not_contact else 0)
    )
    confidence = clamp_score(45 + (10 if asking_price else 0) + len(condition_terms) * 6 + len(objections) * 5)

    return {
        "seller_motivation_reason": motivation_reason,
        "urgency_timeline": timeline or "unknown",
        "asking_price": asking_price,
        "property_condition": condition,
        "repair_clues": condition_terms,
        "occupancy_status": occupancy,
        "seller_objections": objections,
        "decision_maker_status": decision_maker,
        "trust_level": clamp_score(trust_level),
        "price_flexibility": clamp_score(price_flexibility),
        "follow_up_preference": follow_up,
        "do_not_contact_detected": do_not_contact,
        "legal_compliance_red_flags": legal_flags,
        "motivation_score_delta": clamp_score(motivation_delta),
        "contactability_score_delta": contactability_delta,
        "seller_temperature_update": clamp_score(50 + motivation_delta + price_flexibility / 4),
        "contract_readiness_influence": clamp_score(motivation_delta + price_flexibility / 3 - risk_delta / 2),
        "risk_score_influence": clamp_score(risk_delta),
        "call_quality_score": quality_score,
        "confidence_score": confidence,
        "quality_items": quality_items,
        "transcript_basis": {
            "asking_price": _basis(text, ["$", "price", "asking"]),
            "timeline": _basis(text, ["soon", "asap", "next week", "30 days", "no rush"]),
            "condition": _basis(text, condition_terms),
            "objections": {objection: _basis(text, OBJECTION_PATTERNS[objection]) for objection in objections},
            "legal_flags": legal_flags,
        },
    }

