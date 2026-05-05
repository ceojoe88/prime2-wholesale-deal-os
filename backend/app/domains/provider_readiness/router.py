from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.provider_readiness.schemas import ProviderAttemptRequest, WebhookEventRequest
from app.domains.provider_readiness.service import (
    create_provider_attempt,
    provider_detail,
    provider_registry_dashboard,
    record_webhook_event,
)


router = APIRouter(prefix="/api/v1/provider-readiness", tags=["provider-readiness"])


@router.get("")
def provider_readiness_index(session: Session = Depends(get_session)) -> dict[str, object]:
    return provider_registry_dashboard(session)


@router.get("/attempts")
def provider_attempts(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = provider_registry_dashboard(session)
    return {
        "provider_attempts": dashboard["provider_attempts"],
        "provider_called": False,
        "real_network_call_made": False,
    }


@router.get("/webhooks")
def provider_webhooks(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = provider_registry_dashboard(session)
    return {
        "webhook_events": dashboard["webhook_events"],
        "webhooks_mutate_deals_automatically": False,
        "unsigned_live_like_webhooks_allowed": False,
    }


@router.get("/credentials")
def provider_credentials(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = provider_registry_dashboard(session)
    return {
        "providers": dashboard["providers"],
        "credential_posture": dashboard["credential_posture"],
        "raw_secret_exposed": False,
        "credential_source": "env_only",
    }


@router.get("/{provider_id}")
def provider_readiness_detail(
    provider_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    detail = provider_detail(session, provider_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    return detail


@router.post("/attempts")
def provider_attempt(
    payload: ProviderAttemptRequest,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return create_provider_attempt(session, **payload.model_dump())


@router.post("/webhooks")
def webhook_event(
    payload: WebhookEventRequest,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    result = record_webhook_event(session, **payload.model_dump())
    if result["normalized_event_status"] == "blocked":
        raise HTTPException(status_code=400, detail=result)
    return result
