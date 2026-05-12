from __future__ import annotations

from typing import Any

from app.models import (
    ClientAcquisitionBrief,
    ClientAcquisitionDivisionEvent,
    ClientAppointmentReadinessReview,
    ClientActivationBlocker,
    ClientBuyerBuyBox,
    ClientBuyerConfidenceScore,
    ClientBuyerDemandEvidence,
    ClientBuyerListSetup,
    ClientBuyerOutreachDraft,
    ClientBusinessProfile,
    ClientBuyerProfile,
    ClientComplianceSetupChecklist,
    ClientCommunicationApprovalGate,
    ClientComplianceDivisionEvent,
    ClientComplianceReadinessPlaceholder,
    ClientContactConsentRecord,
    ClientContactOptOutRecord,
    ClientDealEvidenceItem,
    ClientDealEvidencePacket,
    ClientDealBuyerMatch,
    ClientDispositionDivisionEvent,
    ClientDispositionReadinessGate,
    ClientFollowUpDraft,
    ClientFirstLeadImportChecklist,
    ClientFirstWeeklyCycleReadiness,
    ClientGoLiveReadinessGate,
    ClientLeadDivisionEvent,
    ClientLeadIntelligenceScore,
    ClientLeadMissingDataItem,
    ClientLeadNextBestAction,
    ClientLeadProfile,
    ClientLeadSourceSetup,
    ClientMarketSetup,
    ClientMessageRiskReview,
    ClientObjectionResponseDraft,
    ClientOnboardingManagerEvent,
    ClientOnboardingReport,
    ClientOnboardingTask,
    ClientOnboardingTimelineEvent,
    ClientPlanCatalog,
    ClientPlanFeature,
    ClientPlanLimit,
    ClientWorkspacePlanAssignment,
    ClientFeatureGateEvaluation,
    ClientUsageCounter,
    ClientSeatUsageRecord,
    ClientPlanUpgradeRecommendation,
    ClientBillingReadinessRecord,
    ClientSubscriptionPlaceholder,
    ClientPlanGateEvent,
    ClientCommunicationProviderProfile,
    ClientCommunicationLiveReadinessCheck,
    ClientCommunicationDryRunReceipt,
    ClientCommunicationSendApproval,
    ClientCommunicationSendAttempt,
    ClientCommunicationExternalMessageReference,
    ClientCommunicationIdempotencyRecord,
    ClientCommunicationLiveFlag,
    ClientCommunicationGateEvent,
    ClientBillingProviderProfile,
    ClientBillingLiveFlag,
    ClientBillingCustomerProfile,
    ClientBillingReadinessCheck,
    ClientCheckoutDryRunReceipt,
    ClientBillingApproval,
    ClientBillingAttempt,
    ClientBillingExternalReference,
    ClientBillingWebhookEventPlaceholder,
    ClientBillingLedgerEntry,
    ClientBillingGateEvent,
    ClientPilotProgram,
    ClientPilotWorkspaceEnrollment,
    ClientPilotOperatingMode,
    ClientPilotHealthSnapshot,
    ClientPilotSupportTicket,
    ClientPilotSupportAction,
    ClientPilotEscalation,
    ClientPilotAdminNote,
    ClientPilotClientSafeUpdate,
    ClientPilotLaunchChecklist,
    ClientPilotRiskReview,
    ClientPilotOutcomeCheckpoint,
    ClientPilotEvent,
    ClientOfferReadinessGate,
    ClientOfferScenario,
    ClientPipelineSetup,
    ClientPipelineStageTemplate,
    ClientSafeContactStatus,
    ClientSellerQuestion,
    ClientSellerQuestionPlan,
    ClientStrategyProfile,
    ClientTeamSetupChecklist,
    ClientUnderwritingDivisionEvent,
    ClientUnderwritingReview,
    ClientWorkspaceReadinessScore,
    ClientWeeklyBottleneck,
    ClientWeeklyCommandReport,
    ClientWeeklyDivisionSummary,
    ClientWeeklyLeadStatusRollup,
    ClientWeeklyRecommendedAction,
    ClientWeeklyReportEvent,
    ClientWeeklyReportMetricSnapshot,
    ClientWorkspace,
    ClientWorkspaceMember,
    ClientWorkspaceRole,
)
from app.serializers import model_to_dict


