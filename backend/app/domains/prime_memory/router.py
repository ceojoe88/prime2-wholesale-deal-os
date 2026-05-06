from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.prime_memory.service import memory_detail, prime_memory_dashboard


router = APIRouter(prefix="/api/v1/prime-memory", tags=["prime-memory"])


@router.get("")
def memory_dashboard(session: Session = Depends(get_session)) -> dict[str, object]:
    return prime_memory_dashboard(session)


@router.get("/patterns")
def memory_patterns(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = prime_memory_dashboard(session)
    return {
        "pattern_summary": dashboard["pattern_summary"],
        "top_learning_insights": dashboard["top_learning_insights"],
        "deterministic_explainable_learning": True,
    }


@router.get("/learning-signals")
def learning_signals(session: Session = Depends(get_session)) -> dict[str, object]:
    return {"learning_signals": prime_memory_dashboard(session)["learning_signals"]}


@router.get("/scoring-weight-recommendations")
def scoring_weight_recommendations(session: Session = Depends(get_session)) -> dict[str, object]:
    return {
        "scoring_weight_recommendations": prime_memory_dashboard(session)["scoring_weight_recommendations"],
        "auto_apply_allowed": False,
    }


@router.get("/playbook-recommendations")
def playbook_recommendations(session: Session = Depends(get_session)) -> dict[str, object]:
    return {
        "playbook_recommendations": prime_memory_dashboard(session)["playbook_recommendations"],
        "draft_only": True,
    }


@router.get("/{memory_id}")
def memory_record(memory_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return memory_detail(session, memory_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
