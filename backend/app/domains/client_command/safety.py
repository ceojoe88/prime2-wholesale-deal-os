from __future__ import annotations


CLIENT_COMMAND_BLOCKED_ACTIONS = {
    "sms_send": "Client command CP1/CP2 cannot send SMS.",
    "email_send": "Client command CP1/CP2 cannot send email.",
    "voice_call": "Client command CP1/CP2 cannot place voice calls.",
    "skip_trace_provider_call": "Skip-trace provider calls are unavailable in CP1/CP2.",
    "dnc_check_provider_call": "DNC provider calls are unavailable in CP1/CP2.",
    "stripe_charge": "Billing and Stripe charges are unavailable in CP1/CP2.",
    "contract_esignature_send": "Contract and e-signature sends are unavailable in CP1/CP2.",
    "legal_advice": "Client command cannot provide legal advice.",
    "fake_roi_claim": "Client command cannot make unsupported ROI claims.",
    "internal_prime_governance_access": "Client command cannot expose internal Prime governance.",
    "provider_payload_access": "Client command cannot expose provider payload internals.",
}


UNSAFE_CLIENT_LANGUAGE = {
    "legal advice": "legal_advice",
    "guaranteed roi": "fake_roi_claim",
    "guaranteed return": "fake_roi_claim",
    "guaranteed profit": "fake_roi_claim",
    "send sms": "sms_send",
    "send email": "email_send",
    "call seller now": "voice_call",
    "run skip trace": "skip_trace_provider_call",
    "charge card": "stripe_charge",
    "send contract": "contract_esignature_send",
}


def client_command_safety_rules() -> dict[str, object]:
    return {
        "phase": "CP1/CP2 controlled foundation",
        "outbound_provider_actions_allowed": False,
        "billing_allowed": False,
        "contract_esign_allowed": False,
        "legal_advice_allowed": False,
        "internal_prime_governance_exposed": False,
        "provider_payload_internals_visible": False,
        "blocked_actions": CLIENT_COMMAND_BLOCKED_ACTIONS,
    }


def validate_client_safe_text(text: str) -> dict[str, object]:
    lowered = text.lower()
    flags = sorted({flag for phrase, flag in UNSAFE_CLIENT_LANGUAGE.items() if phrase in lowered})
    return {
        "allowed": not flags,
        "risk_flags": flags,
        "blocked_reason": ", ".join(flags),
    }
