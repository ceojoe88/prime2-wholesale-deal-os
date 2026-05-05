from __future__ import annotations

from hashlib import sha256
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models import (
    ApprovedTemplate,
    AutoExecutionAttempt,
    AutoExecutionAuditRecord,
    AutoExecutionDryRun,
    AutoExecutionRule,
)
from app.serializers import model_to_dict


AUTO_EXECUTION_ALLOWED_ACTIONS = {
    "internal_reminder",
    "operator_task_creation",
    "seller_follow_up_draft",
    "buyer_response_draft",
    "low_risk_single_message_send",
}

AUTO_EXECUTION_BLOCKED_ACTIONS = {
    "bulk_campaign": "Bulk campaigns are blocked.",
    "buyer_blast": "Buyer blasts are blocked.",
    "cold_sms_automation": "Cold SMS automation is blocked.",
    "legal_contract_message": "Legal or contract messages are blocked.",
    "seller_pressure_message": "Seller pressure language is blocked.",
}

AUTO_EXECUTION_UNSAFE_PATTERNS = {
    "pressure_language": ["must sign now", "last chance", "sign today or lose"],
    "fake_urgency": ["this will sell today", "only chance", "act immediately"],
    "fake_buyer_claim": ["i have buyers lined up", "we already have a buyer"],
    "legal_advice": ["this is legal advice", "no attorney needed", "legally required"],
    "contract_execution": ["execute this contract", "binding contract", "sign the contract"],
    "hidden_assignment_fee": ["hide the assignment fee", "do not disclose our fee"],
    "unsupported_claim": ["guaranteed close", "guaranteed profit"],
}


def content_hash(subject: str, body: str) -> str:
    return sha256(f"{subject}\n{body}".encode("utf-8")).hexdigest()


def validate_auto_execution_template(template: ApprovedTemplate | None) -> dict[str, object]:
    if template is None:
        return {
            "allowed": False,
            "blocked": True,
            "risk_flags": ["template_missing"],
        }
    text = f"{template.subject} {template.body}".lower()
    flags = sorted(
        {
            category
            for category, phrases in AUTO_EXECUTION_UNSAFE_PATTERNS.items()
            if any(phrase in text for phrase in phrases)
        }
    )
    if template.requires_opt_out and not template.includes_opt_out:
        flags.append("missing_sms_opt_out")
    if not template.approved:
        flags.append("template_not_approved")
    return {
        "allowed": not flags,
        "blocked": bool(flags),
        "risk_flags": sorted(set(flags)),
        "template_id": template.id,
        "template_type": template.template_type,
    }


def auto_execution_gate(
    rule: AutoExecutionRule | None,
    template: ApprovedTemplate | None,
    *,
    recipient_count: int = 1,
    v5_safety_passed: bool = False,
    v5_dry_run_receipt_exists: bool = False,
    v5_approval_recorded: bool = False,
    live_flags_enabled: bool = False,
    provider_ready: bool = False,
) -> dict[str, object]:
    reasons: list[str] = []
    if rule is None:
        reasons.append("approved_rule_missing")
    if template is None:
        reasons.append("approved_template_missing")
    if rule is not None and rule.status != "approved":
        reasons.append("rule_not_approved")
    if rule is not None and rule.action_type not in AUTO_EXECUTION_ALLOWED_ACTIONS:
        reasons.append("action_not_allowed_for_auto_execution")
    if rule is not None and rule.autonomy_level >= 5:
        reasons.append("level_5_disabled")
    if rule is not None and rule.risk_score > 35:
        reasons.append("risk_score_too_high")
    if rule is not None and rule.owner_approval_status != "approved":
        reasons.append("owner_approval_not_recorded")
    if rule is not None and rule.bulk_send_allowed:
        reasons.append("bulk_send_enabled")
    if rule is not None and rule.buyer_blast_allowed:
        reasons.append("buyer_blast_enabled")
    if rule is not None and rule.cold_sms_allowed:
        reasons.append("cold_sms_enabled")
    if rule is not None and rule.legal_contract_message_allowed:
        reasons.append("legal_contract_message_enabled")
    if recipient_count != 1:
        reasons.append("single_recipient_required")

    safety = validate_auto_execution_template(template)
    reasons.extend(str(flag) for flag in safety["risk_flags"])

    action_type = rule.action_type if rule is not None else ""
    if action_type == "low_risk_single_message_send":
        if not v5_safety_passed:
            reasons.append("v5_safety_missing")
        if not v5_dry_run_receipt_exists:
            reasons.append("v5_dry_run_missing")
        if not v5_approval_recorded:
            reasons.append("v5_owner_approval_missing")
        if not live_flags_enabled:
            reasons.append("v5_live_flags_disabled")
        if not provider_ready:
            reasons.append("provider_not_ready")
    elif rule is not None and rule.live_flag_required and not live_flags_enabled:
        reasons.append("live_flag_missing")

    allowed = not reasons
    return {
        "can_execute": allowed,
        "blocked_reasons": sorted(set(reasons)),
        "safety_result": safety,
        "provider_call_allowed": allowed and action_type == "low_risk_single_message_send",
        "bulk_send_allowed": False,
        "buyer_blast_allowed": False,
        "legal_contract_message_allowed": False,
        "level_5_available": False,
    }


