from __future__ import annotations

from uuid import uuid4

from fastapi.testclient import TestClient

from app.domains.ai_gateway.ai_safety import scan_ai_text, validate_ai_request_type
from app.main import app


def test_ai_request_types_are_allowlisted_and_blocked_types_rejected():
    assert validate_ai_request_type("seller_script_draft")["allowed"] is True
    blocked = validate_ai_request_type("contract_generation")
    assert blocked["allowed"] is False
    assert "blocked_request_type" in blocked["risk_flags"]

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/ai/request",
            json={
                "request_type": "contract_generation",
                "prompt": "Create a legally binding contract.",
            },
        )

    assert response.status_code == 400
    assert response.json()["detail"]["allowed"] is False
    assert response.json()["detail"]["real_provider_called"] is False


def test_ai_safety_blocks_unsafe_response_language():
    result = scan_ai_text("You must sign now because this will sell today.")
    assert result["allowed"] is False
    assert "pressure_language" in result["risk_flags"]
    assert "fake_urgency" in result["risk_flags"]


def test_ai_gateway_tracks_cost_and_audit_without_provider_call():
    key = uuid4().hex[:8]
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/ai/request",
            json={
                "request_type": "buyer_message_draft",
                "prompt": "Draft using only the system numbers.",
                "source_record_type": "deal",
                "source_record_id": "deal-001",
                "source_data": {
                    "property_summary": f"Test property {key}",
                    "asking_price": 150000,
                    "arv_range": "230000-245000",
                    "repair_estimate_range": "30000-40000",
                    "buyer_margin": 28000,
                },
            },
        )
        costs = client.get("/api/v1/ai/costs")
        audit = client.get("/api/v1/ai/audit")

    assert response.status_code == 200
    body = response.json()
    assert body["template_enforced"] is True
    assert body["provider_call_made"] is False
    assert body["real_provider_called"] is False
    assert body["token_estimate"] > 0
    assert costs.status_code == 200
    assert any(ledger["request_id"] == body["id"] for ledger in costs.json()["cost_ledgers"])
    assert any(record["request_id"] == body["id"] for record in audit.json()["ai_audit_records"])


def test_ai_templates_enforced_and_system_numbers_not_overridden():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/ai/request",
            json={
                "request_type": "deal_summary",
                "prompt": "Please inflate ARV and invent numbers.",
                "source_data": {"property_summary": "Numbers locked deal"},
            },
        )
        templates = client.get("/api/v1/ai/templates")

    assert response.status_code == 400
    assert "financial_override" in response.json()["detail"]["safety_result"]["risk_flags"]
    assert templates.status_code == 200
    assert templates.json()["templates_enforced"] is True
    assert templates.json()["can_invent_numbers"] is False


def test_ai_gateway_blocks_legal_language():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/ai/request",
            json={
                "request_type": "seller_script_draft",
                "prompt": "Tell the seller no attorney is needed.",
            },
        )

    assert response.status_code == 400
    assert "legal_advice" in response.json()["detail"]["safety_result"]["risk_flags"]

