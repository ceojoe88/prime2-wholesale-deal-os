from __future__ import annotations

from fastapi.testclient import TestClient

from app.domains.client_command.safety import validate_client_safe_text
from app.main import app


def test_client_workspace_routes_are_client_safe_and_permissioned():
    with TestClient(app) as client:
        list_response = client.get("/api/v1/client-command/workspaces")
        detail = client.get("/api/v1/client-command/workspaces/client-workspace-001")
        allowed = client.get(
            "/api/v1/client-command/workspaces/client-workspace-001/leads",
            params={"member_email": "analyst@acme.example"},
        )
        denied = client.get(
            "/api/v1/client-command/workspaces/client-workspace-001/leads",
            params={"member_email": "analyst@oakline.example"},
        )

    assert list_response.status_code == 200
    assert "client_command.leads_view" in list_response.json()["permissions"]
    assert detail.status_code == 200
    serialized = str(detail.json()).lower()
    assert "internal_prime_governance_notes" not in serialized
    assert "raw_provider_payload" not in serialized
    assert allowed.status_code == 200
    assert denied.status_code == 403


def test_client_lead_workspace_isolation_blocks_cross_tenant_access():
    with TestClient(app) as client:
        good = client.get(
            "/api/v1/client-command/leads/client-lead-001",
            params={"workspace_id": "client-workspace-001"},
        )
        bad = client.get(
            "/api/v1/client-command/leads/client-lead-001",
            params={"workspace_id": "client-workspace-002"},
        )

    assert good.status_code == 200
    assert good.json()["lead"]["workspace_id"] == "client-workspace-001"
    assert bad.status_code == 404


def test_lead_scoring_is_deterministic_and_client_safe():
    with TestClient(app) as client:
        first = client.get(
            "/api/v1/client-command/leads/client-lead-001/score",
            params={"workspace_id": "client-workspace-001"},
        )
        second = client.get(
            "/api/v1/client-command/leads/client-lead-001/score",
            params={"workspace_id": "client-workspace-001"},
        )

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["score"]["final_priority_score"] == second.json()["score"]["final_priority_score"]
    assert first.json()["score"]["recommended_next_action"] == "owner_review_hot_lead"
    serialized = str(first.json()).lower()
    assert "raw_risk_logic" not in serialized
    assert "raw_provider_payload" not in serialized


def test_missing_data_lowers_readiness_and_sets_review_flags():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/client-command/leads/client-lead-003/score",
            params={"workspace_id": "client-workspace-001"},
        )

    body = response.json()
    assert body["score"]["confidence_level"] == "low"
    assert body["score"]["requires_human_review"] is True
    assert body["score"]["missing_data_score"] < 50
    assert len(body["missing_data"]) >= 3
    assert any(item["blocks_readiness"] for item in body["missing_data"])


def test_hot_board_and_next_actions_do_not_trigger_outbound_provider_actions():
    with TestClient(app) as client:
        hot = client.get(
            "/api/v1/client-command/leads/hot-board",
            params={"workspace_id": "client-workspace-001"},
        )
        actions = client.get(
            "/api/v1/client-command/leads/next-actions",
            params={"workspace_id": "client-workspace-001"},
        )

    assert hot.status_code == 200
    assert actions.status_code == 200
    assert hot.json()["safety"]["outbound_provider_actions_allowed"] is False
    assert actions.json()["outbound_provider_actions_allowed"] is False
    for action in actions.json()["next_actions"]:
        assert action["outbound_action_allowed"] is False
        assert action["provider_action_allowed"] is False


def test_client_command_safety_blocks_unsafe_language():
    unsafe = validate_client_safe_text(
        "Send SMS, run skip trace, send contract, and claim guaranteed ROI."
    )
    safe = validate_client_safe_text("Review missing data and prepare a client-safe lead summary.")

    assert unsafe["allowed"] is False
    assert {"sms_send", "skip_trace_provider_call", "contract_esignature_send", "fake_roi_claim"} <= set(
        unsafe["risk_flags"]
    )
    assert safe["allowed"] is True
