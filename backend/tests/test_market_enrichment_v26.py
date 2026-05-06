from __future__ import annotations

from fastapi.testclient import TestClient

from app.domains.market_enrichment.scoring import (
    buyer_activity_demand_confidence,
    comp_based_arv_confidence,
    lead_source_roi_gate,
    market_heat_score,
)
from app.main import app
from app.models import BuyerActivitySnapshot, ComparableSaleRecord, LeadSourceROIRecord, MarketProfile


def test_market_scoring_uses_demand_source_quality_and_friction():
    profile = MarketProfile(
        market_id="test-market",
        city="Dallas",
        state="TX",
        zip_code="75216",
        buyer_demand_score=85,
        investor_activity_score=88,
        rental_demand_score=74,
        title_friction_score=20,
        competition_score=40,
    )
    score = market_heat_score(profile, lead_quality=82, spread_potential=70)
    assert score >= 75
    profile.competition_score = 95
    profile.title_friction_score = 90
    assert market_heat_score(profile, lead_quality=82, spread_potential=70) < score


def test_comp_based_arv_confidence_rewards_recent_nearby_comps():
    good_comps = [
        ComparableSaleRecord(
            comp_id="good-1",
            market_id="test-market",
            sale_date="2026-01-10",
            distance_miles=0.4,
            confidence_score=90,
        ),
        ComparableSaleRecord(
            comp_id="good-2",
            market_id="test-market",
            sale_date="2026-02-10",
            distance_miles=0.8,
            confidence_score=84,
        ),
        ComparableSaleRecord(
            comp_id="good-3",
            market_id="test-market",
            sale_date="2025-11-10",
            distance_miles=1.1,
            confidence_score=78,
        ),
    ]
    stale = [
        ComparableSaleRecord(
            comp_id="stale-1",
            market_id="test-market",
            sale_date="2022-03-10",
            distance_miles=3.5,
            confidence_score=42,
        )
    ]
    good = comp_based_arv_confidence(good_comps, market_confidence=80)
    weak = comp_based_arv_confidence(stale, market_confidence=40)
    missing = comp_based_arv_confidence([], market_confidence=80)
    assert good["arv_confidence"] > weak["arv_confidence"]
    assert missing["arv_confidence"] == 20
    assert "stale_or_missing_comps_lower_confidence" in weak["basis"]


def test_buyer_activity_snapshot_updates_demand_confidence():
    strong = BuyerActivitySnapshot(
        id="snap-strong",
        market_id="test-market",
        active_buyer_count=8,
        pof_verified_buyer_count=6,
        fast_close_buyer_count=4,
        buyer_response_velocity=86,
        recent_interest_count=5,
    )
    weak = BuyerActivitySnapshot(
        id="snap-weak",
        market_id="test-market",
        active_buyer_count=1,
        pof_verified_buyer_count=0,
        fast_close_buyer_count=0,
        buyer_response_velocity=25,
        recent_interest_count=0,
    )
    assert buyer_activity_demand_confidence(strong) > buyer_activity_demand_confidence(weak)


def test_lead_source_roi_requires_evidence_and_blocks_guarantee_language():
    record = LeadSourceROIRecord(
        id="roi-test",
        source_name="vacant",
        market_id="test-market",
        leads_imported=0,
        evidence_basis=[],
        guaranteed_roi_allowed=True,
    )
    gate = lead_source_roi_gate(record)
    assert gate["allowed_for_strategy"] is False
    assert "source_evidence_required" in gate["blocked_reasons"]
    assert "leads_imported_required" in gate["blocked_reasons"]
    assert "guaranteed_roi_language_blocked" in gate["blocked_reasons"]
    assert gate["estimate_only"] is True
    assert gate["guaranteed_roi_allowed"] is False


def test_market_enrichment_routes_render_and_preserve_boundaries():
    with TestClient(app) as client:
        dashboard = client.get("/api/v1/market-enrichment")
        comps = client.get("/api/v1/market-enrichment/comps")
        rents = client.get("/api/v1/market-enrichment/rent-estimates")
        activity = client.get("/api/v1/market-enrichment/buyer-activity")
        roi = client.get("/api/v1/market-enrichment/lead-source-roi")
        ranking = client.get("/api/v1/market-enrichment/ranking")

    assert dashboard.status_code == 200
    assert comps.status_code == 200
    assert rents.status_code == 200
    assert activity.status_code == 200
    assert roi.status_code == 200
    assert ranking.status_code == 200
    body = dashboard.json()
    assert body["manual_or_imported_data_only"] is True
    assert body["paid_external_api_calls"] is False
    assert body["guaranteed_roi_allowed"] is False
    assert body["integration_signals"]["underwriting_arv_confidence"] is True
