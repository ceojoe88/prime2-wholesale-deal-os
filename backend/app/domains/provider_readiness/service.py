from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.domains.provider_readiness.readiness import provider_readiness
from app.domains.provider_readiness.sanitizer import (
    sanitize_provider_attempt,
    sanitize_provider_registry,
    sanitize_webhook_event,
)
from app.models import ProviderAttemptAudit, ProviderRegistry, ProviderWebhookEvent


def _hash_metadata(metadata: dict[str, object]) -> str:
    return hashlib.sha256(
        json.dumps(metadata or {}, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()


def provider_registry_dashboard(session: Session) -> dict[str, object]:
    providers = session.query(ProviderRegistry).order_by(ProviderRegistry.provider_type).all()
    attempts = (
        session.query(ProviderAttemptAudit)
        .order_by(ProviderAttemptAudit.created_at.desc())
        .all()
    )
    webhooks = (
        session.query(ProviderWebhookEvent)
        .order_by(ProviderWebhookEvent.received_at.desc())
        .all()
    )
    for provider in providers:
        provider_readiness(provider)
    session.commit()
    return {
        "providers": [sanitize_provider_registry(provider) for provider in providers],
        "blocked_providers": [
            sanitize_provider_registry(provider)
            for provider in providers
            if provider.readiness_status != "ready"
        ],
        "provider_attempts": [sanitize_provider_attempt(attempt) for attempt in attempts],
        "webhook_events": [sanitize_webhook_event(event) for event in webhooks],
        "credential_posture": {
            "stored_secret_count": 0,
            "credential_reference_only": True,
            "env_only": True,
            "live_enabled_count": len([provider for provider in providers if provider.live_enabled]),
        },
        "default_provider_mode": "mock",
        "live_provider_calls_allowed": False,
        "bulk_outreach_allowed": False,
    }


def provider_detail(session: Session, provider_id: str) -> dict[str, object] | None:
    provider = session.get(ProviderRegistry, provider_id)
    if provider is None:
        return None
    readiness = provider_readiness(provider)
    session.commit()
    attempts = (
        session.query(ProviderAttemptAudit)
        .filter(ProviderAttemptAudit.provider_id == provider_id)
        .order_by(ProviderAttemptAudit.created_at.desc())
        .all()
    )
    return {
        "provider": sanitize_provider_registry(provider),
        "readiness": readiness,
        "attempts": [sanitize_provider_attempt(attempt) for attempt in attempts],
        "live_network_call_allowed": False,
    }


def create_provider_attempt(
    session: Session,
    *,
    provider_id: str,
    source_domain: str = "",
    action_type: str = "",
    mode: str = "mock",
    idempotency_key: str = "",
    request_metadata: dict[str, object] | None = None,
    owner_approval_recorded: bool = False,
) -> dict[str, object]:
    request_metadata = request_metadata or {}
    key = idempotency_key or f"{provider_id}:{source_domain}:{action_type}:{_hash_metadata(request_metadata)}"
    existing = (
        session.query(ProviderAttemptAudit)
        .filter(ProviderAttemptAudit.idempotency_key == key)
        .one_or_none()
    )
    if existing is not None:
        return {
            **sanitize_provider_attempt(existing),
            "idempotent_replay": True,
            "duplicate_provider_call_prevented": True,
        }

    provider = session.get(ProviderRegistry, provider_id)
    readiness = provider_readiness(
        provider,
        requested_mode=mode,
        owner_approval_recorded=owner_approval_recorded,
    )
    blocked_reasons = list(readiness["blocked_reasons"])
    normalized_mode = str(readiness.get("mode") or mode or "mock")
    if blocked_reasons:
        status = "blocked"
    elif normalized_mode == "mock":
        status = "mock_success"
    elif normalized_mode == "sandbox":
        status = "sandbox_ready"
    else:
        status = "approved_pending_live"

    attempt = ProviderAttemptAudit(
        id=f"provider-attempt-{uuid4().hex[:10]}",
        provider_id=provider.id if provider else None,
        provider_name=provider.provider_name if provider else "",
        provider_type=provider.provider_type if provider else "",
        source_domain=source_domain,
        action_type=action_type,
        mode=normalized_mode,
        readiness_result=readiness,
        attempt_status=status,
        blocked_reason=", ".join(blocked_reasons),
        idempotency_key=key,
        request_metadata_hash=_hash_metadata(request_metadata),
        response_metadata_summary={
            "network_call": "not_performed",
            "provider_mode": normalized_mode,
            "audit_only": True,
        },
        provider_called=False,
        real_network_call_made=False,
    )
    session.add(attempt)
    session.commit()
    return {
        **sanitize_provider_attempt(attempt),
        "idempotent_replay": False,
        "duplicate_provider_call_prevented": False,
    }


def record_webhook_event(
    session: Session,
    *,
    provider_type: str,
    event_type: str,
    mode: str = "mock",
    signature_present: bool = False,
    signature_valid: bool = False,
    payload_metadata: dict[str, object] | None = None,
) -> dict[str, object]:
    payload_metadata = payload_metadata or {}
    normalized_mode = mode.strip().lower() or "mock"
    blocked_reason = ""
    status = "review_queued"
    if normalized_mode == "live" and not (signature_present and signature_valid):
        blocked_reason = "unsigned_live_like_webhook_rejected"
        status = "blocked"

    event = ProviderWebhookEvent(
        id=f"provider-webhook-{uuid4().hex[:10]}",
        provider_type=provider_type,
        event_type=event_type,
        received_at=datetime.now(UTC),
        mode=normalized_mode,
        signature_present=signature_present,
        signature_valid=signature_valid,
        normalized_event_status=status,
        source_metadata_hash=_hash_metadata(payload_metadata),
        review_task_created=status != "blocked",
        deal_mutation_allowed=False,
        deal_mutated=False,
        raw_payload_stored=False,
        blocked_reason=blocked_reason,
    )
    session.add(event)
    session.commit()
    return sanitize_webhook_event(event)
