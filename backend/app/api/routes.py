from __future__ import annotations

from fastapi import APIRouter, Body, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_session
from app.domain.buyer_portal import (
    buyer_portal_rules,
    portal_publish_gate,
    sanitize_buyer_deal,
    update_publication_gate,
)
from app.domain.command_center import build_command_center
from app.domain.compliance import compliance_checklists
from app.domain.contract_control import (
    assignment_readiness_gate,
    contract_prep_gate,
    contract_title_dashboard,
    title_handoff_summary,
    update_assignment_readiness,
    update_contract_prep_gate,
    validate_contract_language,
)
from app.domain.imports import preview_lead_csv
from app.domain.profit_control import ProfitControlInput, calculate_profit_control
from app.domain.rules import system_rules, validate_action
from app.domain.seller_acquisition import (
    offer_packet_gate,
    seller_draft_engine,
    seller_pipeline_command_center,
    update_offer_packet_gate,
    validate_seller_language,
)
from app.models import (
    Agent,
    AssignmentReadinessRecord,
    Buyer,
    BuyerDealPublication,
    BuyerInterest,
    BuyerMatch,
    ComplianceRecord,
    ContractControl,
    Deal,
    Division,
    Lead,
    OfferPacket,
    SellerInteraction,
    TitleHandoffPacket,
)
from app.serializers import model_to_dict

router = APIRouter(prefix="/api")


class ActionRequest(BaseModel):
    actor: str
    action: str
    content: str = ""
    owner_approved: bool = False
    compliance_reviewed: bool = False


class BuyerInterestRequest(BaseModel):
    buyer_id: str
    intended_offer_amount: int | None = None
    notes: str = ""


class SellerLanguageRequest(BaseModel):
    content: str


class ContractLanguageRequest(BaseModel):
    content: str


def all_records(session: Session, model) -> list[dict]:
    return [model_to_dict(row) for row in session.query(model).all()]


