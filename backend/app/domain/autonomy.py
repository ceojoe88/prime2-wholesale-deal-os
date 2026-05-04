from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models import (
    AutomationAttempt,
    AutomationEventTrigger,
    AutomationRule,
    AutonomousAgentTask,
    AutonomyEscalation,
    DailyCommandBriefing,
    Deal,
    Division,
    Lead,
    SchedulerRun,
)
from app.serializers import model_to_dict


AUTONOMY_LEVELS = {
    2: "Autonomous internal prep",
    3: "Autonomous draft creation and scheduling",
    4: "Controlled live-action review with owner approval only",
    5: "Disabled and unavailable",
}

WORKFLOWS = {
    "new_lead_intake": {
        "action": "score_leads",
        "agent": "Attention Queue Agent",
        "division": "Operations Command Division",
        "task_type": "lead_scoring",
        "recommendation": "Score new lead, refresh opportunity fields, and route missing data to the owner queue.",
        "priority": "high",
        "level": 2,
    },
    "hot_deal_acceleration": {
        "action": "create_next_best_action",
        "agent": "Deal Commander Agent",
        "division": "Operations Command Division",
        "task_type": "hot_deal_acceleration",
        "recommendation": "Escalate hot spread, prepare safe follow-up drafts, and verify buyer demand before owner review.",
        "priority": "critical",
        "level": 3,
    },
    "buyer_demand_refresh": {
        "action": "refresh_buyer_demand",
        "agent": "Buyer Demand Agent",
        "division": "Buyer Disposition Division",
        "task_type": "buyer_demand_refresh",
        "recommendation": "Refresh buyer fit, POF gaps, closing speed, and sanitized distribution draft readiness.",
        "priority": "high",
        "level": 2,
    },
    "contract_readiness": {
        "action": "mark_internal_readiness",
        "agent": "Deal Confidence Agent",
        "division": "Deal Underwriting Division",
        "task_type": "contract_readiness",
        "recommendation": "Mark internal readiness only when underwriting, profit, compliance, seller readiness, and owner gates pass.",
        "priority": "high",
        "level": 3,
    },
    "daily_command_briefing": {
        "action": "create_daily_briefing",
        "agent": "Daily Briefing Agent",
        "division": "Operations Command Division",
        "task_type": "daily_briefing",
        "recommendation": "Generate Wholesale Prime briefing with hot deals, blockers, owner approvals, and safe next actions.",
        "priority": "normal",
        "level": 3,
    },
}

AUTONOMOUS_ALLOWED_ACTIONS = {
    "score_leads",
    "refresh_deal_scores",
    "update_priority_queues",
    "create_next_best_action",
    "create_follow_up_draft",
    "create_buyer_distribution_draft",
    "create_offer_packet_draft",
    "create_evidence_packet",
    "create_blocker_record",
    "create_daily_briefing",
    "create_manager_queue",
    "create_agent_task",
    "schedule_reminder",
    "escalate_urgent_deal",
    "mark_internal_readiness",
    "refresh_buyer_demand",
    "controlled_live_action_review",
}

AUTONOMOUS_BLOCKED_ACTIONS = {
    "send_sms": "Autonomy may not send SMS.",
    "send_email": "Autonomy may not send email.",
    "call_seller": "Autonomy may not call sellers.",
    "contact_buyer": "Autonomy may not contact buyers.",
    "execute_contract": "Autonomy may not execute contracts.",
    "buyer_blast_execute": "Autonomy may not execute buyer blasts.",
    "live_buyer_blast": "Autonomy may not run live buyer blasts.",
    "bulk_send": "Autonomy may not bulk send.",
    "submit_to_title_company": "Autonomy may not submit to a title company.",
    "submit_review_packet_to_title": "Autonomy may not submit review packets.",
    "collect_payment": "Autonomy may not collect or handle payments.",
    "publish_buyer_portal": "Autonomy may not publish buyer portal data.",
    "publish_seller_portal": "Autonomy may not publish seller portal data.",
    "change_seller_terms": "Autonomy may not change seller terms.",
    "change_buyer_terms": "Autonomy may not change buyer terms.",
    "give_legal_advice": "Autonomy may not provide legal advice.",
    "make_binding_commitment": "Autonomy may not make binding commitments.",
}


