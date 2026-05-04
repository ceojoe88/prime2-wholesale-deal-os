from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.domain.buyer_portal import portal_publish_gate
from app.models import (
    Buyer,
    BuyerDealPriority,
    BuyerDemandProfile,
    Deal,
    DealDistributionPrep,
)
from app.serializers import model_to_dict


SAFE_DEAL_SHEET_FIELDS = {
    "property_summary",
    "asking_price",
    "arv_range",
    "repair_estimate_range",
    "buyer_margin_estimate",
    "access_instructions_placeholder",
    "availability_status",
    "proof_inspection_notes_placeholder",
}

FORBIDDEN_DEAL_SHEET_KEYS = {
    "seller_name",
    "seller_contact",
    "seller_phone",
    "seller_email",
    "seller_contract_price",
    "assignment_fee",
    "projected_assignment_fee",
    "target_assignment_fee",
    "internal_spread_logic",
    "spread_strategy",
    "lead_source",
    "source_category",
    "motivation_score",
    "seller_temperature",
    "negotiation_notes",
    "internal_notes",
    "agent_recommendations",
    "manager_queues",
    "compliance_internals",
    "compliance_risk_details",
}

DISTRIBUTION_LANGUAGE_PATTERNS = {
    "buyer blast": "live_buyer_blast",
    "blast this deal": "live_buyer_blast",
    "bulk send": "bulk_send",
    "send to all buyers": "bulk_send",
    "campaign": "bulk_send",
    "last chance": "misleading_scarcity",
    "act now or lose": "misleading_scarcity",
    "only buyer getting this": "misleading_scarcity",
    "we already have offers": "fake_buyer_competition",
    "competing offers": "fake_buyer_competition",
    "multiple buyers are lined up": "fake_buyer_competition",
    "fake offer": "fake_offer",
    "seller phone": "seller_private_data_exposure",
    "seller email": "seller_private_data_exposure",
    "seller name": "seller_private_data_exposure",
    "lead source": "seller_private_data_exposure",
    "motivation score": "seller_private_data_exposure",
    "internal spread": "internal_profit_logic_exposure",
    "assignment fee": "assignment_fee_exposure",
    "guaranteed close": "legal_closing_guarantee",
    "guaranteed closing": "legal_closing_guarantee",
    "will close": "legal_closing_guarantee",
    "legal advice": "legal_advice",
}


def _pof_score(status: str) -> float:
    return {"verified": 100, "needs_refresh": 58, "unverified": 25}.get(status, 35)


def _closing_speed_score(days: int) -> float:
    if days <= 7:
        return 100
    if days <= 10:
        return 95
    if days <= 14:
        return 84
    if days <= 21:
        return 66
    return 48


def _buyer_margin_strength(deal: Deal) -> float:
    asking_price = deal.buyer_publication.asking_price if deal.buyer_publication else None
    buyer_margin = (
        deal.arv - deal.repairs - deal.buyer_costs - asking_price
        if asking_price is not None
        else deal.arv - deal.repairs - deal.buyer_costs - deal.buyer_purchase_price
    )
    if buyer_margin >= 50_000:
        return 100
    if buyer_margin >= 35_000:
        return 86
    if buyer_margin >= 25_000:
        return 70
    return 35


def score_buyer_for_deal(
    deal: Deal,
    buyer: Buyer,
    profile: BuyerDemandProfile | None = None,
) -> dict[str, object]:
    lead = deal.lead
    publication = deal.buyer_publication
    asking_price = publication.asking_price if publication and publication.asking_price else deal.buyer_purchase_price
    target_zips = profile.target_zip_codes if profile and profile.target_zip_codes else buyer.target_zip_codes
    buyer_type = profile.property_type if profile else buyer.property_type
    area_match = 100 if lead.zip_code in target_zips else 35
    max_price_fit = 100 if asking_price <= buyer.max_purchase_price else max(15, 100 - ((asking_price - buyer.max_purchase_price) / 1000))
    pof_score = _pof_score(buyer.proof_of_funds_status)
    reliability = profile.reliability_score if profile else buyer.reliability_score
    closing = profile.closing_speed_score if profile and profile.closing_speed_score else _closing_speed_score(buyer.closing_speed_days)
    deal_type_fit = 100 if buyer_type in {lead.property_type, "any"} else 45
    margin_strength = _buyer_margin_strength(deal)
    score = round(
        area_match * 0.22
        + max_price_fit * 0.18
        + pof_score * 0.16
        + reliability * 0.16
        + closing * 0.12
        + deal_type_fit * 0.08
        + margin_strength * 0.08,
        2,
    )
    reasons: list[str] = []
    risks: list[str] = []
    if area_match == 100:
        reasons.append("target_area_match")
    else:
        risks.append("target_area_mismatch")
    if max_price_fit >= 90:
        reasons.append("max_price_fit")
    else:
        risks.append("max_price_gap")
    if pof_score == 100:
        reasons.append("proof_of_funds_verified")
    else:
        risks.append("proof_of_funds_gap")
    if reliability >= 85:
        reasons.append("reliable_past_performance")
    if closing >= 90:
        reasons.append("fast_close")
    if deal_type_fit == 100:
        reasons.append("deal_type_fit")
    else:
        risks.append("property_type_fit_review")
    if margin_strength >= 86:
        reasons.append("buyer_margin_strong")
    else:
        risks.append("buyer_margin_review")
    return {
        "target_area_match": area_match,
        "max_price_fit": round(max_price_fit, 2),
        "proof_of_funds_score": pof_score,
        "past_reliability_score": reliability,
        "closing_speed_score": closing,
        "deal_type_fit": deal_type_fit,
        "buyer_margin_strength": margin_strength,
        "priority_score": score,
        "ranking_reasons": reasons,
        "risk_flags": risks,
    }


