from __future__ import annotations

from fastapi.testclient import TestClient

from app.domains.client_command.safety import (
    CLIENT_COMMAND_BLOCKED_ACTIONS,
    validate_client_safe_text,
)
from app.main import app


def test_cp6_consent_record_creation_enforces_workspace_isolation():
    with TestClient(app) as client:
        created = client.post(
            "/api/v1/client-command/workspaces/client-workspace-003/compliance/consent-records",
            json={
                "contact_type": "seller",
                "lead_id": "client-lead-memphis-001",
                "consent_channel": "email",
                "consent_status": "confirmed",
                "consent_summary": "Test manual consent record.",
            },
        )
        listed = client.get("/api/v1/client-command/workspaces/client-workspace-003/compliance/consent-records")
        denied = client.post(
            "/api/v1/client-command/workspaces/client-workspace-001/compliance/consent-records",
            json={
                "contact_type": "seller",
                "lead_id": "client-lead-memphis-001",
                "consent_channel": "email",
                "consent_status": "confirmed",
            },
        )

    assert created.status_code == 200
    assert any(item["id"] == created.json()["consent_record"]["id"] for item in listed.json()["consent_records"])
    assert denied.status_code == 404


def test_cp6_opt_out_record_creation_enforces_workspace_isolation():
    with TestClient(app) as client:
        created = client.post(
            "/api/v1/client-command/workspaces/client-workspace-003/compliance/opt-outs",
            json={
                "contact_type": "buyer",
                "buyer_id": "client-buyer-memphis-hedge",
                "channel": "email",
                "opt_out_status": "active",
                "opt_out_summary": "Test manual opt-out record.",
            },
        )
        listed = client.get("/api/v1/client-command/workspaces/client-workspace-003/compliance/opt-outs")
        denied = client.post(
            "/api/v1/client-command/workspaces/client-workspace-001/compliance/opt-outs",
            json={
                "contact_type": "buyer",
                "buyer_id": "client-buyer-memphis-hedge",
                "channel": "email",
                "opt_out_status": "active",
            },
        )

    assert created.status_code == 200
    assert any(item["id"] == created.json()["opt_out_record"]["id"] for item in listed.json()["opt_out_records"])
    assert denied.status_code == 404


def test_cp6_safe_contact_status_blocks_active_opt_out():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/client-command/buyers/client-buyer-memphis-review/compliance/safe-contact-status",
            params={"workspace_id": "client-workspace-003"},
        )

    assert response.status_code == 200
    statuses = response.json()["safe_contact_statuses"]
    assert statuses
    assert statuses[0]["status"] == "blocked"
    assert "active_opt_out" in statuses[0]["block_reasons"]


def test_cp6_safe_contact_status_requires_review_for_missing_consent_and_stays_non_live():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/client-command/leads/client-lead-memphis-002/compliance/safe-contact-status",
            params={"workspace_id": "client-workspace-003"},
        )

    assert response.status_code == 200
    statuses = response.json()["safe_contact_statuses"]
    assert statuses
    assert statuses[0]["status"] in {"missing_consent", "needs_review"}
    assert statuses[0]["no_live_send"] is True
    assert statuses[0]["no_provider_check"] is True


def test_cp6_message_risk_review_blocks_guaranteed_profit_and_roi_language():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/client-command/compliance/message-risk-review",
            json={
                "workspace_id": "client-workspace-003",
                "lead_id": "client-lead-memphis-001",
                "source_draft_type": "seller_follow_up",
                "channel": "email",
                "draft_body": "Guaranteed profit and guaranteed ROI if you move now.",
            },
        )

    review = response.json()["message_risk_review"]
    assert response.status_code == 200
    assert review["review_status"] == "blocked"
    assert set(review["unsafe_language_flags"]) >= {"fake_roi_claim"}


def test_cp6_message_risk_review_can_pass_low_risk_draft_for_manual_use_only():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/client-command/compliance/message-risk-review",
            json={
                "workspace_id": "client-workspace-003",
                "lead_id": "client-lead-memphis-001",
                "source_draft_type": "seller_follow_up",
                "channel": "email",
                "draft_body": "Manual note: follow up politely and confirm whether the seller wants to keep reviewing options.",
            },
        )

    review = response.json()["message_risk_review"]
    assert response.status_code == 200
    assert review["review_status"] == "passed_for_manual_use"
    assert review["manual_use_only"] is True
    assert review["no_live_send"] is True


def test_cp6_communication_approval_gate_blocks_opted_out_contact():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/client-command/compliance/communication-approval-gate",
            json={
                "workspace_id": "client-workspace-003",
                "buyer_id": "client-buyer-memphis-review",
                "source_draft_type": "buyer_outreach",
            },
        )

    gate = response.json()["communication_approval_gate"]
    assert response.status_code == 200
    assert gate["gate_status"] == "blocked"
    assert gate["no_live_send"] is True
    assert gate["no_provider_call"] is True


def test_cp6_communication_approval_gate_can_allow_manual_use_only():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/client-command/compliance/communication-approval-gate",
            json={
                "workspace_id": "client-workspace-003",
                "lead_id": "client-lead-memphis-005",
                "buyer_id": "client-buyer-memphis-flipper",
                "source_draft_type": "buyer_outreach",
                "source_draft_id": "client-buyer-draft-memphis-005",
            },
        )

    gate = response.json()["communication_approval_gate"]
    assert response.status_code == 200
    assert gate["gate_status"] == "manual_use_allowed"
    assert gate["no_live_send"] is True
    assert gate["no_campaign_started"] is True


