from __future__ import annotations

from collections import defaultdict

from sqlalchemy.orm import Session

from app.domains.market_enrichment.sanitizer import sanitize_market_record
from app.domains.market_enrichment.scoring import (
    comp_based_arv_confidence,
    lead_source_roi_gate,
    sync_market_profile,
)
from app.models import (
    BuyerActivitySnapshot,
    ComparableSaleRecord,
    Deal,
    LeadSourceROIRecord,
    MarketProfile,
    RentEstimateRecord,
)


def _market_comps(session: Session, market_id: str) -> list[ComparableSaleRecord]:
    return session.query(ComparableSaleRecord).filter_by(market_id=market_id).all()


def _market_snapshot(session: Session, market_id: str) -> BuyerActivitySnapshot | None:
    return session.query(BuyerActivitySnapshot).filter_by(market_id=market_id).first()


def _market_roi_records(session: Session, market_id: str) -> list[LeadSourceROIRecord]:
    return session.query(LeadSourceROIRecord).filter_by(market_id=market_id).all()


def _average_market_spread(session: Session, zip_code: str) -> float:
    deals = (
        session.query(Deal)
        .join(Deal.lead)
        .filter_by(zip_code=zip_code)
        .all()
    )
    if not deals:
        return 0
    return sum(max(deal.projected_assignment_fee, 0) for deal in deals) / len(deals)


def sync_all_markets(session: Session) -> dict[str, dict[str, object]]:
    snapshots: dict[str, dict[str, object]] = {}
    for profile in session.query(MarketProfile).all():
        snapshots[profile.market_id] = sync_market_profile(
            profile,
            comps=_market_comps(session, profile.market_id),
            buyer_snapshot=_market_snapshot(session, profile.market_id),
            lead_source_records=_market_roi_records(session, profile.market_id),
            average_spread=_average_market_spread(session, profile.zip_code),
        )
    for record in session.query(LeadSourceROIRecord).all():
        lead_source_roi_gate(record)
    session.flush()
    return snapshots


def market_dashboard(session: Session) -> dict[str, object]:
    sync = sync_all_markets(session)
    profiles = session.query(MarketProfile).all()
    comps = session.query(ComparableSaleRecord).all()
    rents = session.query(RentEstimateRecord).all()
    snapshots = session.query(BuyerActivitySnapshot).all()
    roi_records = session.query(LeadSourceROIRecord).all()
    comps_by_market: dict[str, list[ComparableSaleRecord]] = defaultdict(list)
    for comp in comps:
        comps_by_market[comp.market_id].append(comp)
    ranked = sorted(profiles, key=lambda item: item.market_heat_score, reverse=True)
    weak = [
        profile
        for profile in profiles
        if profile.confidence_score < 55 or profile.market_heat_score < 55
    ]
    return {
        "market_profiles": [sanitize_market_record(profile) for profile in profiles],
        "market_ranking": [sanitize_market_record(profile) for profile in ranked],
        "comparable_sales": [sanitize_market_record(comp) for comp in comps],
        "rent_estimates": [sanitize_market_record(rent) for rent in rents],
        "buyer_activity_snapshots": [sanitize_market_record(snapshot) for snapshot in snapshots],
        "lead_source_roi_records": [
            {**sanitize_market_record(record), "gate": lead_source_roi_gate(record)}
            for record in roi_records
        ],
        "arv_confidence_by_market": {
            market_id: comp_based_arv_confidence(comps_for_market, market_confidence=session.get(MarketProfile, market_id).confidence_score)
            for market_id, comps_for_market in comps_by_market.items()
        },
        "top_markets": [sanitize_market_record(profile) for profile in ranked[:5]],
        "weak_market_warnings": [sanitize_market_record(profile) for profile in weak],
        "integration_signals": {
            "underwriting_arv_confidence": True,
            "buyer_demand_uses_activity_snapshots": True,
            "revenue_forecast_references_market_confidence": True,
            "field_testing_updates_lead_source_roi": True,
            "campaign_brain_uses_market_ranking": True,
            "operator_mode_shows_market_warnings": True,
        },
        "manual_or_imported_data_only": True,
        "paid_external_api_calls": False,
        "guaranteed_roi_allowed": False,
        "guaranteed_profit_allowed": False,
        "sync": sync,
    }


def market_detail(session: Session, market_id: str) -> dict[str, object]:
    profile = session.get(MarketProfile, market_id)
    if profile is None:
        raise ValueError(f"Market not found: {market_id}")
    sync = sync_market_profile(
        profile,
        comps=_market_comps(session, market_id),
        buyer_snapshot=_market_snapshot(session, market_id),
        lead_source_records=_market_roi_records(session, market_id),
        average_spread=_average_market_spread(session, profile.zip_code),
    )
    session.flush()
    return {
        "market": sanitize_market_record(profile),
        "comparable_sales": [
            sanitize_market_record(comp) for comp in _market_comps(session, market_id)
        ],
        "rent_estimates": [
            sanitize_market_record(rent)
            for rent in session.query(RentEstimateRecord).filter_by(market_id=market_id).all()
        ],
        "buyer_activity_snapshot": (
            sanitize_market_record(_market_snapshot(session, market_id))
            if _market_snapshot(session, market_id)
            else None
        ),
        "lead_source_roi_records": [
            {**sanitize_market_record(record), "gate": lead_source_roi_gate(record)}
            for record in _market_roi_records(session, market_id)
        ],
        "confidence": sync,
        "estimate_only": True,
        "no_fake_comps": True,
    }