FORBIDDEN_KEYS = {
    "internal_prime_governance_notes",
    "internal_prime_governance_visible",
    "can_view_internal_governance",
    "raw_provider_payload",
    "raw_provider_payload_exposed",
    "raw_provider_payload_exposure_allowed",
    "can_view_raw_provider_payloads",
    "raw_risk_logic",
    "raw_scoring_logic",
    "raw_underwriting_logic",
    "raw_risk_reasoning",
    "internal_notes",
    "audit_internals",
    "provider_config",
    "provider_secret",
    "secret_value",
    "secrets",
    "legal_conclusion",
    "legal_conclusions",
    "hidden_policy_logic",
    "unsafe_execution_fields",
    "billing_internals",
    "billing_internal_state",
    "live_provider_flags",
    "live_provider_enabled",
    "provider_payload",
    "admin_only_controls_visible",
    "can_use_admin_controls",
}


def strip_forbidden(data: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in data.items() if key not in FORBIDDEN_KEYS}


def workspace_public(workspace: ClientWorkspace) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(workspace))
    data["client_safe"] = True
    data["live_outreach_enabled"] = False
    data["billing_enabled"] = False
    data["contract_esign_enabled"] = False
    return data


def role_public(role: ClientWorkspaceRole) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(role))
    data["tenant_safe"] = True
    return data


def member_public(member: ClientWorkspaceMember) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(member))
    data["tenant_safe"] = True
    data["client_workspace_safe"] = True
    return data


def lead_public(lead: ClientLeadProfile) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(lead))
    data["outbound_provider_action_allowed"] = False
    data["client_safe"] = True
    return data


def score_public(score: ClientLeadIntelligenceScore) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(score))
    data["client_safe"] = True
    return data


def action_public(action: ClientLeadNextBestAction) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(action))
    data["outbound_action_allowed"] = False
    data["provider_action_allowed"] = False
    return data


def missing_item_public(item: ClientLeadMissingDataItem) -> dict[str, Any]:
    return strip_forbidden(model_to_dict(item))


def event_public(event: ClientLeadDivisionEvent) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(event))
    data["safe_for_client"] = True
    return data


def acquisition_brief_public(brief: ClientAcquisitionBrief) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(brief))
    data["client_safe"] = True
    data["manager_name"] = "Acquisition Manager"
    return data


def question_plan_public(plan: ClientSellerQuestionPlan) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(plan))
    data["client_safe"] = True
    return data


def seller_question_public(question: ClientSellerQuestion) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(question))
    data["client_safe"] = True
    return data


def objection_draft_public(draft: ClientObjectionResponseDraft) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(draft))
    data["client_safe"] = True
    data["manual_use_only"] = True
    return data


def follow_up_draft_public(draft: ClientFollowUpDraft) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(draft))
    data["client_safe"] = True
    data["manual_use_only"] = True
    data["no_live_send"] = True
    return data


def appointment_readiness_public(review: ClientAppointmentReadinessReview) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(review))
    data["client_safe"] = True
    return data


def acquisition_event_public(event: ClientAcquisitionDivisionEvent) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(event))
    data["client_visible"] = True
    return data


def evidence_packet_public(packet: ClientDealEvidencePacket) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(packet))
    data["client_safe"] = True
    return data


def evidence_item_public(item: ClientDealEvidenceItem) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(item))
    data["client_safe"] = True
    return data


def underwriting_review_public(review: ClientUnderwritingReview) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(review))
    data["client_safe"] = True
    return data


def offer_scenario_public(scenario: ClientOfferScenario) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(scenario))
    data["client_safe"] = True
    return data


def offer_readiness_public(gate: ClientOfferReadinessGate) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(gate))
    data["can_present_offer"] = bool(gate.can_present_offer)
    data["no_contract_generated"] = True
    data["no_offer_sent"] = True
    data["client_safe"] = True
    return data


def underwriting_event_public(event: ClientUnderwritingDivisionEvent) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(event))
    data["client_visible"] = True
    return data


def buyer_profile_public(buyer: ClientBuyerProfile) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(buyer))
    data["client_safe"] = True
    return data


def buyer_buy_box_public(buy_box: ClientBuyerBuyBox) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(buy_box))
    data["client_safe"] = True
    return data