def autonomy_safety_guard(
    action: str,
    autonomy_level: int,
    owner_approval_recorded: bool = False,
) -> dict[str, object]:
    normalized = action.strip().lower()
    blocked_reasons: list[str] = []

    if autonomy_level >= 5:
        blocked_reasons.append("level_5_disabled")
    if normalized in AUTONOMOUS_BLOCKED_ACTIONS:
        blocked_reasons.append(normalized)
    if autonomy_level == 4 and not owner_approval_recorded:
        blocked_reasons.append("owner_approval_required_for_level_4")
    if normalized not in AUTONOMOUS_ALLOWED_ACTIONS and normalized not in AUTONOMOUS_BLOCKED_ACTIONS:
        blocked_reasons.append("action_not_allowed_for_autonomy")

    hard_blocked = any(reason in AUTONOMOUS_BLOCKED_ACTIONS for reason in blocked_reasons)
    allowed = not blocked_reasons

    return {
        "allowed": allowed,
        "blocked": not allowed,
        "action": normalized,
        "autonomy_level": autonomy_level,
        "level_description": AUTONOMY_LEVELS.get(autonomy_level, "Unknown level"),
        "blocked_reasons": sorted(set(blocked_reasons)),
        "owner_approval_required": autonomy_level == 4,
        "owner_approval_recorded": owner_approval_recorded,
        "hard_blocked_real_world_action": hard_blocked,
        "real_world_action_allowed": False,
        "level_5_disabled": autonomy_level >= 5,
    }


def sync_automation_rule(rule: AutomationRule) -> None:
    rule.blocked_actions = sorted(AUTONOMOUS_BLOCKED_ACTIONS)
    rule.level_5_disabled = True
    rule.portal_publish_allowed = False
    rule.contract_execution_allowed = False
    rule.title_submission_allowed = False
    rule.payment_collection_allowed = False
    rule.live_action_allowed = False
    rule.draft_only = True
    if rule.autonomy_level >= 5:
        rule.enabled = False
        rule.safety_status = "level_5_disabled"
    elif rule.autonomy_level == 4:
        rule.owner_approval_required = True
        rule.safety_status = "owner_approval_required"
    else:
        rule.safety_status = "guarded"


def _new_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:12]}"


def _source_for_workflow(session: Session, workflow_type: str) -> tuple[str, str]:
    if workflow_type == "new_lead_intake":
        lead = session.query(Lead).order_by(Lead.opportunity_score.desc()).first()
        return ("lead", lead.id if lead else "")
    deal = session.query(Deal).order_by(Deal.projected_assignment_fee.desc()).first()
    return ("deal", deal.id if deal else "")


def create_daily_command_briefing(
    session: Session,
    run_id: str | None = None,
    briefing_id: str | None = None,
) -> DailyCommandBriefing:
    hot_deals = (
        session.query(Deal)
        .filter(Deal.is_hot_opportunity.is_(True))
        .order_by(Deal.projected_assignment_fee.desc())
        .limit(5)
        .all()
    )
    divisions = session.query(Division).order_by(Division.workload.desc()).limit(5).all()
    escalations = (
        session.query(AutonomyEscalation)
        .filter(AutonomyEscalation.status == "open")
        .order_by(AutonomyEscalation.created_at.desc())
        .limit(5)
        .all()
    )
    today = datetime.now(UTC).date().isoformat()
    briefing = DailyCommandBriefing(
        id=briefing_id or _new_id("daily-briefing"),
        run_id=run_id,
        briefing_date=today,
        generated_by="Wholesale Prime",
        hot_deals=[
            {
                "deal_id": deal.id,
                "projected_assignment_fee": deal.projected_assignment_fee,
                "deal_speed_score": deal.deal_speed_score,
                "next_best_action": "Review gates, then approve only draft-ready next steps.",
            }
            for deal in hot_deals
        ],
        priority_actions=[
            "Review hot-deal escalations before any real-world action.",
            "Approve or reject pending Level 4 communication reviews.",
            "Resolve buyer POF, compliance, and owner-approval blockers.",
            "Keep portal publishing, title submission, contracts, and payments disabled.",
        ],
        manager_queue=[
            {
                "division": division.name,
                "manager": division.manager_name,
                "workload": division.workload,
                "next_best_action": division.next_best_action,
            }
            for division in divisions
        ],
        escalations=[
            {
                "id": escalation.id,
                "severity": escalation.severity,
                "reason": escalation.reason,
                "recommended_action": escalation.recommended_action,
            }
            for escalation in escalations
        ],
        safety_summary={
            "autonomy_default_levels": AUTONOMY_LEVELS,
            "live_outreach_allowed": False,
            "buyer_blasts_allowed": False,
            "contract_execution_allowed": False,
            "title_submission_allowed": False,
            "portal_publishing_allowed": False,
            "level_5_available": False,
        },
        owner_review_items=[
            "Level 4 actions require owner approval and still cannot bypass provider gates.",
            "Escalations are recommendations only.",
            "No binding commitments are generated by the scheduler.",
        ],
        draft_only=True,
        legal_advice_allowed=False,
        live_outreach_allowed=False,
        portal_publish_allowed=False,
        title_submission_allowed=False,
        contract_execution_allowed=False,
    )
    session.add(briefing)
    return briefing


