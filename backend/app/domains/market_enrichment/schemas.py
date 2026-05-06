from __future__ import annotations

from pydantic import BaseModel, Field


class MarketProfileCreateRequest(BaseModel):
    market_id: str
    city: str
    state: str
    zip_code: str
    county: str = ""
    market_type: str = "unknown"
    median_estimated_value: int = 0
    average_days_on_market: int = 0
    buyer_demand_score: float = 0
    investor_activity_score: float = 0
    rental_demand_score: float = 0
    title_friction_score: float = 0
    competition_score: float = 0
    evidence_basis: list[str] = Field(default_factory=list)


class ComparableSaleCreateRequest(BaseModel):
    comp_id: str
    market_id: str
    deal_id: str | None = None
    address_summary: str = ""
    property_type: str = ""
    beds: int = 0
    baths: float = 0
    sqft: int = 0
    sale_price: int = 0
    sale_date: str = ""
    distance_miles: float = 0
    condition_notes: str = ""
    source: str = "manual"
    confidence_score: float = 0
    adjustment_notes: str = ""

