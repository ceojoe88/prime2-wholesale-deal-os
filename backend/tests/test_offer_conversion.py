from fastapi.testclient import TestClient

from app.domain.offer_conversion import validate_conversion_language
from app.main import app


def test_readiness_score_and_contract_ready_state_work():
    with TestClient(app) as client:
        ready = client.get("/api/negotiations/negotiation-001")
        stalled = client.get("/api/negotiations/negotiation-004")

    assert ready.status_code == 200
    ready_body = ready.json()
    assert ready_body["readiness_score"] >= 85
    assert ready_body["readiness_level"] == "contract-ready"
    assert ready_body["automatic_acceptance_allowed"] is False

    assert stalled.status_code == 200
    stalled_body = stalled.json()
    assert stalled_body["readiness_level"] == "low readiness"
    assert stalled_body["live_negotiation_automation_allowed"] is False


def test_contract_ready_requires_all_gates():
    with TestClient(app) as client:
        response = client.get("/api/contract-ready")

    assert response.status_code == 200
    body = response.json()
    ready_ids = {state["id"] for state in body["contract_ready_deals"]}
    assert "contract-ready-001" in ready_ids
    blocked = {
        state["id"]: state
        for state in body["contract_ready_states"]
        if state["id"] != "contract-ready-001"
    }
    assert "owner_approval_not_recorded" in blocked["contract-ready-002"]["blocked_reasons"]
    assert "compliance_not_passed" in blocked["contract-ready-003"]["blocked_reasons"]
    assert "profit_control_not_validated" in blocked["contract-ready-004"]["blocked_reasons"]
    assert body["contract_execution_allowed"] is False
    assert body["executable_contract_generation_allowed"] is False


def test_offer_conversion_detail_persists_negotiation_tracking():
    with TestClient(app) as client:
        response = client.get("/api/offer-conversion/deal-001")

    assert response.status_code == 200
    body = response.json()
    assert body["offer_positioning"][0]["offer_strategy_type"] == "as-is"
    assert body["negotiations"][0]["seller_last_response"]
    assert body["negotiations"][0]["negotiation_stage"] == "soft-accepted"
    assert body["contract_ready_states"][0]["ready_for_external_drafting"] is True
    assert body["contract_ready_states"][0]["contract_execution_allowed"] is False


def test_conversion_safety_blocks_unsafe_language():
    result = validate_conversion_language(
        "This will sell today, I have buyers lined up, and you must sign now."
    )

    assert result["allowed"] is False
    assert "false_urgency" in result["risk_flags"]
    assert "fake_buyer_claim" in result["risk_flags"]
    assert "pressure_tactics" in result["risk_flags"]


def test_conversion_safety_blocks_legal_and_guaranteed_close_language():
    with TestClient(app) as client:
        response = client.post(
            "/api/offer-conversion/safety/validate",
            json={"content": "No attorney needed and we guarantee close."},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["allowed"] is False
    assert "legal_statement" in body["risk_flags"]
    assert "guaranteed_close_language" in body["risk_flags"]
