from __future__ import annotations

from hashlib import sha256

from sqlalchemy.orm import Session

from app.models import AIAuditRecord, AIRequestLog


def response_hash(response: str) -> str:
    return sha256(response.encode("utf-8")).hexdigest() if response else ""


def record_ai_audit(
    session: Session,
    request: AIRequestLog,
    *,
    event_type: str,
) -> AIAuditRecord:
    audit = AIAuditRecord(
        id=f"ai-audit-{session.query(AIAuditRecord).count() + 1:03d}",
        request_id=request.id,
        event_type=event_type,
        request_type=request.request_type,
        safety_status=request.safety_status,
        blocked_reason=request.blocked_reason,
        source_record_type=request.source_record_type,
        source_record_id=request.source_record_id,
        token_estimate=request.token_estimate,
        cost_estimate=request.cost_estimate,
        response_hash=response_hash(request.response),
        provider_mode=request.provider_mode,
        real_provider_called=False,
    )
    session.add(audit)
    return audit

