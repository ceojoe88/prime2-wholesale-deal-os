from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class MobileNoteCreate(BaseModel):
    note_type: str = "field_note"
    source_record_type: str = ""
    source_record_id: str = ""
    body: str
    offline_created: bool = False
    idempotency_key: str | None = None


class MobileCallOutcomeCreate(BaseModel):
    lead_id: str
    contact_result: str = "no_answer"
    motivation_notes: str = ""
    asking_price: int | None = None
    timeline: str = ""
    property_condition_notes: str = ""
    seller_objections: list[str] = Field(default_factory=list)
    seller_temperature: float = 0
    next_follow_up_date: datetime | None = None
    operator_notes: str = ""


class MobileDncMark(BaseModel):
    lead_id: str
    notes: str = "Owner marked do-not-contact from mobile field mode."


class MobileOfflineDraftCreate(BaseModel):
    draft_type: str = "field_note"
    source_record_type: str = ""
    source_record_id: str = ""
    payload: dict[str, Any] = Field(default_factory=dict)
    idempotency_key: str


class MobileApprovalGateCheck(BaseModel):
    approval_type: str
    source_record_type: str
    source_record_id: str
    safety_status: str = "missing"
    dry_run_receipt_id: str = ""
    provider_readiness_status: str = "missing"
    idempotency_key: str
    owner_approval_recorded: bool = False
