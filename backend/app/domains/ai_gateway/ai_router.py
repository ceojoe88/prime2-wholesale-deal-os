from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.core.config import settings
from app.domains.ai_gateway.ai_audit import record_ai_audit
from app.domains.ai_gateway.ai_cost_tracker import (
    cost_gate,
    create_cost_ledger,
    estimate_tokens,
)
from app.domains.ai_gateway.ai_safety import (
    combine_safety_results,
    scan_ai_text,
    validate_ai_request_type,
)
from app.domains.ai_gateway.ai_templates import build_template_response, template_for
from app.models import AIRequestLog, AITemplate
from app.serializers import model_to_dict


def _template_record(session: Session, request_type: str, template_id: str | None) -> AITemplate | None:
    if template_id:
        return session.get(AITemplate, template_id)
    return (
        session.query(AITemplate)
        .filter(AITemplate.request_type == request_type, AITemplate.active.is_(True))
        .first()
    )


def _template_safety(template: AITemplate | None) -> dict[str, object]:
    if template is None:
        return {
            "allowed": False,
            "risk_flags": ["template_missing"],
            "blocked_reason": "template_missing",
        }
    flags: list[str] = []
    if not template.active:
        flags.append("template_inactive")
    if template.safety_status != "approved":
        flags.append("template_not_approved")
    if not template.uses_system_data_only:
        flags.append("template_not_system_data_only")
    if template.can_invent_numbers:
        flags.append("template_can_invent_numbers")
    if template.legal_advice_allowed:
        flags.append("template_legal_advice_enabled")
    if template.contract_generation_allowed:
        flags.append("template_contract_generation_enabled")
    flags.extend(template.risk_flags)
    return {
        "allowed": not flags,
        "risk_flags": sorted(set(flags)),
        "blocked_reason": ", ".join(sorted(set(flags))),
    }


def handle_ai_request(
    session: Session,
    *,
    request_type: str,
    prompt: str = "",
    model: str | None = None,
    source_record_type: str = "",
    source_record_id: str = "",
    source_data: dict[str, Any] | None = None,
    template_id: str | None = None,
) -> dict[str, object]:
    normalized_type = request_type.strip().lower()
    selected_model = model or settings.ai_default_model
    source_data = source_data or {}
    template = _template_record(session, normalized_type, template_id)
    template_definition = (
        template_for(normalized_type)
        if normalized_type in {
            "seller_script_draft",
            "buyer_message_draft",
            "objection_response",
            "deal_summary",
            "daily_briefing",
            "negotiation_assist",
            "field_testing_summary",
            "call_intelligence_extraction",
        }
        else {}
    )
    template_text = (
        template.template_body if template else str(template_definition.get("template_body", ""))
    )
    token_estimate = estimate_tokens(prompt, template_text, str(source_data))
    cost = cost_gate(session, selected_model, token_estimate)
    type_safety = validate_ai_request_type(normalized_type)
    prompt_safety = scan_ai_text(prompt)
    template_result = _template_safety(template)
    combined = combine_safety_results(type_safety, prompt_safety, template_result, cost)
    response = ""
    response_safety = {"allowed": True, "risk_flags": []}

    if combined["allowed"]:
        response = build_template_response(normalized_type, source_data)
        response_safety = scan_ai_text(response)
        combined = combine_safety_results(combined, response_safety)
        if not combined["allowed"]:
            response = ""

    status = "approved" if combined["allowed"] else "blocked"
    blocked_reason = str(combined.get("blocked_reason") or "")
    request = AIRequestLog(
        id=f"ai-request-{session.query(AIRequestLog).count() + 1:03d}",
        request_type=normalized_type,
        model=selected_model,
        template_id=template.id if template else None,
        source_record_type=source_record_type,
        source_record_id=source_record_id,
        prompt=prompt,
        source_data=source_data,
        token_estimate=int(cost["token_estimate"]),
        cost_estimate=float(cost["cost_estimate"]),
        response=response,
        safety_status=status,
        blocked_reason=blocked_reason,
        safety_result={
            **combined,
            "request_type_safety": type_safety,
            "prompt_safety": prompt_safety,
            "template_safety": template_result,
            "response_safety": response_safety,
            "cost_gate": cost,
            "uses_system_data_only": template.uses_system_data_only if template else False,
        },
        provider_mode=settings.ai_provider_mode,
        monthly_cost_after_request=float(cost["monthly_total_after_request"]),
        real_provider_called=False,
        legal_advice_allowed=False,
        contract_generation_allowed=False,
        financial_calculation_override_allowed=False,
    )
    session.add(request)
    session.flush()
    create_cost_ledger(
        session,
        request_id=request.id,
        request_type=normalized_type,
        model=selected_model,
        token_estimate=request.token_estimate,
        cost_estimate=request.cost_estimate,
        monthly_total_after=request.monthly_cost_after_request,
    )
    record_ai_audit(
        session,
        request,
        event_type="ai_response_approved" if status == "approved" else "ai_response_blocked",
    )
    session.commit()
    return {
        **model_to_dict(request),
        "allowed": status == "approved",
        "template_enforced": template is not None,
        "provider_call_made": False,
        "openai_api_key_loaded_from_env": bool(settings.openai_api_key),
    }
