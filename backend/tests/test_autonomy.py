from fastapi.testclient import TestClient
from uuid import uuid4

from app.domain.autonomy import autonomy_safety_guard
from app.main import app


def test_autonomy_safety_blocks_real_world_actions():
    blocked_actions = [
        "send_sms",
        "send_email",
        "buyer_blast_execute",
        "execute_contract",
        "submit_to_title_company",
        "publish_buyer_portal",
        "collect_payment",
    ]

    for action in blocked_actions:
        result = autonomy_safety_guard(action, 3)
        assert result["allowed"] is False
        assert result["real_world_action_allowed"] is False
        assert action in result["blocked_reasons"]


def test_level_5_is_disabled_and_level_4_requires_owner_approval():
    level_5 = autonomy_safety_guard("create_daily_briefing", 5)
    assert level_5["allowed"] is False
    assert "level_5_disabled" in level_5["blocked_reasons"]

    level_4_without_owner = autonomy_safety_guard("controlled_live_action_review", 4)
    assert level_4_without_owner["allowed"] is False
    assert "owner_approval_required_for_level_4" in level_4_without_owner["blocked_reasons"]

    level_4_with_owner = autonomy_safety_guard(
        "controlled_live_action_review",
        4,
        owner_approval_recorded=True,
    )
    assert level_4_with_owner["allowed"] is True
    assert level_4_with_owner["real_world_action_allowed"] is False


def test_autonomy_dashboard_exposes_runs_attempts_tasks_and_boundaries():
    with TestClient(app) as client:
        response = client.get("/api/autonomy")

    assert response.status_code == 200
    body = response.json()
    assert len(body["automation_rules"]) == 6
    assert len(body["scheduler_runs"]) >= 5
    assert len(body["automation_attempts"]) >= 10
    assert len(body["autonomous_agent_tasks"]) >= 8
    assert body["safety_boundaries"]["autonomous_live_outreach"] is False
    assert body["safety_boundaries"]["autonomous_buyer_blasts"] is False
    assert body["safety_boundaries"]["autonomous_contract_execution"] is False
    assert body["safety_boundaries"]["autonomous_title_submission"] is False
    assert body["safety_boundaries"]["autonomous_portal_publishing"] is False
    assert body["safety_boundaries"]["level_5_available"] is False


def test_scheduler_idempotency_prevents_duplicate_tasks_and_logs_attempts():
    idempotency_key = f"test-new-lead-intake-{uuid4().hex}"
    payload = {
        "workflow_type": "new_lead_intake",
        "idempotency_key": idempotency_key,
    }
    with TestClient(app) as client:
        first = client.post("/api/autonomy/run", json=payload)
        second = client.post("/api/autonomy/run", json=payload)
        runs = client.get("/api/autonomy/runs")

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["created_tasks"] == 1
    assert second.json()["idempotent_replay"] is True
    assert second.json()["duplicate_tasks_created"] == 0
    body = runs.json()
    assert any(
        attempt["idempotency_key"] == f"{idempotency_key}:attempt:score_leads"
        for attempt in body["automation_attempts"]
    )


def test_hot_deal_workflow_creates_escalation():
    idempotency_key = f"test-hot-deal-escalation-{uuid4().hex}"
    payload = {
        "workflow_type": "hot_deal_acceleration",
        "idempotency_key": idempotency_key,
    }
    with TestClient(app) as client:
        response = client.post("/api/autonomy/run", json=payload)
        escalations = client.get("/api/autonomy/escalations")

    assert response.status_code == 200
    assert response.json()["escalation_created"] is True
    assert any(
        escalation["idempotency_key"] == f"{idempotency_key}:escalation:hot-deal"
        for escalation in escalations.json()["escalations"]
    )


def test_daily_briefing_generates_recommendations_only():
    idempotency_key = f"test-daily-command-briefing-{uuid4().hex}"
    payload = {
        "workflow_type": "daily_command_briefing",
        "idempotency_key": idempotency_key,
    }
    with TestClient(app) as client:
        run = client.post("/api/autonomy/run", json=payload)
        response = client.get("/api/autonomy/daily-briefing")

    assert run.status_code == 200
    assert run.json()["daily_briefing_created"] is True
    assert response.status_code == 200
    latest = response.json()["latest"]
    assert latest["generated_by"] == "Prime 2"
    assert latest["recommendations_only"] is True
    assert latest["live_outreach_allowed"] is False
    assert latest["contract_execution_allowed"] is False
