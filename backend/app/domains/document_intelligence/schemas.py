from __future__ import annotations

from pydantic import BaseModel, Field


class DocumentAnalyzeRequest(BaseModel):
    source_deal_id: str | None = None
    source_lead_id: str | None = None
    source_buyer_id: str | None = None
    uploaded_by: str = "Owner"
    original_filename: str = "document.txt"
    file_type: str = "text"
    storage_reference: str = ""
    manual_document_type: str | None = None
    pasted_text: str = ""
    manual_metadata: dict[str, object] = Field(default_factory=dict)
    use_ai_assist: bool = False

