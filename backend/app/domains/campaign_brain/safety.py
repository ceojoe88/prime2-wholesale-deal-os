from __future__ import annotations

from app.models import CampaignRuleRecord, CampaignSequenceStep


CAMPAIGN_UNSAFE_PATTERNS: dict[str, list[str]] = {
    "deceptive_scarcity": ["this will sell today", "last chance", "buyers are fighting over this"],
    "fake_urgency": ["act immediately", "today only", "offer expires in minutes"],
    "fake_claim": ["we already have a buyer", "guaranteed buyer", "guaranteed close"],
    "guaranteed_profit": ["guaranteed profit", "guaranteed roi", "risk-free return"],
    "pressure_language": ["you must sign", "sign now", "take it or leave it"],
    "legal_contract_language": ["binding contract", "no attorney needed", "execute contract"],
    "bulk_blast": ["send all", "blast", "bulk send", "campaign blast"],
}

REQUIRED_STOP_CONDITIONS = {
    "recipient_replies",
    "dnc_detected",
    "compliance_risk_detected",
    "provider_readiness_fails",
    "owner_pauses",
    "max_attempts_reached",
}


def scan_campaign_text(text: str) -> dict[str, object]:
    lowered = text.lower()
    flags = sorted(
        {
            category
            for category, phrases in CAMPAIGN_UNSAFE_PATTERNS.items()
            if any(phrase in lowered for phrase in phrases)
        }
    )
    return {
        "allowed": not flags,
        "risk_flags": flags,
        "blocked_reason": ", ".join(flags),
        "bulk_blast_allowed": False,
        "deceptive_scarcity_allowed": False,
        "guaranteed_profit_language_allowed": False,
    }


def campaign_rule_gate(rule: CampaignRuleRecord) -> dict[str, object]:
    flags: list[str] = []
    if rule.owner_approval_status != "approved":
        flags.append("owner_approval_required")
    if not rule.approved_template_ids:
        flags.append("approved_templates_required")
    if rule.max_recipients_per_day <= 0:
        flags.append("max_daily_cap_required")
    if rule.max_messages_per_recipient <= 0:
        flags.append("max_messages_per_recipient_required")
    if not rule.stop_conditions:
        flags.append("stop_conditions_required")
    missing_stops = sorted(REQUIRED_STOP_CONDITIONS.difference(set(rule.stop_conditions)))
    if missing_stops:
        flags.append("required_stop_conditions_missing")
    if not rule.audience_preview_approved:
        flags.append("audience_preview_approval_required")
    if not rule.dnc_guard_enabled:
        flags.append("dnc_guard_required")
    if not rule.compliance_guard_enabled:
        flags.append("compliance_guard_required")
    if rule.bulk_blast_allowed:
        flags.append("bulk_blast_blocked")
    if not rule.one_message_event_model:
        flags.append("one_message_event_model_required")
    if rule.live_send_allowed:
        flags.append("live_send_requires_v5_v13_v22_runtime_gates")
    text_scan = scan_campaign_text(f"{rule.name} {rule.segment_definition}")
    flags.extend(str(flag) for flag in text_scan["risk_flags"])
    return {
        "allowed": not flags,
        "blocked_reasons": sorted(set(flags)),
        "status": "ready" if not flags else "blocked",
        "live_send_allowed": False,
        "bulk_blast_allowed": False,
    }


def sequence_step_safety(step: CampaignSequenceStep) -> dict[str, object]:
    result = scan_campaign_text(step.message_purpose)
    flags = list(result["risk_flags"])
    if step.bulk_send_allowed:
        flags.append("bulk_send_blocked")
    if step.deceptive_scarcity_allowed:
        flags.append("deceptive_scarcity_enabled")
    return {
        "allowed": not flags,
        "risk_flags": sorted(set(flags)),
        "blocked_reason": ", ".join(sorted(set(flags))),
        "live_send_allowed": False,
        "draft_only": True,
    }

