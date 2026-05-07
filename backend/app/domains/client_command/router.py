from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.client_command.service import (
    ClientCommandPermissionError,
    hot_board,
    lead_detail,
    leads_for_workspace,
    list_workspaces,
    next_actions,
    require_member_permission,
    score_lead,
    workspace_detail,
)


router = APIRouter(prefix="/api/v1/client-command", tags=["client-command"])


@router.get("/workspaces")
def workspaces(session: Session = Depends(get_session)) -> dict[str, object]:
    return list_workspaces(session)


@router.get("/workspaces/{workspace_id}")
def workspace(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return workspace_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/leads")
def workspace_leads(
    workspace_id: str,
    member_email: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        if member_email:
            require_member_permission(session, workspace_id, member_email, "client_command.leads_view")
        return leads_for_workspace(session, workspace_id)
    except ClientCommandPermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads/hot-board")
def leads_hot_board(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return hot_board(session, workspace_id)


@router.get("/leads/next-actions")
def leads_next_actions(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return next_actions(session, workspace_id)


@router.get("/leads/{lead_id}")
def lead(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return lead_detail(session, lead_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads/{lead_id}/score")
def lead_score(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = score_lead(session, lead_id, workspace_id)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
