from __future__ import annotations

from pydantic import BaseModel, Field


class ClientLeadScoreRequest(BaseModel):
    workspace_id: str | None = None
    refresh: bool = False


class ClientWorkspaceCreate(BaseModel):
    workspace_name: str
    client_name: str = ""
    market_focus: list[str] = Field(default_factory=list)


class ClientBuyerProfileCreate(BaseModel):
    buyer_name: str = "Manual Buyer"
    buyer_company: str | None = None
    buyer_type: str = "unknown"
    primary_market: str = ""
    target_zip_codes: list[str] = Field(default_factory=list)
    preferred_property_types: list[str] = Field(default_factory=list)
    min_price: int | None = None
    max_price: int | None = None
    rehab_tolerance: str = "unknown"
    close_speed: str = "unknown"
    funding_status: str = "unknown"
    proof_of_funds_status: str = "missing"
    communication_preference: str = "unknown"
    active_status: str = "needs_review"
    notes_summary: str = ""


class ClientBuyerBuyBoxCreate(BaseModel):
    market: str = ""
    zip_codes: list[str] = Field(default_factory=list)
    property_types: list[str] = Field(default_factory=list)
    min_beds: int | None = None
    min_baths: float | None = None
    min_sqft: int | None = None
    max_purchase_price: int | None = None
    min_purchase_price: int | None = None
    rehab_level: str = "unknown"
    occupancy_preference: str = "unknown"
    deal_type_preference: str = "unknown"
    notes_summary: str = ""


class ClientBuyerDemandEvidenceCreate(BaseModel):
    buyer_id: str | None = None
    evidence_type: str = "manual_client_note"
    evidence_summary: str = ""
    source_type: str = "manual"
    confidence_level: str = "medium"


class ClientBuyerOutreachDraftCreate(BaseModel):
    buyer_id: str | None = None
    draft_type: str = "deal_preview"
    purpose: str = "manual buyer preview"
