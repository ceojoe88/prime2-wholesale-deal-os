from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import BuyerMatch, ComplianceRecord, Deal, Division, Lead


def build_command_center(session: Session) -> dict[str, object]:
    leads = session.query(Lead).all()
    deals = session.query(Deal).all()
    hot_deals = sorted(
        [deal for deal in deals if deal.is_hot_opportunity],
        key=lambda deal: deal.deal_speed_score,
        reverse=True,
    )
    matches = session.query(BuyerMatch).all()
    compliance = session.query(ComplianceRecord).all()
    divisions = session.query(Division).all()

    action_queue = [
        {
            "title": "Review hot 10K+ spreads",
            "priority": "critical",
            "count": len(hot_deals),
            "owner_approval_required": True,
        },
        {
            "title": "Underwrite missing repair assumptions",
            "priority": "high",
            "count": len([lead for lead in leads if lead.stage in {"researched", "offer_needed"}]),
            "owner_approval_required": False,
        },
        {
            "title": "Compliance review before assignment packet prep",
            "priority": "high",
            "count": len([record for record in compliance if record.status == "needs_review"]),
            "owner_approval_required": True,
        },
    ]

    return {
        "overseer": "Wholesale Prime",
        "daily_strategy": [
            "Prioritize under-contract deals with verified buyer demand.",
            "Protect buyer margin before recommending any seller offer.",
            "Escalate compliance-risk examples before assignment packet prep.",
        ],
        "active_leads": len(leads),
        "active_deals": len(deals),
        "hot_10k_opportunities": len(hot_deals),
        "under_contract": len([deal for deal in deals if deal.is_under_contract]),
        "projected_assignment_fees": sum(deal.projected_assignment_fee for deal in deals),
        "top_hot_deals": [
            {
                "id": deal.id,
                "lead_id": deal.lead_id,
                "projected_assignment_fee": deal.projected_assignment_fee,
                "deal_speed_score": deal.deal_speed_score,
                "risk_flags": deal.risk_flags,
                "next_best_action": "Owner review, then draft-only offer or disposition packet.",
            }
            for deal in hot_deals[:5]
        ],
        "buyer_ready_deals": len({match.deal_id for match in matches}),
        "compliance_alerts": [
            {
                "deal_id": record.deal_id,
                "title": record.title,
                "risk_warnings": record.risk_warnings,
            }
            for record in compliance
            if record.risk_warnings
        ],
        "manager_queues": [
            {
                "division": division.name,
                "manager": division.manager_name,
                "workload": division.workload,
                "priority_queue": division.priority_queue,
                "next_best_action": division.next_best_action,
            }
            for division in divisions
        ],
        "attention_queue": action_queue,
    }
