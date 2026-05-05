from __future__ import annotations

from pydantic import BaseModel, Field


class CampaignCreateRequest(BaseModel):
    name: str
    campaign_type: str = "seller_follow_up"
    audience_type: str = "seller"
    segment_definition: dict[str, object] = Field(default_factory=dict)
    approved_template_ids: list[str] = Field(default_factory=list)
    max_recipients_per_day: int = 0
    max_messages_per_recipient: int = 1
    send_window_start: str = ""
    send_window_end: str = ""
    cooldown_hours: int = 24
    stop_conditions: list[str] = Field(default_factory=list)
    owner_approval_status: str = "pending"
    live_send_allowed: bool = False
    audience_preview_approved: bool = False


class CampaignActivationRequest(BaseModel):
    idempotency_key: str | None = None
    live_send_requested: bool = False
    v5_gate_passed: bool = False
    v13_gate_passed: bool = False
    v22_gate_passed: bool = False
    provider_readiness_passed: bool = False
    live_flag_enabled: bool = False


class CampaignStopEventRequest(BaseModel):
    recipient_id: str = ""
    event_type: str
    reason: str = ""

