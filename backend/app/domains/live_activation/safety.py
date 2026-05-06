from __future__ import annotations

from app.models import LiveProviderActivation


ALLOWED_LANES = {
    "openai_live_request": {"openai_generation"},
    "email_live_send": {"single_email_send"},
    "sms_sandbox_live_eligibility": {"single_sms_send"},
    "crm_sandbox_live_eligibility": {"single_crm_sync"},
    "storage_sandbox_live_eligibility": {"sanitized_storage_upload"},
}


def live_activation_safety(
    activation: LiveProviderActivation,
    *,
    provider_ready: bool,
    provider_blocked_reasons: list[str],
    production_ready: bool,
) -> dict[str, object]:
    reasons: list[str] = []
    if activation.lane_type not in ALLOWED_LANES:
        reasons.append("unsupported_lane")
    elif activation.allowed_action_type not in ALLOWED_LANES[activation.lane_type]:
        reasons.append("action_not_allowed_for_lane")
    if activation.owner_approval_status != "approved":
        reasons.append("owner_approval_required")
    if not activation.dry_run_receipt_id:
        reasons.append("dry_run_required")
    if not activation.dry_run_hash:
        reasons.append("dry_run_hash_required")
    if activation.current_source_hash != activation.dry_run_hash:
        reasons.append("source_changed_after_dry_run")
    if activation.live_flag_status != "enabled":
        reasons.append("live_flag_required")
    if not provider_ready:
        reasons.extend(provider_blocked_reasons or ["provider_readiness_required"])
    if not production_ready:
        reasons.append("production_readiness_required")
    if not activation.idempotency_key:
        reasons.append("idempotency_key_required")
    if not activation.one_action_only:
        reasons.append("one_action_model_required")
    if activation.bulk_action_allowed or activation.campaign_bulk_allowed:
        reasons.append("bulk_action_blocked")
    if activation.worker_bypass_allowed:
        reasons.append("worker_bypass_blocked")
    if activation.legal_advice_allowed:
        reasons.append("legal_advice_blocked")
    if activation.contract_execution_allowed:
        reasons.append("contract_execution_blocked")
    if activation.title_submission_allowed:
        reasons.append("title_submission_blocked")
    if activation.payment_handling_allowed:
        reasons.append("payment_handling_blocked")
    if activation.allowed_action_type == "single_sms_send":
        if activation.consent_status != "verified":
            reasons.append("sms_consent_required")
        if activation.dnc_status != "clear":
            reasons.append("dnc_blocked")
        if not activation.opt_out_included:
            reasons.append("sms_opt_out_required")
    if activation.allowed_action_type == "sanitized_storage_upload":
        if not activation.safety_snapshot.get("sanitized_metadata", False):
            reasons.append("sanitized_storage_metadata_required")
    if activation.allowed_action_type == "openai_generation":
        if activation.safety_snapshot.get("ai_safety_status") != "passed":
            reasons.append("ai_safety_required")
        if activation.safety_snapshot.get("cost_cap_status") == "exceeded":
            reasons.append("ai_cost_cap_blocked")

    return {
        "allowed": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "one_action_only": True,
        "bulk_allowed": False,
        "worker_bypass_allowed": False,
        "campaign_bulk_allowed": False,
        "provider_call_may_proceed": False,
    }
