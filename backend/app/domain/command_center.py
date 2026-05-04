from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.buyer_portal import portal_publish_gate, update_publication_gate
from app.domain.buyer_demand import buyer_demand_dashboard
from app.domain.closing_coordination import closing_coordination_dashboard
from app.domain.communications import communication_dashboard
from app.domain.contract_control import contract_title_dashboard
from app.domain.deal_evidence import evidence_dashboard
from app.domain.seller_acquisition import seller_pipeline_command_center
from app.domain.seller_portal import seller_portal_dashboard
from app.models import (
    BuyerDealPublication,
    BuyerInterest,
    BuyerMatch,
    ComplianceRecord,
    Deal,
    Division,
    Lead,
)


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
    publications = session.query(BuyerDealPublication).all()
    interests = session.query(BuyerInterest).all()
    buyer_visible_deals = []
    blocked_buyer_deals = []
    for publication in publications:
        update_publication_gate(publication, publication.deal)
        gate = portal_publish_gate(publication.deal, publication)
        if gate["can_publish"]:
            buyer_visible_deals.append(publication.deal_id)
        else:
            blocked_buyer_deals.append(
                {"deal_id": publication.deal_id, "blocked_reasons": gate["blocked_reasons"]}
            )

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
        "buyer_portal": {
            "buyer_visible_deals": buyer_visible_deals,
            "buyer_interest_queue": len(interests),
            "proof_of_funds_needed": len(
                [interest for interest in interests if interest.proof_of_funds_status != "verified"]
            ),
            "offers_needing_owner_review": len(
                [interest for interest in interests if interest.interest_status == "owner_review_needed"]
            ),
            "deals_blocked_from_buyer_portal": blocked_buyer_deals,
        },
        "seller_acquisition": seller_pipeline_command_center(session),
        "contract_title_control": contract_title_dashboard(session),
        "communication_gate": communication_dashboard(session),
        "seller_portal": seller_portal_dashboard(session),
        "unified_deal_room": closing_coordination_dashboard(session),
        "deal_evidence": evidence_dashboard(session),
        "buyer_demand_distribution": buyer_demand_dashboard(session),
    }
