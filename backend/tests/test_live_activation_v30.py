from __future__ import annotations

from fastapi.testclient import TestClient

from app.domains.live_activation.safety import live_activation_safety
from app.main import app
from app.models import LiveProviderActivation


def _activation(**overrides) -> LiveProviderActivation:
    base = {
        "id": "live-activation-test",
        "provider_name": "Test provider",
        "provider_type": "email",
        "lane_type": "email_live_send",
        "source_domain": "communications",
        "source_record_type": "communication_draft",
        "source_record_id": "comm-draft-test",
        "allowed_action_type": "single_email_send",
        "activation_mode": "live",
        "owner_approval_status": "approved",
        "dry_run_receipt_id": "dry-run-test",
        "dry_run_hash": "hash-test",
        "current_source_hash": "hash-test",
        "live_flag_status": "enabled",
        "idempotency_key": "live:test",
        "consent_status": "not_applicable",
        "dnc_status": "clear",
        "opt_out_included": False,
        "one_action_only": True,
        "bulk_action_allowed": False,
        "worker_bypass_allowed": False,
        "campaign_bulk_allowed": False,
        "legal_advice_allowed": False,
        "contract_execution_allowed": False,
        "title_submission_allowed": False,
        "payment_handling_allowed": False,
    }
    base.update(overrides)
    return LiveProviderActivation(**base)


def _gate(activation: LiveProviderActivation, *, production_ready: bool = True):
    return live_activation_safety(
        activation,
        provider_ready=True,
        provider_blocked_reasons=[],
        production_ready=production_ready,
    )


def test_live_activation_requires_owner_approval():
    gate = _gate(_activation(owner_approval_status="pending_owner"))
    assert gate["allowed"] is False
    assert "owner_approval_required" in gate["blocked_reasons"]


def test_live_activation_requires_dry_run_and_unchanged_source():
    missing = _gate(_activation(dry_run_receipt_id="", dry_run_hash=""))
    changed = _gate(_activation(current_source_hash="changed"))
    assert "dry_run_required" in missing["blocked_reasons"]
    assert "dry_run_hash_required" in missing["blocked_reasons"]
    assert "source_changed_after_dry_run" in changed["blocked_reasons"]


def test_live_activation_requires_provider_and_production_readiness():
    activation = _activation()
    provider_blocked = live_activation_safety(
        activation,
        provider_ready=False,
        provider_blocked_reasons=["credential_env_value_missing"],
        production_ready=True,
    )
    production_blocked = _gate(activation, production_ready=False)
    assert "credential_env_value_missing" in provider_blocked["blocked_reasons"]
    assert "production_readiness_required" in production_blocked["blocked_reasons"]


def test_worker_and_campaign_cannot_bypass_activation():
    gate = _gate(_activation(worker_bypass_allowed=True, campaign_bulk_allowed=True))
    assert gate["allowed"] is False
    assert "worker_bypass_blocked" in gate["blocked_reasons"]
    assert "bulk_action_blocked" in gate["blocked_reasons"]
    assert gate["worker_bypass_allowed"] is False
    assert gate["bulk_allowed"] is False


def test_unsafe_sms_consent_dnc_and_opt_out_are_blocked():
    activation = _activation(
        provider_type="sms",
        lane_type="sms_sandbox_live_eligibility",
        allowed_action_type="single_sms_send",
        consent_status="missing",
        dnc_status="blocked_do_not_contact",
        opt_out_included=False,
    )
    gate = _gate(activation)
    assert gate["allowed"] is False
    assert "sms_consent_required" in gate["blocked_reasons"]
    assert "dnc_blocked" in gate["blocked_reasons"]
    assert "sms_opt_out_required" in gate["blocked_reasons"]


def test_openai_lane_respects_ai_safety_and_cost_cap():
    activation = _activation(
        provider_type="openai",
        lane_type="openai_live_request",
        allowed_action_type="openai_generation",
        safety_snapshot={"ai_safety_status": "passed", "cost_cap_status": "exceeded"},
    )
    gate = _gate(activation)
    assert gate["allowed"] is False
    assert "ai_cost_cap_blocked" in gate["blocked_reasons"]


def test_live_activation_attempts_are_idempotent_and_audited():
    payload = {"idempotency_key": "test-v30-idempotency-001", "request_metadata": {"source": "test"}}
    with TestClient(app) as client:
        first = client.post("/api/v1/live-activation/live-activation-email-001/attempt", json=payload)
        second = client.post("/api/v1/live-activation/live-activation-email-001/attempt", json=payload)

    assert first.status_code == 200
    assert first.json()["provider_called"] is False
    assert first.json()["live_action_executed"] is False
    assert second.status_code == 200
    assert second.json()["idempotent_replay"] is True
    assert second.json()["duplicate_action_prevented"] is True


def test_live_activation_routes_render_and_preserve_boundaries():
    with TestClient(app) as client:
        dashboard = client.get("/api/v1/live-activation")
        readiness = client.get("/api/v1/live-activation/readiness")
        approvals = client.get("/api/v1/live-activation/approvals")
        attempts = client.get("/api/v1/live-activation/attempts")
        blocked = client.get("/api/v1/live-activation/blocked")
        detail = client.get("/api/v1/live-activation/live-activation-sms-001")

    assert dashboard.status_code == 200
    assert readiness.status_code == 200
    assert approvals.status_code == 200
    assert attempts.status_code == 200
    assert blocked.status_code == 200
    assert detail.status_code == 200
    boundary = dashboard.json()["safety_boundary"]
    assert boundary["bulk_email_sms_allowed"] is False
    assert boundary["contract_execution_allowed"] is False
    assert boundary["worker_bypass_allowed"] is False
    assert "sms_consent_required" in detail.json()["gate"]["blocked_reasons"]
