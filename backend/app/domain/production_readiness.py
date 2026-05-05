from __future__ import annotations

import hashlib
import json
from typing import Any

from sqlalchemy.orm import Session

from app.models import (
    ApprovalUxReview,
    AuditExportPacket,
    BackupExportRecord,
    DeploymentHardeningCheck,
    EnvironmentReadinessCheck,
    EvidenceAttachmentRecord,
    ProviderSandboxReadinessCheck,
)
from app.serializers import model_to_dict


SENSITIVE_EXPORT_FIELDS = {
    "address",
    "buyer_email",
    "buyer_name",
    "buyer_phone",
    "email",
    "phone",
    "seller_contact",
    "seller_email",
    "seller_name",
    "seller_phone",
}

INTERNAL_EXPORT_FIELDS = {
    "agent_recommendations",
    "assignment_fee_logic",
    "buyer_purchase_price",
    "compliance_internals",
    "internal_notes",
    "internal_profit_logic",
    "lead_source",
    "mao",
    "motivation_score",
    "negotiation_notes",
    "seller_contract_price",
    "seller_temperature",
    "spread_strategy",
    "wholesale_prime_recommendations",
}

SECRET_EXPORT_FIELDS = {
    "api_key",
    "authorization",
    "oauth_token",
    "password",
    "provider_secret",
    "secret",
    "token",
}

UNSAFE_EXPORT_FIELDS = SENSITIVE_EXPORT_FIELDS | INTERNAL_EXPORT_FIELDS | SECRET_EXPORT_FIELDS


def _normalize_key(key: str) -> str:
    return key.strip().lower().replace("-", "_").replace(" ", "_")


def sanitize_audit_payload(payload: dict[str, Any]) -> dict[str, Any]:
    sanitized, _, _ = sanitize_audit_payload_with_report(payload)
    return sanitized


def sanitize_audit_payload_with_report(
    payload: dict[str, Any],
) -> tuple[dict[str, Any], list[str], list[str]]:
    omitted_sensitive: set[str] = set()
    removed_internal: set[str] = set()

    def scrub(value: Any) -> Any:
        if isinstance(value, dict):
            cleaned: dict[str, Any] = {}
            for key, child in value.items():
                normalized = _normalize_key(str(key))
                if normalized in SENSITIVE_EXPORT_FIELDS or normalized in SECRET_EXPORT_FIELDS:
                    omitted_sensitive.add(str(key))
                    continue
                if normalized in INTERNAL_EXPORT_FIELDS:
                    removed_internal.add(str(key))
                    continue
                cleaned[str(key)] = scrub(child)
            return cleaned
        if isinstance(value, list):
            return [scrub(item) for item in value]
        return value

    return scrub(payload), sorted(omitted_sensitive), sorted(removed_internal)


