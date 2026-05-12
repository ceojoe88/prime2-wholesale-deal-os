from __future__ import annotations

from datetime import date, timedelta
from hashlib import sha256
from typing import Any
from uuid import uuid4

from sqlalchemy import desc
from sqlalchemy.orm import Session

import app.models as app_models
from app.domains.client_command.permissions import (
    CLIENT_COMMAND_PERMISSIONS,
    has_permission,
    member_permissions,
)
from app.domains.client_command import sanitizer as client_command_sanitizer
from app.domains.client_command.safety import (
    client_command_safety_rules,
    validate_client_safe_text,
)
from app.domains.client_command.sanitizer import (
    acquisition_brief_public,
    acquisition_event_public,
    action_public,
    activation_blocker_public,
    appointment_readiness_public,
    business_profile_public,
    buyer_buy_box_public,
    buyer_confidence_public,
    buyer_demand_evidence_public,
    buyer_list_setup_public,
    buyer_outreach_draft_public,
    buyer_profile_public,
    compliance_setup_checklist_public,
    communication_approval_gate_public,
    compliance_event_public,
    compliance_placeholder_public,
    consent_record_public,
    deal_buyer_match_public,
    disposition_event_public,
    disposition_readiness_public,
    evidence_item_public,
    evidence_packet_public,
    event_public,
    first_lead_import_checklist_public,
    first_weekly_cycle_readiness_public,
    follow_up_draft_public,
    go_live_gate_public,
    lead_public,
    lead_source_setup_public,
    market_setup_public,
    message_risk_review_public,
    member_public,
    missing_item_public,
    objection_draft_public,
    onboarding_manager_event_public,
    onboarding_report_public,
    onboarding_task_public,
    onboarding_timeline_event_public,
    opt_out_record_public,
    offer_readiness_public,
    offer_scenario_public,
    pipeline_setup_public,
    pipeline_stage_public,
    question_plan_public,
    role_public,
    safe_contact_status_public,
    score_public,
    seller_question_public,
    strategy_profile_public,
    team_setup_checklist_public,
    underwriting_event_public,
    underwriting_review_public,
    weekly_bottleneck_public,
    weekly_division_summary_public,
    weekly_lead_rollup_public,
    weekly_metric_snapshot_public,
    weekly_recommended_action_public,
    weekly_report_event_public,
    weekly_report_public,
    workspace_public,
    workspace_readiness_public,
)
from app.domains.client_command.scoring import missing_fields, score_client_lead
from app.models import (
    ClientActivationBlocker,
    ClientLeadDivisionEvent,
    ClientLeadIntelligenceScore,
    ClientLeadMissingDataItem,
    ClientLeadNextBestAction,
    ClientLeadProfile,
    ClientWorkspace,
    ClientWorkspaceMember,
    ClientWorkspaceRole,
    ClientAcquisitionBrief,
    ClientBusinessProfile,
    ClientBuyerBuyBox,
    ClientBuyerConfidenceScore,
    ClientBuyerDemandEvidence,
    ClientBuyerListSetup,
    ClientBuyerOutreachDraft,
    ClientBuyerProfile,
    ClientComplianceSetupChecklist,
    ClientCommunicationApprovalGate,
    ClientComplianceDivisionEvent,
    ClientComplianceReadinessPlaceholder,
    ClientContactConsentRecord,
    ClientContactOptOutRecord,
    ClientSellerQuestionPlan,
    ClientSellerQuestion,
    ClientObjectionResponseDraft,
    ClientFollowUpDraft,
    ClientAppointmentReadinessReview,
    ClientAcquisitionDivisionEvent,
    ClientDealEvidencePacket,
    ClientDealEvidenceItem,
    ClientDealBuyerMatch,
    ClientDispositionDivisionEvent,
    ClientDispositionReadinessGate,
    ClientMessageRiskReview,
    ClientSafeContactStatus,
    ClientFirstLeadImportChecklist,
    ClientFirstWeeklyCycleReadiness,
    ClientUnderwritingReview,
    ClientOfferScenario,
    ClientOfferReadinessGate,
    ClientUnderwritingDivisionEvent,
    ClientGoLiveReadinessGate,
    ClientLeadSourceSetup,
    ClientMarketSetup,
    ClientOnboardingManagerEvent,
    ClientOnboardingReport,
    ClientOnboardingTask,
    ClientOnboardingTimelineEvent,
    ClientPipelineSetup,
    ClientPipelineStageTemplate,
    ClientStrategyProfile,
    ClientTeamSetupChecklist,
    ClientWorkspaceReadinessScore,
    ClientWeeklyBottleneck,
    ClientWeeklyCommandReport,
    ClientWeeklyDivisionSummary,
    ClientWeeklyLeadStatusRollup,
    ClientWeeklyRecommendedAction,
    ClientWeeklyReportEvent,
    ClientWeeklyReportMetricSnapshot,
)


class ClientCommandPermissionError(ValueError):
    pass


def list_workspaces(session: Session) -> dict[str, object]:
    workspaces = session.query(ClientWorkspace).order_by(ClientWorkspace.workspace_name).all()
    return {
        "permissions": sorted(CLIENT_COMMAND_PERMISSIONS),
        "safety": client_command_safety_rules(),
        "workspaces": [workspace_public(workspace) for workspace in workspaces],
    }


