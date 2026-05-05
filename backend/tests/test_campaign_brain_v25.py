from __future__ import annotations

from uuid import uuid4

from fastapi.testclient import TestClient

from app.domains.campaign_brain.safety import campaign_rule_gate, scan_campaign_text
from app.domains.worker_runtime.worker import worker_safety_guard
from app.main import app


def test_campaign_defaults_to_draft_and_requires_governance():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/campaigns",
            json={
                "name": f"Draft seller follow-up {uuid4().hex}",
                "campaign_type": "seller_follow_up",
                "audience_type": "seller",
                "segment_definition": {"segment": "hot_motivation"},
            },
        )

    assert response.status_code == 200
    campaign = response.json()["campaign"]
    assert campaign["status"] == "draft"
    assert "owner_approval_required" in campaign["blocked_reasons"]
    assert "approved_templates_required" in campaign["blocked_reasons"]
    assert campaign["bulk_blast_allowed"] is False
    assert campaign["live_send_allowed"] is False


def test_dnc_records_are_excluded_from_audience_preview():
    with TestClient(app) as client:
        response = client.get("/api/v1/campaigns/segments")

    assert response.status_code == 200
    dnc_rows = response.json()["dnc_exclusions"]
    assert any(row["recipient_id"] == "lead-008" for row in dnc_rows)
    assert all(row["excluded"] is True for row in dnc_rows)


def test_activation_gate_requires_preview_owner_caps_and_templates():
    with TestClient(app) as client:
        blocked = client.post(
            "/api/v1/campaigns/campaign-001/activate",
            json={"idempotency_key": f"blocked-campaign-{uuid4().hex}"},
        )
        allowed = client.post(
            "/api/v1/campaigns/campaign-002/activate",
            json={"idempotency_key": f"allowed-campaign-{uuid4().hex}"},
        )

    assert blocked.status_code == 200
    assert blocked.json()["attempt_status"] == "blocked"
    assert "owner_approval_required" in blocked.json()["blocked_reasons"]
    assert allowed.status_code == 200
    assert allowed.json()["attempt_status"] == "active_controlled"
    assert allowed.json()["bulk_blast_allowed"] is False
    assert allowed.json()["one_recipient_per_event"] is True
    assert allowed.json()["live_send_attempted"] is False


def test_live_send_path_requires_v5_v13_v22_and_provider_gates():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/campaigns/campaign-002/activate",
            json={
                "idempotency_key": f"live-campaign-{uuid4().hex}",
                "live_send_requested": True,
                "v5_gate_passed": False,
                "v13_gate_passed": False,
                "v22_gate_passed": False,
                "provider_readiness_passed": False,
                "live_flag_enabled": False,
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["attempt_status"] == "blocked"
    assert "live_send_requires_v5_v13_v22_provider_live_flags" in body["blocked_reasons"]
    assert body["live_send_attempted"] is False


def test_campaign_pauses_on_stop_conditions():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/campaigns/campaign-002/stop-events",
            json={
                "recipient_id": "buyer-001",
                "event_type": "provider_readiness_fails",
                "reason": "Sandbox readiness failed.",
            },
        )
        detail = client.get("/api/v1/campaigns/campaign-002")

    assert response.status_code == 200
    assert response.json()["campaign_paused"] is True
    assert detail.json()["campaign"]["status"] == "paused"
    assert detail.json()["campaign"]["live_send_allowed"] is False


def test_campaign_safety_blocks_deceptive_or_bulk_language():
    result = scan_campaign_text("Blast this to every buyer, last chance, guaranteed profit.")
    assert result["allowed"] is False
    assert "bulk_blast" in result["risk_flags"]
    assert "deceptive_scarcity" in result["risk_flags"]
    assert "guaranteed_profit" in result["risk_flags"]


def test_worker_campaign_jobs_prepare_only():
    safety = worker_safety_guard("campaign_sequence_prep")
    assert safety["allowed"] is True
    assert safety["live_outreach_allowed"] is False
    with TestClient(app) as client:
        created = client.post(
            "/api/v1/worker/jobs",
            json={
                "job_type": "campaign_sequence_prep",
                "source_record": "campaign-001",
                "idempotency_key": f"campaign-job-{uuid4().hex}",
            },
        )
        run = client.post(f"/api/v1/worker/jobs/{created.json()['job_id']}/run")

    assert created.status_code == 200
    assert run.status_code == 200
    assert run.json()["provider_called"] is False
    assert run.json()["real_world_action_taken"] is False
    assert run.json()["bulk_send_allowed"] is False
