from __future__ import annotations

from uuid import uuid4

from sqlalchemy.orm import Session

from app.domains.campaign_brain.safety import campaign_rule_gate, sequence_step_safety
from app.domains.campaign_brain.sanitizer import sanitize_campaign_record
from app.domains.campaign_brain.segmentation import buyer_audience_preview, seller_audience_preview
from app.models import (
    ApprovedTemplate,
    CampaignActivationAttempt,
    CampaignAudiencePreview,
    CampaignPerformanceRecord,
    CampaignRuleRecord,
    CampaignSequenceStep,
    CampaignStopEvent,
)


def _next_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:10]}"


def _default_stop_conditions() -> list[str]:
    return [
        "recipient_replies",
        "dnc_detected",
        "compliance_risk_detected",
        "seller_legal_question",
        "buyer_terms_not_approved",
        "provider_readiness_fails",
        "owner_pauses",
        "max_attempts_reached",
    ]


def create_campaign(session: Session, **payload: object) -> dict[str, object]:
    campaign_id = f"campaign-{session.query(CampaignRuleRecord).count() + 1:03d}"
    rule = CampaignRuleRecord(
        id=_next_id("campaign-rule"),
        campaign_id=campaign_id,
        name=str(payload.get("name") or "Controlled campaign draft"),
        campaign_type=str(payload.get("campaign_type") or "seller_follow_up"),
        audience_type=str(payload.get("audience_type") or "seller"),
        segment_definition=dict(payload.get("segment_definition") or {}),
        approved_template_ids=list(payload.get("approved_template_ids") or []),
        max_recipients_per_day=int(payload.get("max_recipients_per_day") or 0),
        max_messages_per_recipient=int(payload.get("max_messages_per_recipient") or 1),
        send_window_start=str(payload.get("send_window_start") or ""),
        send_window_end=str(payload.get("send_window_end") or ""),
        cooldown_hours=int(payload.get("cooldown_hours") or 24),
        stop_conditions=list(payload.get("stop_conditions") or []),
        owner_approval_status=str(payload.get("owner_approval_status") or "pending"),
        live_flag_required=True,
        provider_readiness_required=True,
        status="draft",
        audience_preview_approved=bool(payload.get("audience_preview_approved")),
        live_send_allowed=bool(payload.get("live_send_allowed")) and False,
        bulk_blast_allowed=False,
        one_message_event_model=True,
    )
    gate = campaign_rule_gate(rule)
    rule.safety_status = "passed" if not gate["blocked_reasons"] else "blocked"
    rule.blocked_reasons = list(gate["blocked_reasons"])
    session.add(rule)
    session.flush()
    preview_campaign_audience(session, rule.campaign_id)
    prepare_campaign_sequence(session, rule.campaign_id)
    session.add(
        CampaignPerformanceRecord(
            id=_next_id("campaign-performance"),
            campaign_id=rule.campaign_id,
            recipients_queued=0,
            messages_prepared=0,
            dry_runs_passed=0,
            approvals_pending=1,
            attempts_blocked=0,
            responses_received=0,
            dnc_events=0,
            conversions_to_call=0,
            conversions_to_appointment=0,
            conversions_to_interest=0,
            campaign_health_score=40,
            roi_claims_allowed=False,
            guaranteed_profit_language_allowed=False,
            bulk_blast_allowed=False,
        )
    )
    session.commit()
    return campaign_detail(session, rule.campaign_id)


def preview_campaign_audience(session: Session, campaign_id: str) -> list[dict[str, object]]:
    rule = _get_rule(session, campaign_id)
    session.query(CampaignAudiencePreview).filter_by(campaign_id=campaign_id).delete()
    segment_name = str(rule.segment_definition.get("segment") or "")
    if rule.audience_type == "buyer":
        rows = buyer_audience_preview(
            session,
            segment_name or "reliability_high",
            deal_id=rule.segment_definition.get("deal_id"),
        )
    else:
        rows = seller_audience_preview(session, segment_name or "hot_motivation")
    records = []
    for row in rows:
        record = CampaignAudiencePreview(
            id=_next_id("campaign-preview"),
            campaign_id=campaign_id,
            recipient_id=str(row["recipient_id"]),
            recipient_type=str(row["recipient_type"]),
            segment_name=str(row["segment_name"]),
            inclusion_status=str(row["inclusion_status"]),
            excluded=bool(row["excluded"]),
            exclusion_reasons=list(row["exclusion_reasons"]),
            score=float(row["score"]),
            preview_approved=False,
            do_not_contact=bool(row["do_not_contact"]),
            compliance_risk_status=str(row["compliance_risk_status"]),
            consent_status=str(row["consent_status"]),
        )
        session.add(record)
        records.append(record)
    session.flush()
    return [sanitize_campaign_record(record) for record in records]


