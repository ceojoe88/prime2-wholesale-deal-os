from fastapi.testclient import TestClient

from app.domain.optimization import (
    agent_performance_overall,
    validate_learning_record,
    validate_optimization_claim,
)
from app.main import app
from app.models import AgentPerformanceScore, OutcomeLearningRecord


def test_learning_records_require_source_evidence():
    record = OutcomeLearningRecord(
        id="learning-test",
        lead_source="vacant",
        market="75217",
        conversion_result="stalled",
        projected_assignment_fee=11000,
        source_records_present=False,
        source_evidence_ids=[],
    )

    gate = validate_learning_record(record)

    assert gate["allowed"] is False
    assert "source_evidence_required" in gate["blocked_reasons"]
    assert "projected_fee_needs_source_records" in gate["blocked_reasons"]


def test_optimization_recommendations_are_explainable():
    with TestClient(app) as client:
        response = client.get("/api/optimization/recommendations")

    assert response.status_code == 200
    body = response.json()
    assert body["explainable_recommendations_only"] is True
    for recommendation in body["optimization_recommendations"]:
        assert recommendation["explainable"] is True
        assert recommendation["source_record_ids"]
        assert recommendation["explanation"]
        assert recommendation["guaranteed_revenue_claim_allowed"] is False


def test_fake_revenue_and_unsupported_roi_claims_blocked():
    result = validate_optimization_claim(
        "This is guaranteed revenue with guaranteed ROI and a risk-free return."
    )

    assert result["allowed"] is False
    assert "guaranteed_revenue" in result["risk_flags"]
    assert "unsupported_roi" in result["risk_flags"]


def test_scoring_changes_are_logged():
    with TestClient(app) as client:
        response = client.get("/api/optimization/source-quality")

    assert response.status_code == 200
    body = response.json()
    assert body["changes_logged"] >= 3
    assert all(change["explanation"] for change in body["scoring_weight_changes"])


def test_agent_performance_calculates_deterministically():
    score = AgentPerformanceScore(
        id="agent-score-test",
        quality_score=90,
        conversion_score=80,
        accuracy_score=85,
        effectiveness_score=82,
        compliance_block_rate=10,
        follow_up_score=78,
        recommendation_accuracy=84,
    )

    overall = agent_performance_overall(score)

    assert overall > 80
    assert score.overall_score == overall


def test_optimization_routes_render_backend():
    routes = [
        "/api/optimization",
        "/api/optimization/patterns",
        "/api/optimization/recommendations",
        "/api/optimization/agent-performance",
        "/api/optimization/lost-deals",
        "/api/optimization/source-quality",
    ]
    with TestClient(app) as client:
        for route in routes:
            response = client.get(route)
            assert response.status_code == 200, route