def buyer_confidence_public(score: ClientBuyerConfidenceScore) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(score))
    data["client_safe"] = True
    return data


def deal_buyer_match_public(match: ClientDealBuyerMatch) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(match))
    data["client_safe"] = True
    return data


def buyer_demand_evidence_public(evidence: ClientBuyerDemandEvidence) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(evidence))
    data["client_safe"] = True
    return data


def disposition_readiness_public(gate: ClientDispositionReadinessGate) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(gate))
    data["no_buyer_contacted"] = True
    data["no_campaign_started"] = True
    data["no_contract_generated"] = True
    data["client_safe"] = True
    return data


def buyer_outreach_draft_public(draft: ClientBuyerOutreachDraft) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(draft))
    data["manual_use_only"] = True
    data["no_live_send"] = True
    data["no_blast"] = True
    data["client_safe"] = True
    return data


def disposition_event_public(event: ClientDispositionDivisionEvent) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(event))
    data["client_visible"] = True
    return data


def consent_record_public(record: ClientContactConsentRecord) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(record))
    data["client_safe"] = True
    return data


def opt_out_record_public(record: ClientContactOptOutRecord) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(record))
    data["client_safe"] = True
    return data


def safe_contact_status_public(status: ClientSafeContactStatus) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(status))
    data["can_use_manual_draft"] = bool(status.can_use_manual_draft)
    data["no_live_send"] = True
    data["no_provider_check"] = True
    data["client_safe"] = True
    return data


def message_risk_review_public(review: ClientMessageRiskReview) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(review))
    data["manual_use_only"] = True
    data["no_live_send"] = True
    data["client_safe"] = True
    return data


def communication_approval_gate_public(gate: ClientCommunicationApprovalGate) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(gate))
    data["no_live_send"] = True
    data["no_provider_call"] = True
    data["no_campaign_started"] = True
    data["client_safe"] = True
    return data


def compliance_placeholder_public(placeholder: ClientComplianceReadinessPlaceholder) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(placeholder))
    data["required_before_live"] = True
    data["no_provider_call"] = True
    data["client_safe"] = True
    return data


def compliance_event_public(event: ClientComplianceDivisionEvent) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(event))
    data["client_visible"] = True
    return data


def weekly_report_public(report: ClientWeeklyCommandReport) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(report))
    data["no_revenue_guarantee"] = True
    data["no_roi_claim"] = True
    data["no_live_actions_taken"] = True
    data["client_safe"] = True
    return data


def weekly_metric_snapshot_public(snapshot: ClientWeeklyReportMetricSnapshot) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(snapshot))
    data["client_safe"] = True
    return data


def weekly_lead_rollup_public(rollup: ClientWeeklyLeadStatusRollup) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(rollup))
    data["client_safe"] = True
    return data


def weekly_bottleneck_public(bottleneck: ClientWeeklyBottleneck) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(bottleneck))
    data["client_safe"] = True
    return data


def weekly_recommended_action_public(action: ClientWeeklyRecommendedAction) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(action))
    data["client_safe"] = True
    return data


def weekly_division_summary_public(summary: ClientWeeklyDivisionSummary) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(summary))
    data["client_safe"] = True
    return data


def weekly_report_event_public(event: ClientWeeklyReportEvent) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(event))
    data["client_visible"] = True
    return data


def business_profile_public(profile: ClientBusinessProfile) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(profile))
    data["client_safe"] = True
    return data


def strategy_profile_public(profile: ClientStrategyProfile) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(profile))
    data["client_safe"] = True
    return data


def market_setup_public(market: ClientMarketSetup) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(market))
    data["client_safe"] = True
    data["no_live_data_provider"] = True
    return data


def pipeline_setup_public(pipeline: ClientPipelineSetup) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(pipeline))
    data["client_safe"] = True
    return data


def pipeline_stage_public(stage: ClientPipelineStageTemplate) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(stage))
    data["client_safe"] = True
    return data


def lead_source_setup_public(source: ClientLeadSourceSetup) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(source))
    data["client_safe"] = True
    data["provider_connected"] = False
    data["no_provider_sync"] = True
    return data


def buyer_list_setup_public(setup: ClientBuyerListSetup) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(setup))
    data["client_safe"] = True
    data["no_buyer_contacted"] = True
    data["no_campaign_started"] = True
    return data


