from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.config import settings
from app.domains.ai_gateway.ai_cost_tracker import current_period, monthly_total
from app.domains.ai_gateway.ai_safety import ALLOWED_AI_REQUEST_TYPES, BLOCKED_AI_REQUEST_TYPES
from app.models import AIAuditRecord, AICostLedger, AIRequestLog, AITemplate
from app.serializers import model_to_dict


def ai_gateway_dashboard(session: Session) -> dict[str, object]:
    requests = session.query(AIRequestLog).order_by(AIRequestLog.created_at.desc()).all()
    templates = session.query(AITemplate).all()
    audits = session.query(AIAuditRecord).order_by(AIAuditRecord.created_at.desc()).all()
    period = current_period()
    total = monthly_total(session, period)
    return {
        "overseer": settings.overseer_name,
        "provider_mode": settings.ai_provider_mode,
        "openai_key_configured": bool(settings.openai_api_key),
        "allowed_request_types": sorted(ALLOWED_AI_REQUEST_TYPES),
        "blocked_request_types": sorted(BLOCKED_AI_REQUEST_TYPES),
        "requests": [model_to_dict(request) for request in requests],
        "blocked_requests": [
            model_to_dict(request)
            for request in requests
            if request.safety_status == "blocked"
        ],
        "templates": [model_to_dict(template) for template in templates],
        "audit_records": [model_to_dict(audit) for audit in audits],
        "cost_summary": {
            "period": period,
            "monthly_total_estimate": total,
            "monthly_cap": settings.ai_monthly_cost_cap,
            "cap_status": "blocked" if total > settings.ai_monthly_cost_cap else "within_cap",
            "max_tokens_per_request": settings.ai_max_tokens_per_request,
        },
        "real_provider_calls_allowed": False,
        "legal_advice_allowed": False,
        "contract_generation_allowed": False,
        "financial_calculation_override_allowed": False,
    }


def ai_cost_dashboard(session: Session) -> dict[str, object]:
    ledgers = session.query(AICostLedger).order_by(AICostLedger.created_at.desc()).all()
    return {
        "cost_ledgers": [model_to_dict(ledger) for ledger in ledgers],
        "monthly_cost_estimate": monthly_total(session),
        "monthly_cap": settings.ai_monthly_cost_cap,
        "provider_mode": settings.ai_provider_mode,
        "real_provider_calls_allowed": False,
    }

