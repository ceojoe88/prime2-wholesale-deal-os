from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.client_command.service import (
    ClientCommandPermissionError,
    acquisition_brief_for_lead,
    acquisition_briefs,
    acquisition_needs_review,
    appointment_readiness_for_lead,
    buyer_buy_boxes_for_buyer,
    buyer_confidence_for_buyer,
    buyer_demand_evidence_for_lead,
    buyer_detail,
    buyer_matches_for_lead,
    buyer_outreach_drafts_for_lead,
    create_buyer_buy_box,
    create_buyer_demand_evidence,
    create_buyer_profile,
    disposition_blocked,
    disposition_matches,
    disposition_needs_review,
    disposition_readiness_for_lead,
    disposition_ready_review,
    disposition_strong_matches,
    evidence_items_for_lead,
    evidence_packet_for_lead,
    follow_up_drafts_for_lead,
    hot_board,
    lead_detail,
    list_leads,
    leads_for_workspace,
    list_workspaces,
    next_actions,
    objection_drafts_for_lead,
    offer_readiness_for_lead,
    question_plan_for_lead,
    require_member_permission,
    score_lead,
    underwriting_blocked,
    underwriting_needs_human_review,
    underwriting_ready_review,
    underwriting_review_for_lead,
    workspace_detail,
    workspace_buyers,
)
from app.domains.client_command.schemas import (
    ClientBuyerBuyBoxCreate,
    ClientBuyerDemandEvidenceCreate,
    ClientBuyerOutreachDraftCreate,
    ClientBuyerProfileCreate,
)


router = APIRouter(prefix="/api/v1/client-command", tags=["client-command"])


@router.get("/workspaces")
def workspaces(session: Session = Depends(get_session)) -> dict[str, object]:
    return list_workspaces(session)