def team_setup_checklist_public(checklist: ClientTeamSetupChecklist) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(checklist))
    data["client_safe"] = True
    return data


def compliance_setup_checklist_public(checklist: ClientComplianceSetupChecklist) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(checklist))
    data["client_safe"] = True
    data["no_provider_check"] = True
    data["no_live_registration"] = True
    return data


def first_lead_import_checklist_public(checklist: ClientFirstLeadImportChecklist) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(checklist))
    data["client_safe"] = True
    data["no_external_import"] = True
    return data


def workspace_readiness_public(score: ClientWorkspaceReadinessScore) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(score))
    data["client_safe"] = True
    data["no_live_actions_enabled"] = True
    return data


def activation_blocker_public(blocker: ClientActivationBlocker) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(blocker))
    data["client_safe"] = True
    return data


def go_live_gate_public(gate: ClientGoLiveReadinessGate) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(gate))
    data["client_safe"] = True
    data["no_live_communication"] = True
    data["no_provider_execution"] = True
    data["no_billing_action"] = True
    data["no_contract_action"] = True
    data["no_campaign_action"] = True
    return data


def onboarding_task_public(task: ClientOnboardingTask) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(task))
    data["client_safe"] = True
    return data


def onboarding_timeline_event_public(event: ClientOnboardingTimelineEvent) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(event))
    data["client_visible"] = True
    return data


def first_weekly_cycle_readiness_public(readiness: ClientFirstWeeklyCycleReadiness) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(readiness))
    data["client_safe"] = True
    data["no_live_actions_taken"] = True
    return data


def onboarding_report_public(report: ClientOnboardingReport) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(report))
    data["client_safe"] = True
    data["no_live_actions_enabled"] = True
    data["no_revenue_guarantee"] = True
    data["no_roi_claim"] = True
    return data


def onboarding_manager_event_public(event: ClientOnboardingManagerEvent) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(event))
    data["client_visible"] = True
    return data


def plan_catalog_public(plan: ClientPlanCatalog) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(plan))
    data["client_safe"] = True
    data["no_live_billing"] = True
    data["no_payment_collected"] = True
    return data


def plan_feature_public(feature: ClientPlanFeature) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(feature))
    data["client_safe"] = True
    return data


def plan_limit_public(limit: ClientPlanLimit) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(limit))
    data["client_safe"] = True
    return data


def plan_assignment_public(assignment: ClientWorkspacePlanAssignment) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(assignment))
    data["client_safe"] = True
    data["no_live_billing"] = True
    data["no_payment_collected"] = True
    return data


def feature_gate_public(gate: ClientFeatureGateEvaluation) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(gate))
    data["client_safe"] = True
    data["no_live_action"] = True
    return data


def usage_counter_public(counter: ClientUsageCounter) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(counter))
    data["client_safe"] = True
    return data


def seat_usage_public(record: ClientSeatUsageRecord) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(record))
    data["client_safe"] = True
    return data


def upgrade_recommendation_public(recommendation: ClientPlanUpgradeRecommendation) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(recommendation))
    data["client_safe"] = True
    return data


def billing_readiness_record_public(record: ClientBillingReadinessRecord) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(record))
    data["client_safe"] = True
    data["no_provider_call"] = True
    data["no_payment_collected"] = True
    data["no_invoice_created"] = True
    return data


def subscription_placeholder_public(placeholder: ClientSubscriptionPlaceholder) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(placeholder))
    data["client_safe"] = True
    data["no_live_billing"] = True
    data["no_payment_collected"] = True
    return data


def plan_gate_event_public(event: ClientPlanGateEvent) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(event))
    data["client_visible"] = True
    return data


def communication_provider_public(profile: ClientCommunicationProviderProfile) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(profile))
    data["client_safe"] = True
    data["secret_present"] = bool(profile.secret_present)
    return data


def communication_readiness_check_public(check: ClientCommunicationLiveReadinessCheck) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(check))
    data["client_safe"] = True
    data["no_live_send"] = True
    return data


def communication_dry_run_public(receipt: ClientCommunicationDryRunReceipt) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(receipt))
    data["client_safe"] = True
    data["no_live_send"] = True
    return data


def communication_send_approval_public(approval: ClientCommunicationSendApproval) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(approval))
    data["client_safe"] = True
    data["no_live_send"] = True
    return data


