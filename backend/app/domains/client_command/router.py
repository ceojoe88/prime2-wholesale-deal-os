from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.client_command import schemas as client_command_schemas
from app.domains.client_command import service as client_command_service
from app.domains.client_command.service import (
    ClientCommandPermissionError,
    acquisition_brief_for_lead,
    acquisition_briefs,
    acquisition_needs_review,
    appointment_readiness_for_lead,
    business_profile_detail,
    buyer_buy_boxes_for_buyer,
    buyer_confidence_for_buyer,
    buyer_demand_evidence_for_lead,
    buyer_detail,
    buyer_matches_for_lead,
    buyer_outreach_drafts_for_lead,
    buyer_list_setup_detail,
    communication_approval_gate_detail,
    communication_approval_gates,
    compliance_blocked,
    compliance_needs_review,
    compliance_overview,
    compliance_setup_checklist_detail,
    compliance_safe_manual_use,
    consent_record_detail,
    create_business_profile,
    create_buyer_buy_box,
    create_buyer_demand_evidence,
    create_buyer_list_setup,
    create_buyer_profile,
    create_communication_approval_gate,
    create_compliance_setup_checklist,
    create_compliance_readiness_placeholder,
    create_consent_record,
    create_default_pipeline_stages,
    create_first_leads_checklist,
    create_first_weekly_cycle_readiness,
    create_go_live_gate,
    create_lead_source_setup,
    create_market_setup,
    create_message_risk_review,
    create_onboarding_report,
    create_onboarding_task,
    create_opt_out_record,
    create_pipeline_setup,
    create_readiness_score,
    create_strategy_profile,
    create_team_setup_checklist,
    create_weekly_report,
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
    lead_source_setups_detail,
    list_leads,
    leads_for_workspace,
    list_workspaces,
    market_setups_detail,
    mark_weekly_report_client_visible,
    mark_weekly_report_reviewed,
    first_leads_checklist_detail,
    first_weekly_cycle_readiness_detail,
    go_live_gate_detail,
    message_risk_review_detail,
    next_actions,
    onboarding_activation_board,
    onboarding_blockers_detail,
    onboarding_overview,
    onboarding_report_detail,
    onboarding_tasks_blocked,
    onboarding_tasks_detail,
    onboarding_tasks_urgent,
    opt_out_record_detail,
    objection_drafts_for_lead,
    offer_readiness_for_lead,
    pipeline_setup_detail,
    pipeline_stage_detail,
    question_plan_for_lead,
    readiness_score_detail,
    reports_bottlenecks,
    reports_overview,
    reports_recommended_actions,
    reports_weekly,
    require_member_permission,
    safe_contact_status_for_buyer,
    safe_contact_status_for_lead,
    score_lead,
    strategy_profile_detail,
    team_setup_checklist_detail,
    underwriting_blocked,
    underwriting_needs_human_review,
    underwriting_ready_review,
    underwriting_review_for_lead,
    weekly_report_bottlenecks,
    weekly_report_detail,
    weekly_report_division_summaries,
    weekly_report_lead_rollups,
    weekly_report_metrics,
    weekly_report_recommended_actions,
    workspace_detail,
    workspace_buyers,
    workspace_compliance_placeholders,
    workspace_consent_records,
    workspace_opt_out_records,
    workspace_weekly_reports,
)
from app.domains.client_command.schemas import (
    ClientBusinessProfileCreate,
    ClientBuyerListSetupCreate,
    ClientBuyerBuyBoxCreate,
    ClientBuyerDemandEvidenceCreate,
    ClientBuyerOutreachDraftCreate,
    ClientBuyerProfileCreate,
    ClientCommunicationApprovalGateCreate,
    ClientComplianceSetupChecklistCreate,
    ClientComplianceReadinessPlaceholderCreate,
    ClientContactConsentRecordCreate,
    ClientContactOptOutRecordCreate,
    ClientFirstLeadImportChecklistCreate,
    ClientLeadSourceSetupCreate,
    ClientMarketSetupCreate,
    ClientMessageRiskReviewCreate,
    ClientOnboardingTaskCreate,
    ClientPipelineSetupCreate,
    ClientStrategyProfileCreate,
    ClientTeamSetupChecklistCreate,
    ClientWeeklyCommandReportCreate,
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


@router.post("/workspaces/{workspace_id}/compliance/consent-records")
def create_workspace_consent_record(
    workspace_id: str,
    payload: ClientContactConsentRecordCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_consent_record(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/compliance/consent-records")
def get_workspace_consent_records(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return workspace_consent_records(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/compliance/consent-records/{record_id}")
def get_consent_record(
    record_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return consent_record_detail(session, record_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/compliance/opt-outs")
def create_workspace_opt_out(
    workspace_id: str,
    payload: ClientContactOptOutRecordCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_opt_out_record(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/compliance/opt-outs")
def get_workspace_opt_outs(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return workspace_opt_out_records(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/compliance/opt-outs/{record_id}")
def get_opt_out_record(
    record_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return opt_out_record_detail(session, record_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/leads/{lead_id}/compliance/safe-contact-status")
def create_lead_safe_contact_status(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = safe_contact_status_for_lead(session, lead_id, workspace_id, refresh=True)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/leads/{lead_id}/compliance/safe-contact-status")
def get_lead_safe_contact_status(
    lead_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return safe_contact_status_for_lead(session, lead_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/buyers/{buyer_id}/compliance/safe-contact-status")
def create_buyer_safe_contact_status(
    buyer_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = safe_contact_status_for_buyer(session, buyer_id, workspace_id, refresh=True)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/buyers/{buyer_id}/compliance/safe-contact-status")
def get_buyer_safe_contact_status(
    buyer_id: str,
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return safe_contact_status_for_buyer(session, buyer_id, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/compliance/blocked")
def list_compliance_blocked(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return compliance_blocked(session, workspace_id)


@router.get("/compliance/needs-review")
def list_compliance_needs_review(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return compliance_needs_review(session, workspace_id)


@router.get("/compliance/safe-manual-use")
def list_compliance_safe_manual_use(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return compliance_safe_manual_use(session, workspace_id)


@router.post("/compliance/message-risk-review")
def create_compliance_message_risk_review(
    payload: ClientMessageRiskReviewCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_message_risk_review(session, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/compliance/message-risk-review/{review_id}")
def get_compliance_message_risk_review(
    review_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return message_risk_review_detail(session, review_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/compliance/communication-approval-gate")
def create_compliance_communication_gate(
    payload: ClientCommunicationApprovalGateCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_communication_approval_gate(session, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/compliance/communication-approval-gates")
def list_compliance_communication_gates(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return communication_approval_gates(session, workspace_id)


@router.get("/compliance/communication-approval-gates/{gate_id}")
def get_compliance_communication_gate(
    gate_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return communication_approval_gate_detail(session, gate_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/compliance/readiness-placeholders")
def create_workspace_compliance_placeholder(
    workspace_id: str,
    payload: ClientComplianceReadinessPlaceholderCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_compliance_readiness_placeholder(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/compliance/readiness-placeholders")
def get_workspace_compliance_placeholders(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return workspace_compliance_placeholders(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/compliance/overview")
def get_compliance_overview(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return compliance_overview(session, workspace_id)


@router.post("/workspaces/{workspace_id}/weekly-reports")
def create_workspace_weekly_report(
    workspace_id: str,
    payload: ClientWeeklyCommandReportCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_weekly_report(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/weekly-reports")
def get_workspace_weekly_reports(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return workspace_weekly_reports(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/weekly-reports/{report_id}")
def get_weekly_report(
    report_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return weekly_report_detail(session, report_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/weekly-reports/{report_id}/mark-reviewed")
def review_weekly_report(
    report_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = mark_weekly_report_reviewed(session, report_id)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/weekly-reports/{report_id}/mark-client-visible")
def publish_weekly_report(
    report_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = mark_weekly_report_client_visible(session, report_id)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/weekly-reports/{report_id}/metrics")
def get_weekly_report_metrics(
    report_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return weekly_report_metrics(session, report_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/weekly-reports/{report_id}/lead-rollups")
def get_weekly_report_lead_rollups(
    report_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return weekly_report_lead_rollups(session, report_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/weekly-reports/{report_id}/bottlenecks")
def get_weekly_report_bottlenecks(
    report_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return weekly_report_bottlenecks(session, report_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/weekly-reports/{report_id}/recommended-actions")
def get_weekly_report_recommended_actions(
    report_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return weekly_report_recommended_actions(session, report_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/weekly-reports/{report_id}/division-summaries")
def get_weekly_report_division_summaries(
    report_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return weekly_report_division_summaries(session, report_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/reports/overview")
def get_reports_overview(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return reports_overview(session, workspace_id)


@router.get("/reports/weekly")
def get_reports_weekly(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return reports_weekly(session, workspace_id)


@router.get("/reports/bottlenecks")
def get_reports_bottlenecks(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return reports_bottlenecks(session, workspace_id)


@router.get("/reports/recommended-actions")
def get_reports_recommended_actions(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return reports_recommended_actions(session, workspace_id)


@router.post("/workspaces/{workspace_id}/onboarding/business-profile")
def post_business_profile(
    workspace_id: str,
    payload: ClientBusinessProfileCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_business_profile(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/onboarding/business-profile")
def get_business_profile(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return business_profile_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/onboarding/strategy-profile")
def post_strategy_profile(
    workspace_id: str,
    payload: ClientStrategyProfileCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_strategy_profile(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/onboarding/strategy-profile")
def get_strategy_profile(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return strategy_profile_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/onboarding/markets")
def post_market_setup(
    workspace_id: str,
    payload: ClientMarketSetupCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_market_setup(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/onboarding/markets")
def get_market_setups(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return market_setups_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/onboarding/pipeline")
def post_pipeline_setup(
    workspace_id: str,
    payload: ClientPipelineSetupCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_pipeline_setup(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/onboarding/pipeline")
def get_pipeline_setup(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return pipeline_setup_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/onboarding/pipeline/default-stages")
def post_default_pipeline_stages(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_default_pipeline_stages(session, workspace_id)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/onboarding/pipeline/stages")
def get_pipeline_stages(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return pipeline_stage_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/onboarding/lead-sources")
def post_lead_source_setup(
    workspace_id: str,
    payload: ClientLeadSourceSetupCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_lead_source_setup(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/onboarding/lead-sources")
def get_lead_source_setups(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return lead_source_setups_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/onboarding/buyer-list-setup")
def post_buyer_list_setup(
    workspace_id: str,
    payload: ClientBuyerListSetupCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_buyer_list_setup(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/onboarding/buyer-list-setup")
def get_buyer_list_setup(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return buyer_list_setup_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/onboarding/team-checklist")
def post_team_checklist(
    workspace_id: str,
    payload: ClientTeamSetupChecklistCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_team_setup_checklist(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/onboarding/team-checklist")
def get_team_checklist(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return team_setup_checklist_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/onboarding/compliance-checklist")
def post_onboarding_compliance_checklist(
    workspace_id: str,
    payload: ClientComplianceSetupChecklistCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_compliance_setup_checklist(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/onboarding/compliance-checklist")
def get_onboarding_compliance_checklist(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return compliance_setup_checklist_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/onboarding/first-leads-checklist")
def post_first_leads_checklist(
    workspace_id: str,
    payload: ClientFirstLeadImportChecklistCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_first_leads_checklist(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/onboarding/first-leads-checklist")
def get_first_leads_checklist(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return first_leads_checklist_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/onboarding/readiness-score")
def post_readiness_score(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_readiness_score(session, workspace_id)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/onboarding/readiness-score")
def get_readiness_score(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return readiness_score_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/onboarding/blockers")
def get_onboarding_blockers(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return onboarding_blockers_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/onboarding/go-live-gate")
def post_go_live_gate(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_go_live_gate(session, workspace_id)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/onboarding/go-live-gate")
def get_go_live_gate(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return go_live_gate_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/onboarding/first-weekly-cycle-readiness")
def post_first_weekly_cycle_readiness(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_first_weekly_cycle_readiness(session, workspace_id)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/onboarding/first-weekly-cycle-readiness")
def get_first_weekly_cycle_readiness(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return first_weekly_cycle_readiness_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/onboarding/tasks")
def post_onboarding_task(
    workspace_id: str,
    payload: ClientOnboardingTaskCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_onboarding_task(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/onboarding/tasks")
def get_onboarding_tasks(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return onboarding_tasks_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/onboarding/tasks/blocked")
def get_onboarding_tasks_blocked(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return onboarding_tasks_blocked(session, workspace_id)


@router.get("/onboarding/tasks/urgent")
def get_onboarding_tasks_urgent(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return onboarding_tasks_urgent(session, workspace_id)


@router.post("/workspaces/{workspace_id}/onboarding/report")
def post_onboarding_report(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = create_onboarding_report(session, workspace_id)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/onboarding/report")
def get_onboarding_report(
    workspace_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        return onboarding_report_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/onboarding/overview")
def get_onboarding_overview(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return onboarding_overview(session, workspace_id)


@router.get("/onboarding/activation-board")
def get_onboarding_activation_board(
    workspace_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return onboarding_activation_board(session, workspace_id)


@router.get("/plans/catalog")
def get_plan_catalog(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.plan_catalog(session)


@router.post("/plans/catalog")
def post_plan_catalog(
    payload: client_command_schemas.ClientPlanCatalogCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    body = client_command_service.create_plan_catalog(session, payload.model_dump())
    session.commit()
    return body


@router.get("/plans/features")
def get_plan_features(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.plan_features(session)


@router.get("/plans/limits")
def get_plan_limits(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.plan_limits(session)


@router.post("/workspaces/{workspace_id}/plan-assignment")
def post_plan_assignment(
    workspace_id: str,
    payload: client_command_schemas.ClientWorkspacePlanAssignmentCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.create_plan_assignment(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/plan-assignment")
def get_plan_assignment(workspace_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return client_command_service.plan_assignment_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/feature-gates/evaluate")
def post_feature_gate_evaluation(
    workspace_id: str,
    payload: client_command_schemas.ClientFeatureGateEvaluationCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.evaluate_feature_gates(session, workspace_id, payload.feature_key)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/feature-gates")
def get_feature_gates(workspace_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return client_command_service.feature_gate_list(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/usage")
def get_usage(workspace_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return client_command_service.usage_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/usage/recalculate")
def post_usage_recalculate(workspace_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        body = client_command_service.recalculate_usage(session, workspace_id)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/upgrade-recommendations")
def get_upgrade_recommendations(workspace_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return client_command_service.upgrade_recommendations_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/billing-readiness")
def post_billing_readiness(
    workspace_id: str,
    payload: client_command_schemas.ClientBillingReadinessRecordCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.create_billing_readiness_record(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/billing-readiness")
def get_billing_readiness(workspace_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return client_command_service.billing_readiness_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/subscription-placeholder")
def post_subscription_placeholder(
    workspace_id: str,
    payload: client_command_schemas.ClientSubscriptionPlaceholderCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.create_subscription_placeholder(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/subscription-placeholder")
def get_subscription_placeholder(workspace_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return client_command_service.subscription_placeholder_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/plans/overview")
def get_plans_overview(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.plans_overview(session)


@router.get("/communication/providers")
def get_communication_providers(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.communication_providers(session)


@router.post("/communication/providers")
def post_communication_provider(
    payload: client_command_schemas.ClientCommunicationProviderProfileCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    body = client_command_service.create_communication_provider(session, payload.model_dump())
    session.commit()
    return body


@router.post("/communication/readiness-check")
def post_communication_readiness_check(
    payload: client_command_schemas.ClientCommunicationReadinessCheckCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.create_communication_readiness_check(session, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/communication/readiness-checks")
def get_communication_readiness_checks(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.communication_readiness_checks(session)


@router.post("/communication/dry-run")
def post_communication_dry_run(
    payload: client_command_schemas.ClientCommunicationDryRunCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.create_communication_dry_run(session, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/communication/dry-runs")
def get_communication_dry_runs(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.communication_dry_runs(session)


@router.post("/communication/send-approval")
def post_communication_send_approval(
    payload: client_command_schemas.ClientCommunicationSendApprovalCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.create_communication_send_approval(session, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/communication/send-approvals")
def get_communication_send_approvals(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.communication_send_approvals(session)


@router.post("/communication/send-attempt")
def post_communication_send_attempt(
    payload: client_command_schemas.ClientCommunicationSendAttemptCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.create_communication_send_attempt(session, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/communication/send-attempts")
def get_communication_send_attempts(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.communication_send_attempts(session)


@router.get("/communication/external-references")
def get_communication_external_references(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.communication_external_references(session)


@router.get("/communication/overview")
def get_communication_overview(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.communication_overview(session)


@router.get("/billing/providers")
def get_billing_providers(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.billing_providers(session)


@router.post("/billing/providers")
def post_billing_provider(
    payload: client_command_schemas.ClientBillingProviderProfileCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    body = client_command_service.create_billing_provider(session, payload.model_dump())
    session.commit()
    return body


@router.get("/billing/customer-profiles")
def get_billing_customer_profiles(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.billing_customer_profiles(session)


@router.post("/billing/customer-profiles")
def post_billing_customer_profile(
    payload: client_command_schemas.ClientBillingCustomerProfileCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.create_billing_customer_profile(session, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/billing/readiness-check")
def post_billing_readiness_check(
    payload: client_command_schemas.ClientBillingReadinessCheckCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.create_billing_readiness_check(session, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/billing/readiness-checks")
def get_billing_readiness_checks(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.billing_readiness_checks(session)


@router.post("/billing/checkout-dry-run")
def post_checkout_dry_run(
    payload: client_command_schemas.ClientCheckoutDryRunCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.create_checkout_dry_run(session, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/billing/checkout-dry-runs")
def get_checkout_dry_runs(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.checkout_dry_runs(session)


@router.post("/billing/approval")
def post_billing_approval(
    payload: client_command_schemas.ClientBillingApprovalCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.create_billing_approval(session, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/billing/approvals")
def get_billing_approvals(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.billing_approvals(session)


@router.post("/billing/attempt")
def post_billing_attempt(
    payload: client_command_schemas.ClientBillingAttemptCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.create_billing_attempt(session, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/billing/attempts")
def get_billing_attempts(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.billing_attempts(session)


@router.get("/billing/external-references")
def get_billing_external_references(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.billing_external_references(session)


@router.get("/billing/ledger")
def get_billing_ledger(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.billing_ledger(session)


@router.get("/billing/overview")
def get_billing_overview(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.billing_overview(session)


@router.get("/pilot/programs")
def get_pilot_programs(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.pilot_programs(session)


@router.post("/pilot/programs")
def post_pilot_program(
    payload: client_command_schemas.ClientPilotProgramCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    body = client_command_service.create_pilot_program(session, payload.model_dump())
    session.commit()
    return body


@router.get("/workspaces/{workspace_id}/pilot/enrollment")
def get_pilot_enrollment(workspace_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return client_command_service.pilot_enrollment_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/pilot/enrollment")
def post_pilot_enrollment(
    workspace_id: str,
    payload: client_command_schemas.ClientPilotWorkspaceEnrollmentCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.create_pilot_enrollment(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/pilot/operating-mode")
def get_pilot_operating_mode(workspace_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return client_command_service.pilot_operating_mode_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/pilot/operating-mode")
def post_pilot_operating_mode(
    workspace_id: str,
    payload: client_command_schemas.ClientPilotOperatingModeCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.create_pilot_operating_mode(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/pilot/health-snapshot")
def post_pilot_health_snapshot(workspace_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        body = client_command_service.create_pilot_health_snapshot(session, workspace_id)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/pilot/health-snapshot")
def get_pilot_health_snapshot(workspace_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return client_command_service.pilot_health_snapshot_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/pilot/support-tickets")
def post_pilot_support_ticket(
    workspace_id: str,
    payload: client_command_schemas.ClientPilotSupportTicketCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.create_pilot_support_ticket(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/pilot/support-tickets")
def get_pilot_support_tickets(workspace_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return client_command_service.pilot_support_tickets(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/pilot/support-actions")
def post_pilot_support_action(
    payload: client_command_schemas.ClientPilotSupportActionCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.create_pilot_support_action(session, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/pilot/support-actions")
def get_pilot_support_actions(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.pilot_support_actions(session)


@router.post("/pilot/escalations")
def post_pilot_escalation(
    payload: client_command_schemas.ClientPilotEscalationCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.create_pilot_escalation(session, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/pilot/escalations")
def get_pilot_escalations(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.pilot_escalations(session)


@router.post("/workspaces/{workspace_id}/pilot/launch-checklist")
def post_pilot_launch_checklist(workspace_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        body = client_command_service.create_pilot_launch_checklist(session, workspace_id)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/pilot/launch-checklist")
def get_pilot_launch_checklist(workspace_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return client_command_service.pilot_launch_checklist_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/pilot/risk-review")
def post_pilot_risk_review(workspace_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        body = client_command_service.create_pilot_risk_review(session, workspace_id)
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/pilot/risk-review")
def get_pilot_risk_review(workspace_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return client_command_service.pilot_risk_review_detail(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/pilot/client-safe-updates")
def post_pilot_client_safe_update(
    workspace_id: str,
    payload: client_command_schemas.ClientPilotClientSafeUpdateCreate,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    try:
        body = client_command_service.create_pilot_client_safe_update(session, workspace_id, payload.model_dump())
        session.commit()
        return body
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/pilot/client-safe-updates")
def get_pilot_client_safe_updates(workspace_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    try:
        return client_command_service.pilot_client_safe_updates(session, workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/pilot/admin-console")
def get_pilot_admin_console(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.pilot_admin_console(session)


@router.get("/pilot/support-console")
def get_pilot_support_console(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.pilot_support_console(session)


@router.get("/pilot/blocked")
def get_pilot_blocked(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.pilot_blocked(session)


@router.get("/pilot/needs-review")
def get_pilot_needs_review(session: Session = Depends(get_session)) -> dict[str, object]:
    return client_command_service.pilot_needs_review(session)
