from __future__ import annotations

from typing import Any

from app.models import (
    ClientAcquisitionBrief,
    ClientAcquisitionDivisionEvent,
    ClientAppointmentReadinessReview,
    ClientDealEvidenceItem,
    ClientDealEvidencePacket,
    ClientFollowUpDraft,
    ClientLeadDivisionEvent,
    ClientLeadIntelligenceScore,
    ClientLeadMissingDataItem,
    ClientLeadNextBestAction,
    ClientLeadProfile,
    ClientObjectionResponseDraft,
    ClientOfferReadinessGate,
    ClientOfferScenario,
    ClientSellerQuestion,
    ClientSellerQuestionPlan,
    ClientUnderwritingDivisionEvent,
    ClientUnderwritingReview,
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
