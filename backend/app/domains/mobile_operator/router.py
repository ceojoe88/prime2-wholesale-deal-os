from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.mobile_operator.schemas import (
    MobileApprovalGateCheck,
    MobileCallOutcomeCreate,
    MobileDncMark,
    MobileNoteCreate,
    MobileOfflineDraftCreate,
)
from app.domains.mobile_operator.service import (
    approval_queue,
    buyers_snapshot,
    call_queue,
    capture_mobile_note,
    deal_detail,
    documents_snapshot,
    field_briefing,
    lead_detail,
    mobile_overview,
    quick_approval_check,
    quick_call_outcome,
    quick_dnc_mark,
    sync_offline_draft,
    today_actions,
)


router = APIRouter(prefix="/api/v1/mobile", tags=["mobile-operator"])


@router.get("")
def overview(session: Session = Depends(get_session)) -> dict[str, object]:
    return mobile_overview(session)


@router.get("/today")
def today(session: Session = Depends(get_session)) -> dict[str, object]:
    return today_actions(session)


@router.get("/calls")
def calls(session: Session = Depends(get_session)) -> dict[str, object]:
    return call_queue(session)


@router.get("/leads/{lead_id}")
def lead(lead_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return lead_detail(session, lead_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/deals/{deal_id}")
def deal(deal_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return deal_detail(session, deal_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/approvals")
def approvals(session: Session = Depends(get_session)) -> dict[str, object]:
    return approval_queue(session)


@router.get("/briefing")
def briefing(session: Session = Depends(get_session)) -> dict[str, object]:
    return field_briefing(session)


@router.get("/buyers")
def buyers(session: Session = Depends(get_session)) -> dict[str, object]:
    return buyers_snapshot(session)


@router.get("/documents")
def documents(session: Session = Depends(get_session)) -> dict[str, object]:
    return documents_snapshot(session)


@router.post("/notes")
def notes(request: MobileNoteCreate, session: Session = Depends(get_session)) -> dict[str, object]:
    return capture_mobile_note(session, request)


@router.post("/calls/outcomes")
def call_outcomes(
    request: MobileCallOutcomeCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return quick_call_outcome(session, request)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/dnc")
def dnc(request: MobileDncMark, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return quick_dnc_mark(session, request)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/offline-drafts")
def offline_drafts(
    request: MobileOfflineDraftCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return sync_offline_draft(session, request)


@router.post("/approvals/quick-check")
def quick_check(
    request: MobileApprovalGateCheck,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return quick_approval_check(session, request)
