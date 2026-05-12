from __future__ import annotations

from fastapi.testclient import TestClient

from app.domains.client_command.safety import (
    CLIENT_COMMAND_BLOCKED_ACTIONS,
    validate_client_safe_text,
)
from app.main import app


def test_cp9_plan_gates_usage_and_upgrade_recommendations_are_deterministic_and_non_live():
    with TestClient(app) as client:
        catalog = client.get("/api/v1/client-command/plans/catalog")
        first = client.post(
            "/api/v1/client-command/workspaces/client-workspace-003/feature-gates/evaluate",
            json={"feature_key": "billing"},
        )
        second = client.post(
            "/api/v1/client-command/workspaces/client-workspace-003/feature-gates/evaluate",
            json={"feature_key": "billing"},
        )
        usage = client.get("/api/v1/client-command/workspaces/client-workspace-003/usage")
        upgrade = client.get("/api/v1/client-command/workspaces/client-workspace-003/upgrade-recommendations")

    assert catalog.status_code == 200
    plans = {plan["plan_code"]: plan for plan in catalog.json()["plans"]}
    assert "command" in plans
    assert plans["command"]["no_live_billing"] is True
    assert plans["command"]["no_payment_collected"] is True

    assert first.status_code == 200
    assert second.status_code == 200
    first_gate = first.json()["feature_gates"][0]
    second_gate = second.json()["feature_gates"][0]
    assert first_gate["gate_status"] == second_gate["gate_status"] == "blocked_by_plan"
    assert first_gate["required_upgrade_plan"] == "command"
    assert first_gate["no_live_action"] is True

    assert usage.status_code == 200
    usage_body = usage.json()["usage"]
    assert usage_body["leads_count"] == 5
    assert usage_body["buyers_count"] >= 4
    assert usage_body["users_count"] == 1
    assert usage_body["weekly_reports_count"] >= 1
    assert usage_body["manual_drafts_count"] >= 6
    assert any(
        record["seat_label"] == "Memphis Demo Operator" and record["counts_against_limit"] is True
        for record in usage.json()["seat_usage"]
    )

    assert upgrade.status_code == 200
    recommendation = upgrade.json()["upgrade_recommendation"]
    assert recommendation["current_plan_code"] == "pro"
    assert recommendation["recommended_plan_code"] == "command"
    assert {"billing", "admin_support"} <= set(recommendation["blocked_features"])
    assert recommendation["client_safe_summary"] == "Feature access is controlled by plan, readiness, and safety gates."


def test_cp10_communication_readiness_and_attempts_stay_manual_only_and_blocked_until_live_gates_clear():
    with TestClient(app) as client:
        readiness_checks = client.get("/api/v1/client-command/communication/readiness-checks")
        dry_run = client.post(
            "/api/v1/client-command/communication/dry-run",
            json={
                "workspace_id": "client-workspace-003",
                "lead_id": "client-lead-memphis-001",
                "source_draft_type": "seller_follow_up",
                "source_draft_id": "client-follow-up-memphis-001",
                "channel": "email",
                "provider_profile_id": "client-comm-provider-memphis-email",
                "idempotency_key": "worker-tests-cp10-dry-run-001",
            },
        )
        approval = client.post(
            "/api/v1/client-command/communication/send-approval",
            json={
                "workspace_id": "client-workspace-003",
                "readiness_check_id": "client-comm-readiness-memphis-lead-001",
                "dry_run_receipt_id": dry_run.json()["dry_run"]["id"],
                "approved_by": "Worker Tests",
                "reason_summary": "Approval does not send a message.",
            },
        )
        attempt = client.post(
            "/api/v1/client-command/communication/send-attempt",
            json={
                "workspace_id": "client-workspace-003",
                "readiness_check_id": "client-comm-readiness-memphis-lead-001",
                "dry_run_receipt_id": dry_run.json()["dry_run"]["id"],
                "approval_id": approval.json()["send_approval"]["id"],
                "provider_profile_id": "client-comm-provider-memphis-email",
                "lead_id": "client-lead-memphis-001",
                "source_draft_type": "seller_follow_up",
                "source_draft_id": "client-follow-up-memphis-001",
                "channel": "email",
                "idempotency_key": "worker-tests-cp10-attempt-001",
            },
        )
        attempts = client.get("/api/v1/client-command/communication/send-attempts")

    assert readiness_checks.status_code == 200
    checks_by_id = {item["id"]: item for item in readiness_checks.json()["readiness_checks"]}
    blocked_memphis = checks_by_id["client-comm-readiness-memphis-lead-002"]
    assert blocked_memphis["readiness_status"] == "blocked"
    assert {"cp6_safe_contact_not_clear", "message_risk_not_passed", "live_flags_not_enabled"} <= set(
        blocked_memphis["block_reasons"]
    )
    assert blocked_memphis["cp9_gate_snapshot"] == "allowed"
    assert blocked_memphis["no_live_send"] is True

    assert dry_run.status_code == 200
    assert dry_run.json()["dry_run"]["no_live_send"] is True
    assert approval.status_code == 200
    assert approval.json()["send_approval"]["no_live_send"] is True

    assert attempt.status_code == 200
    send_attempt = attempt.json()["send_attempt"]
    assert send_attempt["attempt_status"] == "blocked"
    assert "readiness_not_ready" in send_attempt["block_reasons"]
    assert send_attempt["no_bulk"] is True

    assert attempts.status_code == 200
    assert any(item["id"] == send_attempt["id"] for item in attempts.json()["send_attempts"])


