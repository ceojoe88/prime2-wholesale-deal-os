from __future__ import annotations


def mobile_approval_gate(
    *,
    source_record_present: bool,
    safety_status: str,
    dry_run_receipt_id: str,
    provider_readiness_status: str,
    idempotency_key: str,
    owner_approval_recorded: bool,
) -> dict[str, object]:
    reasons: list[str] = []
    if not source_record_present:
        reasons.append("source_record_required")
    if safety_status != "passed":
        reasons.append("safety_check_required")
    if not dry_run_receipt_id:
        reasons.append("dry_run_receipt_required")
    if provider_readiness_status != "ready":
        reasons.append("provider_readiness_required")
    if not idempotency_key:
        reasons.append("idempotency_key_required")
    if not owner_approval_recorded:
        reasons.append("owner_approval_required")

    return {
        "allowed_for_owner_review": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "live_action_allowed": False,
        "contract_execution_allowed": False,
        "portal_publish_allowed": False,
        "approval_is_not_execution": True,
    }


def mobile_capture_safety(body: str) -> dict[str, object]:
    lowered = body.lower()
    blocked_terms = {
        "must sign": "pressure_language",
        "last chance": "pressure_language",
        "guaranteed profit": "unsupported_claim_language",
        "guarantee profit": "unsupported_claim_language",
        "execute contract": "contract_execution_language",
        "submit to title": "title_submission_language",
        "publish automatically": "portal_publish_language",
        "send all": "bulk_action_language",
        "blast": "bulk_action_language",
    }
    reasons = sorted({flag for term, flag in blocked_terms.items() if term in lowered})
    return {
        "allowed": not reasons,
        "blocked_reasons": reasons,
        "field_capture_only": True,
        "real_world_action_taken": False,
    }
