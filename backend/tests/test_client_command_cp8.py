from __future__ import annotations

from fastapi.testclient import TestClient

from app.domains.client_command.safety import (
    CLIENT_COMMAND_BLOCKED_ACTIONS,
    validate_client_safe_text,
)
from app.main import app


def test_cp8_business_profile_creation_and_strategy_routes_are_workspace_scoped():
    with TestClient(app) as client:
        created = client.post(
            "/api/v1/client-command/workspaces/client-workspace-003/onboarding/business-profile",
            json={
                "business_name": "Memphis Virtual Wholesale Operator",
                "business_type": "solo_wholesaler",
                "primary_market": "Memphis, TN",
                "preferred_strategy": "wholesaling",
                "biggest_bottleneck": "buyers",
            },
        )
        allowed = client.get("/api/v1/client-command/workspaces/client-workspace-003/onboarding/business-profile")
        other = client.get("/api/v1/client-command/workspaces/client-workspace-001/onboarding/business-profile")
        strategy = client.get("/api/v1/client-command/workspaces/client-workspace-003/onboarding/strategy-profile")

    assert created.status_code == 200
    assert allowed.status_code == 200
    assert other.status_code == 200
    assert strategy.status_code == 200
    assert allowed.json()["business_profile"]["workspace_id"] == "client-workspace-003"
    assert other.json()["business_profile"]["workspace_id"] == "client-workspace-001"
    assert strategy.json()["strategy_profile"]["workspace_id"] == "client-workspace-003"


def test_cp8_market_pipeline_and_lead_source_setup_are_deterministic_and_non_live():
    with TestClient(app) as client:
        markets = client.get("/api/v1/client-command/workspaces/client-workspace-003/onboarding/markets")
        pipeline = client.get("/api/v1/client-command/workspaces/client-workspace-003/onboarding/pipeline/stages")
        lead_sources = client.get("/api/v1/client-command/workspaces/client-workspace-003/onboarding/lead-sources")

    assert markets.status_code == 200
    assert pipeline.status_code == 200
    assert lead_sources.status_code == 200
    assert markets.json()["markets"][0]["no_live_data_provider"] is True
    assert [item["stage_order"] for item in pipeline.json()["stages"]] == list(range(1, 13))
    assert pipeline.json()["stages"][0]["manager_owner"] == "Lead Intelligence Manager"
    assert pipeline.json()["stages"][-1]["manager_owner"] == "Client Success Manager"
    for item in lead_sources.json()["lead_sources"]:
        assert item["provider_connected"] is False
        assert item["no_provider_sync"] is True


def test_cp8_buyer_team_compliance_and_first_leads_checklists_reflect_demo_state():
    with TestClient(app) as client:
        buyer_list = client.get("/api/v1/client-command/workspaces/client-workspace-003/onboarding/buyer-list-setup")
        team = client.get("/api/v1/client-command/workspaces/client-workspace-003/onboarding/team-checklist")
        compliance = client.get("/api/v1/client-command/workspaces/client-workspace-003/onboarding/compliance-checklist")
        first_leads = client.get("/api/v1/client-command/workspaces/client-workspace-003/onboarding/first-leads-checklist")

    assert buyer_list.status_code == 200
    assert team.status_code == 200
    assert compliance.status_code == 200
    assert first_leads.status_code == 200
    buyer_setup = buyer_list.json()["buyer_list_setup"]
    assert buyer_setup["buyer_count"] == 4
    assert buyer_setup["clear_buy_box_count"] >= 1
    assert buyer_setup["no_buyer_contacted"] is True
    team_checklist = team.json()["team_checklist"]
    assert "compliance_owner" in team_checklist["missing_roles"]
    assert team_checklist["setup_status"] in {"partial", "needs_review"}
    compliance_checklist = compliance.json()["compliance_checklist"]
    assert compliance_checklist["no_provider_check"] is True
    assert compliance_checklist["no_live_registration"] is True
    first_lead_checklist = first_leads.json()["first_leads_checklist"]
    assert first_lead_checklist["current_lead_count"] == 5
    assert first_lead_checklist["first_10_leads_target"] == 10
    assert "first_10_leads_target_not_met" in first_lead_checklist["missing_requirements"]


def test_cp8_workspace_readiness_is_weighted_deterministic_and_manual_only():
    with TestClient(app) as client:
        first = client.post("/api/v1/client-command/workspaces/client-workspace-003/onboarding/readiness-score")
        second = client.post("/api/v1/client-command/workspaces/client-workspace-003/onboarding/readiness-score")

    assert first.status_code == 200
    assert second.status_code == 200
    first_score = first.json()["readiness_score"]
    second_score = second.json()["readiness_score"]
    assert first_score["readiness_score"] == second_score["readiness_score"] == 83
    assert first_score["readiness_status"] == "ready_for_manual_operation"
    assert first_score["no_live_actions_enabled"] is True


def test_cp8_critical_blockers_can_block_activation_on_less_ready_workspace():
    with TestClient(app) as client:
        readiness = client.post("/api/v1/client-command/workspaces/client-workspace-001/onboarding/readiness-score")
        gate = client.post("/api/v1/client-command/workspaces/client-workspace-001/onboarding/go-live-gate")

    assert readiness.status_code == 200
    assert gate.status_code == 200
    assert gate.json()["go_live_gate"]["gate_status"] in {"blocked", "not_ready"}
    assert gate.json()["go_live_gate"]["approved_scope"] == "none"
    assert gate.json()["go_live_gate"]["no_live_communication"] is True