def run_scheduler_workflow(
    session: Session,
    workflow_type: str,
    idempotency_key: str,
    owner_approval_recorded: bool = False,
) -> dict[str, object]:
    existing = (
        session.query(SchedulerRun)
        .filter(SchedulerRun.idempotency_key == idempotency_key)
        .one_or_none()
    )
    if existing is not None:
        existing.idempotent_replay = True
        session.commit()
        return {
            **model_to_dict(existing),
            "idempotent_replay": True,
            "duplicate_tasks_created": 0,
        }

    workflow = WORKFLOWS.get(workflow_type)
    if workflow is None:
        guard = autonomy_safety_guard("unknown_workflow", 2)
        return {"created": False, "workflow_type": workflow_type, "safety_result": guard}

    rule = (
        session.query(AutomationRule)
        .filter(AutomationRule.workflow_type == workflow_type, AutomationRule.enabled.is_(True))
        .first()
    )
    level = rule.autonomy_level if rule else int(workflow["level"])
    safety = autonomy_safety_guard(
        str(workflow["action"]),
        level,
        owner_approval_recorded=owner_approval_recorded,
    )
    run = SchedulerRun(
        id=_new_id("run"),
        rule_id=rule.id if rule else None,
        workflow_type=workflow_type,
        run_status="completed" if safety["allowed"] else "blocked",
        scheduled_for=datetime.now(UTC),
        started_at=datetime.now(UTC),
        finished_at=datetime.now(UTC),
        idempotency_key=idempotency_key,
        owner_approval_required=bool(safety["owner_approval_required"]),
        autonomy_level=level,
        summary={
            "workflow": workflow_type,
            "action": workflow["action"],
            "safe_internal_prep_only": True,
            "real_world_action_taken": False,
        },
        real_world_action_taken=False,
    )
    session.add(run)
    session.flush()

    source_type, source_id = _source_for_workflow(session, workflow_type)
    attempt = AutomationAttempt(
        id=_new_id("attempt"),
        run_id=run.id,
        action_type=str(workflow["action"]),
        source_record_type=source_type,
        source_record_id=source_id,
        attempt_status="prepared" if safety["allowed"] else "blocked",
        autonomy_level=level,
        safety_result=safety,
        blocked_reasons=safety["blocked_reasons"],
        owner_approval_required=bool(safety["owner_approval_required"]),
        owner_approval_recorded=owner_approval_recorded,
        provider_called=False,
        real_world_action_taken=False,
        idempotency_key=f"{idempotency_key}:attempt:{workflow['action']}",
    )
    session.add(attempt)

    task_count = 0
    if safety["allowed"]:
        task = AutonomousAgentTask(
            id=_new_id("task"),
            rule_id=rule.id if rule else None,
            run_id=run.id,
            agent_name=str(workflow["agent"]),
            division=str(workflow["division"]),
            task_type=str(workflow["task_type"]),
            source_record_type=source_type,
            source_record_id=source_id,
            priority=str(workflow["priority"]),
            status="queued_for_internal_review",
            recommendation=str(workflow["recommendation"]),
            due_at=datetime.now(UTC),
            idempotency_key=f"{idempotency_key}:task:{workflow['task_type']}",
            owner_approval_required=level >= 4,
            draft_only=True,
            live_action_allowed=False,
            readiness_marked=workflow_type == "contract_readiness",
        )
        session.add(task)
        task_count += 1

    run.created_attempts = 1
    run.created_tasks = task_count

    if workflow_type == "hot_deal_acceleration" and source_id:
        escalation = AutonomyEscalation(
            id=_new_id("escalation"),
            run_id=run.id,
            deal_id=source_id,
            lead_id=None,
            escalation_type="hot_deal_acceleration",
            severity="critical",
            reason="Hot 10K+ spread needs owner review before any live action.",
            recommended_action="Review seller follow-up draft, buyer demand, compliance gates, and approval status.",
            status="open",
            owner_action_required=True,
            autonomy_level=level,
            real_world_action_blocked=True,
            idempotency_key=f"{idempotency_key}:escalation:hot-deal",
        )
        session.add(escalation)
        run.escalation_created = True

    if workflow_type == "daily_command_briefing":
        create_daily_command_briefing(
            session,
            run_id=run.id,
            briefing_id=f"daily-briefing-{uuid4().hex[:10]}",
        )
        run.daily_briefing_created = True

    if rule is not None:
        rule.last_run_status = run.run_status
        sync_automation_rule(rule)

    session.commit()
    return {
        **model_to_dict(run),
        "safety_result": safety,
        "duplicate_tasks_created": 0,
    }


