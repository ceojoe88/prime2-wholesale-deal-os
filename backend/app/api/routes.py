from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Body, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_session
from app.domain.autonomy import (
    autonomy_dashboard,
    autonomy_safety_guard,
    daily_briefing_summary,
    run_scheduler_workflow,
)
from app.domain.auto_execution import (
    auto_execution_dashboard,
    execute_with_auto_gate,
    validate_auto_execution_template,
)
from app.domain.buyer_portal import (
    buyer_portal_rules,
    portal_publish_gate,
    sanitize_buyer_deal,
    update_publication_gate,
)
from app.domain.buyer_acceleration import (
    buyer_acceleration_dashboard,
    buyer_distribution_gate,
    buyer_velocity_score,
    sync_buyer_sequence,
    validate_buyer_sequence_text,
)
from app.domain.buyer_demand import (
    buyer_deal_priority_summary,
    buyer_demand_dashboard,
    distribution_prep_summary,
    validate_distribution_language,
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
from app.domain.closing_coordination import (
    closing_coordination_dashboard,
    closing_readiness_gate,
    sync_deal_room,
    unified_deal_room_summary,
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
from app.domain.deal_evidence import (
    assignment_fee_summary,
    evidence_dashboard,
    evidence_packet_summary,
    sync_assignment_fee_attribution,
    sync_evidence_packet,
    validate_profit_claims,
)
from app.domain.field_testing import (
    CALL_RESULTS,
    V19_CSV_FIELDS,
    apply_call_outcome,
    commit_approved_import_rows,
    field_testing_briefing,
    field_testing_dashboard,
    outreach_eligibility_for_lead,
    preview_real_lead_csv,
    sanitize_field_testing_text,
    scoring_adjustment_from_feedback,
    sync_batch_counts,
    sync_lead_quality_review,
    sync_prediction_feedback,
)
from app.domain.imports import preview_lead_csv
from app.domain.offer_conversion import (
    contract_ready_summary,
    negotiation_summary,
    offer_conversion_dashboard,
    offer_positioning_summary,
    validate_conversion_language,
)
from app.domain.optimization import (
    agent_performance_overall,
    optimization_dashboard,
    validate_learning_record,
    validate_optimization_claim,
)
from app.domain.operator_mode import (
    approval_console_summary,
    calculate_system_trust,
    command_loop_safety,
    operator_mode_dashboard,
    operator_mode_gate,
)
from app.domain.production_readiness import (
    attachment_linkage_gate,
    audit_export_gate,
    backup_metadata,
    production_readiness_dashboard,
    provider_readiness_gate,
    sync_audit_export,
)
from app.domain.profit_control import ProfitControlInput, calculate_profit_control
from app.domain.revenue_forecast import (
    calculate_deal_probability,
    calculate_market_scaling,
    revenue_forecast_dashboard,
    sync_revenue_forecast,
    validate_forecast_language,
    validate_lead_spend_plan,
)
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
from app.domain.title_review import (
    review_packet_prep_summary,
    title_review_coordination_summary,
    title_review_dashboard,
    validate_title_review_language,
)
from app.models import (
    Agent,
    ApprovalUxReview,
    AssignmentFeeAttribution,
    AssignmentReadinessRecord,
    ApprovedTemplate,
    AuditExportPacket,
    AutoExecutionAttempt,
    AutoExecutionAuditRecord,
    AutoExecutionDryRun,
    AutoExecutionRule,
    AutomationAttempt,
    AutomationEventTrigger,
    AutomationRule,
    AutonomousAgentTask,
    AutonomyEscalation,
    BackupExportRecord,
    Buyer,
    BuyerAccelerationRecord,
    BuyerDealPriority,
    BuyerDealPublication,
    BuyerDemandProfile,
    BuyerInterest,
    BuyerMatch,
    BuyerResponseRoute,
    BuyerSequencePrep,
    BuyerVelocityProfile,
    ClosingCoordinationChecklist,
    ComplianceRecord,
    CommunicationApproval,
    CommunicationDraft,
    CommunicationDryRunReceipt,
    CommunicationSendAttempt,
    ContractControl,
    ContractReadyState,
    DailyCommandBriefing,
    Deal,
    DealDistributionPrep,
    DealEvidencePacket,
    DealProbabilityRecord,
    DealRoomBlocker,
    DeploymentHardeningCheck,
    Division,
    EnvironmentReadinessCheck,
    EvidenceAttachmentRecord,
    FieldCallOutcome,
    LeadImportBatch,
    LeadImportRow,
    LeadQualityReview,
    LeadSpendPlan,
    Lead,
    MarketScalingScore,
    NegotiationRecord,
    AgentPerformanceScore,
    AutonomousDailyOperatingReport,
    OperatorExceptionRecord,
    OperatorModeSetting,
    OfferPacket,
    OfferPositioningRecord,
    OptimizationRecommendation,
    OutcomeLearningRecord,
    OwnerApprovalItem,
    PredictionFeedbackRecord,
    ProviderSandboxReadinessCheck,
    RevenueForecastRecord,
    ReviewPacketPrep,
    SellerInteraction,
    SellerOfferPublication,
    SellerPortalResponse,
    SchedulerRun,
    ScoringAdjustmentSuggestion,
    ScoringWeightChange,
    SemiAutonomousCommandLoopRun,
    SystemTrustScore,
    TitleReviewCoordination,
    TitleHandoffPacket,
    UnifiedDealRoom,
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


class ProfitClaimValidationRequest(BaseModel):
    content: str


class DistributionSafetyRequest(BaseModel):
    content: str
    assignment_fee_exposure_approved: bool = False


class BuyerSequenceSafetyRequest(BaseModel):
    content: str


class OptimizationClaimRequest(BaseModel):
    content: str


class ForecastSafetyRequest(BaseModel):
    content: str


class ConversionSafetyRequest(BaseModel):
    content: str


class TitleReviewSafetyRequest(BaseModel):
    content: str


class AutonomySafetyRequest(BaseModel):
    action: str
    autonomy_level: int = 2
    owner_approval_recorded: bool = False


class AutonomyRunRequest(BaseModel):
    workflow_type: str
    idempotency_key: str
    owner_approval_recorded: bool = False


class AutoExecutionRequest(BaseModel):
    rule_id: str | None = None
    template_id: str | None = None
    idempotency_key: str
    source_record_type: str = ""
    source_record_id: str = ""
    recipient_count: int = 1
    v5_safety_passed: bool = False
    v5_dry_run_receipt_exists: bool = False
    v5_approval_recorded: bool = False
    live_flags_enabled: bool = False
    provider_ready: bool = False


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


class LeadImportBatchCreateRequest(BaseModel):
    batch_name: str = "Manual field-testing batch"
    source_filename: str = "manual-entry.csv"
    imported_by: str = "Owner"


class LeadImportRowStatusRequest(BaseModel):
    row_status: str
    approved_for_commit: bool | None = None
    operator_notes: str = ""


class FieldCallOutcomeRequest(BaseModel):
    lead_id: str
    call_datetime: datetime | None = None
    contact_result: str = "no_answer"
    motivation_notes: str = ""
    asking_price: int | None = None
    timeline: str = ""
    property_condition_notes: str = ""
    seller_objections: list[str] = []
    seller_temperature: float = 0
    next_follow_up_date: datetime | None = None
    operator_notes: str = ""
    prime2_next_recommendation: str = ""


class PredictionFeedbackRequest(BaseModel):
    lead_id: str | None = None
    deal_id: str | None = None
    call_outcome_id: str | None = None
    source_prediction_type: str
    source_prediction_value: str
    actual_result: str
    owner_reviewed: bool = False


class FieldTestingSafetyRequest(BaseModel):
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


@router.get("/lead-imports")
def lead_import_batches(session: Session = Depends(get_session)) -> dict[str, object]:
    batches = session.query(LeadImportBatch).all()
    for batch in batches:
        sync_batch_counts(batch)
    session.commit()
    return {
        "lead_import_batches": [model_to_dict(batch) for batch in batches],
        "csv_fields": V19_CSV_FIELDS,
        "preview_before_commit_required": True,
        "live_outreach_allowed": False,
        "bulk_outreach_allowed": False,
        "auto_portal_publish_allowed": False,
    }


@router.post("/lead-imports")
def create_lead_import_batch(
    payload: LeadImportBatchCreateRequest,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    batch = LeadImportBatch(
        id=f"lead-import-{session.query(LeadImportBatch).count() + 1:03d}",
        batch_name=payload.batch_name,
        source_filename=payload.source_filename,
        imported_by=payload.imported_by,
        status="created_waiting_preview",
        safety_notes=[
            "Import batch created only; no rows committed and no outreach triggered.",
            "CSV preview and row approval are required before commit.",
        ],
    )
    session.add(batch)
    session.commit()
    return {
        **model_to_dict(batch),
        "supported_fields": V19_CSV_FIELDS,
        "live_outreach_allowed": False,
        "bulk_outreach_allowed": False,
    }


@router.get("/lead-imports/preview")
def lead_import_preview_template() -> dict[str, object]:
    return {
        "supported_fields": V19_CSV_FIELDS,
        "critical_fields": [
            "owner_name",
            "property_address",
            "property_city",
            "property_state",
            "property_zip",
            "lead_source",
        ],
        "preview_before_commit_required": True,
        "commit_approved_rows_only": True,
        "live_outreach_allowed": False,
    }


@router.post("/lead-imports/preview")
def lead_import_real_preview(
    csv_text: str = Body(..., media_type="text/csv"),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    batch = preview_real_lead_csv(session, csv_text)
    return {
        **model_to_dict(batch),
        "rows": [model_to_dict(row) for row in batch.rows],
        "quality_reviews": [model_to_dict(review) for review in batch.quality_reviews],
        "live_outreach_allowed": False,
        "bulk_outreach_allowed": False,
    }


@router.patch("/lead-imports/rows/{row_id}")
def update_import_row_status(
    row_id: str,
    payload: LeadImportRowStatusRequest,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    row = session.get(LeadImportRow, row_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Lead import row not found")
    if row.row_status == "committed":
        raise HTTPException(
            status_code=400,
            detail={"allowed": False, "reason": "Committed rows cannot be changed."},
        )
    if payload.row_status not in {"approved", "blocked", "needs_review"}:
        raise HTTPException(status_code=400, detail="Invalid row status")
    row.row_status = payload.row_status
    row.approved_for_commit = (
        payload.approved_for_commit
        if payload.approved_for_commit is not None
        else payload.row_status == "approved"
    )
    if payload.operator_notes:
        row.notes = f"{row.notes}\nOperator status note: {payload.operator_notes}".strip()
    if payload.row_status == "blocked" and "operator_blocked" not in row.blocked_reasons:
        row.blocked_reasons = [*row.blocked_reasons, "operator_blocked"]
    review = session.get(LeadQualityReview, f"qa-{row.id}")
    if review:
        review.blocked_reasons = row.blocked_reasons
        sync_lead_quality_review(review)
    sync_batch_counts(row.batch)
    session.commit()
    return {
        **model_to_dict(row),
        "batch": model_to_dict(row.batch),
        "live_outreach_allowed": False,
    }


@router.post("/lead-imports/{batch_id}/commit")
def commit_lead_import_batch(
    batch_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    batch = session.get(LeadImportBatch, batch_id)
    if batch is None:
        raise HTTPException(status_code=404, detail="Lead import batch not found")
    return commit_approved_import_rows(session, batch)


@router.get("/lead-imports/{batch_id}")
def lead_import_batch_detail(
    batch_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    batch = session.get(LeadImportBatch, batch_id)
    if batch is None:
        raise HTTPException(status_code=404, detail="Lead import batch not found")
    sync_batch_counts(batch)
    session.commit()
    return {
        **model_to_dict(batch),
        "rows": [model_to_dict(row) for row in batch.rows],
        "quality_reviews": [model_to_dict(review) for review in batch.quality_reviews],
        "blocked_rows": [model_to_dict(row) for row in batch.rows if row.blocked_reasons],
        "commit_approved_rows_only": True,
        "live_outreach_allowed": False,
        "bulk_outreach_allowed": False,
    }


@router.get("/lead-qa")
def lead_quality_assurance(session: Session = Depends(get_session)) -> dict[str, object]:
    reviews = session.query(LeadQualityReview).all()
    for review in reviews:
        sync_lead_quality_review(review)
    session.commit()
    return {
        "lead_quality_reviews": [model_to_dict(review) for review in reviews],
        "call_priority": [
            model_to_dict(review)
            for review in reviews
            if review.recommended_next_action == "call_priority"
        ],
        "research_more": [
            model_to_dict(review)
            for review in reviews
            if review.recommended_next_action == "research_more"
        ],
        "duplicate_review": [
            model_to_dict(review)
            for review in reviews
            if review.recommended_next_action == "duplicate_review"
        ],
        "live_outreach_allowed": False,
    }


@router.get("/lead-qa/{lead_id}")
def lead_quality_detail(lead_id: str, session: Session = Depends(get_session)) -> dict[str, object]:
    reviews = (
        session.query(LeadQualityReview)
        .filter(LeadQualityReview.lead_id == lead_id)
        .all()
    )
    if not reviews:
        import_row = session.get(LeadImportRow, lead_id)
        if import_row is not None:
            reviews = import_row.quality_reviews
    if not reviews:
        raise HTTPException(status_code=404, detail="Lead QA record not found")
    for review in reviews:
        sync_lead_quality_review(review)
    session.commit()
    return {
        "lead_id": lead_id,
        "quality_reviews": [model_to_dict(review) for review in reviews],
        "blocked_reasons": sorted(
            {reason for review in reviews for reason in review.blocked_reasons}
        ),
        "recommended_next_action": reviews[0].recommended_next_action,
        "live_outreach_allowed": False,
    }


@router.get("/call-outcomes")
def call_outcomes(session: Session = Depends(get_session)) -> dict[str, object]:
    outcomes = session.query(FieldCallOutcome).all()
    return {
        "call_outcomes": [model_to_dict(outcome) for outcome in outcomes],
        "allowed_contact_results": sorted(CALL_RESULTS),
        "do_not_contact_records": [
            model_to_dict(outcome) for outcome in outcomes if outcome.do_not_contact
        ],
        "live_calling_inside_system": False,
    }


@router.post("/call-outcomes")
def create_call_outcome(
    payload: FieldCallOutcomeRequest,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    lead = session.get(Lead, payload.lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    if payload.contact_result not in CALL_RESULTS:
        raise HTTPException(status_code=400, detail="Invalid contact result")
    safety = sanitize_field_testing_text(
        " ".join(
            [
                payload.motivation_notes,
                payload.timeline,
                payload.property_condition_notes,
                " ".join(payload.seller_objections),
                payload.operator_notes,
                payload.prime2_next_recommendation,
            ]
        )
    )
    if not safety["allowed"]:
        raise HTTPException(status_code=400, detail=safety)
    outcome = FieldCallOutcome(
        id=f"call-outcome-{session.query(FieldCallOutcome).count() + 1:03d}",
        lead_id=payload.lead_id,
        call_datetime=payload.call_datetime or datetime.now(),
        contact_result=payload.contact_result,
        motivation_notes=payload.motivation_notes,
        asking_price=payload.asking_price,
        timeline=payload.timeline,
        property_condition_notes=payload.property_condition_notes,
        seller_objections=payload.seller_objections,
        seller_temperature=payload.seller_temperature,
        next_follow_up_date=payload.next_follow_up_date,
        operator_notes=payload.operator_notes,
        prime2_next_recommendation=payload.prime2_next_recommendation
        or "Prime 2 recommends owner review before any field follow-up.",
    )
    session.add(outcome)
    session.flush()
    apply_call_outcome(session, outcome)
    session.commit()
    return {
        **model_to_dict(outcome),
        "lead": model_to_dict(lead),
        "outreach_eligibility": outreach_eligibility_for_lead(session, lead.id),
        "live_calling_inside_system": False,
    }


@router.get("/call-outcomes/{outcome_id}")
def call_outcome_detail(
    outcome_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    outcome = session.get(FieldCallOutcome, outcome_id)
    if outcome is None:
        raise HTTPException(status_code=404, detail="Call outcome not found")
    return {
        **model_to_dict(outcome),
        "lead": model_to_dict(outcome.lead),
        "outreach_eligibility": outreach_eligibility_for_lead(session, outcome.lead_id),
        "live_calling_inside_system": False,
    }


@router.get("/field-testing")
def field_testing(session: Session = Depends(get_session)) -> dict[str, object]:
    return field_testing_dashboard(session)


@router.post("/field-testing/safety/validate")
def field_testing_safety(payload: FieldTestingSafetyRequest) -> dict[str, object]:
    return sanitize_field_testing_text(payload.content)


@router.get("/field-briefing")
def field_briefing(session: Session = Depends(get_session)) -> dict[str, object]:
    return field_testing_briefing(session)


@router.get("/feedback-loop")
def feedback_loop(session: Session = Depends(get_session)) -> dict[str, object]:
    records = session.query(PredictionFeedbackRecord).all()
    for record in records:
        sync_prediction_feedback(record)
    session.commit()
    return {
        "feedback_records": [model_to_dict(record) for record in records],
        "prediction_misses": [
            model_to_dict(record) for record in records if record.accuracy_score < 70
        ],
        "deterministic_explainable_scoring": True,
    }


@router.post("/feedback-loop")
def create_feedback_record(
    payload: PredictionFeedbackRequest,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    if payload.lead_id and session.get(Lead, payload.lead_id) is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    if payload.call_outcome_id and session.get(FieldCallOutcome, payload.call_outcome_id) is None:
        raise HTTPException(status_code=404, detail="Call outcome not found")
    safety = sanitize_field_testing_text(
        f"{payload.source_prediction_value} {payload.actual_result}"
    )
    if not safety["allowed"]:
        raise HTTPException(status_code=400, detail=safety)
    feedback = PredictionFeedbackRecord(
        id=f"feedback-{session.query(PredictionFeedbackRecord).count() + 1:03d}",
        lead_id=payload.lead_id,
        deal_id=payload.deal_id,
        call_outcome_id=payload.call_outcome_id,
        source_prediction_type=payload.source_prediction_type,
        source_prediction_value=payload.source_prediction_value,
        actual_result=payload.actual_result,
        owner_reviewed=payload.owner_reviewed,
        source_record_ids=[
            record_id
            for record_id in [payload.lead_id, payload.deal_id, payload.call_outcome_id]
            if record_id
        ],
    )
    sync_prediction_feedback(feedback)
    session.add(feedback)
    session.flush()
    suggestion = scoring_adjustment_from_feedback(feedback)
    session.add(suggestion)
    session.commit()
    return {
        **model_to_dict(feedback),
        "scoring_adjustment": model_to_dict(suggestion),
        "deterministic_explainable_scoring": True,
    }


@router.get("/feedback-loop/{feedback_id}")
def feedback_detail(
    feedback_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    feedback = session.get(PredictionFeedbackRecord, feedback_id)
    if feedback is None:
        raise HTTPException(status_code=404, detail="Feedback record not found")
    sync_prediction_feedback(feedback)
    session.commit()
    return {
        **model_to_dict(feedback),
        "scoring_adjustments": [
            model_to_dict(adjustment) for adjustment in feedback.scoring_adjustments
        ],
        "deterministic_explainable_scoring": True,
    }


@router.get("/scoring-adjustments")
def scoring_adjustments(session: Session = Depends(get_session)) -> dict[str, object]:
    suggestions = session.query(ScoringAdjustmentSuggestion).all()
    return {
        "scoring_adjustments": [model_to_dict(suggestion) for suggestion in suggestions],
        "pending_owner_review": [
            model_to_dict(suggestion)
            for suggestion in suggestions
            if suggestion.owner_review_status == "pending_review"
        ],
        "black_box_ml_used": False,
        "deterministic_explainable_scoring": True,
    }


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


@router.get("/deal-room")
def unified_deal_rooms(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = closing_coordination_dashboard(session)
    session.commit()
    return {
        "active_deal_rooms": dashboard["active_deal_rooms"],
        "closing_ready_deals": dashboard["closing_ready_deals"],
        "blocked_deals": dashboard["blocked_deals"],
        "assignment_ready_deals": dashboard["assignment_ready_deals"],
        "next_best_actions": dashboard["next_best_actions"],
        "projected_assignment_fees_at_risk": dashboard["projected_assignment_fees_at_risk"],
        "recommendation_only": True,
        "legal_execution_allowed": False,
        "title_submission_allowed": False,
        "payment_handling_allowed": False,
        "automatic_negotiation_allowed": False,
    }


@router.get("/deal-room/{deal_room_id}")
def unified_deal_room_detail(
    deal_room_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    room = session.get(UnifiedDealRoom, deal_room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Deal room not found")
    sync_deal_room(session, room)
    session.commit()
    return unified_deal_room_summary(room)


@router.get("/closing-coordination")
def closing_coordination(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = closing_coordination_dashboard(session)
    session.commit()
    return dashboard


@router.get("/closing-coordination/blockers")
def closing_coordination_blockers(session: Session = Depends(get_session)) -> list[dict]:
    rooms = session.query(UnifiedDealRoom).all()
    for room in rooms:
        sync_deal_room(session, room)
    session.commit()
    return [
        model_to_dict(blocker)
        for blocker in session.query(DealRoomBlocker).all()
        if not blocker.resolved
    ]


@router.get("/closing-coordination/readiness")
def closing_coordination_readiness(session: Session = Depends(get_session)) -> list[dict[str, object]]:
    rooms = session.query(UnifiedDealRoom).all()
    response = []
    for room in rooms:
        gate = sync_deal_room(session, room)
        response.append(
            {
                "deal_room_id": room.id,
                "deal_id": room.deal_id,
                "coordination_status": room.coordination_status,
                "checklist": model_to_dict(room.closing_checklist) if room.closing_checklist else None,
                "gate": gate,
                "recommendation_only": True,
                "legal_execution_allowed": False,
                "title_submission_allowed": False,
                "payment_handling_allowed": False,
                "automatic_negotiation_allowed": False,
            }
        )
    session.commit()
    return response


@router.get("/deal-evidence")
def deal_evidence(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = evidence_dashboard(session)
    session.commit()
    return dashboard


@router.get("/deal-evidence/{packet_id}")
def deal_evidence_detail(
    packet_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    packet = session.get(DealEvidencePacket, packet_id)
    if packet is None:
        raise HTTPException(status_code=404, detail="Evidence packet not found")
    sync_evidence_packet(session, packet)
    session.commit()
    return evidence_packet_summary(packet)


@router.post("/deal-evidence/safety/validate")
def deal_evidence_safety(payload: ProfitClaimValidationRequest) -> dict[str, object]:
    return validate_profit_claims(payload.content)


@router.get("/assignment-fees")
def assignment_fees(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = evidence_dashboard(session)
    session.commit()
    return {
        "assignment_fee_attributions": dashboard["assignment_fee_attributions"],
        "projected_assignment_fees": dashboard["projected_assignment_fees"],
        "verified_assignment_fees": dashboard["verified_assignment_fees"],
        "fees_at_risk": dashboard["fees_at_risk"],
        "verified_10k_opportunities": dashboard["verified_10k_opportunities"],
        "client_facing_proof_allowed": False,
        "legal_closing_guarantee_allowed": False,
    }


@router.get("/assignment-fees/{fee_id}")
def assignment_fee_detail(
    fee_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    attribution = session.get(AssignmentFeeAttribution, fee_id)
    if attribution is None:
        raise HTTPException(status_code=404, detail="Assignment fee attribution not found")
    sync_assignment_fee_attribution(session, attribution)
    session.commit()
    return assignment_fee_summary(attribution)


@router.get("/buyer-demand")
def buyer_demand(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = buyer_demand_dashboard(session)
    session.commit()
    return dashboard


@router.get("/buyer-demand/{buyer_id}")
def buyer_demand_detail(
    buyer_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    buyer = session.get(Buyer, buyer_id)
    if buyer is None:
        raise HTTPException(status_code=404, detail="Buyer not found")
    dashboard = buyer_demand_dashboard(session)
    session.commit()
    profile = session.query(BuyerDemandProfile).filter(BuyerDemandProfile.buyer_id == buyer_id).first()
    return {
        "buyer": model_to_dict(buyer),
        "demand_profile": model_to_dict(profile) if profile else None,
        "deal_priorities": [
            buyer_deal_priority_summary(priority)
            for priority in session.query(BuyerDealPriority)
            .filter(BuyerDealPriority.buyer_id == buyer_id)
            .order_by(BuyerDealPriority.priority_score.desc())
            .all()
        ],
        "distribution_preps": [
            distribution_prep_summary(prep)
            for prep in session.query(DealDistributionPrep)
            .filter(DealDistributionPrep.buyer_id == buyer_id)
            .all()
        ],
        "highest_demand_zip_codes": dashboard["highest_demand_zip_codes"],
        "draft_only": True,
        "live_buyer_blast_allowed": False,
        "bulk_send_allowed": False,
    }


@router.get("/buyer-priority")
def buyer_priority(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = buyer_demand_dashboard(session)
    session.commit()
    return {
        "buyer_priority_rankings": dashboard["buyer_priority_rankings"],
        "best_buyers_for_hot_deals": dashboard["best_buyers_for_hot_deals"],
        "buyer_ready_deals": dashboard["buyer_ready_deals"],
        "proof_of_funds_gaps": dashboard["proof_of_funds_gaps"],
        "live_contact_allowed": False,
        "buyer_blast_allowed": False,
        "bulk_send_allowed": False,
    }


@router.get("/deal-distribution")
def deal_distribution(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = buyer_demand_dashboard(session)
    session.commit()
    return {
        "distribution_preps": dashboard["distribution_preps"],
        "distribution_drafts_pending_approval": dashboard["distribution_drafts_pending_approval"],
        "buyer_ready_deals": dashboard["buyer_ready_deals"],
        "ten_k_deals_with_strong_buyer_demand": dashboard[
            "ten_k_deals_with_strong_buyer_demand"
        ],
        "live_send_allowed": False,
        "bulk_blast_allowed": False,
        "buyer_blast_allowed": False,
    }


@router.post("/deal-distribution/safety/validate")
def deal_distribution_safety(payload: DistributionSafetyRequest) -> dict[str, object]:
    return validate_distribution_language(
        payload.content,
        assignment_fee_exposure_approved=payload.assignment_fee_exposure_approved,
    )


@router.get("/deal-distribution/{distribution_id}")
def deal_distribution_detail(
    distribution_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    prep = session.get(DealDistributionPrep, distribution_id)
    if prep is None:
        raise HTTPException(status_code=404, detail="Distribution prep not found")
    summary = distribution_prep_summary(prep)
    session.commit()
    return summary


@router.get("/buyer-acceleration")
def buyer_acceleration(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = buyer_acceleration_dashboard(session)
    session.commit()
    return dashboard


@router.get("/buyer-acceleration/{deal_id}")
def buyer_acceleration_detail(
    deal_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    record = (
        session.query(BuyerAccelerationRecord)
        .filter(BuyerAccelerationRecord.deal_id == deal_id)
        .first()
    )
    if record is None:
        raise HTTPException(status_code=404, detail="Buyer acceleration record not found")
    gate = buyer_distribution_gate(record)
    sequences = (
        session.query(BuyerSequencePrep)
        .filter(BuyerSequencePrep.deal_id == deal_id)
        .all()
    )
    routes = (
        session.query(BuyerResponseRoute)
        .filter(BuyerResponseRoute.deal_id == deal_id)
        .all()
    )
    for sequence in sequences:
        sync_buyer_sequence(sequence)
    session.commit()
    return {
        **model_to_dict(record),
        "gate": gate,
        "buyer_sequences": [model_to_dict(sequence) for sequence in sequences],
        "response_routes": [model_to_dict(route) for route in routes],
        "live_send_requires_v5_v13_gates": True,
        "bulk_blast_allowed": False,
        "seller_private_data_exposed": False,
        "internal_profit_logic_exposed": False,
    }


@router.get("/buyer-sequences")
def buyer_sequences(session: Session = Depends(get_session)) -> dict[str, object]:
    sequences = session.query(BuyerSequencePrep).all()
    for sequence in sequences:
        sync_buyer_sequence(sequence)
    session.commit()
    return {
        "buyer_sequence_preps": [model_to_dict(sequence) for sequence in sequences],
        "draft_only": True,
        "live_send_allowed": False,
        "bulk_blast_allowed": False,
        "deceptive_scarcity_allowed": False,
        "seller_private_data_exposed": False,
        "internal_profit_logic_exposed": False,
    }


@router.post("/buyer-sequences/safety/validate")
def buyer_sequence_safety(payload: BuyerSequenceSafetyRequest) -> dict[str, object]:
    return validate_buyer_sequence_text(payload.content)


@router.get("/buyer-response-router")
def buyer_response_router(session: Session = Depends(get_session)) -> dict[str, object]:
    routes = session.query(BuyerResponseRoute).all()
    return {
        "buyer_response_routes": [model_to_dict(route) for route in routes],
        "buyer_interested": [
            model_to_dict(route)
            for route in routes
            if route.response_type == "buyer_interested"
        ],
        "needs_pof": [model_to_dict(route) for route in routes if route.pof_gap],
        "wants_showing_access": [
            model_to_dict(route) for route in routes if route.access_requested
        ],
        "submits_offer_intent": [
            model_to_dict(route)
            for route in routes
            if route.offer_intent_recorded
        ],
        "owner_action_required": [
            model_to_dict(route) for route in routes if route.owner_action_required
        ],
        "draft_only": True,
        "contract_execution_allowed": False,
    }


@router.get("/buyer-velocity")
def buyer_velocity(session: Session = Depends(get_session)) -> dict[str, object]:
    profiles = session.query(BuyerVelocityProfile).all()
    for profile in profiles:
        buyer_velocity_score(profile)
    session.commit()
    return {
        "buyer_velocity_profiles": [
            model_to_dict(profile)
            for profile in sorted(profiles, key=lambda item: item.velocity_score, reverse=True)
        ],
        "fast_close_buyers": [
            model_to_dict(profile)
            for profile in profiles
            if profile.recommended_use == "fast_close_priority"
        ],
        "draft_only": True,
        "live_contact_allowed": False,
        "buyer_blast_allowed": False,
    }


@router.get("/optimization")
def optimization(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = optimization_dashboard(session)
    session.commit()
    return dashboard


@router.get("/optimization/patterns")
def optimization_patterns(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = optimization_dashboard(session)
    session.commit()
    return dashboard["patterns"]


@router.get("/optimization/recommendations")
def optimization_recommendations(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = optimization_dashboard(session)
    session.commit()
    return {
        "optimization_recommendations": dashboard["optimization_recommendations"],
        "explainable_recommendations_only": True,
        "guaranteed_revenue_allowed": False,
        "unsupported_roi_allowed": False,
    }


@router.get("/optimization/agent-performance")
def optimization_agent_performance(session: Session = Depends(get_session)) -> dict[str, object]:
    scores = session.query(AgentPerformanceScore).all()
    for score in scores:
        agent_performance_overall(score)
    session.commit()
    return {
        "agent_performance_scores": [model_to_dict(score) for score in scores],
        "deterministic_scoring": True,
    }


@router.get("/optimization/lost-deals")
def optimization_lost_deals(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = optimization_dashboard(session)
    session.commit()
    return {
        "lost_deals": dashboard["lost_deals"],
        "deals_dying_before_contract_ready": dashboard["patterns"][
            "deals_dying_before_contract_ready"
        ],
    }


@router.get("/optimization/source-quality")
def optimization_source_quality(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = optimization_dashboard(session)
    session.commit()
    return {
        "source_quality": dashboard["source_quality"],
        "scoring_weight_changes": dashboard["scoring_weight_changes"],
        "changes_logged": len(dashboard["scoring_weight_changes"]),
    }


@router.post("/optimization/safety/validate")
def optimization_safety(payload: OptimizationClaimRequest) -> dict[str, object]:
    return validate_optimization_claim(payload.content)


@router.get("/optimization/records/{record_id}/gate")
def optimization_record_gate(
    record_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    record = session.get(OutcomeLearningRecord, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Learning record not found")
    gate = validate_learning_record(record)
    session.commit()
    return {**model_to_dict(record), "gate": gate}


@router.get("/revenue-forecast")
def revenue_forecast(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = revenue_forecast_dashboard(session)
    session.commit()
    return dashboard


@router.post("/revenue-forecast/safety/validate")
def revenue_forecast_safety(payload: ForecastSafetyRequest) -> dict[str, object]:
    return validate_forecast_language(payload.content)


@router.get("/revenue-forecast/{forecast_id}")
def revenue_forecast_detail(
    forecast_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    forecast = session.get(RevenueForecastRecord, forecast_id)
    if forecast is None:
        raise HTTPException(status_code=404, detail="Revenue forecast not found")
    sync_revenue_forecast(forecast)
    probabilities = session.query(DealProbabilityRecord).all()
    for probability in probabilities:
        calculate_deal_probability(probability)
    session.commit()
    return {
        **model_to_dict(forecast),
        "deal_probabilities": [model_to_dict(probability) for probability in probabilities],
        "forecasts_are_estimates": True,
        "guaranteed_revenue_allowed": False,
    }


@router.get("/market-scaling")
def market_scaling(session: Session = Depends(get_session)) -> dict[str, object]:
    markets = session.query(MarketScalingScore).all()
    for market in markets:
        calculate_market_scaling(market)
    session.commit()
    return {
        "market_scaling_scores": [model_to_dict(market) for market in markets],
        "market_ranking": sorted(
            [model_to_dict(market) for market in markets],
            key=lambda item: item["scaling_score"],
            reverse=True,
        ),
        "forecasts_are_estimates": True,
    }


@router.get("/lead-spend-planner")
def lead_spend_planner(session: Session = Depends(get_session)) -> dict[str, object]:
    plans = session.query(LeadSpendPlan).all()
    return {
        "lead_spend_plans": [
            {**model_to_dict(plan), "gate": validate_lead_spend_plan(plan)}
            for plan in plans
        ],
        "unsupported_spend_recommended": any(
            plan.unsupported_spend_recommended for plan in plans
        ),
        "owner_review_required": True,
        "forecasts_are_estimates": True,
    }


@router.get("/pipeline-value")
def pipeline_value(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = revenue_forecast_dashboard(session)
    session.commit()
    return {
        **dashboard["pipeline_value"],
        "ten_k_likely_deals": dashboard["ten_k_likely_deals"],
        "market_ranking": dashboard["market_scaling_scores"],
        "lead_spend_recommendations": dashboard["lead_spend_plans"],
    }


@router.get("/operator-mode")
def operator_mode(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = operator_mode_dashboard(session)
    session.commit()
    return dashboard


@router.get("/operator-mode/approvals")
def operator_mode_approvals(session: Session = Depends(get_session)) -> dict[str, object]:
    items = session.query(OwnerApprovalItem).all()
    return approval_console_summary(items)


@router.get("/operator-mode/exceptions")
def operator_mode_exceptions(session: Session = Depends(get_session)) -> dict[str, object]:
    exceptions = session.query(OperatorExceptionRecord).all()
    return {
        "exceptions": [model_to_dict(exception) for exception in exceptions],
        "owner_action_required": [
            model_to_dict(exception)
            for exception in exceptions
            if exception.owner_action_required
        ],
    }


@router.get("/operator-mode/daily-report")
def operator_mode_daily_report(session: Session = Depends(get_session)) -> dict[str, object]:
    reports = session.query(AutonomousDailyOperatingReport).all()
    return {
        "daily_reports": [model_to_dict(report) for report in reports],
        "latest_report": model_to_dict(reports[0]) if reports else None,
        "high_risk_actions_executed": False,
    }


@router.get("/operator-mode/system-trust")
def operator_mode_system_trust(session: Session = Depends(get_session)) -> dict[str, object]:
    scores = session.query(SystemTrustScore).all()
    for score in scores:
        calculate_system_trust(score)
    session.commit()
    return {
        "system_trust_scores": [model_to_dict(score) for score in scores],
        "hard_boundary_enforced": True,
    }


@router.get("/operator-mode/settings")
def operator_mode_settings(session: Session = Depends(get_session)) -> dict[str, object]:
    settings_records = session.query(OperatorModeSetting).all()
    return {
        "settings": [
            {**model_to_dict(setting), "gate": operator_mode_gate(setting)}
            for setting in settings_records
        ],
        "available_modes": ["manual", "assisted", "near_autonomous", "semi_autonomous"],
        "level_5_disabled": True,
    }


@router.get("/operator-mode/runs/{run_id}/safety")
def operator_mode_run_safety(
    run_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    loop = session.get(SemiAutonomousCommandLoopRun, run_id)
    if loop is None:
        raise HTTPException(status_code=404, detail="Command loop run not found")
    return {**model_to_dict(loop), "safety": command_loop_safety(loop)}


@router.get("/production-readiness")
def production_readiness(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = production_readiness_dashboard(session)
    session.commit()
    return dashboard


@router.get("/audit-exports")
def audit_exports(session: Session = Depends(get_session)) -> dict[str, object]:
    packets = session.query(AuditExportPacket).all()
    for packet in packets:
        sync_audit_export(packet)
    session.commit()
    return {
        "audit_exports": [
            {**model_to_dict(packet), "gate": audit_export_gate(packet)}
            for packet in packets
        ],
        "raw_private_data_allowed": False,
        "secrets_committed_allowed": False,
    }


@router.get("/audit-exports/{export_id}")
def audit_export_detail(
    export_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    packet = session.get(AuditExportPacket, export_id)
    if packet is None:
        raise HTTPException(status_code=404, detail="Audit export not found")
    sync_audit_export(packet)
    session.commit()
    return {**model_to_dict(packet), "gate": audit_export_gate(packet)}


@router.get("/evidence-attachments")
def evidence_attachments(session: Session = Depends(get_session)) -> dict[str, object]:
    attachments = session.query(EvidenceAttachmentRecord).all()
    return {
        "evidence_attachments": [
            {**model_to_dict(attachment), "gate": attachment_linkage_gate(attachment)}
            for attachment in attachments
        ],
        "source_linkage_required": True,
        "raw_file_path_committed_allowed": False,
    }


@router.get("/provider-readiness")
def provider_readiness(session: Session = Depends(get_session)) -> dict[str, object]:
    providers = session.query(ProviderSandboxReadinessCheck).all()
    return {
        "provider_readiness": [
            {**model_to_dict(provider), "gate": provider_readiness_gate(provider)}
            for provider in providers
        ],
        "default_provider_mode": "mock",
        "real_provider_calls_require_sandbox_and_gates": True,
        "bulk_send_allowed": False,
    }


@router.get("/backups")
def backups(session: Session = Depends(get_session)) -> dict[str, object]:
    records = session.query(BackupExportRecord).all()
    return {
        "backup_exports": [
            {**model_to_dict(record), "safe_metadata": backup_metadata(record)}
            for record in records
        ],
        "safe_metadata_only": True,
        "raw_private_data_allowed": False,
    }


@router.get("/offer-conversion")
def offer_conversion(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = offer_conversion_dashboard(session)
    session.commit()
    return dashboard


@router.get("/offer-conversion/{deal_id}")
def offer_conversion_detail(
    deal_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    deal = session.get(Deal, deal_id)
    if deal is None:
        raise HTTPException(status_code=404, detail="Deal not found")
    dashboard = offer_conversion_dashboard(session)
    session.commit()
    return {
        "deal": model_to_dict(deal),
        "offer_positioning": [
            offer_positioning_summary(record)
            for record in session.query(OfferPositioningRecord)
            .filter(OfferPositioningRecord.deal_id == deal_id)
            .all()
        ],
        "negotiations": [
            negotiation_summary(record)
            for record in session.query(NegotiationRecord)
            .filter(NegotiationRecord.deal_id == deal_id)
            .all()
        ],
        "contract_ready_states": [
            contract_ready_summary(state)
            for state in session.query(ContractReadyState)
            .filter(ContractReadyState.deal_id == deal_id)
            .all()
        ],
        "fastest_path_to_contract": [
            item for item in dashboard["fastest_path_to_contract"] if item["deal_id"] == deal_id
        ],
        "contract_execution_allowed": False,
        "legal_advice_allowed": False,
    }


@router.post("/offer-conversion/safety/validate")
def offer_conversion_safety(payload: ConversionSafetyRequest) -> dict[str, object]:
    return validate_conversion_language(payload.content)


@router.get("/negotiations")
def negotiations(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = offer_conversion_dashboard(session)
    session.commit()
    return {
        "negotiation_records": dashboard["negotiation_records"],
        "high_readiness_sellers": dashboard["high_readiness_sellers"],
        "stalled_negotiations": dashboard["stalled_negotiations"],
        "deals_needing_price_adjustment": dashboard["deals_needing_price_adjustment"],
        "live_negotiation_automation_allowed": False,
        "automatic_acceptance_allowed": False,
    }


@router.get("/negotiations/{record_id}")
def negotiation_detail(
    record_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    record = session.get(NegotiationRecord, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Negotiation record not found")
    summary = negotiation_summary(record)
    session.commit()
    return summary


@router.get("/contract-ready")
def contract_ready(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = offer_conversion_dashboard(session)
    session.commit()
    return {
        "contract_ready_deals": dashboard["contract_ready_deals"],
        "contract_ready_states": dashboard["contract_ready_states"],
        "projected_10k_contracts_ready": dashboard["projected_10k_contracts_ready"],
        "deals_at_risk": dashboard["deals_at_risk"],
        "contract_execution_allowed": False,
        "executable_contract_generation_allowed": False,
        "legal_advice_allowed": False,
        "automatic_acceptance_allowed": False,
    }


@router.get("/title-review")
def title_review(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = title_review_dashboard(session)
    session.commit()
    return dashboard


@router.get("/title-review/{review_id}")
def title_review_detail(
    review_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    record = session.get(TitleReviewCoordination, review_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Title review record not found")
    summary = title_review_coordination_summary(record)
    session.commit()
    return {
        **summary,
        "review_packets": [
            review_packet_prep_summary(packet) for packet in record.review_packets
        ],
    }


@router.post("/title-review/safety/validate")
def title_review_safety(payload: TitleReviewSafetyRequest) -> dict[str, object]:
    return validate_title_review_language(payload.content)


@router.get("/review-packets")
def review_packets(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = title_review_dashboard(session)
    session.commit()
    return {
        "review_packet_preps": dashboard["review_packet_preps"],
        "packet_prep_ready": dashboard["packet_prep_ready"],
        "draft_only": True,
        "document_submission_allowed": False,
        "title_company_email_send_allowed": False,
        "contract_execution_allowed": False,
        "legal_advice_allowed": False,
    }


@router.get("/review-packets/{packet_id}")
def review_packet_detail(
    packet_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    packet = session.get(ReviewPacketPrep, packet_id)
    if packet is None:
        raise HTTPException(status_code=404, detail="Review packet not found")
    summary = review_packet_prep_summary(packet)
    session.commit()
    return summary


@router.get("/autonomy")
def autonomy(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = autonomy_dashboard(session)
    session.commit()
    return dashboard


@router.get("/autonomy/rules")
def autonomy_rules(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = autonomy_dashboard(session)
    session.commit()
    return {
        "automation_rules": dashboard["automation_rules"],
        "level_4_owner_approval_required": dashboard[
            "level_4_owner_approval_required"
        ],
        "level_5_available": False,
        "live_action_allowed": False,
    }


@router.get("/autonomy/runs")
def autonomy_runs(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = autonomy_dashboard(session)
    session.commit()
    return {
        "scheduler_runs": dashboard["scheduler_runs"],
        "automation_attempts": dashboard["automation_attempts"],
        "blocked_attempts": dashboard["blocked_attempts"],
        "real_world_action_taken": False,
    }


@router.get("/autonomy/tasks")
def autonomy_tasks(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = autonomy_dashboard(session)
    session.commit()
    return {
        "autonomous_agent_tasks": dashboard["autonomous_agent_tasks"],
        "draft_creation_tasks": dashboard["draft_creation_tasks"],
        "recommendations_only": True,
        "live_action_allowed": False,
    }


@router.get("/autonomy/daily-briefing")
def autonomy_daily_briefing(session: Session = Depends(get_session)) -> dict[str, object]:
    briefings = (
        session.query(DailyCommandBriefing)
        .order_by(DailyCommandBriefing.created_at.desc())
        .all()
    )
    if not briefings:
        return {
            "daily_command_briefings": [],
            "latest": None,
            "generated_by": "Prime 2",
            "recommendations_only": True,
        }
    return {
        "daily_command_briefings": [
            daily_briefing_summary(briefing) for briefing in briefings
        ],
        "latest": daily_briefing_summary(briefings[0]),
        "generated_by": "Prime 2",
        "recommendations_only": True,
        "live_outreach_allowed": False,
    }


@router.get("/autonomy/escalations")
def autonomy_escalations(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = autonomy_dashboard(session)
    session.commit()
    return {
        "escalations": dashboard["escalations"],
        "escalation_queue": dashboard["escalation_queue"],
        "recommendations_only": True,
        "real_world_action_blocked": True,
    }


@router.post("/autonomy/safety/validate")
def autonomy_safety(payload: AutonomySafetyRequest) -> dict[str, object]:
    return autonomy_safety_guard(
        payload.action,
        payload.autonomy_level,
        owner_approval_recorded=payload.owner_approval_recorded,
    )


@router.post("/autonomy/run")
def autonomy_run(
    payload: AutonomyRunRequest,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return run_scheduler_workflow(
        session,
        payload.workflow_type,
        payload.idempotency_key,
        owner_approval_recorded=payload.owner_approval_recorded,
    )


@router.get("/auto-execution")
def auto_execution(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = auto_execution_dashboard(session)
    session.commit()
    return dashboard


@router.get("/auto-execution/rules")
def auto_execution_rules(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = auto_execution_dashboard(session)
    session.commit()
    return {
        "auto_execution_rules": dashboard["auto_execution_rules"],
        "allowed_actions": dashboard["allowed_actions"],
        "blocked_actions": dashboard["blocked_actions"],
    }


@router.get("/auto-execution/templates")
def auto_execution_templates(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = auto_execution_dashboard(session)
    session.commit()
    return {
        "approved_templates": dashboard["approved_templates"],
        "template_library": [
            "seller follow-up templates",
            "buyer response templates",
            "internal reminder templates",
            "title/review coordination templates",
            "opt-out-safe SMS templates",
            "email templates",
        ],
    }


@router.get("/auto-execution/dry-runs")
def auto_execution_dry_runs(session: Session = Depends(get_session)) -> list[dict]:
    return all_records(session, AutoExecutionDryRun)


@router.get("/auto-execution/attempts")
def auto_execution_attempts(session: Session = Depends(get_session)) -> dict[str, object]:
    dashboard = auto_execution_dashboard(session)
    session.commit()
    return {
        "attempts": dashboard["attempts"],
        "blocked_attempts": dashboard["blocked_attempts"],
        "bulk_send_allowed": False,
        "buyer_blast_allowed": False,
    }


@router.get("/auto-execution/audit")
def auto_execution_audit(session: Session = Depends(get_session)) -> list[dict]:
    return all_records(session, AutoExecutionAuditRecord)


@router.post("/auto-execution/execute")
def auto_execution_execute(
    payload: AutoExecutionRequest,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    return execute_with_auto_gate(
        session,
        rule_id=payload.rule_id,
        template_id=payload.template_id,
        idempotency_key=payload.idempotency_key,
        source_record_type=payload.source_record_type,
        source_record_id=payload.source_record_id,
        recipient_count=payload.recipient_count,
        v5_safety_passed=payload.v5_safety_passed,
        v5_dry_run_receipt_exists=payload.v5_dry_run_receipt_exists,
        v5_approval_recorded=payload.v5_approval_recorded,
        live_flags_enabled=payload.live_flags_enabled,
        provider_ready=payload.provider_ready,
    )


@router.post("/auto-execution/templates/{template_id}/safety")
def auto_execution_template_safety(
    template_id: str,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    template = session.get(ApprovedTemplate, template_id)
    if template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return validate_auto_execution_template(template)


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
