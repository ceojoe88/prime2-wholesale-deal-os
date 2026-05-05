from __future__ import annotations


DNC_PATTERNS = [
    "do not contact",
    "don't contact",
    "stop calling",
    "remove me",
    "take me off your list",
    "do not call",
]

LEGAL_REQUEST_PATTERNS = [
    "is this legal",
    "what does the contract mean",
    "legal meaning",
    "legal advice",
    "attorney",
    "lawyer",
]

UNSAFE_RESPONSE_PATTERNS = {
    "pressure_language": ["must sign", "sign now", "you must", "last chance"],
    "fake_urgency": ["today only", "this will sell today", "act immediately"],
    "fake_buyer_claim": ["buyers lined up", "guaranteed buyer", "buyers are fighting"],
    "guaranteed_close": ["guaranteed close", "will definitely close"],
    "misleading_assignment": ["hide the assignment", "do not disclose"],
}


def detect_do_not_contact(text: str) -> bool:
    lowered = text.lower()
    return any(pattern in lowered for pattern in DNC_PATTERNS)


def detect_legal_request(text: str) -> list[str]:
    lowered = text.lower()
    return [pattern for pattern in LEGAL_REQUEST_PATTERNS if pattern in lowered]


def scan_call_response_safety(text: str) -> dict[str, object]:
    lowered = text.lower()
    flags = sorted(
        {
            category
            for category, patterns in UNSAFE_RESPONSE_PATTERNS.items()
            if any(pattern in lowered for pattern in patterns)
        }
    )
    return {
        "allowed": not flags,
        "risk_flags": flags,
        "blocked_reasons": flags,
        "live_response_allowed": False,
    }

