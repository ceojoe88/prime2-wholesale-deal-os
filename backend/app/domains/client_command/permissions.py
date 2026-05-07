from __future__ import annotations

from app.models import ClientWorkspaceMember, ClientWorkspaceRole


CLIENT_COMMAND_PERMISSIONS = {
    "client_command.view",
    "client_command.manage",
    "client_command.leads_view",
    "client_command.leads_manage",
    "client_command.reports_view",
    "client_command.acquisition_view",
    "client_command.acquisition_manage",
    "client_command.underwriting_view",
    "client_command.underwriting_manage",
    "client_command.offer_review",
    "client_command.disposition_view",
    "client_command.disposition_manage",
    "client_command.buyers_view",
    "client_command.buyers_manage",
    "client_command.buyer_matching_view",
    "client_command.buyer_matching_manage",
    "client_command.admin",
}


def normalize_permissions(values: list[str] | None) -> list[str]:
    return sorted({value for value in (values or []) if value in CLIENT_COMMAND_PERMISSIONS})


def role_permissions(role: ClientWorkspaceRole | None) -> list[str]:
    if role is None:
        return []
    return normalize_permissions(role.permissions)


def member_permissions(
    member: ClientWorkspaceMember | None,
    role: ClientWorkspaceRole | None,
) -> list[str]:
    if member is None:
        return []
    return normalize_permissions(role_permissions(role) + (member.permission_overrides or []))


def has_permission(
    member: ClientWorkspaceMember | None,
    role: ClientWorkspaceRole | None,
    permission: str,
) -> bool:
    permissions = set(member_permissions(member, role))
    return permission in permissions or "client_command.admin" in permissions