def prepare_campaign_sequence(session: Session, campaign_id: str) -> list[dict[str, object]]:
    rule = _get_rule(session, campaign_id)
    if session.query(CampaignSequenceStep).filter_by(campaign_id=campaign_id).count():
        return [
            sanitize_campaign_record(record)
            for record in session.query(CampaignSequenceStep).filter_by(campaign_id=campaign_id).all()
        ]
    purposes = (
        ["checking if still interested", "offer clarification", "appointment reminder"]
        if rule.audience_type == "seller"
        else ["new deal notice", "POF request", "offer intent follow-up"]
    )
    steps = []
    for index, purpose in enumerate(purposes, start=1):
        template_id = rule.approved_template_ids[min(index - 1, len(rule.approved_template_ids) - 1)] if rule.approved_template_ids else None
        step = CampaignSequenceStep(
            id=_next_id("campaign-step"),
            campaign_id=campaign_id,
            step_order=index,
            message_purpose=purpose,
            template_id=template_id,
            timing_offset_hours=(index - 1) * rule.cooldown_hours,
            recipient_type=rule.audience_type,
            dry_run_status="not_started",
            approval_status="pending",
            stop_condition="stop if recipient replies, DNC, compliance risk, provider failure, owner pause, or max attempts",
            draft_only=True,
            live_send_allowed=False,
            bulk_send_allowed=False,
            deceptive_scarcity_allowed=False,
        )
        safety = sequence_step_safety(step)
        step.safety_status = "passed" if safety["allowed"] else "blocked"
        session.add(step)
        steps.append(step)
    session.flush()
    return [sanitize_campaign_record(step) for step in steps]


def activation_gate(
    session: Session,
    campaign_id: str,
    *,
    idempotency_key: str | None = None,
    live_send_requested: bool = False,
    v5_gate_passed: bool = False,
    v13_gate_passed: bool = False,
    v22_gate_passed: bool = False,
    provider_readiness_passed: bool = False,
    live_flag_enabled: bool = False,
) -> dict[str, object]:
    rule = _get_rule(session, campaign_id)
    key = idempotency_key or f"{campaign_id}:activation"
    existing = session.query(CampaignActivationAttempt).filter_by(idempotency_key=key).one_or_none()
    if existing is not None:
        return {
            **sanitize_campaign_record(existing),
            "idempotent_replay": True,
            "duplicate_activation_prevented": True,
        }
    blocked = list(campaign_rule_gate(rule)["blocked_reasons"])
    templates = (
        session.query(ApprovedTemplate)
        .filter(ApprovedTemplate.id.in_(rule.approved_template_ids))
        .all()
        if rule.approved_template_ids
        else []
    )
    if len(templates) != len(rule.approved_template_ids) or any(not template.approved for template in templates):
        blocked.append("all_templates_must_be_approved")
    preview_count = session.query(CampaignAudiencePreview).filter_by(campaign_id=campaign_id).count()
    included_count = (
        session.query(CampaignAudiencePreview)
        .filter_by(campaign_id=campaign_id, excluded=False)
        .count()
    )
    if preview_count == 0:
        blocked.append("audience_preview_required")
    if included_count > rule.max_recipients_per_day:
        blocked.append("daily_recipient_cap_exceeded")
    if live_send_requested:
        if not all([v5_gate_passed, v13_gate_passed, v22_gate_passed, provider_readiness_passed, live_flag_enabled]):
            blocked.append("live_send_requires_v5_v13_v22_provider_live_flags")
    status = "active_controlled" if not blocked else "blocked"
    attempt = CampaignActivationAttempt(
        id=_next_id("campaign-activation"),
        campaign_id=campaign_id,
        attempt_status=status,
        gate_result={
            "preview_count": preview_count,
            "included_count": included_count,
            "live_send_requested": live_send_requested,
            "one_message_event_model": True,
        },
        blocked_reasons=sorted(set(blocked)),
        idempotency_key=key,
        owner_approval_required=True,
        provider_readiness_required=True,
        v5_gate_required=True,
        v13_gate_required=True,
        v22_gate_required=True,
        bulk_blast_allowed=False,
        one_recipient_per_event=True,
        live_send_attempted=False,
    )
    session.add(attempt)
    if not blocked:
        rule.status = "active_controlled"
        rule.live_send_allowed = False
        rule.bulk_blast_allowed = False
    else:
        rule.status = "blocked"
        rule.blocked_reasons = sorted(set(blocked))
    session.commit()
    return {
        **sanitize_campaign_record(attempt),
        "idempotent_replay": False,
        "duplicate_activation_prevented": False,
    }