def workspace_detail(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    roles = (
        session.query(ClientWorkspaceRole)
        .filter(ClientWorkspaceRole.workspace_id == workspace_id)
        .order_by(ClientWorkspaceRole.role_name)
        .all()
    )
    members = (
        session.query(ClientWorkspaceMember)
        .filter(ClientWorkspaceMember.workspace_id == workspace_id)
        .order_by(ClientWorkspaceMember.member_name)
        .all()
    )
    leads = (
        session.query(ClientLeadProfile)
        .filter(ClientLeadProfile.workspace_id == workspace_id)
        .order_by(ClientLeadProfile.created_at)
        .all()
    )
    return {
        "workspace": workspace_public(workspace),
        "roles": [role_public(role) for role in roles],
        "members": [member_public(member) for member in members],
        "lead_count": len(leads),
        "hot_lead_count": len(
            [
                score
                for score in _scores_for_workspace(session, workspace_id)
                if score.final_priority_score >= 78
            ]
        ),
        "safety": client_command_safety_rules(),
    }


def leads_for_workspace(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    leads = (
        session.query(ClientLeadProfile)
        .filter(ClientLeadProfile.workspace_id == workspace_id)
        .order_by(ClientLeadProfile.created_at)
        .all()
    )
    return {
        "workspace_id": workspace_id,
        "leads": [lead_card(session, lead) for lead in leads],
        "safety": client_command_safety_rules(),
    }


def list_leads(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientLeadProfile)
    if workspace_id:
        query = query.filter(ClientLeadProfile.workspace_id == workspace_id)
    leads = query.order_by(ClientLeadProfile.workspace_id, ClientLeadProfile.created_at).all()
    return {
        "workspace_id": workspace_id,
        "leads": [lead_card(session, lead) for lead in leads],
        "safety": client_command_safety_rules(),
    }


def lead_detail(session: Session, lead_id: str, workspace_id: str | None = None) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    score = ensure_score(session, lead)
    brief = ensure_acquisition_brief(session, lead)
    plan = ensure_question_plan(session, lead)
    ensure_objection_drafts(session, lead)
    ensure_follow_up_drafts(session, lead)
    readiness = ensure_appointment_readiness(session, lead)
    packet = ensure_evidence_packet(session, lead)
    review = ensure_underwriting_review(session, lead, packet)
    gate = ensure_offer_readiness(session, lead, packet, review)
    buyer_matches = ensure_buyer_matches(session, lead)
    disposition_gate = ensure_disposition_readiness(session, lead)
    outreach_drafts = ensure_buyer_outreach_drafts(session, lead)
    safe_contacts = ensure_safe_contact_statuses_for_lead(session, lead)
    return {
        "lead": lead_public(lead),
        "score": score_public(score),
        "missing_data": [
            missing_item_public(item)
            for item in _missing_items(session, lead.workspace_id, lead.id)
        ],
        "next_actions": [
            action_public(action)
            for action in _next_actions(session, lead.workspace_id, lead.id)
        ],
        "division_events": [
            event_public(event)
            for event in _division_events(session, lead.workspace_id, lead.id)
        ],
        "acquisition": {
            "brief": acquisition_brief_public(brief),
            "question_plan": question_plan_public(plan),
            "questions": [
                seller_question_public(question)
                for question in _seller_questions(session, lead.workspace_id, lead.id, plan.id)
            ],
            "objection_drafts": [
                objection_draft_public(draft)
                for draft in _objection_drafts(session, lead.workspace_id, lead.id)
            ],
            "follow_up_drafts": [
                follow_up_draft_public(draft)
                for draft in _follow_up_drafts(session, lead.workspace_id, lead.id)
            ],
            "appointment_readiness": appointment_readiness_public(readiness),
            "division_events": [
                acquisition_event_public(event)
                for event in _acquisition_events(session, lead.workspace_id, lead.id)
            ],
        },
        "underwriting": {
            "evidence_packet": evidence_packet_public(packet),
            "evidence_items": [
                evidence_item_public(item)
                for item in _evidence_items(session, lead.workspace_id, lead.id, packet.id)
            ],
            "underwriting_review": underwriting_review_public(review),
            "offer_scenarios": [
                offer_scenario_public(scenario)
                for scenario in _offer_scenarios(session, lead.workspace_id, lead.id, review.id)
            ],
            "offer_readiness": offer_readiness_public(gate),
            "division_events": [
                underwriting_event_public(event)
                for event in _underwriting_events(session, lead.workspace_id, lead.id)
            ],
        },
        "disposition": {
            "buyer_matches": [deal_buyer_match_public(match) for match in buyer_matches],
            "buyer_demand_evidence": [
                buyer_demand_evidence_public(item)
                for item in _buyer_demand_evidence(session, lead.workspace_id, lead.id)
            ],
            "disposition_readiness": disposition_readiness_public(disposition_gate),
            "buyer_outreach_drafts": [buyer_outreach_draft_public(draft) for draft in outreach_drafts],
            "division_events": [
                disposition_event_public(event)
                for event in _disposition_events(session, lead.workspace_id, lead.id)
            ],
        },
        "compliance": {
            "consent_records": [
                consent_record_public(record)
                for record in _consent_records(session, lead.workspace_id, lead.id, None)
            ],
            "opt_out_records": [
                opt_out_record_public(record)
                for record in _opt_out_records(session, lead.workspace_id, lead.id, None)
            ],
            "safe_contact_statuses": [safe_contact_status_public(status) for status in safe_contacts],
            "message_risk_reviews": [
                message_risk_review_public(review)
                for review in _message_risk_reviews(session, lead.workspace_id, lead.id, None)
            ],
            "communication_gates": [
                communication_approval_gate_public(gate)
                for gate in _communication_gates(session, lead.workspace_id, lead.id, None)
            ],
            "division_events": [
                compliance_event_public(event)
                for event in _compliance_events(session, lead.workspace_id, lead.id, None)
            ],
        },
        "safety": client_command_safety_rules(),
    }


def score_lead(session: Session, lead_id: str, workspace_id: str | None = None) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    score = ensure_score(session, lead, refresh=True)
    return {
        "lead": lead_public(lead),
        "score": score_public(score),
        "missing_data": [
            missing_item_public(item)
            for item in _missing_items(session, lead.workspace_id, lead.id)
        ],
        "next_action": action_public(_ensure_next_action(session, lead, score)),
        "safety": client_command_safety_rules(),
    }


def hot_board(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientLeadIntelligenceScore)
    if workspace_id:
        query = query.filter(ClientLeadIntelligenceScore.workspace_id == workspace_id)
    scores = query.order_by(desc(ClientLeadIntelligenceScore.final_priority_score)).all()
    hot_scores = [score for score in scores if score.final_priority_score >= 70]
    return {
        "workspace_id": workspace_id,
        "hot_leads": [
            {
                "lead": lead_public(_lead_or_404(session, score.lead_id, score.workspace_id)),
                "score": score_public(score),
            }
            for score in hot_scores
        ],
        "safety": client_command_safety_rules(),
    }


def next_actions(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientLeadNextBestAction)
    if workspace_id:
        query = query.filter(ClientLeadNextBestAction.workspace_id == workspace_id)
    actions = query.order_by(desc(ClientLeadNextBestAction.priority)).all()
    return {
        "workspace_id": workspace_id,
        "next_actions": [action_public(action) for action in actions],
        "outbound_provider_actions_allowed": False,
        "safety": client_command_safety_rules(),
    }


def lead_card(session: Session, lead: ClientLeadProfile) -> dict[str, object]:
    score = ensure_score(session, lead)
    return {
        "lead": lead_public(lead),
        "score": score_public(score),
        "missing_data_count": len(missing_fields(lead)),
        "recommended_next_action": score.recommended_next_action,
        "requires_human_review": score.requires_human_review,
    }


def ensure_score(
    session: Session,
    lead: ClientLeadProfile,
    refresh: bool = False,
) -> ClientLeadIntelligenceScore:
    score = (
        session.query(ClientLeadIntelligenceScore)
        .filter(ClientLeadIntelligenceScore.lead_id == lead.id)
        .first()
    )
    values = score_client_lead(lead)
    if score is None:
        score = ClientLeadIntelligenceScore(
            id=f"client-score-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
        )
        session.add(score)
    if refresh or score.final_priority_score == 0:
        for key, value in values.items():
            if key != "missing_fields":
                setattr(score, key, value)
        score.client_safe = True
        _sync_missing_items(session, lead, values["missing_fields"])
        _ensure_next_action(session, lead, score)
        _ensure_division_event(session, lead, score)
        session.flush()
    return score


def acquisition_brief_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    brief = ensure_acquisition_brief(session, lead, refresh=refresh)
    return {"lead": lead_public(lead), "brief": acquisition_brief_public(brief), "safety": client_command_safety_rules()}


def question_plan_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    plan = ensure_question_plan(session, lead, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "question_plan": question_plan_public(plan),
        "questions": [
            seller_question_public(question)
            for question in _seller_questions(session, lead.workspace_id, lead.id, plan.id)
        ],
        "safety": client_command_safety_rules(),
    }


def objection_drafts_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    drafts = ensure_objection_drafts(session, lead, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "objection_drafts": [objection_draft_public(draft) for draft in drafts],
        "safety": client_command_safety_rules(),
    }


def follow_up_drafts_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    drafts = ensure_follow_up_drafts(session, lead, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "follow_up_drafts": [follow_up_draft_public(draft) for draft in drafts],
        "outbound_provider_actions_allowed": False,
        "safety": client_command_safety_rules(),
    }


def appointment_readiness_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    review = ensure_appointment_readiness(session, lead, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "appointment_readiness": appointment_readiness_public(review),
        "safety": client_command_safety_rules(),
    }


def acquisition_briefs(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientAcquisitionBrief)
    if workspace_id:
        query = query.filter(ClientAcquisitionBrief.workspace_id == workspace_id)
    briefs = query.order_by(desc(ClientAcquisitionBrief.updated_at)).all()
    return {
        "workspace_id": workspace_id,
        "briefs": [acquisition_brief_public(brief) for brief in briefs],
        "safety": client_command_safety_rules(),
    }


def acquisition_needs_review(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientAppointmentReadinessReview).filter(
        ClientAppointmentReadinessReview.requires_human_review.is_(True)
    )
    if workspace_id:
        query = query.filter(ClientAppointmentReadinessReview.workspace_id == workspace_id)
    reviews = query.order_by(ClientAppointmentReadinessReview.readiness_score).all()
    return {
        "workspace_id": workspace_id,
        "needs_review": [appointment_readiness_public(review) for review in reviews],
        "safety": client_command_safety_rules(),
    }


def evidence_packet_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    packet = ensure_evidence_packet(session, lead, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "evidence_packet": evidence_packet_public(packet),
        "evidence_items": [
            evidence_item_public(item)
            for item in _evidence_items(session, lead.workspace_id, lead.id, packet.id)
        ],
        "safety": client_command_safety_rules(),
    }


def evidence_items_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    packet = ensure_evidence_packet(session, lead, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "packet_id": packet.id,
        "evidence_items": [
            evidence_item_public(item)
            for item in _evidence_items(session, lead.workspace_id, lead.id, packet.id)
        ],
        "safety": client_command_safety_rules(),
    }


def underwriting_review_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    packet = ensure_evidence_packet(session, lead)
    review = ensure_underwriting_review(session, lead, packet, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "evidence_packet": evidence_packet_public(packet),
        "underwriting_review": underwriting_review_public(review),
        "offer_scenarios": [
            offer_scenario_public(scenario)
            for scenario in _offer_scenarios(session, lead.workspace_id, lead.id, review.id)
        ],
        "safety": client_command_safety_rules(),
    }


def offer_readiness_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    packet = ensure_evidence_packet(session, lead)
    review = ensure_underwriting_review(session, lead, packet)
    gate = ensure_offer_readiness(session, lead, packet, review, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "offer_readiness": offer_readiness_public(gate),
        "decision_support_only": True,
        "safety": client_command_safety_rules(),
    }


def underwriting_ready_review(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientOfferReadinessGate).filter(
        ClientOfferReadinessGate.readiness_status == "ready_for_client_review"
    )
    if workspace_id:
        query = query.filter(ClientOfferReadinessGate.workspace_id == workspace_id)
    gates = query.order_by(desc(ClientOfferReadinessGate.readiness_score)).all()
    return {
        "workspace_id": workspace_id,
        "ready_review": [offer_readiness_public(gate) for gate in gates],
        "safety": client_command_safety_rules(),
    }


def underwriting_blocked(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientOfferReadinessGate).filter(
        ClientOfferReadinessGate.readiness_status.in_(["blocked", "evidence_missing", "underwriting_review_needed"])
    )
    if workspace_id:
        query = query.filter(ClientOfferReadinessGate.workspace_id == workspace_id)
    gates = query.order_by(ClientOfferReadinessGate.readiness_score).all()
    return {
        "workspace_id": workspace_id,
        "blocked": [offer_readiness_public(gate) for gate in gates],
        "safety": client_command_safety_rules(),
    }


def underwriting_needs_human_review(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientOfferReadinessGate).filter(
        ClientOfferReadinessGate.requires_human_review.is_(True)
    )
    if workspace_id:
        query = query.filter(ClientOfferReadinessGate.workspace_id == workspace_id)
    gates = query.order_by(ClientOfferReadinessGate.readiness_score).all()
    return {
        "workspace_id": workspace_id,
        "needs_human_review": [offer_readiness_public(gate) for gate in gates],
        "safety": client_command_safety_rules(),
    }


def create_buyer_profile(
    session: Session,
    workspace_id: str,
    values: dict[str, object] | None = None,
) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    values = values or {}
    buyer = ClientBuyerProfile(
        id=f"client-buyer-{uuid4().hex[:10]}",
        workspace_id=workspace_id,
        buyer_name=str(values.get("buyer_name") or "Manual Buyer"),
        buyer_company=values.get("buyer_company") if values.get("buyer_company") else None,
        buyer_type=str(values.get("buyer_type") or "unknown"),
        primary_market=str(values.get("primary_market") or ""),
        target_zip_codes=list(values.get("target_zip_codes") or []),
        preferred_property_types=list(values.get("preferred_property_types") or []),
        min_price=values.get("min_price") if values.get("min_price") is not None else None,
        max_price=values.get("max_price") if values.get("max_price") is not None else None,
        rehab_tolerance=str(values.get("rehab_tolerance") or "unknown"),
        close_speed=str(values.get("close_speed") or "unknown"),
        funding_status=str(values.get("funding_status") or "unknown"),
        proof_of_funds_status=str(values.get("proof_of_funds_status") or "missing"),
        communication_preference=str(values.get("communication_preference") or "unknown"),
        active_status=str(values.get("active_status") or "needs_review"),
        notes_summary=str(values.get("notes_summary") or ""),
        client_safe_summary="Client-entered buyer profile only; no provider lookup occurred.",
    )
    session.add(buyer)
    session.flush()
    return {"buyer": buyer_profile_public(buyer), "safety": client_command_safety_rules()}


def workspace_buyers(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    buyers = (
        session.query(ClientBuyerProfile)
        .filter(ClientBuyerProfile.workspace_id == workspace_id)
        .order_by(ClientBuyerProfile.buyer_name)
        .all()
    )
    return {
        "workspace_id": workspace_id,
        "buyers": [
            {
                "buyer": buyer_profile_public(buyer),
                "confidence": buyer_confidence_public(ensure_buyer_confidence(session, buyer)),
                "buy_boxes": [
                    buyer_buy_box_public(box)
                    for box in _buyer_buy_boxes(session, buyer.workspace_id, buyer.id)
                ],
            }
            for buyer in buyers
        ],
        "safety": client_command_safety_rules(),
    }


def buyer_detail(session: Session, buyer_id: str, workspace_id: str | None = None) -> dict[str, object]:
    buyer = _buyer_or_404(session, buyer_id, workspace_id)
    return {
        "buyer": buyer_profile_public(buyer),
        "confidence": buyer_confidence_public(ensure_buyer_confidence(session, buyer)),
        "buy_boxes": [
            buyer_buy_box_public(box)
            for box in _buyer_buy_boxes(session, buyer.workspace_id, buyer.id)
        ],
        "matches": [
            deal_buyer_match_public(match)
            for match in _buyer_matches_for_buyer(session, buyer.workspace_id, buyer.id)
        ],
        "compliance": {
            "consent_records": [
                consent_record_public(record)
                for record in _consent_records(session, buyer.workspace_id, None, buyer.id)
            ],
            "opt_out_records": [
                opt_out_record_public(record)
                for record in _opt_out_records(session, buyer.workspace_id, None, buyer.id)
            ],
            "safe_contact_statuses": [
                safe_contact_status_public(status)
                for status in ensure_safe_contact_statuses_for_buyer(session, buyer)
            ],
        },
        "safety": client_command_safety_rules(),
    }


def buyer_confidence_for_buyer(
    session: Session,
    buyer_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    buyer = _buyer_or_404(session, buyer_id, workspace_id)
    score = ensure_buyer_confidence(session, buyer, refresh=refresh)
    return {
        "buyer": buyer_profile_public(buyer),
        "confidence": buyer_confidence_public(score),
        "safety": client_command_safety_rules(),
    }


def create_buyer_buy_box(
    session: Session,
    buyer_id: str,
    values: dict[str, object] | None = None,
) -> dict[str, object]:
    buyer = _buyer_or_404(session, buyer_id)
    values = values or {}
    buy_box = ClientBuyerBuyBox(
        id=f"client-buy-box-{uuid4().hex[:10]}",
        workspace_id=buyer.workspace_id,
        buyer_id=buyer.id,
        market=str(values.get("market") or buyer.primary_market),
        zip_codes=list(values.get("zip_codes") or buyer.target_zip_codes or []),
        property_types=list(values.get("property_types") or buyer.preferred_property_types or []),
        min_beds=values.get("min_beds") if values.get("min_beds") is not None else None,
        min_baths=values.get("min_baths") if values.get("min_baths") is not None else None,
        min_sqft=values.get("min_sqft") if values.get("min_sqft") is not None else None,
        max_purchase_price=values.get("max_purchase_price") if values.get("max_purchase_price") is not None else buyer.max_price,
        min_purchase_price=values.get("min_purchase_price") if values.get("min_purchase_price") is not None else buyer.min_price,
        rehab_level=str(values.get("rehab_level") or buyer.rehab_tolerance or "unknown"),
        occupancy_preference=str(values.get("occupancy_preference") or "unknown"),
        deal_type_preference=str(values.get("deal_type_preference") or "unknown"),
        notes_summary=str(values.get("notes_summary") or ""),
        client_safe=True,
    )
    session.add(buy_box)
    session.flush()
    ensure_buyer_confidence(session, buyer, refresh=True)
    return {"buy_box": buyer_buy_box_public(buy_box), "safety": client_command_safety_rules()}


def buyer_buy_boxes_for_buyer(session: Session, buyer_id: str, workspace_id: str | None = None) -> dict[str, object]:
    buyer = _buyer_or_404(session, buyer_id, workspace_id)
    return {
        "buyer": buyer_profile_public(buyer),
        "buy_boxes": [buyer_buy_box_public(box) for box in _buyer_buy_boxes(session, buyer.workspace_id, buyer.id)],
        "safety": client_command_safety_rules(),
    }


def buyer_matches_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    matches = ensure_buyer_matches(session, lead, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "buyer_matches": [deal_buyer_match_public(match) for match in matches],
        "safety": client_command_safety_rules(),
    }


def disposition_matches(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientDealBuyerMatch)
    if workspace_id:
        query = query.filter(ClientDealBuyerMatch.workspace_id == workspace_id)
    matches = query.order_by(desc(ClientDealBuyerMatch.match_score)).all()
    return {"workspace_id": workspace_id, "matches": [deal_buyer_match_public(match) for match in matches], "safety": client_command_safety_rules()}


def disposition_strong_matches(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientDealBuyerMatch).filter(ClientDealBuyerMatch.match_status == "strong_match")
    if workspace_id:
        query = query.filter(ClientDealBuyerMatch.workspace_id == workspace_id)
    matches = query.order_by(desc(ClientDealBuyerMatch.match_score)).all()
    return {"workspace_id": workspace_id, "strong_matches": [deal_buyer_match_public(match) for match in matches], "safety": client_command_safety_rules()}


def disposition_needs_review(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientDispositionReadinessGate).filter(ClientDispositionReadinessGate.requires_human_review.is_(True))
    if workspace_id:
        query = query.filter(ClientDispositionReadinessGate.workspace_id == workspace_id)
    gates = query.order_by(ClientDispositionReadinessGate.readiness_score).all()
    return {"workspace_id": workspace_id, "needs_review": [disposition_readiness_public(gate) for gate in gates], "safety": client_command_safety_rules()}


def create_buyer_demand_evidence(
    session: Session,
    lead_id: str,
    values: dict[str, object] | None = None,
    workspace_id: str | None = None,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    values = values or {}
    buyer_id = values.get("buyer_id") if values.get("buyer_id") else None
    if buyer_id:
        _buyer_or_404(session, str(buyer_id), lead.workspace_id)
    evidence = ClientBuyerDemandEvidence(
        id=f"client-buyer-demand-{uuid4().hex[:10]}",
        workspace_id=lead.workspace_id,
        lead_id=lead.id,
        buyer_id=str(buyer_id) if buyer_id else None,
        evidence_type=str(values.get("evidence_type") or "manual_client_note"),
        evidence_summary=str(values.get("evidence_summary") or "Manual buyer demand evidence added for review."),
        source_type=str(values.get("source_type") or "manual"),
        confidence_level=str(values.get("confidence_level") or "medium"),
        client_safe=True,
        internal_notes="Hidden manual evidence note.",
    )
    session.add(evidence)
    session.flush()
    ensure_disposition_readiness(session, lead, refresh=True)
    return {"buyer_demand_evidence": buyer_demand_evidence_public(evidence), "safety": client_command_safety_rules()}


def buyer_demand_evidence_for_lead(session: Session, lead_id: str, workspace_id: str | None = None) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    return {
        "lead": lead_public(lead),
        "buyer_demand_evidence": [
            buyer_demand_evidence_public(evidence)
            for evidence in _buyer_demand_evidence(session, lead.workspace_id, lead.id)
        ],
        "safety": client_command_safety_rules(),
    }


def disposition_readiness_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    gate = ensure_disposition_readiness(session, lead, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "disposition_readiness": disposition_readiness_public(gate),
        "decision_support_only": True,
        "safety": client_command_safety_rules(),
    }


def disposition_ready_review(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientDispositionReadinessGate).filter(ClientDispositionReadinessGate.readiness_status == "ready_for_client_review")
    if workspace_id:
        query = query.filter(ClientDispositionReadinessGate.workspace_id == workspace_id)
    gates = query.order_by(desc(ClientDispositionReadinessGate.readiness_score)).all()
    return {"workspace_id": workspace_id, "ready_review": [disposition_readiness_public(gate) for gate in gates], "safety": client_command_safety_rules()}


def disposition_blocked(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientDispositionReadinessGate).filter(ClientDispositionReadinessGate.readiness_status.in_(["blocked", "buyer_demand_missing", "buyer_match_needed", "offer_readiness_blocked", "not_ready"]))
    if workspace_id:
        query = query.filter(ClientDispositionReadinessGate.workspace_id == workspace_id)
    gates = query.order_by(ClientDispositionReadinessGate.readiness_score).all()
    return {"workspace_id": workspace_id, "blocked": [disposition_readiness_public(gate) for gate in gates], "safety": client_command_safety_rules()}


def buyer_outreach_drafts_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
    values: dict[str, object] | None = None,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    drafts = ensure_buyer_outreach_drafts(session, lead, refresh=refresh, values=values)
    return {
        "lead": lead_public(lead),
        "buyer_outreach_drafts": [buyer_outreach_draft_public(draft) for draft in drafts],
        "buyer_contacted": False,
        "campaign_started": False,
        "safety": client_command_safety_rules(),
    }


def ensure_acquisition_brief(
    session: Session,
    lead: ClientLeadProfile,
    refresh: bool = False,
) -> ClientAcquisitionBrief:
    score = ensure_score(session, lead)
    missing = _missing_items(session, lead.workspace_id, lead.id)
    brief = (
        session.query(ClientAcquisitionBrief)
        .filter(ClientAcquisitionBrief.lead_id == lead.id)
        .first()
    )
    if brief is None:
        brief = ClientAcquisitionBrief(
            id=f"client-acq-brief-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
        )
        session.add(brief)
    if refresh or not brief.seller_summary:
        signals = ", ".join(lead.motivation_signals or []) or "motivation not confirmed"
        channels = ", ".join(lead.contact_channels_present or []) or "contact channel missing"
        brief.seller_summary = f"{lead.display_name} in {lead.property_city or 'unknown market'} with {signals}."
        brief.lead_priority_snapshot = {
            "final_priority_score": score.final_priority_score,
            "recommended_next_action": score.recommended_next_action,
            "missing_data_count": len([item for item in missing if item.resolution_status == "open"]),
        }
        brief.motivation_hypothesis = (
            "Likely motivated by " + signals
            if lead.motivation_signals
            else "Motivation is unconfirmed; ask open discovery questions first."
        )
        brief.urgency_hypothesis = (
            "Timeline signal is strong; confirm whether the seller has a specific date."
            if score.urgency_score >= 70
            else "Timeline is not yet strong enough for appointment pressure; keep tone exploratory."
        )
        brief.property_context_summary = (
            f"{lead.property_type or 'Property type unknown'} in {lead.property_address_summary or 'address missing'}; "
            f"estimated value signal {lead.estimated_value or 0} and equity signal {lead.estimated_equity_percent or 0}%."
        )
        brief.recommended_call_objective = _acquisition_objective(score, missing)
        brief.suggested_opening_angle = (
            "Open with a calm property check-in and ask what the seller would like to do next."
        )
        brief.top_questions_to_ask_summary = _question_summary(lead, missing)
        brief.sensitive_topics_to_avoid = [
            "Do not pressure the seller.",
            "Do not imply a legal conclusion.",
            "Do not claim buyer demand or pricing certainty without evidence.",
        ]
        brief.suggested_tone = "calm, curious, respectful"
        brief.confidence_level = score.confidence_level
        brief.requires_human_review = score.requires_human_review or len(missing) >= 3
        brief.manager_name = "Acquisition Manager"
        brief.source_basis_summary = "Built from CP2 lead score, lead profile fields, and missing-data checklist."
        brief.client_safe_summary = (
            f"Prepare a manual seller conversation using {channels}; no outbound action is performed."
        )
        _ensure_acquisition_event(session, lead, "acquisition_brief", "Acquisition Manager prepared a client-safe call brief.")
        session.flush()
    return brief


def ensure_question_plan(
    session: Session,
    lead: ClientLeadProfile,
    refresh: bool = False,
) -> ClientSellerQuestionPlan:
    missing = _missing_items(session, lead.workspace_id, lead.id)
    plan = (
        session.query(ClientSellerQuestionPlan)
        .filter(ClientSellerQuestionPlan.lead_id == lead.id)
        .first()
    )
    if plan is None:
        plan = ClientSellerQuestionPlan(
            id=f"client-question-plan-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
        )
        session.add(plan)
    existing = _seller_questions(session, lead.workspace_id, lead.id, plan.id)
    if refresh or not existing:
        if existing:
            session.query(ClientSellerQuestion).filter(
                ClientSellerQuestion.question_plan_id == plan.id
            ).delete(synchronize_session=False)
        questions = _build_questions(lead, missing)
        for question in questions:
            session.add(
                ClientSellerQuestion(
                    id=f"client-question-{uuid4().hex[:10]}",
                    question_plan_id=plan.id,
                    workspace_id=lead.workspace_id,
                    lead_id=lead.id,
                    **question,
                )
            )
        plan.total_questions = len(questions)
        plan.high_priority_count = len([question for question in questions if question["priority"] == "high"])
        plan.missing_data_focus_count = len([question for question in questions if question.get("tied_missing_data_key")])
        plan.plan_status = "needs_review" if plan.high_priority_count >= 4 else "ready_for_manual_use"
        plan.client_safe_summary = "Question plan is manual-use only and is based on CP2 missing-data signals."
        _ensure_acquisition_event(session, lead, "question_plan", "Acquisition Manager prepared seller discovery questions.")
        session.flush()
    return plan


def ensure_objection_drafts(
    session: Session,
    lead: ClientLeadProfile,
    refresh: bool = False,
) -> list[ClientObjectionResponseDraft]:
    existing = _objection_drafts(session, lead.workspace_id, lead.id)
    if refresh and existing:
        session.query(ClientObjectionResponseDraft).filter(
            ClientObjectionResponseDraft.lead_id == lead.id
        ).delete(synchronize_session=False)
        existing = []
    if not existing:
        drafts = [
            (
                "price_too_low",
                "The number feels lower than expected.",
                "I understand. My goal is to be transparent about the repairs, timeline, and as-is purchase assumptions. If your target number is different, I can note it and compare it against the property facts before any next step.",
                "medium",
            ),
            (
                "needs_time",
                "I need more time to think.",
                "That makes sense. I can summarize what we discussed and note a follow-up date that works for you. Nothing is final from this conversation.",
                "low",
            ),
            (
                "trust_concern",
                "How do I know this is legitimate?",
                "Fair question. You should review any paperwork with qualified title or legal professionals. I can keep the next step simple and provide a clear summary for manual review.",
                "medium",
            ),
        ]
        for objection_type, objection, response, risk_level in drafts:
            safety = validate_client_safe_text(response)
            existing.append(
                ClientObjectionResponseDraft(
                    id=f"client-objection-{uuid4().hex[:10]}",
                    workspace_id=lead.workspace_id,
                    lead_id=lead.id,
                    objection_type=objection_type,
                    seller_objection=objection,
                    suggested_response=response,
                    risk_level="high" if not safety["allowed"] else risk_level,
                    requires_human_review=not safety["allowed"] or risk_level != "low",
                    client_safe=bool(safety["allowed"]),
                    manual_use_only=True,
                )
            )
            session.add(existing[-1])
        _ensure_acquisition_event(session, lead, "objection_drafts", "Acquisition Manager prepared manual-use objection responses.")
        session.flush()
    return _objection_drafts(session, lead.workspace_id, lead.id)


def ensure_follow_up_drafts(
    session: Session,
    lead: ClientLeadProfile,
    refresh: bool = False,
) -> list[ClientFollowUpDraft]:
    existing = _follow_up_drafts(session, lead.workspace_id, lead.id)
    if refresh and existing:
        session.query(ClientFollowUpDraft).filter(ClientFollowUpDraft.lead_id == lead.id).delete(
            synchronize_session=False
        )
        existing = []
    if not existing:
        draft_values = [
            (
                "sms_draft",
                "Manual note: follow up about the property and ask whether the seller still wants to talk through options.",
                "simple seller check-in",
            ),
            (
                "email_draft",
                "Manual note: summarize the property questions, timeline, and next step for seller review.",
                "conversation recap",
            ),
            (
                "call_note",
                "Manual note: ask motivation, timeline, condition, price expectation, and decision-maker status before any offer review.",
                "call preparation",
            ),
        ]
        for channel_type, draft_body, purpose in draft_values:
            safety = validate_client_safe_text(draft_body)
            existing.append(
                ClientFollowUpDraft(
                    id=f"client-follow-up-{uuid4().hex[:10]}",
                    workspace_id=lead.workspace_id,
                    lead_id=lead.id,
                    channel_type=channel_type,
                    draft_body=draft_body,
                    purpose=purpose,
                    risk_level="high" if not safety["allowed"] else "low",
                    approval_status="needs_review" if not safety["allowed"] else "draft_only",
                    manual_use_only=True,
                    no_live_send=True,
                    unsafe_language_flag=not safety["allowed"],
                )
            )
            session.add(existing[-1])
        _ensure_acquisition_event(session, lead, "follow_up_drafts", "Acquisition Manager queued manual-use follow-up drafts.")
        session.flush()
    return _follow_up_drafts(session, lead.workspace_id, lead.id)


def ensure_appointment_readiness(
    session: Session,
    lead: ClientLeadProfile,
    refresh: bool = False,
) -> ClientAppointmentReadinessReview:
    score = ensure_score(session, lead)
    review = (
        session.query(ClientAppointmentReadinessReview)
        .filter(ClientAppointmentReadinessReview.lead_id == lead.id)
        .first()
    )
    if review is None:
        review = ClientAppointmentReadinessReview(
            id=f"client-appt-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
        )
        session.add(review)
    if refresh or review.readiness_score == 0:
        missing = _appointment_missing_requirements(lead, score)
        score_value = max(0, min(100, 100 - len(missing) * 14 - max(0, 70 - score.missing_data_score)))
        review.readiness_score = score_value
        review.appointment_ready = score_value >= 72 and not lead.dnc_flag
        review.missing_requirements = missing
        review.recommended_next_step = (
            "Use the manual call plan and confirm appointment logistics."
            if review.appointment_ready
            else "Complete missing seller context before appointment readiness."
        )
        review.reason_summary = f"{len(missing)} appointment requirements need review."
        review.confidence_level = "high" if score_value >= 80 else "medium" if score_value >= 55 else "low"
        review.requires_human_review = not review.appointment_ready or len(missing) > 0
        _ensure_acquisition_event(session, lead, "appointment_readiness", "Acquisition Manager reviewed appointment readiness.")
        session.flush()
    return review


def ensure_evidence_packet(
    session: Session,
    lead: ClientLeadProfile,
    refresh: bool = False,
) -> ClientDealEvidencePacket:
    packet = (
        session.query(ClientDealEvidencePacket)
        .filter(ClientDealEvidencePacket.lead_id == lead.id)
        .first()
    )
    if packet is None:
        packet = ClientDealEvidencePacket(
            id=f"client-evidence-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
        )
        session.add(packet)
    existing = _evidence_items(session, lead.workspace_id, lead.id, packet.id)
    if refresh and existing:
        session.query(ClientDealEvidenceItem).filter(ClientDealEvidenceItem.packet_id == packet.id).delete(
            synchronize_session=False
        )
        existing = []
    if not existing:
        for item in _default_evidence_items(lead):
            session.add(
                ClientDealEvidenceItem(
                    id=f"client-evidence-item-{uuid4().hex[:10]}",
                    workspace_id=lead.workspace_id,
                    lead_id=lead.id,
                    packet_id=packet.id,
                    **item,
                )
            )
    missing = _missing_evidence_types(_evidence_items(session, lead.workspace_id, lead.id, packet.id))
    packet.property_address = lead.property_address_summary
    packet.seller_motivation_summary = ", ".join(lead.motivation_signals or []) or "Seller motivation not confirmed."
    packet.property_condition_summary = _condition_summary(lead)
    packet.occupancy_status = "vacancy signal" if "vacant_signal" in (lead.distress_signals or []) else "occupancy not confirmed"
    packet.title_status_summary = "Title status not externally verified; client must use qualified review."
    packet.evidence_status = "ready_for_underwriting" if not missing else "missing_evidence"
    packet.missing_evidence_count = len(missing)
    packet.required_evidence_summary = missing
    packet.confidence_level = "high" if not missing else "medium" if len(missing) <= 2 else "low"
    packet.requires_human_review = bool(missing)
    packet.client_safe_summary = "Evidence packet uses manual/demo records only and does not call property, title, tax, or MLS providers."
    _ensure_underwriting_event(session, lead, "evidence_packet", "Underwriting Manager prepared a client-safe evidence packet.")
    session.flush()
    return packet


def ensure_underwriting_review(
    session: Session,
    lead: ClientLeadProfile,
    packet: ClientDealEvidencePacket,
    refresh: bool = False,
) -> ClientUnderwritingReview:
    review = (
        session.query(ClientUnderwritingReview)
        .filter(ClientUnderwritingReview.lead_id == lead.id)
        .first()
    )
    if review is None:
        review = ClientUnderwritingReview(
            id=f"client-underwriting-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
            packet_id=packet.id,
        )
        session.add(review)
    if refresh or (review.arv_estimate is None and review.repair_estimate is None):
        inputs = _manual_underwriting_inputs(lead)
        review.packet_id = packet.id
        review.arv_estimate = inputs.get("arv_estimate")
        review.repair_estimate = inputs.get("repair_estimate")
        review.holding_cost_estimate = inputs.get("holding_cost_estimate")
        review.desired_assignment_fee = inputs.get("desired_assignment_fee")
        missing = []
        if review.arv_estimate is None:
            missing.append("arv_estimate")
        if review.repair_estimate is None:
            missing.append("repair_estimate")
        if review.holding_cost_estimate is None:
            missing.append("holding_cost_estimate")
        if review.desired_assignment_fee is None:
            missing.append("desired_assignment_fee")
        review.missing_data_summary = missing
        if missing:
            review.max_allowable_offer = None
            review.conservative_offer = None
            review.standard_offer = None
            review.aggressive_offer = None
            review.margin_warning = True
            review.confidence_level = "low"
            review.assumptions_summary = "Missing underwriting inputs; no values are invented."
            review.requires_human_review = True
        else:
            mao = int(round((review.arv_estimate or 0) * 0.70 - (review.repair_estimate or 0) - (review.desired_assignment_fee or 0) - (review.holding_cost_estimate or 0)))
            review.max_allowable_offer = mao
            review.conservative_offer = int(round(mao * 0.90))
            review.standard_offer = mao
            review.aggressive_offer = int(round(mao * 1.05))
            review.margin_warning = mao <= 0 or packet.missing_evidence_count > 0
            review.confidence_level = "high" if not review.margin_warning and packet.confidence_level == "high" else "medium"
            review.assumptions_summary = (
                "Formula: ARV * 0.70 - repairs - desired assignment fee - holding costs. "
                "Inputs are manual/demo values and decision support only."
            )
            review.requires_human_review = review.margin_warning
        _sync_offer_scenarios(session, lead, review)
        _ensure_underwriting_event(session, lead, "underwriting_review", "Underwriting Manager completed deterministic offer math review.")
        session.flush()
    return review


def ensure_offer_readiness(
    session: Session,
    lead: ClientLeadProfile,
    packet: ClientDealEvidencePacket,
    review: ClientUnderwritingReview,
    refresh: bool = False,
) -> ClientOfferReadinessGate:
    gate = (
        session.query(ClientOfferReadinessGate)
        .filter(ClientOfferReadinessGate.lead_id == lead.id)
        .first()
    )
    if gate is None:
        gate = ClientOfferReadinessGate(
            id=f"client-offer-gate-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
            packet_id=packet.id,
        )
        session.add(gate)
    if refresh or not gate.recommended_next_step:
        block_reasons: list[str] = []
        risk_flags: list[str] = []
        if packet.missing_evidence_count > 0:
            block_reasons.append("evidence_missing")
        if review.arv_estimate is None:
            block_reasons.append("arv_estimate_missing")
        if review.repair_estimate is None:
            block_reasons.append("repair_estimate_missing")
        if review.max_allowable_offer is None:
            block_reasons.append("underwriting_review_needed")
        if review.max_allowable_offer is not None and review.max_allowable_offer <= 0:
            block_reasons.append("thin_or_negative_offer_margin")
        if lead.dnc_flag:
            risk_flags.append("do_not_contact")
        if lead.legal_question_flag:
            risk_flags.append("legal_review_needed")
        if review.margin_warning:
            risk_flags.append("margin_warning")

        gate.packet_id = packet.id
        gate.underwriting_review_id = review.id
        gate.block_reasons = block_reasons
        gate.risk_flags = risk_flags
        gate.readiness_score = max(0, 100 - len(block_reasons) * 22 - len(risk_flags) * 12)
        if block_reasons:
            gate.readiness_status = "evidence_missing" if "evidence_missing" in block_reasons else "underwriting_review_needed"
        elif risk_flags:
            gate.readiness_status = "blocked"
        else:
            gate.readiness_status = "ready_for_client_review"
        gate.can_present_offer = gate.readiness_status == "ready_for_client_review"
        gate.no_contract_generated = True
        gate.no_offer_sent = True
        gate.requires_human_review = True
        gate.recommended_next_step = (
            "Client can review the decision-support offer range manually."
            if gate.can_present_offer
            else "Resolve evidence, underwriting, or risk blockers before offer review."
        )
        _ensure_underwriting_event(session, lead, "offer_readiness", f"Underwriting Manager set offer readiness to {gate.readiness_status}.")
        session.flush()
    return gate


def ensure_buyer_confidence(
    session: Session,
    buyer: ClientBuyerProfile,
    refresh: bool = False,
) -> ClientBuyerConfidenceScore:
    score = (
        session.query(ClientBuyerConfidenceScore)
        .filter(ClientBuyerConfidenceScore.buyer_id == buyer.id)
        .first()
    )
    if score is None:
        score = ClientBuyerConfidenceScore(
            id=f"client-buyer-confidence-{uuid4().hex[:10]}",
            workspace_id=buyer.workspace_id,
            buyer_id=buyer.id,
        )
        session.add(score)
    if refresh or not score.confidence_score:
        boxes = _buyer_buy_boxes(session, buyer.workspace_id, buyer.id)
        funding = 90 if buyer.proof_of_funds_status == "verified" else 72 if buyer.funding_status in {"verified", "stated"} else 35
        buy_box_clarity = 30
        if buyer.target_zip_codes:
            buy_box_clarity += 18
        if buyer.preferred_property_types:
            buy_box_clarity += 14
        if buyer.max_price:
            buy_box_clarity += 18
        if buyer.rehab_tolerance != "unknown":
            buy_box_clarity += 10
        if boxes:
            buy_box_clarity += 10
        responsiveness = {"fast": 82, "standard": 65, "slow": 42}.get(buyer.close_speed, 35)
        historical = 70 if buyer.active_status == "active" else 45 if buyer.active_status == "needs_review" else 20
        confidence = int(round((funding + min(100, buy_box_clarity) + responsiveness + historical) / 4))
        if buyer.active_status == "inactive":
            confidence = min(confidence, 45)
        score.confidence_score = max(0, min(100, confidence))
        score.responsiveness_score = responsiveness
        score.funding_confidence_score = funding
        score.buy_box_clarity_score = min(100, buy_box_clarity)
        score.historical_interest_score = historical
        score.overall_grade = _buyer_grade(score.confidence_score)
        score.requires_human_review = score.confidence_score < 70 or buyer.proof_of_funds_status in {"missing", "unknown", "unverified"}
        score.reason_summary = (
            f"Funding {buyer.funding_status}/{buyer.proof_of_funds_status}; "
            f"{len(buyer.target_zip_codes or [])} target zips; {len(boxes)} buy boxes; close speed {buyer.close_speed}."
        )
        session.flush()
    return score


def ensure_buyer_matches(
    session: Session,
    lead: ClientLeadProfile,
    refresh: bool = False,
) -> list[ClientDealBuyerMatch]:
    buyers = (
        session.query(ClientBuyerProfile)
        .filter(ClientBuyerProfile.workspace_id == lead.workspace_id)
        .order_by(ClientBuyerProfile.buyer_name)
        .all()
    )
    if refresh:
        session.query(ClientDealBuyerMatch).filter(ClientDealBuyerMatch.lead_id == lead.id).delete(synchronize_session=False)
    existing = {
        match.buyer_id: match
        for match in session.query(ClientDealBuyerMatch).filter(ClientDealBuyerMatch.lead_id == lead.id).all()
    }
    packet = ensure_evidence_packet(session, lead)
    review = ensure_underwriting_review(session, lead, packet)
    offer_gate = ensure_offer_readiness(session, lead, packet, review)
    for buyer in buyers:
        buy_boxes = _buyer_buy_boxes(session, buyer.workspace_id, buyer.id)
        confidence = ensure_buyer_confidence(session, buyer)
        best = _best_buy_box_match(lead, review, buyer, buy_boxes, confidence.confidence_score)
        match = existing.get(buyer.id)
        if match is None:
            match = ClientDealBuyerMatch(
                id=f"client-buyer-match-{uuid4().hex[:10]}",
                workspace_id=lead.workspace_id,
                lead_id=lead.id,
                buyer_id=buyer.id,
            )
            session.add(match)
        match.buy_box_id = best["buy_box_id"]
        match.match_score = best["match_score"]
        match.match_status = best["match_status"]
        match.matched_reasons = best["matched_reasons"]
        match.mismatch_reasons = best["mismatch_reasons"]
        match.price_fit_status = best["price_fit_status"]
        match.market_fit_status = best["market_fit_status"]
        match.property_type_fit_status = best["property_type_fit_status"]
        match.rehab_fit_status = best["rehab_fit_status"]
        match.funding_confidence_snapshot = confidence.funding_confidence_score
        match.buyer_confidence_snapshot = confidence.confidence_score
        match.requires_human_review = best["match_status"] != "strong_match" or confidence.requires_human_review
        match.recommended_next_step = (
            "Review this buyer manually as a CP5 fit candidate."
            if match.match_status in {"strong_match", "possible_match"}
            else "Keep buyer out of disposition readiness until fit improves."
        )
        match.client_safe_summary = "Client-safe deterministic buyer fit only; no buyer has been contacted."
    _ensure_disposition_event(session, lead, None, "buyer_matching", "Disposition Manager refreshed deterministic buyer matches.")
    if offer_gate.readiness_status != "ready_for_client_review":
        _ensure_disposition_event(session, lead, None, "offer_gate_block", "Disposition Manager blocked buyer readiness because CP4 offer readiness is not clear.")
    session.flush()
    return (
        session.query(ClientDealBuyerMatch)
        .filter(ClientDealBuyerMatch.workspace_id == lead.workspace_id, ClientDealBuyerMatch.lead_id == lead.id)
        .order_by(desc(ClientDealBuyerMatch.match_score))
        .all()
    )


def ensure_disposition_readiness(
    session: Session,
    lead: ClientLeadProfile,
    refresh: bool = False,
) -> ClientDispositionReadinessGate:
    gate = (
        session.query(ClientDispositionReadinessGate)
        .filter(ClientDispositionReadinessGate.lead_id == lead.id)
        .first()
    )
    if gate is None:
        gate = ClientDispositionReadinessGate(
            id=f"client-disposition-gate-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
        )
        session.add(gate)
    if refresh or not gate.recommended_next_step:
        packet = ensure_evidence_packet(session, lead)
        review = ensure_underwriting_review(session, lead, packet)
        offer_gate = ensure_offer_readiness(session, lead, packet, review)
        matches = ensure_buyer_matches(session, lead)
        evidence = _buyer_demand_evidence(session, lead.workspace_id, lead.id)
        possible_matches = [match for match in matches if match.match_status in {"strong_match", "possible_match"}]
        strong_matches = [match for match in matches if match.match_status == "strong_match"]
        block_reasons: list[str] = []
        risk_flags: list[str] = []
        if offer_gate.readiness_status != "ready_for_client_review":
            block_reasons.append("offer_readiness_blocked")
        if not matches:
            block_reasons.append("buyer_match_needed")
        if not possible_matches:
            block_reasons.append("strong_or_possible_buyer_match_missing")
        if not evidence and not strong_matches:
            block_reasons.append("buyer_demand_evidence_missing")
        if packet.evidence_status == "missing_evidence" or review.max_allowable_offer is None:
            block_reasons.append("critical_evidence_missing")
        if any(match.requires_human_review for match in possible_matches):
            risk_flags.append("buyer_match_human_review")
        gate.buyer_match_count = len(matches)
        gate.strong_buyer_match_count = len(strong_matches)
        gate.buyer_demand_evidence_count = len(evidence)
        gate.block_reasons = sorted(set(block_reasons))
        gate.risk_flags = sorted(set(risk_flags))
        gate.readiness_score = max(0, min(100, 100 - len(gate.block_reasons) * 22 - len(gate.risk_flags) * 10))
        if "offer_readiness_blocked" in gate.block_reasons:
            gate.readiness_status = "offer_readiness_blocked"
        elif "buyer_demand_evidence_missing" in gate.block_reasons:
            gate.readiness_status = "buyer_demand_missing"
        elif "buyer_match_needed" in gate.block_reasons or "strong_or_possible_buyer_match_missing" in gate.block_reasons:
            gate.readiness_status = "buyer_match_needed"
        elif gate.block_reasons:
            gate.readiness_status = "blocked"
        else:
            gate.readiness_status = "ready_for_client_review"
        gate.can_prepare_buyer_outreach = gate.readiness_status == "ready_for_client_review"
        gate.no_buyer_contacted = True
        gate.no_campaign_started = True
        gate.no_contract_generated = True
        gate.requires_human_review = True
        gate.recommended_next_step = (
            "Review matched buyers and manual-only buyer preview draft."
            if gate.can_prepare_buyer_outreach
            else "Resolve CP4, buyer match, or buyer demand evidence blockers before disposition review."
        )
        gate.client_safe_summary = "Decision support only; no campaign, contract, or buyer outreach has been sent."
        _ensure_disposition_event(session, lead, None, "disposition_readiness", f"Disposition Manager set readiness to {gate.readiness_status}.")
        session.flush()
    return gate


def ensure_buyer_outreach_drafts(
    session: Session,
    lead: ClientLeadProfile,
    refresh: bool = False,
    values: dict[str, object] | None = None,
) -> list[ClientBuyerOutreachDraft]:
    if refresh:
        session.query(ClientBuyerOutreachDraft).filter(ClientBuyerOutreachDraft.lead_id == lead.id).delete(synchronize_session=False)
    drafts = _buyer_outreach_drafts(session, lead.workspace_id, lead.id)
    if not drafts:
        matches = ensure_buyer_matches(session, lead)
        top_match = next((match for match in matches if match.match_status in {"strong_match", "possible_match"}), None)
        body = (
            f"Manual preview note for {lead.property_city or 'the market'} {lead.property_zip or ''}: "
            "share only client-safe property type, high-level price context, and ask whether the buyer wants manual review."
        )
        draft = ClientBuyerOutreachDraft(
            id=f"client-buyer-draft-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
            buyer_id=str((values or {}).get("buyer_id") or (top_match.buyer_id if top_match else "")) or None,
            draft_type=str((values or {}).get("draft_type") or "deal_preview"),
            draft_body=body,
            purpose=str((values or {}).get("purpose") or "manual buyer preview"),
            risk_level="low" if top_match else "medium",
            approval_status="draft_only",
            manual_use_only=True,
            no_live_send=True,
            no_blast=True,
            unsafe_language_flag=False,
        )
        session.add(draft)
        _ensure_disposition_event(session, lead, draft.buyer_id, "buyer_outreach_draft", "Disposition Manager prepared a manual-use buyer draft.")
        session.flush()
    return _buyer_outreach_drafts(session, lead.workspace_id, lead.id)


def require_member_permission(
    session: Session,
    workspace_id: str,
    member_email: str,
    permission: str,
) -> dict[str, object]:
    member = (
        session.query(ClientWorkspaceMember)
        .filter(
            ClientWorkspaceMember.workspace_id == workspace_id,
            ClientWorkspaceMember.member_email == member_email,
        )
        .first()
    )
    role = session.get(ClientWorkspaceRole, member.role_id) if member else None
    if not has_permission(member, role, permission):
        raise ClientCommandPermissionError("member_not_authorized_for_workspace")
    return {
        "member": member_public(member),
        "permissions": member_permissions(member, role),
    }


def _acquisition_objective(
    score: ClientLeadIntelligenceScore,
    missing: list[ClientLeadMissingDataItem],
) -> str:
    if score.recommended_next_action == "complete_missing_data" or missing:
        return "Confirm missing seller, property, and timeline facts before any offer discussion."
    if score.final_priority_score >= 75:
        return "Confirm motivation, timeline, condition, price expectation, and whether a manual appointment makes sense."
    return "Use a respectful discovery call to decide whether the lead should stay in the client queue."


def _question_summary(
    lead: ClientLeadProfile,
    missing: list[ClientLeadMissingDataItem],
) -> str:
    focus = [item.field_name for item in missing if item.resolution_status == "open"][:3]
    if focus:
        return f"Lead has missing data focus: {', '.join(focus)}."
    if lead.asking_price:
        return "Ask seller to explain timeline, property condition, and flexibility around the stated price expectation."
    return "Ask motivation, timeline, condition, price expectation, and decision-maker questions."


def _build_questions(
    lead: ClientLeadProfile,
    missing: list[ClientLeadMissingDataItem],
) -> list[dict[str, object]]:
    missing_fields_by_name = {item.field_name for item in missing if item.resolution_status == "open"}
    questions: list[dict[str, object]] = [
        {
            "question_text": "What has you thinking about selling this property now?",
            "question_category": "motivation",
            "priority": "high" if not lead.motivation_signals else "medium",
            "reason": "Motivation drives whether this lead belongs in the acquisition queue.",
            "tied_missing_data_key": "motivation_signals" if not lead.motivation_signals else None,
            "client_safe": True,
        },
        {
            "question_text": "Is there a specific timeline you are hoping to work around?",
            "question_category": "timeline",
            "priority": "high" if not lead.timeline_days or lead.timeline_days > 90 else "medium",
            "reason": "Timeline clarifies urgency without pressure.",
            "tied_missing_data_key": "timeline_days" if not lead.timeline_days else None,
            "client_safe": True,
        },
        {
            "question_text": "What condition is the property in today, and what repairs are you aware of?",
            "question_category": "condition",
            "priority": "high",
            "reason": "Condition is required before underwriting review.",
            "tied_missing_data_key": "property_condition" if "property_type" in missing_fields_by_name else None,
            "client_safe": True,
        },
        {
            "question_text": "Do you already have a price in mind, or are you looking for a clear as-is number?",
            "question_category": "price_expectation",
            "priority": "high" if not lead.asking_price else "medium",
            "reason": "Price expectation helps compare seller goals against underwriting inputs.",
            "tied_missing_data_key": "asking_price" if not lead.asking_price else None,
            "client_safe": True,
        },
        {
            "question_text": "Is the property currently occupied, vacant, or rented?",
            "question_category": "occupancy",
            "priority": "medium",
            "reason": "Occupancy affects access planning and client next steps.",
            "tied_missing_data_key": "occupancy_status",
            "client_safe": True,
        },
        {
            "question_text": "Are you the decision maker, or does anyone else need to review next steps with you?",
            "question_category": "decision_authority",
            "priority": "medium",
            "reason": "Decision authority reduces appointment and offer confusion.",
            "tied_missing_data_key": "decision_authority",
            "client_safe": True,
        },
        {
            "question_text": "Are there mortgage, lien, probate, or title questions that should be reviewed by qualified professionals?",
            "question_category": "mortgage_or_lien_context",
            "priority": "medium",
            "reason": "Title or legal questions should be routed to qualified review, not answered by the system.",
            "tied_missing_data_key": "title_status",
            "client_safe": True,
        },
    ]
    if "contact_channels_present" in missing_fields_by_name:
        questions.append(
            {
                "question_text": "What is the best way for you to receive a manual follow-up summary?",
                "question_category": "access_showing",
                "priority": "high",
                "reason": "Contactability is missing; no provider lookup is performed.",
                "tied_missing_data_key": "contact_channels_present",
                "client_safe": True,
            }
        )
    if "property_address_summary" in missing_fields_by_name:
        questions.append(
            {
                "question_text": "Can you confirm the property address before we review anything else?",
                "question_category": "access_showing",
                "priority": "high",
                "reason": "Property address is required for safe client review.",
                "tied_missing_data_key": "property_address_summary",
                "client_safe": True,
            }
        )
    return questions


def _appointment_missing_requirements(
    lead: ClientLeadProfile,
    score: ClientLeadIntelligenceScore,
) -> list[str]:
    missing: list[str] = []
    if not lead.motivation_signals:
        missing.append("seller_motivation")
    if not lead.contact_channels_present:
        missing.append("phone_or_email")
    if not lead.timeline_days or lead.timeline_days > 120:
        missing.append("timeline")
    if not lead.distress_signals and not lead.client_notes:
        missing.append("property_condition")
    if not lead.asking_price:
        missing.append("asking_price_or_expectation")
    if score.missing_data_score < 70:
        missing.append("cp2_missing_data_score")
    if lead.dnc_flag:
        missing.append("do_not_contact")
    return missing


def _default_evidence_items(lead: ClientLeadProfile) -> list[dict[str, object]]:
    if lead.id.startswith("client-lead-memphis-"):
        if lead.id == "client-lead-memphis-002":
            return [
                {
                    "item_type": "seller_note",
                    "item_summary": "High seller motivation is present, but ARV and repair evidence are still missing.",
                    "source_type": "manual",
                    "confidence_level": "medium",
                    "client_safe": True,
                    "internal_notes": "Memphis demo: keep evidence gap visible.",
                }
            ]
        return [
            {
                "item_type": item_type,
                "item_summary": "Memphis demo manual evidence item; no external provider call occurred.",
                "source_type": "manual",
                "confidence_level": "medium" if lead.id in {"client-lead-memphis-003", "client-lead-memphis-004"} else "high",
                "client_safe": True,
                "internal_notes": "Memphis demo support note.",
            }
            for item_type in ["seller_note", "repair_note", "comp_note", "occupancy_note", "title_note"]
        ]
    if lead.id == "client-lead-001":
        return [
            {
                "item_type": "seller_note",
                "item_summary": "Seller signals include absentee ownership, tired landlord context, and deferred-maintenance notes.",
                "source_type": "system_generated",
                "confidence_level": "high",
                "client_safe": True,
                "internal_notes": "Source: CP demo lead profile.",
            },
            {
                "item_type": "repair_note",
                "item_summary": "Manual demo repair note assumes visible deferred maintenance requires client review.",
                "source_type": "manual",
                "confidence_level": "medium",
                "client_safe": True,
                "internal_notes": "Internal estimate support hidden from client payload.",
            },
            {
                "item_type": "comp_note",
                "item_summary": "Manual comp note supports using the imported estimated value as a placeholder for review.",
                "source_type": "manual",
                "confidence_level": "medium",
                "client_safe": True,
                "internal_notes": "No live comp provider was called.",
            },
            {
                "item_type": "occupancy_note",
                "item_summary": "Vacancy signal requires seller confirmation before appointment planning.",
                "source_type": "system_generated",
                "confidence_level": "medium",
                "client_safe": True,
                "internal_notes": "Distress signal only.",
            },
            {
                "item_type": "title_note",
                "item_summary": "Title status is not verified; external review is required for any real file.",
                "source_type": "manual",
                "confidence_level": "low",
                "client_safe": True,
                "internal_notes": "Review reminder only.",
            },
        ]
    if lead.id == "client-lead-002":
        return [
            {
                "item_type": "seller_note",
                "item_summary": "Inherited/out-of-area signals are present, but property condition and valuation support are incomplete.",
                "source_type": "system_generated",
                "confidence_level": "medium",
                "client_safe": True,
                "internal_notes": "Needs manual data.",
            },
            {
                "item_type": "title_note",
                "item_summary": "Probate context needs external title or attorney review before any real paperwork.",
                "source_type": "manual",
                "confidence_level": "low",
                "client_safe": True,
                "internal_notes": "Review reminder only.",
            },
        ]
    if lead.id == "client-lead-004":
        return [
            {
                "item_type": "seller_note",
                "item_summary": "High-equity signal exists, but distress and seller motivation evidence are weak.",
                "source_type": "system_generated",
                "confidence_level": "low",
                "client_safe": True,
                "internal_notes": "Cross-workspace demo lead.",
            },
            {
                "item_type": "repair_note",
                "item_summary": "Manual review note expects high repair sensitivity and thin offer margin.",
                "source_type": "manual",
                "confidence_level": "low",
                "client_safe": True,
                "internal_notes": "Blocked example support.",
            },
            {
                "item_type": "comp_note",
                "item_summary": "Estimated value is a placeholder only and needs verification before client review.",
                "source_type": "manual",
                "confidence_level": "low",
                "client_safe": True,
                "internal_notes": "No live comp provider was called.",
            },
        ]
    return [
        {
            "item_type": "manual_note",
            "item_summary": "Lead requires manual evidence before underwriting can be reviewed.",
            "source_type": "system_generated",
            "confidence_level": "low",
            "client_safe": True,
            "internal_notes": "Incomplete demo lead.",
        }
    ]


def _missing_evidence_types(items: list[ClientDealEvidenceItem]) -> list[str]:
    present = {item.item_type for item in items}
    required = ["seller_note", "repair_note", "comp_note", "occupancy_note", "title_note"]
    return [item_type for item_type in required if item_type not in present]


def _condition_summary(lead: ClientLeadProfile) -> str:
    if "deferred_maintenance" in (lead.motivation_signals or []) or "property_condition_unknown" in (lead.distress_signals or []):
        return "Condition needs seller confirmation and repair evidence before final review."
    if lead.distress_signals:
        return f"Distress signals: {', '.join(lead.distress_signals)}."
    return "No condition evidence recorded yet."


def _manual_underwriting_inputs(lead: ClientLeadProfile) -> dict[str, int | None]:
    inputs: dict[str, dict[str, int | None]] = {
        "client-lead-001": {
            "arv_estimate": 238000,
            "repair_estimate": 42000,
            "holding_cost_estimate": 8000,
            "desired_assignment_fee": 10000,
        },
        "client-lead-004": {
            "arv_estimate": 210000,
            "repair_estimate": 120000,
            "holding_cost_estimate": 8000,
            "desired_assignment_fee": 10000,
        },
        "client-lead-memphis-001": {
            "arv_estimate": 165000,
            "repair_estimate": 32000,
            "holding_cost_estimate": 6000,
            "desired_assignment_fee": 10000,
        },
        "client-lead-memphis-003": {
            "arv_estimate": 210000,
            "repair_estimate": 36000,
            "holding_cost_estimate": 7000,
            "desired_assignment_fee": 10000,
        },
        "client-lead-memphis-004": {
            "arv_estimate": 135000,
            "repair_estimate": 76000,
            "holding_cost_estimate": 7000,
            "desired_assignment_fee": 10000,
        },
        "client-lead-memphis-005": {
            "arv_estimate": 240000,
            "repair_estimate": 50000,
            "holding_cost_estimate": 9000,
            "desired_assignment_fee": 15000,
        },
    }
    return inputs.get(
        lead.id,
        {
            "arv_estimate": None,
            "repair_estimate": None,
            "holding_cost_estimate": None,
            "desired_assignment_fee": 10000,
        },
    )


def _sync_offer_scenarios(
    session: Session,
    lead: ClientLeadProfile,
    review: ClientUnderwritingReview,
) -> None:
    session.query(ClientOfferScenario).filter(
        ClientOfferScenario.underwriting_review_id == review.id
    ).delete(synchronize_session=False)
    if review.max_allowable_offer is None:
        return
    scenario_values = [
        ("conservative", review.conservative_offer, "low"),
        ("standard", review.standard_offer, "medium"),
        ("aggressive", review.aggressive_offer, "high"),
    ]
    for name, amount, risk_level in scenario_values:
        amount_value = int(amount or 0)
        session.add(
            ClientOfferScenario(
                id=f"client-scenario-{uuid4().hex[:10]}",
                workspace_id=lead.workspace_id,
                lead_id=lead.id,
                underwriting_review_id=review.id,
                scenario_name=name,
                offer_amount=amount_value,
                projected_margin=max(0, int((review.max_allowable_offer or 0) - amount_value)),
                assumptions="Decision-support scenario from manual underwriting inputs only.",
                risk_level=risk_level if amount_value > 0 else "high",
                client_safe_explanation="No offer has been sent and no contract has been generated.",
            )
        )


def _ensure_acquisition_event(
    session: Session,
    lead: ClientLeadProfile,
    event_type: str,
    summary: str,
) -> None:
    event = (
        session.query(ClientAcquisitionDivisionEvent)
        .filter(
            ClientAcquisitionDivisionEvent.lead_id == lead.id,
            ClientAcquisitionDivisionEvent.event_type == event_type,
        )
        .first()
    )
    if event is None:
        event = ClientAcquisitionDivisionEvent(
            id=f"client-acq-event-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
            event_type=event_type,
        )
        session.add(event)
    event.event_summary = summary
    event.manager_name = "Acquisition Manager"
    event.client_visible = True


def _ensure_underwriting_event(
    session: Session,
    lead: ClientLeadProfile,
    event_type: str,
    summary: str,
) -> None:
    event = (
        session.query(ClientUnderwritingDivisionEvent)
        .filter(
            ClientUnderwritingDivisionEvent.lead_id == lead.id,
            ClientUnderwritingDivisionEvent.event_type == event_type,
        )
        .first()
    )
    if event is None:
        event = ClientUnderwritingDivisionEvent(
            id=f"client-underwriting-event-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
            event_type=event_type,
        )
        session.add(event)
    event.event_summary = summary
    event.manager_name = "Underwriting Manager"
    event.client_visible = True


def _workspace_or_404(session: Session, workspace_id: str) -> ClientWorkspace:
    workspace = session.get(ClientWorkspace, workspace_id)
    if workspace is None:
        raise ValueError(f"Client workspace not found: {workspace_id}")
    return workspace


def _lead_or_404(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
) -> ClientLeadProfile:
    query = session.query(ClientLeadProfile).filter(ClientLeadProfile.id == lead_id)
    if workspace_id is not None:
        query = query.filter(ClientLeadProfile.workspace_id == workspace_id)
    lead = query.first()
    if lead is None:
        raise ValueError(f"Client lead not found in requested workspace: {lead_id}")
    return lead


def _buyer_or_404(
    session: Session,
    buyer_id: str,
    workspace_id: str | None = None,
) -> ClientBuyerProfile:
    query = session.query(ClientBuyerProfile).filter(ClientBuyerProfile.id == buyer_id)
    if workspace_id is not None:
        query = query.filter(ClientBuyerProfile.workspace_id == workspace_id)
    buyer = query.first()
    if buyer is None:
        raise ValueError(f"Client buyer not found in requested workspace: {buyer_id}")
    return buyer


def _scores_for_workspace(session: Session, workspace_id: str) -> list[ClientLeadIntelligenceScore]:
    return (
        session.query(ClientLeadIntelligenceScore)
        .filter(ClientLeadIntelligenceScore.workspace_id == workspace_id)
        .all()
    )


def _missing_items(
    session: Session,
    workspace_id: str,
    lead_id: str,
) -> list[ClientLeadMissingDataItem]:
    return (
        session.query(ClientLeadMissingDataItem)
        .filter(
            ClientLeadMissingDataItem.workspace_id == workspace_id,
            ClientLeadMissingDataItem.lead_id == lead_id,
        )
        .order_by(ClientLeadMissingDataItem.severity.desc(), ClientLeadMissingDataItem.field_name)
        .all()
    )


def _next_actions(
    session: Session,
    workspace_id: str,
    lead_id: str,
) -> list[ClientLeadNextBestAction]:
    return (
        session.query(ClientLeadNextBestAction)
        .filter(
            ClientLeadNextBestAction.workspace_id == workspace_id,
            ClientLeadNextBestAction.lead_id == lead_id,
        )
        .order_by(desc(ClientLeadNextBestAction.priority))
        .all()
    )


def _division_events(
    session: Session,
    workspace_id: str,
    lead_id: str,
) -> list[ClientLeadDivisionEvent]:
    return (
        session.query(ClientLeadDivisionEvent)
        .filter(
            ClientLeadDivisionEvent.workspace_id == workspace_id,
            ClientLeadDivisionEvent.lead_id == lead_id,
        )
        .order_by(desc(ClientLeadDivisionEvent.created_at))
        .all()
    )


def _seller_questions(
    session: Session,
    workspace_id: str,
    lead_id: str,
    question_plan_id: str,
) -> list[ClientSellerQuestion]:
    return (
        session.query(ClientSellerQuestion)
        .filter(
            ClientSellerQuestion.workspace_id == workspace_id,
            ClientSellerQuestion.lead_id == lead_id,
            ClientSellerQuestion.question_plan_id == question_plan_id,
        )
        .order_by(ClientSellerQuestion.priority.desc(), ClientSellerQuestion.question_category)
        .all()
    )


def _objection_drafts(
    session: Session,
    workspace_id: str,
    lead_id: str,
) -> list[ClientObjectionResponseDraft]:
    return (
        session.query(ClientObjectionResponseDraft)
        .filter(
            ClientObjectionResponseDraft.workspace_id == workspace_id,
            ClientObjectionResponseDraft.lead_id == lead_id,
        )
        .order_by(ClientObjectionResponseDraft.objection_type)
        .all()
    )


def _follow_up_drafts(
    session: Session,
    workspace_id: str,
    lead_id: str,
) -> list[ClientFollowUpDraft]:
    return (
        session.query(ClientFollowUpDraft)
        .filter(
            ClientFollowUpDraft.workspace_id == workspace_id,
            ClientFollowUpDraft.lead_id == lead_id,
        )
        .order_by(ClientFollowUpDraft.channel_type)
        .all()
    )


def _acquisition_events(
    session: Session,
    workspace_id: str,
    lead_id: str,
) -> list[ClientAcquisitionDivisionEvent]:
    return (
        session.query(ClientAcquisitionDivisionEvent)
        .filter(
            ClientAcquisitionDivisionEvent.workspace_id == workspace_id,
            ClientAcquisitionDivisionEvent.lead_id == lead_id,
        )
        .order_by(desc(ClientAcquisitionDivisionEvent.created_at))
        .all()
    )


def _evidence_items(
    session: Session,
    workspace_id: str,
    lead_id: str,
    packet_id: str,
) -> list[ClientDealEvidenceItem]:
    return (
        session.query(ClientDealEvidenceItem)
        .filter(
            ClientDealEvidenceItem.workspace_id == workspace_id,
            ClientDealEvidenceItem.lead_id == lead_id,
            ClientDealEvidenceItem.packet_id == packet_id,
        )
        .order_by(ClientDealEvidenceItem.item_type)
        .all()
    )


def _offer_scenarios(
    session: Session,
    workspace_id: str,
    lead_id: str,
    underwriting_review_id: str,
) -> list[ClientOfferScenario]:
    return (
        session.query(ClientOfferScenario)
        .filter(
            ClientOfferScenario.workspace_id == workspace_id,
            ClientOfferScenario.lead_id == lead_id,
            ClientOfferScenario.underwriting_review_id == underwriting_review_id,
        )
        .order_by(ClientOfferScenario.scenario_name)
        .all()
    )


def _underwriting_events(
    session: Session,
    workspace_id: str,
    lead_id: str,
) -> list[ClientUnderwritingDivisionEvent]:
    return (
        session.query(ClientUnderwritingDivisionEvent)
        .filter(
            ClientUnderwritingDivisionEvent.workspace_id == workspace_id,
            ClientUnderwritingDivisionEvent.lead_id == lead_id,
        )
        .order_by(desc(ClientUnderwritingDivisionEvent.created_at))
        .all()
    )


def _buyer_buy_boxes(session: Session, workspace_id: str, buyer_id: str) -> list[ClientBuyerBuyBox]:
    return (
        session.query(ClientBuyerBuyBox)
        .filter(ClientBuyerBuyBox.workspace_id == workspace_id, ClientBuyerBuyBox.buyer_id == buyer_id)
        .order_by(ClientBuyerBuyBox.market, ClientBuyerBuyBox.id)
        .all()
    )


def _buyer_matches_for_buyer(session: Session, workspace_id: str, buyer_id: str) -> list[ClientDealBuyerMatch]:
    return (
        session.query(ClientDealBuyerMatch)
        .filter(ClientDealBuyerMatch.workspace_id == workspace_id, ClientDealBuyerMatch.buyer_id == buyer_id)
        .order_by(desc(ClientDealBuyerMatch.match_score))
        .all()
    )


def _buyer_demand_evidence(session: Session, workspace_id: str, lead_id: str) -> list[ClientBuyerDemandEvidence]:
    return (
        session.query(ClientBuyerDemandEvidence)
        .filter(ClientBuyerDemandEvidence.workspace_id == workspace_id, ClientBuyerDemandEvidence.lead_id == lead_id)
        .order_by(desc(ClientBuyerDemandEvidence.created_at))
        .all()
    )


def _buyer_outreach_drafts(session: Session, workspace_id: str, lead_id: str) -> list[ClientBuyerOutreachDraft]:
    return (
        session.query(ClientBuyerOutreachDraft)
        .filter(ClientBuyerOutreachDraft.workspace_id == workspace_id, ClientBuyerOutreachDraft.lead_id == lead_id)
        .order_by(desc(ClientBuyerOutreachDraft.created_at))
        .all()
    )


def _disposition_events(
    session: Session,
    workspace_id: str,
    lead_id: str,
) -> list[ClientDispositionDivisionEvent]:
    return (
        session.query(ClientDispositionDivisionEvent)
        .filter(ClientDispositionDivisionEvent.workspace_id == workspace_id, ClientDispositionDivisionEvent.lead_id == lead_id)
        .order_by(desc(ClientDispositionDivisionEvent.created_at))
        .all()
    )


def _buyer_grade(score: int) -> str:
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 55:
        return "C"
    if score >= 40:
        return "D"
    return "Review"


def _rehab_level(review: ClientUnderwritingReview) -> str:
    repairs = review.repair_estimate or 0
    if repairs >= 65000:
        return "heavy"
    if repairs >= 30000:
        return "medium"
    if repairs > 0:
        return "light"
    return "unknown"


def _best_buy_box_match(
    lead: ClientLeadProfile,
    review: ClientUnderwritingReview,
    buyer: ClientBuyerProfile,
    buy_boxes: list[ClientBuyerBuyBox],
    buyer_confidence: int,
) -> dict[str, object]:
    boxes = buy_boxes or [
        ClientBuyerBuyBox(
            id="",
            workspace_id=buyer.workspace_id,
            buyer_id=buyer.id,
            market=buyer.primary_market,
            zip_codes=buyer.target_zip_codes or [],
            property_types=buyer.preferred_property_types or [],
            min_purchase_price=buyer.min_price,
            max_purchase_price=buyer.max_price,
            rehab_level=buyer.rehab_tolerance,
        )
    ]
    best: dict[str, object] | None = None
    for box in boxes:
        score = 0
        matched: list[str] = []
        mismatches: list[str] = []
        market_fit = "unknown"
        if lead.property_zip and lead.property_zip in (box.zip_codes or []):
            score += 25
            matched.append("zip_match")
            market_fit = "fits"
        elif lead.property_city and (lead.property_city.lower() in (box.market or buyer.primary_market or "").lower()):
            score += 16
            matched.append("market_match")
            market_fit = "partial"
        else:
            mismatches.append("market_or_zip_not_in_buy_box")
            market_fit = "missing"
        property_fit = "unknown"
        if lead.property_type and lead.property_type in (box.property_types or []):
            score += 18
            matched.append("property_type_match")
            property_fit = "fits"
        elif box.property_types:
            mismatches.append("property_type_not_preferred")
            property_fit = "partial"
        else:
            mismatches.append("property_type_preference_missing")
            property_fit = "missing"
        price = review.standard_offer or review.max_allowable_offer
        price_fit = "unknown"
        if price is not None and box.max_purchase_price is not None:
            if (box.min_purchase_price is None or price >= box.min_purchase_price) and price <= box.max_purchase_price:
                score += 22
                matched.append("price_range_fit")
                price_fit = "fits"
            elif price <= int(box.max_purchase_price * 1.08):
                score += 12
                matched.append("price_close_to_buy_box")
                price_fit = "close"
            else:
                mismatches.append("price_above_buy_box")
                price_fit = "too_high"
        else:
            mismatches.append("price_range_missing")
        rehab = _rehab_level(review)
        rehab_fit = "unknown"
        allowed_rehab = box.rehab_level or buyer.rehab_tolerance
        if allowed_rehab in {"any", rehab}:
            score += 15
            matched.append("rehab_fit")
            rehab_fit = "fits"
        elif allowed_rehab == "heavy" and rehab in {"medium", "light"}:
            score += 12
            matched.append("rehab_within_tolerance")
            rehab_fit = "partial"
        elif allowed_rehab in {"medium", "heavy"} and rehab == "light":
            score += 10
            matched.append("rehab_below_tolerance")
            rehab_fit = "partial"
        else:
            mismatches.append("rehab_tolerance_mismatch")
            rehab_fit = "missing" if allowed_rehab == "unknown" else "partial"
        if buyer.proof_of_funds_status == "verified":
            score += 10
            matched.append("proof_of_funds_verified")
        elif buyer.funding_status == "stated":
            score += 5
            matched.append("funding_stated")
        else:
            mismatches.append("funding_or_pof_unclear")
        if not buy_boxes:
            mismatches.append("buyer_buy_box_missing")
        score += min(10, int((buyer_confidence or 0) / 10))
        score = max(0, min(100, score))
        status = "strong_match" if score >= 90 else "possible_match" if score >= 70 else "needs_review" if score >= 40 else "weak_match"
        candidate = {
            "buy_box_id": box.id or None,
            "match_score": score,
            "match_status": status,
            "matched_reasons": matched,
            "mismatch_reasons": mismatches,
            "price_fit_status": price_fit,
            "market_fit_status": market_fit,
            "property_type_fit_status": property_fit,
            "rehab_fit_status": rehab_fit,
        }
        if best is None or score > int(best["match_score"]):
            best = candidate
    return best or {
        "buy_box_id": None,
        "match_score": 0,
        "match_status": "blocked",
        "matched_reasons": [],
        "mismatch_reasons": ["buyer_buy_box_missing"],
        "price_fit_status": "unknown",
        "market_fit_status": "unknown",
        "property_type_fit_status": "unknown",
        "rehab_fit_status": "unknown",
    }


def _ensure_disposition_event(
    session: Session,
    lead: ClientLeadProfile,
    buyer_id: str | None,
    event_type: str,
    summary: str,
) -> None:
    event = (
        session.query(ClientDispositionDivisionEvent)
        .filter(
            ClientDispositionDivisionEvent.lead_id == lead.id,
            ClientDispositionDivisionEvent.buyer_id == buyer_id,
            ClientDispositionDivisionEvent.event_type == event_type,
        )
        .first()
    )
    if event is None:
        event = ClientDispositionDivisionEvent(
            id=f"client-disposition-event-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
            buyer_id=buyer_id,
            event_type=event_type,
        )
        session.add(event)
    event.event_summary = summary
    event.manager_name = "Disposition Manager"
    event.client_visible = True


def _sync_missing_items(
    session: Session,
    lead: ClientLeadProfile,
    fields: list[str],
) -> None:
    existing = {
        item.field_name: item
        for item in _missing_items(session, lead.workspace_id, lead.id)
    }
    for field in fields:
        if field not in existing:
            session.add(
                ClientLeadMissingDataItem(
                    id=f"client-missing-{uuid4().hex[:10]}",
                    workspace_id=lead.workspace_id,
                    lead_id=lead.id,
                    field_name=field,
                    reason=f"{field} is required before this lead is ready for client action.",
                    severity="high" if field in {"property_address_summary", "contact_channels_present"} else "medium",
                    blocks_readiness=True,
                )
            )
        else:
            existing[field].resolution_status = "open"
    for field, item in existing.items():
        if field not in fields:
            item.resolution_status = "resolved"
            item.blocks_readiness = False


def _ensure_next_action(
    session: Session,
    lead: ClientLeadProfile,
    score: ClientLeadIntelligenceScore,
) -> ClientLeadNextBestAction:
    action = (
        session.query(ClientLeadNextBestAction)
        .filter(ClientLeadNextBestAction.lead_id == lead.id)
        .first()
    )
    if action is None:
        action = ClientLeadNextBestAction(
            id=f"client-action-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
        )
        session.add(action)
    action.action_type = score.recommended_next_action
    action.action_label = _action_label(score.recommended_next_action)
    action.reason = score.reason_summary
    action.priority = score.final_priority_score
    action.status = "owner_review" if score.requires_human_review else "open"
    action.confidence_level = score.confidence_level
    action.requires_human_review = score.requires_human_review
    action.outbound_action_allowed = False
    action.provider_action_allowed = False
    action.client_safe = True
    return action


def _ensure_division_event(
    session: Session,
    lead: ClientLeadProfile,
    score: ClientLeadIntelligenceScore,
) -> None:
    event = (
        session.query(ClientLeadDivisionEvent)
        .filter(
            ClientLeadDivisionEvent.lead_id == lead.id,
            ClientLeadDivisionEvent.event_type == "lead_intelligence_score",
        )
        .first()
    )
    if event is None:
        event = ClientLeadDivisionEvent(
            id=f"client-event-{uuid4().hex[:10]}",
            workspace_id=lead.workspace_id,
            lead_id=lead.id,
            event_type="lead_intelligence_score",
        )
        session.add(event)
    event.division_name = "Lead Intelligence Division"
    event.manager_status = "human_review" if score.requires_human_review else "client_safe_queue"
    event.event_summary = f"Lead Intelligence Manager scored priority {score.final_priority_score} with {score.confidence_level} confidence."
    event.safe_for_client = True
    event.internal_prime_governance_visible = False
    event.raw_provider_payload_exposed = False


def _action_label(action_type: str) -> str:
    labels = {
        "human_review_required": "Review before any client action",
        "complete_missing_data": "Complete missing lead data",
        "owner_review_hot_lead": "Review hot lead with client-safe notes",
        "research_and_prepare_call_plan": "Research and prepare a call plan",
        "nurture_or_skip_for_now": "Nurture or skip for now",
        "manual_acquisition_ready": "Use acquisition brief for manual seller prep",
        "collect_repair_arv_evidence": "Collect repair and ARV evidence",
        "validate_buyer_demand_before_matching": "Validate buyer demand before matching",
        "hold_due_to_thin_offer_margin": "Hold until margin improves or evidence changes",
        "ready_for_buyer_matching_cp5": "Ready for buyer matching review",
    }
    return labels.get(action_type, "Review next best action")


def create_consent_record(
    session: Session,
    workspace_id: str,
    values: dict[str, object] | None = None,
) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    values = values or {}
    lead_id = str(values.get("lead_id") or "") or None
    buyer_id = str(values.get("buyer_id") or "") or None
    if lead_id:
        _lead_or_404(session, lead_id, workspace_id)
    if buyer_id:
        _buyer_or_404(session, buyer_id, workspace_id)
    record = ClientContactConsentRecord(
        id=f"client-consent-{uuid4().hex[:10]}",
        workspace_id=workspace_id,
        lead_id=lead_id,
        buyer_id=buyer_id,
        contact_type=str(values.get("contact_type") or ("seller" if lead_id else "buyer" if buyer_id else "unknown")),
        contact_name=str(values.get("contact_name") or "") or None,
        phone=str(values.get("phone") or "") or None,
        email=str(values.get("email") or "") or None,
        consent_channel=str(values.get("consent_channel") or "unknown"),
        consent_status=str(values.get("consent_status") or "unknown"),
        consent_source=str(values.get("consent_source") or "manual_entry"),
        consent_summary=str(values.get("consent_summary") or "Manual/demo consent record added for client-safe review."),
        consent_captured_at=str(values.get("consent_captured_at") or "") or None,
        expires_at=str(values.get("expires_at") or "") or None,
        requires_human_review=bool(values.get("requires_human_review", False)),
        client_safe=True,
        internal_notes="Hidden compliance note.",
    )
    session.add(record)
    session.flush()
    if lead_id:
        ensure_safe_contact_statuses_for_lead(session, _lead_or_404(session, lead_id, workspace_id), refresh=True)
    if buyer_id:
        ensure_safe_contact_statuses_for_buyer(session, _buyer_or_404(session, buyer_id, workspace_id), refresh=True)
    return {"consent_record": consent_record_public(record), "safety": client_command_safety_rules()}


def workspace_consent_records(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    records = (
        session.query(ClientContactConsentRecord)
        .filter(ClientContactConsentRecord.workspace_id == workspace_id)
        .order_by(desc(ClientContactConsentRecord.created_at))
        .all()
    )
    return {"workspace_id": workspace_id, "consent_records": [consent_record_public(record) for record in records], "safety": client_command_safety_rules()}


def consent_record_detail(session: Session, record_id: str) -> dict[str, object]:
    record = session.get(ClientContactConsentRecord, record_id)
    if record is None:
        raise ValueError(f"Consent record not found: {record_id}")
    return {"consent_record": consent_record_public(record), "safety": client_command_safety_rules()}


def create_opt_out_record(
    session: Session,
    workspace_id: str,
    values: dict[str, object] | None = None,
) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    values = values or {}
    lead_id = str(values.get("lead_id") or "") or None
    buyer_id = str(values.get("buyer_id") or "") or None
    if lead_id:
        _lead_or_404(session, lead_id, workspace_id)
    if buyer_id:
        _buyer_or_404(session, buyer_id, workspace_id)
    record = ClientContactOptOutRecord(
        id=f"client-opt-out-{uuid4().hex[:10]}",
        workspace_id=workspace_id,
        lead_id=lead_id,
        buyer_id=buyer_id,
        contact_type=str(values.get("contact_type") or ("seller" if lead_id else "buyer" if buyer_id else "unknown")),
        phone=str(values.get("phone") or "") or None,
        email=str(values.get("email") or "") or None,
        channel=str(values.get("channel") or "unknown"),
        opt_out_status=str(values.get("opt_out_status") or "unknown"),
        opt_out_source=str(values.get("opt_out_source") or "manual_entry"),
        opt_out_summary=str(values.get("opt_out_summary") or "Manual/demo opt-out record added for client-safe review."),
        recorded_at=str(values.get("recorded_at") or date.today().isoformat()),
        requires_human_review=bool(values.get("requires_human_review", True)),
        client_safe=True,
        internal_notes="Hidden opt-out note.",
    )
    session.add(record)
    session.flush()
    if lead_id:
        ensure_safe_contact_statuses_for_lead(session, _lead_or_404(session, lead_id, workspace_id), refresh=True)
    if buyer_id:
        ensure_safe_contact_statuses_for_buyer(session, _buyer_or_404(session, buyer_id, workspace_id), refresh=True)
    return {"opt_out_record": opt_out_record_public(record), "safety": client_command_safety_rules()}


def workspace_opt_out_records(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    records = (
        session.query(ClientContactOptOutRecord)
        .filter(ClientContactOptOutRecord.workspace_id == workspace_id)
        .order_by(desc(ClientContactOptOutRecord.created_at))
        .all()
    )
    return {"workspace_id": workspace_id, "opt_out_records": [opt_out_record_public(record) for record in records], "safety": client_command_safety_rules()}


def opt_out_record_detail(session: Session, record_id: str) -> dict[str, object]:
    record = session.get(ClientContactOptOutRecord, record_id)
    if record is None:
        raise ValueError(f"Opt-out record not found: {record_id}")
    return {"opt_out_record": opt_out_record_public(record), "safety": client_command_safety_rules()}


def safe_contact_status_for_lead(
    session: Session,
    lead_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    statuses = ensure_safe_contact_statuses_for_lead(session, lead, refresh=refresh)
    return {
        "lead": lead_public(lead),
        "safe_contact_statuses": [safe_contact_status_public(status) for status in statuses],
        "safety": client_command_safety_rules(),
    }


def safe_contact_status_for_buyer(
    session: Session,
    buyer_id: str,
    workspace_id: str | None = None,
    refresh: bool = False,
) -> dict[str, object]:
    buyer = _buyer_or_404(session, buyer_id, workspace_id)
    statuses = ensure_safe_contact_statuses_for_buyer(session, buyer, refresh=refresh)
    return {
        "buyer": buyer_profile_public(buyer),
        "safe_contact_statuses": [safe_contact_status_public(status) for status in statuses],
        "safety": client_command_safety_rules(),
    }


def compliance_blocked(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientSafeContactStatus).filter(ClientSafeContactStatus.status.in_(["blocked", "opted_out"]))
    if workspace_id:
        query = query.filter(ClientSafeContactStatus.workspace_id == workspace_id)
    rows = query.order_by(desc(ClientSafeContactStatus.created_at)).all()
    return {"workspace_id": workspace_id, "blocked": [safe_contact_status_public(row) for row in rows], "safety": client_command_safety_rules()}


def compliance_needs_review(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientSafeContactStatus).filter(ClientSafeContactStatus.status.in_(["needs_review", "missing_consent", "placeholder_check_required"]))
    if workspace_id:
        query = query.filter(ClientSafeContactStatus.workspace_id == workspace_id)
    rows = query.order_by(desc(ClientSafeContactStatus.created_at)).all()
    return {"workspace_id": workspace_id, "needs_review": [safe_contact_status_public(row) for row in rows], "safety": client_command_safety_rules()}


def compliance_safe_manual_use(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientSafeContactStatus).filter(ClientSafeContactStatus.status == "safe_for_manual_use")
    if workspace_id:
        query = query.filter(ClientSafeContactStatus.workspace_id == workspace_id)
    rows = query.order_by(desc(ClientSafeContactStatus.created_at)).all()
    return {"workspace_id": workspace_id, "safe_manual_use": [safe_contact_status_public(row) for row in rows], "safety": client_command_safety_rules()}


def create_message_risk_review(
    session: Session,
    values: dict[str, object] | None = None,
) -> dict[str, object]:
    values = values or {}
    workspace_id = str(values.get("workspace_id") or "")
    if not workspace_id:
        raise ValueError("workspace_id is required")
    _workspace_or_404(session, workspace_id)
    lead_id = str(values.get("lead_id") or "") or None
    buyer_id = str(values.get("buyer_id") or "") or None
    if lead_id:
        _lead_or_404(session, lead_id, workspace_id)
    if buyer_id:
        _buyer_or_404(session, buyer_id, workspace_id)
    source_draft_type = str(values.get("source_draft_type") or "unknown")
    source_draft_id = str(values.get("source_draft_id") or "") or None
    channel = str(values.get("channel") or "unknown")
    draft_body = str(values.get("draft_body") or _message_source_text(session, workspace_id, source_draft_type, source_draft_id, lead_id, buyer_id))
    safety = validate_client_safe_text(draft_body)
    flags = list(safety["risk_flags"])
    blocked_terms = flags[:]
    review_status = "passed_for_manual_use"
    risk_level = "low"
    if source_draft_type == "unknown" or channel == "unknown":
        review_status = "needs_review"
        risk_level = "medium"
        flags.append("missing_channel_or_source_context")
    if not safety["allowed"]:
        review_status = "blocked"
        risk_level = "high"
    review = ClientMessageRiskReview(
        id=f"client-message-risk-{uuid4().hex[:10]}",
        workspace_id=workspace_id,
        lead_id=lead_id,
        buyer_id=buyer_id,
        source_draft_type=source_draft_type,
        source_draft_id=source_draft_id,
        channel=channel,
        review_status=review_status,
        risk_level=risk_level,
        unsafe_language_flags=sorted(set(flags)),
        blocked_terms=sorted(set(blocked_terms)),
        safe_rewrite_suggestion=None if review_status == "passed_for_manual_use" else "Use factual, non-urgent language and remove guarantees, pressure, and legal conclusions.",
        reason_summary="Manual-use draft review only. No live communication or provider check occurred.",
        manual_use_only=True,
        no_live_send=True,
        requires_human_review=review_status != "passed_for_manual_use",
    )
    session.add(review)
    session.flush()
    if lead_id:
        _ensure_compliance_event(session, workspace_id, lead_id, None, "message_risk_review", f"Compliance Manager set draft review to {review_status}.")
    if buyer_id:
        _ensure_compliance_event(session, workspace_id, None, buyer_id, "message_risk_review", f"Compliance Manager set buyer draft review to {review_status}.")
    return {"message_risk_review": message_risk_review_public(review), "safety": client_command_safety_rules()}


def message_risk_review_detail(session: Session, review_id: str) -> dict[str, object]:
    review = session.get(ClientMessageRiskReview, review_id)
    if review is None:
        raise ValueError(f"Message risk review not found: {review_id}")
    return {"message_risk_review": message_risk_review_public(review), "safety": client_command_safety_rules()}


def create_communication_approval_gate(
    session: Session,
    values: dict[str, object] | None = None,
) -> dict[str, object]:
    values = values or {}
    workspace_id = str(values.get("workspace_id") or "")
    if not workspace_id:
        raise ValueError("workspace_id is required")
    _workspace_or_404(session, workspace_id)
    lead_id = str(values.get("lead_id") or "") or None
    buyer_id = str(values.get("buyer_id") or "") or None
    source_draft_type = str(values.get("source_draft_type") or "unknown")
    source_draft_id = str(values.get("source_draft_id") or "") or None
    if source_draft_type == "buyer_outreach" and buyer_id:
        buyer = _buyer_or_404(session, buyer_id, workspace_id)
        contact_status = _select_contact_status(ensure_safe_contact_statuses_for_buyer(session, buyer, refresh=True), source_draft_type)
    elif lead_id:
        lead = _lead_or_404(session, lead_id, workspace_id)
        contact_status = _select_contact_status(ensure_safe_contact_statuses_for_lead(session, lead, refresh=True), source_draft_type)
    elif buyer_id:
        buyer = _buyer_or_404(session, buyer_id, workspace_id)
        contact_status = _select_contact_status(ensure_safe_contact_statuses_for_buyer(session, buyer, refresh=True), source_draft_type)
    else:
        raise ValueError("lead_id or buyer_id is required")
    review_id = str(values.get("message_risk_review_id") or "") or None
    review = session.get(ClientMessageRiskReview, review_id) if review_id else None
    if review is None:
        review = create_message_risk_review(
            session,
            {
                "workspace_id": workspace_id,
                "lead_id": lead_id,
                "buyer_id": buyer_id,
                "source_draft_type": source_draft_type,
                "source_draft_id": source_draft_id,
                "channel": contact_status.channel if contact_status else "unknown",
            },
        )["message_risk_review"]
        review = session.get(ClientMessageRiskReview, review["id"])
    block_reasons: list[str] = []
    required_next_steps: list[str] = []
    gate_status = "manual_use_allowed"
    if contact_status is None:
        gate_status = "needs_review"
        block_reasons.append("contact_status_missing")
        required_next_steps.append("check_safe_contact_status")
    elif contact_status.status in {"blocked", "opted_out"}:
        gate_status = "blocked"
        block_reasons.extend(contact_status.block_reasons or [contact_status.status])
        required_next_steps.append("respect_opt_out_and_hold_draft")
    elif contact_status.status in {"needs_review", "missing_consent", "placeholder_check_required", "channel_not_configured"}:
        gate_status = "needs_review"
        block_reasons.extend(contact_status.block_reasons or [contact_status.status])
        required_next_steps.append("resolve_manual_consent_or_placeholder_gap")
    if review.review_status == "blocked":
        gate_status = "blocked"
        block_reasons.extend(review.blocked_terms or ["message_risk_blocked"])
        required_next_steps.append("rewrite_message_for_manual_use")
    elif review.review_status == "needs_review" and gate_status != "blocked":
        gate_status = "needs_review"
        required_next_steps.append("review_message_language")
    if gate_status == "manual_use_allowed":
        required_next_steps.append("manual_use_only_no_send")
    gate = ClientCommunicationApprovalGate(
        id=f"client-comm-gate-{uuid4().hex[:10]}",
        workspace_id=workspace_id,
        lead_id=lead_id,
        buyer_id=buyer_id,
        source_draft_type=source_draft_type,
        source_draft_id=source_draft_id,
        contact_status_id=contact_status.id if contact_status else None,
        message_risk_review_id=review.id if review else None,
        gate_status=gate_status if gate_status != "manual_use_allowed" else "manual_use_allowed",
        approval_scope="manual_use_only",
        block_reasons=sorted(set(block_reasons)),
        required_next_steps=required_next_steps,
        no_live_send=True,
        no_provider_call=True,
        no_campaign_started=True,
        client_safe_summary="Manual-use approval only; no message has been sent.",
        requires_human_review=gate_status != "manual_use_allowed",
    )
    session.add(gate)
    session.flush()
    _ensure_compliance_event(session, workspace_id, lead_id, buyer_id, "communication_gate", f"Compliance Manager set communication gate to {gate.gate_status}.")
    return {"communication_approval_gate": communication_approval_gate_public(gate), "safety": client_command_safety_rules()}


def communication_approval_gates(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientCommunicationApprovalGate)
    if workspace_id:
        query = query.filter(ClientCommunicationApprovalGate.workspace_id == workspace_id)
    rows = query.order_by(desc(ClientCommunicationApprovalGate.created_at)).all()
    return {"workspace_id": workspace_id, "communication_approval_gates": [communication_approval_gate_public(row) for row in rows], "safety": client_command_safety_rules()}


def communication_approval_gate_detail(session: Session, gate_id: str) -> dict[str, object]:
    gate = session.get(ClientCommunicationApprovalGate, gate_id)
    if gate is None:
        raise ValueError(f"Communication approval gate not found: {gate_id}")
    return {"communication_approval_gate": communication_approval_gate_public(gate), "safety": client_command_safety_rules()}


def create_compliance_readiness_placeholder(
    session: Session,
    workspace_id: str,
    values: dict[str, object] | None = None,
) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    values = values or {}
    placeholder = ClientComplianceReadinessPlaceholder(
        id=f"client-placeholder-{uuid4().hex[:10]}",
        workspace_id=workspace_id,
        placeholder_type=str(values.get("placeholder_type") or "dnc_check"),
        readiness_status=str(values.get("readiness_status") or "placeholder_only"),
        summary=str(values.get("summary") or "Manual compliance placeholder only; no provider registration or external check occurred."),
        required_before_live=bool(values.get("required_before_live", True)),
        no_provider_call=True,
        client_safe=True,
    )
    session.add(placeholder)
    session.flush()
    return {"readiness_placeholder": compliance_placeholder_public(placeholder), "safety": client_command_safety_rules()}


def workspace_compliance_placeholders(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    rows = _compliance_placeholders(session, workspace_id)
    return {"workspace_id": workspace_id, "readiness_placeholders": [compliance_placeholder_public(row) for row in rows], "safety": client_command_safety_rules()}


def compliance_overview(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    blocked = compliance_blocked(session, workspace_id)["blocked"]
    needs_review = compliance_needs_review(session, workspace_id)["needs_review"]
    safe_rows = compliance_safe_manual_use(session, workspace_id)["safe_manual_use"]
    query = session.query(ClientCommunicationApprovalGate)
    if workspace_id:
        query = query.filter(ClientCommunicationApprovalGate.workspace_id == workspace_id)
    gates = query.order_by(desc(ClientCommunicationApprovalGate.created_at)).all()
    return {
        "workspace_id": workspace_id,
        "blocked_count": len(blocked),
        "needs_review_count": len(needs_review),
        "safe_manual_use_count": len(safe_rows),
        "gate_count": len(gates),
        "blocked": blocked,
        "needs_review": needs_review,
        "safe_manual_use": safe_rows,
        "communication_approval_gates": [communication_approval_gate_public(gate) for gate in gates],
        "safety": client_command_safety_rules(),
    }


def create_weekly_report(
    session: Session,
    workspace_id: str,
    values: dict[str, object] | None = None,
) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    values = values or {}
    week_end = str(values.get("report_week_end") or date.today().isoformat())
    week_start = str(values.get("report_week_start") or (date.fromisoformat(week_end) - timedelta(days=6)).isoformat())
    report = ClientWeeklyCommandReport(
        id=f"client-weekly-report-{uuid4().hex[:10]}",
        workspace_id=workspace_id,
        report_week_start=week_start,
        report_week_end=week_end,
    )
    session.add(report)
    session.flush()
    _refresh_weekly_report(session, workspace, report)
    return weekly_report_detail(session, report.id)


def workspace_weekly_reports(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    rows = _weekly_reports(session, workspace_id)
    return {"workspace_id": workspace_id, "weekly_reports": [weekly_report_public(row) for row in rows], "safety": client_command_safety_rules()}


def weekly_report_detail(session: Session, report_id: str) -> dict[str, object]:
    report = session.get(ClientWeeklyCommandReport, report_id)
    if report is None:
        raise ValueError(f"Weekly report not found: {report_id}")
    return {
        "weekly_report": weekly_report_public(report),
        "metrics": [weekly_metric_snapshot_public(item) for item in _weekly_metric_snapshots(session, report.workspace_id, report.id)],
        "lead_rollups": [weekly_lead_rollup_public(item) for item in _weekly_lead_rollups(session, report.workspace_id, report.id)],
        "bottlenecks": [weekly_bottleneck_public(item) for item in _weekly_bottlenecks(session, report.workspace_id, report.id)],
        "recommended_actions": [weekly_recommended_action_public(item) for item in _weekly_recommended_actions(session, report.workspace_id, report.id)],
        "division_summaries": [weekly_division_summary_public(item) for item in _weekly_division_summaries(session, report.workspace_id, report.id)],
        "events": [weekly_report_event_public(item) for item in _weekly_report_events(session, report.workspace_id, report.id)],
        "safety": client_command_safety_rules(),
    }


def mark_weekly_report_reviewed(session: Session, report_id: str) -> dict[str, object]:
    report = session.get(ClientWeeklyCommandReport, report_id)
    if report is None:
        raise ValueError(f"Weekly report not found: {report_id}")
    report.report_status = "reviewed"
    session.flush()
    return weekly_report_detail(session, report_id)


def mark_weekly_report_client_visible(session: Session, report_id: str) -> dict[str, object]:
    report = session.get(ClientWeeklyCommandReport, report_id)
    if report is None:
        raise ValueError(f"Weekly report not found: {report_id}")
    report.report_status = "client_visible"
    session.flush()
    return weekly_report_detail(session, report_id)


def weekly_report_metrics(session: Session, report_id: str) -> dict[str, object]:
    report = session.get(ClientWeeklyCommandReport, report_id)
    if report is None:
        raise ValueError(f"Weekly report not found: {report_id}")
    return {"report_id": report_id, "metrics": [weekly_metric_snapshot_public(item) for item in _weekly_metric_snapshots(session, report.workspace_id, report.id)], "safety": client_command_safety_rules()}


def weekly_report_lead_rollups(session: Session, report_id: str) -> dict[str, object]:
    report = session.get(ClientWeeklyCommandReport, report_id)
    if report is None:
        raise ValueError(f"Weekly report not found: {report_id}")
    return {"report_id": report_id, "lead_rollups": [weekly_lead_rollup_public(item) for item in _weekly_lead_rollups(session, report.workspace_id, report.id)], "safety": client_command_safety_rules()}


def weekly_report_bottlenecks(session: Session, report_id: str) -> dict[str, object]:
    report = session.get(ClientWeeklyCommandReport, report_id)
    if report is None:
        raise ValueError(f"Weekly report not found: {report_id}")
    return {"report_id": report_id, "bottlenecks": [weekly_bottleneck_public(item) for item in _weekly_bottlenecks(session, report.workspace_id, report.id)], "safety": client_command_safety_rules()}


def weekly_report_recommended_actions(session: Session, report_id: str) -> dict[str, object]:
    report = session.get(ClientWeeklyCommandReport, report_id)
    if report is None:
        raise ValueError(f"Weekly report not found: {report_id}")
    return {"report_id": report_id, "recommended_actions": [weekly_recommended_action_public(item) for item in _weekly_recommended_actions(session, report.workspace_id, report.id)], "safety": client_command_safety_rules()}


def weekly_report_division_summaries(session: Session, report_id: str) -> dict[str, object]:
    report = session.get(ClientWeeklyCommandReport, report_id)
    if report is None:
        raise ValueError(f"Weekly report not found: {report_id}")
    return {"report_id": report_id, "division_summaries": [weekly_division_summary_public(item) for item in _weekly_division_summaries(session, report.workspace_id, report.id)], "safety": client_command_safety_rules()}


def reports_overview(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientWeeklyCommandReport)
    if workspace_id:
        query = query.filter(ClientWeeklyCommandReport.workspace_id == workspace_id)
    reports = query.order_by(desc(ClientWeeklyCommandReport.created_at)).all()
    latest = reports[0] if reports else None
    latest_detail = weekly_report_detail(session, latest.id) if latest else None
    return {
        "workspace_id": workspace_id,
        "latest_report": latest_detail["weekly_report"] if latest_detail else None,
        "report_count": len(reports),
        "latest_bottleneck": latest_detail["bottlenecks"][0] if latest_detail and latest_detail["bottlenecks"] else None,
        "next_recommended_action": latest_detail["recommended_actions"][0] if latest_detail and latest_detail["recommended_actions"] else None,
        "safety": client_command_safety_rules(),
    }


def reports_weekly(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientWeeklyCommandReport)
    if workspace_id:
        query = query.filter(ClientWeeklyCommandReport.workspace_id == workspace_id)
    reports = query.order_by(desc(ClientWeeklyCommandReport.created_at)).all()
    return {"workspace_id": workspace_id, "weekly_reports": [weekly_report_public(item) for item in reports], "safety": client_command_safety_rules()}


def reports_bottlenecks(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    report = _latest_weekly_report(session, workspace_id)
    if report is None:
        return {"workspace_id": workspace_id, "bottlenecks": [], "safety": client_command_safety_rules()}
    return weekly_report_bottlenecks(session, report.id)


def reports_recommended_actions(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    report = _latest_weekly_report(session, workspace_id)
    if report is None:
        return {"workspace_id": workspace_id, "recommended_actions": [], "safety": client_command_safety_rules()}
    return weekly_report_recommended_actions(session, report.id)


def ensure_safe_contact_statuses_for_lead(
    session: Session,
    lead: ClientLeadProfile,
    refresh: bool = False,
) -> list[ClientSafeContactStatus]:
    existing = _safe_contact_statuses(session, lead.workspace_id, lead.id, None)
    if existing and not refresh:
        return existing
    if refresh:
        session.query(ClientSafeContactStatus).filter(ClientSafeContactStatus.lead_id == lead.id).delete(synchronize_session=False)
    channels = _contact_channels_for_lead(session, lead)
    statuses: list[ClientSafeContactStatus] = []
    placeholders = {item.placeholder_type: item for item in _compliance_placeholders(session, lead.workspace_id)}
    for channel in channels:
        status = (
            session.query(ClientSafeContactStatus)
            .filter(ClientSafeContactStatus.lead_id == lead.id, ClientSafeContactStatus.channel == channel)
            .first()
        )
        if status is None:
            status = ClientSafeContactStatus(
                id=f"client-safe-contact-{uuid4().hex[:10]}",
                workspace_id=lead.workspace_id,
                lead_id=lead.id,
                contact_type="seller",
                channel=channel,
            )
            session.add(status)
        _populate_safe_contact_status(session, status, lead.workspace_id, lead.id, None, channel, placeholders)
        statuses.append(status)
    if statuses:
        _ensure_compliance_event(session, lead.workspace_id, lead.id, None, "safe_contact_status", "Compliance Manager refreshed seller contact readiness.")
    session.flush()
    return _safe_contact_statuses(session, lead.workspace_id, lead.id, None)


def ensure_safe_contact_statuses_for_buyer(
    session: Session,
    buyer: ClientBuyerProfile,
    refresh: bool = False,
) -> list[ClientSafeContactStatus]:
    existing = _safe_contact_statuses(session, buyer.workspace_id, None, buyer.id)
    if existing and not refresh:
        return existing
    if refresh:
        session.query(ClientSafeContactStatus).filter(ClientSafeContactStatus.buyer_id == buyer.id).delete(synchronize_session=False)
    channels = _contact_channels_for_buyer(session, buyer)
    statuses: list[ClientSafeContactStatus] = []
    placeholders = {item.placeholder_type: item for item in _compliance_placeholders(session, buyer.workspace_id)}
    for channel in channels:
        status = (
            session.query(ClientSafeContactStatus)
            .filter(ClientSafeContactStatus.buyer_id == buyer.id, ClientSafeContactStatus.channel == channel)
            .first()
        )
        if status is None:
            status = ClientSafeContactStatus(
                id=f"client-safe-contact-{uuid4().hex[:10]}",
                workspace_id=buyer.workspace_id,
                buyer_id=buyer.id,
                contact_type="buyer",
                channel=channel,
            )
            session.add(status)
        _populate_safe_contact_status(session, status, buyer.workspace_id, None, buyer.id, channel, placeholders)
        statuses.append(status)
    if statuses:
        _ensure_compliance_event(session, buyer.workspace_id, None, buyer.id, "safe_contact_status", "Compliance Manager refreshed buyer contact readiness.")
    session.flush()
    return _safe_contact_statuses(session, buyer.workspace_id, None, buyer.id)


def _populate_safe_contact_status(
    session: Session,
    status: ClientSafeContactStatus,
    workspace_id: str,
    lead_id: str | None,
    buyer_id: str | None,
    channel: str,
    placeholders: dict[str, ClientComplianceReadinessPlaceholder],
) -> None:
    disposition_gate = (
        session.query(ClientDispositionReadinessGate)
        .filter(ClientDispositionReadinessGate.lead_id == lead_id)
        .first()
        if lead_id
        else None
    )
    consents = [
        record
        for record in _consent_records(session, workspace_id, lead_id, buyer_id)
        if record.consent_channel in {channel, "unknown"}
    ]
    opt_outs = [
        record
        for record in _opt_out_records(session, workspace_id, lead_id, buyer_id)
        if record.channel in {channel, "all", "unknown"}
    ]
    consent = consents[0] if consents else None
    active_opt_out = next((record for record in opt_outs if record.opt_out_status == "active"), None)
    dnc = placeholders.get("dnc_check")
    ten_dlc = placeholders.get("ten_dlc_registration")
    block_reasons: list[str] = []
    risk_flags: list[str] = []
    if active_opt_out:
        status.status = "blocked"
        status.opt_out_status_snapshot = active_opt_out.opt_out_status
        status.consent_status_snapshot = consent.consent_status if consent else "unknown"
        block_reasons.append("active_opt_out")
        status.can_use_manual_draft = False
    elif consent is None or consent.consent_status in {"missing", "unknown", "disputed"}:
        status.status = (
            "needs_review"
            if disposition_gate and disposition_gate.readiness_status in {"buyer_demand_missing", "ready_for_client_review"}
            else "missing_consent"
        )
        status.consent_status_snapshot = consent.consent_status if consent else "missing"
        status.opt_out_status_snapshot = "unknown" if not opt_outs else opt_outs[0].opt_out_status
        block_reasons.append("consent_missing_or_unconfirmed")
        status.can_use_manual_draft = False
    elif consent.consent_status == "expired":
        status.status = "needs_review"
        status.consent_status_snapshot = "expired"
        status.opt_out_status_snapshot = "unknown" if not opt_outs else opt_outs[0].opt_out_status
        block_reasons.append("consent_expired")
        status.can_use_manual_draft = False
    else:
        status.status = "safe_for_manual_use"
        status.consent_status_snapshot = consent.consent_status
        status.opt_out_status_snapshot = "cleared" if not opt_outs else opt_outs[0].opt_out_status
        status.can_use_manual_draft = True
    if channel == "call":
        status.dnc_placeholder_status = "placeholder_required" if not dnc or dnc.readiness_status != "documented" else "review_needed"
        status.ten_dlc_placeholder_status = "not_applicable"
    elif channel == "sms":
        status.dnc_placeholder_status = "placeholder_required" if not dnc or dnc.readiness_status != "documented" else "review_needed"
        status.ten_dlc_placeholder_status = "placeholder_required" if not ten_dlc or ten_dlc.readiness_status != "documented" else "review_needed"
    else:
        status.dnc_placeholder_status = "not_applicable"
        status.ten_dlc_placeholder_status = "not_applicable"
    if channel == "unknown":
        status.status = "needs_review"
        block_reasons.append("channel_unknown")
        status.can_use_manual_draft = False
    if channel == "email" and consent is not None and consent.email is None:
        risk_flags.append("email_not_recorded")
    if channel in {"call", "sms"} and consent is not None and consent.phone is None:
        risk_flags.append("phone_not_recorded")
    status.reason_summary = _contact_reason_summary(status.status, channel, consent, active_opt_out)
    status.block_reasons = sorted(set(block_reasons))
    status.risk_flags = sorted(set(risk_flags))
    status.no_live_send = True
    status.no_provider_check = True
    status.requires_human_review = status.status != "safe_for_manual_use"
    status.client_safe_summary = "Readiness check only; no provider check or live communication occurred."


def _refresh_weekly_report(
    session: Session,
    workspace: ClientWorkspace,
    report: ClientWeeklyCommandReport,
) -> None:
    leads = (
        session.query(ClientLeadProfile)
        .filter(ClientLeadProfile.workspace_id == workspace.id)
        .order_by(ClientLeadProfile.created_at)
        .all()
    )
    session.query(ClientWeeklyReportMetricSnapshot).filter(ClientWeeklyReportMetricSnapshot.report_id == report.id).delete(synchronize_session=False)
    session.query(ClientWeeklyLeadStatusRollup).filter(ClientWeeklyLeadStatusRollup.report_id == report.id).delete(synchronize_session=False)
    session.query(ClientWeeklyBottleneck).filter(ClientWeeklyBottleneck.report_id == report.id).delete(synchronize_session=False)
    session.query(ClientWeeklyRecommendedAction).filter(ClientWeeklyRecommendedAction.report_id == report.id).delete(synchronize_session=False)
    session.query(ClientWeeklyDivisionSummary).filter(ClientWeeklyDivisionSummary.report_id == report.id).delete(synchronize_session=False)
    session.query(ClientWeeklyReportEvent).filter(ClientWeeklyReportEvent.report_id == report.id).delete(synchronize_session=False)

    hot_leads = 0
    acquisition_ready = 0
    appointment_ready = 0
    evidence_missing = 0
    underwriting_ready = 0
    offer_ready = 0
    buyer_match_count = 0
    disposition_ready = 0
    compliance_blocked = 0
    compliance_needs_review = 0
    manual_drafts = 0
    blocked_actions = 0
    bottlenecks: dict[str, int] = {}

    for lead in leads:
        score = ensure_score(session, lead)
        brief = ensure_acquisition_brief(session, lead)
        readiness = ensure_appointment_readiness(session, lead)
        packet = ensure_evidence_packet(session, lead)
        review = ensure_underwriting_review(session, lead, packet)
        offer_gate = ensure_offer_readiness(session, lead, packet, review)
        matches = ensure_buyer_matches(session, lead)
        disposition_gate = ensure_disposition_readiness(session, lead)
        follow_up = ensure_follow_up_drafts(session, lead)
        buyer_drafts = ensure_buyer_outreach_drafts(session, lead)
        compliance_statuses = ensure_safe_contact_statuses_for_lead(session, lead)

        if score.final_priority_score >= 78:
            hot_leads += 1
        if brief and not brief.requires_human_review:
            acquisition_ready += 1
        if readiness.appointment_ready:
            appointment_ready += 1
        if packet.evidence_status == "missing_evidence":
            evidence_missing += 1
        if review.max_allowable_offer is not None:
            underwriting_ready += 1
        if offer_gate.readiness_status == "ready_for_client_review":
            offer_ready += 1
        if matches:
            buyer_match_count += 1
        if disposition_gate.readiness_status == "ready_for_client_review":
            disposition_ready += 1
        if any(item.status in {"blocked", "opted_out"} for item in compliance_statuses):
            compliance_blocked += 1
            blocked_actions += 1
        if any(item.status in {"needs_review", "missing_consent", "placeholder_check_required"} for item in compliance_statuses):
            compliance_needs_review += 1
        manual_drafts += len(follow_up) + len(buyer_drafts)

        top_blocker = None
        if "arv_estimate_missing" in offer_gate.block_reasons or "repair_estimate_missing" in offer_gate.block_reasons:
            bottlenecks["missing_arv"] = bottlenecks.get("missing_arv", 0) + 1
            bottlenecks["missing_repairs"] = bottlenecks.get("missing_repairs", 0) + 1
            top_blocker = "missing_arv_or_repairs"
        if "buyer_demand_evidence_missing" in disposition_gate.block_reasons:
            bottlenecks["buyer_demand_missing"] = bottlenecks.get("buyer_demand_missing", 0) + 1
            top_blocker = top_blocker or "buyer_demand_missing"
        if any(item.status in {"needs_review", "missing_consent", "blocked", "opted_out"} for item in compliance_statuses):
            bottlenecks["compliance_blocked"] = bottlenecks.get("compliance_blocked", 0) + 1
            top_blocker = top_blocker or "compliance_review_needed"
        if "thin_or_negative_offer_margin" in offer_gate.block_reasons:
            bottlenecks["thin_margin"] = bottlenecks.get("thin_margin", 0) + 1
            top_blocker = top_blocker or "thin_margin"
        if _missing_items(session, lead.workspace_id, lead.id):
            bottlenecks["missing_contact_data"] = bottlenecks.get("missing_contact_data", 0) + 1
            top_blocker = top_blocker or "missing_contact_data"

        rollup = ClientWeeklyLeadStatusRollup(
            id=f"client-rollup-{uuid4().hex[:10]}",
            workspace_id=workspace.id,
            report_id=report.id,
            lead_id=lead.id,
            lead_name_or_address=lead.display_name or lead.property_address_summary,
            current_stage=_lead_stage(offer_gate, disposition_gate, compliance_statuses),
            status_summary=_lead_status_summary(score, offer_gate, disposition_gate, compliance_statuses),
            top_blocker=top_blocker,
            recommended_next_step=_weekly_next_step(score, offer_gate, disposition_gate, compliance_statuses),
            priority_level="urgent" if score.final_priority_score >= 78 else "high" if score.final_priority_score >= 65 else "medium" if score.final_priority_score >= 40 else "low",
            client_safe=True,
        )
        session.add(rollup)

    metric = ClientWeeklyReportMetricSnapshot(
        id=f"client-metric-{uuid4().hex[:10]}",
        workspace_id=workspace.id,
        report_id=report.id,
        total_leads=len(leads),
        hot_leads_count=hot_leads,
        acquisition_ready_count=acquisition_ready,
        appointment_ready_count=appointment_ready,
        evidence_missing_count=evidence_missing,
        underwriting_ready_count=underwriting_ready,
        offer_ready_count=offer_ready,
        buyer_match_count=buyer_match_count,
        disposition_ready_count=disposition_ready,
        compliance_blocked_count=compliance_blocked,
        compliance_needs_review_count=compliance_needs_review,
        manual_drafts_count=manual_drafts,
        blocked_actions_count=blocked_actions,
    )
    session.add(metric)

    for bottleneck_type, count in bottlenecks.items():
        session.add(
            ClientWeeklyBottleneck(
                id=f"client-bottleneck-{uuid4().hex[:10]}",
                workspace_id=workspace.id,
                report_id=report.id,
                bottleneck_type=bottleneck_type,
                bottleneck_summary=_bottleneck_summary(bottleneck_type),
                affected_lead_count=count,
                severity="high" if count >= 2 else "medium",
                recommended_fix=_bottleneck_fix(bottleneck_type),
            )
        )

    for action in _build_weekly_actions(session, workspace.id, report.id):
        session.add(ClientWeeklyRecommendedAction(id=f"client-weekly-action-{uuid4().hex[:10]}", workspace_id=workspace.id, report_id=report.id, **action))

    for division in _build_division_summaries(metric):
        session.add(ClientWeeklyDivisionSummary(id=f"client-division-summary-{uuid4().hex[:10]}", workspace_id=workspace.id, report_id=report.id, **division))

    report.report_status = "generated"
    report.report_title = f"{workspace.workspace_name} weekly command report"
    report.executive_summary = f"{metric.hot_leads_count} hot leads, {metric.offer_ready_count} offer-ready leads, and {metric.disposition_ready_count} disposition-ready leads are in view for this week."
    report.lead_flow_summary = f"{metric.total_leads} leads are tracked, with {metric.acquisition_ready_count} acquisition-ready and {metric.underwriting_ready_count} underwritten."
    report.acquisition_summary = f"{metric.appointment_ready_count} leads are appointment-ready while manual drafts remain manual-use only."
    report.underwriting_summary = f"{metric.evidence_missing_count} leads still need evidence before underwriting or offer confidence improves."
    report.disposition_summary = f"{metric.buyer_match_count} leads have buyer matching context and {metric.disposition_ready_count} are ready for client review."
    report.compliance_summary = f"{metric.compliance_blocked_count} leads are compliance blocked and {metric.compliance_needs_review_count} need manual review."
    report.bottleneck_summary = ", ".join(_bottleneck_summary(name) for name in bottlenecks.keys()) or "No major bottlenecks detected in the current demo records."
    report.next_week_focus = _weekly_focus(metric, bottlenecks)
    report.client_safe_summary = "Client-safe weekly report only. No revenue, ROI, buyer purchase, or outcome is guaranteed."
    report.source_basis_summary = "Built from CP2-CP6 lead, acquisition, underwriting, disposition, and compliance records only."
    report.no_revenue_guarantee = True
    report.no_roi_claim = True
    report.no_live_actions_taken = True
    report.requires_human_review = metric.compliance_blocked_count > 0 or metric.evidence_missing_count > 0
    session.add(
        ClientWeeklyReportEvent(
            id=f"client-report-event-{uuid4().hex[:10]}",
            workspace_id=workspace.id,
            report_id=report.id,
            event_type="weekly_report_generated",
            event_summary="Client Success Manager generated a deterministic weekly command report.",
            manager_name="Client Success Manager",
            client_visible=True,
        )
    )
    session.flush()


def _contact_channels_for_lead(session: Session, lead: ClientLeadProfile) -> list[str]:
    channels: list[str] = []
    if "phone" in (lead.contact_channels_present or []):
        channels.extend(["call", "sms"])
    if "email" in (lead.contact_channels_present or []):
        channels.append("email")
    channels.extend(
        record.consent_channel
        for record in _consent_records(session, lead.workspace_id, lead.id, None)
        if record.consent_channel not in {"unknown", ""}
    )
    return sorted(set(channels or ["call"]))


def _contact_channels_for_buyer(session: Session, buyer: ClientBuyerProfile) -> list[str]:
    channels: list[str] = []
    if buyer.communication_preference in {"call", "sms", "email"}:
        channels.append(buyer.communication_preference)
    channels.extend(
        record.consent_channel
        for record in _consent_records(session, buyer.workspace_id, None, buyer.id)
        if record.consent_channel not in {"unknown", ""}
    )
    return sorted(set(channels or ["email"]))


def _message_source_text(
    session: Session,
    workspace_id: str,
    source_draft_type: str,
    source_draft_id: str | None,
    lead_id: str | None,
    buyer_id: str | None,
) -> str:
    if source_draft_id:
        if source_draft_type == "seller_follow_up":
            draft = session.get(ClientFollowUpDraft, source_draft_id)
            if draft and draft.workspace_id == workspace_id:
                return draft.draft_body
        if source_draft_type == "buyer_outreach":
            draft = session.get(ClientBuyerOutreachDraft, source_draft_id)
            if draft and draft.workspace_id == workspace_id:
                return draft.draft_body
    if lead_id and source_draft_type == "seller_follow_up":
        draft = next(iter(_follow_up_drafts(session, workspace_id, lead_id)), None)
        if draft:
            return draft.draft_body
    if lead_id and source_draft_type == "buyer_outreach":
        draft = next(iter(_buyer_outreach_drafts(session, workspace_id, lead_id)), None)
        if draft:
            return draft.draft_body
    if buyer_id and source_draft_type == "buyer_outreach":
        drafts = (
            session.query(ClientBuyerOutreachDraft)
            .filter(ClientBuyerOutreachDraft.workspace_id == workspace_id, ClientBuyerOutreachDraft.buyer_id == buyer_id)
            .order_by(desc(ClientBuyerOutreachDraft.created_at))
            .all()
        )
        if drafts:
            return drafts[0].draft_body
    return "Manual-use draft only."


def _select_contact_status(statuses: list[ClientSafeContactStatus], source_draft_type: str) -> ClientSafeContactStatus | None:
    preferred = "email"
    if source_draft_type == "seller_follow_up":
        preferred = "call"
    elif source_draft_type == "buyer_outreach":
        preferred = "email"
    return next((item for item in statuses if item.channel == preferred), statuses[0] if statuses else None)


def _contact_reason_summary(
    status: str,
    channel: str,
    consent: ClientContactConsentRecord | None,
    active_opt_out: ClientContactOptOutRecord | None,
) -> str:
    if active_opt_out is not None:
        return f"{channel} channel is blocked because an opt-out is active."
    if consent is None:
        return f"{channel} channel needs manual consent tracking before even manual-use drafting is considered safe."
    if status == "safe_for_manual_use":
        return f"{channel} channel is cleared for manual-use drafting only. No live communication is allowed."
    return f"{channel} channel needs review because consent is {consent.consent_status}."


def _lead_stage(
    offer_gate: ClientOfferReadinessGate,
    disposition_gate: ClientDispositionReadinessGate,
    compliance_statuses: list[ClientSafeContactStatus],
) -> str:
    if any(item.status in {"blocked", "opted_out"} for item in compliance_statuses):
        return "compliance"
    if disposition_gate.readiness_status == "ready_for_client_review":
        return "disposition"
    if offer_gate.readiness_status == "ready_for_client_review":
        return "offer_readiness"
    if offer_gate.readiness_status == "underwriting_review_needed":
        return "underwriting"
    if offer_gate.readiness_status == "evidence_missing":
        return "acquisition"
    return "lead_intelligence"


def _lead_status_summary(
    score: ClientLeadIntelligenceScore,
    offer_gate: ClientOfferReadinessGate,
    disposition_gate: ClientDispositionReadinessGate,
    compliance_statuses: list[ClientSafeContactStatus],
) -> str:
    if any(item.status in {"blocked", "opted_out"} for item in compliance_statuses):
        return "Compliance gate is blocked until opt-out or manual review issues are resolved."
    if disposition_gate.readiness_status == "buyer_demand_missing":
        return "Lead is underwritten but still needs buyer demand evidence."
    if offer_gate.readiness_status != "ready_for_client_review":
        return f"Offer readiness is {offer_gate.readiness_status}."
    return f"Lead priority {score.final_priority_score} is ready for the next client-review step."


def _weekly_next_step(
    score: ClientLeadIntelligenceScore,
    offer_gate: ClientOfferReadinessGate,
    disposition_gate: ClientDispositionReadinessGate,
    compliance_statuses: list[ClientSafeContactStatus],
) -> str:
    if any(item.status in {"blocked", "opted_out"} for item in compliance_statuses):
        return "Review consent or opt-out records before using any draft manually."
    if "arv_estimate_missing" in offer_gate.block_reasons or "repair_estimate_missing" in offer_gate.block_reasons:
        return "Add ARV and repair evidence before more underwriting review."
    if "buyer_demand_evidence_missing" in disposition_gate.block_reasons:
        return "Add buyer demand evidence or stronger buy box matches."
    if "thin_or_negative_offer_margin" in offer_gate.block_reasons:
        return "Hold the lead until price or evidence changes improve margin."
    return _action_label(score.recommended_next_action)


def _bottleneck_summary(bottleneck_type: str) -> str:
    mapping = {
        "missing_contact_data": "Missing seller contact data is slowing manual follow-up prep.",
        "missing_seller_motivation": "Seller motivation details are incomplete.",
        "missing_arv": "ARV evidence is missing from underwriting-ready leads.",
        "missing_repairs": "Repair estimates are missing from underwriting review.",
        "buyer_demand_missing": "Buyer demand evidence is missing for leads that are otherwise progressing.",
        "compliance_blocked": "Compliance review is blocking manual-use readiness.",
        "human_review_needed": "Human review flags are stacking up.",
        "thin_margin": "Thin deal margin is blocking offer or disposition readiness.",
        "stale_follow_up": "Manual follow-up drafts exist without newer review.",
        "unclear_buy_box": "Buyer buy boxes are too unclear for high-confidence matching.",
    }
    return mapping.get(bottleneck_type, "Manual review bottleneck detected.")


def _bottleneck_fix(bottleneck_type: str) -> str:
    mapping = {
        "missing_contact_data": "Collect confirmed seller contact details and log consent manually.",
        "missing_seller_motivation": "Use the acquisition brief and question plan to capture motivation and timeline.",
        "missing_arv": "Add manual ARV evidence before another underwriting pass.",
        "missing_repairs": "Add repair notes before another underwriting pass.",
        "buyer_demand_missing": "Add buyer demand evidence or stronger buy box matches before disposition review.",
        "compliance_blocked": "Review consent, opt-out, and channel placeholders before using any manual draft.",
        "human_review_needed": "Work the human-review queue before adding more manual drafts.",
        "thin_margin": "Hold or re-evaluate the opportunity after better data arrives.",
        "stale_follow_up": "Refresh manual follow-up drafts with current lead context.",
        "unclear_buy_box": "Clarify buyer preferences and proof-of-funds posture manually.",
    }
    return mapping.get(bottleneck_type, "Review the relevant division queue.")


def _weekly_focus(metric: ClientWeeklyReportMetricSnapshot, bottlenecks: dict[str, int]) -> str:
    if bottlenecks.get("missing_arv") or bottlenecks.get("missing_repairs"):
        return "Tighten underwriting inputs first, then revisit offer readiness."
    if bottlenecks.get("buyer_demand_missing"):
        return "Collect buyer demand evidence before spending more time on blocked disposition leads."
    if metric.compliance_needs_review_count or metric.compliance_blocked_count:
        return "Resolve consent and opt-out questions before any manual outreach planning."
    return "Advance the hottest client-safe leads through manual review in order of score and readiness."


def _build_weekly_actions(session: Session, workspace_id: str, report_id: str) -> list[dict[str, object]]:
    report_rollups = _weekly_lead_rollups(session, workspace_id, report_id)
    actions: list[dict[str, object]] = []
    for rollup in report_rollups[:5]:
        action_type = "human_review"
        if rollup.top_blocker == "missing_arv_or_repairs":
            action_type = "add_evidence"
        elif rollup.top_blocker == "buyer_demand_missing":
            action_type = "add_buyer_demand_evidence"
        elif rollup.top_blocker == "compliance_review_needed":
            action_type = "review_compliance"
        elif rollup.current_stage == "acquisition":
            action_type = "call_seller"
        actions.append(
            {
                "action_type": action_type,
                "action_summary": rollup.recommended_next_step,
                "priority": rollup.priority_level if rollup.priority_level in {"low", "medium", "high", "urgent"} else "medium",
                "related_lead_id": rollup.lead_id,
                "related_buyer_id": None,
                "due_window": "this_week" if rollup.priority_level != "urgent" else "today",
                "client_safe": True,
            }
        )
    return actions


def _build_division_summaries(metric: ClientWeeklyReportMetricSnapshot) -> list[dict[str, object]]:
    lead_health = "strong" if metric.hot_leads_count and metric.evidence_missing_count <= 1 else "watch" if metric.total_leads else "blocked"
    acquisition_health = "strong" if metric.appointment_ready_count else "watch" if metric.manual_drafts_count else "blocked"
    underwriting_health = "strong" if metric.offer_ready_count else "watch" if metric.evidence_missing_count else "blocked"
    disposition_health = "strong" if metric.disposition_ready_count else "watch" if metric.buyer_match_count else "blocked"
    compliance_health = "blocked" if metric.compliance_blocked_count else "watch" if metric.compliance_needs_review_count else "strong"
    return [
        {
            "division_name": "Lead Intelligence",
            "health_status": lead_health,
            "summary": "Lead intelligence remains deterministic and workspace-scoped.",
            "wins": [f"{metric.hot_leads_count} hot leads identified."],
            "risks": [f"{metric.total_leads - metric.hot_leads_count} leads are below the hot threshold."],
            "next_actions": ["Work the highest-priority leads first."],
        },
        {
            "division_name": "Acquisition",
            "health_status": acquisition_health,
            "summary": "Acquisition prep is manual-use only.",
            "wins": [f"{metric.appointment_ready_count} leads are appointment-ready."],
            "risks": [f"{metric.manual_drafts_count} manual drafts still need human use and review."],
            "next_actions": ["Use the call brief and question plan before any manual outreach."],
        },
        {
            "division_name": "Underwriting",
            "health_status": underwriting_health,
            "summary": "Underwriting remains decision support only.",
            "wins": [f"{metric.underwriting_ready_count} leads have underwriting math."],
            "risks": [f"{metric.evidence_missing_count} leads still need evidence."],
            "next_actions": ["Add ARV and repair evidence where missing."],
        },
        {
            "division_name": "Disposition",
            "health_status": disposition_health,
            "summary": "Disposition remains manual-use and non-live.",
            "wins": [f"{metric.disposition_ready_count} leads are ready for client review."],
            "risks": [f"{metric.buyer_match_count - metric.disposition_ready_count if metric.buyer_match_count > metric.disposition_ready_count else 0} leads still need stronger buyer demand."],
            "next_actions": ["Improve buyer demand evidence before any manual deal preview."],
        },
        {
            "division_name": "Compliance",
            "health_status": compliance_health,
            "summary": "Compliance is a readiness gate only; no live channels are enabled.",
            "wins": [f"{metric.compliance_blocked_count} blocked manual-use contacts are clearly surfaced."],
            "risks": [f"{metric.compliance_needs_review_count} records need consent or channel review."],
            "next_actions": ["Resolve consent and opt-out questions before manual use."],
        },
    ]


def _consent_records(
    session: Session,
    workspace_id: str,
    lead_id: str | None,
    buyer_id: str | None,
) -> list[ClientContactConsentRecord]:
    query = session.query(ClientContactConsentRecord).filter(ClientContactConsentRecord.workspace_id == workspace_id)
    if lead_id is not None:
        query = query.filter(ClientContactConsentRecord.lead_id == lead_id)
    if buyer_id is not None:
        query = query.filter(ClientContactConsentRecord.buyer_id == buyer_id)
    return query.order_by(desc(ClientContactConsentRecord.created_at)).all()


def _opt_out_records(
    session: Session,
    workspace_id: str,
    lead_id: str | None,
    buyer_id: str | None,
) -> list[ClientContactOptOutRecord]:
    query = session.query(ClientContactOptOutRecord).filter(ClientContactOptOutRecord.workspace_id == workspace_id)
    if lead_id is not None:
        query = query.filter(ClientContactOptOutRecord.lead_id == lead_id)
    if buyer_id is not None:
        query = query.filter(ClientContactOptOutRecord.buyer_id == buyer_id)
    return query.order_by(desc(ClientContactOptOutRecord.created_at)).all()


def _safe_contact_statuses(
    session: Session,
    workspace_id: str,
    lead_id: str | None,
    buyer_id: str | None,
) -> list[ClientSafeContactStatus]:
    query = session.query(ClientSafeContactStatus).filter(ClientSafeContactStatus.workspace_id == workspace_id)
    if lead_id is not None:
        query = query.filter(ClientSafeContactStatus.lead_id == lead_id)
    if buyer_id is not None:
        query = query.filter(ClientSafeContactStatus.buyer_id == buyer_id)
    return query.order_by(ClientSafeContactStatus.channel).all()


def _message_risk_reviews(
    session: Session,
    workspace_id: str,
    lead_id: str | None,
    buyer_id: str | None,
) -> list[ClientMessageRiskReview]:
    query = session.query(ClientMessageRiskReview).filter(ClientMessageRiskReview.workspace_id == workspace_id)
    if lead_id is not None:
        query = query.filter(ClientMessageRiskReview.lead_id == lead_id)
    if buyer_id is not None:
        query = query.filter(ClientMessageRiskReview.buyer_id == buyer_id)
    return query.order_by(desc(ClientMessageRiskReview.created_at)).all()


def _communication_gates(
    session: Session,
    workspace_id: str,
    lead_id: str | None,
    buyer_id: str | None,
) -> list[ClientCommunicationApprovalGate]:
    query = session.query(ClientCommunicationApprovalGate).filter(ClientCommunicationApprovalGate.workspace_id == workspace_id)
    if lead_id is not None:
        query = query.filter(ClientCommunicationApprovalGate.lead_id == lead_id)
    if buyer_id is not None:
        query = query.filter(ClientCommunicationApprovalGate.buyer_id == buyer_id)
    return query.order_by(desc(ClientCommunicationApprovalGate.created_at)).all()


def _compliance_placeholders(session: Session, workspace_id: str) -> list[ClientComplianceReadinessPlaceholder]:
    return (
        session.query(ClientComplianceReadinessPlaceholder)
        .filter(ClientComplianceReadinessPlaceholder.workspace_id == workspace_id)
        .order_by(ClientComplianceReadinessPlaceholder.placeholder_type)
        .all()
    )


def _compliance_events(
    session: Session,
    workspace_id: str,
    lead_id: str | None,
    buyer_id: str | None,
) -> list[ClientComplianceDivisionEvent]:
    query = session.query(ClientComplianceDivisionEvent).filter(ClientComplianceDivisionEvent.workspace_id == workspace_id)
    if lead_id is not None:
        query = query.filter(ClientComplianceDivisionEvent.lead_id == lead_id)
    if buyer_id is not None:
        query = query.filter(ClientComplianceDivisionEvent.buyer_id == buyer_id)
    return query.order_by(desc(ClientComplianceDivisionEvent.created_at)).all()


def _ensure_compliance_event(
    session: Session,
    workspace_id: str,
    lead_id: str | None,
    buyer_id: str | None,
    event_type: str,
    summary: str,
) -> None:
    event = (
        session.query(ClientComplianceDivisionEvent)
        .filter(
            ClientComplianceDivisionEvent.workspace_id == workspace_id,
            ClientComplianceDivisionEvent.lead_id == lead_id,
            ClientComplianceDivisionEvent.buyer_id == buyer_id,
            ClientComplianceDivisionEvent.event_type == event_type,
        )
        .first()
    )
    if event is None:
        event = ClientComplianceDivisionEvent(
            id=f"client-compliance-event-{uuid4().hex[:10]}",
            workspace_id=workspace_id,
            lead_id=lead_id,
            buyer_id=buyer_id,
            event_type=event_type,
        )
        session.add(event)
    event.event_summary = summary
    event.manager_name = "Compliance Manager"
    event.client_visible = True


def _weekly_reports(session: Session, workspace_id: str) -> list[ClientWeeklyCommandReport]:
    return (
        session.query(ClientWeeklyCommandReport)
        .filter(ClientWeeklyCommandReport.workspace_id == workspace_id)
        .order_by(desc(ClientWeeklyCommandReport.created_at))
        .all()
    )


def _latest_weekly_report(session: Session, workspace_id: str | None) -> ClientWeeklyCommandReport | None:
    query = session.query(ClientWeeklyCommandReport)
    if workspace_id:
        query = query.filter(ClientWeeklyCommandReport.workspace_id == workspace_id)
    return query.order_by(desc(ClientWeeklyCommandReport.created_at)).first()


def _weekly_metric_snapshots(session: Session, workspace_id: str, report_id: str) -> list[ClientWeeklyReportMetricSnapshot]:
    return (
        session.query(ClientWeeklyReportMetricSnapshot)
        .filter(ClientWeeklyReportMetricSnapshot.workspace_id == workspace_id, ClientWeeklyReportMetricSnapshot.report_id == report_id)
        .order_by(desc(ClientWeeklyReportMetricSnapshot.created_at))
        .all()
    )


def _weekly_lead_rollups(session: Session, workspace_id: str, report_id: str) -> list[ClientWeeklyLeadStatusRollup]:
    return (
        session.query(ClientWeeklyLeadStatusRollup)
        .filter(ClientWeeklyLeadStatusRollup.workspace_id == workspace_id, ClientWeeklyLeadStatusRollup.report_id == report_id)
        .order_by(desc(ClientWeeklyLeadStatusRollup.priority_level), ClientWeeklyLeadStatusRollup.lead_name_or_address)
        .all()
    )


def _weekly_bottlenecks(session: Session, workspace_id: str, report_id: str) -> list[ClientWeeklyBottleneck]:
    return (
        session.query(ClientWeeklyBottleneck)
        .filter(ClientWeeklyBottleneck.workspace_id == workspace_id, ClientWeeklyBottleneck.report_id == report_id)
        .order_by(desc(ClientWeeklyBottleneck.affected_lead_count), ClientWeeklyBottleneck.bottleneck_type)
        .all()
    )


def _weekly_recommended_actions(session: Session, workspace_id: str, report_id: str) -> list[ClientWeeklyRecommendedAction]:
    return (
        session.query(ClientWeeklyRecommendedAction)
        .filter(ClientWeeklyRecommendedAction.workspace_id == workspace_id, ClientWeeklyRecommendedAction.report_id == report_id)
        .order_by(desc(ClientWeeklyRecommendedAction.created_at))
        .all()
    )


def _weekly_division_summaries(session: Session, workspace_id: str, report_id: str) -> list[ClientWeeklyDivisionSummary]:
    return (
        session.query(ClientWeeklyDivisionSummary)
        .filter(ClientWeeklyDivisionSummary.workspace_id == workspace_id, ClientWeeklyDivisionSummary.report_id == report_id)
        .order_by(ClientWeeklyDivisionSummary.division_name)
        .all()
    )


def _weekly_report_events(session: Session, workspace_id: str, report_id: str) -> list[ClientWeeklyReportEvent]:
    return (
        session.query(ClientWeeklyReportEvent)
        .filter(ClientWeeklyReportEvent.workspace_id == workspace_id, ClientWeeklyReportEvent.report_id == report_id)
        .order_by(desc(ClientWeeklyReportEvent.created_at))
        .all()
    )


def create_business_profile(session: Session, workspace_id: str, values: dict[str, object]) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    profile = ensure_business_profile(session, workspace, values=values)
    _ensure_onboarding_manager_event(session, workspace.id, "business_profile_updated", "Onboarding Manager updated the client business profile.")
    session.flush()
    return {
        "workspace": workspace_public(workspace),
        "business_profile": business_profile_public(profile),
        "safety": client_command_safety_rules(),
    }


def business_profile_detail(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    return {
        "workspace": workspace_public(workspace),
        "business_profile": business_profile_public(ensure_business_profile(session, workspace)),
        "safety": client_command_safety_rules(),
    }


def create_strategy_profile(session: Session, workspace_id: str, values: dict[str, object]) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    profile = ensure_strategy_profile(session, workspace, values=values)
    _ensure_onboarding_manager_event(session, workspace.id, "strategy_profile_updated", "Onboarding Manager updated the client strategy profile.")
    session.flush()
    return {
        "workspace": workspace_public(workspace),
        "strategy_profile": strategy_profile_public(profile),
        "safety": client_command_safety_rules(),
    }


def strategy_profile_detail(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    return {
        "workspace": workspace_public(workspace),
        "strategy_profile": strategy_profile_public(ensure_strategy_profile(session, workspace)),
        "safety": client_command_safety_rules(),
    }


def create_market_setup(session: Session, workspace_id: str, values: dict[str, object]) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    market = ClientMarketSetup(
        id=f"client-market-setup-{uuid4().hex[:10]}",
        workspace_id=workspace.id,
        market_name=str(values.get("market_name") or ""),
        state=str(values.get("state") or ""),
        counties=list(values.get("counties") or []),
        cities=list(values.get("cities") or []),
        zip_codes=list(values.get("zip_codes") or []),
        market_priority=str(values.get("market_priority") or "primary"),
        market_status=str(values.get("market_status") or "draft"),
        market_notes_summary=str(values.get("market_notes_summary") or ""),
        no_live_data_provider=True,
    )
    session.add(market)
    _ensure_onboarding_manager_event(session, workspace.id, "market_added", f"Onboarding Manager added market setup for {market.market_name or 'the workspace'}")
    session.flush()
    return {
        "workspace": workspace_public(workspace),
        "market": market_setup_public(market),
        "markets": [market_setup_public(item) for item in _market_setups(session, workspace.id)],
        "safety": client_command_safety_rules(),
    }


def market_setups_detail(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    return {
        "workspace": workspace_public(workspace),
        "markets": [market_setup_public(item) for item in _market_setups(session, workspace.id)],
        "safety": client_command_safety_rules(),
    }


def create_pipeline_setup(session: Session, workspace_id: str, values: dict[str, object]) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    pipeline = ensure_pipeline_setup(session, workspace, values=values)
    _ensure_onboarding_manager_event(session, workspace.id, "pipeline_updated", "Onboarding Manager updated the pipeline setup.")
    session.flush()
    return {
        "workspace": workspace_public(workspace),
        "pipeline": pipeline_setup_public(pipeline),
        "stages": [pipeline_stage_public(stage) for stage in _pipeline_stages(session, workspace.id, pipeline.id)],
        "safety": client_command_safety_rules(),
    }


def pipeline_setup_detail(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    pipeline = ensure_pipeline_setup(session, workspace)
    return {
        "workspace": workspace_public(workspace),
        "pipeline": pipeline_setup_public(pipeline),
        "stages": [pipeline_stage_public(stage) for stage in _pipeline_stages(session, workspace.id, pipeline.id)],
        "safety": client_command_safety_rules(),
    }


def create_default_pipeline_stages(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    pipeline = ensure_pipeline_setup(session, workspace)
    stages = ensure_default_pipeline_stages(session, workspace, pipeline)
    _ensure_onboarding_manager_event(session, workspace.id, "default_stages_added", "Onboarding Manager added default full-deal-loop stages.")
    session.flush()
    return {
        "workspace": workspace_public(workspace),
        "pipeline": pipeline_setup_public(pipeline),
        "stages": [pipeline_stage_public(stage) for stage in stages],
        "safety": client_command_safety_rules(),
    }


def pipeline_stage_detail(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    pipeline = ensure_pipeline_setup(session, workspace)
    return {
        "workspace": workspace_public(workspace),
        "pipeline": pipeline_setup_public(pipeline),
        "stages": [pipeline_stage_public(stage) for stage in _pipeline_stages(session, workspace.id, pipeline.id)],
        "safety": client_command_safety_rules(),
    }


def create_lead_source_setup(session: Session, workspace_id: str, values: dict[str, object]) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    source = ClientLeadSourceSetup(
        id=f"client-lead-source-{uuid4().hex[:10]}",
        workspace_id=workspace.id,
        source_name=str(values.get("source_name") or "Manual lead source"),
        source_type=str(values.get("source_type") or "manual_entry"),
        source_status=str(values.get("source_status") or "planned"),
        expected_monthly_leads=values.get("expected_monthly_leads"),
        cost_tracking_enabled=bool(values.get("cost_tracking_enabled") or False),
        provider_connected=False,
        no_provider_sync=True,
        notes_summary=str(values.get("notes_summary") or ""),
    )
    session.add(source)
    _ensure_onboarding_manager_event(session, workspace.id, "lead_source_added", f"Onboarding Manager added lead source {source.source_name}.")
    session.flush()
    return {
        "workspace": workspace_public(workspace),
        "lead_source": lead_source_setup_public(source),
        "lead_sources": [lead_source_setup_public(item) for item in _lead_source_setups(session, workspace.id)],
        "safety": client_command_safety_rules(),
    }


def lead_source_setups_detail(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    return {
        "workspace": workspace_public(workspace),
        "lead_sources": [lead_source_setup_public(item) for item in _lead_source_setups(session, workspace.id)],
        "safety": client_command_safety_rules(),
    }


def create_buyer_list_setup(session: Session, workspace_id: str, values: dict[str, object] | None = None) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    setup = ensure_buyer_list_setup(session, workspace, refresh=True, values=values)
    _ensure_onboarding_manager_event(session, workspace.id, "buyer_list_reviewed", "Onboarding Manager refreshed buyer list setup readiness.")
    session.flush()
    return {
        "workspace": workspace_public(workspace),
        "buyer_list_setup": buyer_list_setup_public(setup),
        "safety": client_command_safety_rules(),
    }


def buyer_list_setup_detail(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    return {
        "workspace": workspace_public(workspace),
        "buyer_list_setup": buyer_list_setup_public(ensure_buyer_list_setup(session, workspace)),
        "safety": client_command_safety_rules(),
    }


def create_team_setup_checklist(session: Session, workspace_id: str, values: dict[str, object] | None = None) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    checklist = ensure_team_setup_checklist(session, workspace, refresh=True, values=values)
    _ensure_onboarding_manager_event(session, workspace.id, "team_checklist_reviewed", "Onboarding Manager refreshed the team setup checklist.")
    session.flush()
    return {
        "workspace": workspace_public(workspace),
        "team_checklist": team_setup_checklist_public(checklist),
        "safety": client_command_safety_rules(),
    }


def team_setup_checklist_detail(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    return {
        "workspace": workspace_public(workspace),
        "team_checklist": team_setup_checklist_public(ensure_team_setup_checklist(session, workspace)),
        "safety": client_command_safety_rules(),
    }


def create_compliance_setup_checklist(session: Session, workspace_id: str, values: dict[str, object] | None = None) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    checklist = ensure_compliance_setup_checklist(session, workspace, refresh=True, values=values)
    _ensure_onboarding_manager_event(session, workspace.id, "compliance_checklist_reviewed", "Onboarding Manager refreshed the compliance setup checklist.")
    session.flush()
    return {
        "workspace": workspace_public(workspace),
        "compliance_checklist": compliance_setup_checklist_public(checklist),
        "safety": client_command_safety_rules(),
    }


def compliance_setup_checklist_detail(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    return {
        "workspace": workspace_public(workspace),
        "compliance_checklist": compliance_setup_checklist_public(ensure_compliance_setup_checklist(session, workspace)),
        "safety": client_command_safety_rules(),
    }


def create_first_leads_checklist(session: Session, workspace_id: str, values: dict[str, object] | None = None) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    checklist = ensure_first_lead_import_checklist(session, workspace, refresh=True, values=values)
    _ensure_onboarding_manager_event(session, workspace.id, "first_leads_reviewed", "Onboarding Manager refreshed the first-leads checklist.")
    session.flush()
    return {
        "workspace": workspace_public(workspace),
        "first_leads_checklist": first_lead_import_checklist_public(checklist),
        "safety": client_command_safety_rules(),
    }


def first_leads_checklist_detail(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    return {
        "workspace": workspace_public(workspace),
        "first_leads_checklist": first_lead_import_checklist_public(ensure_first_lead_import_checklist(session, workspace)),
        "safety": client_command_safety_rules(),
    }


def create_readiness_score(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    score = ensure_workspace_readiness_score(session, workspace, refresh=True)
    session.flush()
    return {
        "workspace": workspace_public(workspace),
        "readiness_score": workspace_readiness_public(score),
        "blockers": [activation_blocker_public(item) for item in _activation_blockers(session, workspace.id)],
        "safety": client_command_safety_rules(),
    }


def readiness_score_detail(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    return {
        "workspace": workspace_public(workspace),
        "readiness_score": workspace_readiness_public(ensure_workspace_readiness_score(session, workspace)),
        "blockers": [activation_blocker_public(item) for item in _activation_blockers(session, workspace.id)],
        "safety": client_command_safety_rules(),
    }


def onboarding_blockers_detail(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    ensure_workspace_readiness_score(session, workspace)
    return {
        "workspace": workspace_public(workspace),
        "blockers": [activation_blocker_public(item) for item in _activation_blockers(session, workspace.id)],
        "safety": client_command_safety_rules(),
    }


def create_go_live_gate(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    gate = ensure_go_live_gate(session, workspace, refresh=True)
    session.flush()
    return {
        "workspace": workspace_public(workspace),
        "go_live_gate": go_live_gate_public(gate),
        "safety": client_command_safety_rules(),
    }


def go_live_gate_detail(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    return {
        "workspace": workspace_public(workspace),
        "go_live_gate": go_live_gate_public(ensure_go_live_gate(session, workspace)),
        "safety": client_command_safety_rules(),
    }


def create_first_weekly_cycle_readiness(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    readiness = ensure_first_weekly_cycle_readiness(session, workspace, refresh=True)
    session.flush()
    return {
        "workspace": workspace_public(workspace),
        "first_weekly_cycle_readiness": first_weekly_cycle_readiness_public(readiness),
        "safety": client_command_safety_rules(),
    }


def first_weekly_cycle_readiness_detail(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    return {
        "workspace": workspace_public(workspace),
        "first_weekly_cycle_readiness": first_weekly_cycle_readiness_public(ensure_first_weekly_cycle_readiness(session, workspace)),
        "safety": client_command_safety_rules(),
    }


def create_onboarding_task(session: Session, workspace_id: str, values: dict[str, object]) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    task = ClientOnboardingTask(
        id=f"client-onboarding-task-{uuid4().hex[:10]}",
        workspace_id=workspace.id,
        task_title=str(values.get("task_title") or "Review onboarding blocker"),
        task_description=str(values.get("task_description") or ""),
        task_category=str(values.get("task_category") or "review"),
        task_status=str(values.get("task_status") or "todo"),
        priority=str(values.get("priority") or "medium"),
        owner_role=str(values.get("owner_role") or "onboarding_manager"),
        due_window=str(values.get("due_window") or "this_week"),
        related_blocker_id=values.get("related_blocker_id"),
        client_safe=True,
    )
    session.add(task)
    _ensure_onboarding_manager_event(session, workspace.id, "task_added", f"Onboarding Manager added task: {task.task_title}.")
    session.flush()
    return {
        "workspace": workspace_public(workspace),
        "task": onboarding_task_public(task),
        "tasks": [onboarding_task_public(item) for item in _onboarding_tasks(session, workspace.id)],
        "safety": client_command_safety_rules(),
    }


def onboarding_tasks_detail(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    tasks = ensure_onboarding_tasks(session, workspace)
    return {
        "workspace": workspace_public(workspace),
        "tasks": [onboarding_task_public(item) for item in tasks],
        "safety": client_command_safety_rules(),
    }


def onboarding_tasks_blocked(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientOnboardingTask).filter(ClientOnboardingTask.task_status == "blocked")
    if workspace_id:
        query = query.filter(ClientOnboardingTask.workspace_id == workspace_id)
    tasks = query.order_by(desc(ClientOnboardingTask.created_at)).all()
    return {
        "workspace_id": workspace_id,
        "tasks": [onboarding_task_public(item) for item in tasks],
        "safety": client_command_safety_rules(),
    }


def onboarding_tasks_urgent(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    query = session.query(ClientOnboardingTask).filter(ClientOnboardingTask.priority == "urgent")
    if workspace_id:
        query = query.filter(ClientOnboardingTask.workspace_id == workspace_id)
    tasks = query.order_by(desc(ClientOnboardingTask.created_at)).all()
    return {
        "workspace_id": workspace_id,
        "tasks": [onboarding_task_public(item) for item in tasks],
        "safety": client_command_safety_rules(),
    }


def create_onboarding_report(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    report = ensure_onboarding_report(session, workspace, refresh=True)
    session.flush()
    return {
        "workspace": workspace_public(workspace),
        "report": onboarding_report_public(report),
        "timeline": [onboarding_timeline_event_public(item) for item in ensure_onboarding_timeline(session, workspace)],
        "manager_events": [onboarding_manager_event_public(item) for item in ensure_onboarding_manager_events(session, workspace)],
        "safety": client_command_safety_rules(),
    }


def onboarding_report_detail(session: Session, workspace_id: str) -> dict[str, object]:
    workspace = _workspace_or_404(session, workspace_id)
    return {
        "workspace": workspace_public(workspace),
        "report": onboarding_report_public(ensure_onboarding_report(session, workspace)),
        "timeline": [onboarding_timeline_event_public(item) for item in ensure_onboarding_timeline(session, workspace)],
        "manager_events": [onboarding_manager_event_public(item) for item in ensure_onboarding_manager_events(session, workspace)],
        "safety": client_command_safety_rules(),
    }


def onboarding_overview(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    workspaces = [_workspace_or_404(session, workspace_id)] if workspace_id else session.query(ClientWorkspace).order_by(ClientWorkspace.workspace_name).all()
    items = []
    for workspace in workspaces:
        readiness = ensure_workspace_readiness_score(session, workspace)
        gate = ensure_go_live_gate(session, workspace)
        weekly = ensure_first_weekly_cycle_readiness(session, workspace)
        blockers = _activation_blockers(session, workspace.id)
        tasks = ensure_onboarding_tasks(session, workspace)
        items.append(
            {
                "workspace": workspace_public(workspace),
                "readiness_score": workspace_readiness_public(readiness),
                "go_live_gate": go_live_gate_public(gate),
                "first_weekly_cycle_readiness": first_weekly_cycle_readiness_public(weekly),
                "top_blocker": activation_blocker_public(blockers[0]) if blockers else None,
                "next_task": onboarding_task_public(tasks[0]) if tasks else None,
            }
        )
    return {
        "workspace_id": workspace_id,
        "overview": items,
        "safety": client_command_safety_rules(),
    }


def onboarding_activation_board(session: Session, workspace_id: str | None = None) -> dict[str, object]:
    workspaces = [_workspace_or_404(session, workspace_id)] if workspace_id else session.query(ClientWorkspace).order_by(ClientWorkspace.workspace_name).all()
    board = []
    for workspace in workspaces:
        readiness = ensure_workspace_readiness_score(session, workspace)
        gate = ensure_go_live_gate(session, workspace)
        blockers = _activation_blockers(session, workspace.id)
        board.append(
            {
                "workspace": workspace_public(workspace),
                "readiness_score": workspace_readiness_public(readiness),
                "go_live_gate": go_live_gate_public(gate),
                "blockers": [activation_blocker_public(item) for item in blockers],
                "tasks": [onboarding_task_public(item) for item in ensure_onboarding_tasks(session, workspace)],
            }
        )
    return {
        "workspace_id": workspace_id,
        "activation_board": board,
        "safety": client_command_safety_rules(),
    }


def ensure_business_profile(
    session: Session,
    workspace: ClientWorkspace,
    values: dict[str, object] | None = None,
) -> ClientBusinessProfile:
    profile = session.query(ClientBusinessProfile).filter(ClientBusinessProfile.workspace_id == workspace.id).first()
    if profile is None:
        profile = ClientBusinessProfile(
            id=f"client-business-profile-{uuid4().hex[:10]}",
            workspace_id=workspace.id,
        )
        session.add(profile)
    if values:
        for key in [
            "business_name",
            "operator_name",
            "business_type",
            "experience_level",
            "primary_market",
            "secondary_markets",
            "monthly_lead_goal",
            "monthly_contract_goal",
            "preferred_strategy",
            "current_tools_summary",
            "biggest_bottleneck",
        ]:
            if key in values and values.get(key) is not None:
                setattr(profile, key, values.get(key))
    profile.business_name = profile.business_name or workspace.client_name or workspace.workspace_name
    if not profile.primary_market and workspace.market_focus:
        profile.primary_market = workspace.market_focus[0]
    if not profile.operator_name:
        member = (
            session.query(ClientWorkspaceMember)
            .filter(ClientWorkspaceMember.workspace_id == workspace.id)
            .order_by(ClientWorkspaceMember.created_at)
            .first()
        )
        profile.operator_name = member.member_name if member else None
    profile.client_safe_summary = (
        f"{profile.business_name or workspace.workspace_name} operates as a "
        f"{(profile.business_type or 'unknown').replace('_', ' ')} in "
        f"{profile.primary_market or 'the selected market'} with a "
        f"{(profile.preferred_strategy or 'unknown').replace('_', ' ')} focus."
    )
    session.flush()
    return profile


def ensure_strategy_profile(
    session: Session,
    workspace: ClientWorkspace,
    values: dict[str, object] | None = None,
) -> ClientStrategyProfile:
    profile = session.query(ClientStrategyProfile).filter(ClientStrategyProfile.workspace_id == workspace.id).first()
    if profile is None:
        profile = ClientStrategyProfile(
            id=f"client-strategy-profile-{uuid4().hex[:10]}",
            workspace_id=workspace.id,
        )
        session.add(profile)
    if values:
        for key in [
            "strategy_type",
            "acquisition_channels",
            "disposition_channels",
            "target_property_types",
            "target_seller_situations",
            "target_price_band_min",
            "target_price_band_max",
            "assignment_fee_target",
            "risk_tolerance",
            "operating_mode",
            "strategy_summary",
            "requires_human_review",
        ]:
            if key in values and values.get(key) is not None:
                setattr(profile, key, values.get(key))
    if not profile.strategy_type or profile.strategy_type == "unknown":
        business = ensure_business_profile(session, workspace)
        if business.preferred_strategy and business.preferred_strategy != "unknown":
            profile.strategy_type = business.preferred_strategy
    if not profile.strategy_summary:
        profile.strategy_summary = (
            f"Client strategy is {(profile.strategy_type or 'unknown').replace('_', ' ')} "
            f"with acquisition channels {', '.join(profile.acquisition_channels or ['manual'])}."
        )
    session.flush()
    return profile


def ensure_pipeline_setup(
    session: Session,
    workspace: ClientWorkspace,
    values: dict[str, object] | None = None,
) -> ClientPipelineSetup:
    pipeline = session.query(ClientPipelineSetup).filter(ClientPipelineSetup.workspace_id == workspace.id).first()
    if pipeline is None:
        pipeline = ClientPipelineSetup(
            id=f"client-pipeline-setup-{uuid4().hex[:10]}",
            workspace_id=workspace.id,
            pipeline_name="Prime2 Full Deal Loop",
            pipeline_type="full_deal_loop",
            setup_status="draft",
        )
        session.add(pipeline)
    if values:
        for key in ["pipeline_name", "pipeline_type", "setup_status"]:
            if key in values and values.get(key) is not None:
                setattr(pipeline, key, values.get(key))
    pipeline.stage_count = len(_pipeline_stages(session, workspace.id, pipeline.id))
    pipeline.client_safe_summary = "Client-safe setup only; pipeline stages support controlled/manual Prime2 operation."
    session.flush()
    return pipeline


def ensure_default_pipeline_stages(
    session: Session,
    workspace: ClientWorkspace,
    pipeline: ClientPipelineSetup,
) -> list[ClientPipelineStageTemplate]:
    existing = _pipeline_stages(session, workspace.id, pipeline.id)
    if not existing:
        for stage in _default_pipeline_stage_templates():
            session.add(
                ClientPipelineStageTemplate(
                    id=f"client-pipeline-stage-{uuid4().hex[:10]}",
                    workspace_id=workspace.id,
                    pipeline_setup_id=pipeline.id,
                    stage_name=stage["stage_name"],
                    stage_order=stage["stage_order"],
                    stage_type=stage["stage_type"],
                    required_before_next=stage["required_before_next"],
                    manager_owner=stage["manager_owner"],
                    client_safe=True,
                )
            )
        pipeline.setup_status = "configured"
    pipeline.stage_count = len(_pipeline_stages(session, workspace.id, pipeline.id)) or len(_default_pipeline_stage_templates())
    session.flush()
    return _pipeline_stages(session, workspace.id, pipeline.id)


def ensure_buyer_list_setup(
    session: Session,
    workspace: ClientWorkspace,
    refresh: bool = False,
    values: dict[str, object] | None = None,
) -> ClientBuyerListSetup:
    setup = session.query(ClientBuyerListSetup).filter(ClientBuyerListSetup.workspace_id == workspace.id).first()
    if setup is None:
        setup = ClientBuyerListSetup(
            id=f"client-buyer-list-setup-{uuid4().hex[:10]}",
            workspace_id=workspace.id,
        )
        session.add(setup)
    if refresh or not setup.recommended_next_step:
        buyers = (
            session.query(ClientBuyerProfile)
            .filter(ClientBuyerProfile.workspace_id == workspace.id)
            .order_by(ClientBuyerProfile.buyer_name)
            .all()
        )
        setup.buyer_count = len(buyers)
        setup.active_buyer_count = len([buyer for buyer in buyers if buyer.active_status == "active"])
        clear = 0
        funding = 0
        needs_review = 0
        for buyer in buyers:
            boxes = _buyer_buy_boxes(session, workspace.id, buyer.id)
            clear_box = any(
                (box.zip_codes or box.property_types or box.max_purchase_price or box.min_purchase_price)
                for box in boxes
            )
            if clear_box:
                clear += 1
            if buyer.funding_status in {"verified", "stated"} or buyer.proof_of_funds_status in {"verified", "requested"}:
                funding += 1
            if buyer.active_status == "needs_review" or not clear_box or buyer.communication_preference == "unknown":
                needs_review += 1
        setup.clear_buy_box_count = clear
        setup.missing_buy_box_count = max(0, setup.buyer_count - clear)
        setup.verified_or_stated_funding_count = funding
        setup.needs_review_count = needs_review
        if setup.buyer_count == 0:
            setup.setup_status = "not_started"
            setup.recommended_next_step = "Add at least one buyer profile before using disposition workflows."
        elif setup.active_buyer_count and setup.clear_buy_box_count:
            setup.setup_status = "ready_for_matching"
            setup.recommended_next_step = "Use buyer profiles as manual matching context only."
        elif setup.clear_buy_box_count == 0:
            setup.setup_status = "buyer_profiles_started"
            setup.recommended_next_step = "Clarify buy boxes before relying on buyer matching."
        else:
            setup.setup_status = "needs_review"
            setup.recommended_next_step = "Review buyers missing clear buy boxes or funding posture."
    if values:
        if values.get("setup_status"):
            setup.setup_status = str(values["setup_status"])
        if values.get("recommended_next_step"):
            setup.recommended_next_step = str(values["recommended_next_step"])
    setup.no_buyer_contacted = True
    setup.no_campaign_started = True
    session.flush()
    return setup


def ensure_team_setup_checklist(
    session: Session,
    workspace: ClientWorkspace,
    refresh: bool = False,
    values: dict[str, object] | None = None,
) -> ClientTeamSetupChecklist:
    checklist = session.query(ClientTeamSetupChecklist).filter(ClientTeamSetupChecklist.workspace_id == workspace.id).first()
    if checklist is None:
        checklist = ClientTeamSetupChecklist(
            id=f"client-team-checklist-{uuid4().hex[:10]}",
            workspace_id=workspace.id,
        )
        session.add(checklist)
    if refresh or not checklist.recommended_next_step:
        roles = (
            session.query(ClientWorkspaceRole)
            .filter(ClientWorkspaceRole.workspace_id == workspace.id)
            .all()
        )
        members = (
            session.query(ClientWorkspaceMember)
            .filter(ClientWorkspaceMember.workspace_id == workspace.id)
            .all()
        )
        role_map = {role.id: role for role in roles}
        checklist.team_member_count = len(members)
        checklist.owner_added = False
        checklist.acquisition_role_added = False
        checklist.underwriting_role_added = False
        checklist.disposition_role_added = False
        checklist.compliance_owner_added = False
        checklist.client_success_owner_added = False
        for member in members:
            role = role_map.get(member.role_id)
            name = f"{member.member_name} {(role.role_name if role else '')} {(role.role_key if role else '')}".lower()
            perms = set(member_permissions(member, role))
            if "client_command.admin" in perms or "owner" in name or "operator" in name:
                checklist.owner_added = True
            if "acquisition" in name:
                checklist.acquisition_role_added = True
            if "underwriting" in name:
                checklist.underwriting_role_added = True
            if "disposition" in name or "buyer" in name:
                checklist.disposition_role_added = True
            if "compliance" in name:
                checklist.compliance_owner_added = True
            if "success" in name:
                checklist.client_success_owner_added = True
        missing_roles = []
        if not checklist.owner_added:
            missing_roles.append("owner")
        if not checklist.acquisition_role_added:
            missing_roles.append("acquisition_role")
        if not checklist.underwriting_role_added:
            missing_roles.append("underwriting_role")
        if not checklist.disposition_role_added:
            missing_roles.append("disposition_role")
        if not checklist.compliance_owner_added:
            missing_roles.append("compliance_owner")
        if not checklist.client_success_owner_added:
            missing_roles.append("client_success_owner")
        checklist.missing_roles = missing_roles
        if not checklist.owner_added:
            checklist.setup_status = "not_started"
            checklist.recommended_next_step = "Add an owner/operator record before manual operation readiness can clear."
        elif missing_roles:
            checklist.setup_status = "partial"
            checklist.recommended_next_step = "Document missing roles or note that the owner will cover them manually."
        else:
            checklist.setup_status = "ready"
            checklist.recommended_next_step = "Team structure is documented for controlled/manual Prime2 operation."
    if values:
        for key in [
            "owner_added",
            "acquisition_role_added",
            "underwriting_role_added",
            "disposition_role_added",
            "compliance_owner_added",
            "client_success_owner_added",
        ]:
            if key in values and values.get(key) is not None:
                setattr(checklist, key, bool(values.get(key)))
        if values.get("recommended_next_step"):
            checklist.recommended_next_step = str(values["recommended_next_step"])
    session.flush()
    return checklist


def ensure_compliance_setup_checklist(
    session: Session,
    workspace: ClientWorkspace,
    refresh: bool = False,
    values: dict[str, object] | None = None,
) -> ClientComplianceSetupChecklist:
    checklist = session.query(ClientComplianceSetupChecklist).filter(ClientComplianceSetupChecklist.workspace_id == workspace.id).first()
    if checklist is None:
        checklist = ClientComplianceSetupChecklist(
            id=f"client-compliance-setup-{uuid4().hex[:10]}",
            workspace_id=workspace.id,
        )
        session.add(checklist)
    if refresh or not checklist.recommended_next_step:
        placeholders = _compliance_placeholders(session, workspace.id)
        consent_records = session.query(ClientContactConsentRecord).filter(ClientContactConsentRecord.workspace_id == workspace.id).all()
        opt_out_records = session.query(ClientContactOptOutRecord).filter(ClientContactOptOutRecord.workspace_id == workspace.id).all()
        placeholder_types = {item.placeholder_type for item in placeholders}
        checklist.consent_policy_documented = bool(consent_records) or "consent_capture_policy" in placeholder_types
        checklist.opt_out_process_documented = bool(opt_out_records) or "email_unsubscribe" in placeholder_types
        checklist.dnc_placeholder_created = "dnc_check" in placeholder_types
        checklist.ten_dlc_placeholder_created = "ten_dlc_registration" in placeholder_types
        checklist.email_unsubscribe_placeholder_created = "email_unsubscribe" in placeholder_types
        checklist.call_recording_notice_placeholder_created = "call_recording_notice" in placeholder_types
        team = ensure_team_setup_checklist(session, workspace)
        checklist.compliance_owner_assigned = team.compliance_owner_added or team.owner_added
        block_reasons = []
        if not checklist.consent_policy_documented:
            block_reasons.append("consent_policy_missing")
        if not checklist.opt_out_process_documented:
            block_reasons.append("opt_out_process_missing")
        if not checklist.dnc_placeholder_created:
            block_reasons.append("dnc_placeholder_missing")
        if not checklist.compliance_owner_assigned:
            block_reasons.append("compliance_owner_missing")
        checklist.block_reasons = block_reasons
        if not any([
            checklist.consent_policy_documented,
            checklist.opt_out_process_documented,
            checklist.dnc_placeholder_created,
            checklist.ten_dlc_placeholder_created,
        ]):
            checklist.setup_status = "not_started"
            checklist.recommended_next_step = "Document consent and opt-out basics before manual contact review."
        elif block_reasons:
            checklist.setup_status = "needs_review"
            checklist.recommended_next_step = "Finish compliance documentation and placeholder setup before treating contacts as ready."
        else:
            checklist.setup_status = "ready_for_manual_use"
            checklist.recommended_next_step = "Compliance placeholders are documented for manual-use review only."
    if values:
        for key in [
            "consent_policy_documented",
            "opt_out_process_documented",
            "dnc_placeholder_created",
            "ten_dlc_placeholder_created",
            "email_unsubscribe_placeholder_created",
            "call_recording_notice_placeholder_created",
            "compliance_owner_assigned",
        ]:
            if key in values and values.get(key) is not None:
                setattr(checklist, key, bool(values.get(key)))
        if values.get("recommended_next_step"):
            checklist.recommended_next_step = str(values["recommended_next_step"])
    checklist.no_provider_check = True
    checklist.no_live_registration = True
    session.flush()
    return checklist


def ensure_first_lead_import_checklist(
    session: Session,
    workspace: ClientWorkspace,
    refresh: bool = False,
    values: dict[str, object] | None = None,
) -> ClientFirstLeadImportChecklist:
    checklist = session.query(ClientFirstLeadImportChecklist).filter(ClientFirstLeadImportChecklist.workspace_id == workspace.id).first()
    if checklist is None:
        checklist = ClientFirstLeadImportChecklist(
            id=f"client-first-leads-{uuid4().hex[:10]}",
            workspace_id=workspace.id,
        )
        session.add(checklist)
    if checklist.first_10_leads_target is None:
        checklist.first_10_leads_target = 10
    if refresh or not checklist.recommended_next_step:
        leads = session.query(ClientLeadProfile).filter(ClientLeadProfile.workspace_id == workspace.id).all()
        scores = _scores_for_workspace(session, workspace.id)
        checklist.current_lead_count = len(leads)
        checklist.leads_with_contact_count = len([lead for lead in leads if lead.contact_channels_present])
        checklist.leads_with_property_address_count = len([lead for lead in leads if lead.property_address_summary])
        checklist.leads_with_motivation_count = len([lead for lead in leads if lead.motivation_signals])
        checklist.leads_with_condition_count = len([lead for lead in leads if lead.client_notes or lead.distress_signals])
        checklist.leads_with_timeline_count = len([lead for lead in leads if lead.timeline_days and lead.timeline_days <= 120])
        checklist.leads_scored_count = len(scores)
        checklist.hot_leads_count = len([score for score in scores if score.final_priority_score >= 78])
        missing_requirements = []
        if checklist.current_lead_count < checklist.first_10_leads_target:
            missing_requirements.append("first_10_leads_target_not_met")
        if checklist.leads_with_contact_count < checklist.current_lead_count:
            missing_requirements.append("missing_contactability_data")
        if checklist.leads_with_motivation_count < checklist.current_lead_count:
            missing_requirements.append("missing_motivation_data")
        if checklist.leads_with_condition_count < checklist.current_lead_count:
            missing_requirements.append("missing_condition_data")
        if checklist.leads_with_timeline_count < checklist.current_lead_count:
            missing_requirements.append("missing_timeline_data")
        checklist.missing_requirements = missing_requirements
        if checklist.current_lead_count == 0:
            checklist.import_status = "not_started"
            checklist.recommended_next_step = "Load the first 10 leads before the first command cycle."
        elif checklist.current_lead_count >= checklist.first_10_leads_target and len(missing_requirements) <= 1:
            checklist.import_status = "ready_for_first_command_cycle"
            checklist.recommended_next_step = "Lead minimum is met for the first controlled command cycle."
        elif checklist.current_lead_count >= max(5, checklist.first_10_leads_target // 2):
            checklist.import_status = "ready_for_review"
            checklist.recommended_next_step = "Demo or partial lead batch is ready for manual review, but the first-10 target is not met yet."
        else:
            checklist.import_status = "partial"
            checklist.recommended_next_step = "Add more leads and fill missing contact, motivation, condition, and timeline data."
    if values:
        if values.get("first_10_leads_target") is not None:
            checklist.first_10_leads_target = int(values["first_10_leads_target"])
        if values.get("recommended_next_step"):
            checklist.recommended_next_step = str(values["recommended_next_step"])
    checklist.no_external_import = True
    session.flush()
    return checklist


def ensure_workspace_readiness_score(
    session: Session,
    workspace: ClientWorkspace,
    refresh: bool = False,
) -> ClientWorkspaceReadinessScore:
    score = session.query(ClientWorkspaceReadinessScore).filter(ClientWorkspaceReadinessScore.workspace_id == workspace.id).first()
    if score is not None and not refresh:
        return score
    if score is None:
        score = ClientWorkspaceReadinessScore(
            id=f"client-readiness-score-{uuid4().hex[:10]}",
            workspace_id=workspace.id,
        )
        session.add(score)
    business = ensure_business_profile(session, workspace)
    strategy = ensure_strategy_profile(session, workspace)
    pipeline = ensure_pipeline_setup(session, workspace)
    buyer_setup = ensure_buyer_list_setup(session, workspace)
    team = ensure_team_setup_checklist(session, workspace)
    compliance = ensure_compliance_setup_checklist(session, workspace)
    first_leads = ensure_first_lead_import_checklist(session, workspace)
    markets = _market_setups(session, workspace.id)
    lead_sources = _lead_source_setups(session, workspace.id)
    latest_report = _latest_weekly_report(session, workspace.id)
    score.business_profile_score = _business_profile_score(business, strategy)
    score.market_setup_score = _market_setup_score(markets)
    score.pipeline_setup_score = _pipeline_setup_score(session, pipeline)
    score.lead_source_score = _lead_source_score(lead_sources)
    score.lead_import_score = _lead_import_score(first_leads)
    score.buyer_setup_score = _buyer_setup_score(buyer_setup)
    score.team_setup_score = _team_setup_score(team)
    score.compliance_setup_score = _compliance_setup_score(compliance)
    score.report_readiness_score = 100 if latest_report else 0
    weighted = (
        score.business_profile_score * 0.10
        + score.market_setup_score * 0.10
        + score.pipeline_setup_score * 0.10
        + score.lead_source_score * 0.10
        + score.lead_import_score * 0.20
        + score.buyer_setup_score * 0.15
        + score.team_setup_score * 0.10
        + score.compliance_setup_score * 0.10
        + score.report_readiness_score * 0.05
    )
    score.readiness_score = int(round(weighted))
    blockers = ensure_activation_blockers(session, workspace, refresh=True)
    critical = [item for item in blockers if item.severity == "critical" and not item.resolved]
    score.top_blockers = [item.blocker_type for item in blockers[:3]]
    if score.readiness_score <= 24:
        status = "not_started"
    elif critical:
        status = "blocked"
    elif score.readiness_score <= 79:
        status = "setup_in_progress"
    elif score.readiness_score <= 89:
        status = "ready_for_manual_operation"
    else:
        status = "ready_for_first_weekly_cycle"
    score.readiness_status = status
    score.recommended_next_step = (
        blockers[0].recommended_fix
        if blockers
        else "Workspace is ready for controlled/manual Prime2 operation."
    )
    score.no_live_actions_enabled = True
    session.flush()
    return score


def ensure_activation_blockers(
    session: Session,
    workspace: ClientWorkspace,
    refresh: bool = False,
) -> list[ClientActivationBlocker]:
    existing = _activation_blockers(session, workspace.id)
    if existing and not refresh:
        return existing
    if refresh and existing:
        session.query(ClientActivationBlocker).filter(ClientActivationBlocker.workspace_id == workspace.id).delete(synchronize_session=False)
    business = ensure_business_profile(session, workspace)
    pipeline = ensure_pipeline_setup(session, workspace)
    markets = _market_setups(session, workspace.id)
    leads = session.query(ClientLeadProfile).filter(ClientLeadProfile.workspace_id == workspace.id).all()
    lead_sources = _lead_source_setups(session, workspace.id)
    buyer_setup = ensure_buyer_list_setup(session, workspace)
    team = ensure_team_setup_checklist(session, workspace)
    compliance = ensure_compliance_setup_checklist(session, workspace)
    first_leads = ensure_first_lead_import_checklist(session, workspace)
    safe_manual_use = session.query(ClientSafeContactStatus).filter(
        ClientSafeContactStatus.workspace_id == workspace.id,
        ClientSafeContactStatus.status == "safe_for_manual_use",
    ).count()
    compliance_risks = session.query(ClientSafeContactStatus).filter(
        ClientSafeContactStatus.workspace_id == workspace.id,
        ClientSafeContactStatus.status.in_(["blocked", "needs_review", "missing_consent"]),
    ).count()
    latest_report = _latest_weekly_report(session, workspace.id)
    blockers: list[dict[str, object]] = []
    if not business.business_name or business.business_type == "unknown":
        blockers.append(
            _blocker_payload(
                "missing_business_profile",
                "critical",
                "business",
                "Business identity is incomplete for this workspace.",
                "Complete the client business profile before manual operation readiness can clear.",
            )
        )
    if not markets:
        blockers.append(
            _blocker_payload(
                "missing_market",
                "critical",
                "market",
                "No market setup is configured.",
                "Add at least one primary market with zip or city coverage.",
            )
        )
    if pipeline.stage_count == 0:
        blockers.append(
            _blocker_payload(
                "missing_pipeline",
                "critical",
                "pipeline",
                "The client pipeline has no configured stages yet.",
                "Add the default full-deal-loop stages before activation.",
            )
        )
    if not lead_sources:
        blockers.append(
            _blocker_payload(
                "missing_lead_source",
                "medium",
                "leads",
                "No lead source setup has been documented yet.",
                "Add at least one manual lead source setup record.",
            )
        )
    if not leads:
        blockers.append(
            _blocker_payload(
                "missing_leads",
                "critical",
                "leads",
                "No leads are loaded into the workspace yet.",
                "Load leads before the first command cycle.",
            )
        )
    if buyer_setup.buyer_count == 0:
        blockers.append(
            _blocker_payload(
                "missing_buyer_list",
                "critical",
                "buyers",
                "No buyer setup exists for disposition review.",
                "Add buyer profiles with clear buy boxes before relying on CP5.",
            )
        )
    elif buyer_setup.setup_status != "ready_for_matching":
        blockers.append(
            _blocker_payload(
                "missing_buyer_list",
                "medium",
                "buyers",
                "Buyer setup is present but still needs stronger buy-box clarity.",
                "Clarify buy boxes and funding posture for buyer matching.",
            )
        )
    if not team.owner_added:
        blockers.append(
            _blocker_payload(
                "missing_team_owner",
                "critical",
                "team",
                "No workspace owner/operator is documented.",
                "Add the client owner before activation can proceed.",
            )
        )
    if compliance.setup_status in {"not_started", "blocked"}:
        blockers.append(
            _blocker_payload(
                "missing_compliance_setup",
                "critical",
                "compliance",
                "Compliance setup is incomplete for manual-use operation.",
                compliance.recommended_next_step or "Document consent, opt-out, and DNC placeholders.",
            )
        )
    elif compliance.setup_status in {"partial", "needs_review"} or compliance_risks:
        blockers.append(
            _blocker_payload(
                "unsafe_contact_posture",
                "medium",
                "compliance",
                "Manual-use contact posture still needs review on one or more records.",
                "Resolve consent and opt-out questions before treating more contacts as ready.",
            )
        )
    if first_leads.current_lead_count and first_leads.current_lead_count < first_leads.first_10_leads_target:
        blockers.append(
            _blocker_payload(
                "unknown",
                "medium",
                "leads",
                "The first 10-lead target is not met yet.",
                "Continue loading or qualifying leads until the first-10 target is reached.",
            )
        )
    disposition_gaps = session.query(ClientDispositionReadinessGate).filter(
        ClientDispositionReadinessGate.workspace_id == workspace.id,
        ClientDispositionReadinessGate.readiness_status == "buyer_demand_missing",
    ).count()
    if disposition_gaps:
        blockers.append(
            _blocker_payload(
                "unknown",
                "medium",
                "buyers",
                "Some leads still need buyer demand evidence before disposition review.",
                "Add buyer demand evidence or stronger buyer matches for blocked leads.",
            )
        )
    if latest_report is None:
        blockers.append(
            _blocker_payload(
                "missing_weekly_report",
                "medium",
                "reporting",
                "No weekly client command report exists yet.",
                "Generate the first weekly report once setup basics are documented.",
            )
        )
    if compliance_risks and safe_manual_use == 0:
        blockers.append(
            _blocker_payload(
                "unsafe_contact_posture",
                "critical",
                "compliance",
                "No safe manual-use contact records exist yet.",
                "Resolve safe-contact posture before any manual outreach planning.",
            )
        )
    for payload in blockers:
        session.add(
            ClientActivationBlocker(
                id=f"client-activation-blocker-{uuid4().hex[:10]}",
                workspace_id=workspace.id,
                blocker_type=str(payload["blocker_type"]),
                severity=str(payload["severity"]),
                blocker_summary=str(payload["blocker_summary"]),
                affected_area=str(payload["affected_area"]),
                recommended_fix=str(payload["recommended_fix"]),
                resolved=False,
            )
        )
    session.flush()
    return _activation_blockers(session, workspace.id)


def ensure_go_live_gate(
    session: Session,
    workspace: ClientWorkspace,
    refresh: bool = False,
) -> ClientGoLiveReadinessGate:
    gate = session.query(ClientGoLiveReadinessGate).filter(ClientGoLiveReadinessGate.workspace_id == workspace.id).first()
    if gate is not None and not refresh:
        return gate
    if gate is None:
        gate = ClientGoLiveReadinessGate(
            id=f"client-go-live-gate-{uuid4().hex[:10]}",
            workspace_id=workspace.id,
        )
        session.add(gate)
    readiness = ensure_workspace_readiness_score(session, workspace, refresh=refresh)
    blockers = ensure_activation_blockers(session, workspace, refresh=refresh)
    critical = [item for item in blockers if item.severity == "critical" and not item.resolved]
    gate.readiness_score_snapshot = readiness.readiness_score
    gate.required_before_manual_operation = [item.blocker_type for item in blockers]
    gate.block_reasons = [item.blocker_summary for item in blockers]
    if critical:
        gate.gate_status = "blocked"
        gate.approved_scope = "none"
    elif readiness.readiness_score >= 90 and ensure_first_weekly_cycle_readiness(session, workspace).ready_for_first_weekly_cycle:
        gate.gate_status = "ready_for_first_weekly_cycle"
        gate.approved_scope = "first_weekly_cycle_only"
    elif readiness.readiness_score >= 80:
        gate.gate_status = "ready_for_manual_operation"
        gate.approved_scope = "manual_operation_only"
    else:
        gate.gate_status = "not_ready"
        gate.approved_scope = "none"
    gate.no_live_communication = True
    gate.no_provider_execution = True
    gate.no_billing_action = True
    gate.no_contract_action = True
    gate.no_campaign_action = True
    gate.requires_human_review = bool(blockers)
    gate.client_safe_summary = "Manual operation readiness only - no live communication, provider execution, billing, contracts, or campaigns are enabled."
    session.flush()
    return gate


def ensure_first_weekly_cycle_readiness(
    session: Session,
    workspace: ClientWorkspace,
    refresh: bool = False,
) -> ClientFirstWeeklyCycleReadiness:
    readiness = session.query(ClientFirstWeeklyCycleReadiness).filter(ClientFirstWeeklyCycleReadiness.workspace_id == workspace.id).first()
    if readiness is not None and not refresh:
        return readiness
    if readiness is None:
        readiness = ClientFirstWeeklyCycleReadiness(
            id=f"client-first-weekly-cycle-{uuid4().hex[:10]}",
            workspace_id=workspace.id,
        )
        session.add(readiness)
    buyer_setup = ensure_buyer_list_setup(session, workspace)
    compliance = ensure_compliance_setup_checklist(session, workspace)
    first_leads = ensure_first_lead_import_checklist(session, workspace)
    latest_report = _latest_weekly_report(session, workspace.id)
    readiness.lead_minimum_met = first_leads.current_lead_count >= first_leads.first_10_leads_target or (
        first_leads.current_lead_count >= 5 and latest_report is not None
    )
    readiness.buyer_setup_minimum_met = buyer_setup.clear_buy_box_count >= 1
    readiness.compliance_minimum_met = compliance.setup_status in {"ready_for_manual_use", "needs_review"} and (
        session.query(ClientSafeContactStatus)
        .filter(ClientSafeContactStatus.workspace_id == workspace.id, ClientSafeContactStatus.status == "safe_for_manual_use")
        .count()
        > 0
    )
    readiness.report_can_generate = latest_report is not None or first_leads.current_lead_count > 0
    readiness.top_missing_items = [
        label
        for label, passed in [
            ("lead_minimum", readiness.lead_minimum_met),
            ("buyer_setup", readiness.buyer_setup_minimum_met),
            ("compliance_setup", readiness.compliance_minimum_met),
            ("weekly_report", readiness.report_can_generate),
        ]
        if not passed
    ]
    readiness.ready_for_first_weekly_cycle = not readiness.top_missing_items
    readiness.recommended_next_step = (
        "Run the first weekly client command cycle in manual mode."
        if readiness.ready_for_first_weekly_cycle
        else "Resolve missing readiness items before relying on the first weekly cycle."
    )
    readiness.no_live_actions_taken = True
    session.flush()
    return readiness


def ensure_onboarding_tasks(
    session: Session,
    workspace: ClientWorkspace,
    refresh: bool = False,
) -> list[ClientOnboardingTask]:
    tasks = _onboarding_tasks(session, workspace.id)
    if tasks and not refresh:
        return tasks
    if refresh and tasks:
        session.query(ClientOnboardingTask).filter(ClientOnboardingTask.workspace_id == workspace.id).delete(synchronize_session=False)
    blockers = ensure_activation_blockers(session, workspace, refresh=refresh)
    payloads = []
    for blocker in blockers:
        payloads.append(
            {
                "task_title": blocker.recommended_fix.split(".")[0],
                "task_description": blocker.blocker_summary,
                "task_category": _task_category_for_area(blocker.affected_area),
                "task_status": "blocked" if blocker.severity == "critical" else "todo",
                "priority": "urgent" if blocker.severity == "critical" else "high" if blocker.severity == "high" else "medium",
                "owner_role": _task_owner_for_area(blocker.affected_area),
                "due_window": "before_activation" if blocker.severity == "critical" else "this_week",
                "related_blocker_id": blocker.id,
            }
        )
    if not payloads:
        payloads.append(
            {
                "task_title": "Review workspace activation board",
                "task_description": "No major blockers are present. Review readiness and keep manual-operation boundaries in place.",
                "task_category": "review",
                "task_status": "todo",
                "priority": "medium",
                "owner_role": "onboarding_manager",
                "due_window": "this_week",
                "related_blocker_id": None,
            }
        )
    for payload in payloads:
        session.add(
            ClientOnboardingTask(
                id=f"client-onboarding-task-{uuid4().hex[:10]}",
                workspace_id=workspace.id,
                task_title=str(payload["task_title"]),
                task_description=str(payload["task_description"]),
                task_category=str(payload["task_category"]),
                task_status=str(payload["task_status"]),
                priority=str(payload["priority"]),
                owner_role=str(payload["owner_role"]),
                due_window=str(payload["due_window"]),
                related_blocker_id=payload["related_blocker_id"],
                client_safe=True,
            )
        )
    session.flush()
    return _onboarding_tasks(session, workspace.id)


def ensure_onboarding_timeline(
    session: Session,
    workspace: ClientWorkspace,
    refresh: bool = False,
) -> list[ClientOnboardingTimelineEvent]:
    events = _onboarding_timeline(session, workspace.id)
    if events and not refresh:
        return events
    if refresh and events:
        session.query(ClientOnboardingTimelineEvent).filter(ClientOnboardingTimelineEvent.workspace_id == workspace.id).delete(synchronize_session=False)
    readiness = ensure_workspace_readiness_score(session, workspace, refresh=refresh)
    milestones = [
        ("workspace_created", "Workspace foundation", 15, "Client workspace foundation is in place."),
        ("setup_reviewed", "Setup review", min(45, readiness.readiness_score), "Onboarding Manager reviewed setup records and checklists."),
        ("readiness_scored", "Readiness scored", min(80, readiness.readiness_score), "Workspace readiness score was calculated for manual operation."),
        ("weekly_cycle_reviewed", "Weekly cycle readiness", readiness.readiness_score, "First weekly cycle readiness was reviewed without enabling live actions."),
    ]
    for event_type, milestone_name, progress_percent, summary in milestones:
        session.add(
            ClientOnboardingTimelineEvent(
                id=f"client-onboarding-timeline-{uuid4().hex[:10]}",
                workspace_id=workspace.id,
                event_type=event_type,
                event_summary=summary,
                milestone_name=milestone_name,
                progress_percent=int(progress_percent),
                manager_name="Onboarding Manager",
                client_visible=True,
            )
        )
    session.flush()
    return _onboarding_timeline(session, workspace.id)


def ensure_onboarding_manager_events(
    session: Session,
    workspace: ClientWorkspace,
    refresh: bool = False,
) -> list[ClientOnboardingManagerEvent]:
    events = _onboarding_manager_events(session, workspace.id)
    if events and not refresh:
        return events
    if refresh and events:
        session.query(ClientOnboardingManagerEvent).filter(ClientOnboardingManagerEvent.workspace_id == workspace.id).delete(synchronize_session=False)
    readiness = ensure_workspace_readiness_score(session, workspace, refresh=refresh)
    summaries = [
        ("onboarding_summary", "Onboarding Manager summarized the current workspace setup posture."),
        ("readiness_status", f"Onboarding Manager marked workspace readiness as {readiness.readiness_status}."),
    ]
    for event_type, summary in summaries:
        session.add(
            ClientOnboardingManagerEvent(
                id=f"client-onboarding-event-{uuid4().hex[:10]}",
                workspace_id=workspace.id,
                event_type=event_type,
                event_summary=summary,
                manager_name="Onboarding Manager",
                client_visible=True,
            )
        )
    session.flush()
    return _onboarding_manager_events(session, workspace.id)


def ensure_onboarding_report(
    session: Session,
    workspace: ClientWorkspace,
    refresh: bool = False,
) -> ClientOnboardingReport:
    report = session.query(ClientOnboardingReport).filter(ClientOnboardingReport.workspace_id == workspace.id).first()
    if report is not None and not refresh:
        return report
    if report is None:
        report = ClientOnboardingReport(
            id=f"client-onboarding-report-{uuid4().hex[:10]}",
            workspace_id=workspace.id,
        )
        session.add(report)
    readiness = ensure_workspace_readiness_score(session, workspace, refresh=refresh)
    gate = ensure_go_live_gate(session, workspace, refresh=refresh)
    first_weekly = ensure_first_weekly_cycle_readiness(session, workspace, refresh=refresh)
    blockers = ensure_activation_blockers(session, workspace, refresh=refresh)
    tasks = ensure_onboarding_tasks(session, workspace, refresh=refresh)
    report.report_status = "generated"
    report.report_title = f"{workspace.workspace_name} onboarding readiness report"
    report.executive_summary = (
        f"{workspace.workspace_name} is {readiness.readiness_status.replace('_', ' ')} with a readiness score of {readiness.readiness_score}. "
        "Prime2 remains in manual-operation mode only."
    )
    report.setup_progress_summary = (
        f"Business, market, pipeline, buyer, team, compliance, and reporting readiness are tracked in CP8 without enabling live actions."
    )
    report.readiness_summary = (
        f"Go-live gate status: {gate.gate_status}. First weekly cycle ready: {first_weekly.ready_for_first_weekly_cycle}."
    )
    report.blocker_summary = "; ".join(item.blocker_summary for item in blockers[:3]) if blockers else "No major onboarding blockers remain."
    report.next_steps_summary = "; ".join(task.task_title for task in tasks[:3]) if tasks else "Review the activation board."
    report.first_week_focus = first_weekly.recommended_next_step
    report.client_safe_summary = "Client-safe onboarding report - no revenue, ROI, or deal outcome is guaranteed."
    report.no_live_actions_enabled = True
    report.no_revenue_guarantee = True
    report.no_roi_claim = True
    session.flush()
    return report


def _business_profile_score(profile: ClientBusinessProfile, strategy: ClientStrategyProfile) -> int:
    score = 0
    score += 20 if profile.business_type != "unknown" else 0
    score += 15 if (profile.preferred_strategy != "unknown" or strategy.strategy_type != "unknown") else 0
    score += 20 if profile.primary_market else 0
    score += 15 if (profile.monthly_lead_goal or profile.monthly_contract_goal) else 0
    score += 15 if profile.biggest_bottleneck != "unknown" else 0
    score += 15 if (profile.operator_name or profile.current_tools_summary) else 0
    return min(score, 100)


def _market_setup_score(markets: list[ClientMarketSetup]) -> int:
    if not markets:
        return 0
    best = max(
        (
            (25 if market.market_status == "configured" else 10)
            + (15 if market.state else 0)
            + (20 if (market.counties or market.cities) else 0)
            + (20 if market.zip_codes else 0)
            + (20 if market.market_priority == "primary" else 10)
            for market in markets
        ),
        default=0,
    )
    return min(best, 100)


def _pipeline_setup_score(session: Session, pipeline: ClientPipelineSetup) -> int:
    if not pipeline:
        return 0
    stage_count = len(_pipeline_stages(session, pipeline.workspace_id, pipeline.id))
    if stage_count == 0:
        return 20
    return min(100, 40 + stage_count * 5 + (20 if pipeline.setup_status == "configured" else 0))


def _lead_source_score(sources: list[ClientLeadSourceSetup]) -> int:
    if not sources:
        return 0
    active = len([item for item in sources if item.source_status == "active_manual"])
    planned = len([item for item in sources if item.source_status in {"planned", "needs_setup"}])
    score = 30 + active * 25 + planned * 10
    if any(item.provider_connected for item in sources):
        score -= 20
    return max(0, min(100, score))


def _lead_import_score(checklist: ClientFirstLeadImportChecklist) -> int:
    score = 0
    score += min(40, checklist.current_lead_count * 4)
    score += min(15, checklist.leads_with_contact_count * 2)
    score += min(15, checklist.leads_with_motivation_count * 2)
    score += min(15, checklist.leads_with_condition_count * 2)
    score += min(15, checklist.hot_leads_count * 5)
    return max(0, min(100, score))


def _buyer_setup_score(setup: ClientBuyerListSetup) -> int:
    score = 0
    score += min(30, setup.buyer_count * 8)
    score += min(25, setup.clear_buy_box_count * 12)
    score += min(20, setup.verified_or_stated_funding_count * 8)
    score += 15 if setup.setup_status == "ready_for_matching" else 5 if setup.buyer_count else 0
    score -= min(20, setup.needs_review_count * 5)
    return max(0, min(100, score))


def _team_setup_score(checklist: ClientTeamSetupChecklist) -> int:
    score = 0
    score += 40 if checklist.owner_added else 0
    score += 10 if checklist.acquisition_role_added else 0
    score += 10 if checklist.underwriting_role_added else 0
    score += 10 if checklist.disposition_role_added else 0
    score += 15 if checklist.compliance_owner_added else 0
    score += 15 if checklist.client_success_owner_added else 0
    return min(score, 100)


def _compliance_setup_score(checklist: ClientComplianceSetupChecklist) -> int:
    score = 0
    score += 20 if checklist.consent_policy_documented else 0
    score += 20 if checklist.opt_out_process_documented else 0
    score += 20 if checklist.dnc_placeholder_created else 0
    score += 10 if checklist.ten_dlc_placeholder_created else 0
    score += 10 if checklist.email_unsubscribe_placeholder_created else 0
    score += 10 if checklist.call_recording_notice_placeholder_created else 0
    score += 10 if checklist.compliance_owner_assigned else 0
    return min(score, 100)


def _activation_blockers(session: Session, workspace_id: str) -> list[ClientActivationBlocker]:
    return (
        session.query(ClientActivationBlocker)
        .filter(ClientActivationBlocker.workspace_id == workspace_id)
        .order_by(
            desc(ClientActivationBlocker.severity == "critical"),
            desc(ClientActivationBlocker.severity == "high"),
            ClientActivationBlocker.affected_area,
            ClientActivationBlocker.blocker_type,
        )
        .all()
    )


def _onboarding_tasks(session: Session, workspace_id: str) -> list[ClientOnboardingTask]:
    return (
        session.query(ClientOnboardingTask)
        .filter(ClientOnboardingTask.workspace_id == workspace_id)
        .order_by(desc(ClientOnboardingTask.priority), ClientOnboardingTask.task_title)
        .all()
    )


def _onboarding_timeline(session: Session, workspace_id: str) -> list[ClientOnboardingTimelineEvent]:
    return (
        session.query(ClientOnboardingTimelineEvent)
        .filter(ClientOnboardingTimelineEvent.workspace_id == workspace_id)
        .order_by(ClientOnboardingTimelineEvent.created_at)
        .all()
    )


def _onboarding_manager_events(session: Session, workspace_id: str) -> list[ClientOnboardingManagerEvent]:
    return (
        session.query(ClientOnboardingManagerEvent)
        .filter(ClientOnboardingManagerEvent.workspace_id == workspace_id)
        .order_by(desc(ClientOnboardingManagerEvent.created_at))
        .all()
    )


def _market_setups(session: Session, workspace_id: str) -> list[ClientMarketSetup]:
    return (
        session.query(ClientMarketSetup)
        .filter(ClientMarketSetup.workspace_id == workspace_id)
        .order_by(desc(ClientMarketSetup.market_priority == "primary"), ClientMarketSetup.market_name)
        .all()
    )


def _pipeline_stages(session: Session, workspace_id: str, pipeline_setup_id: str) -> list[ClientPipelineStageTemplate]:
    return (
        session.query(ClientPipelineStageTemplate)
        .filter(
            ClientPipelineStageTemplate.workspace_id == workspace_id,
            ClientPipelineStageTemplate.pipeline_setup_id == pipeline_setup_id,
        )
        .order_by(ClientPipelineStageTemplate.stage_order)
        .all()
    )


def _lead_source_setups(session: Session, workspace_id: str) -> list[ClientLeadSourceSetup]:
    return (
        session.query(ClientLeadSourceSetup)
        .filter(ClientLeadSourceSetup.workspace_id == workspace_id)
        .order_by(ClientLeadSourceSetup.source_name)
        .all()
    )


def _default_pipeline_stage_templates() -> list[dict[str, object]]:
    return [
        {"stage_name": "New Lead", "stage_order": 1, "stage_type": "new_lead", "required_before_next": [], "manager_owner": "Lead Intelligence Manager"},
        {"stage_name": "Contact Needed", "stage_order": 2, "stage_type": "contact_needed", "required_before_next": ["lead_profile"], "manager_owner": "Lead Intelligence Manager"},
        {"stage_name": "Acquisition Prep", "stage_order": 3, "stage_type": "acquisition_prep", "required_before_next": ["contact_channels"], "manager_owner": "Acquisition Manager"},
        {"stage_name": "Appointment Ready", "stage_order": 4, "stage_type": "appointment_ready", "required_before_next": ["motivation", "timeline", "condition"], "manager_owner": "Acquisition Manager"},
        {"stage_name": "Evidence Needed", "stage_order": 5, "stage_type": "evidence_needed", "required_before_next": ["seller_notes"], "manager_owner": "Underwriting Manager"},
        {"stage_name": "Underwriting Review", "stage_order": 6, "stage_type": "underwriting_review", "required_before_next": ["arv", "repairs"], "manager_owner": "Underwriting Manager"},
        {"stage_name": "Offer Ready", "stage_order": 7, "stage_type": "offer_ready", "required_before_next": ["mao", "evidence_packet"], "manager_owner": "Underwriting Manager"},
        {"stage_name": "Buyer Matching", "stage_order": 8, "stage_type": "buyer_matching", "required_before_next": ["offer_readiness"], "manager_owner": "Disposition Manager"},
        {"stage_name": "Disposition Ready", "stage_order": 9, "stage_type": "disposition_ready", "required_before_next": ["buyer_match"], "manager_owner": "Disposition Manager"},
        {"stage_name": "Compliance Review", "stage_order": 10, "stage_type": "compliance_review", "required_before_next": ["manual_use_gate"], "manager_owner": "Compliance Manager"},
        {"stage_name": "Blocked / Needs Review", "stage_order": 11, "stage_type": "blocked", "required_before_next": [], "manager_owner": "Onboarding Manager"},
        {"stage_name": "Closed / Archived", "stage_order": 12, "stage_type": "closed_archived", "required_before_next": [], "manager_owner": "Client Success Manager"},
    ]


def _blocker_payload(
    blocker_type: str,
    severity: str,
    affected_area: str,
    summary: str,
    fix: str,
) -> dict[str, object]:
    return {
        "blocker_type": blocker_type,
        "severity": severity,
        "affected_area": affected_area,
        "blocker_summary": summary,
        "recommended_fix": fix,
    }


def _task_category_for_area(area: str) -> str:
    return {
        "business": "business_profile",
        "market": "market_setup",
        "pipeline": "pipeline_setup",
        "leads": "lead_import",
        "buyers": "buyer_list",
        "team": "team_setup",
        "compliance": "compliance",
        "reporting": "reporting",
    }.get(area, "review")


def _task_owner_for_area(area: str) -> str:
    return {
        "business": "client_owner",
        "market": "onboarding_manager",
        "pipeline": "onboarding_manager",
        "leads": "acquisition_manager",
        "buyers": "disposition_manager",
        "team": "client_success_manager",
        "compliance": "compliance_manager",
        "reporting": "client_success_manager",
    }.get(area, "onboarding_manager")


def _ensure_onboarding_manager_event(
    session: Session,
    workspace_id: str,
    event_type: str,
    summary: str,
) -> None:
    event = (
        session.query(ClientOnboardingManagerEvent)
        .filter(
            ClientOnboardingManagerEvent.workspace_id == workspace_id,
            ClientOnboardingManagerEvent.event_type == event_type,
        )
        .first()
    )
    if event is None:
        event = ClientOnboardingManagerEvent(
            id=f"client-onboarding-event-{uuid4().hex[:10]}",
            workspace_id=workspace_id,
            event_type=event_type,
        )
        session.add(event)
    event.event_summary = summary
    event.manager_name = "Onboarding Manager"
    event.client_visible = True


PLAN_FEATURE_GROUPS = [
    "onboarding",
    "lead_intelligence",
    "acquisition",
    "underwriting",
    "buyer_matching",
    "compliance",
    "weekly_reports",
    "live_communication",
    "billing",
    "admin_support",
    "pilot_mode",
    "exports",
    "integrations",
]


DEFAULT_PLAN_DEFINITIONS: list[dict[str, Any]] = [
    {
        "plan_code": "beta_demo",
        "plan_name": "Beta Demo",
        "monthly_price_placeholder": 0.0,
        "setup_fee_placeholder": 0.0,
        "is_public": False,
        "is_active": True,
        "client_safe_summary": "Demo-only plan for onboarding, scoring, and manual reviews.",
        "limits": {
            "max_workspaces": 1,
            "max_users": 2,
            "max_leads": 25,
            "max_buyers": 10,
            "max_weekly_reports": 4,
            "max_manual_drafts": 25,
            "live_communication_allowed": False,
            "billing_live_allowed": False,
            "support_console_allowed": False,
            "pilot_mode_allowed": False,
        },
        "features": {
            "onboarding": True,
            "lead_intelligence": True,
            "acquisition": True,
            "underwriting": True,
            "buyer_matching": True,
            "compliance": True,
            "weekly_reports": True,
            "live_communication": False,
            "billing": False,
            "admin_support": False,
            "pilot_mode": False,
            "exports": False,
            "integrations": False,
        },
    },
    {
        "plan_code": "starter",
        "plan_name": "Starter",
        "monthly_price_placeholder": 99.0,
        "setup_fee_placeholder": 0.0,
        "is_public": True,
        "is_active": True,
        "client_safe_summary": "Starter plan for manual investor command workflows.",
        "limits": {
            "max_workspaces": 1,
            "max_users": 3,
            "max_leads": 100,
            "max_buyers": 40,
            "max_weekly_reports": 8,
            "max_manual_drafts": 100,
            "live_communication_allowed": False,
            "billing_live_allowed": False,
            "support_console_allowed": False,
            "pilot_mode_allowed": False,
        },
        "features": {
            "onboarding": True,
            "lead_intelligence": True,
            "acquisition": True,
            "underwriting": True,
            "buyer_matching": True,
            "compliance": True,
            "weekly_reports": True,
            "live_communication": False,
            "billing": False,
            "admin_support": False,
            "pilot_mode": False,
            "exports": True,
            "integrations": False,
        },
    },
    {
        "plan_code": "pro",
        "plan_name": "Pro",
        "monthly_price_placeholder": 249.0,
        "setup_fee_placeholder": 99.0,
        "is_public": True,
        "is_active": True,
        "client_safe_summary": "Pro plan for expanded manual operations and guarded pilot readiness.",
        "limits": {
            "max_workspaces": 2,
            "max_users": 6,
            "max_leads": 500,
            "max_buyers": 200,
            "max_weekly_reports": 24,
            "max_manual_drafts": 400,
            "live_communication_allowed": True,
            "billing_live_allowed": False,
            "support_console_allowed": False,
            "pilot_mode_allowed": True,
        },
        "features": {
            "onboarding": True,
            "lead_intelligence": True,
            "acquisition": True,
            "underwriting": True,
            "buyer_matching": True,
            "compliance": True,
            "weekly_reports": True,
            "live_communication": True,
            "billing": False,
            "admin_support": False,
            "pilot_mode": True,
            "exports": True,
            "integrations": True,
        },
    },
    {
        "plan_code": "command",
        "plan_name": "Command",
        "monthly_price_placeholder": 499.0,
        "setup_fee_placeholder": 149.0,
        "is_public": True,
        "is_active": True,
        "client_safe_summary": "Command plan for tightly controlled live communication and support review.",
        "limits": {
            "max_workspaces": 5,
            "max_users": 12,
            "max_leads": 1500,
            "max_buyers": 600,
            "max_weekly_reports": 60,
            "max_manual_drafts": 1200,
            "live_communication_allowed": True,
            "billing_live_allowed": True,
            "support_console_allowed": True,
            "pilot_mode_allowed": True,
        },
        "features": {feature: True for feature in PLAN_FEATURE_GROUPS},
    },
    {
        "plan_code": "managed_growth",
        "plan_name": "Managed Growth",
        "monthly_price_placeholder": 999.0,
        "setup_fee_placeholder": 499.0,
        "is_public": False,
        "is_active": True,
        "client_safe_summary": "Managed plan for coached pilots and controlled live lanes.",
        "limits": {
            "max_workspaces": 10,
            "max_users": 25,
            "max_leads": 5000,
            "max_buyers": 1500,
            "max_weekly_reports": 120,
            "max_manual_drafts": 3000,
            "live_communication_allowed": True,
            "billing_live_allowed": True,
            "support_console_allowed": True,
            "pilot_mode_allowed": True,
        },
        "features": {feature: True for feature in PLAN_FEATURE_GROUPS},
    },
    {
        "plan_code": "enterprise_custom",
        "plan_name": "Enterprise Custom",
        "monthly_price_placeholder": 0.0,
        "setup_fee_placeholder": 0.0,
        "is_public": False,
        "is_active": True,
        "client_safe_summary": "Custom enterprise plan with explicit commercial review required.",
        "limits": {
            "max_workspaces": 100,
            "max_users": 200,
            "max_leads": 50000,
            "max_buyers": 10000,
            "max_weekly_reports": 500,
            "max_manual_drafts": 20000,
            "live_communication_allowed": True,
            "billing_live_allowed": True,
            "support_console_allowed": True,
            "pilot_mode_allowed": True,
        },
        "features": {feature: True for feature in PLAN_FEATURE_GROUPS},
    },
]


def _generate_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:10]}"


def _hash_value(*parts: str) -> str:
    return sha256("|".join(parts).encode("utf-8")).hexdigest()


def _latest(query):
    return query.order_by(desc(query.column_descriptions[0]["entity"].created_at)).first()


def _ensure_plan_catalog_scaffolding(session: Session) -> None:
    if session.query(app_models.ClientPlanCatalog).count():
        return

    for definition in DEFAULT_PLAN_DEFINITIONS:
        plan = app_models.ClientPlanCatalog(
            id=f"client-plan-{definition['plan_code']}",
            plan_name=definition["plan_name"],
            plan_code=definition["plan_code"],
            monthly_price_placeholder=definition["monthly_price_placeholder"],
            setup_fee_placeholder=definition["setup_fee_placeholder"],
            is_public=definition["is_public"],
            is_active=definition["is_active"],
            client_safe_summary=definition["client_safe_summary"],
            no_live_billing=True,
            no_payment_collected=True,
        )
        limit = app_models.ClientPlanLimit(
            id=f"client-plan-limit-{definition['plan_code']}",
            plan_code=definition["plan_code"],
            **definition["limits"],
        )
        session.add(plan)
        session.add(limit)
        for feature_key in PLAN_FEATURE_GROUPS:
            session.add(
                app_models.ClientPlanFeature(
                    id=f"client-plan-feature-{definition['plan_code']}-{feature_key}",
                    plan_code=definition["plan_code"],
                    feature_group=feature_key,
                    feature_key=feature_key,
                    feature_name=feature_key.replace("_", " ").title(),
                    allowed=bool(definition["features"].get(feature_key, False)),
                    feature_summary=f"{definition['plan_name']} {'allows' if definition['features'].get(feature_key, False) else 'blocks'} {feature_key.replace('_', ' ')}.",
                )
            )
    session.flush()


def _plan_record(session: Session, plan_code: str) -> tuple[Any, Any]:
    _ensure_plan_catalog_scaffolding(session)
    plan = session.query(app_models.ClientPlanCatalog).filter_by(plan_code=plan_code).first()
    limit = session.query(app_models.ClientPlanLimit).filter_by(plan_code=plan_code).first()
    if plan is None or limit is None:
        raise ValueError(f"Client plan not found: {plan_code}")
    return plan, limit


def create_plan_catalog(session: Session, values: dict[str, object]) -> dict[str, object]:
    _ensure_plan_catalog_scaffolding(session)
    plan_code = str(values.get("plan_code") or "custom").lower()
    existing = session.query(app_models.ClientPlanCatalog).filter_by(plan_code=plan_code).first()
    if existing is not None:
        existing.plan_name = str(values.get("plan_name") or existing.plan_name)
        existing.monthly_price_placeholder = float(values.get("monthly_price_placeholder") or existing.monthly_price_placeholder)
        existing.setup_fee_placeholder = float(values.get("setup_fee_placeholder") or existing.setup_fee_placeholder)
        existing.is_public = bool(values.get("is_public", existing.is_public))
        existing.is_active = bool(values.get("is_active", existing.is_active))
        existing.client_safe_summary = str(values.get("client_safe_summary") or existing.client_safe_summary)
        session.flush()
        return {"plan": client_command_sanitizer.plan_catalog_public(existing)}
    plan = app_models.ClientPlanCatalog(
        id=f"client-plan-{plan_code}",
        plan_name=str(values.get("plan_name") or plan_code.replace("_", " ").title()),
        plan_code=plan_code,
        monthly_price_placeholder=float(values.get("monthly_price_placeholder") or 0),
        setup_fee_placeholder=float(values.get("setup_fee_placeholder") or 0),
        is_public=bool(values.get("is_public", False)),
        is_active=bool(values.get("is_active", True)),
        client_safe_summary=str(values.get("client_safe_summary") or ""),
    )
    session.add(plan)
    if session.query(app_models.ClientPlanLimit).filter_by(plan_code=plan_code).first() is None:
        session.add(
            app_models.ClientPlanLimit(
                id=f"client-plan-limit-{plan_code}",
                plan_code=plan_code,
            )
        )
    session.flush()
    return {"plan": client_command_sanitizer.plan_catalog_public(plan)}


def plan_catalog(session: Session) -> dict[str, object]:
    _ensure_plan_catalog_scaffolding(session)
    plans = session.query(app_models.ClientPlanCatalog).order_by(app_models.ClientPlanCatalog.plan_name).all()
    return {
        "plans": [client_command_sanitizer.plan_catalog_public(plan) for plan in plans],
        "safety": client_command_safety_rules(),
    }


def plan_features(session: Session) -> dict[str, object]:
    _ensure_plan_catalog_scaffolding(session)
    features = session.query(app_models.ClientPlanFeature).order_by(
        app_models.ClientPlanFeature.plan_code,
        app_models.ClientPlanFeature.feature_key,
    ).all()
    return {"features": [client_command_sanitizer.plan_feature_public(item) for item in features]}


def plan_limits(session: Session) -> dict[str, object]:
    _ensure_plan_catalog_scaffolding(session)
    limits = session.query(app_models.ClientPlanLimit).order_by(app_models.ClientPlanLimit.plan_code).all()
    return {"limits": [client_command_sanitizer.plan_limit_public(item) for item in limits]}


def _latest_plan_assignment(session: Session, workspace_id: str):
    return (
        session.query(app_models.ClientWorkspacePlanAssignment)
        .filter(app_models.ClientWorkspacePlanAssignment.workspace_id == workspace_id)
        .order_by(desc(app_models.ClientWorkspacePlanAssignment.created_at))
        .first()
    )


def _current_billing_readiness(session: Session, workspace_id: str):
    return (
        session.query(app_models.ClientBillingReadinessRecord)
        .filter(app_models.ClientBillingReadinessRecord.workspace_id == workspace_id)
        .order_by(desc(app_models.ClientBillingReadinessRecord.created_at))
        .first()
    )


def create_plan_assignment(session: Session, workspace_id: str, values: dict[str, object]) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    _ensure_plan_catalog_scaffolding(session)
    plan_code = str(values.get("plan_code") or "beta_demo")
    plan, _ = _plan_record(session, plan_code)
    assignment = _latest_plan_assignment(session, workspace_id)
    if assignment is None:
        assignment = app_models.ClientWorkspacePlanAssignment(
            id=_generate_id("client-plan-assignment"),
            workspace_id=workspace_id,
        )
        session.add(assignment)
    assignment.plan_code = plan_code
    assignment.plan_name = str(values.get("plan_name") or plan.plan_name)
    assignment.assignment_status = str(values.get("assignment_status") or "active")
    assignment.client_safe_summary = str(values.get("client_safe_summary") or f"{assignment.plan_name} assigned for client-safe feature gating.")
    assignment.no_live_billing = True
    assignment.no_payment_collected = True
    session.flush()
    _ensure_plan_gate_event(session, workspace_id, "plan_assignment", f"Workspace assigned to {assignment.plan_name}.")
    return {"plan_assignment": client_command_sanitizer.plan_assignment_public(assignment)}


def plan_assignment_detail(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    _ensure_plan_catalog_scaffolding(session)
    assignment = _latest_plan_assignment(session, workspace_id)
    if assignment is None:
        return create_plan_assignment(session, workspace_id, {"plan_code": "beta_demo"})
    return {"plan_assignment": client_command_sanitizer.plan_assignment_public(assignment)}


def _usage_counts(session: Session, workspace_id: str) -> dict[str, int]:
    return {
        "leads_count": session.query(ClientLeadProfile).filter_by(workspace_id=workspace_id).count(),
        "buyers_count": session.query(ClientBuyerProfile).filter_by(workspace_id=workspace_id).count(),
        "users_count": session.query(ClientWorkspaceMember).filter_by(workspace_id=workspace_id).count(),
        "weekly_reports_count": session.query(ClientWeeklyCommandReport).filter_by(workspace_id=workspace_id).count(),
        "manual_drafts_count": session.query(ClientFollowUpDraft).filter_by(workspace_id=workspace_id).count()
        + session.query(ClientBuyerOutreachDraft).filter_by(workspace_id=workspace_id).count(),
        "compliance_gates_count": session.query(ClientCommunicationApprovalGate).filter_by(workspace_id=workspace_id).count(),
        "live_attempts_count": session.query(app_models.ClientCommunicationSendAttempt).filter_by(workspace_id=workspace_id).count(),
        "billing_attempts_count": session.query(app_models.ClientBillingAttempt).filter_by(workspace_id=workspace_id).count(),
    }


def _seat_usage_records(session: Session, workspace_id: str) -> list[Any]:
    records: list[Any] = []
    members = session.query(ClientWorkspaceMember).filter_by(workspace_id=workspace_id).all()
    for member in members:
        role = session.get(ClientWorkspaceRole, member.role_id) if member.role_id else None
        record = (
            session.query(app_models.ClientSeatUsageRecord)
            .filter_by(workspace_id=workspace_id, member_id=member.id)
            .first()
        )
        if record is None:
            record = app_models.ClientSeatUsageRecord(
                id=_generate_id("client-seat"),
                workspace_id=workspace_id,
                member_id=member.id,
            )
            session.add(record)
        record.seat_label = member.member_name
        record.seat_status = member.member_status
        record.role_name = role.role_name if role else ""
        record.counts_against_limit = member.member_status != "inactive"
        records.append(record)
    session.flush()
    return records


def recalculate_usage(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    counts = _usage_counts(session, workspace_id)
    counter = (
        session.query(app_models.ClientUsageCounter)
        .filter(app_models.ClientUsageCounter.workspace_id == workspace_id)
        .first()
    )
    if counter is None:
        counter = app_models.ClientUsageCounter(
            id=_generate_id("client-usage"),
            workspace_id=workspace_id,
        )
        session.add(counter)
    for key, value in counts.items():
        setattr(counter, key, value)
    seat_records = _seat_usage_records(session, workspace_id)
    session.flush()
    return {
        "usage": client_command_sanitizer.usage_counter_public(counter),
        "seat_usage": [client_command_sanitizer.seat_usage_public(item) for item in seat_records],
    }


def usage_detail(session: Session, workspace_id: str) -> dict[str, object]:
    return recalculate_usage(session, workspace_id)


def create_billing_readiness_record(session: Session, workspace_id: str, values: dict[str, object]) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    record = _current_billing_readiness(session, workspace_id)
    if record is None:
        record = app_models.ClientBillingReadinessRecord(
            id=_generate_id("client-billing-readiness"),
            workspace_id=workspace_id,
        )
        session.add(record)
    record.readiness_status = str(values.get("readiness_status") or record.readiness_status or "setup_needed")
    record.customer_info_collected = bool(values.get("customer_info_collected", record.customer_info_collected))
    record.billing_contact_collected = bool(values.get("billing_contact_collected", record.billing_contact_collected))
    record.tax_info_placeholder = bool(values.get("tax_info_placeholder", record.tax_info_placeholder))
    record.terms_acknowledgment_placeholder = bool(values.get("terms_acknowledgment_placeholder", record.terms_acknowledgment_placeholder))
    record.notes_summary = str(values.get("notes_summary") or record.notes_summary)
    record.no_provider_call = True
    record.no_payment_collected = True
    record.no_invoice_created = True
    session.flush()
    return {"billing_readiness": client_command_sanitizer.billing_readiness_record_public(record)}


def billing_readiness_detail(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    record = _current_billing_readiness(session, workspace_id)
    if record is None:
        return create_billing_readiness_record(session, workspace_id, {})
    return {"billing_readiness": client_command_sanitizer.billing_readiness_record_public(record)}


def create_subscription_placeholder(session: Session, workspace_id: str, values: dict[str, object]) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    placeholder = (
        session.query(app_models.ClientSubscriptionPlaceholder)
        .filter(app_models.ClientSubscriptionPlaceholder.workspace_id == workspace_id)
        .order_by(desc(app_models.ClientSubscriptionPlaceholder.created_at))
        .first()
    )
    if placeholder is None:
        placeholder = app_models.ClientSubscriptionPlaceholder(
            id=_generate_id("client-subscription"),
            workspace_id=workspace_id,
        )
        session.add(placeholder)
    assignment = _latest_plan_assignment(session, workspace_id)
    plan_code = str(values.get("plan_code") or (assignment.plan_code if assignment else "beta_demo"))
    placeholder.plan_code = plan_code
    placeholder.placeholder_status = str(values.get("placeholder_status") or "draft")
    placeholder.monthly_price_placeholder = float(values.get("monthly_price_placeholder") or 0)
    placeholder.setup_fee_placeholder = float(values.get("setup_fee_placeholder") or 0)
    placeholder.billing_contact_email = str(values.get("billing_contact_email") or "")
    placeholder.client_safe_summary = str(values.get("client_safe_summary") or "Plan gate only - no payment has been collected.")
    placeholder.no_live_billing = True
    placeholder.no_payment_collected = True
    session.flush()
    return {"subscription_placeholder": client_command_sanitizer.subscription_placeholder_public(placeholder)}


def subscription_placeholder_detail(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    placeholder = (
        session.query(app_models.ClientSubscriptionPlaceholder)
        .filter(app_models.ClientSubscriptionPlaceholder.workspace_id == workspace_id)
        .order_by(desc(app_models.ClientSubscriptionPlaceholder.created_at))
        .first()
    )
    if placeholder is None:
        return create_subscription_placeholder(session, workspace_id, {})
    return {"subscription_placeholder": client_command_sanitizer.subscription_placeholder_public(placeholder)}


def _required_upgrade_for_feature(feature_key: str) -> str | None:
    mapping = {
        "live_communication": "pro",
        "billing": "command",
        "admin_support": "command",
        "pilot_mode": "pro",
        "integrations": "pro",
        "exports": "starter",
    }
    return mapping.get(feature_key)


def _feature_allowed_for_plan(session: Session, plan_code: str, feature_key: str) -> bool:
    feature = (
        session.query(app_models.ClientPlanFeature)
        .filter_by(plan_code=plan_code, feature_key=feature_key)
        .first()
    )
    return bool(feature and feature.allowed)


def _compliance_posture_ok(session: Session, workspace_id: str) -> bool:
    blocked = session.query(ClientSafeContactStatus).filter(
        ClientSafeContactStatus.workspace_id == workspace_id,
        ClientSafeContactStatus.status.in_(["blocked", "opted_out", "missing_consent"]),
    ).count()
    return blocked == 0


def _evaluate_feature_gate(
    session: Session,
    workspace_id: str,
    feature_key: str,
    assignment: Any,
    limit: Any,
    usage: Any,
    billing_readiness: Any,
) -> tuple[str, str, str | None]:
    if not _feature_allowed_for_plan(session, assignment.plan_code, feature_key):
        return ("blocked_by_plan", f"{feature_key.replace('_', ' ').title()} is not included in the current plan.", _required_upgrade_for_feature(feature_key))

    if feature_key == "lead_intelligence" and usage.leads_count > limit.max_leads:
        return ("blocked_by_usage_limit", "Lead limit reached for the current plan.", "starter" if assignment.plan_code == "beta_demo" else "pro")
    if feature_key == "buyer_matching" and usage.buyers_count > limit.max_buyers:
        return ("blocked_by_usage_limit", "Buyer limit reached for the current plan.", "starter" if assignment.plan_code == "beta_demo" else "pro")
    if feature_key == "weekly_reports" and usage.weekly_reports_count > limit.max_weekly_reports:
        return ("blocked_by_usage_limit", "Weekly report limit reached for the current plan.", "pro")
    if feature_key == "acquisition" and usage.manual_drafts_count > limit.max_manual_drafts:
        return ("blocked_by_usage_limit", "Manual draft limit reached for the current plan.", "pro")
    if feature_key == "live_communication":
        if not limit.live_communication_allowed:
            return ("blocked_by_plan", "Live communication is blocked by the current plan.", "pro")
        if not _compliance_posture_ok(session, workspace_id):
            return ("blocked_by_compliance", "Compliance posture is not clear enough for future live communication review.", None)
    if feature_key == "billing":
        if not limit.billing_live_allowed:
            return ("blocked_by_plan", "Billing is blocked by the current plan.", "command")
        if billing_readiness.readiness_status != "ready_for_future_billing_gate":
            return ("blocked_by_billing_readiness", "Billing readiness must be completed before future billing review.", "command")
    if feature_key == "admin_support" and not limit.support_console_allowed:
        return ("blocked_by_plan", "Admin support console is blocked by the current plan.", "command")
    if feature_key == "pilot_mode" and not limit.pilot_mode_allowed:
        return ("blocked_by_plan", "Pilot mode is blocked by the current plan.", "pro")
    return ("allowed", f"{feature_key.replace('_', ' ').title()} is allowed for the current plan and readiness posture.", None)


def evaluate_feature_gates(session: Session, workspace_id: str, feature_key: str | None = None) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    assignment = _latest_plan_assignment(session, workspace_id)
    if assignment is None:
        assignment = create_plan_assignment(session, workspace_id, {"plan_code": "beta_demo"})["plan_assignment"]
        assignment = _latest_plan_assignment(session, workspace_id)
    _, limit = _plan_record(session, assignment.plan_code)
    usage = recalculate_usage(session, workspace_id)["usage"]
    usage_counter = session.query(app_models.ClientUsageCounter).filter_by(workspace_id=workspace_id).first()
    billing_readiness = _current_billing_readiness(session, workspace_id)
    if billing_readiness is None:
        create_billing_readiness_record(session, workspace_id, {})
        billing_readiness = _current_billing_readiness(session, workspace_id)

    keys = [feature_key] if feature_key else PLAN_FEATURE_GROUPS
    evaluations: list[dict[str, object]] = []
    for key in keys:
        gate = (
            session.query(app_models.ClientFeatureGateEvaluation)
            .filter_by(workspace_id=workspace_id, feature_key=key)
            .first()
        )
        if gate is None:
            gate = app_models.ClientFeatureGateEvaluation(
                id=_generate_id("client-feature-gate"),
                workspace_id=workspace_id,
                feature_key=key,
            )
            session.add(gate)
        status, reason, upgrade = _evaluate_feature_gate(
            session,
            workspace_id,
            key,
            assignment,
            limit,
            usage_counter,
            billing_readiness,
        )
        gate.gate_status = status
        gate.reason_summary = reason
        gate.required_upgrade_plan = upgrade
        gate.no_live_action = True
        evaluations.append(client_command_sanitizer.feature_gate_public(gate))
    session.flush()
    _ensure_plan_upgrade_recommendation(session, workspace_id)
    return {"workspace_id": workspace_id, "feature_gates": evaluations, "usage": usage}


def feature_gate_list(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    if session.query(app_models.ClientFeatureGateEvaluation).filter_by(workspace_id=workspace_id).count() == 0:
        return evaluate_feature_gates(session, workspace_id)
    gates = (
        session.query(app_models.ClientFeatureGateEvaluation)
        .filter_by(workspace_id=workspace_id)
        .order_by(app_models.ClientFeatureGateEvaluation.feature_key)
        .all()
    )
    return {
        "workspace_id": workspace_id,
        "feature_gates": [client_command_sanitizer.feature_gate_public(gate) for gate in gates],
    }


def _ensure_plan_upgrade_recommendation(session: Session, workspace_id: str) -> Any:
    assignment = _latest_plan_assignment(session, workspace_id)
    if assignment is None:
        return None
    gates = session.query(app_models.ClientFeatureGateEvaluation).filter_by(workspace_id=workspace_id).all()
    blocked_features = [gate.feature_key for gate in gates if gate.gate_status != "allowed"]
    usage = session.query(app_models.ClientUsageCounter).filter_by(workspace_id=workspace_id).first()
    pressure: list[str] = []
    if usage:
        if assignment.plan_code == "beta_demo" and usage.leads_count >= 20:
            pressure.append("lead_capacity_near_demo_limit")
        if usage.manual_drafts_count >= 20:
            pressure.append("manual_draft_volume_rising")
    current_index = [item["plan_code"] for item in DEFAULT_PLAN_DEFINITIONS].index(assignment.plan_code) if assignment.plan_code in [item["plan_code"] for item in DEFAULT_PLAN_DEFINITIONS] else 0
    target_code = assignment.plan_code
    for blocked in blocked_features:
        upgrade = _required_upgrade_for_feature(blocked)
        if upgrade and upgrade in [item["plan_code"] for item in DEFAULT_PLAN_DEFINITIONS]:
            if [item["plan_code"] for item in DEFAULT_PLAN_DEFINITIONS].index(upgrade) > current_index:
                target_code = upgrade
                current_index = [item["plan_code"] for item in DEFAULT_PLAN_DEFINITIONS].index(upgrade)
    if target_code == assignment.plan_code and pressure:
        target_code = "starter" if assignment.plan_code == "beta_demo" else assignment.plan_code
    recommendation = (
        session.query(app_models.ClientPlanUpgradeRecommendation)
        .filter_by(workspace_id=workspace_id)
        .first()
    )
    if recommendation is None:
        recommendation = app_models.ClientPlanUpgradeRecommendation(
            id=_generate_id("client-plan-upgrade"),
            workspace_id=workspace_id,
        )
        session.add(recommendation)
    recommendation.current_plan_code = assignment.plan_code
    recommendation.recommended_plan_code = target_code
    recommendation.blocked_features = blocked_features
    recommendation.usage_pressure = pressure
    recommendation.reason_summary = (
        "Current plan supports the workspace." if target_code == assignment.plan_code and not blocked_features
        else f"Upgrade to {target_code.replace('_', ' ').title()} to clear blocked features or usage pressure."
    )
    recommendation.client_safe_summary = "Feature access is controlled by plan, readiness, and safety gates."
    session.flush()
    return recommendation


def upgrade_recommendations_detail(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    if session.query(app_models.ClientFeatureGateEvaluation).filter_by(workspace_id=workspace_id).count() == 0:
        evaluate_feature_gates(session, workspace_id)
    recommendation = _ensure_plan_upgrade_recommendation(session, workspace_id)
    return {
        "workspace_id": workspace_id,
        "upgrade_recommendation": client_command_sanitizer.upgrade_recommendation_public(recommendation) if recommendation else None,
    }


def _ensure_plan_gate_event(session: Session, workspace_id: str, feature_key: str, summary: str) -> None:
    event = app_models.ClientPlanGateEvent(
        id=_generate_id("client-plan-event"),
        workspace_id=workspace_id,
        feature_key=feature_key,
        event_type=feature_key,
        event_summary=summary,
        client_visible=True,
    )
    session.add(event)


def plans_overview(session: Session) -> dict[str, object]:
    _ensure_plan_catalog_scaffolding(session)
    plans = session.query(app_models.ClientPlanCatalog).count()
    assignments = session.query(app_models.ClientWorkspacePlanAssignment).count()
    blocked_gates = session.query(app_models.ClientFeatureGateEvaluation).filter(
        app_models.ClientFeatureGateEvaluation.gate_status != "allowed"
    ).count()
    readiness_needed = session.query(app_models.ClientBillingReadinessRecord).filter(
        app_models.ClientBillingReadinessRecord.readiness_status != "ready_for_future_billing_gate"
    ).count()
    return {
        "metrics": {
            "plan_count": plans,
            "workspace_assignments": assignments,
            "blocked_feature_gates": blocked_gates,
            "billing_readiness_needed": readiness_needed,
        },
        "plans": [client_command_sanitizer.plan_catalog_public(plan) for plan in session.query(app_models.ClientPlanCatalog).order_by(app_models.ClientPlanCatalog.plan_name).all()],
        "safety": client_command_safety_rules(),
    }


def create_communication_provider(session: Session, values: dict[str, object]) -> dict[str, object]:
    workspace_id = str(values.get("workspace_id") or "client-workspace-001")
    _workspace_or_404(session, workspace_id)
    profile = (
        session.query(app_models.ClientCommunicationProviderProfile)
        .filter_by(workspace_id=workspace_id, provider_name=str(values.get("provider_name") or "Mock Communication Provider"), channel=str(values.get("channel") or "email"))
        .first()
    )
    if profile is None:
        profile = app_models.ClientCommunicationProviderProfile(
            id=_generate_id("client-comm-provider"),
            workspace_id=workspace_id,
        )
        session.add(profile)
    profile.provider_name = str(values.get("provider_name") or profile.provider_name or "Mock Communication Provider")
    profile.provider_mode = str(values.get("provider_mode") or profile.provider_mode or "mock")
    profile.channel = str(values.get("channel") or profile.channel or "email")
    profile.enabled = bool(values.get("enabled", profile.enabled))
    profile.credential_reference_name = str(values.get("credential_reference_name") or profile.credential_reference_name)
    profile.config_summary = str(values.get("config_summary") or profile.config_summary)
    profile.secret_present = bool(profile.credential_reference_name)
    profile.client_safe_summary = f"{profile.provider_name} is configured in {profile.provider_mode} mode."
    flag = (
        session.query(app_models.ClientCommunicationLiveFlag)
        .filter_by(workspace_id=workspace_id, provider_profile_id=profile.id, channel=profile.channel)
        .first()
    )
    if flag is None:
        flag = app_models.ClientCommunicationLiveFlag(
            id=_generate_id("client-comm-flag"),
            workspace_id=workspace_id,
            provider_profile_id=profile.id,
            channel=profile.channel,
        )
        session.add(flag)
    flag.global_communication_live_enabled = bool(values.get("global_communication_live_enabled", flag.global_communication_live_enabled))
    flag.workspace_communication_live_enabled = bool(values.get("workspace_communication_live_enabled", flag.workspace_communication_live_enabled))
    flag.provider_live_enabled = bool(values.get("provider_live_enabled", flag.provider_live_enabled))
    flag.channel_live_enabled = bool(values.get("channel_live_enabled", flag.channel_live_enabled))
    session.flush()
    return {
        "provider": client_command_sanitizer.communication_provider_public(profile),
        "live_flag": client_command_sanitizer.communication_live_flag_public(flag),
    }


def communication_providers(session: Session) -> dict[str, object]:
    providers = session.query(app_models.ClientCommunicationProviderProfile).order_by(
        app_models.ClientCommunicationProviderProfile.workspace_id,
        app_models.ClientCommunicationProviderProfile.provider_name,
    ).all()
    flags = session.query(app_models.ClientCommunicationLiveFlag).order_by(
        app_models.ClientCommunicationLiveFlag.workspace_id,
        app_models.ClientCommunicationLiveFlag.channel,
    ).all()
    return {
        "providers": [client_command_sanitizer.communication_provider_public(item) for item in providers],
        "live_flags": [client_command_sanitizer.communication_live_flag_public(item) for item in flags],
    }


def _latest_safe_contact_status(session: Session, workspace_id: str, lead_id: str | None, buyer_id: str | None, channel: str):
    query = session.query(ClientSafeContactStatus).filter(
        ClientSafeContactStatus.workspace_id == workspace_id,
        ClientSafeContactStatus.channel == channel,
    )
    if lead_id:
        query = query.filter(ClientSafeContactStatus.lead_id == lead_id)
    if buyer_id:
        query = query.filter(ClientSafeContactStatus.buyer_id == buyer_id)
    return query.order_by(desc(ClientSafeContactStatus.created_at)).first()


def _latest_message_risk_review(session: Session, workspace_id: str, source_draft_id: str | None, channel: str):
    if source_draft_id is None:
        return None
    return (
        session.query(ClientMessageRiskReview)
        .filter_by(workspace_id=workspace_id, source_draft_id=source_draft_id, channel=channel)
        .order_by(desc(ClientMessageRiskReview.created_at))
        .first()
    )


def _latest_comm_gate(session: Session, workspace_id: str, source_draft_id: str | None):
    if source_draft_id is None:
        return None
    return (
        session.query(ClientCommunicationApprovalGate)
        .filter_by(workspace_id=workspace_id, source_draft_id=source_draft_id)
        .order_by(desc(ClientCommunicationApprovalGate.created_at))
        .first()
    )


def _comm_live_flag(session: Session, workspace_id: str, provider_profile_id: str | None, channel: str):
    return (
        session.query(app_models.ClientCommunicationLiveFlag)
        .filter_by(workspace_id=workspace_id, provider_profile_id=provider_profile_id, channel=channel)
        .order_by(desc(app_models.ClientCommunicationLiveFlag.created_at))
        .first()
    )


def _comm_provider(session: Session, provider_profile_id: str | None):
    if provider_profile_id is None:
        return None
    return session.get(app_models.ClientCommunicationProviderProfile, provider_profile_id)


def _workspace_ready_for_controlled_live(session: Session, workspace_id: str) -> bool:
    gate = (
        session.query(ClientGoLiveReadinessGate)
        .filter_by(workspace_id=workspace_id)
        .order_by(desc(ClientGoLiveReadinessGate.created_at))
        .first()
    )
    return bool(gate and gate.readiness_score_snapshot >= 80 and gate.gate_status in {"ready_for_manual_operation", "ready_for_first_weekly_cycle"})


def _communication_gate_status(session: Session, workspace_id: str) -> tuple[str, str]:
    evaluation = (
        session.query(app_models.ClientFeatureGateEvaluation)
        .filter_by(workspace_id=workspace_id, feature_key="live_communication")
        .order_by(desc(app_models.ClientFeatureGateEvaluation.created_at))
        .first()
    )
    if evaluation is None:
        evaluation = evaluate_feature_gates(session, workspace_id, "live_communication")["feature_gates"][0]
        evaluation = (
            session.query(app_models.ClientFeatureGateEvaluation)
            .filter_by(workspace_id=workspace_id, feature_key="live_communication")
            .order_by(desc(app_models.ClientFeatureGateEvaluation.created_at))
            .first()
        )
    return evaluation.gate_status, evaluation.reason_summary


def create_communication_readiness_check(session: Session, values: dict[str, object]) -> dict[str, object]:
    workspace_id = str(values.get("workspace_id") or "")
    _workspace_or_404(session, workspace_id)
    lead_id = str(values.get("lead_id")) if values.get("lead_id") else None
    buyer_id = str(values.get("buyer_id")) if values.get("buyer_id") else None
    source_draft_id = str(values.get("source_draft_id")) if values.get("source_draft_id") else None
    channel = str(values.get("channel") or "email")
    provider_profile_id = str(values.get("provider_profile_id")) if values.get("provider_profile_id") else None
    idempotency_key = str(values.get("idempotency_key") or _generate_id("comm-idem"))
    safe_status = _latest_safe_contact_status(session, workspace_id, lead_id, buyer_id, channel)
    risk_review = _latest_message_risk_review(session, workspace_id, source_draft_id, channel)
    comm_gate = _latest_comm_gate(session, workspace_id, source_draft_id)
    provider = _comm_provider(session, provider_profile_id)
    live_flag = _comm_live_flag(session, workspace_id, provider_profile_id, channel)
    plan_status, plan_reason = _communication_gate_status(session, workspace_id)
    dry_run_present = session.query(app_models.ClientCommunicationDryRunReceipt).filter_by(
        workspace_id=workspace_id, source_draft_id=source_draft_id, channel=channel
    ).count() > 0
    if source_draft_id:
        matching_dry_run_ids = [
            record_id
            for (record_id,) in session.query(app_models.ClientCommunicationDryRunReceipt.id)
            .filter_by(workspace_id=workspace_id, source_draft_id=source_draft_id, channel=channel)
            .all()
        ]
        approval_present = (
            session.query(app_models.ClientCommunicationSendApproval)
            .filter(
                app_models.ClientCommunicationSendApproval.workspace_id == workspace_id,
                app_models.ClientCommunicationSendApproval.dry_run_receipt_id.in_(matching_dry_run_ids),
            )
            .count()
            > 0
        ) if matching_dry_run_ids else False
    else:
        approval_present = False
    block_reasons: list[str] = []
    risk_flags: list[str] = []
    if safe_status is None or safe_status.status != "safe_for_manual_use":
        block_reasons.append("cp6_safe_contact_not_clear")
    if safe_status and safe_status.status in {"blocked", "opted_out"}:
        block_reasons.append("opt_out_or_blocked_contact")
    if risk_review is None or risk_review.review_status != "passed_for_manual_use":
        block_reasons.append("message_risk_not_passed")
    if risk_review is not None:
        risk_flags.extend(risk_review.unsafe_language_flags or [])
    if comm_gate is None or comm_gate.gate_status != "manual_use_allowed":
        block_reasons.append("communication_gate_not_manual_use_allowed")
    if plan_status != "allowed":
        block_reasons.append(f"plan_gate_{plan_status}")
        risk_flags.append(plan_reason)
    if not _workspace_ready_for_controlled_live(session, workspace_id):
        block_reasons.append("workspace_not_ready_for_controlled_live_review")
    if provider is None or not provider.enabled:
        block_reasons.append("provider_not_configured")
    if live_flag is None or not all(
        [
            live_flag.global_communication_live_enabled,
            live_flag.workspace_communication_live_enabled,
            live_flag.provider_live_enabled,
            live_flag.channel_live_enabled,
        ]
    ):
        block_reasons.append("live_flags_not_enabled")
    if not dry_run_present:
        block_reasons.append("dry_run_missing")
    if not approval_present:
        block_reasons.append("approval_missing")
    if session.query(app_models.ClientCommunicationIdempotencyRecord).filter_by(
        workspace_id=workspace_id, idempotency_key=idempotency_key
    ).count():
        block_reasons.append("idempotency_key_already_used")
    readiness = app_models.ClientCommunicationLiveReadinessCheck(
        id=_generate_id("client-comm-readiness"),
        workspace_id=workspace_id,
        lead_id=lead_id,
        buyer_id=buyer_id,
        source_draft_type=str(values.get("source_draft_type") or "unknown"),
        source_draft_id=source_draft_id,
        channel=channel,
        provider_profile_id=provider_profile_id,
        readiness_status="ready" if not block_reasons else "blocked",
        block_reasons=sorted(set(block_reasons)),
        risk_flags=sorted(set(risk_flags)),
        cp6_status_snapshot=safe_status.status if safe_status else "missing",
        cp9_gate_snapshot=plan_status,
        cp8_readiness_snapshot="adequate" if _workspace_ready_for_controlled_live(session, workspace_id) else "not_ready",
        live_flag_snapshot={
            "global": bool(live_flag.global_communication_live_enabled) if live_flag else False,
            "workspace": bool(live_flag.workspace_communication_live_enabled) if live_flag else False,
            "provider": bool(live_flag.provider_live_enabled) if live_flag else False,
            "channel": bool(live_flag.channel_live_enabled) if live_flag else False,
        },
        dry_run_present=dry_run_present,
        approval_present=approval_present,
        idempotency_key=idempotency_key,
        no_live_send=True,
    )
    session.add(readiness)
    session.flush()
    return {"readiness_check": client_command_sanitizer.communication_readiness_check_public(readiness)}


def communication_readiness_checks(session: Session) -> dict[str, object]:
    checks = session.query(app_models.ClientCommunicationLiveReadinessCheck).order_by(
        desc(app_models.ClientCommunicationLiveReadinessCheck.created_at)
    ).all()
    return {"readiness_checks": [client_command_sanitizer.communication_readiness_check_public(item) for item in checks]}


def create_communication_dry_run(session: Session, values: dict[str, object]) -> dict[str, object]:
    workspace_id = str(values.get("workspace_id") or "")
    _workspace_or_404(session, workspace_id)
    source_draft_id = str(values.get("source_draft_id") or "")
    channel = str(values.get("channel") or "email")
    summary = "Dry run does not send a message."
    receipt = app_models.ClientCommunicationDryRunReceipt(
        id=_generate_id("client-comm-dry-run"),
        workspace_id=workspace_id,
        lead_id=str(values.get("lead_id")) if values.get("lead_id") else None,
        buyer_id=str(values.get("buyer_id")) if values.get("buyer_id") else None,
        source_draft_type=str(values.get("source_draft_type") or "unknown"),
        source_draft_id=source_draft_id or None,
        channel=channel,
        provider_profile_id=str(values.get("provider_profile_id")) if values.get("provider_profile_id") else None,
        idempotency_key=str(values.get("idempotency_key") or _generate_id("comm-idem")),
        dry_run_summary=summary,
        status="created",
        content_hash=_hash_value(workspace_id, source_draft_id, channel),
        no_live_send=True,
    )
    session.add(receipt)
    session.flush()
    return {"dry_run": client_command_sanitizer.communication_dry_run_public(receipt)}


def communication_dry_runs(session: Session) -> dict[str, object]:
    receipts = session.query(app_models.ClientCommunicationDryRunReceipt).order_by(
        desc(app_models.ClientCommunicationDryRunReceipt.created_at)
    ).all()
    return {"dry_runs": [client_command_sanitizer.communication_dry_run_public(item) for item in receipts]}


def create_communication_send_approval(session: Session, values: dict[str, object]) -> dict[str, object]:
    workspace_id = str(values.get("workspace_id") or "")
    _workspace_or_404(session, workspace_id)
    approval = app_models.ClientCommunicationSendApproval(
        id=_generate_id("client-comm-approval"),
        workspace_id=workspace_id,
        readiness_check_id=str(values.get("readiness_check_id")) if values.get("readiness_check_id") else None,
        dry_run_receipt_id=str(values.get("dry_run_receipt_id")) if values.get("dry_run_receipt_id") else None,
        approval_status="approved",
        approved_by=str(values.get("approved_by") or "Prime2 Operator"),
        reason_summary=str(values.get("reason_summary") or "Approval does not send a message."),
        no_live_send=True,
    )
    session.add(approval)
    session.flush()
    return {"send_approval": client_command_sanitizer.communication_send_approval_public(approval)}


def communication_send_approvals(session: Session) -> dict[str, object]:
    approvals = session.query(app_models.ClientCommunicationSendApproval).order_by(
        desc(app_models.ClientCommunicationSendApproval.created_at)
    ).all()
    return {"send_approvals": [client_command_sanitizer.communication_send_approval_public(item) for item in approvals]}


def create_communication_send_attempt(session: Session, values: dict[str, object]) -> dict[str, object]:
    workspace_id = str(values.get("workspace_id") or "")
    _workspace_or_404(session, workspace_id)
    readiness = session.get(app_models.ClientCommunicationLiveReadinessCheck, str(values.get("readiness_check_id") or "")) if values.get("readiness_check_id") else None
    approval = session.get(app_models.ClientCommunicationSendApproval, str(values.get("approval_id") or "")) if values.get("approval_id") else None
    dry_run = session.get(app_models.ClientCommunicationDryRunReceipt, str(values.get("dry_run_receipt_id") or "")) if values.get("dry_run_receipt_id") else None
    provider = _comm_provider(session, str(values.get("provider_profile_id")) if values.get("provider_profile_id") else None)
    idempotency_key = str(values.get("idempotency_key") or (readiness.idempotency_key if readiness else _generate_id("comm-idem")))
    block_reasons = []
    if readiness is None or readiness.readiness_status != "ready":
        block_reasons.append("readiness_not_ready")
    if approval is None or approval.approval_status != "approved":
        block_reasons.append("approval_not_present")
    if dry_run is None:
        block_reasons.append("dry_run_missing")
    if session.query(app_models.ClientCommunicationIdempotencyRecord).filter_by(
        workspace_id=workspace_id, idempotency_key=idempotency_key
    ).count():
        block_reasons.append("idempotency_key_already_used")
    if provider is None:
        block_reasons.append("provider_not_configured")
    status = "blocked"
    reference = None
    if not block_reasons and provider is not None:
        mode_map = {
            "mock": "sent_mock",
            "sandbox": "sent_sandbox",
            "test": "sent_sandbox",
            "live": "sent_live",
        }
        status = mode_map.get(provider.provider_mode, "failed")
        reference = app_models.ClientCommunicationExternalMessageReference(
            id=_generate_id("client-comm-ref"),
            workspace_id=workspace_id,
            attempt_id="pending",
            provider_profile_id=provider.id,
            channel=str(values.get("channel") or (dry_run.channel if dry_run else "email")),
            provider_mode=provider.provider_mode,
            external_reference=f"{provider.provider_mode}-message-{uuid4().hex[:8]}",
            external_status=status,
            response_metadata_summary="Sanitized provider response summary.",
        )
        session.add(reference)
        session.add(
            app_models.ClientCommunicationIdempotencyRecord(
                id=_generate_id("client-comm-idempotency"),
                workspace_id=workspace_id,
                idempotency_key=idempotency_key,
                source_draft_id=dry_run.source_draft_id if dry_run else None,
                attempt_id="pending",
            )
        )
    attempt = app_models.ClientCommunicationSendAttempt(
        id=_generate_id("client-comm-attempt"),
        workspace_id=workspace_id,
        readiness_check_id=readiness.id if readiness else None,
        dry_run_receipt_id=dry_run.id if dry_run else None,
        approval_id=approval.id if approval else None,
        provider_profile_id=provider.id if provider else None,
        lead_id=str(values.get("lead_id")) if values.get("lead_id") else (readiness.lead_id if readiness else None),
        buyer_id=str(values.get("buyer_id")) if values.get("buyer_id") else (readiness.buyer_id if readiness else None),
        channel=str(values.get("channel") or (dry_run.channel if dry_run else "email")),
        source_draft_type=str(values.get("source_draft_type") or (readiness.source_draft_type if readiness else "unknown")),
        source_draft_id=str(values.get("source_draft_id")) if values.get("source_draft_id") else (readiness.source_draft_id if readiness else None),
        idempotency_key=idempotency_key,
        attempt_status=status,
        block_reasons=sorted(set(block_reasons or (readiness.block_reasons if readiness and readiness.readiness_status != "ready" else []))),
        failure_reason="" if status != "failed" else "Provider mode is unknown.",
        provider_mode=provider.provider_mode if provider else "unknown",
        request_summary="Controlled single-message gate - no bulk campaigns.",
        no_bulk=True,
    )
    session.add(attempt)
    session.flush()
    if reference is not None:
        reference.attempt_id = attempt.id
    idem = session.query(app_models.ClientCommunicationIdempotencyRecord).filter_by(
        workspace_id=workspace_id, idempotency_key=idempotency_key, attempt_id="pending"
    ).first()
    if idem is not None:
        idem.attempt_id = attempt.id
    usage = session.query(app_models.ClientUsageCounter).filter_by(workspace_id=workspace_id).first()
    if usage is not None:
        usage.live_attempts_count += 1
    session.add(
        app_models.ClientCommunicationGateEvent(
            id=_generate_id("client-comm-event"),
            workspace_id=workspace_id,
            lead_id=attempt.lead_id,
            buyer_id=attempt.buyer_id,
            event_type="send_attempt",
            event_summary=f"Communication send attempt recorded with status {attempt.attempt_status}.",
            client_visible=True,
        )
    )
    session.flush()
    return {"send_attempt": client_command_sanitizer.communication_send_attempt_public(attempt)}


def communication_send_attempts(session: Session) -> dict[str, object]:
    attempts = session.query(app_models.ClientCommunicationSendAttempt).order_by(
        desc(app_models.ClientCommunicationSendAttempt.created_at)
    ).all()
    return {"send_attempts": [client_command_sanitizer.communication_send_attempt_public(item) for item in attempts]}


def communication_external_references(session: Session) -> dict[str, object]:
    refs = session.query(app_models.ClientCommunicationExternalMessageReference).order_by(
        desc(app_models.ClientCommunicationExternalMessageReference.created_at)
    ).all()
    return {"external_references": [client_command_sanitizer.communication_external_reference_public(item) for item in refs]}


def communication_overview(session: Session) -> dict[str, object]:
    providers = session.query(app_models.ClientCommunicationProviderProfile).count()
    readiness = session.query(app_models.ClientCommunicationLiveReadinessCheck).count()
    dry_runs = session.query(app_models.ClientCommunicationDryRunReceipt).count()
    approvals = session.query(app_models.ClientCommunicationSendApproval).count()
    attempts = session.query(app_models.ClientCommunicationSendAttempt).count()
    blocked = session.query(app_models.ClientCommunicationSendAttempt).filter_by(attempt_status="blocked").count()
    refs = session.query(app_models.ClientCommunicationExternalMessageReference).count()
    return {
        "metrics": {
            "provider_profiles": providers,
            "readiness_checks": readiness,
            "dry_runs": dry_runs,
            "approvals": approvals,
            "send_attempts": attempts,
            "blocked_attempts": blocked,
            "external_references": refs,
        },
        "safety": client_command_safety_rules(),
    }


def create_billing_provider(session: Session, values: dict[str, object]) -> dict[str, object]:
    workspace_id = str(values.get("workspace_id") or "client-workspace-001")
    _workspace_or_404(session, workspace_id)
    profile = (
        session.query(app_models.ClientBillingProviderProfile)
        .filter_by(workspace_id=workspace_id, provider_name=str(values.get("provider_name") or "Mock Billing Provider"))
        .first()
    )
    if profile is None:
        profile = app_models.ClientBillingProviderProfile(
            id=_generate_id("client-billing-provider"),
            workspace_id=workspace_id,
        )
        session.add(profile)
    profile.provider_name = str(values.get("provider_name") or profile.provider_name or "Mock Billing Provider")
    profile.provider_mode = str(values.get("provider_mode") or profile.provider_mode or "mock")
    profile.enabled = bool(values.get("enabled", profile.enabled))
    profile.credential_reference_name = str(values.get("credential_reference_name") or profile.credential_reference_name)
    profile.config_summary = str(values.get("config_summary") or profile.config_summary)
    profile.secret_present = bool(profile.credential_reference_name)
    profile.supports_payment_links = bool(values.get("supports_payment_links", profile.supports_payment_links))
    profile.supports_subscriptions = bool(values.get("supports_subscriptions", profile.supports_subscriptions))
    profile.client_safe_summary = f"{profile.provider_name} is configured in {profile.provider_mode} mode."
    flag = (
        session.query(app_models.ClientBillingLiveFlag)
        .filter_by(workspace_id=workspace_id, provider_profile_id=profile.id)
        .first()
    )
    if flag is None:
        flag = app_models.ClientBillingLiveFlag(
            id=_generate_id("client-billing-flag"),
            workspace_id=workspace_id,
            provider_profile_id=profile.id,
        )
        session.add(flag)
    flag.global_billing_live_enabled = bool(values.get("global_billing_live_enabled", flag.global_billing_live_enabled))
    flag.workspace_billing_live_enabled = bool(values.get("workspace_billing_live_enabled", flag.workspace_billing_live_enabled))
    flag.provider_billing_live_enabled = bool(values.get("provider_billing_live_enabled", flag.provider_billing_live_enabled))
    flag.payment_link_live_enabled = bool(values.get("payment_link_live_enabled", flag.payment_link_live_enabled))
    flag.subscription_live_enabled = bool(values.get("subscription_live_enabled", flag.subscription_live_enabled))
    session.flush()
    return {
        "provider": client_command_sanitizer.billing_provider_public(profile),
        "live_flag": client_command_sanitizer.billing_live_flag_public(flag),
    }


def billing_providers(session: Session) -> dict[str, object]:
    providers = session.query(app_models.ClientBillingProviderProfile).order_by(
        app_models.ClientBillingProviderProfile.workspace_id,
        app_models.ClientBillingProviderProfile.provider_name,
    ).all()
    flags = session.query(app_models.ClientBillingLiveFlag).order_by(
        app_models.ClientBillingLiveFlag.workspace_id,
        app_models.ClientBillingLiveFlag.created_at,
    ).all()
    return {
        "providers": [client_command_sanitizer.billing_provider_public(item) for item in providers],
        "live_flags": [client_command_sanitizer.billing_live_flag_public(item) for item in flags],
    }


def create_billing_customer_profile(session: Session, values: dict[str, object]) -> dict[str, object]:
    workspace_id = str(values.get("workspace_id") or "")
    _workspace_or_404(session, workspace_id)
    profile = (
        session.query(app_models.ClientBillingCustomerProfile)
        .filter_by(workspace_id=workspace_id)
        .order_by(desc(app_models.ClientBillingCustomerProfile.created_at))
        .first()
    )
    if profile is None:
        profile = app_models.ClientBillingCustomerProfile(
            id=_generate_id("client-billing-customer"),
            workspace_id=workspace_id,
        )
        session.add(profile)
    profile.customer_name = str(values.get("customer_name") or profile.customer_name)
    profile.billing_email = str(values.get("billing_email") or profile.billing_email)
    profile.billing_contact_name = str(values.get("billing_contact_name") or profile.billing_contact_name)
    profile.billing_contact_collected = bool(values.get("billing_contact_collected", profile.billing_contact_collected))
    profile.tax_info_placeholder = bool(values.get("tax_info_placeholder", profile.tax_info_placeholder))
    profile.terms_acknowledgment_placeholder = bool(values.get("terms_acknowledgment_placeholder", profile.terms_acknowledgment_placeholder))
    profile.raw_card_data_present = False
    profile.client_safe_summary = "No raw card data is stored."
    session.flush()
    create_billing_readiness_record(
        session,
        workspace_id,
        {
            "customer_info_collected": bool(profile.customer_name or profile.billing_email),
            "billing_contact_collected": profile.billing_contact_collected,
            "tax_info_placeholder": profile.tax_info_placeholder,
            "terms_acknowledgment_placeholder": profile.terms_acknowledgment_placeholder,
            "readiness_status": "ready_for_future_billing_gate"
            if profile.billing_contact_collected and profile.terms_acknowledgment_placeholder
            else "setup_needed",
        },
    )
    return {"customer_profile": client_command_sanitizer.billing_customer_profile_public(profile)}


def billing_customer_profiles(session: Session) -> dict[str, object]:
    profiles = session.query(app_models.ClientBillingCustomerProfile).order_by(
        desc(app_models.ClientBillingCustomerProfile.created_at)
    ).all()
    return {"customer_profiles": [client_command_sanitizer.billing_customer_profile_public(item) for item in profiles]}


def _billing_provider(session: Session, provider_profile_id: str | None):
    if provider_profile_id is None:
        return None
    return session.get(app_models.ClientBillingProviderProfile, provider_profile_id)


def _billing_live_flag(session: Session, workspace_id: str, provider_profile_id: str | None):
    return (
        session.query(app_models.ClientBillingLiveFlag)
        .filter_by(workspace_id=workspace_id, provider_profile_id=provider_profile_id)
        .order_by(desc(app_models.ClientBillingLiveFlag.created_at))
        .first()
    )


def _billing_feature_gate(session: Session, workspace_id: str) -> tuple[str, str]:
    evaluation = (
        session.query(app_models.ClientFeatureGateEvaluation)
        .filter_by(workspace_id=workspace_id, feature_key="billing")
        .order_by(desc(app_models.ClientFeatureGateEvaluation.created_at))
        .first()
    )
    if evaluation is None:
        evaluate_feature_gates(session, workspace_id, "billing")
        evaluation = (
            session.query(app_models.ClientFeatureGateEvaluation)
            .filter_by(workspace_id=workspace_id, feature_key="billing")
            .order_by(desc(app_models.ClientFeatureGateEvaluation.created_at))
            .first()
        )
    return evaluation.gate_status, evaluation.reason_summary


def create_billing_readiness_check(session: Session, values: dict[str, object]) -> dict[str, object]:
    workspace_id = str(values.get("workspace_id") or "")
    _workspace_or_404(session, workspace_id)
    provider_profile_id = str(values.get("provider_profile_id")) if values.get("provider_profile_id") else None
    plan_assignment = _latest_plan_assignment(session, workspace_id)
    billing_readiness = _current_billing_readiness(session, workspace_id)
    provider = _billing_provider(session, provider_profile_id)
    live_flag = _billing_live_flag(session, workspace_id, provider_profile_id)
    plan_gate_status, plan_gate_reason = _billing_feature_gate(session, workspace_id)
    block_reasons: list[str] = []
    if plan_assignment is None:
        block_reasons.append("plan_assignment_missing")
    if billing_readiness is None or billing_readiness.readiness_status != "ready_for_future_billing_gate":
        block_reasons.append("billing_readiness_not_ready")
    if billing_readiness is not None and not billing_readiness.billing_contact_collected:
        block_reasons.append("billing_contact_missing")
    if provider is None or not provider.enabled:
        block_reasons.append("provider_not_configured")
    if live_flag is None or not all(
        [
            live_flag.global_billing_live_enabled,
            live_flag.workspace_billing_live_enabled,
            live_flag.provider_billing_live_enabled,
        ]
    ):
        block_reasons.append("live_flags_not_enabled")
    if plan_gate_status != "allowed":
        block_reasons.append(f"plan_gate_{plan_gate_status}")
        block_reasons.append(plan_gate_reason)
    check = app_models.ClientBillingReadinessCheck(
        id=_generate_id("client-billing-readiness-check"),
        workspace_id=workspace_id,
        plan_assignment_present=plan_assignment is not None,
        billing_readiness_status_snapshot=billing_readiness.readiness_status if billing_readiness else "not_ready",
        provider_profile_id=provider_profile_id,
        provider_mode=provider.provider_mode if provider else "unknown",
        live_flag_snapshot={
            "global": bool(live_flag.global_billing_live_enabled) if live_flag else False,
            "workspace": bool(live_flag.workspace_billing_live_enabled) if live_flag else False,
            "provider": bool(live_flag.provider_billing_live_enabled) if live_flag else False,
            "payment_link": bool(live_flag.payment_link_live_enabled) if live_flag else False,
            "subscription": bool(live_flag.subscription_live_enabled) if live_flag else False,
        },
        readiness_status="ready" if not block_reasons else "blocked",
        block_reasons=sorted(set(block_reasons)),
        no_payment_collected=True,
        no_invoice_created=True,
    )
    session.add(check)
    session.flush()
    return {"readiness_check": client_command_sanitizer.billing_readiness_check_public(check)}


def billing_readiness_checks(session: Session) -> dict[str, object]:
    checks = session.query(app_models.ClientBillingReadinessCheck).order_by(
        desc(app_models.ClientBillingReadinessCheck.created_at)
    ).all()
    return {"readiness_checks": [client_command_sanitizer.billing_readiness_check_public(item) for item in checks]}


def create_checkout_dry_run(session: Session, values: dict[str, object]) -> dict[str, object]:
    workspace_id = str(values.get("workspace_id") or "")
    _workspace_or_404(session, workspace_id)
    receipt = app_models.ClientCheckoutDryRunReceipt(
        id=_generate_id("client-billing-dry-run"),
        workspace_id=workspace_id,
        plan_code=str(values.get("plan_code") or "beta_demo"),
        attempt_type=str(values.get("attempt_type") or "checkout_session"),
        provider_profile_id=str(values.get("provider_profile_id")) if values.get("provider_profile_id") else None,
        dry_run_summary="Dry run does not charge a card.",
        idempotency_key=str(values.get("idempotency_key") or _generate_id("billing-idem")),
        amount_placeholder=float(values.get("amount_placeholder") or 0),
        status="created",
        no_payment_collected=True,
    )
    session.add(receipt)
    session.flush()
    return {"dry_run": client_command_sanitizer.checkout_dry_run_public(receipt)}


def checkout_dry_runs(session: Session) -> dict[str, object]:
    runs = session.query(app_models.ClientCheckoutDryRunReceipt).order_by(
        desc(app_models.ClientCheckoutDryRunReceipt.created_at)
    ).all()
    return {"dry_runs": [client_command_sanitizer.checkout_dry_run_public(item) for item in runs]}


def create_billing_approval(session: Session, values: dict[str, object]) -> dict[str, object]:
    workspace_id = str(values.get("workspace_id") or "")
    _workspace_or_404(session, workspace_id)
    approval = app_models.ClientBillingApproval(
        id=_generate_id("client-billing-approval"),
        workspace_id=workspace_id,
        readiness_check_id=str(values.get("readiness_check_id")) if values.get("readiness_check_id") else None,
        dry_run_receipt_id=str(values.get("dry_run_receipt_id")) if values.get("dry_run_receipt_id") else None,
        approval_status="approved",
        approved_by=str(values.get("approved_by") or "Prime2 Operator"),
        reason_summary=str(values.get("reason_summary") or "Approval does not charge a card."),
        no_payment_collected=True,
    )
    session.add(approval)
    session.flush()
    return {"approval": client_command_sanitizer.billing_approval_public(approval)}


def billing_approvals(session: Session) -> dict[str, object]:
    approvals = session.query(app_models.ClientBillingApproval).order_by(
        desc(app_models.ClientBillingApproval.created_at)
    ).all()
    return {"approvals": [client_command_sanitizer.billing_approval_public(item) for item in approvals]}


def create_billing_attempt(session: Session, values: dict[str, object]) -> dict[str, object]:
    workspace_id = str(values.get("workspace_id") or "")
    _workspace_or_404(session, workspace_id)
    provider = _billing_provider(session, str(values.get("provider_profile_id")) if values.get("provider_profile_id") else None)
    customer = session.get(app_models.ClientBillingCustomerProfile, str(values.get("customer_profile_id") or "")) if values.get("customer_profile_id") else None
    readiness = session.get(app_models.ClientBillingReadinessCheck, str(values.get("readiness_check_id") or "")) if values.get("readiness_check_id") else None
    dry_run = session.get(app_models.ClientCheckoutDryRunReceipt, str(values.get("dry_run_receipt_id") or "")) if values.get("dry_run_receipt_id") else None
    approval = session.get(app_models.ClientBillingApproval, str(values.get("approval_id") or "")) if values.get("approval_id") else None
    idempotency_key = str(values.get("idempotency_key") or (dry_run.idempotency_key if dry_run else _generate_id("billing-idem")))
    block_reasons = []
    if _latest_plan_assignment(session, workspace_id) is None:
        block_reasons.append("plan_assignment_missing")
    if readiness is None or readiness.readiness_status != "ready":
        block_reasons.append("billing_readiness_check_not_ready")
    if dry_run is None:
        block_reasons.append("dry_run_missing")
    if approval is None or approval.approval_status != "approved":
        block_reasons.append("approval_not_present")
    if provider is None or not provider.enabled:
        block_reasons.append("provider_not_configured")
    if customer is None:
        block_reasons.append("customer_profile_missing")
    if customer is not None and customer.raw_card_data_present:
        block_reasons.append("raw_card_data_forbidden")
    if session.query(app_models.ClientBillingAttempt).filter_by(workspace_id=workspace_id, idempotency_key=idempotency_key).count():
        block_reasons.append("idempotency_key_already_used")
    status = "blocked"
    if not block_reasons and provider is not None:
        status = {
            "mock": "created_mock",
            "sandbox": "created_sandbox",
            "test": "created_sandbox",
            "live": "created_live",
        }.get(provider.provider_mode, "failed")
    attempt = app_models.ClientBillingAttempt(
        id=_generate_id("client-billing-attempt"),
        workspace_id=workspace_id,
        provider_profile_id=provider.id if provider else None,
        customer_profile_id=customer.id if customer else None,
        plan_code=str(values.get("plan_code") or (_latest_plan_assignment(session, workspace_id).plan_code if _latest_plan_assignment(session, workspace_id) else "beta_demo")),
        readiness_check_id=readiness.id if readiness else None,
        dry_run_receipt_id=dry_run.id if dry_run else None,
        approval_id=approval.id if approval else None,
        attempt_type=str(values.get("attempt_type") or "checkout_session"),
        idempotency_key=idempotency_key,
        attempt_status=status,
        block_reasons=sorted(set(block_reasons or (readiness.block_reasons if readiness and readiness.readiness_status != "ready" else []))),
        provider_mode=provider.provider_mode if provider else "unknown",
        request_summary="Billing gate only - no payment occurs unless all billing gates pass.",
        no_raw_card_data=True,
    )
    session.add(attempt)
    session.flush()
    if status.startswith("created_"):
        session.add(
            app_models.ClientBillingExternalReference(
                id=_generate_id("client-billing-ref"),
                workspace_id=workspace_id,
                attempt_id=attempt.id,
                provider_mode=provider.provider_mode if provider else "unknown",
                external_reference=f"{provider.provider_mode if provider else 'mock'}-billing-{uuid4().hex[:8]}",
                external_status=status,
                response_metadata_summary="Sanitized billing provider response summary.",
            )
        )
        session.add(
            app_models.ClientBillingLedgerEntry(
                id=_generate_id("client-billing-ledger"),
                workspace_id=workspace_id,
                attempt_id=attempt.id,
                entry_type=attempt.attempt_type,
                amount_placeholder=dry_run.amount_placeholder if dry_run else 0,
                currency="USD",
                status=status,
                summary="Billing gate entry created without storing raw card data.",
                client_safe=True,
            )
        )
    else:
        session.add(
            app_models.ClientBillingLedgerEntry(
                id=_generate_id("client-billing-ledger"),
                workspace_id=workspace_id,
                attempt_id=attempt.id,
                entry_type=attempt.attempt_type,
                amount_placeholder=0,
                currency="USD",
                status="blocked",
                summary="Billing attempt blocked before any payment action.",
                client_safe=True,
            )
        )
    session.add(
        app_models.ClientBillingGateEvent(
            id=_generate_id("client-billing-event"),
            workspace_id=workspace_id,
            event_type="billing_attempt",
            event_summary=f"Billing attempt recorded with status {attempt.attempt_status}.",
            client_visible=True,
        )
    )
    usage = session.query(app_models.ClientUsageCounter).filter_by(workspace_id=workspace_id).first()
    if usage is not None:
        usage.billing_attempts_count += 1
    session.flush()
    return {"attempt": client_command_sanitizer.billing_attempt_public(attempt)}


def billing_attempts(session: Session) -> dict[str, object]:
    attempts = session.query(app_models.ClientBillingAttempt).order_by(
        desc(app_models.ClientBillingAttempt.created_at)
    ).all()
    return {"attempts": [client_command_sanitizer.billing_attempt_public(item) for item in attempts]}


def billing_external_references(session: Session) -> dict[str, object]:
    refs = session.query(app_models.ClientBillingExternalReference).order_by(
        desc(app_models.ClientBillingExternalReference.created_at)
    ).all()
    return {"external_references": [client_command_sanitizer.billing_external_reference_public(item) for item in refs]}


def billing_ledger(session: Session) -> dict[str, object]:
    entries = session.query(app_models.ClientBillingLedgerEntry).order_by(
        desc(app_models.ClientBillingLedgerEntry.created_at)
    ).all()
    return {"ledger": [client_command_sanitizer.billing_ledger_public(item) for item in entries]}


def billing_overview(session: Session) -> dict[str, object]:
    return {
        "metrics": {
            "provider_profiles": session.query(app_models.ClientBillingProviderProfile).count(),
            "customer_profiles": session.query(app_models.ClientBillingCustomerProfile).count(),
            "readiness_checks": session.query(app_models.ClientBillingReadinessCheck).count(),
            "dry_runs": session.query(app_models.ClientCheckoutDryRunReceipt).count(),
            "approvals": session.query(app_models.ClientBillingApproval).count(),
            "attempts": session.query(app_models.ClientBillingAttempt).count(),
            "blocked_attempts": session.query(app_models.ClientBillingAttempt).filter_by(attempt_status="blocked").count(),
        },
        "safety": client_command_safety_rules(),
    }


def _ensure_default_pilot_program(session: Session) -> Any:
    program = session.query(app_models.ClientPilotProgram).filter_by(program_code="prime2_pilot").first()
    if program is None:
        program = app_models.ClientPilotProgram(
            id="client-pilot-program-001",
            program_name="Prime2 Pilot",
            program_code="prime2_pilot",
            program_status="active",
            client_safe_summary="Pilot mode does not bypass source gates.",
        )
        session.add(program)
        session.flush()
    return program


def create_pilot_program(session: Session, values: dict[str, object]) -> dict[str, object]:
    program = app_models.ClientPilotProgram(
        id=_generate_id("client-pilot-program"),
        program_name=str(values.get("program_name") or "Prime2 Pilot"),
        program_code=str(values.get("program_code") or f"pilot_{uuid4().hex[:6]}"),
        program_status=str(values.get("program_status") or "active"),
        client_safe_summary=str(values.get("client_safe_summary") or "Pilot mode does not bypass source gates."),
    )
    session.add(program)
    session.flush()
    return {"program": client_command_sanitizer.pilot_program_public(program)}


def pilot_programs(session: Session) -> dict[str, object]:
    _ensure_default_pilot_program(session)
    programs = session.query(app_models.ClientPilotProgram).order_by(app_models.ClientPilotProgram.program_name).all()
    return {"programs": [client_command_sanitizer.pilot_program_public(item) for item in programs]}


def create_pilot_enrollment(session: Session, workspace_id: str, values: dict[str, object]) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    program = session.get(app_models.ClientPilotProgram, str(values.get("program_id") or _ensure_default_pilot_program(session).id))
    enrollment = (
        session.query(app_models.ClientPilotWorkspaceEnrollment)
        .filter_by(workspace_id=workspace_id)
        .order_by(desc(app_models.ClientPilotWorkspaceEnrollment.created_at))
        .first()
    )
    if enrollment is None:
        enrollment = app_models.ClientPilotWorkspaceEnrollment(
            id=_generate_id("client-pilot-enrollment"),
            workspace_id=workspace_id,
        )
        session.add(enrollment)
    enrollment.program_id = program.id
    enrollment.pilot_mode = str(values.get("pilot_mode") or "beta_pilot")
    enrollment.enrollment_status = str(values.get("enrollment_status") or "active")
    enrollment.support_owner_name = str(values.get("support_owner_name") or "Client Success Manager")
    enrollment.client_safe_summary = str(values.get("client_safe_summary") or "Pilot workspace enrolled without bypassing source gates.")
    session.flush()
    return {"enrollment": client_command_sanitizer.pilot_enrollment_public(enrollment)}


def pilot_enrollment_detail(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    enrollment = (
        session.query(app_models.ClientPilotWorkspaceEnrollment)
        .filter_by(workspace_id=workspace_id)
        .order_by(desc(app_models.ClientPilotWorkspaceEnrollment.created_at))
        .first()
    )
    if enrollment is None:
        return create_pilot_enrollment(session, workspace_id, {})
    return {"enrollment": client_command_sanitizer.pilot_enrollment_public(enrollment)}


def create_pilot_operating_mode(session: Session, workspace_id: str, values: dict[str, object]) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    mode = (
        session.query(app_models.ClientPilotOperatingMode)
        .filter_by(workspace_id=workspace_id)
        .order_by(desc(app_models.ClientPilotOperatingMode.created_at))
        .first()
    )
    if mode is None:
        mode = app_models.ClientPilotOperatingMode(
            id=_generate_id("client-pilot-mode"),
            workspace_id=workspace_id,
        )
        session.add(mode)
    mode.pilot_mode = str(values.get("pilot_mode") or "beta_pilot")
    mode.operating_posture = str(values.get("operating_posture") or "manual_only")
    mode.reason_summary = str(values.get("reason_summary") or "Controlled live posture requires CP9, CP10, and CP11 gates.")
    mode.requires_human_review = bool(values.get("requires_human_review", False))
    mode.no_gate_bypass = True
    session.flush()
    return {"operating_mode": client_command_sanitizer.pilot_operating_mode_public(mode)}


def pilot_operating_mode_detail(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    mode = (
        session.query(app_models.ClientPilotOperatingMode)
        .filter_by(workspace_id=workspace_id)
        .order_by(desc(app_models.ClientPilotOperatingMode.created_at))
        .first()
    )
    if mode is None:
        return create_pilot_operating_mode(session, workspace_id, {})
    return {"operating_mode": client_command_sanitizer.pilot_operating_mode_public(mode)}


def create_pilot_health_snapshot(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    readiness = (
        session.query(ClientWorkspaceReadinessScore)
        .filter_by(workspace_id=workspace_id)
        .order_by(desc(ClientWorkspaceReadinessScore.created_at))
        .first()
    )
    assignment = _latest_plan_assignment(session, workspace_id)
    communication_blocks = session.query(app_models.ClientCommunicationSendAttempt).filter_by(
        workspace_id=workspace_id, attempt_status="blocked"
    ).count()
    billing_blocks = session.query(app_models.ClientBillingAttempt).filter_by(
        workspace_id=workspace_id, attempt_status="blocked"
    ).count()
    compliance_blocks = session.query(ClientSafeContactStatus).filter(
        ClientSafeContactStatus.workspace_id == workspace_id,
        ClientSafeContactStatus.status.in_(["blocked", "opted_out", "missing_consent"]),
    ).count()
    weekly_report = (
        session.query(ClientWeeklyCommandReport)
        .filter_by(workspace_id=workspace_id)
        .order_by(desc(ClientWeeklyCommandReport.created_at))
        .first()
    )
    blockers = (
        session.query(ClientActivationBlocker)
        .filter_by(workspace_id=workspace_id)
        .order_by(desc(ClientActivationBlocker.severity))
        .all()
    )
    block_reasons = [item.blocker_summary for item in blockers if item.severity in {"critical", "high"}]
    if communication_blocks:
        block_reasons.append("communication_gate_blocked")
    if billing_blocks:
        block_reasons.append("billing_gate_blocked")
    if compliance_blocks:
        block_reasons.append("compliance_review_needed")
    health_status = "healthy"
    if any(item.severity == "critical" for item in blockers):
        health_status = "critical"
    elif block_reasons:
        health_status = "blocked"
    elif readiness and readiness.readiness_status not in {"ready_for_manual_operation", "ready_for_first_weekly_cycle"}:
        health_status = "watch"
    snapshot = (
        session.query(app_models.ClientPilotHealthSnapshot)
        .filter_by(workspace_id=workspace_id)
        .order_by(desc(app_models.ClientPilotHealthSnapshot.created_at))
        .first()
    )
    if snapshot is None:
        snapshot = app_models.ClientPilotHealthSnapshot(
            id=_generate_id("client-pilot-health"),
            workspace_id=workspace_id,
        )
        session.add(snapshot)
    snapshot.health_status = health_status
    snapshot.onboarding_status = readiness.readiness_status if readiness else "not_started"
    snapshot.plan_status = assignment.plan_code if assignment else "unassigned"
    snapshot.communication_status = "blocked" if communication_blocks else "ready_for_review"
    snapshot.billing_status = "blocked" if billing_blocks else "ready_for_review"
    snapshot.compliance_status = "blocked" if compliance_blocks else "acceptable"
    snapshot.weekly_report_status = weekly_report.report_status if weekly_report else "missing"
    snapshot.block_reasons = block_reasons
    snapshot.next_actions = [
        "Review onboarding blockers.",
        "Check plan gates before any live action.",
        "Keep pilot operations inside source-domain safety gates.",
    ]
    snapshot.client_safe_summary = "Pilot mode does not bypass source gates."
    session.flush()
    return {"health_snapshot": client_command_sanitizer.pilot_health_snapshot_public(snapshot)}


def pilot_health_snapshot_detail(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    snapshot = (
        session.query(app_models.ClientPilotHealthSnapshot)
        .filter_by(workspace_id=workspace_id)
        .order_by(desc(app_models.ClientPilotHealthSnapshot.created_at))
        .first()
    )
    if snapshot is None:
        return create_pilot_health_snapshot(session, workspace_id)
    return {"health_snapshot": client_command_sanitizer.pilot_health_snapshot_public(snapshot)}


def create_pilot_support_ticket(session: Session, workspace_id: str, values: dict[str, object]) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    ticket = app_models.ClientPilotSupportTicket(
        id=_generate_id("client-pilot-ticket"),
        workspace_id=workspace_id,
        ticket_type=str(values.get("ticket_type") or "bug"),
        title=str(values.get("title") or "Pilot support item"),
        summary=str(values.get("summary") or ""),
        status=str(values.get("status") or "open"),
        priority=str(values.get("priority") or "medium"),
        assigned_to=str(values.get("assigned_to") or "Client Success Manager"),
        client_safe=True,
    )
    session.add(ticket)
    session.flush()
    return {"ticket": client_command_sanitizer.pilot_support_ticket_public(ticket)}


def pilot_support_tickets(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    tickets = session.query(app_models.ClientPilotSupportTicket).filter_by(workspace_id=workspace_id).order_by(
        desc(app_models.ClientPilotSupportTicket.created_at)
    ).all()
    return {"tickets": [client_command_sanitizer.pilot_support_ticket_public(item) for item in tickets]}


def create_pilot_support_action(session: Session, values: dict[str, object]) -> dict[str, object]:
    workspace_id = str(values.get("workspace_id") or "")
    _workspace_or_404(session, workspace_id)
    action = app_models.ClientPilotSupportAction(
        id=_generate_id("client-pilot-action"),
        workspace_id=workspace_id,
        ticket_id=str(values.get("ticket_id")) if values.get("ticket_id") else None,
        action_summary=str(values.get("action_summary") or ""),
        action_status=str(values.get("action_status") or "queued"),
        owner_role=str(values.get("owner_role") or "client_success_manager"),
        client_visible=bool(values.get("client_visible", True)),
    )
    session.add(action)
    session.flush()
    return {"support_action": client_command_sanitizer.pilot_support_action_public(action)}


def pilot_support_actions(session: Session) -> dict[str, object]:
    actions = session.query(app_models.ClientPilotSupportAction).order_by(
        desc(app_models.ClientPilotSupportAction.created_at)
    ).all()
    return {"support_actions": [client_command_sanitizer.pilot_support_action_public(item) for item in actions]}


def create_pilot_escalation(session: Session, values: dict[str, object]) -> dict[str, object]:
    workspace_id = str(values.get("workspace_id") or "")
    _workspace_or_404(session, workspace_id)
    escalation = app_models.ClientPilotEscalation(
        id=_generate_id("client-pilot-escalation"),
        workspace_id=workspace_id,
        escalation_type=str(values.get("escalation_type") or "review"),
        source_domain=str(values.get("source_domain") or "client_command"),
        source_record_id=str(values.get("source_record_id")) if values.get("source_record_id") else None,
        escalation_status=str(values.get("escalation_status") or "open"),
        escalation_reason=str(values.get("escalation_reason") or ""),
        requires_human_review=bool(values.get("requires_human_review", True)),
    )
    session.add(escalation)
    session.flush()
    return {"escalation": client_command_sanitizer.pilot_escalation_public(escalation)}


def pilot_escalations(session: Session) -> dict[str, object]:
    escalations = session.query(app_models.ClientPilotEscalation).order_by(
        desc(app_models.ClientPilotEscalation.created_at)
    ).all()
    return {"escalations": [client_command_sanitizer.pilot_escalation_public(item) for item in escalations]}


def create_pilot_launch_checklist(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    readiness = (
        session.query(ClientWorkspaceReadinessScore)
        .filter_by(workspace_id=workspace_id)
        .order_by(desc(ClientWorkspaceReadinessScore.created_at))
        .first()
    )
    assignment = _latest_plan_assignment(session, workspace_id)
    weekly_report = session.query(ClientWeeklyCommandReport).filter_by(workspace_id=workspace_id).first()
    compliance_ok = _compliance_posture_ok(session, workspace_id)
    support_owner_assigned = session.query(app_models.ClientPilotWorkspaceEnrollment).filter(
        app_models.ClientPilotWorkspaceEnrollment.workspace_id == workspace_id,
        app_models.ClientPilotWorkspaceEnrollment.support_owner_name != "",
    ).count() > 0
    critical_blockers = session.query(ClientActivationBlocker).filter_by(
        workspace_id=workspace_id, severity="critical"
    ).count()
    live_flags_unsafe = session.query(app_models.ClientCommunicationLiveFlag).filter(
        app_models.ClientCommunicationLiveFlag.workspace_id == workspace_id,
        app_models.ClientCommunicationLiveFlag.workspace_communication_live_enabled.is_(True),
    ).count() > 0 and _communication_gate_status(session, workspace_id)[0] != "allowed"
    checklist = (
        session.query(app_models.ClientPilotLaunchChecklist)
        .filter_by(workspace_id=workspace_id)
        .order_by(desc(app_models.ClientPilotLaunchChecklist.created_at))
        .first()
    )
    if checklist is None:
        checklist = app_models.ClientPilotLaunchChecklist(
            id=_generate_id("client-pilot-launch"),
            workspace_id=workspace_id,
        )
        session.add(checklist)
    checklist.onboarding_ready = bool(readiness and readiness.readiness_score >= 80)
    checklist.plan_assigned = assignment is not None
    checklist.compliance_acceptable = compliance_ok
    checklist.weekly_report_available = weekly_report is not None
    checklist.support_owner_assigned = support_owner_assigned
    checklist.no_critical_blockers = critical_blockers == 0
    checklist.no_unsafe_live_flags = not live_flags_unsafe
    checklist.block_reasons = [
        reason
        for reason, enabled in [
            ("onboarding_not_ready", not checklist.onboarding_ready),
            ("plan_not_assigned", not checklist.plan_assigned),
            ("compliance_not_acceptable", not checklist.compliance_acceptable),
            ("weekly_report_missing", not checklist.weekly_report_available),
            ("support_owner_missing", not checklist.support_owner_assigned),
            ("critical_blockers_present", not checklist.no_critical_blockers),
            ("unsafe_live_flags_present", not checklist.no_unsafe_live_flags),
        ]
        if enabled
    ]
    checklist.checklist_status = "ready" if not checklist.block_reasons else "blocked"
    checklist.client_safe_summary = "Pilot launch checklist does not bypass source gates."
    session.flush()
    return {"launch_checklist": client_command_sanitizer.pilot_launch_checklist_public(checklist)}


def pilot_launch_checklist_detail(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    checklist = (
        session.query(app_models.ClientPilotLaunchChecklist)
        .filter_by(workspace_id=workspace_id)
        .order_by(desc(app_models.ClientPilotLaunchChecklist.created_at))
        .first()
    )
    if checklist is None:
        return create_pilot_launch_checklist(session, workspace_id)
    return {"launch_checklist": client_command_sanitizer.pilot_launch_checklist_public(checklist)}


def create_pilot_risk_review(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    communication_blocked = session.query(app_models.ClientCommunicationSendAttempt).filter_by(
        workspace_id=workspace_id, attempt_status="blocked"
    ).count() > 0
    billing_blocked = session.query(app_models.ClientBillingAttempt).filter_by(
        workspace_id=workspace_id, attempt_status="blocked"
    ).count() > 0
    compliance_blocked = not _compliance_posture_ok(session, workspace_id)
    critical_blockers = [
        blocker.blocker_type
        for blocker in session.query(ClientActivationBlocker).filter_by(workspace_id=workspace_id).all()
        if blocker.severity in {"critical", "high"}
    ]
    review = (
        session.query(app_models.ClientPilotRiskReview)
        .filter_by(workspace_id=workspace_id)
        .order_by(desc(app_models.ClientPilotRiskReview.created_at))
        .first()
    )
    if review is None:
        review = app_models.ClientPilotRiskReview(
            id=_generate_id("client-pilot-risk"),
            workspace_id=workspace_id,
        )
        session.add(review)
    review.communication_blocked = communication_blocked
    review.billing_blocked = billing_blocked
    review.compliance_blocked = compliance_blocked
    review.critical_blockers = critical_blockers
    review.escalation_required = communication_blocked or billing_blocked or compliance_blocked or bool(critical_blockers)
    review.risk_status = "blocked" if review.escalation_required else "watch"
    review.summary = "Controlled live posture requires CP9, CP10, and CP11 gates."
    session.flush()
    if review.escalation_required:
        create_pilot_escalation(
            session,
            {
                "workspace_id": workspace_id,
                "escalation_type": "risk_review",
                "source_domain": "pilot",
                "source_record_id": review.id,
                "escalation_reason": review.summary,
                "requires_human_review": True,
            },
        )
    return {"risk_review": client_command_sanitizer.pilot_risk_review_public(review)}


def pilot_risk_review_detail(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    review = (
        session.query(app_models.ClientPilotRiskReview)
        .filter_by(workspace_id=workspace_id)
        .order_by(desc(app_models.ClientPilotRiskReview.created_at))
        .first()
    )
    if review is None:
        return create_pilot_risk_review(session, workspace_id)
    return {"risk_review": client_command_sanitizer.pilot_risk_review_public(review)}


def create_pilot_client_safe_update(session: Session, workspace_id: str, values: dict[str, object]) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    update = app_models.ClientPilotClientSafeUpdate(
        id=_generate_id("client-pilot-update"),
        workspace_id=workspace_id,
        update_title=str(values.get("update_title") or "Pilot update"),
        update_summary=str(values.get("update_summary") or ""),
        status=str(values.get("status") or "draft"),
        client_safe_summary=str(values.get("client_safe_summary") or "Client-safe updates hide internal governance, provider payloads, and admin notes."),
        hides_admin_notes=True,
    )
    session.add(update)
    session.flush()
    return {"client_safe_update": client_command_sanitizer.pilot_client_safe_update_public(update)}


def pilot_client_safe_updates(session: Session, workspace_id: str) -> dict[str, object]:
    _workspace_or_404(session, workspace_id)
    updates = session.query(app_models.ClientPilotClientSafeUpdate).filter_by(workspace_id=workspace_id).order_by(
        desc(app_models.ClientPilotClientSafeUpdate.created_at)
    ).all()
    return {"client_safe_updates": [client_command_sanitizer.pilot_client_safe_update_public(item) for item in updates]}


def pilot_admin_console(session: Session) -> dict[str, object]:
    return {
        "metrics": {
            "programs": session.query(app_models.ClientPilotProgram).count(),
            "enrollments": session.query(app_models.ClientPilotWorkspaceEnrollment).count(),
            "support_tickets": session.query(app_models.ClientPilotSupportTicket).count(),
            "escalations": session.query(app_models.ClientPilotEscalation).count(),
            "blocked_health_snapshots": session.query(app_models.ClientPilotHealthSnapshot).filter(
                app_models.ClientPilotHealthSnapshot.health_status.in_(["blocked", "critical"])
            ).count(),
        },
        "programs": [client_command_sanitizer.pilot_program_public(item) for item in session.query(app_models.ClientPilotProgram).all()],
        "enrollments": [client_command_sanitizer.pilot_enrollment_public(item) for item in session.query(app_models.ClientPilotWorkspaceEnrollment).all()],
        "health": [client_command_sanitizer.pilot_health_snapshot_public(item) for item in session.query(app_models.ClientPilotHealthSnapshot).all()],
        "safety": client_command_safety_rules(),
    }


def pilot_support_console(session: Session) -> dict[str, object]:
    return {
        "tickets": [client_command_sanitizer.pilot_support_ticket_public(item) for item in session.query(app_models.ClientPilotSupportTicket).order_by(desc(app_models.ClientPilotSupportTicket.created_at)).all()],
        "actions": [client_command_sanitizer.pilot_support_action_public(item) for item in session.query(app_models.ClientPilotSupportAction).order_by(desc(app_models.ClientPilotSupportAction.created_at)).all()],
        "escalations": [client_command_sanitizer.pilot_escalation_public(item) for item in session.query(app_models.ClientPilotEscalation).order_by(desc(app_models.ClientPilotEscalation.created_at)).all()],
    }


def pilot_blocked(session: Session) -> dict[str, object]:
    blocked = session.query(app_models.ClientPilotHealthSnapshot).filter(
        app_models.ClientPilotHealthSnapshot.health_status.in_(["blocked", "critical"])
    ).order_by(desc(app_models.ClientPilotHealthSnapshot.created_at)).all()
    return {"blocked": [client_command_sanitizer.pilot_health_snapshot_public(item) for item in blocked]}


def pilot_needs_review(session: Session) -> dict[str, object]:
    needs_review = session.query(app_models.ClientPilotHealthSnapshot).filter(
        app_models.ClientPilotHealthSnapshot.health_status.in_(["watch", "needs_review"])
    ).order_by(desc(app_models.ClientPilotHealthSnapshot.created_at)).all()
    return {"needs_review": [client_command_sanitizer.pilot_health_snapshot_public(item) for item in needs_review]}
