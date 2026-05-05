from __future__ import annotations

from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_provider_registry_defaults_to_mock_and_live_disabled():
    with TestClient(app) as client:
        response = client.get("/api/v1/provider-readiness")

    assert response.status_code == 200
    body = response.json()
    assert body["default_provider_mode"] == "mock"
    assert body["live_provider_calls_allowed"] is False
    assert body["credential_posture"]["stored_secret_count"] == 0
    assert any(provider["provider_mode"] == "mock" for provider in body["providers"])


def test_provider_api_never_exposes_secret_values_or_raw_references():
    with TestClient(app) as client:
        response = client.get("/api/v1/provider-readiness/credentials")

    assert response.status_code == 200
    serialized = str(response.json()).lower()
    assert "credential_reference_name" not in serialized
    assert "sk-" not in serialized
    assert "secret_value" not in serialized
    assert response.json()["raw_secret_exposed"] is False


def test_readiness_blocks_missing_credentials_for_sandbox():
    with TestClient(app) as client:
        detail = client.get("/api/v1/provider-readiness/provider-email-sandbox")

    assert detail.status_code == 200
    readiness = detail.json()["readiness"]
    assert readiness["ready"] is False
    assert readiness["status"] == "missing_credentials"
    assert "credential_env_value_missing" in readiness["blocked_reasons"]


def test_readiness_blocks_live_without_live_flag_and_owner_approval():
    with TestClient(app) as client:
        attempt = client.post(
            "/api/v1/provider-readiness/attempts",
            json={
                "provider_id": "provider-sms-live",
                "source_domain": "communications",
                "action_type": "single_sms_send",
                "mode": "live",
                "idempotency_key": f"live-block-{uuid4().hex}",
            },
        )

    assert attempt.status_code == 200
    body = attempt.json()
    assert body["attempt_status"] == "blocked"
    assert body["provider_called"] is False
    assert body["real_network_call_made"] is False
    blocked = body["readiness_result"]["blocked_reasons"]
    assert "live_flag_required" in blocked
    assert "owner_approval_required_for_live" in blocked


def test_provider_attempts_record_blocked_readiness_and_idempotency():
    key = f"provider-idem-{uuid4().hex}"
    payload = {
        "provider_id": "provider-email-sandbox",
        "source_domain": "communications",
        "action_type": "seller_follow_up",
        "mode": "sandbox",
        "idempotency_key": key,
    }
    with TestClient(app) as client:
        first = client.post("/api/v1/provider-readiness/attempts", json=payload)
        second = client.post("/api/v1/provider-readiness/attempts", json=payload)
        attempts = client.get("/api/v1/provider-readiness/attempts")

    assert first.status_code == 200
    assert first.json()["attempt_status"] == "blocked"
    assert second.json()["idempotent_replay"] is True
    assert second.json()["duplicate_provider_call_prevented"] is True
    assert any(record["idempotency_key"] == key for record in attempts.json()["provider_attempts"])


def test_webhook_skeleton_queues_review_without_deal_mutation():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/provider-readiness/webhooks",
            json={
                "provider_type": "crm",
                "event_type": "mock_lead_update",
                "mode": "sandbox",
                "signature_present": True,
                "signature_valid": True,
                "payload_metadata": {"source": "sandbox-fixture"},
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["review_task_created"] is True
    assert body["deal_mutation_allowed"] is False
    assert body["deal_mutated"] is False


def test_unsigned_live_like_webhook_is_rejected_and_recorded_safely():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/provider-readiness/webhooks",
            json={
                "provider_type": "sms",
                "event_type": "delivery_status",
                "mode": "live",
                "signature_present": False,
                "signature_valid": False,
            },
        )
        webhooks = client.get("/api/v1/provider-readiness/webhooks")

    assert response.status_code == 400
    detail = response.json()["detail"]
    assert detail["normalized_event_status"] == "blocked"
    assert detail["deal_mutated"] is False
    assert any(
        event["blocked_reason"] == "unsigned_live_like_webhook_rejected"
        for event in webhooks.json()["webhook_events"]
    )
