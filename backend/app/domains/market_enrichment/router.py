from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.market_enrichment.service import market_dashboard, market_detail


router = APIRouter(prefix="/api/v1/market-enrichment", tags=["market-enrichment"])


@router.get("")
def markets(session: Session = Depends(get_session)) -> dict[str, object]:
    return market_dashboard(session)


@router.get("/comps")
def comps(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = market_dashboard(session)
    return {
        "comparable_sales": dashboard["comparable_sales"],
        "arv_confidence_by_market": dashboard["arv_confidence_by_market"],
        "no_fake_comps": True,
    }


@router.get("/rent-estimates")
def rent_estimates(session: Session = Depends(get_session)) -> dict[str, object]:
    return {"rent_estimates": market_dashboard(session)["rent_estimates"], "estimate_only": True}


@router.get("/buyer-activity")
def buyer_activity(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = market_dashboard(session)
    return {
        "buyer_activity_snapshots": dashboard["buyer_activity_snapshots"],
        "buyer_demand_uses_activity_snapshots": True,
    }


@router.get("/lead-source-roi")
def lead_source_roi(session: Session = Depends(get_session)) -> dict[str, object]:
    return {
        "lead_source_roi_records": market_dashboard(session)["lead_source_roi_records"],
        "estimate_only": True,
        "guaranteed_roi_allowed": False,
    }


@router.get("/ranking")
def market_ranking(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = market_dashboard(session)
    return {
        "market_ranking": dashboard["market_ranking"],
        "weak_market_warnings": dashboard["weak_market_warnings"],
    }


@router.get("/{market_id}")
def market_record(market_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return market_detail(session, market_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
