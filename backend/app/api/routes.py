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
from app.domain.communications import (
    approval_gate,
    communication_dashboard,
    communication_hash,
    generate_dry_run_receipt,
    latest_approval_for,
    send_with_gate,
    update_draft_safety,
    validate_communication_safety,
)
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
from app.domain.seller_portal import (
    response_content,
    sanitize_seller_offer,
    seller_portal_dashboard,
    seller_portal_rules,
    seller_response_is_review_only,
    seller_visibility_gate,
    update_seller_visibility_gate,
    validate_seller_portal_language,
)
from app.models import (
    Agent,
    AssignmentReadinessRecord,
    Buyer,
    BuyerDealPublication,
    BuyerInterest,
    BuyerMatch,
    ComplianceRecord,
    CommunicationApproval,
    CommunicationDraft,
    CommunicationDryRunReceipt,
    CommunicationSendAttempt,
    ContractControl,
    Deal,
    Division,
    Lead,
    OfferPacket,
    SellerInteraction,
    SellerOfferPublication,
    SellerPortalResponse,
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


class CommunicationSendRequest(BaseModel):
    dry_run_receipt_id: str | None = None
    approval_id: str | None = None
    recipients: list[str] | None = None


class SellerPortalResponseRequest(BaseModel):
    offer_id: str
    response_type: str = "seller_portal_note"
    seller_portal_note: str = ""
    offer_question: str = ""
    appointment_access_preference: str = ""
    document_upload_placeholder: str = ""


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


def require_seller_invite(x_seller_invite: str | None = Header(default=None)) -> None:
    if x_seller_invite != "demo-seller-invite":
        raise HTTPException(status_code=403, detail="Seller portal invite is required")


@router.get("/system/rules")
def get_system_rules() -> dict[str, object]:
    return {
        **system_rules(),
        "buyer_portal": buyer_portal_rules(),
        "seller_portal": seller_portal_rules(),
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


@router.get("/communications")
def communications_dashboard(session: Session = Depends(get_session)) -> dict[str, object]:
    return communication_dashboard(session)


@router.get("/communications/dry-runs")
def communication_dry_runs(session: Session = Depends(get_session)) -> list[dict]:
    return all_records(session, CommunicationDryRunReceipt)


@router.get("/communications/attempts")
def communication_attempts(session: Session = Depends(get_session)) -> list[dict]:
    return all_records(session, CommunicationSendAttempt)


@router.get("/communications/approvals")
def communication_approvals(session: Session = Depends(get_session)) -> list[dict]:
    return all_records(session, CommunicationApproval)


@router.get("/communications/{draft_id}")
def communication_draft_detail(
    draft_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    draft = session.get(CommunicationDraft, draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="Communication draft not found")
    receipt = (
        session.get(CommunicationDryRunReceipt, draft.last_dry_run_receipt_id)
        if draft.last_dry_run_receipt_id
        else None
    )
    approval = latest_approval_for(session, draft, receipt)
    return {
        **model_to_dict(draft),
        "safety_preview": validate_communication_safety(draft),
        "latest_dry_run": model_to_dict(receipt) if receipt else None,
        "latest_gate": approval_gate(session, draft, receipt, approval),
        "bulk_send_allowed": False,
        "campaign_allowed": False,
        "auto_followup_allowed": False,
        "buyer_blast_allowed": False,
        "title_submission_allowed": False,
    }


@router.post("/communications/{draft_id}/safety-check")
def communication_safety_check(
    draft_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    draft = session.get(CommunicationDraft, draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="Communication draft not found")
    result = update_draft_safety(draft)
    session.commit()
    return {**model_to_dict(draft), "safety_result": result}


@router.post("/communications/{draft_id}/dry-run")
def communication_dry_run(
    draft_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    draft = session.get(CommunicationDraft, draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="Communication draft not found")
    receipt = generate_dry_run_receipt(session, draft)
    session.commit()
    session.refresh(receipt)
    return {
        **model_to_dict(receipt),
        "provider_call_made": False,
        "provider_mode": receipt.provider_mode,
        "draft_hash": communication_hash(draft.subject, draft.draft_body),
    }


@router.post("/communications/{draft_id}/approvals")
def communication_owner_approval(
    draft_id: str,
    dry_run_receipt_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    draft = session.get(CommunicationDraft, draft_id)
    receipt = session.get(CommunicationDryRunReceipt, dry_run_receipt_id)
    if draft is None or receipt is None or receipt.draft_id != draft.id:
        raise HTTPException(status_code=404, detail="Draft or dry-run receipt not found")
    if receipt.safety_result.get("allowed") is not True:
        raise HTTPException(
            status_code=400,
            detail={"allowed": False, "reason": "Safety must pass before owner approval."},
        )
    if communication_hash(draft.subject, draft.draft_body) != receipt.subject_body_hash:
        raise HTTPException(
            status_code=400,
            detail={"allowed": False, "reason": "Draft changed after dry-run."},
        )
    count = session.query(CommunicationApproval).count() + 1
    approval = CommunicationApproval(
        id=f"comm-approval-{count:03d}",
        draft_id=draft.id,
        dry_run_receipt_id=receipt.id,
        owner_approval_recorded=True,
        approval_status="approved",
        approval_notes="Owner approval recorded for one draft, one recipient, and one source record.",
        approved_by="Owner",
        draft_hash_at_approval=receipt.subject_body_hash,
    )
    draft.owner_approval_recorded = True
    draft.approved_dry_run_receipt_id = receipt.id
    session.add(approval)
    session.commit()
    session.refresh(approval)
    return model_to_dict(approval)


@router.post("/communications/{draft_id}/send")
def communication_send(
    draft_id: str,
    payload: CommunicationSendRequest | None = None,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    draft = session.get(CommunicationDraft, draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="Communication draft not found")
    payload = payload or CommunicationSendRequest()
    receipt_id = payload.dry_run_receipt_id or draft.last_dry_run_receipt_id
    receipt = session.get(CommunicationDryRunReceipt, receipt_id) if receipt_id else None
    approval = (
        session.get(CommunicationApproval, payload.approval_id)
        if payload.approval_id
        else latest_approval_for(session, draft, receipt)
    )
    recipient_count = len(payload.recipients) if payload.recipients is not None else 1
    attempt, gate = send_with_gate(session, draft, receipt, approval, recipient_count)
    session.commit()
    body = {
        **model_to_dict(attempt),
        "gate": gate,
        "provider_called": attempt.provider_called,
        "mock_sent": attempt.mock_sent,
    }
    if not gate["can_send"]:
        raise HTTPException(status_code=400, detail=body)
    return body


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


@router.get("/seller-portal/rules")
def seller_portal_policy() -> dict[str, object]:
    return seller_portal_rules()


@router.get("/seller-portal/offer")
def seller_portal_offer(
    offer_id: str = "seller-offer-001",
    _: None = Depends(require_seller_invite),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    publication = session.get(SellerOfferPublication, offer_id)
    if publication is None:
        raise HTTPException(status_code=404, detail="Offer is not available in seller portal")
    update_seller_visibility_gate(publication)
    session.commit()
    if not seller_visibility_gate(publication)["can_show"]:
        raise HTTPException(status_code=404, detail="Offer is not available in seller portal")
    return sanitize_seller_offer(publication)


@router.get("/seller-portal/offers/{offer_id}")
def seller_portal_offer_detail(
    offer_id: str,
    _: None = Depends(require_seller_invite),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    publication = session.get(SellerOfferPublication, offer_id)
    if publication is None:
        raise HTTPException(status_code=404, detail="Offer is not available in seller portal")
    update_seller_visibility_gate(publication)
    session.commit()
    if not seller_visibility_gate(publication)["can_show"]:
        raise HTTPException(status_code=404, detail="Offer is not available in seller portal")
    return sanitize_seller_offer(publication)


@router.get("/seller-portal/property")
def seller_portal_property(
    offer_id: str = "seller-offer-001",
    _: None = Depends(require_seller_invite),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    offer = seller_portal_offer(offer_id, _, session)
    return {
        "property_address_summary": offer["property_address_summary"],
        "inspection_access_next_step": offer["inspection_access_next_step"],
        "seller_questions_notes_action": offer["seller_questions_notes_action"],
    }


@router.get("/seller-portal/timeline")
def seller_portal_timeline(
    offer_id: str = "seller-offer-001",
    _: None = Depends(require_seller_invite),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    offer = seller_portal_offer(offer_id, _, session)
    return {
        "offer_status": offer["offer_status"],
        "closing_timeline_estimate": offer["closing_timeline_estimate"],
        "title_company_review_status": offer["title_company_review_status"],
    }


@router.get("/seller-portal/documents")
def seller_portal_documents(
    offer_id: str = "seller-offer-001",
    _: None = Depends(require_seller_invite),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    offer = seller_portal_offer(offer_id, _, session)
    return {
        "document_checklist": offer["document_checklist"],
        "seller_questions_notes_action": offer["seller_questions_notes_action"],
    }


@router.get("/seller-portal/messages")
def seller_portal_messages(
    _: None = Depends(require_seller_invite),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    responses = session.query(SellerPortalResponse).all()
    return {
        "responses": [model_to_dict(response) for response in responses],
        "draft_intake_only": True,
        "automatic_negotiation_allowed": False,
        "contract_execution_allowed": False,
    }


@router.post("/seller-portal/responses")
def record_seller_portal_response(
    payload: SellerPortalResponseRequest,
    _: None = Depends(require_seller_invite),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    publication = session.get(SellerOfferPublication, payload.offer_id)
    if publication is None:
        raise HTTPException(status_code=404, detail="Offer is not available in seller portal")
    update_seller_visibility_gate(publication)
    if not seller_visibility_gate(publication)["can_show"]:
        raise HTTPException(status_code=404, detail="Offer is not available in seller portal")
    if payload.response_type not in {
        "seller_portal_note",
        "offer_question",
        "appointment_access_preference",
        "document_upload_placeholder",
    }:
        raise HTTPException(status_code=400, detail="Unsupported seller response type")
    language = validate_seller_portal_language(response_content(payload.model_dump()))
    if not language["allowed"]:
        raise HTTPException(status_code=400, detail=language)

    count = session.query(SellerPortalResponse).count() + 1
    response = SellerPortalResponse(
        id=f"seller-response-{count:03d}",
        seller_offer_publication_id=publication.id,
        response_type=payload.response_type,
        seller_portal_note=payload.seller_portal_note,
        offer_question=payload.offer_question,
        appointment_access_preference=payload.appointment_access_preference,
        document_upload_placeholder=payload.document_upload_placeholder,
        response_status="received_for_operator_review",
        operator_review_status="pending_review",
        draft_only=True,
        negotiation_execution_allowed=False,
        contract_execution_allowed=False,
        automatic_acceptance_allowed=False,
    )
    session.add(response)
    session.commit()
    session.refresh(response)
    return {
        **model_to_dict(response),
        "review_only": seller_response_is_review_only(response),
        "automatic_negotiation_allowed": False,
        "contract_execution_allowed": False,
        "automatic_acceptance_allowed": False,
    }


@router.post("/seller-portal/offers/{offer_id}/accept")
def seller_portal_acceptance_blocked(
    offer_id: str,
    _: None = Depends(require_seller_invite),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    publication = session.get(SellerOfferPublication, offer_id)
    if publication is None:
        raise HTTPException(status_code=404, detail="Offer is not available in seller portal")
    raise HTTPException(
        status_code=400,
        detail={
            "allowed": False,
            "reason": "Seller portal responses are intake-only; no acceptance, negotiation automation, or contract execution is available.",
            "offer_id": publication.id,
            "automatic_negotiation_allowed": False,
            "contract_execution_allowed": False,
            "automatic_acceptance_allowed": False,
        },
    )


@router.get("/seller-portal/internal-dashboard")
def seller_portal_internal_dashboard(
    session: Session = Depends(get_session),
) -> dict[str, object]:
    dashboard = seller_portal_dashboard(session)
    session.commit()
    return dashboard


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