def sync_auto_execution_rule(rule: AutoExecutionRule) -> dict[str, object]:
    template = rule.approved_template
    gate = auto_execution_gate(
        rule,
        template,
        recipient_count=1,
        v5_safety_passed=rule.action_type != "low_risk_single_message_send",
        v5_dry_run_receipt_exists=rule.action_type != "low_risk_single_message_send",
        v5_approval_recorded=rule.action_type != "low_risk_single_message_send",
        live_flags_enabled=not rule.live_flag_required,
        provider_ready=rule.action_type != "low_risk_single_message_send",
    )
    rule.blocked_reasons = gate["blocked_reasons"]
    rule.bulk_send_allowed = False
    rule.buyer_blast_allowed = False
    rule.legal_contract_message_allowed = False
    rule.cold_sms_allowed = False
    return gate


def create_auto_execution_dry_run(
    session: Session,
    rule: AutoExecutionRule,
    template: ApprovedTemplate,
    idempotency_key: str,
    source_record_type: str,
    source_record_id: str,
    recipient_placeholder: str,
) -> AutoExecutionDryRun:
    existing = (
        session.query(AutoExecutionDryRun)
        .filter(AutoExecutionDryRun.idempotency_key == idempotency_key)
        .one_or_none()
    )
    if existing is not None:
        return existing
    safety = validate_auto_execution_template(template)
    dry_run = AutoExecutionDryRun(
        id=f"auto-dryrun-{uuid4().hex[:10]}",
        rule_id=rule.id,
        template_id=template.id,
        source_record_type=source_record_type,
        source_record_id=source_record_id,
        recipient_type=rule.allowed_recipient_type,
        recipient_placeholder=recipient_placeholder,
        subject_body_hash=content_hash(template.subject, template.body),
        safety_passed=bool(safety["allowed"]),
        safety_result=safety,
        risk_status="clear" if safety["allowed"] else "blocked",
        provider_mode="mock/dry_run",
        idempotency_key=idempotency_key,
        status="created",
    )
    session.add(dry_run)
    session.flush()
    return dry_run