def test_cp6_compliance_placeholders_never_call_providers():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/client-command/workspaces/client-workspace-003/compliance/readiness-placeholders"
        )

    assert response.status_code == 200
    assert response.json()["readiness_placeholders"]
    for item in response.json()["readiness_placeholders"]:
        assert item["no_provider_call"] is True


def test_cp7_weekly_report_generation_is_deterministic():
    with TestClient(app) as client:
        first = client.post(
            "/api/v1/client-command/workspaces/client-workspace-003/weekly-reports",
            json={"report_week_start": "2026-05-01", "report_week_end": "2026-05-07"},
        )
        second = client.post(
            "/api/v1/client-command/workspaces/client-workspace-003/weekly-reports",
            json={"report_week_start": "2026-05-01", "report_week_end": "2026-05-07"},
        )

    assert first.status_code == 200
    assert second.status_code == 200
    first_metrics = first.json()["metrics"][0]
    second_metrics = second.json()["metrics"][0]
    assert first_metrics["total_leads"] == second_metrics["total_leads"]
    assert first_metrics["compliance_needs_review_count"] == second_metrics["compliance_needs_review_count"]
    assert first_metrics["disposition_ready_count"] == second_metrics["disposition_ready_count"]


def test_cp7_weekly_report_metric_snapshot_and_bottlenecks_reflect_cp2_to_cp6_records():
    with TestClient(app) as client:
        report = client.get("/api/v1/client-command/weekly-reports/client-weekly-report-memphis-2026-05-07")

    assert report.status_code == 200
    metrics = report.json()["metrics"][0]
    bottlenecks = {item["bottleneck_type"] for item in report.json()["bottlenecks"]}
    assert metrics["total_leads"] == 5
    assert metrics["compliance_needs_review_count"] >= 1
    assert {"missing_arv", "missing_repairs", "buyer_demand_missing", "compliance_blocked", "thin_margin"} <= bottlenecks


def test_cp7_weekly_report_recommended_actions_are_client_safe_and_flags_are_true():
    with TestClient(app) as client:
        report = client.get("/api/v1/client-command/weekly-reports/client-weekly-report-memphis-2026-05-07")

    body = report.json()
    weekly = body["weekly_report"]
    assert report.status_code == 200
    assert weekly["no_revenue_guarantee"] is True
    assert weekly["no_roi_claim"] is True
    assert weekly["no_live_actions_taken"] is True
    assert body["recommended_actions"]
    assert all(item["client_safe"] is True for item in body["recommended_actions"])
    serialized = str(body).lower()
    assert "closed deal" not in serialized
    assert "revenue booked" not in serialized


def test_cp6_cp7_sanitizer_hides_internal_notes_and_unsafe_fields():
    with TestClient(app) as client:
        lead = client.get(
            "/api/v1/client-command/leads/client-lead-memphis-005",
            params={"workspace_id": "client-workspace-003"},
        )
        report = client.get("/api/v1/client-command/weekly-reports/client-weekly-report-memphis-2026-05-07")

    serialized = f"{lead.json()} {report.json()}".lower()
    assert "internal_notes" not in serialized
    assert "raw_provider_payload" not in serialized
    assert "provider_config" not in serialized
    assert "internal_prime_governance" not in serialized


def test_cp6_cp7_safety_guard_proves_no_provider_calls_outbound_actions_or_campaigns_occur():
    unsafe = validate_client_safe_text(
        "Send SMS, Send Email, Contact Seller, Blast Buyers, Check DNC Live, Register 10DLC Live, "
        "Generate Contract, Sync to Provider, and guaranteed assignment fee."
    )
    assert unsafe["allowed"] is False
    assert {
        "sms_send",
        "email_send",
        "seller_blast",
        "buyer_blast",
        "dnc_check_provider_call",
        "ten_dlc_live_registration",
        "contract_generation",
        "provider_sync",
        "guaranteed_buyer_claim",
    } <= set(unsafe["risk_flags"])
    for blocked in [
        "buyer_blast",
        "seller_blast",
        "campaign_launch",
        "skip_trace_provider_call",
        "dnc_check_provider_call",
        "ten_dlc_live_registration",
        "provider_sync",
        "contract_generation",
    ]:
        assert blocked in CLIENT_COMMAND_BLOCKED_ACTIONS


def test_memphis_demo_validates_all_five_cp6_compliance_and_cp7_report_states():
    expected_statuses = {
        "client-lead-memphis-001": "safe_for_manual_use",
        "client-lead-memphis-002": "missing_consent",
        "client-lead-memphis-003": "needs_review",
        "client-lead-memphis-004": "needs_review",
        "client-lead-memphis-005": "safe_for_manual_use",
    }
    with TestClient(app) as client:
        responses = {
            lead_id: client.get(
                f"/api/v1/client-command/leads/{lead_id}/compliance/safe-contact-status",
                params={"workspace_id": "client-workspace-003"},
            )
            for lead_id in expected_statuses
        }
        report = client.get("/api/v1/client-command/weekly-reports/client-weekly-report-memphis-2026-05-07")

    for lead_id, expected in expected_statuses.items():
        assert responses[lead_id].status_code == 200
        assert responses[lead_id].json()["safe_contact_statuses"][0]["status"] == expected
    assert report.status_code == 200
    assert len(report.json()["lead_rollups"]) == 5
