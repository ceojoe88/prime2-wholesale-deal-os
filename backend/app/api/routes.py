from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_session
from app.domain.command_center import build_command_center
from app.domain.compliance import compliance_checklists
from app.domain.imports import preview_lead_csv
from app.domain.profit_control import ProfitControlInput, calculate_profit_control
from app.domain.rules import system_rules, validate_action
from app.models import Agent, Buyer, BuyerMatch, ComplianceRecord, Deal, Division, Lead
from app.serializers import model_to_dict

router = APIRouter(prefix="/api")


class ActionRequest(BaseModel):
    actor: str
    action: str
    content: str = ""
    owner_approved: bool = False
    compliance_reviewed: bool = False


def all_records(session: Session, model) -> list[dict]:
    return [model_to_dict(row) for row in session.query(model).all()]


def get_record(session: Session, model, record_id: str) -> dict:
    record = session.get(model, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return model_to_dict(record)


@router.get("/system/rules")
def get_system_rules() -> dict[str, object]:
    return {
        **system_rules(),
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
