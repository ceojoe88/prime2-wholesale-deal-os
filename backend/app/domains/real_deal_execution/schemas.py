from __future__ import annotations

from pydantic import BaseModel, Field


class RealDealExecutionBatchCreate(BaseModel):
    batch_name: str
    lead_import_batch_id: str | None = None
    market_zip_focus: list[str] = Field(default_factory=list)
    target_assignment_fee: int = 10_000
    owner_notes: str = ""


class RealDealExecutionBatchStatusUpdate(BaseModel):
    batch_status: str
    owner_notes: str | None = None
