from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.document_intelligence.schemas import DocumentAnalyzeRequest
from app.domains.document_intelligence.service import (
    analyze_document,
    document_dashboard,
    document_detail,
)


router = APIRouter(prefix="/api/v1/documents", tags=["document-intelligence"])


@router.get("")
def documents(session: Session = Depends(get_session)) -> dict[str, object]:
    return document_dashboard(session)


@router.get("/issues")
def document_issues(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = document_dashboard(session)
    return {"issues": dashboard["issues"], "legal_advice_provided": False}


@router.get("/review-queue")
def document_review_queue(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = document_dashboard(session)
    return {"review_tasks": dashboard["review_tasks"], "automatic_sending_allowed": False}


@router.get("/evidence")
def document_evidence(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = document_dashboard(session)
    return {"evidence_links": dashboard["linked_deal_evidence"], "portal_publish_allowed": False}


@router.get("/{document_id}")
def document_intelligence_detail(
    document_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return document_detail(session, document_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/analyze")
def document_analyze(
    payload: DocumentAnalyzeRequest,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return analyze_document(session, **payload.model_dump())
