from __future__ import annotations

from app.domain.autonomy import autonomy_safety_guard


ALLOWED_WORKER_JOB_TYPES = {
    "lead_scoring_refresh",
    "follow_up_scheduling",
    "daily_briefing_generation",
    "buyer_ranking_refresh",
    "qa_checks",
    "automation_rule_evaluation",
    "field_testing_summary",
    "forecast_refresh",
    "call_analysis",
    "campaign_segment_evaluation",
    "campaign_sequence_prep",
    "campaign_dry_run_task",
    "campaign_pause_evaluation",
    "campaign_owner_approval_task",
}

JOB_ACTION_MAP = {
    "lead_scoring_refresh": "refresh_deal_scores",
    "follow_up_scheduling": "schedule_reminder",
    "daily_briefing_generation": "create_daily_briefing",
    "buyer_ranking_refresh": "refresh_buyer_demand",
    "qa_checks": "score_leads",
    "automation_rule_evaluation": "update_priority_queues",
    "field_testing_summary": "create_next_best_action",
    "forecast_refresh": "create_next_best_action",
    "call_analysis": "create_next_best_action",
    "campaign_segment_evaluation": "create_next_best_action",
    "campaign_sequence_prep": "create_next_best_action",
    "campaign_dry_run_task": "create_next_best_action",
    "campaign_pause_evaluation": "create_next_best_action",
    "campaign_owner_approval_task": "create_next_best_action",
}

WORKER_BLOCKED_ACTIONS = {
    "send_sms",
    "send_email",
    "call_seller",
    "contact_buyer",
    "execute_contract",
    "submit_to_title_company",
    "publish_buyer_portal",
    "publish_seller_portal",
    "change_seller_terms",
    "change_buyer_terms",
    "collect_payment",
    "bulk_send",
}


def worker_safety_guard(job_type: str, autonomy_level: int = 3) -> dict[str, object]:
    normalized = job_type.strip().lower()
    flags: list[str] = []
    if normalized not in ALLOWED_WORKER_JOB_TYPES:
        flags.append("unsupported_worker_job_type")
    action = JOB_ACTION_MAP.get(normalized, "unsupported_worker_job")
    autonomy = autonomy_safety_guard(action, autonomy_level)
    flags.extend(str(reason) for reason in autonomy["blocked_reasons"])
    return {
        "allowed": not flags,
        "job_type": normalized,
        "autonomy_action": action,
        "blocked_reasons": sorted(set(flags)),
        "autonomy_safety": autonomy,
        "live_outreach_allowed": False,
        "contract_execution_allowed": False,
        "title_submission_allowed": False,
        "portal_publish_allowed": False,
        "payment_handling_allowed": False,
        "bulk_send_allowed": False,
    }
