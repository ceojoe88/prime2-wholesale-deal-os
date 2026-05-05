from __future__ import annotations

from pydantic import BaseModel, Field


class CallIntelligenceAnalyzeRequest(BaseModel):
    lead_id: str
    input_type: str = "manual_call_notes"
    transcript_text: str
    call_outcome_id: str | None = None
    source_metadata: dict[str, object] = Field(default_factory=dict)
    use_ai_assist: bool = True