def sync_buyer_deal_priority(priority: BuyerDealPriority) -> None:
    profile = priority.demand_profile or priority.buyer.demand_profile
    result = score_buyer_for_deal(priority.deal, priority.buyer, profile)
    for key, value in result.items():
        setattr(priority, key, value)
    priority.buyer_demand_profile_id = profile.id if profile else None
    priority.recommended_next_step = (
        "Prepare one-buyer distribution draft for owner review; no live send or buyer blast."
        if priority.priority_score >= 85 and not priority.risk_flags
        else "Review POF, price fit, or margin before preparing any buyer communication draft."
    )
    priority.draft_only = True
    priority.live_contact_allowed = False
    priority.buyer_blast_allowed = False
    priority.internal_profit_logic_exposed = False


def sync_priority_rankings(session: Session) -> None:
    priorities = session.query(BuyerDealPriority).all()
    for priority in priorities:
        sync_buyer_deal_priority(priority)
    by_deal: dict[str, list[BuyerDealPriority]] = defaultdict(list)
    for priority in priorities:
        by_deal[priority.deal_id].append(priority)
    for deal_priorities in by_deal.values():
        for rank, priority in enumerate(
            sorted(deal_priorities, key=lambda item: item.priority_score, reverse=True),
            start=1,
        ):
            priority.rank = rank


def validate_distribution_language(
    content: str,
    *,
    assignment_fee_exposure_approved: bool = False,
) -> dict[str, object]:
    lowered = content.lower()
    flags = sorted(
        {
            flag
            for pattern, flag in DISTRIBUTION_LANGUAGE_PATTERNS.items()
            if pattern in lowered
        }
    )
    if assignment_fee_exposure_approved:
        flags = [flag for flag in flags if flag != "assignment_fee_exposure"]
    return {
        "allowed": not flags,
        "blocked": bool(flags),
        "risk_flags": flags,
        "live_buyer_blast_blocked": "live_buyer_blast" in flags,
        "bulk_send_blocked": "bulk_send" in flags,
        "misleading_scarcity_blocked": "misleading_scarcity" in flags,
        "fake_competition_blocked": "fake_buyer_competition" in flags,
        "seller_private_data_blocked": "seller_private_data_exposure" in flags,
        "assignment_fee_exposure_blocked": "assignment_fee_exposure" in flags,
        "legal_closing_guarantee_blocked": "legal_closing_guarantee" in flags,
    }


def sanitize_buyer_deal_sheet(prep: DealDistributionPrep) -> dict[str, object]:
    publication = prep.buyer_deal_publication or prep.deal.buyer_publication
    deal = prep.deal
    if publication is None:
        sheet = {
            "property_summary": {
                "city": deal.lead.city,
                "state": deal.lead.state,
                "zip_code": deal.lead.zip_code,
                "property_type": deal.lead.property_type,
            },
            "asking_price": None,
            "arv_range": {"low": None, "high": None},
            "repair_estimate_range": {"low": None, "high": None},
            "buyer_margin_estimate": None,
            "access_instructions_placeholder": "Access instructions placeholder pending publication record.",
            "availability_status": "draft",
            "proof_inspection_notes_placeholder": "Proof of funds and inspection notes placeholder.",
        }
    else:
        sheet = {
            "property_summary": {
                "city": deal.lead.city,
                "state": deal.lead.state,
                "zip_code": deal.lead.zip_code,
                "property_type": deal.lead.property_type,
                "beds": publication.beds,
                "baths": publication.baths,
                "sqft": publication.sqft,
            },
            "asking_price": publication.asking_price,
            "arv_range": {"low": publication.arv_low, "high": publication.arv_high},
            "repair_estimate_range": {
                "low": publication.repair_low,
                "high": publication.repair_high,
            },
            "buyer_margin_estimate": publication.estimated_buyer_margin,
            "access_instructions_placeholder": publication.access_instructions_placeholder,
            "availability_status": publication.availability_status,
            "proof_inspection_notes_placeholder": "POF verification and inspection/access notes placeholder only.",
        }
    assert_no_deal_sheet_leaks(sheet)
    return sheet