def get_record(session: Session, model, record_id: str) -> dict:
    record = session.get(model, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return model_to_dict(record)


def require_buyer_invite(x_buyer_invite: str | None = Header(default=None)) -> None:
    if x_buyer_invite != "demo-buyer-invite":
        raise HTTPException(status_code=403, detail="Buyer portal invite is required")


@router.get("/system/rules")
def get_system_rules() -> dict[str, object]:
    return {
        **system_rules(),
        "buyer_portal": buyer_portal_rules(),
        "app_name": settings.app_name,
        "overseer": settings.overseer_name,
        "target_assignment_fee": settings.target_assignment_fee,
    }


@router.post("/actions/validate")
def validate_system_action(payload: ActionRequest) -> dict[str, object]:
    return validate_action(
        actor=payload.actor,
        action=payload.action,
        content=payload.content,
        owner_approved=payload.owner_approved,
        compliance_reviewed=payload.compliance_reviewed,
    ).as_dict()


@router.post("/data-import/leads/preview")
def lead_import_preview(csv_text: str = Body(..., media_type="text/csv")) -> dict[str, object]:
    return preview_lead_csv(csv_text)


@router.get("/command-center")
def command_center(session: Session = Depends(get_session)) -> dict[str, object]:
    return build_command_center(session)


@router.get("/hierarchy")
def hierarchy(session: Session = Depends(get_session)) -> dict[str, object]:
    divisions = session.query(Division).all()
    return {
        "owner": {"role": settings.owner_role, "final_approver": True},
        "overseer": {
            "name": settings.overseer_name,
            "role": "Executive overseer",
            "may_execute_real_world_actions": False,
        },
        "divisions": [
            {
                **model_to_dict(division),
                "agents": [model_to_dict(agent) for agent in division.agents],
            }
            for division in divisions
        ],
    }


@router.get("/divisions")
def divisions(session: Session = Depends(get_session)) -> list[dict]:
    return all_records(session, Division)


@router.get("/divisions/{division_id}")
def division_detail(division_id: str, session: Session = Depends(get_session)) -> dict:
    division = session.get(Division, division_id)
    if division is None:
        raise HTTPException(status_code=404, detail="Division not found")
    return {
        **model_to_dict(division),
        "agents": [model_to_dict(agent) for agent in division.agents],
    }


@router.get("/managers")
def managers(session: Session = Depends(get_session)) -> list[dict[str, object]]:
    return [
        {
            "manager_name": division.manager_name,
            "division": division.name,
            "division_id": division.id,
            "responsibilities": division.responsibilities,
            "priority_queue": division.priority_queue,
            "workload": division.workload,
            "active_recommendations": division.active_recommendations,
            "risk_flags": division.risk_flags,
            "performance_notes": division.performance_notes,
            "next_best_action": division.next_best_action,
        }
        for division in session.query(Division).all()
    ]


@router.get("/agents")
def agents(session: Session = Depends(get_session)) -> list[dict]:
    return all_records(session, Agent)


@router.get("/agents/{agent_id}")
def agent_detail(agent_id: str, session: Session = Depends(get_session)) -> dict:
    return get_record(session, Agent, agent_id)


@router.get("/leads")
def leads(session: Session = Depends(get_session)) -> list[dict]:
    return all_records(session, Lead)


@router.get("/leads/{lead_id}")
def lead_detail(lead_id: str, session: Session = Depends(get_session)) -> dict:
    lead = session.get(Lead, lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {
        **model_to_dict(lead),
        "deals": [model_to_dict(deal) for deal in lead.deals],
    }


@router.get("/deals")
def deals(session: Session = Depends(get_session)) -> list[dict]:
    return all_records(session, Deal)


@router.get("/deals/{deal_id}")
def deal_detail(deal_id: str, session: Session = Depends(get_session)) -> dict:
    deal = session.get(Deal, deal_id)
    if deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    return {
        **model_to_dict(deal),
        "lead": model_to_dict(deal.lead),
        "buyer_matches": [model_to_dict(match) for match in deal.matches],
        "compliance_records": [model_to_dict(record) for record in deal.compliance_records],
        "contract_controls": [model_to_dict(record) for record in deal.contract_controls],
        "title_handoff_packets": [
            model_to_dict(packet) for packet in deal.title_handoff_packets
        ],
    }


@router.get("/underwriting")
def underwriting(session: Session = Depends(get_session)) -> dict[str, object]:
    return {
        "engine": "Deal Underwriting Engine",
        "fields": [
            "ARV",
            "repairs",
            "holding costs",
            "closing costs",
            "buyer desired profit",
            "MAO",
            "offer range",
            "risk score",
            "confidence score",
            "notes",
        ],
        "deals": all_records(session, Deal),
    }


@router.post("/underwriting/profit-preview")
def profit_preview(payload: ProfitControlInput) -> dict[str, object]:
    return calculate_profit_control(payload)


@router.get("/profit-control")
def profit_control(session: Session = Depends(get_session)) -> dict[str, object]:
    return {
        "engine": "Middle-Man Profit Control Engine",
        "target_assignment_fee": settings.target_assignment_fee,
        "rules": [
            "Protect projected assignment fees of $10,000+",
            "Do not destroy buyer margin",
            "Do not recommend fake ARV or repair numbers",
            "Require owner approval before offer packet prep",
            "Require compliance review before assignment packet prep",
        ],
        "deals": all_records(session, Deal),
    }


@router.get("/seller-followups")
def seller_followups(session: Session = Depends(get_session)) -> list[dict[str, object]]:
    stages = {"follow_up", "offer_sent", "negotiating", "contacted"}
    leads = session.query(Lead).filter(Lead.stage.in_(stages)).all()
    return [
        {
            **model_to_dict(lead),
            "draft_outputs": [
                "first_call_script",
                "sms_draft",
                "email_draft",
                "objection_response",
                "follow_up_plan",
                "offer_explanation",
                "negotiation_notes",
            ],
            "live_outreach_allowed": False,
        }
        for lead in leads
    ]


@router.get("/seller-acquisition")
def seller_acquisition_center(session: Session = Depends(get_session)) -> dict[str, object]:
    return seller_pipeline_command_center(session)


@router.get("/seller-acquisition/{lead_id}")
def seller_acquisition_detail(lead_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    lead = session.get(Lead, lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    interaction = (
        session.query(SellerInteraction)
        .filter(SellerInteraction.lead_id == lead_id)
        .order_by(SellerInteraction.created_at.desc())
        .first()
    )
    drafts = seller_draft_engine(lead, interaction)
    return {
        "lead": model_to_dict(lead),
        "seller_interaction": model_to_dict(interaction) if interaction else None,
        "draft_follow_up_engine": drafts,
        "next_best_seller_action": (
            interaction.next_best_seller_action
            if interaction
            else "Capture seller interaction details before offer prep."
        ),
    }


@router.post("/seller-acquisition/safety/validate")
def seller_safety_validate(payload: SellerLanguageRequest) -> dict[str, object]:
    return validate_seller_language(payload.content)


@router.get("/follow-up-control")
def follow_up_control(session: Session = Depends(get_session)) -> dict[str, object]:
    interactions = session.query(SellerInteraction).all()
    return {
        "draft_only": True,
        "live_outreach_allowed": False,
        "stale_followups": [
            model_to_dict(interaction)
            for interaction in interactions
            if interaction.follow_up_urgency in {"hot", "high"}
        ],
        "follow_up_sequences": [
            {
                "lead_id": interaction.lead_id,
                "seller_temperature_score": interaction.seller_temperature_score,
                "follow_up_urgency": interaction.follow_up_urgency,
                "next_follow_up_date": interaction.next_follow_up_date.isoformat()
                if interaction.next_follow_up_date
                else None,
                "sequence": seller_draft_engine(interaction.lead, interaction)["follow_up_sequence_draft"],
                "draft_only": True,
                "live_outreach_allowed": False,
            }
            for interaction in interactions
        ],
    }


@router.get("/offer-packets")
def offer_packets(session: Session = Depends(get_session)) -> list[dict[str, object]]:
    packets = session.query(OfferPacket).all()
    response = []
    for packet in packets:
        update_offer_packet_gate(packet, packet.deal)
        response.append({**model_to_dict(packet), "gate": offer_packet_gate(packet.deal, packet)})
    return response


@router.get("/offer-packets/{packet_id}")
def offer_packet_detail(packet_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    packet = session.get(OfferPacket, packet_id)
    if packet is None:
        raise HTTPException(status_code=404, detail="Offer packet not found")
    update_offer_packet_gate(packet, packet.deal)
    return {
        **model_to_dict(packet),
        "deal": model_to_dict(packet.deal),
        "lead": model_to_dict(packet.deal.lead),
        "gate": offer_packet_gate(packet.deal, packet),
        "draft_only": True,
        "real_world_action_taken": False,
    }


@router.post("/offer-packets/{packet_id}/prepare")
def prepare_offer_packet(packet_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    packet = session.get(OfferPacket, packet_id)
    if packet is None:
        raise HTTPException(status_code=404, detail="Offer packet not found")
    update_offer_packet_gate(packet, packet.deal)
    gate = offer_packet_gate(packet.deal, packet)
    if not gate["can_prepare"]:
        raise HTTPException(status_code=400, detail=gate)
    return {
        "packet_id": packet.id,
        "packet_status": packet.packet_status,
        "draft_only": True,
        "live_outreach_allowed": False,
        "contract_execution_allowed": False,
        "real_world_action_taken": False,
        "gate": gate,
    }


@router.get("/contract-control")
def contract_control_queue(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = contract_title_dashboard(session)
    session.commit()
    return dashboard


@router.get("/contract-control/{contract_id}")
def contract_control_detail(
    contract_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    contract = session.get(ContractControl, contract_id)
    if contract is None:
        raise HTTPException(status_code=404, detail="Contract control not found")
    update_contract_prep_gate(contract)
    session.commit()
    return {
        **model_to_dict(contract),
        "lead": model_to_dict(contract.lead),
        "deal": model_to_dict(contract.deal),
        "offer_packet": model_to_dict(contract.offer_packet),
        "gate": contract_prep_gate(contract),
        "draft_only": True,
        "contract_execution_allowed": False,
        "title_submission_allowed": False,
        "live_sending_allowed": False,
    }


@router.post("/contract-control/{contract_id}/prepare")
def prepare_contract_control(
    contract_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    contract = session.get(ContractControl, contract_id)
    if contract is None:
        raise HTTPException(status_code=404, detail="Contract control not found")
    update_contract_prep_gate(contract)
    gate = contract_prep_gate(contract)
    session.commit()
    if not gate["can_prepare"]:
        raise HTTPException(status_code=400, detail=gate)
    return {
        "contract_id": contract.id,
        "contract_status": contract.contract_status,
        "seller_accepted_terms": contract.seller_accepted_terms,
        "required_documents_checklist": contract.required_documents_checklist,
        "attorney_title_review_reminder": True,
        "draft_only": True,
        "executable_contract_generated": False,
        "contract_execution_allowed": False,
        "live_sending_allowed": False,
        "title_submission_allowed": False,
        "automatic_status_change_allowed": False,
        "gate": gate,
    }


@router.post("/contract-control/safety/validate")
def contract_safety_validate(payload: ContractLanguageRequest) -> dict[str, object]:
    return validate_contract_language(payload.content)


@router.get("/title-handoff")
def title_handoff_packets(session: Session = Depends(get_session)) -> list[dict[str, object]]:
    return [title_handoff_summary(packet) for packet in session.query(TitleHandoffPacket).all()]


@router.get("/title-handoff/{packet_id}")
def title_handoff_detail(
    packet_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    packet = session.get(TitleHandoffPacket, packet_id)
    if packet is None:
        raise HTTPException(status_code=404, detail="Title handoff packet not found")
    return {
        **title_handoff_summary(packet),
        "contract_control": model_to_dict(packet.contract_control),
        "deal": model_to_dict(packet.deal),
    }


@router.post("/title-handoff/{packet_id}/submit")
def submit_title_handoff_blocked(packet_id: str, session: Session = Depends(get_session)) -> dict:
    packet = session.get(TitleHandoffPacket, packet_id)
    if packet is None:
        raise HTTPException(status_code=404, detail="Title handoff packet not found")
    raise HTTPException(
        status_code=400,
        detail={
            "allowed": False,
            "reason": "Title-company submission is blocked in V4.",
            "packet_id": packet.id,
            "title_submission_allowed": False,
            "submitted_to_title": False,
        },
    )


@router.get("/assignment-readiness")
def assignment_readiness(session: Session = Depends(get_session)) -> list[dict[str, object]]:
    records = session.query(AssignmentReadinessRecord).all()
    response = []
    for record in records:
        update_assignment_readiness(record)
        response.append(
            {
                **model_to_dict(record),
                "gate": assignment_readiness_gate(record),
                "draft_only": True,
                "contract_execution_allowed": False,
                "title_submission_allowed": False,
            }
        )
    session.commit()
    return response


@router.get("/buyers")
def buyers(session: Session = Depends(get_session)) -> list[dict]:
    return all_records(session, Buyer)


@router.get("/buyers/{buyer_id}")
def buyer_detail(buyer_id: str, session: Session = Depends(get_session)) -> dict:
    buyer = session.get(Buyer, buyer_id)
    if buyer is None:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return {
        **model_to_dict(buyer),
        "matches": [model_to_dict(match) for match in buyer.matches],
    }


@router.get("/buyer-matches")
def buyer_matches(session: Session = Depends(get_session)) -> list[dict]:
    return all_records(session, BuyerMatch)


@router.get("/buyer-portal/rules")
def buyer_portal_policy() -> dict[str, object]:
    return buyer_portal_rules()


@router.get("/buyer-portal/deals")
def buyer_portal_deals(
    buyer_id: str = "buyer-001",
    _: None = Depends(require_buyer_invite),
    session: Session = Depends(get_session),
) -> list[dict[str, object]]:
    buyer = session.get(Buyer, buyer_id)
    publications = session.query(BuyerDealPublication).all()
    visible = []
    for publication in publications:
        update_publication_gate(publication, publication.deal)
        if portal_publish_gate(publication.deal, publication)["can_publish"]:
            visible.append(sanitize_buyer_deal(publication.deal, publication, buyer))
    return visible


@router.get("/buyer-portal/deals/{deal_id}")
def buyer_portal_deal_detail(
    deal_id: str,
    buyer_id: str = "buyer-001",
    _: None = Depends(require_buyer_invite),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    deal = session.get(Deal, deal_id)
    buyer = session.get(Buyer, buyer_id)
    if deal is None or deal.buyer_publication is None:
        raise HTTPException(status_code=404, detail="Deal is not available in buyer portal")
    update_publication_gate(deal.buyer_publication, deal)
    if not portal_publish_gate(deal, deal.buyer_publication)["can_publish"]:
        raise HTTPException(status_code=404, detail="Deal is not available in buyer portal")
    return sanitize_buyer_deal(deal, deal.buyer_publication, buyer)


@router.post("/buyer-portal/deals/{deal_id}/interest")
def record_buyer_interest(
    deal_id: str,
    payload: BuyerInterestRequest,
    _: None = Depends(require_buyer_invite),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    deal = session.get(Deal, deal_id)
    buyer = session.get(Buyer, payload.buyer_id)
    if deal is None or buyer is None or deal.buyer_publication is None:
        raise HTTPException(status_code=404, detail="Buyer or deal not found")
    update_publication_gate(deal.buyer_publication, deal)
    if not portal_publish_gate(deal, deal.buyer_publication)["can_publish"]:
        raise HTTPException(status_code=404, detail="Deal is not available in buyer portal")
    language_guard = validate_action(
        actor="Buyer Portal",
        action="draft",
        content=payload.notes,
    )
    if not language_guard.allowed:
        raise HTTPException(status_code=400, detail=language_guard.as_dict())

    count = session.query(BuyerInterest).count() + 1
    interest = BuyerInterest(
        id=f"interest-{count:03d}",
        buyer_id=buyer.id,
        deal_id=deal.id,
        interest_status="owner_review_needed",
        intended_offer_amount=payload.intended_offer_amount,
        proof_of_funds_status=buyer.proof_of_funds_status,
        notes=payload.notes,
        draft_only=True,
        contract_execution_allowed=False,
    )
    session.add(interest)
    session.commit()
    session.refresh(interest)
    return {
        **model_to_dict(interest),
        "real_world_action_taken": False,
        "payment_collected": False,
        "contract_executed": False,
    }


@router.get("/buyer-portal/profile")
def buyer_portal_profile(
    buyer_id: str = "buyer-001",
    _: None = Depends(require_buyer_invite),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    buyer = session.get(Buyer, buyer_id)
    if buyer is None:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return {
        "buyer_id": buyer.id,
        "name": buyer.name,
        "company": buyer.company,
        "target_zip_codes": buyer.target_zip_codes,
        "max_purchase_price": buyer.max_purchase_price,
        "property_type": buyer.property_type,
        "proof_of_funds_status": buyer.proof_of_funds_status,
        "closing_speed_days": buyer.closing_speed_days,
        "invite_gated": True,
    }


@router.get("/buyer-portal/watchlist")
def buyer_portal_watchlist(
    buyer_id: str = "buyer-001",
    _: None = Depends(require_buyer_invite),
    session: Session = Depends(get_session),
) -> list[dict[str, object]]:
    buyer = session.get(Buyer, buyer_id)
    if buyer is None:
        raise HTTPException(status_code=404, detail="Buyer not found")
    watchlist = []
    for match in buyer.matches:
        publication = match.deal.buyer_publication
        if publication and portal_publish_gate(match.deal, publication)["can_publish"]:
            watchlist.append(
                {
                    "match_id": match.id,
                    "match_score": match.score,
                    "deal": sanitize_buyer_deal(match.deal, publication, buyer),
                    "draft_only": True,
                }
            )
    return watchlist


@router.get("/buyer-portal/internal-dashboard")
def buyer_portal_internal_dashboard(
    session: Session = Depends(get_session),
) -> dict[str, object]:
    publications = session.query(BuyerDealPublication).all()
    visible_deals = []
    blocked_deals = []
    for publication in publications:
        update_publication_gate(publication, publication.deal)
        gate = portal_publish_gate(publication.deal, publication)
        item = {
            "deal_id": publication.deal_id,
            "operator_marked_visible": publication.operator_marked_visible,
            "availability_status": publication.availability_status,
            "blocked_reasons": gate["blocked_reasons"],
        }
        if gate["can_publish"]:
            visible_deals.append(item)
        else:
            blocked_deals.append(item)

    interests = session.query(BuyerInterest).all()
    return {
        "buyer_visible_deals": visible_deals,
        "buyer_interest_queue": [model_to_dict(interest) for interest in interests],
        "proof_of_funds_needed": [
            model_to_dict(interest)
            for interest in interests
            if interest.proof_of_funds_status != "verified"
        ],
        "offers_needing_owner_review": [
            model_to_dict(interest)
            for interest in interests
            if interest.interest_status == "owner_review_needed"
        ],
        "deals_blocked_from_buyer_portal": blocked_deals,
    }


@router.get("/compliance")
def compliance(session: Session = Depends(get_session)) -> dict[str, object]:
    return {
        **compliance_checklists("operator market"),
        "records": all_records(session, ComplianceRecord),
    }


@router.get("/daily-briefing")
def daily_briefing(session: Session = Depends(get_session)) -> dict[str, object]:
    command = build_command_center(session)
    return {
        "overseer": settings.overseer_name,
        "briefing": command["daily_strategy"],
        "top_hot_deals": command["top_hot_deals"],
        "attention_queue": command["attention_queue"],
        "compliance_alerts": command["compliance_alerts"],
        "owner_final_approval_required": True,
    }
