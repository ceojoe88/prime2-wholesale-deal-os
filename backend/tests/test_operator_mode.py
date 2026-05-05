from fastapi.testclient import TestClient

from app.domain.operator_mode import (
    calculate_system_trust,
    command_loop_safety,
    operator_mode_gate,
)
from app.main import app
from app.models import (
    OperatorModeSetting,
    SemiAutonomousCommandLoopRun,
    SystemTrustScore,
)


def test_semi_autonomous_mode_cannot_bypass_approvals_or_level_5():
    setting = OperatorModeSetting(
        id="mode-test",
        current_mode="semi_autonomous",
        semi_autonomous_enabled=True,
        owner_enabled=True,
        max_autonomy_level=5,
        level_5_disabled=False,
        high_risk_requires_approval=False,
    )

    gate = operator_mode_gate(setting)

    assert gate["allowed"] is False
    assert "level_5_must_remain_disabled" in gate["blocked_reasons"]
    assert "high_risk_approval_required" in gate["blocked_reasons"]
    assert gate["owner_approval_required_for_high_risk"] is True


def test_command_loop_prepares_but_does_not_execute_high_risk_actions():
    loop = SemiAutonomousCommandLoopRun(
        id="loop-test",
        mode_setting_id="operator-mode-ready",
        high_risk_actions_executed=False,
        contracts_executed=False,
        title_submitted=False,
        bulk_campaigns_sent=False,
        portal_publish_without_approval=False,
    )

    safety = command_loop_safety(loop)

    assert safety["allowed"] is True
    assert safety["prepares_without_executing_high_risk_actions"] is True


def test_hard_boundary_blocks_execution_paths():
    with TestClient(app) as client:
        response = client.get("/api/operator-mode")

    assert response.status_code == 200
    body = response.json()
    assert body["semi_autonomous_cannot_bypass_approvals"] is True
    assert body["level_5_disabled"] is True
    boundary = body["hard_boundary"]
    assert boundary["contract_execution_allowed"] is False
    assert boundary["title_submission_allowed"] is False
    assert boundary["bulk_campaigns_allowed"] is False
    assert boundary["payment_handling_allowed"] is False


def test_owner_approval_console_aggregates_required_items():
    with TestClient(app) as client:
        response = client.get("/api/operator-mode/approvals")

    assert response.status_code == 200
    body = response.json()
    assert body["execution_allowed"] is False
    assert body["aggregates"]["seller_follow_up_live_send"] == 1
    assert body["aggregates"]["buyer_distribution"] == 1
    assert body["aggregates"]["automation_rule_activation"] == 1
    assert all(item["owner_required"] is True for item in body["approval_items"])


def test_daily_report_generated_and_exception_routing():
    with TestClient(app) as client:
        report = client.get("/api/operator-mode/daily-report")
        exceptions = client.get("/api/operator-mode/exceptions")

    assert report.status_code == 200
    latest = report.json()["latest_report"]
    assert latest["draft_only"] is True
    assert latest["high_risk_actions_executed"] is False
    assert latest["top_money_actions"]
    assert exceptions.status_code == 200
    assert len(exceptions.json()["owner_action_required"]) >= 1


def test_system_trust_score_calculates():
    score = SystemTrustScore(
        id="trust-test",
        automation_success_rate=85,
        blocked_unsafe_actions=8,
        approval_queue_age_hours=5,
        stale_tasks=2,
        scoring_confidence=84,
        forecast_confidence=78,
        buyer_response_velocity=86,
        seller_conversion_velocity=76,
    )

    overall = calculate_system_trust(score)

    assert overall > 70
    assert score.trust_status in {"strong_guarded", "stable_review"}


def test_operator_mode_routes_render_backend():
    routes = [
        "/api/operator-mode",
        "/api/operator-mode/approvals",
        "/api/operator-mode/exceptions",
        "/api/operator-mode/daily-report",
        "/api/operator-mode/system-trust",
        "/api/operator-mode/settings",
    ]
    with TestClient(app) as client:
        for route in routes:
            response = client.get(route)
            assert response.status_code == 200, route