def automation_rule_summary(rule: AutomationRule) -> dict[str, object]:
    sync_automation_rule(rule)
    return {
        **model_to_dict(rule),
        "level_description": AUTONOMY_LEVELS.get(rule.autonomy_level),
        "level_5_available": False,
        "real_world_actions_blocked": True,
    }


def daily_briefing_summary(briefing: DailyCommandBriefing) -> dict[str, object]:
    return {
        **model_to_dict(briefing),
        "generated_by": "Wholesale Prime",
        "recommendations_only": True,
        "legal_advice_allowed": False,
        "live_outreach_allowed": False,
        "portal_publish_allowed": False,
        "title_submission_allowed": False,
        "contract_execution_allowed": False,
    }


def autonomy_dashboard(session: Session) -> dict[str, object]:
    rules = session.query(AutomationRule).all()
    for rule in rules:
        sync_automation_rule(rule)
    runs = session.query(SchedulerRun).order_by(SchedulerRun.created_at.desc()).all()
    attempts = (
        session.query(AutomationAttempt).order_by(AutomationAttempt.created_at.desc()).all()
    )
    tasks = (
        session.query(AutonomousAgentTask)
        .order_by(AutonomousAgentTask.created_at.desc())
        .all()
    )
    triggers = (
        session.query(AutomationEventTrigger)
        .order_by(AutomationEventTrigger.created_at.desc())
        .all()
    )
    briefings = (
        session.query(DailyCommandBriefing)
        .order_by(DailyCommandBriefing.created_at.desc())
        .all()
    )
    escalations = (
        session.query(AutonomyEscalation)
        .order_by(AutonomyEscalation.created_at.desc())
        .all()
    )
    blocked_attempts = [
        model_to_dict(attempt)
        for attempt in attempts
        if attempt.attempt_status == "blocked" or attempt.blocked_reasons
    ]

    return {
        "autonomy_levels": AUTONOMY_LEVELS,
        "default_autonomy": {
            "level_2": "autonomous internal prep",
            "level_3": "autonomous draft creation and scheduling",
            "level_4": "controlled live-action review with owner approval only",
            "level_5": "disabled/unavailable",
        },
        "automation_rules": [automation_rule_summary(rule) for rule in rules],
        "scheduler_runs": [model_to_dict(run) for run in runs],
        "automation_attempts": [model_to_dict(attempt) for attempt in attempts],
        "autonomous_agent_tasks": [model_to_dict(task) for task in tasks],
        "event_triggers": [model_to_dict(trigger) for trigger in triggers],
        "daily_command_briefings": [
            daily_briefing_summary(briefing) for briefing in briefings
        ],
        "escalations": [model_to_dict(escalation) for escalation in escalations],
        "draft_creation_tasks": [
            model_to_dict(task)
            for task in tasks
            if task.task_type
            in {
                "follow_up_draft",
                "buyer_distribution_draft",
                "offer_packet_draft",
                "daily_briefing",
            }
        ],
        "escalation_queue": [
            model_to_dict(escalation)
            for escalation in escalations
            if escalation.status == "open"
        ],
        "blocked_attempts": blocked_attempts,
        "level_4_owner_approval_required": [
            automation_rule_summary(rule) for rule in rules if rule.autonomy_level == 4
        ],
        "wholesale_prime_panel": {
            "mode": "near_autonomous_internal_prep",
            "global_live_action_enabled": False,
            "level_5_available": False,
            "owner_final_approver": True,
            "rules_enabled": len([rule for rule in rules if rule.enabled]),
            "open_tasks": len([task for task in tasks if task.status != "completed"]),
            "open_escalations": len([item for item in escalations if item.status == "open"]),
            "blocked_live_attempts": len(blocked_attempts),
        },
        "safety_boundaries": {
            "autonomous_live_outreach": False,
            "autonomous_buyer_blasts": False,
            "autonomous_contract_execution": False,
            "autonomous_title_submission": False,
            "autonomous_portal_publishing": False,
            "autonomous_payment_collection": False,
            "level_5_available": False,
        },
    }
