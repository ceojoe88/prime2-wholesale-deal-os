from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import (
    AutonomousDailyOperatingReport,
    LeadQualityReview,
    OperatorExceptionRecord,
    OperatorModeSetting,
    OwnerApprovalItem,
    PredictionFeedbackRecord,
    SemiAutonomousCommandLoopRun,
    SystemTrustScore,
)
from app.serializers import model_to_dict


HARD_BOUNDARY_FLAGS = {
    "contract_execution_allowed": False,
    "title_submission_allowed": False,
    "bulk_campaigns_allowed": False,
    "payment_handling_allowed": False,
    "portal_publish_without_approval_allowed": False,
    "legal_advice_allowed": False,
    "guaranteed_profit_allowed": False,
    "level_5_available": False,
}


def operator_mode_gate(setting: OperatorModeSetting) -> dict[str, object]:
    reasons: list[str] = []
    if setting.current_mode == "semi_autonomous" and not (
        setting.semi_autonomous_enabled and setting.owner_enabled
    ):
        reasons.append("semi_autonomous_requires_owner_enablement")
    if setting.max_autonomy_level >= 5 or not setting.level_5_disabled:
        reasons.append("level_5_must_remain_disabled")
    if not setting.high_risk_requires_approval:
        reasons.append("high_risk_approval_required")
    if not setting.live_actions_require_gates:
        reasons.append("live_actions_require_gates")
    if setting.contract_execution_allowed:
        reasons.append("contract_execution_blocked")
    if setting.title_submission_allowed:
        reasons.append("title_submission_blocked")
    if setting.bulk_campaigns_allowed:
        reasons.append("bulk_campaigns_blocked")
    if setting.payment_handling_allowed:
        reasons.append("payment_handling_blocked")
    return {
        "allowed": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "hard_boundary": HARD_BOUNDARY_FLAGS,
        "owner_approval_required_for_high_risk": True,
    }


def command_loop_safety(loop: SemiAutonomousCommandLoopRun) -> dict[str, object]:
    reasons = []
    if loop.high_risk_actions_executed:
        reasons.append("high_risk_action_executed")
    if loop.contracts_executed:
        reasons.append("contract_execution_blocked")
    if loop.title_submitted:
        reasons.append("title_submission_blocked")
    if loop.bulk_campaigns_sent:
        reasons.append("bulk_campaign_blocked")
    if loop.portal_publish_without_approval:
        reasons.append("portal_publish_without_approval_blocked")
    return {
        "allowed": not reasons,
        "blocked_reasons": reasons,
        "prepares_without_executing_high_risk_actions": not reasons,
    }


def approval_console_summary(items: list[OwnerApprovalItem]) -> dict[str, object]:
    return {
        "approval_items": [model_to_dict(item) for item in items],
        "pending_approvals": [
            model_to_dict(item) for item in items if item.approval_status == "pending_owner"
        ],
        "ready_for_approval": [
            model_to_dict(item) for item in items if item.ready_for_approval
        ],
        "blocked_approvals": [
            model_to_dict(item) for item in items if item.blocked_reasons
        ],
        "aggregates": {
            "seller_follow_up_live_send": len(
                [item for item in items if item.approval_type == "seller_follow_up_live_send"]
            ),
            "buyer_response_live_send": len(
                [item for item in items if item.approval_type == "buyer_response_live_send"]
            ),
            "offer_packet_prep": len(
                [item for item in items if item.approval_type == "offer_packet_prep"]
            ),
            "contract_ready_status": len(
                [item for item in items if item.approval_type == "contract_ready_status"]
            ),
            "title_review_packet": len(
                [item for item in items if item.approval_type == "title_review_packet"]
            ),
            "buyer_distribution": len(
                [item for item in items if item.approval_type == "buyer_distribution"]
            ),
            "portal_visibility": len(
                [item for item in items if item.approval_type == "portal_visibility"]
            ),
            "forecast_spend_recommendation": len(
                [item for item in items if item.approval_type == "forecast_spend_recommendation"]
            ),
            "automation_rule_activation": len(
                [item for item in items if item.approval_type == "automation_rule_activation"]
            ),
        },
        "execution_allowed": False,
    }


def calculate_system_trust(score: SystemTrustScore) -> float:
    overall = (
        score.automation_success_rate * 0.16
        + min(score.blocked_unsafe_actions * 5, 100) * 0.10
        + (100 - min(score.approval_queue_age_hours * 4, 100)) * 0.12
        + (100 - min(score.stale_tasks * 8, 100)) * 0.10
        + score.scoring_confidence * 0.15
        + score.forecast_confidence * 0.15
        + score.buyer_response_velocity * 0.11
        + score.seller_conversion_velocity * 0.11
    )
    score.overall_trust_score = round(max(0, min(100, overall)), 2)
    if score.overall_trust_score >= 82:
        score.trust_status = "strong_guarded"
    elif score.overall_trust_score >= 68:
        score.trust_status = "stable_review"
    else:
        score.trust_status = "needs_operator_attention"
    return score.overall_trust_score


def operator_mode_dashboard(session: Session) -> dict[str, object]:
    settings = session.query(OperatorModeSetting).all()
    loops = session.query(SemiAutonomousCommandLoopRun).all()
    approvals = session.query(OwnerApprovalItem).all()
    exceptions = session.query(OperatorExceptionRecord).all()
    reports = session.query(AutonomousDailyOperatingReport).all()
    trust_scores = session.query(SystemTrustScore).all()
    lead_quality_reviews = session.query(LeadQualityReview).all()
    prediction_feedback = session.query(PredictionFeedbackRecord).all()
    for trust in trust_scores:
        calculate_system_trust(trust)
    return {
        "settings": [{**model_to_dict(setting), "gate": operator_mode_gate(setting)} for setting in settings],
        "command_loops": [
            {**model_to_dict(loop), "safety": command_loop_safety(loop)} for loop in loops
        ],
        "approval_console": approval_console_summary(approvals),
        "exceptions": [model_to_dict(exception) for exception in exceptions],
        "daily_reports": [model_to_dict(report) for report in reports],
        "system_trust_scores": [model_to_dict(score) for score in trust_scores],
        "field_testing_queue": [
            model_to_dict(review)
            for review in lead_quality_reviews
            if review.recommended_next_action in {"call_priority", "underwrite_now"}
        ],
        "real_lead_qa_queue": [
            model_to_dict(review)
            for review in lead_quality_reviews
            if review.import_confidence < 70 or review.blocked_reasons
        ],
        "first_deal_candidates": [
            model_to_dict(review)
            for review in lead_quality_reviews
            if review.import_confidence >= 70 and review.lead_id
        ],
        "prediction_accuracy_warnings": [
            model_to_dict(record)
            for record in prediction_feedback
            if record.accuracy_score < 70
        ],
        "hard_boundary": HARD_BOUNDARY_FLAGS,
        "semi_autonomous_cannot_bypass_approvals": True,
        "level_5_disabled": True,
    }
