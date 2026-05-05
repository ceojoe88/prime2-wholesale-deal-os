from __future__ import annotations

from app.models import ProviderAttemptAudit, ProviderRegistry, ProviderWebhookEvent
from app.serializers import model_to_dict


SECRET_HINTS = {"key", "token", "secret", "password", "credential"}


def mask_credential_reference(reference_name: str) -> str:
    if not reference_name:
        return ""
    if len(reference_name) <= 6:
        return "***"
    return f"{reference_name[:3]}***{reference_name[-3:]}"


def contains_secret_like_value(value: object) -> bool:
    text = str(value or "")
    lowered = text.lower()
    return any(hint in lowered for hint in SECRET_HINTS) and "=" in text


def sanitize_provider_registry(provider: ProviderRegistry) -> dict[str, object]:
    data = model_to_dict(provider)
    reference = str(data.pop("credential_reference_name", "") or "")
    data.pop("raw_secret_value_stored", None)
    data["credential_reference_masked"] = mask_credential_reference(reference)
    data["credential_reference_present"] = bool(reference)
    data["raw_secret_stored"] = False
    data["live_network_call_allowed"] = False
    return data


def sanitize_provider_attempt(attempt: ProviderAttemptAudit) -> dict[str, object]:
    data = model_to_dict(attempt)
    data["provider_called"] = False
    data["real_network_call_made"] = False
    return data


def sanitize_webhook_event(event: ProviderWebhookEvent) -> dict[str, object]:
    data = model_to_dict(event)
    data["deal_mutation_allowed"] = False
    data["deal_mutated"] = False
    data["raw_payload_stored"] = False
    return data