def assert_no_deal_sheet_leaks(sheet: dict[str, object]) -> None:
    if not set(sheet.keys()).issubset(SAFE_DEAL_SHEET_FIELDS):
        extras = sorted(set(sheet.keys()) - SAFE_DEAL_SHEET_FIELDS)
        raise ValueError(f"Deal sheet emitted unexpected fields: {extras}")
    leaked = FORBIDDEN_DEAL_SHEET_KEYS.intersection(sheet.keys())
    serialized = str(sheet).lower()
    leaked |= {key for key in FORBIDDEN_DEAL_SHEET_KEYS if key in serialized}
    if leaked:
        raise ValueError(f"Deal sheet leaked forbidden data: {sorted(leaked)}")


def distribution_prep_gate(prep: DealDistributionPrep) -> dict[str, object]:
    reasons: list[str] = []
    content = " ".join(
        [
            prep.buyer_deal_email_draft,
            prep.buyer_sms_draft,
            prep.buyer_call_notes,
            str(prep.private_deal_sheet_draft),
        ]
    )
    safety = validate_distribution_language(
        content,
        assignment_fee_exposure_approved=prep.assignment_fee_exposed,
    )
    reasons.extend(safety["risk_flags"])
    if prep.live_send_allowed:
        reasons.append("live_send_enabled")
    if prep.bulk_blast_allowed:
        reasons.append("bulk_blast_enabled")
    if prep.seller_private_data_exposed:
        reasons.append("seller_private_data_exposed")
    if prep.assignment_fee_exposed:
        reasons.append("assignment_fee_exposed_without_v9_approval")
    if prep.legal_closing_guarantee_allowed:
        reasons.append("legal_closing_guarantee_enabled")
    publication = prep.buyer_deal_publication or prep.deal.buyer_publication
    if publication:
        portal_gate = portal_publish_gate(prep.deal, publication)
        if not portal_gate["can_publish"]:
            reasons.extend(f"buyer_publication_{reason}" for reason in portal_gate["blocked_reasons"])
    else:
        reasons.append("missing_buyer_publication")
    return {
        "can_prepare_distribution": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "safety_result": safety,
        "live_buyer_blast_allowed": False,
        "bulk_send_allowed": False,
        "contract_execution_allowed": False,
        "legal_closing_guarantee_allowed": False,
    }


def sync_distribution_prep(prep: DealDistributionPrep) -> dict[str, object]:
    prep.private_deal_sheet_draft = sanitize_buyer_deal_sheet(prep)
    gate = distribution_prep_gate(prep)
    prep.blocked_reasons = gate["blocked_reasons"]
    prep.safety_status = "passed" if not gate["safety_result"]["risk_flags"] else "blocked"
    prep.draft_status = "draft_ready" if gate["can_prepare_distribution"] else "blocked"
    prep.draft_only = True
    prep.live_send_allowed = False
    prep.bulk_blast_allowed = False
    prep.seller_private_data_exposed = False
    prep.assignment_fee_exposed = False
    prep.legal_closing_guarantee_allowed = False
    return gate


def buyer_deal_priority_summary(priority: BuyerDealPriority) -> dict[str, object]:
    return {
        **model_to_dict(priority),
        "buyer": {
            "id": priority.buyer.id,
            "name": priority.buyer.name,
            "company": priority.buyer.company,
            "proof_of_funds_status": priority.buyer.proof_of_funds_status,
            "closing_speed_days": priority.buyer.closing_speed_days,
        },
        "deal": {
            "id": priority.deal.id,
            "city": priority.deal.lead.city,
            "state": priority.deal.lead.state,
            "zip_code": priority.deal.lead.zip_code,
            "property_type": priority.deal.lead.property_type,
            "asking_price": priority.deal.buyer_publication.asking_price
            if priority.deal.buyer_publication
            else priority.deal.buyer_purchase_price,
        },
        "draft_only": True,
        "live_contact_allowed": False,
        "buyer_blast_allowed": False,
    }


def distribution_prep_summary(prep: DealDistributionPrep) -> dict[str, object]:
    gate = sync_distribution_prep(prep)
    return {
        **model_to_dict(prep),
        "sanitized_deal_sheet": sanitize_buyer_deal_sheet(prep),
        "distribution_gate": gate,
        "draft_only": True,
        "live_send_allowed": False,
        "bulk_blast_allowed": False,
        "buyer_blast_allowed": False,
        "seller_private_data_exposed": False,
        "contract_execution_allowed": False,
    }


