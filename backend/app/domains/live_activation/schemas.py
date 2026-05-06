from __future__ import annotations

from pydantic import BaseModel, Field


class LiveActivationAttemptRequest(BaseModel):
    idempotency_key: str
    request_metadata: dict[str, object] = Field(default_factory=dict)
