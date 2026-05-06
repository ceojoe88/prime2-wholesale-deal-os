from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.real_deal_execution.schemas import (
    RealDealExecutionBatchCreate,
    RealDealExecutionBatchStatusUpdate,
)
from app.domains.real_deal_execution.service import (
    buyer_validation_board,
    cockpit_dashboard,
    contract_ready_board,
    create_execution_batch,
    evidence_tracker,
    field_test_report,
    offer_decision_board,
    seller_call_workflow,
    update_batch_status,
)


router = APIRouter(prefix="/api/v1/real-deal-execution", tags=["real-deal-execution"])


@router.get("")
def cockpit(session: Session = Depends(get_session)) -> dict[str, object]:
    return cockpit_dashboard(session)


@router.post("/batches")
def create_batch(
    request: RealDealExecutionBatchCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return create_execution_batch(session, request)


@router.post("/batches/{batch_id}/status")
def update_status(
    batch_id: str,
    request: RealDealExecutionBatchStatusUpdate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return update_batch_status(session, batch_id, request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/calls")
def calls(session: Session = Depends(get_session)) -> dict[str, object]:
    return seller_call_workflow(session)


@router.get("/offers")
def offers(session: Session = Depends(get_session)) -> dict[str, object]:
    return offer_decision_board(session)


@router.get("/buyer-validation")
def buyer_validation(session: Session = Depends(get_session)) -> dict[str, object]:
    return buyer_validation_board(session)


@router.get("/contract-ready")
def contract_ready(session: Session = Depends(get_session)) -> dict[str, object]:
    return contract_ready_board(session)


@router.get("/evidence")
def evidence(session: Session = Depends(get_session)) -> dict[str, object]:
    return evidence_tracker(session)


@router.get("/report")
def report(session: Session = Depends(get_session)) -> dict[str, object]:
    return field_test_report(session)
