from __future__ import annotations

from pydantic import BaseModel, Field


class PrimeMemoryCreateRequest(BaseModel):
    memory_id: str
    memory_type: str
    source_domain: str
    source_record_id: str
    summary: str
    evidence_basis: list[str] = Field(default_factory=list)
    confidence_score: float = 0
    impact_area: str = ""
    status: str = "active"


class LearningSignalCreateRequest(BaseModel):
    signal_id: str
    signal_type: str
    source_domain: str
    source_record_id: str
    predicted_value: str
    actual_value: str
    evidence_basis: list[str] = Field(default_factory=list)