def test_cp11_billing_profiles_checks_attempts_and_ledger_never_store_card_data_or_charge():
    with TestClient(app) as client:
        readiness = client.get("/api/v1/client-command/workspaces/client-workspace-003/billing-readiness")
        providers = client.get("/api/v1/client-command/billing/providers")
        profiles = client.get("/api/v1/client-command/billing/customer-profiles")
        checks = client.get("/api/v1/client-command/billing/readiness-checks")
        dry_runs = client.get("/api/v1/client-command/billing/checkout-dry-runs")
        attempts = client.get("/api/v1/client-command/billing/attempts")
        ledger = client.get("/api/v1/client-command/billing/ledger")
        overview = client.get("/api/v1/client-command/billing/overview")

    assert readiness.status_code == 200
    billing_readiness = readiness.json()["billing_readiness"]
    assert billing_readiness["readiness_status"] == "setup_needed"
    assert billing_readiness["no_provider_call"] is True
    assert billing_readiness["no_payment_collected"] is True
    assert billing_readiness["no_invoice_created"] is True

    assert providers.status_code == 200
    provider = next(item for item in providers.json()["providers"] if item["id"] == "client-billing-provider-memphis")
    assert provider["secret_present"] is True
    assert provider["client_safe"] is True

    assert profiles.status_code == 200
    customer = next(item for item in profiles.json()["customer_profiles"] if item["id"] == "client-billing-customer-memphis")
    assert customer["raw_card_data_present"] is False
    assert customer["client_safe_summary"] == "No raw card data is stored."

    assert checks.status_code == 200
    readiness_check = next(item for item in checks.json()["readiness_checks"] if item["id"] == "client-billing-check-memphis")
    assert readiness_check["readiness_status"] == "blocked"
    assert {"billing_readiness_not_ready", "live_flags_not_enabled", "plan_gate_blocked_by_plan"} <= set(
        readiness_check["block_reasons"]
    )
    assert readiness_check["no_payment_collected"] is True
    assert readiness_check["no_invoice_created"] is True

    assert dry_runs.status_code == 200
    checkout_dry_run = next(item for item in dry_runs.json()["dry_runs"] if item["id"] == "client-billing-dry-run-memphis")
    assert checkout_dry_run["no_payment_collected"] is True

    assert attempts.status_code == 200
    billing_attempt = next(item for item in attempts.json()["attempts"] if item["id"] == "client-billing-attempt-memphis")
    assert billing_attempt["attempt_status"] == "blocked"
    assert {"billing_readiness_not_ready", "plan_gate_blocked_by_plan", "live_flags_not_enabled"} <= set(
        billing_attempt["block_reasons"]
    )
    assert billing_attempt["no_raw_card_data"] is True

    assert ledger.status_code == 200
    ledger_entry = next(item for item in ledger.json()["ledger"] if item["id"] == "client-billing-ledger-memphis")
    assert ledger_entry["status"] == "blocked"
    assert "before any payment action" in ledger_entry["summary"].lower()
    assert ledger_entry["client_safe"] is True

    assert overview.status_code == 200
    assert overview.json()["metrics"]["blocked_attempts"] >= 1
    assert overview.json()["safety"]["billing_allowed"] is False