def pause_campaign_for_stop_event(
    session: Session,
    campaign_id: str,
    *,
    recipient_id: str = "",
    event_type: str,
    reason: str = "",
) -> dict[str, object]:
    rule = _get_rule(session, campaign_id)
    event = CampaignStopEvent(
        id=_next_id("campaign-stop"),
        campaign_id=campaign_id,
        recipient_id=recipient_id,
        event_type=event_type,
        reason=reason or f"Campaign paused because {event_type}.",
        campaign_paused=True,
        owner_review_required=True,
    )
    rule.status = "paused"
    rule.live_send_allowed = False
    session.add(event)
    session.commit()
    return sanitize_campaign_record(event)


def campaign_detail(session: Session, campaign_id: str) -> dict[str, object]:
    rule = _get_rule(session, campaign_id)
    return {
        "campaign": sanitize_campaign_record(rule),
        "audience_preview": [
            sanitize_campaign_record(record)
            for record in session.query(CampaignAudiencePreview).filter_by(campaign_id=campaign_id).all()
        ],
        "sequence_steps": [
            sanitize_campaign_record(record)
            for record in session.query(CampaignSequenceStep).filter_by(campaign_id=campaign_id).all()
        ],
        "activation_attempts": [
            sanitize_campaign_record(record)
            for record in session.query(CampaignActivationAttempt).filter_by(campaign_id=campaign_id).all()
        ],
        "stop_events": [
            sanitize_campaign_record(record)
            for record in session.query(CampaignStopEvent).filter_by(campaign_id=campaign_id).all()
        ],
        "performance": [
            sanitize_campaign_record(record)
            for record in session.query(CampaignPerformanceRecord).filter_by(campaign_id=campaign_id).all()
        ],
        "bulk_blast_allowed": False,
        "one_message_event_model": True,
        "live_send_path_requires_v5_v13_v22": True,
    }


def campaign_dashboard(session: Session) -> dict[str, object]:
    campaigns = session.query(CampaignRuleRecord).order_by(CampaignRuleRecord.created_at.desc()).all()
    previews = session.query(CampaignAudiencePreview).all()
    steps = session.query(CampaignSequenceStep).all()
    attempts = session.query(CampaignActivationAttempt).all()
    stops = session.query(CampaignStopEvent).all()
    performance = session.query(CampaignPerformanceRecord).all()
    return {
        "campaigns": [sanitize_campaign_record(record) for record in campaigns],
        "campaign_drafts": [sanitize_campaign_record(record) for record in campaigns if record.status == "draft"],
        "controlled_active_campaigns": [sanitize_campaign_record(record) for record in campaigns if record.status == "active_controlled"],
        "blocked_campaigns": [sanitize_campaign_record(record) for record in campaigns if record.status == "blocked"],
        "audience_preview": [sanitize_campaign_record(record) for record in previews],
        "dnc_exclusions": [sanitize_campaign_record(record) for record in previews if record.do_not_contact],
        "sequence_steps": [sanitize_campaign_record(record) for record in steps],
        "approvals_needed": [
            sanitize_campaign_record(record)
            for record in campaigns
            if record.owner_approval_status != "approved"
        ],
        "activation_attempts": [sanitize_campaign_record(record) for record in attempts],
        "stop_condition_events": [sanitize_campaign_record(record) for record in stops],
        "performance_records": [sanitize_campaign_record(record) for record in performance],
        "bulk_blast_allowed": False,
        "campaigns_are_draft_by_default": True,
    }


def _get_rule(session: Session, campaign_id: str) -> CampaignRuleRecord:
    rule = (
        session.query(CampaignRuleRecord)
        .filter((CampaignRuleRecord.campaign_id == campaign_id) | (CampaignRuleRecord.id == campaign_id))
        .one_or_none()
    )
    if rule is None:
        raise ValueError("campaign_not_found")
    return rule

