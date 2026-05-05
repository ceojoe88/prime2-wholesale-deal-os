from __future__ import annotations

from pydantic import BaseModel, Field


class ProviderAttemptRequest(BaseModel):
    provider_id: str
    source_domain: str = ""
    action_type: str = ""
    mode: str = "mock"
    idempotency_key: str = ""
    request_metadata: dict[str, object] = Field(default_factory=dict)
    owner_approval_recorded: bool = False


class WebhookEventRequest(BaseModel):
    provider_type: str
    event_type: str
    mode: str = "mock"
    signature_present: bool = False
    signature_valid: bool = False
    payload_metadata: dict[str, object] = Field(default_factory=dict)

