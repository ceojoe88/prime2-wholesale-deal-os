from __future__ import annotations

from uuid import uuid4

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.domains.client_command.permissions import (
    CLIENT_COMMAND_PERMISSIONS,
    has_permission,
    member_permissions,
)
from app.domains.client_command.safety import client_command_safety_rules
from app.domains.client_command.sanitizer import (
    action_public,
    event_public,
    lead_public,
    member_public,
    missing_item_public,
    role_public,
    score_public,
    workspace_public,
)
from app.domains.client_command.scoring import missing_fields, score_client_lead
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


def lead_detail(session: Session, lead_id: str, workspace_id: str | None = None) -> dict[str, object]:
    lead = _lead_or_404(session, lead_id, workspace_id)
    score = ensure_score(session, lead)
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
    }
    return labels.get(action_type, "Review next best action")
