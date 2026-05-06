from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.live_activation.schemas import LiveActivationAttemptRequest
from app.domains.live_activation.service import (
    activation_detail,
    attempt_activation,
    live_activation_dashboard,
)


router = APIRouter(prefix="/api/v1/live-activation", tags=["live-activation"])


@router.get("")
def dashboard(session: Session = Depends(get_session)) -> dict[str, object]:
    return live_activation_dashboard(session)


@router.get("/readiness")
def readiness(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = live_activation_dashboard(session)
    return {
        "ready_activations": dashboard["ready_activations"],
        "blocked_activations": dashboard["blocked_activations"],
        "safety_boundary": dashboard["safety_boundary"],
    }


@router.get("/approvals")
def approvals(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = live_activation_dashboard(session)
    return {
        "activations_needing_owner_approval": [
            item
            for item in dashboard["activations"]
            if item["owner_approval_status"] != "approved"
        ],
        "owner_approval_required": True,
    }


@router.get("/attempts")
def attempts(session: Session = Depends(get_session)) -> dict[str, object]:
    return {"attempts": live_activation_dashboard(session)["attempts"]}


@router.get("/blocked")
def blocked(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = live_activation_dashboard(session)
    return {
        "blocked_activations": dashboard["blocked_activations"],
        "blocked_attempts": dashboard["blocked_attempts"],
    }


@router.get("/{activation_id}")
def detail(activation_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return activation_detail(session, activation_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{activation_id}/attempt")
def attempt(
    activation_id: str,
    request: LiveActivationAttemptRequest,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return attempt_activation(
            session,
            activation_id,
            idempotency_key=request.idempotency_key,
            request_metadata=request.request_metadata,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
