from uuid import uuid4

from fastapi.testclient import TestClient

from app.domain.auto_execution import auto_execution_gate, validate_auto_execution_template
from app.main import app
from app.models import ApprovedTemplate, AutoExecutionRule


def test_auto_execution_requires_approved_rule_and_template():
    gate = auto_execution_gate(None, None)

    assert gate["can_execute"] is False
    assert "approved_rule_missing" in gate["blocked_reasons"]
    assert "approved_template_missing" in gate["blocked_reasons"]


def test_auto_execution_blocks_unsafe_language():
    template = ApprovedTemplate(
        id="test-unsafe-template",
        template_name="Unsafe",
        template_type="seller_follow_up",
        channel="sms",
        recipient_type="seller",
        body="You must sign now. This is your last chance and we already have a buyer.",
        approved=True,
        requires_opt_out=True,
        includes_opt_out=False,
    )

    result = validate_auto_execution_template(template)

    assert result["allowed"] is False
    assert "pressure_language" in result["risk_flags"]
    assert "fake_buyer_claim" in result["risk_flags"]
    assert "missing_sms_opt_out" in result["risk_flags"]


def test_no_live_action_without_v5_gate_stack():
    rule = AutoExecutionRule(
        id="rule-test",
        rule_name="Test",
        action_type="low_risk_single_message_send",
        source_type="buyer_interest",
        allowed_recipient_type="buyer",
        autonomy_level=4,
        live_flag_required=True,
        risk_score=10,
        owner_approval_status="approved",
        status="approved",
    )
    template = ApprovedTemplate(
        id="template-test",
        template_name="Safe",
        template_type="buyer_response",
        channel="email",
        recipient_type="buyer",
        subject="Draft response",
        body="Thanks for the interest. The owner will review next steps. This is not a contract or commitment.",
        approved=True,
    )

    gate = auto_execution_gate(rule, template)

    assert gate["can_execute"] is False
    assert "v5_safety_missing" in gate["blocked_reasons"]
    assert "v5_dry_run_missing" in gate["blocked_reasons"]
    assert "v5_owner_approval_missing" in gate["blocked_reasons"]
    assert "v5_live_flags_disabled" in gate["blocked_reasons"]


def test_no_bulk_send_and_audit_record_created():
    idempotency_key = f"test-auto-bulk-{uuid4().hex}"
    with TestClient(app) as client:
        response = client.post(
            "/api/auto-execution/execute",
            json={
                "rule_id": "auto-rule-buyer-response-send",
                "template_id": "template-buyer-response-safe",
                "idempotency_key": idempotency_key,
                "source_record_type": "buyer_interest",
                "source_record_id": "interest-001",
                "recipient_count": 2,
                "v5_safety_passed": True,
                "v5_dry_run_receipt_exists": True,
                "v5_approval_recorded": True,
                "live_flags_enabled": True,
                "provider_ready": True,
            },
        )
        audit = client.get("/api/auto-execution/audit")

    assert response.status_code == 200
    body = response.json()
    assert body["attempt_status"] == "blocked"
    assert "single_recipient_required" in body["blocked_reasons"]
    assert body["provider_called"] is False
    assert any(record["idempotency_key"] == f"{idempotency_key}:audit" for record in audit.json())


def test_idempotency_prevents_duplicate_sends():
    idempotency_key = f"test-auto-send-{uuid4().hex}"
    payload = {
        "rule_id": "auto-rule-buyer-response-send",
        "template_id": "template-buyer-response-safe",
        "idempotency_key": idempotency_key,
        "source_record_type": "buyer_interest",
        "source_record_id": "interest-001",
        "recipient_count": 1,
        "v5_safety_passed": True,
        "v5_dry_run_receipt_exists": True,
        "v5_approval_recorded": True,
        "live_flags_enabled": True,
        "provider_ready": True,
    }
    with TestClient(app) as client:
        first = client.post("/api/auto-execution/execute", json=payload)
        second = client.post("/api/auto-execution/execute", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["attempt_status"] == "mock_sent"
    assert first.json()["provider_called"] is True
    assert second.json()["idempotent_replay"] is True
    assert second.json()["duplicate_provider_call"] is False


def test_auto_execution_dashboard_routes_render_backend():
    routes = [
        "/api/auto-execution",
        "/api/auto-execution/rules",
        "/api/auto-execution/templates",
        "/api/auto-execution/dry-runs",
        "/api/auto-execution/attempts",
        "/api/auto-execution/audit",
    ]
    with TestClient(app) as client:
        for route in routes:
            response = client.get(route)
            assert response.status_code == 200, route