def execute_with_auto_gate(
    session: Session,
    *,
    rule_id: str | None,
    template_id: str | None,
    idempotency_key: str,
    source_record_type: str = "",
    source_record_id: str = "",
    recipient_count: int = 1,
    v5_safety_passed: bool = False,
    v5_dry_run_receipt_exists: bool = False,
    v5_approval_recorded: bool = False,
    live_flags_enabled: bool = False,
    provider_ready: bool = False,
) -> dict[str, object]:
    existing = (
        session.query(AutoExecutionAttempt)
        .filter(AutoExecutionAttempt.idempotency_key == idempotency_key)
        .one_or_none()
    )
    if existing is not None:
        return {
            **model_to_dict(existing),
            "idempotent_replay": True,
            "duplicate_provider_call": False,
        }

    rule = session.get(AutoExecutionRule, rule_id) if rule_id else None
    template = session.get(ApprovedTemplate, template_id) if template_id else None
    gate = auto_execution_gate(
        rule,
        template,
        recipient_count=recipient_count,
        v5_safety_passed=v5_safety_passed,
        v5_dry_run_receipt_exists=v5_dry_run_receipt_exists,
        v5_approval_recorded=v5_approval_recorded,
        live_flags_enabled=live_flags_enabled,
        provider_ready=provider_ready,
    )
    dry_run = None
    if rule is not None and template is not None:
        dry_run = create_auto_execution_dry_run(
            session,
            rule,
            template,
            f"{idempotency_key}:dry-run",
            source_record_type,
            source_record_id,
            f"{rule.allowed_recipient_type}-placeholder",
        )
    status = "mock_sent" if gate["can_execute"] else "blocked"
    attempt = AutoExecutionAttempt(
        id=f"auto-attempt-{uuid4().hex[:10]}",
        rule_id=rule.id if rule else None,
        template_id=template.id if template else None,
        dry_run_id=dry_run.id if dry_run else None,
        action_type=rule.action_type if rule else "missing_rule",
        source_record_type=source_record_type,
        source_record_id=source_record_id,
        recipient_type=rule.allowed_recipient_type if rule else "",
        recipient_count=recipient_count,
        attempt_status=status,
        blocked_reasons=gate["blocked_reasons"],
        safety_result=gate["safety_result"],
        owner_approval_recorded=bool(rule and rule.owner_approval_status == "approved"),
        v5_safety_passed=v5_safety_passed,
        v5_dry_run_receipt_exists=v5_dry_run_receipt_exists,
        v5_approval_recorded=v5_approval_recorded,
        live_flags_enabled=live_flags_enabled,
        provider_ready=provider_ready,
        provider_called=bool(gate["provider_call_allowed"]),
        provider_mode="mock/dry_run",
        idempotency_key=idempotency_key,
        audit_record_created=True,
    )
    session.add(attempt)
    session.flush()
    audit = AutoExecutionAuditRecord(
        id=f"auto-audit-{uuid4().hex[:10]}",
        attempt_id=attempt.id,
        rule_id=attempt.rule_id,
        event_type="single_execution_attempt",
        source_record_type=source_record_type,
        source_record_id=source_record_id,
        outcome=status,
        blocked_reasons=gate["blocked_reasons"],
        safety_snapshot=gate,
        provider_called=attempt.provider_called,
        idempotency_key=f"{idempotency_key}:audit",
    )
    session.add(audit)
    session.commit()
    return {
        **model_to_dict(attempt),
        "gate": gate,
        "idempotent_replay": False,
        "duplicate_provider_call": False,
    }


def auto_execution_dashboard(session: Session) -> dict[str, object]:
    rules = session.query(AutoExecutionRule).all()
    templates = session.query(ApprovedTemplate).all()
    for rule in rules:
        sync_auto_execution_rule(rule)
    dry_runs = session.query(AutoExecutionDryRun).all()
    attempts = session.query(AutoExecutionAttempt).all()
    audits = session.query(AutoExecutionAuditRecord).all()
    blocked = [
        model_to_dict(attempt)
        for attempt in attempts
        if attempt.attempt_status == "blocked" or attempt.blocked_reasons
    ]
    return {
        "auto_execution_rules": [
            {**model_to_dict(rule), "gate": sync_auto_execution_rule(rule)}
            for rule in rules
        ],
        "approved_templates": [
            {**model_to_dict(template), "safety": validate_auto_execution_template(template)}
            for template in templates
        ],
        "dry_runs": [model_to_dict(dry_run) for dry_run in dry_runs],
        "attempts": [model_to_dict(attempt) for attempt in attempts],
        "audit_records": [model_to_dict(audit) for audit in audits],
        "blocked_attempts": blocked,
        "allowed_actions": sorted(AUTO_EXECUTION_ALLOWED_ACTIONS),
        "blocked_actions": AUTO_EXECUTION_BLOCKED_ACTIONS,
        "live_send_limits": {
            "single_recipient": True,
            "bulk_send_allowed": False,
            "buyer_blast_allowed": False,
            "campaign_allowed": False,
            "legal_contract_message_allowed": False,
        },
    }
