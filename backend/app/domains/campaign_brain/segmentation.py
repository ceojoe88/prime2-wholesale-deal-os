from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import Buyer, BuyerDealPriority, Deal, FieldCallOutcome, Lead


SELLER_SEGMENTS = {
    "hot_motivation",
    "follow_up_due",
    "stale_but_qualified",
    "offer_requested",
    "appointment_set",
    "contract_ready",
}

BUYER_SEGMENTS = {
    "area_match",
    "POF_verified",
    "fast_close_buyer",
    "recent_interest",
    "price_band_match",
    "deal_type_match",
    "reliability_high",
}


def _lead_is_dnc(session: Session, lead_id: str) -> bool:
    return (
        session.query(FieldCallOutcome)
        .filter(FieldCallOutcome.lead_id == lead_id, FieldCallOutcome.do_not_contact.is_(True))
        .count()
        > 0
    )


def seller_audience_preview(session: Session, segment_name: str, limit: int = 25) -> list[dict[str, object]]:
    leads = session.query(Lead).order_by(Lead.opportunity_score.desc()).limit(limit).all()
    preview: list[dict[str, object]] = []
    for lead in leads:
        excluded = False
        reasons: list[str] = []
        if _lead_is_dnc(session, lead.id):
            excluded = True
            reasons.append("do_not_contact_excluded")
        if lead.compliance_risk >= 75:
            excluded = True
            reasons.append("high_risk_compliance_excluded")
        if segment_name == "hot_motivation" and lead.motivation_score < 70:
            excluded = True
            reasons.append("motivation_below_segment_threshold")
        if segment_name == "offer_requested" and lead.stage not in {"offer_needed", "offer_sent", "negotiating"}:
            excluded = True
            reasons.append("offer_stage_not_matched")
        preview.append(
            {
                "recipient_id": lead.id,
                "recipient_type": "seller",
                "segment_name": segment_name,
                "excluded": excluded,
                "inclusion_status": "excluded" if excluded else "included",
                "exclusion_reasons": reasons,
                "score": round((lead.motivation_score + lead.opportunity_score + lead.contactability_score) / 3, 2),
                "do_not_contact": _lead_is_dnc(session, lead.id),
                "compliance_risk_status": "high" if lead.compliance_risk >= 75 else "clear",
                "consent_status": "unknown",
            }
        )
    return preview


def buyer_audience_preview(
    session: Session,
    segment_name: str,
    *,
    deal_id: str | None = None,
    limit: int = 25,
) -> list[dict[str, object]]:
    buyers = session.query(Buyer).order_by(Buyer.reliability_score.desc()).limit(limit).all()
    deal = session.get(Deal, deal_id) if deal_id else None
    preview: list[dict[str, object]] = []
    for buyer in buyers:
        excluded = False
        reasons: list[str] = []
        score = buyer.reliability_score
        if not buyer.active:
            excluded = True
            reasons.append("inactive_buyer_excluded")
        if segment_name == "POF_verified" and buyer.proof_of_funds_status != "verified":
            excluded = True
            reasons.append("pof_not_verified")
        if segment_name == "fast_close_buyer" and buyer.closing_speed_days > 14:
            excluded = True
            reasons.append("closing_speed_too_slow")
        if deal is not None:
            priority = (
                session.query(BuyerDealPriority)
                .filter(BuyerDealPriority.deal_id == deal.id, BuyerDealPriority.buyer_id == buyer.id)
                .first()
            )
            if priority:
                score = priority.priority_score
                if priority.buyer_margin_strength < 60:
                    excluded = True
                    reasons.append("weak_margin_deal_excluded")
                if priority.proof_of_funds_score < 60 and segment_name != "POF_verified":
                    reasons.append("pof_gap")
            if deal.risk_score >= 75:
                excluded = True
                reasons.append("high_risk_deal_excluded")
            if deal.projected_assignment_fee < 10_000:
                excluded = True
                reasons.append("below_10k_target_excluded")
        preview.append(
            {
                "recipient_id": buyer.id,
                "recipient_type": "buyer",
                "segment_name": segment_name,
                "excluded": excluded,
                "inclusion_status": "excluded" if excluded else "included",
                "exclusion_reasons": reasons,
                "score": round(score, 2),
                "do_not_contact": False,
                "compliance_risk_status": "clear" if not excluded else "review",
                "consent_status": "unknown",
            }
        )
    return preview