def _highest_demand_zips(profiles: list[BuyerDemandProfile]) -> list[dict[str, object]]:
    zip_scores: dict[str, list[float]] = defaultdict(list)
    for profile in profiles:
        for zip_code in profile.target_zip_codes:
            zip_scores[zip_code].append(profile.zip_code_demand_score)
    ranked = [
        {
            "zip_code": zip_code,
            "demand_score": round(sum(scores) / len(scores), 2),
            "buyer_count": len(scores),
        }
        for zip_code, scores in zip_scores.items()
    ]
    return sorted(ranked, key=lambda item: (item["demand_score"], item["buyer_count"]), reverse=True)


def buyer_demand_dashboard(session: Session) -> dict[str, object]:
    sync_priority_rankings(session)
    profiles = session.query(BuyerDemandProfile).all()
    priorities = session.query(BuyerDealPriority).all()
    preps = session.query(DealDistributionPrep).all()
    for prep in preps:
        sync_distribution_prep(prep)

    by_deal: dict[str, list[BuyerDealPriority]] = defaultdict(list)
    for priority in priorities:
        by_deal[priority.deal_id].append(priority)

    best_buyers = []
    buyer_ready_deals = []
    strong_10k = []
    for deal in session.query(Deal).all():
        ranked = sorted(by_deal.get(deal.id, []), key=lambda item: item.priority_score, reverse=True)
        top = ranked[0] if ranked else None
        if top:
            best_buyers.append(
                {
                    "deal_id": deal.id,
                    "buyer_id": top.buyer_id,
                    "buyer_name": top.buyer.name,
                    "priority_score": top.priority_score,
                    "rank": top.rank,
                    "risk_flags": top.risk_flags,
                }
            )
        publication_gate = (
            portal_publish_gate(deal, deal.buyer_publication)
            if deal.buyer_publication
            else {"can_publish": False}
        )
        if top and publication_gate["can_publish"] and top.priority_score >= 85:
            buyer_ready_deals.append(
                {
                    "deal_id": deal.id,
                    "top_buyer_id": top.buyer_id,
                    "priority_score": top.priority_score,
                    "proof_of_funds_status": top.buyer.proof_of_funds_status,
                }
            )
        if top and deal.projected_assignment_fee >= deal.target_assignment_fee and top.priority_score >= 85:
            strong_10k.append(
                {
                    "deal_id": deal.id,
                    "projected_assignment_fee": deal.projected_assignment_fee,
                    "top_buyer_id": top.buyer_id,
                    "buyer_demand_score": top.priority_score,
                }
            )

    pof_gaps = [
        buyer_deal_priority_summary(priority)
        for priority in priorities
        if priority.buyer.proof_of_funds_status != "verified"
    ]
    fast_close_buyers = [
        {
            **model_to_dict(profile),
            "buyer": {
                "id": profile.buyer.id,
                "name": profile.buyer.name,
                "company": profile.buyer.company,
                "closing_speed_days": profile.buyer.closing_speed_days,
                "proof_of_funds_status": profile.buyer.proof_of_funds_status,
            },
        }
        for profile in profiles
        if profile.buyer.closing_speed_days <= 10 and profile.buyer.proof_of_funds_status == "verified"
    ]

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "buyer_demand_profiles": [model_to_dict(profile) for profile in profiles],
        "buyer_priority_rankings": [
            buyer_deal_priority_summary(priority)
            for priority in sorted(priorities, key=lambda item: (item.deal_id, item.rank))
        ],
        "distribution_preps": [distribution_prep_summary(prep) for prep in preps],
        "highest_demand_zip_codes": _highest_demand_zips(profiles),
        "best_buyers_for_hot_deals": [
            item
            for item in best_buyers
            if session.get(Deal, item["deal_id"]).is_hot_opportunity
        ],
        "buyer_ready_deals": buyer_ready_deals,
        "distribution_drafts_pending_approval": [
            distribution_prep_summary(prep)
            for prep in preps
            if prep.approval_status != "owner_approved"
        ],
        "proof_of_funds_gaps": pof_gaps,
        "fast_close_buyer_list": sorted(
            fast_close_buyers,
            key=lambda item: (
                item["buyer"]["closing_speed_days"],
                -float(item["reliability_score"]),
            ),
        ),
        "ten_k_deals_with_strong_buyer_demand": strong_10k,
        "live_buyer_blast_allowed": False,
        "bulk_send_allowed": False,
        "payment_collection_allowed": False,
        "contract_execution_allowed": False,
    }
