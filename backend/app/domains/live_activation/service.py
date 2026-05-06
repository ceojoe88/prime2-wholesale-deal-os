from __future__ import annotations

import hashlib
import json
from uuid import uuid4

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.domains.cloud_readiness.service import sync_cloud_readiness
from app.domains.live_activation.safety import live_activation_safety
from app.domains.live_activation.sanitizer import sanitize_live_activation_record
from app.domains.provider_readiness.readiness import provider_readiness
from app.domains.provider_readiness.service import create_provider_attempt
from app.models import (
    CampaignActivationAttempt,
    CommunicationDraft,
    LiveProviderActivation,
    LiveProviderActivationAttempt,
    LiveProviderAuditEvent,
    LiveProviderBlockedAttempt,
    ProviderRegistry,
    WorkerJob,
)
from app.serializers import model_to_dict


def metadata_hash(metadata: dict[str, object]) -> str:
    return hashlib.sha256(
        json.dumps(metadata or {}, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()


def source_record_hash(session: Session, activation: LiveProviderActivation) -> str:
    model_by_type = {
        "communication_draft": CommunicationDraft,
        "campaign_activation": CampaignActivationAttempt,
        "worker_job": WorkerJob,
    }
    model = model_by_type.get(activation.source_record_type)
    if model is None or not activation.source_record_id:
        return activation.current_source_hash or ""
    record = session.get(model, activation.source_record_id)
    if record is None:
        return ""
    return metadata_hash(model_to_dict(record))


def refresh_activation_gate(session: Session, activation: LiveProviderActivation) -> dict[str, object]:
    provider = session.get(ProviderRegistry, activation.provider_id) if activation.provider_id else None
    readiness = provider_readiness(
        provider,
        requested_mode=activation.activation_mode,
        owner_approval_recorded=activation.owner_approval_status == "approved",
    )
    cloud = sync_cloud_readiness(session)
    current_hash = source_record_hash(session, activation)
    if current_hash:
        activation.current_source_hash = current_hash
    safety = live_activation_safety(
        activation,
        provider_ready=bool(readiness["ready"]),
        provider_blocked_reasons=list(readiness["blocked_reasons"]),
        production_ready=bool(cloud["production_ready"]),
    )
    activation.readiness_snapshot = {
        "provider": readiness,
        "cloud_production_ready": cloud["production_ready"],
        "cloud_blocked_reasons": cloud["blocked_reasons"],
    }
    activation.safety_snapshot = {
        **(activation.safety_snapshot or {}),
        "gate": safety,
        "source_hash_verified": activation.current_source_hash == activation.dry_run_hash,
    }
    activation.blocked_reasons = list(safety["blocked_reasons"])
    activation.activation_status = "approved_pending_provider" if safety["allowed"] else "blocked"
    activation.provider_called = False
    activation.audit_event_created = True
    return safety


def live_activation_dashboard(session: Session) -> dict[str, object]:
    activations = (
        session.query(LiveProviderActivation)
        .order_by(desc(LiveProviderActivation.created_at))
        .all()
    )
    for activation in activations:
        refresh_activation_gate(session, activation)
    session.commit()
    attempts = (
        session.query(LiveProviderActivationAttempt)
        .order_by(desc(LiveProviderActivationAttempt.created_at))
        .all()
    )
    blocked = (
        session.query(LiveProviderBlockedAttempt)
        .order_by(desc(LiveProviderBlockedAttempt.created_at))
        .all()
    )
    audit = (
        session.query(LiveProviderAuditEvent)
        .order_by(desc(LiveProviderAuditEvent.created_at))
        .all()
    )
    return {
        "activations": [sanitize_live_activation_record(item) for item in activations],
        "ready_activations": [
            sanitize_live_activation_record(item)
            for item in activations
            if item.activation_status == "approved_pending_provider"
        ],
        "blocked_activations": [
            sanitize_live_activation_record(item)
            for item in activations
            if item.activation_status == "blocked"
        ],
        "attempts": [sanitize_live_activation_record(item) for item in attempts],
        "blocked_attempts": [sanitize_live_activation_record(item) for item in blocked],
        "audit_events": [sanitize_live_activation_record(item) for item in audit],
        "safety_boundary": {
            "bulk_email_sms_allowed": False,
            "buyer_blasts_allowed": False,
            "contract_execution_allowed": False,
            "title_submission_allowed": False,
            "payment_handling_allowed": False,
            "worker_bypass_allowed": False,
        },
    }


def activation_detail(session: Session, activation_id: str) -> dict[str, object]:
    activation = session.get(LiveProviderActivation, activation_id)
    if activation is None:
        raise ValueError(f"Activation not found: {activation_id}")
    gate = refresh_activation_gate(session, activation)
    session.commit()
    return {
        "activation": sanitize_live_activation_record(activation),
        "gate": gate,
        "provider_call_executed": False,
    }


def attempt_activation(
    session: Session,
    activation_id: str,
    *,
    idempotency_key: str,
    request_metadata: dict[str, object] | None = None,
) -> dict[str, object]:
    request_metadata = request_metadata or {}
    existing = (
        session.query(LiveProviderActivationAttempt)
        .filter(LiveProviderActivationAttempt.idempotency_key == idempotency_key)
        .one_or_none()
    )
    if existing is not None:
        existing.duplicate_prevented = True
        session.commit()
        return {
            **sanitize_live_activation_record(existing),
            "idempotent_replay": True,
            "duplicate_action_prevented": True,
        }

    activation = session.get(LiveProviderActivation, activation_id)
    if activation is None:
        raise ValueError(f"Activation not found: {activation_id}")
    gate = refresh_activation_gate(session, activation)
    request_hash = metadata_hash(request_metadata)
    provider_attempt = create_provider_attempt(
        session,
        provider_id=activation.provider_id or "",
        source_domain=activation.source_domain,
        action_type=activation.allowed_action_type,
        mode=activation.activation_mode,
        idempotency_key=f"v30:{idempotency_key}",
        request_metadata=request_metadata,
        owner_approval_recorded=activation.owner_approval_status == "approved",
    )
    provider_attempt_id = str(provider_attempt.get("id", ""))
    status = "approved_pending_provider" if gate["allowed"] else "blocked"
    attempt = LiveProviderActivationAttempt(
        id=f"live-attempt-{uuid4().hex[:10]}",
        activation_id=activation.id,
        provider_attempt_id=provider_attempt_id,
        attempt_status=status,
        blocked_reasons=list(gate["blocked_reasons"]),
        idempotency_key=idempotency_key,
        request_metadata_hash=request_hash,
        response_summary={
            "provider_attempt_status": provider_attempt.get("attempt_status"),
            "provider_called": False,
            "response_sanitized": True,
        },
        provider_called=False,
        live_action_executed=False,
        duplicate_prevented=False,
    )
    session.add(attempt)
    if not gate["allowed"]:
        blocked = LiveProviderBlockedAttempt(
            id=f"live-blocked-{uuid4().hex[:10]}",
            activation_id=activation.id,
            source_domain=activation.source_domain,
            action_type=activation.allowed_action_type,
            reason=", ".join(gate["blocked_reasons"]),
            provider_called=False,
            audit_logged=True,
        )
        session.add(blocked)
    audit = LiveProviderAuditEvent(
        id=f"live-audit-{uuid4().hex[:10]}",
        activation_id=activation.id,
        event_type=status,
        summary="V30 live provider activation gate recorded an attempt without unsafe provider execution.",
        safety_snapshot=activation.safety_snapshot,
        readiness_snapshot=activation.readiness_snapshot,
        provider_response_sanitized=True,
        secrets_exposed=False,
        live_action_executed=False,
    )
    session.add(audit)
    session.commit()
    return {
        **sanitize_live_activation_record(attempt),
        "gate": gate,
        "provider_attempt": provider_attempt,
        "idempotent_replay": False,
    }
