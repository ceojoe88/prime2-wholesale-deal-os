from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.campaign_brain.schemas import (
    CampaignActivationRequest,
    CampaignCreateRequest,
    CampaignStopEventRequest,
)
from app.domains.campaign_brain.service import (
    activation_gate,
    campaign_dashboard,
    campaign_detail,
    create_campaign,
    pause_campaign_for_stop_event,
    prepare_campaign_sequence,
    preview_campaign_audience,
)


router = APIRouter(prefix="/api/v1/campaigns", tags=["campaign-brain"])


@router.get("")
def campaigns(session: Session = Depends(get_session)) -> dict[str, object]:
    return campaign_dashboard(session)


@router.post("")
def campaign_create(
    payload: CampaignCreateRequest,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return create_campaign(session, **payload.model_dump())


@router.get("/segments")
def campaign_segments(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = campaign_dashboard(session)
    return {"audience_preview": dashboard["audience_preview"], "dnc_exclusions": dashboard["dnc_exclusions"]}


@router.get("/sequences")
def campaign_sequences(session: Session = Depends(get_session)) -> dict[str, object]:
    return {"sequence_steps": campaign_dashboard(session)["sequence_steps"], "draft_only": True}


@router.get("/approvals")
def campaign_approvals(session: Session = Depends(get_session)) -> dict[str, object]:
    return {"approvals_needed": campaign_dashboard(session)["approvals_needed"], "owner_approval_required": True}


@router.get("/performance")
def campaign_performance(session: Session = Depends(get_session)) -> dict[str, object]:
    return {
        "performance_records": campaign_dashboard(session)["performance_records"],
        "roi_claims_allowed": False,
        "guaranteed_profit_language_allowed": False,
    }


@router.get("/{campaign_id}")
def campaign_record(campaign_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return campaign_detail(session, campaign_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{campaign_id}/preview")
def campaign_preview(campaign_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        preview = preview_campaign_audience(session, campaign_id)
        session.commit()
        return {"audience_preview": preview, "activation_requires_preview_approval": True}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{campaign_id}/sequences")
def campaign_sequence_prepare(
    campaign_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        steps = prepare_campaign_sequence(session, campaign_id)
        session.commit()
        return {"sequence_steps": steps, "draft_only": True}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{campaign_id}/activate")
def campaign_activate(
    campaign_id: str,
    payload: CampaignActivationRequest,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return activation_gate(session, campaign_id, **payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{campaign_id}/stop-events")
def campaign_stop_event(
    campaign_id: str,
    payload: CampaignStopEventRequest,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return pause_campaign_for_stop_event(session, campaign_id, **payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