@router.get("/workspaces/{workspace_id}")
def workspace(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return workspace_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/leads")
def workspace_leads(
    workspace_id: str,
    member_email: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        if member_email:
            require_member_permission(session, workspace_id, member_email, "client_command.leads_view")
        return leads_for_workspace(session, workspace_id)
    except ClientCommandPermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads")
def leads(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return list_leads(session, workspace_id)


@router.get("/leads/hot-board")
def leads_hot_board(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return hot_board(session, workspace_id)


@router.get("/leads/next-actions")
def leads_next_actions(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return next_actions(session, workspace_id)


@router.get("/leads/{lead_id}")
def lead(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return lead_detail(session, lead_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/leads/{lead_id}/acquisition-brief")
def create_acquisition_brief(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = acquisition_brief_for_lead(session, lead_id, workspace_id, refresh=True)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads/{lead_id}/acquisition-brief")
def get_acquisition_brief(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return acquisition_brief_for_lead(session, lead_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/leads/{lead_id}/question-plan")
def create_question_plan(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = question_plan_for_lead(session, lead_id, workspace_id, refresh=True)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads/{lead_id}/question-plan")
def get_question_plan(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return question_plan_for_lead(session, lead_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/leads/{lead_id}/objection-drafts")
def create_objection_drafts(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = objection_drafts_for_lead(session, lead_id, workspace_id, refresh=True)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads/{lead_id}/objection-drafts")
def get_objection_drafts(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return objection_drafts_for_lead(session, lead_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/leads/{lead_id}/follow-up-drafts")
def create_follow_up_drafts(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = follow_up_drafts_for_lead(session, lead_id, workspace_id, refresh=True)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads/{lead_id}/follow-up-drafts")
def get_follow_up_drafts(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return follow_up_drafts_for_lead(session, lead_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/leads/{lead_id}/appointment-readiness")
def create_appointment_readiness(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = appointment_readiness_for_lead(session, lead_id, workspace_id, refresh=True)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads/{lead_id}/appointment-readiness")
def get_appointment_readiness(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return appointment_readiness_for_lead(session, lead_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/leads/{lead_id}/deal-evidence-packet")
def create_deal_evidence_packet(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = evidence_packet_for_lead(session, lead_id, workspace_id, refresh=True)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads/{lead_id}/deal-evidence-packet")
def get_deal_evidence_packet(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return evidence_packet_for_lead(session, lead_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/leads/{lead_id}/evidence-items")
def create_evidence_items(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = evidence_items_for_lead(session, lead_id, workspace_id, refresh=True)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads/{lead_id}/evidence-items")
def get_evidence_items(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return evidence_items_for_lead(session, lead_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/leads/{lead_id}/underwriting-review")
def create_underwriting_review(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = underwriting_review_for_lead(session, lead_id, workspace_id, refresh=True)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads/{lead_id}/underwriting-review")
def get_underwriting_review(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return underwriting_review_for_lead(session, lead_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/leads/{lead_id}/offer-readiness")
def create_offer_readiness(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = offer_readiness_for_lead(session, lead_id, workspace_id, refresh=True)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads/{lead_id}/offer-readiness")
def get_offer_readiness(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return offer_readiness_for_lead(session, lead_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/acquisition/briefs")
def list_acquisition_briefs(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return acquisition_briefs(session, workspace_id)


@router.get("/acquisition/needs-review")
def list_acquisition_needs_review(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return acquisition_needs_review(session, workspace_id)


@router.get("/underwriting/ready-review")
def list_underwriting_ready_review(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return underwriting_ready_review(session, workspace_id)


@router.get("/underwriting/blocked")
def list_underwriting_blocked(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return underwriting_blocked(session, workspace_id)


@router.get("/underwriting/needs-human-review")
def list_underwriting_needs_human_review(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return underwriting_needs_human_review(session, workspace_id)


@router.post("/workspaces/{workspace_id}/buyers")
def create_workspace_buyer(
    workspace_id: str,
    payload: ClientBuyerProfileCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_buyer_profile(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/buyers")
def list_workspace_buyers(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return workspace_buyers(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/buyers/{buyer_id}")
def get_buyer_detail(
    buyer_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return buyer_detail(session, buyer_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/buyers/{buyer_id}/confidence-score")
def create_buyer_confidence(
    buyer_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = buyer_confidence_for_buyer(session, buyer_id, workspace_id, refresh=True)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/buyers/{buyer_id}/confidence-score")
def get_buyer_confidence(
    buyer_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return buyer_confidence_for_buyer(session, buyer_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/buyers/{buyer_id}/buy-boxes")
def create_buy_box(
    buyer_id: str,
    payload: ClientBuyerBuyBoxCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_buyer_buy_box(session, buyer_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/buyers/{buyer_id}/buy-boxes")
def get_buy_boxes(
    buyer_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return buyer_buy_boxes_for_buyer(session, buyer_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/leads/{lead_id}/buyer-matches")
def create_buyer_matches(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = buyer_matches_for_lead(session, lead_id, workspace_id, refresh=True)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads/{lead_id}/buyer-matches")
def get_buyer_matches(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return buyer_matches_for_lead(session, lead_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/disposition/matches")
def list_disposition_matches(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return disposition_matches(session, workspace_id)


@router.get("/disposition/strong-matches")
def list_disposition_strong_matches(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return disposition_strong_matches(session, workspace_id)


@router.get("/disposition/needs-review")
def list_disposition_needs_review(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return disposition_needs_review(session, workspace_id)


@router.post("/leads/{lead_id}/buyer-demand-evidence")
def create_lead_buyer_demand_evidence(
    lead_id: str,
    payload: ClientBuyerDemandEvidenceCreate,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_buyer_demand_evidence(session, lead_id, payload.model_dump(), workspace_id)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads/{lead_id}/buyer-demand-evidence")
def get_lead_buyer_demand_evidence(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return buyer_demand_evidence_for_lead(session, lead_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/leads/{lead_id}/disposition-readiness")
def create_disposition_readiness(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = disposition_readiness_for_lead(session, lead_id, workspace_id, refresh=True)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads/{lead_id}/disposition-readiness")
def get_disposition_readiness(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return disposition_readiness_for_lead(session, lead_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/disposition/ready-review")
def list_disposition_ready_review(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return disposition_ready_review(session, workspace_id)


@router.get("/disposition/blocked")
def list_disposition_blocked(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return disposition_blocked(session, workspace_id)


@router.post("/leads/{lead_id}/buyer-outreach-drafts")
def create_lead_buyer_outreach_drafts(
    lead_id: str,
    payload: ClientBuyerOutreachDraftCreate,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = buyer_outreach_drafts_for_lead(session, lead_id, workspace_id, refresh=True, values=payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads/{lead_id}/buyer-outreach-drafts")
def get_lead_buyer_outreach_drafts(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return buyer_outreach_drafts_for_lead(session, lead_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads/{lead_id}/score")
def lead_score(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = score_lead(session, lead_id, workspace_id)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
