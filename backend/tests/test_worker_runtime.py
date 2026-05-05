from __future__ import annotations

from uuid import uuid4

from fastapi.testclient import TestClient

from app.domains.worker_runtime.worker import worker_safety_guard
from app.main import app


def test_worker_jobs_created_and_idempotency_blocks_duplicate_queue_items():
    key = f"test-worker-{uuid4().hex}"
    payload = {
        "job_type": "lead_scoring_refresh",
        "source_record": "leads",
        "idempotency_key": key,
    }
    with TestClient(app) as client:
        first = client.post("/api/v1/worker/jobs", json=payload)
        second = client.post("/api/v1/worker/jobs", json=payload)

    assert first.status_code == 200
    assert first.json()["status"] == "pending"
    assert second.status_code == 200
    assert second.json()["idempotent_replay"] is True
    assert second.json()["duplicate_job_created"] is False


def test_worker_runner_completes_safe_jobs_and_logs_attempts():
    key = f"test-worker-run-{uuid4().hex}"
    with TestClient(app) as client:
        created = client.post(
            "/api/v1/worker/jobs",
            json={
                "job_type": "buyer_ranking_refresh",
                "source_record": "deal-001",
                "idempotency_key": key,
            },
        ).json()
        run = client.post(f"/api/v1/worker/jobs/{created['job_id']}/run")
        logs = client.get("/api/v1/worker/logs")

    assert run.status_code == 200
    assert run.json()["status"] == "completed"
    assert run.json()["provider_called"] is False
    assert run.json()["real_world_action_taken"] is False
    assert any(log["job_id"] == created["job_id"] for log in logs.json()["logs"])


def test_worker_rejects_unsupported_or_live_action_jobs():
    result = worker_safety_guard("send_sms")
    assert result["allowed"] is False
    assert result["live_outreach_allowed"] is False

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/worker/jobs",
            json={
                "job_type": "send_sms",
                "source_record": "lead-001",
                "idempotency_key": f"blocked-worker-{uuid4().hex}",
            },
        )

    assert response.status_code == 200
    assert response.json()["status"] == "failed"
    assert "unsupported_worker_job_type" in response.json()["error_message"]


def test_scheduler_runs_and_does_not_trigger_live_actions():
    with TestClient(app) as client:
        response = client.post("/api/v1/worker/scheduler/run")

    assert response.status_code == 200
    body = response.json()
    assert body["live_action_triggered"] is False
    assert body["created_count"] >= 0
    assert body["due_run"]["live_action_triggered"] is False


def test_worker_heartbeat_reports_health():
    with TestClient(app) as client:
        response = client.get("/api/v1/worker/health")

    assert response.status_code == 200
    body = response.json()
    assert body["live_actions_allowed"] is False
    assert body["contract_execution_allowed"] is False
    assert body["title_submission_allowed"] is False
    assert body["heartbeat"]["worker_name"] == "prime2-worker"

