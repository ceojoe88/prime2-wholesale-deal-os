from fastapi.testclient import TestClient

from app.core.config import settings
from app.domain.communications import MockEmailAdapter, MockSmsAdapter, validate_communication_safety
from app.main import app


def test_live_flags_default_off():
    assert settings.communication_global_live_enabled is False
    with TestClient(app) as client:
        response = client.get("/api/communications")
    assert response.status_code == 200
    body = response.json()
    assert body["global_live_flag_enabled"] is False
    assert body["bulk_send_allowed"] is False
    assert body["campaigns_allowed"] is False


def test_no_send_without_safety_or_dry_run():
    with TestClient(app) as client:
        response = client.post("/api/communications/comm-draft-003/send", json={})
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert detail["provider_called"] is False
    assert "safety_check_missing" in detail["gate"]["blocked_reasons"]
    assert "dry_run_receipt_missing" in detail["gate"]["blocked_reasons"]


def test_no_send_without_owner_approval():
    with TestClient(app) as client:
        response = client.post("/api/communications/comm-draft-001/send", json={})
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert detail["provider_called"] is False
    assert "owner_approval_not_recorded" in detail["gate"]["blocked_reasons"]


def test_no_send_if_draft_changed_after_dry_run():
    with TestClient(app) as client:
        response = client.post("/api/communications/comm-draft-006/send", json={})
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert detail["provider_called"] is False
    assert "draft_changed_after_dry_run" in detail["gate"]["blocked_reasons"]


def test_no_bulk_send_and_blocked_attempt_is_audited():
    with TestClient(app) as client:
        before = client.get("/api/communications/attempts").json()
        response = client.post(
            "/api/communications/comm-draft-002/send",
            json={"recipients": ["jules@example.test", "extra@example.test"]},
        )
        after = client.get("/api/communications/attempts").json()
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert detail["provider_called"] is False
    assert "bulk_send_blocked" in detail["gate"]["blocked_reasons"]
    assert len(after) == len(before) + 1
    assert after[-1]["attempt_status"] == "blocked"
    assert after[-1]["provider_called"] is False


def test_mock_adapters_only():
    assert MockEmailAdapter().provider_mode == "mock/dry_run"
    assert MockSmsAdapter().provider_mode == "mock/dry_run"


def test_communication_safety_blocks_unsafe_language():
    samples = [
        ("sms", "seller_follow_up", "", "You must sign now. This is your last chance."),
        ("email", "buyer_interest_response", "Legal", "This is legal advice and no attorney needed."),
        ("email", "buyer_interest_response", "Urgent", "Offer expires in minutes."),
        ("sms", "seller_follow_up", "", "We already have a buyer and guaranteed closing."),
        ("email", "buyer_interest_response", "Blast", "Send to all buyers in a campaign."),
        ("email", "buyer_interest_response", "Fee", "Keep the fee hidden from everyone."),
    ]
    for channel, draft_type, subject, body in samples:
        draft = type(
            "Draft",
            (),
            {
                "channel": channel,
                "draft_type": draft_type,
                "subject": subject,
                "draft_body": body,
            },
        )()
        result = validate_communication_safety(draft)
        assert result["allowed"] is False
        assert result["risk_flags"]


def test_dry_run_receipt_created_without_provider_call():
    with TestClient(app) as client:
        response = client.post("/api/communications/comm-draft-003/dry-run")
    assert response.status_code == 200
    body = response.json()
    assert body["provider_mode"] == "mock/dry_run"
    assert body["provider_call_made"] is False
    assert body["idempotency_key"]
