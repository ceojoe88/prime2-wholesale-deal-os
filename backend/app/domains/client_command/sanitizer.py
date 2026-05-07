from __future__ import annotations

from typing import Any

from app.models import (
    ClientLeadDivisionEvent,
    ClientLeadIntelligenceScore,
    ClientLeadMissingDataItem,
    ClientLeadNextBestAction,
    ClientLeadProfile,
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
