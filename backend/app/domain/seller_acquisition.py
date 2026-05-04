from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models import Deal, Lead, OfferPacket, SellerInteraction


SELLER_UNSAFE_PATTERNS = {
    "pressure_language": [
        "you must sign",
        "sign now",
        "take it or leave it",
        "last chance",
        "do not talk to anyone else",
    ],
    "fake_buyer_claim": [
        "we already have a buyer",
        "cash buyer is guaranteed",
        "my buyer will definitely close",
    ],
    "fake_urgency": [
        "offer expires in minutes",
        "title closes today no matter what",
        "you will lose the house if you wait",
    ],
    "guaranteed_closing_claim": [
        "guaranteed closing",
        "we guarantee close",
        "guaranteed cash closing",
    ],
    "legal_advice": [
        "this is legal advice",
        "no attorney needed",
        "you are legally required",
        "ignore title",
    ],
    "misleading_assignment_language": [
        "hide the assignment",
        "do not mention assignment",
        "we are the end buyer no matter what",
        "assignment fee does not matter",
    ],
    "live_outreach": [
        "send sms",
        "send email",
        "call seller now",
        "dial seller",
    ],
}


def validate_seller_language(content: str) -> dict[str, object]:
    text = content.lower()
    flags = [
        category
        for category, phrases in SELLER_UNSAFE_PATTERNS.items()
        if any(phrase in text for phrase in phrases)
    ]
    return {
        "allowed": not flags,
        "risk_flags": flags,
        "reason": "Seller language is draft-safe." if not flags else "Unsafe seller language blocked.",
    }


def seller_draft_engine(lead: Lead, interaction: SellerInteraction | None = None) -> dict[str, object]:
    condition = interaction.property_condition if interaction else "condition still needs confirmation"
    timeline = interaction.timeline if interaction else "seller timeline still needs discovery"
    asking = interaction.asking_price if interaction else lead.asking_price
    drafts = {
        "call_script_draft": (
            f"Confirm the property at {lead.city}, {lead.state}, ask what changed for the seller, "
            f"listen for timeline, condition, and payoff constraints, then explain that any offer "
            "would be based on documented repair and resale assumptions."
        ),
        "sms_draft": (
            f"Hi {lead.seller_name}, this is a draft note for owner review. I wanted to follow up "
            "on your property and see if it still makes sense to discuss a possible as-is offer."
        ),
        "email_draft": (
            "Subject: Property follow-up\n\nThis is a draft for owner review. Based on the property "
            f"condition noted as {condition}, the next step would be to verify details before any offer is discussed."
        ),
        "objection_response_draft": (
            "Acknowledge the concern, restate that there is no pressure, and explain that the offer basis "
            "depends on verified ARV, repairs, holding costs, and buyer margin."
        ),
        "offer_explanation_draft": (
            f"If the seller asks about price, explain that the current asking reference is {asking or 'not confirmed'} "
            f"and the timeline is {timeline}. Any owner-approved offer packet must pass underwriting and compliance gates."
        ),
        "follow_up_sequence_draft": [
            "Day 0: owner reviews call notes and approves whether to contact",
            "Day 2: draft check-in focused on condition and timeline gaps",
            "Day 5: draft offer-basis explanation if underwriting is complete",
            "Day 10: draft close-the-loop note with no pressure language",
        ],
        "draft_only": True,
        "live_outreach_allowed": False,
    }
    combined = " ".join(str(value) for value in drafts.values())
    language = validate_seller_language(combined)
    return {**drafts, "language_guard": language}


def offer_packet_gate(deal: Deal, packet: OfferPacket | None = None) -> dict[str, object]:
    reasons: list[str] = []
    if deal.arv <= 0:
        reasons.append("missing_arv")
    if deal.repairs <= 0:
        reasons.append("missing_repair_estimate")
    if deal.max_seller_offer <= 0:
        reasons.append("max_seller_offer_missing")

    buyer_margin = deal.arv - deal.repairs - deal.buyer_costs - deal.buyer_purchase_price
    margin_protected = buyer_margin >= deal.buyer_desired_profit
    target_checked = deal.projected_assignment_fee >= deal.target_assignment_fee
    underwriting_complete = deal.arv > 0 and deal.repairs > 0 and deal.max_seller_offer > 0

    if not margin_protected:
        reasons.append("buyer_margin_not_protected")
    if not target_checked:
        reasons.append("target_assignment_fee_not_checked")
    if packet is None:
        reasons.append("missing_offer_packet_record")
        return {"can_prepare": False, "blocked_reasons": sorted(set(reasons))}
    if not packet.compliance_guard_passed:
        reasons.append("compliance_guard_not_passed")
    if not packet.owner_approval_recorded:
        reasons.append("owner_approval_not_recorded")
    if not packet.underwriting_complete or not underwriting_complete:
        reasons.append("underwriting_not_complete")
    if not packet.buyer_margin_protected or not margin_protected:
        reasons.append("buyer_margin_not_protected")
    if not packet.target_assignment_fee_checked or not target_checked:
        reasons.append("target_assignment_fee_not_checked")

    return {
        "can_prepare": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "buyer_margin": buyer_margin,
        "target_assignment_fee": deal.target_assignment_fee,
        "projected_assignment_fee": deal.projected_assignment_fee,
    }


def update_offer_packet_gate(packet: OfferPacket, deal: Deal) -> None:
    gate = offer_packet_gate(deal, packet)
    packet.blocked_reasons = gate["blocked_reasons"]
    packet.packet_prep_allowed = gate["can_prepare"]
    packet.approval_status = "owner_approved_draft_ready" if gate["can_prepare"] else "blocked"
    if gate["can_prepare"]:
        packet.packet_status = "draft_ready"


def seller_pipeline_command_center(session: Session) -> dict[str, object]:
    leads = session.query(Lead).all()
    interactions = session.query(SellerInteraction).all()
    interactions_by_lead = {interaction.lead_id: interaction for interaction in interactions}
    today = datetime.now(UTC)

    hot_sellers = []
    for lead in leads:
        interaction = interactions_by_lead.get(lead.id)
        temperature = interaction.seller_temperature_score if interaction else 0
        if lead.opportunity_score >= 80 or temperature >= 80:
            hot_sellers.append(lead)
    stale_followups = [
        interaction
        for interaction in interactions
        if interaction.next_follow_up_date and interaction.next_follow_up_date.replace(tzinfo=UTC) < today
    ]
    offer_needed = [lead for lead in leads if lead.stage == "offer_needed"]
    negotiating = [lead for lead in leads if lead.stage == "negotiating"]
    under_contract_candidates = [
        lead for lead in leads if lead.stage in {"offer_sent", "negotiating"} and lead.opportunity_score >= 72
    ]
    packets = session.query(OfferPacket).all()

    return {
        "hot_sellers": [lead.id for lead in hot_sellers],
        "stale_followups": [interaction.lead_id for interaction in stale_followups],
        "offer_needed_leads": [lead.id for lead in offer_needed],
        "negotiation_stage_leads": [lead.id for lead in negotiating],
        "under_contract_candidates": [lead.id for lead in under_contract_candidates],
        "seller_temperature": {
            interaction.lead_id: interaction.seller_temperature_score
            for interaction in interactions
        },
        "offer_readiness": {
            packet.id: {
                "deal_id": packet.deal_id,
                "packet_prep_allowed": packet.packet_prep_allowed,
                "approval_status": packet.approval_status,
                "blocked_reasons": packet.blocked_reasons,
            }
            for packet in packets
        },
        "draft_only": True,
        "live_outreach_allowed": False,
    }
