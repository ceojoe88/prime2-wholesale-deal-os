from __future__ import annotations

from typing import Iterable


ALLOWED_AI_REQUEST_TYPES = {
    "seller_script_draft",
    "buyer_message_draft",
    "objection_response",
    "deal_summary",
    "daily_briefing",
    "negotiation_assist",
    "field_testing_summary",
}

BLOCKED_AI_REQUEST_TYPES = {
    "legal_advice",
    "contract_generation",
    "purchase_agreement",
    "assignment_contract",
    "closing_instruction",
    "profit_guarantee",
    "financial_calculation_override",
}

AI_UNSAFE_PATTERNS: dict[str, list[str]] = {
    "legal_advice": [
        "this is legal advice",
        "no attorney needed",
        "no attorney is needed",
        "you are legally required",
        "legal conclusion",
        "attorney-client relationship",
    ],
    "contract_generation": [
        "legally binding",
        "binding contract",
        "execute this contract",
        "signature block",
        "purchase agreement terms",
    ],
    "pressure_language": [
        "you must",
        "must sign",
        "sign now",
        "take it or leave it",
        "do not talk to anyone else",
    ],
    "fake_urgency": [
        "last chance",
        "offer expires in minutes",
        "this will sell today",
        "act immediately",
        "today only",
    ],
    "fake_scarcity": [
        "buyers are fighting over this",
        "multiple buyers already committed",
        "we have guaranteed buyers lined up",
    ],
    "guaranteed_profit_claim": [
        "guarantee",
        "guaranteed profit",
        "risk free",
        "will definitely close",
    ],
    "role_misrepresentation": [
        "we are the end buyer",
        "hide the assignment",
        "do not disclose the assignment",
        "do not mention our role",
    ],
    "financial_override": [
        "fake arv",
        "inflate arv",
        "change the repair estimate",
        "make the repairs lower",
        "alter the numbers",
        "invent numbers",
    ],
}


def _scan(text: str, patterns: dict[str, Iterable[str]]) -> list[str]:
    lowered = text.lower()
    return sorted(
        {
            category
            for category, phrases in patterns.items()
            if any(phrase in lowered for phrase in phrases)
        }
    )


def validate_ai_request_type(request_type: str) -> dict[str, object]:
    normalized = request_type.strip().lower()
    flags: list[str] = []
    if normalized in BLOCKED_AI_REQUEST_TYPES:
        flags.append("blocked_request_type")
    if normalized not in ALLOWED_AI_REQUEST_TYPES:
        flags.append("unsupported_request_type")
    return {
        "allowed": not flags,
        "request_type": normalized,
        "risk_flags": flags,
        "blocked_reason": ", ".join(flags),
    }


def scan_ai_text(content: str) -> dict[str, object]:
    flags = _scan(content, AI_UNSAFE_PATTERNS)
    return {
        "allowed": not flags,
        "risk_flags": flags,
        "blocked_reason": ", ".join(flags),
        "legal_advice_allowed": False,
        "contract_generation_allowed": False,
        "financial_calculation_override_allowed": False,
    }


def combine_safety_results(*results: dict[str, object]) -> dict[str, object]:
    flags = sorted(
        {
            str(flag)
            for result in results
            for flag in result.get("risk_flags", [])
        }
    )
    return {
        "allowed": not flags,
        "risk_flags": flags,
        "blocked_reason": ", ".join(flags),
        "legal_advice_allowed": False,
        "contract_generation_allowed": False,
        "financial_calculation_override_allowed": False,
    }
