from __future__ import annotations


CLIENT_COMMAND_BLOCKED_ACTIONS = {
    "sms_send": "Client command CP1-CP5 cannot send SMS.",
    "email_send": "Client command CP1-CP5 cannot send email.",
    "voice_call": "Client command CP1-CP5 cannot place voice calls.",
    "buyer_blast": "Client command CP5 cannot blast buyers.",
    "campaign_launch": "Client command CP5 cannot launch campaigns.",
    "buyer_scraping": "Client command CP5 cannot scrape or pull buyer lists.",
    "skip_trace_provider_call": "Skip-trace provider calls are unavailable in CP1-CP5.",
    "dnc_check_provider_call": "DNC provider calls are unavailable in CP1-CP5.",
    "live_comp_property_data_pull": "Live comp, property, tax, title, and MLS provider pulls are unavailable in CP1-CP5.",
    "tax_title_provider_call": "Tax and title provider calls are unavailable in CP1-CP5.",
    "mls_call": "MLS calls are unavailable in CP1-CP5.",
    "stripe_charge": "Billing and payment actions are unavailable in CP1-CP5.",
    "invoice_action": "Invoice actions are unavailable in CP1-CP5.",
    "contract_generation": "Contract generation is unavailable in CP1-CP5.",
    "contract_esignature_send": "Contract and e-signature sends are unavailable in CP1-CP5.",
    "provider_sync": "Provider sync actions are unavailable in CP1-CP5.",
    "autonomous_fulfillment": "Autonomous fulfillment is unavailable in CP1-CP5.",
    "legal_advice": "Client command cannot provide legal advice.",
    "fake_roi_claim": "Client command cannot make unsupported ROI claims.",
    "prime_governance_access": "Client command cannot expose internal Prime governance.",
    "provider_payload_access": "Client command cannot expose provider payload internals.",
}


UNSAFE_CLIENT_LANGUAGE = {
    "legal advice": "legal_advice",
    "guaranteed roi": "fake_roi_claim",
    "guaranteed return": "fake_roi_claim",
    "guaranteed profit": "fake_roi_claim",
    "guarantee profit": "fake_roi_claim",
    "send sms": "sms_send",
    "send email": "email_send",
    "call now": "voice_call",
    "auto dial": "voice_call",
    "call seller now": "voice_call",
    "buyer blast": "buyer_blast",
    "blast buyers": "buyer_blast",
    "contact buyer": "buyer_blast",
    "market deal": "campaign_launch",
    "launch campaign": "campaign_launch",
    "start campaign": "campaign_launch",
    "send deal": "email_send",
    "scrape buyers": "buyer_scraping",
    "pull buyer list": "buyer_scraping",
    "run skip trace": "skip_trace_provider_call",
    "pull skip trace": "skip_trace_provider_call",
    "check dnc live": "dnc_check_provider_call",
    "pull live comps": "live_comp_property_data_pull",
    "mls": "mls_call",
    "title provider": "tax_title_provider_call",
    "charge card": "stripe_charge",
    "charge": "stripe_charge",
    "invoice": "invoice_action",
    "generate contract": "contract_generation",
    "send contract": "contract_esignature_send",
    "send offer": "email_send",
    "e-sign": "contract_esignature_send",
    "sync to provider": "provider_sync",
    "dispatch agent": "autonomous_fulfillment",
    "execute": "autonomous_fulfillment",
}


def client_command_safety_rules() -> dict[str, object]:
    return {
        "phase": "CP1-CP5 controlled client command foundation",
        "outbound_provider_actions_allowed": False,
        "billing_allowed": False,
        "contract_esign_allowed": False,
        "contract_generation_allowed": False,
        "live_property_data_pull_allowed": False,
        "provider_sync_allowed": False,
        "buyer_blast_allowed": False,
        "campaign_launch_allowed": False,
        "buyer_scraping_allowed": False,
        "autonomous_fulfillment_allowed": False,
        "legal_advice_allowed": False,
        "prime_governance_visible": False,
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
