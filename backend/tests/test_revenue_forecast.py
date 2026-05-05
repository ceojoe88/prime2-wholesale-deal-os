from fastapi.testclient import TestClient

from app.domain.revenue_forecast import (
    calculate_deal_probability,
    calculate_market_scaling,
    validate_forecast_language,
    validate_lead_spend_plan,
)
from app.main import app
from app.models import DealProbabilityRecord, LeadSpendPlan, MarketScalingScore


def test_forecast_requires_source_records_and_estimate_label():
    with TestClient(app) as client:
        response = client.get("/api/revenue-forecast/forecast-2026-05")

    assert response.status_code == 200
    body = response.json()
    assert body["source_basis"]
    assert body["forecasts_are_estimates"] is True
    assert body["guaranteed_revenue_allowed"] is False
    assert "Estimate only" in body["estimate_label"]


def test_no_guaranteed_revenue_or_unsupported_roi_language():
    result = validate_forecast_language(
        "This is guaranteed revenue with guaranteed ROI and invented close probability."
    )

    assert result["allowed"] is False
    assert "guaranteed_revenue" in result["risk_flags"]
    assert "unsupported_roi" in result["risk_flags"]
    assert result["forecasts_are_estimates"] is True


def test_probability_adjusted_revenue_and_scenarios_work():
    with TestClient(app) as client:
        response = client.get("/api/revenue-forecast")

    assert response.status_code == 200
    body = response.json()
    forecast = body["revenue_forecasts"][0]
    assert forecast["conservative_forecast"] < forecast["base_forecast"]
    assert forecast["aggressive_forecast"] > forecast["base_forecast"]
    assert body["pipeline_value"]["probability_adjusted_revenue"] > 0


def test_deal_probability_engine_scores_inputs():
    record = DealProbabilityRecord(
        id="probability-test",
        deal_id="deal-001",
        seller_readiness=90,
        buyer_demand=90,
        underwriting_confidence=90,
        compliance_status_score=90,
        title_review_readiness=85,
        blocker_severity=5,
        buyer_pof_strength=95,
        communication_momentum=85,
    )

    score = calculate_deal_probability(record)

    assert score >= 80
    assert record.probability_band == "high_estimate"
    assert record.estimate_only is True


def test_market_scaling_score_and_spend_guard():
    market = MarketScalingScore(
        id="market-test",
        market_zip="75216",
        lead_volume=40,
        hot_lead_percentage=40,
        buyer_demand=95,
        average_spread=21000,
        conversion_rate=28,
        title_compliance_friction=15,
        competition_risk=35,
        source_record_ids=["learning-001"],
    )
    plan = LeadSpendPlan(
        id="spend-test",
        target_zip_codes=["75216"],
        lead_types=["absentee owner"],
        max_monthly_spend=1000,
        expected_deal_count=1,
        break_even_assignment_target=10000,
        evidence_basis=["market-test"],
    )

    assert calculate_market_scaling(market) >= 70
    assert validate_lead_spend_plan(plan)["allowed"] is True


def test_unsupported_lead_spend_is_blocked():
    plan = LeadSpendPlan(
        id="spend-blocked",
        max_monthly_spend=2500,
        break_even_assignment_target=0,
        evidence_basis=[],
        unsupported_spend_recommended=True,
    )

    gate = validate_lead_spend_plan(plan)

    assert gate["allowed"] is False
    assert "evidence_basis_required" in gate["blocked_reasons"]
    assert "unsupported_spend_recommended" in gate["blocked_reasons"]


def test_revenue_forecast_routes_render_backend():
    routes = [
        "/api/revenue-forecast",
        "/api/revenue-forecast/forecast-2026-05",
        "/api/market-scaling",
        "/api/lead-spend-planner",
        "/api/pipeline-value",
    ]
    with TestClient(app) as client:
        for route in routes:
            response = client.get(route)
            assert response.status_code == 200, route

