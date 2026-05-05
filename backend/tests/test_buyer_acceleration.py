from fastapi.testclient import TestClient

from app.domain.buyer_acceleration import (
    buyer_distribution_gate,
    buyer_velocity_score,
    validate_buyer_sequence_text,
)
from app.main import app
from app.models import BuyerAccelerationRecord, BuyerVelocityProfile


def test_buyer_sequence_blocks_bulk_blast_and_unsafe_claims():
    result = validate_buyer_sequence_text(
        "Buyer blast this to all buyers. This will sell today and we already have multiple offers."
    )

    assert result["allowed"] is False
    assert "bulk_blast" in result["risk_flags"]
    assert "deceptive_scarcity" in result["risk_flags"]
    assert "fake_competition" in result["risk_flags"]


def test_buyer_acceleration_sanitized_only_and_draft_sequences():
    with TestClient(app) as client:
        response = client.get("/api/buyer-acceleration/deal-001")

    assert response.status_code == 200
    body = response.json()
    assert body["controlled_send_allowed"] is True
    assert body["bulk_blast_allowed"] is False
    assert body["seller_private_data_exposed"] is False
    assert body["internal_profit_logic_exposed"] is False
    for sequence in body["buyer_sequences"]:
        assert sequence["draft_only"] is True
        assert sequence["live_send_allowed"] is False
        assert sequence["bulk_blast_allowed"] is False
        assert sequence["seller_private_data_exposed"] is False
        assert sequence["internal_profit_logic_exposed"] is False


def test_controlled_send_requires_v5_and_v13_gate_stack():
    record = BuyerAccelerationRecord(
        id="buyer-accel-test",
        deal_id="deal-001",
        pof_status="verified",
        buyer_reliability=92,
        buyer_margin_strength=91,
        owner_approval_status="approved",
        buyer_visible=True,
        sanitized_deal_sheet_ready=True,
        buyer_match_approved=True,
        compliance_passed=True,
        v13_gate_passed=False,
        v5_gate_passed=False,
    )

    gate = buyer_distribution_gate(record)

    assert gate["controlled_send_allowed"] is False
    assert "v13_gate_not_passed" in gate["blocked_reasons"]
    assert "v5_gate_not_passed" in gate["blocked_reasons"]


def test_buyer_response_router_routes_pof_gaps():
    with TestClient(app) as client:
        response = client.get("/api/buyer-response-router")

    assert response.status_code == 200
    body = response.json()
    assert body["draft_only"] is True
    assert body["contract_execution_allowed"] is False
    assert any(route["response_type"] == "needs_pof" for route in body["needs_pof"])
    assert all(route["pof_gap"] is True for route in body["needs_pof"])


def test_buyer_velocity_score_calculates_fast_close_priority():
    profile = BuyerVelocityProfile(
        id="velocity-test",
        buyer_id="buyer-001",
        response_speed=95,
        pof_strength=95,
        close_history=90,
        price_fit=90,
        market_fit=95,
        reliability=90,
        previous_intent_quality=85,
    )

    score = buyer_velocity_score(profile)

    assert score >= 90
    assert profile.recommended_use == "fast_close_priority"


def test_buyer_acceleration_routes_render_backend():
    routes = [
        "/api/buyer-acceleration",
        "/api/buyer-sequences",
        "/api/buyer-response-router",
        "/api/buyer-velocity",
    ]
    with TestClient(app) as client:
        for route in routes:
            response = client.get(route)
            assert response.status_code == 200, route