def test_cp8_go_live_gate_only_approves_manual_or_first_weekly_cycle_scope():
    with TestClient(app) as client:
        response = client.post("/api/v1/client-command/workspaces/client-workspace-003/onboarding/go-live-gate")

    gate = response.json()["go_live_gate"]
    assert response.status_code == 200
    assert gate["approved_scope"] in {"manual_operation_only", "first_weekly_cycle_only", "none"}
    assert gate["approved_scope"] == "manual_operation_only"
    assert gate["no_live_communication"] is True
    assert gate["no_provider_execution"] is True
    assert gate["no_billing_action"] is True
    assert gate["no_contract_action"] is True
    assert gate["no_campaign_action"] is True


def test_cp8_onboarding_tasks_are_workspace_scoped_and_client_safe():
    with TestClient(app) as client:
        created = client.post(
            "/api/v1/client-command/workspaces/client-workspace-003/onboarding/tasks",
            json={
                "task_title": "Review Memphis activation notes",
                "task_description": "Client-safe onboarding task.",
                "task_category": "review",
                "task_status": "todo",
                "priority": "medium",
                "owner_role": "onboarding_manager",
                "due_window": "this_week",
            },
        )
        listed = client.get("/api/v1/client-command/workspaces/client-workspace-003/onboarding/tasks")

    assert created.status_code == 200
    assert listed.status_code == 200
    tasks = listed.json()["tasks"]
    assert any(item["id"] == created.json()["task"]["id"] for item in tasks)
    assert all(item["workspace_id"] == "client-workspace-003" for item in tasks)
    assert all(item["client_safe"] is True for item in tasks)


def test_cp8_first_weekly_cycle_readiness_reflects_report_availability():
    with TestClient(app) as client:
        response = client.get("/api/v1/client-command/workspaces/client-workspace-003/onboarding/first-weekly-cycle-readiness")

    readiness = response.json()["first_weekly_cycle_readiness"]
    assert response.status_code == 200
    assert readiness["ready_for_first_weekly_cycle"] is True
    assert readiness["report_can_generate"] is True
    assert readiness["no_live_actions_taken"] is True


def test_cp8_onboarding_report_is_client_safe_and_has_no_roi_or_revenue_claims():
    with TestClient(app) as client:
        response = client.post("/api/v1/client-command/workspaces/client-workspace-003/onboarding/report")

    report = response.json()["report"]
    serialized = str(response.json()).lower()
    assert response.status_code == 200
    assert report["no_revenue_guarantee"] is True
    assert report["no_roi_claim"] is True
    assert report["no_live_actions_enabled"] is True
    assert "messages sent" not in serialized
    assert "closed deals" not in serialized
    assert "guaranteed roi" not in serialized
    assert "revenue booked" not in serialized


def test_cp8_sanitizer_hides_unsafe_fields():
    with TestClient(app) as client:
        overview = client.get("/api/v1/client-command/onboarding/overview")
        report = client.get("/api/v1/client-command/workspaces/client-workspace-003/onboarding/report")

    serialized = f"{overview.json()} {report.json()}".lower()
    assert "internal_notes" not in serialized
    assert "provider_config" not in serialized
    assert "billing_internals" not in serialized
    assert "live_provider_flags" not in serialized
    assert "internal_prime_governance" not in serialized


def test_cp8_safety_guard_blocks_provider_billing_campaign_and_live_activation_language():
    unsafe = validate_client_safe_text(
        "Send SMS, send email, start campaign, check DNC live, register 10DLC live, activate billing, "
        "activate live, sync to provider, generate contract, and guaranteed ROI."
    )
    assert unsafe["allowed"] is False
    assert {
        "sms_send",
        "email_send",
        "campaign_launch",
        "dnc_check_provider_call",
        "ten_dlc_live_registration",
        "billing_activation",
        "live_provider_activation",
        "provider_sync",
        "contract_generation",
        "fake_roi_claim",
    } <= set(unsafe["risk_flags"])
    for blocked in [
        "billing_activation",
        "live_provider_activation",
        "campaign_launch",
        "provider_sync",
        "dnc_check_provider_call",
        "ten_dlc_live_registration",
        "contract_generation",
    ]:
        assert blocked in CLIENT_COMMAND_BLOCKED_ACTIONS


def test_memphis_demo_validates_cp8_readiness_blockers_and_onboarding_report():
    with TestClient(app) as client:
        readiness = client.get("/api/v1/client-command/workspaces/client-workspace-003/onboarding/readiness-score")
        blockers = client.get("/api/v1/client-command/workspaces/client-workspace-003/onboarding/blockers")
        report = client.get("/api/v1/client-command/workspaces/client-workspace-003/onboarding/report")

    assert readiness.status_code == 200
    assert blockers.status_code == 200
    assert report.status_code == 200
    assert readiness.json()["readiness_score"]["readiness_status"] == "ready_for_manual_operation"
    blocker_types = {item["blocker_type"] for item in blockers.json()["blockers"]}
    assert "unsafe_contact_posture" in blocker_types
    assert len(blockers.json()["blockers"]) >= 3
    assert report.json()["report"]["client_safe_summary"] == "Client-safe onboarding report - no revenue, ROI, or deal outcome is guaranteed."
