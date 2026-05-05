from __future__ import annotations

import os
from datetime import UTC, datetime

from app.models import ProviderRegistry


SUPPORTED_PROVIDER_TYPES = {
    "openai",
    "email",
    "sms",
    "crm",
    "skip_trace",
    "storage",
    "webhook",
}

SUPPORTED_PROVIDER_MODES = {"mock", "sandbox", "live"}
PRIME2_ALLOWED_PROVIDER_TYPES = SUPPORTED_PROVIDER_TYPES


def credential_present_from_env(reference_name: str) -> bool:
    reference = reference_name.strip()
    if not reference:
        return False
    return bool(os.getenv(reference))


def provider_readiness(
    provider: ProviderRegistry | None,
    *,
    requested_mode: str | None = None,
    owner_approval_recorded: bool = False,
) -> dict[str, object]:
    if provider is None:
        return {
            "status": "unsupported",
            "ready": False,
            "blocked_reasons": ["provider_not_registered"],
            "provider_calls_allowed": False,
            "real_network_call_allowed": False,
        }

    mode = (requested_mode or provider.provider_mode or "mock").strip().lower()
    reasons: list[str] = []
    status = "ready"

    if provider.provider_type not in SUPPORTED_PROVIDER_TYPES:
        reasons.append("unsupported_provider_type")
        status = "unsupported"
    if mode not in SUPPORTED_PROVIDER_MODES:
        reasons.append("unsupported_provider_mode")
        status = "unsupported"
    if provider.provider_type not in PRIME2_ALLOWED_PROVIDER_TYPES:
        reasons.append("provider_type_blocked_by_prime2_policy")
        status = "blocked"
    if not provider.enabled:
        reasons.append("provider_disabled")
        status = "disabled"

    credential_present = provider.credential_present
    if mode in {"sandbox", "live"}:
        if not provider.credential_reference_name:
            reasons.append("credential_reference_required")
            status = "missing_credentials"
        else:
            credential_present = credential_present_from_env(provider.credential_reference_name)
            if not credential_present:
                reasons.append("credential_env_value_missing")
                status = "missing_credentials"

    if mode == "sandbox" and not provider.sandbox_enabled:
        reasons.append("sandbox_flag_required")
        if status == "ready":
            status = "blocked"
    if mode == "live":
        if not provider.live_enabled:
            reasons.append("live_flag_required")
            status = "blocked"
        if provider.owner_approval_required and not owner_approval_recorded:
            reasons.append("owner_approval_required_for_live")
            status = "owner_approval_required"
    if provider.raw_secret_value_stored:
        reasons.append("raw_secret_storage_blocked")
        status = "blocked"

    provider.credential_present = credential_present
    provider.readiness_status = "ready" if not reasons else status
    provider.blocked_reason = ", ".join(sorted(set(reasons)))
    provider.last_checked_at = datetime.now(UTC)
    provider.live_network_call_allowed = False

    return {
        "status": provider.readiness_status,
        "ready": not reasons,
        "mode": mode,
        "blocked_reasons": sorted(set(reasons)),
        "credential_present": credential_present,
        "provider_calls_allowed": False,
        "real_network_call_allowed": False,
        "owner_approval_required": provider.owner_approval_required,
    }