def communication_send_attempt_public(attempt: ClientCommunicationSendAttempt) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(attempt))
    data["client_safe"] = True
    data["no_bulk"] = True
    return data


def communication_external_reference_public(reference: ClientCommunicationExternalMessageReference) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(reference))
    data["client_safe"] = True
    return data


def communication_idempotency_public(record: ClientCommunicationIdempotencyRecord) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(record))
    data["client_safe"] = True
    return data


def communication_live_flag_public(flag: ClientCommunicationLiveFlag) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(flag))
    data["client_safe"] = True
    return data


def communication_gate_event_public(event: ClientCommunicationGateEvent) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(event))
    data["client_visible"] = True
    return data


def billing_provider_public(profile: ClientBillingProviderProfile) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(profile))
    data["client_safe"] = True
    data["secret_present"] = bool(profile.secret_present)
    return data


def billing_live_flag_public(flag: ClientBillingLiveFlag) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(flag))
    data["client_safe"] = True
    return data


def billing_customer_profile_public(profile: ClientBillingCustomerProfile) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(profile))
    data["client_safe"] = True
    data["raw_card_data_present"] = False
    return data


def billing_readiness_check_public(check: ClientBillingReadinessCheck) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(check))
    data["client_safe"] = True
    data["no_payment_collected"] = True
    data["no_invoice_created"] = True
    return data


def checkout_dry_run_public(receipt: ClientCheckoutDryRunReceipt) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(receipt))
    data["client_safe"] = True
    data["no_payment_collected"] = True
    return data


def billing_approval_public(approval: ClientBillingApproval) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(approval))
    data["client_safe"] = True
    data["no_payment_collected"] = True
    return data


def billing_attempt_public(attempt: ClientBillingAttempt) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(attempt))
    data["client_safe"] = True
    data["no_raw_card_data"] = True
    return data


def billing_external_reference_public(reference: ClientBillingExternalReference) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(reference))
    data["client_safe"] = True
    return data


def billing_webhook_placeholder_public(event: ClientBillingWebhookEventPlaceholder) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(event))
    data["client_safe"] = True
    return data


def billing_ledger_public(entry: ClientBillingLedgerEntry) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(entry))
    data["client_safe"] = True
    return data


def billing_gate_event_public(event: ClientBillingGateEvent) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(event))
    data["client_visible"] = True
    return data


def pilot_program_public(program: ClientPilotProgram) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(program))
    data["client_safe"] = True
    return data


def pilot_enrollment_public(enrollment: ClientPilotWorkspaceEnrollment) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(enrollment))
    data["client_safe"] = True
    return data


def pilot_operating_mode_public(mode: ClientPilotOperatingMode) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(mode))
    data["client_safe"] = True
    data["no_gate_bypass"] = True
    return data


def pilot_health_snapshot_public(snapshot: ClientPilotHealthSnapshot) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(snapshot))
    data["client_safe"] = True
    return data


def pilot_support_ticket_public(ticket: ClientPilotSupportTicket) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(ticket))
    data["client_safe"] = True
    return data


def pilot_support_action_public(action: ClientPilotSupportAction) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(action))
    data["client_visible"] = bool(action.client_visible)
    return data


def pilot_escalation_public(escalation: ClientPilotEscalation) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(escalation))
    data["client_safe"] = True
    return data


def pilot_admin_note_public(note: ClientPilotAdminNote) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(note))
    data["client_visible"] = False
    return data


def pilot_client_safe_update_public(update: ClientPilotClientSafeUpdate) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(update))
    data["client_safe"] = True
    data["hides_admin_notes"] = True
    return data


def pilot_launch_checklist_public(checklist: ClientPilotLaunchChecklist) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(checklist))
    data["client_safe"] = True
    return data


def pilot_risk_review_public(review: ClientPilotRiskReview) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(review))
    data["client_safe"] = True
    return data


def pilot_outcome_checkpoint_public(checkpoint: ClientPilotOutcomeCheckpoint) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(checkpoint))
    data["client_safe"] = True
    return data


def pilot_event_public(event: ClientPilotEvent) -> dict[str, Any]:
    data = strip_forbidden(model_to_dict(event))
    data["client_visible"] = True
    return data