def test_cp11_cp12_sanitizers_hide_billing_and_pilot_internals():
    with TestClient(app) as client:
        plans = client.get("/api/v1/client-command/plans/overview")
        billing = client.get("/api/v1/client-command/billing/providers")
        pilot_updates = client.get("/api/v1/client-command/workspaces/client-workspace-003/pilot/client-safe-updates")
        pilot_admin = client.get("/api/v1/client-command/pilot/admin-console")

    serialized = f"{plans.json()} {billing.json()} {pilot_updates.json()} {pilot_admin.json()}".lower()
    assert "internal_prime_governance" not in serialized
    assert "raw_provider_payload" not in serialized
    assert "provider_secret" not in serialized
    assert "secret_value" not in serialized
    assert "note_body" not in serialized
    assert "hidden admin-only note for pilot coordination" not in serialized
    assert pilot_updates.json()["client_safe_updates"][0]["hides_admin_notes"] is True


def test_cp12_pilot_health_launch_risk_and_console_aggregation_reflect_memphis_demo_state():
    with TestClient(app) as client:
        seeded_launch = client.get("/api/v1/client-command/workspaces/client-workspace-003/pilot/launch-checklist")
        seeded_risk = client.get("/api/v1/client-command/workspaces/client-workspace-003/pilot/risk-review")
        blocked_snapshot = client.post("/api/v1/client-command/workspaces/client-workspace-003/pilot/health-snapshot")
        admin = client.get("/api/v1/client-command/pilot/admin-console")
        support = client.get("/api/v1/client-command/pilot/support-console")
        blocked = client.get("/api/v1/client-command/pilot/blocked")
        updates = client.get("/api/v1/client-command/workspaces/client-workspace-003/pilot/client-safe-updates")

    assert seeded_launch.status_code == 200
    launch = seeded_launch.json()["launch_checklist"]
    assert launch["checklist_status"] == "blocked"
    assert {"compliance_not_acceptable", "communication_gate_blocked", "billing_gate_blocked"} <= set(
        launch["block_reasons"]
    )
    assert launch["client_safe_summary"] == "Pilot launch checklist does not bypass source gates."

    assert seeded_risk.status_code == 200
    risk_review = seeded_risk.json()["risk_review"]
    assert risk_review["risk_status"] == "blocked"
    assert risk_review["communication_blocked"] is True
    assert risk_review["billing_blocked"] is True
    assert risk_review["compliance_blocked"] is True
    assert risk_review["escalation_required"] is True
    assert risk_review["summary"] == "Controlled live posture requires CP9, CP10, and CP11 gates."

    assert blocked_snapshot.status_code == 200
    snapshot = blocked_snapshot.json()["health_snapshot"]
    assert snapshot["health_status"] == "blocked"
    assert {"communication_gate_blocked", "billing_gate_blocked", "compliance_review_needed"} <= set(
        snapshot["block_reasons"]
    )
    assert snapshot["client_safe_summary"] == "Pilot mode does not bypass source gates."

    assert admin.status_code == 200
    assert admin.json()["metrics"]["programs"] >= 1
    assert admin.json()["metrics"]["enrollments"] >= 1
    assert admin.json()["metrics"]["support_tickets"] >= 3
    assert admin.json()["metrics"]["escalations"] >= 1
    assert admin.json()["metrics"]["blocked_health_snapshots"] >= 1

    assert support.status_code == 200
    assert len(support.json()["tickets"]) >= 3
    assert len(support.json()["actions"]) >= 1
    assert len(support.json()["escalations"]) >= 1

    assert blocked.status_code == 200
    assert any(
        item["workspace_id"] == "client-workspace-003" and item["health_status"] == "blocked"
        for item in blocked.json()["blocked"]
    )

    assert updates.status_code == 200
    assert updates.json()["client_safe_updates"][0]["status"] == "client_visible"
    assert updates.json()["client_safe_updates"][0]["hides_admin_notes"] is True


def test_cp9_cp12_safety_guard_blocks_bulk_billing_and_gate_override_language():
    unsafe = validate_client_safe_text(
        "Auto follow-up, auto reply, send bulk, create Stripe customer, start subscription, "
        "store card, force charge, override gate, and delete client data."
    )

    assert unsafe["allowed"] is False
    assert {
        "auto_follow_up",
        "auto_reply",
        "bulk_send",
        "create_stripe_customer",
        "subscription_start",
        "store_card",
        "force_charge",
        "override_gate",
        "delete_client_data",
    } <= set(unsafe["risk_flags"])
    for blocked in [
        "auto_follow_up",
        "auto_reply",
        "bulk_send",
        "create_stripe_customer",
        "subscription_start",
        "store_card",
        "force_charge",
        "override_gate",
        "delete_client_data",
    ]:
        assert blocked in CLIENT_COMMAND_BLOCKED_ACTIONS
