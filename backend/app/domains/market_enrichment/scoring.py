from __future__ import annotations

from datetime import UTC, datetime

from app.domain.scoring import clamp_score
from app.models import (
    BuyerActivitySnapshot,
    ComparableSaleRecord,
    LeadSourceROIRecord,
    MarketProfile,
)


def _year_from_date(value: str) -> int | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).year
    except ValueError:
        try:
            return datetime.strptime(value, "%Y-%m-%d").year
        except ValueError:
            return None


def comp_recency_score(comp: ComparableSaleRecord, *, current_year: int | None = None) -> float:
    current_year = current_year or datetime.now(UTC).year
    sale_year = _year_from_date(comp.sale_date)
    if sale_year is None:
        return 35
    age = max(0, current_year - sale_year)
    if age == 0:
        return 100
    if age == 1:
        return 82
    if age == 2:
        return 62
    return 38


def comp_distance_score(comp: ComparableSaleRecord) -> float:
    if comp.distance_miles <= 0.5:
        return 100
    if comp.distance_miles <= 1:
        return 88
    if comp.distance_miles <= 2:
        return 70
    if comp.distance_miles <= 3:
        return 54
    return 32


def comparable_quality_score(comp: ComparableSaleRecord) -> float:
    score = (
        comp_recency_score(comp) * 0.38
        + comp_distance_score(comp) * 0.34
        + clamp_score(comp.confidence_score) * 0.28
    )
    return clamp_score(score)


def comp_based_arv_confidence(
    comps: list[ComparableSaleRecord],
    *,
    market_confidence: float = 0,
) -> dict[str, object]:
    if not comps:
        return {
            "arv_confidence": 20,
            "pricing_confidence": 20,
            "comp_count": 0,
            "basis": ["missing_recent_comps"],
        }
    qualities = [comparable_quality_score(comp) for comp in comps]
    count_score = clamp_score(len(comps) * 26)
    avg_quality = sum(qualities) / len(qualities)
    confidence = clamp_score(count_score * 0.28 + avg_quality * 0.48 + market_confidence * 0.24)
    basis = [
        f"{len(comps)} manual/imported comp records",
        "comp distance, recency, and confidence weighted",
    ]
    if len(comps) < 3:
        basis.append("stale_or_missing_comps_lower_confidence")
    if any(comp_recency_score(comp) < 60 for comp in comps):
        basis.append("stale_comp_penalty_applied")
    return {
        "arv_confidence": confidence,
        "pricing_confidence": confidence,
        "comp_count": len(comps),
        "basis": basis,
    }


def buyer_activity_demand_confidence(snapshot: BuyerActivitySnapshot) -> float:
    buyer_depth = clamp_score(snapshot.active_buyer_count * 10)
    pof_ratio = (
        (snapshot.pof_verified_buyer_count / snapshot.active_buyer_count) * 100
        if snapshot.active_buyer_count
        else 0
    )
    fast_close_ratio = (
        (snapshot.fast_close_buyer_count / snapshot.active_buyer_count) * 100
        if snapshot.active_buyer_count
        else 0
    )
    score = (
        buyer_depth * 0.22
        + pof_ratio * 0.24
        + fast_close_ratio * 0.18
        + clamp_score(snapshot.buyer_response_velocity) * 0.20
        + clamp_score(snapshot.recent_interest_count * 16) * 0.16
    )
    return clamp_score(score)


def lead_source_quality_score(record: LeadSourceROIRecord) -> float:
    leads_imported = record.leads_imported or 0
    if not record.evidence_basis or leads_imported <= 0:
        return 0
    qa_passed = record.qa_passed or 0
    calls_made = record.calls_made or 0
    motivated_sellers = record.motivated_sellers or 0
    offers_requested = record.offers_requested or 0
    contract_ready_count = record.contract_ready_count or 0
    qa_rate = qa_passed / leads_imported * 100
    motivated_rate = motivated_sellers / max(calls_made, 1) * 100
    offer_rate = offers_requested / max(qa_passed, 1) * 100
    contract_rate = contract_ready_count / max(offers_requested, 1) * 100
    score = qa_rate * 0.26 + motivated_rate * 0.24 + offer_rate * 0.22 + contract_rate * 0.28
    return clamp_score(score)


def lead_source_roi_gate(record: LeadSourceROIRecord) -> dict[str, object]:
    blocked_reasons: list[str] = []
    if not record.evidence_basis:
        blocked_reasons.append("source_evidence_required")
    if (record.leads_imported or 0) <= 0:
        blocked_reasons.append("leads_imported_required")
    if (record.cost_placeholder or 0) <= 0:
        blocked_reasons.append("cost_placeholder_missing_estimate_only")
    if record.guaranteed_roi_allowed:
        blocked_reasons.append("guaranteed_roi_language_blocked")
    record.roi_confidence = lead_source_quality_score(record)
    record.estimate_only = True
    record.guaranteed_roi_allowed = False
    return {
        "allowed_for_strategy": not blocked_reasons,
        "blocked_reasons": sorted(set(blocked_reasons)),
        "estimate_only": True,
        "guaranteed_roi_allowed": False,
        "roi_confidence": record.roi_confidence,
    }


def market_heat_score(
    profile: MarketProfile,
    *,
    lead_quality: float = 0,
    spread_potential: float = 0,
) -> float:
    score = (
        clamp_score(profile.buyer_demand_score) * 0.25
        + clamp_score(profile.investor_activity_score) * 0.18
        + clamp_score(profile.rental_demand_score) * 0.10
        + clamp_score(lead_quality) * 0.18
        + clamp_score(spread_potential) * 0.16
        + (100 - clamp_score(profile.competition_score)) * 0.06
        + (100 - clamp_score(profile.title_friction_score)) * 0.07
    )
    return clamp_score(score)


def sync_market_profile(
    profile: MarketProfile,
    *,
    comps: list[ComparableSaleRecord],
    buyer_snapshot: BuyerActivitySnapshot | None,
    lead_source_records: list[LeadSourceROIRecord],
    average_spread: float = 0,
) -> dict[str, object]:
    lead_quality = (
        sum(lead_source_quality_score(record) for record in lead_source_records) / len(lead_source_records)
        if lead_source_records
        else 0
    )
    if buyer_snapshot is not None:
        buyer_snapshot.demand_confidence = buyer_activity_demand_confidence(buyer_snapshot)
        profile.buyer_demand_score = max(profile.buyer_demand_score, buyer_snapshot.demand_confidence)
    spread_potential = clamp_score(average_spread / 300)
    profile.market_heat_score = market_heat_score(
        profile,
        lead_quality=lead_quality,
        spread_potential=spread_potential,
    )
    arv = comp_based_arv_confidence(comps, market_confidence=profile.confidence_score)
    evidence_count = len(profile.evidence_basis) + len(comps) + len(lead_source_records)
    profile.confidence_score = clamp_score(
        profile.confidence_score * 0.35
        + float(arv["arv_confidence"]) * 0.35
        + (buyer_snapshot.demand_confidence if buyer_snapshot else 25) * 0.20
        + clamp_score(evidence_count * 12) * 0.10
    )
    if not comps:
        profile.confidence_score = min(profile.confidence_score, 45)
    return {
        "market_heat_score": profile.market_heat_score,
        "confidence_score": profile.confidence_score,
        "arv_confidence": arv,
        "lead_source_quality": lead_quality,
        "spread_potential": spread_potential,
        "estimate_only": True,
    }