def sync_audit_export(packet: AuditExportPacket) -> dict[str, object]:
    sanitized, omitted_sensitive, removed_internal = sanitize_audit_payload_with_report(
        packet.requested_payload or {}
    )
    packet.sanitized_payload = sanitized
    packet.omitted_sensitive_fields = omitted_sensitive
    packet.internal_fields_removed = removed_internal
    packet.packet_hash = hashlib.sha256(
        json.dumps(sanitized, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()
    packet.contains_raw_private_data = False
    packet.secrets_included = False
    gate = audit_export_gate(packet)
    packet.blocked_reasons = gate["blocked_reasons"]
    packet.export_status = "ready_for_owner_review" if gate["allowed"] else "blocked"
    return gate


def audit_export_gate(packet: AuditExportPacket) -> dict[str, object]:
    reasons: list[str] = []
    if packet.contains_raw_private_data:
        reasons.append("raw_private_data_blocked")
    if packet.secrets_included:
        reasons.append("secrets_blocked_from_export")
    if packet.legal_advice_included:
        reasons.append("legal_advice_blocked")
    if packet.safe_for_external_share and packet.owner_approval_status != "approved":
        reasons.append("external_share_requires_owner_approval")
    if not packet.sanitized_payload:
        reasons.append("sanitized_payload_required")
    return {
        "allowed": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "sanitized_only": True,
        "raw_private_data_allowed": False,
        "legal_advice_allowed": False,
        "secrets_allowed": False,
    }


def attachment_linkage_gate(attachment: EvidenceAttachmentRecord) -> dict[str, object]:
    reasons: list[str] = []
    if not attachment.source_record_type or not attachment.source_record_id:
        reasons.append("source_record_link_required")
    if not attachment.deal_id and not attachment.evidence_packet_id:
        reasons.append("deal_or_evidence_packet_link_required")
    if attachment.raw_file_path_committed:
        reasons.append("raw_file_path_must_not_be_committed")
    if attachment.contains_sensitive_data and attachment.safe_to_export:
        reasons.append("sensitive_attachment_cannot_be_export_ready")
    attachment.source_linkage_verified = not reasons
    attachment.blocked_reasons = sorted(set(reasons))
    return {
        "allowed": not reasons,
        "blocked_reasons": attachment.blocked_reasons,
        "source_linkage_required": True,
        "raw_file_path_committed_allowed": False,
    }


def backup_metadata(record: BackupExportRecord) -> dict[str, object]:
    metadata = {
        "backup_id": record.id,
        "backup_type": record.backup_type,
        "scope": record.backup_scope,
        "included_table_count": len(record.included_tables),
        "excluded_fields": sorted(set(record.excluded_fields)),
        "storage_target": record.storage_target,
        "restore_test_status": record.restore_test_status,
        "contains_raw_private_data": False,
        "safe_metadata_only": True,
    }
    record.safe_metadata = metadata
    record.contains_raw_private_data = False
    record.safe_metadata_only = True
    record.blocked_reasons = []
    return metadata


def provider_readiness_gate(check: ProviderSandboxReadinessCheck) -> dict[str, object]:
    reasons: list[str] = []
    if check.mode not in {"mock", "sandbox"}:
        reasons.append("production_provider_mode_blocked")
    if not check.sandbox_ready:
        reasons.append("sandbox_ready_required")
    if not check.secrets_configured:
        reasons.append("sandbox_secrets_missing")
    for flag, reason in [
        (check.safety_check_required, "safety_check_required"),
        (check.dry_run_required, "dry_run_required"),
        (check.owner_approval_required, "owner_approval_required"),
        (check.idempotency_required, "idempotency_required"),
        (check.audit_trail_required, "audit_trail_required"),
    ]:
        if not flag:
            reasons.append(reason)
    check.provider_calls_allowed = not reasons and check.mode == "sandbox"
    check.readiness_status = "sandbox_ready" if check.provider_calls_allowed else "blocked"
    check.blocked_reasons = sorted(set(reasons))
    return {
        "allowed": check.provider_calls_allowed,
        "blocked_reasons": check.blocked_reasons,
        "real_provider_calls_require_sandbox_and_gates": True,
        "bulk_send_allowed": False,
    }


def production_readiness_gate(
    environment_checks: list[EnvironmentReadinessCheck],
    provider_checks: list[ProviderSandboxReadinessCheck],
    hardening_checks: list[DeploymentHardeningCheck],
) -> dict[str, object]:
    reasons: list[str] = []
    if any(check.required and not check.passed for check in environment_checks):
        reasons.append("required_environment_checks_missing")
    if any(
        check.category == "auth" and check.required and not check.passed
        for check in environment_checks
    ):
        reasons.append("auth_checklist_missing")
    if any(
        check.category == "env" and check.required and not check.passed
        for check in environment_checks
    ):
        reasons.append("environment_variables_missing")
    if any(
        check.category == "secrets" and check.required and not check.passed
        for check in environment_checks
    ):
        reasons.append("secrets_configuration_missing")
    provider_gates = [provider_readiness_gate(check) for check in provider_checks]
    if any(not gate["allowed"] for gate in provider_gates):
        reasons.append("provider_sandbox_readiness_blocked")
    if any(check.required and not check.passed for check in hardening_checks):
        reasons.append("deployment_hardening_incomplete")
    if any(
        check.check_name == "public exposure auth checklist" and not check.passed
        for check in hardening_checks
    ):
        reasons.append("public_production_exposure_blocked_without_auth")
    return {
        "production_ready": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "public_exposure_allowed": False,
        "real_provider_calls_allowed": all(gate["allowed"] for gate in provider_gates),
        "no_secrets_committed": True,
        "owner_final_approval_required": True,
    }


def production_readiness_dashboard(session: Session) -> dict[str, object]:
    approvals = session.query(ApprovalUxReview).all()
    audit_exports = session.query(AuditExportPacket).all()
    attachments = session.query(EvidenceAttachmentRecord).all()
    backups = session.query(BackupExportRecord).all()
    providers = session.query(ProviderSandboxReadinessCheck).all()
    environment = session.query(EnvironmentReadinessCheck).all()
    hardening = session.query(DeploymentHardeningCheck).all()

    for packet in audit_exports:
        sync_audit_export(packet)
    for attachment in attachments:
        attachment_linkage_gate(attachment)
    for backup in backups:
        backup_metadata(backup)
    provider_gates = {provider.id: provider_readiness_gate(provider) for provider in providers}
    readiness_gate = production_readiness_gate(environment, providers, hardening)

    return {
        "production_gate": readiness_gate,
        "approval_ux_reviews": [model_to_dict(review) for review in approvals],
        "audit_exports": [
            {**model_to_dict(packet), "gate": audit_export_gate(packet)}
            for packet in audit_exports
        ],
        "evidence_attachments": [
            {**model_to_dict(attachment), "gate": attachment_linkage_gate(attachment)}
            for attachment in attachments
        ],
        "backup_exports": [
            {**model_to_dict(backup), "safe_metadata": backup_metadata(backup)}
            for backup in backups
        ],
        "provider_readiness": [
            {**model_to_dict(provider), "gate": provider_gates[provider.id]}
            for provider in providers
        ],
        "environment_readiness": [model_to_dict(check) for check in environment],
        "deployment_hardening": [model_to_dict(check) for check in hardening],
        "counts": {
            "approval_reviews": len(approvals),
            "audit_exports": len(audit_exports),
            "attachments": len(attachments),
            "backups": len(backups),
            "providers": len(providers),
            "environment_checks": len(environment),
            "hardening_checks": len(hardening),
        },
        "safety_boundary": {
            "real_provider_calls_require_sandbox": True,
            "legal_advice_allowed": False,
            "public_production_exposure_without_auth_allowed": False,
            "secrets_committed_allowed": False,
            "raw_private_export_allowed": False,
        },
    }
