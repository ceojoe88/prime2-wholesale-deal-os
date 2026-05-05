from fastapi.testclient import TestClient

from app.domain.production_readiness import (
    attachment_linkage_gate,
    audit_export_gate,
    backup_metadata,
    production_readiness_gate,
    provider_readiness_gate,
    sanitize_audit_payload,
    sync_audit_export,
)
from app.main import app
from app.models import (
    AuditExportPacket,
    BackupExportRecord,
    DeploymentHardeningCheck,
    EnvironmentReadinessCheck,
    EvidenceAttachmentRecord,
    ProviderSandboxReadinessCheck,
)


def test_audit_exports_sanitize_sensitive_and_internal_fields():
    packet = AuditExportPacket(
        id="audit-test",
        source_record_type="deal",
        source_record_id="deal-001",
        requested_payload={
            "deal_id": "deal-001",
            "seller_name": "Private Seller",
            "buyer_email": "buyer@example.test",
            "lead_source": "internal list",
            "seller_contract_price": 151000,
            "assignment_fee_logic": "internal spread logic",
            "public_summary": "Evidence-backed internal packet",
        },
    )

    gate = sync_audit_export(packet)

    assert gate["allowed"] is True
    assert packet.contains_raw_private_data is False
    assert packet.secrets_included is False
    assert "seller_name" not in packet.sanitized_payload
    assert "buyer_email" not in packet.sanitized_payload
    assert "lead_source" not in packet.sanitized_payload
    assert "assignment_fee_logic" not in packet.sanitized_payload
    assert packet.sanitized_payload["public_summary"] == "Evidence-backed internal packet"
    assert "seller_name" in packet.omitted_sensitive_fields
    assert "assignment_fee_logic" in packet.internal_fields_removed


def test_sanitizer_removes_nested_private_fields():
    sanitized = sanitize_audit_payload(
        {
            "deal": {
                "city": "Dallas",
                "seller_phone": "214-555-0101",
                "internal_notes": "do not export",
            },
            "status": "owner_review",
        }
    )

    assert sanitized == {"deal": {"city": "Dallas"}, "status": "owner_review"}


def test_backup_generates_safe_metadata_only():
    record = BackupExportRecord(
        id="backup-test",
        backup_type="metadata_snapshot",
        backup_scope="operator_local",
        storage_target="local_export_placeholder",
        included_tables=["deals", "buyers", "leads"],
        excluded_fields=["seller_name", "buyer_email", "provider_secret"],
        contains_raw_private_data=True,
        safe_metadata_only=False,
    )

    metadata = backup_metadata(record)

    assert metadata["safe_metadata_only"] is True
    assert metadata["contains_raw_private_data"] is False
    assert "seller_name" in metadata["excluded_fields"]
    assert record.contains_raw_private_data is False
    assert record.safe_metadata_only is True


def test_attachment_records_require_source_linkage():
    attachment = EvidenceAttachmentRecord(
        id="attachment-test",
        source_record_type="",
        source_record_id="",
        deal_id=None,
        evidence_packet_id=None,
    )

    gate = attachment_linkage_gate(attachment)

    assert gate["allowed"] is False
    assert "source_record_link_required" in gate["blocked_reasons"]
    assert "deal_or_evidence_packet_link_required" in gate["blocked_reasons"]
    assert attachment.source_linkage_verified is False


def test_provider_readiness_defaults_blocked():
    provider = ProviderSandboxReadinessCheck(
        id="provider-test",
        provider_type="email",
        provider_name="Email sandbox",
    )

    gate = provider_readiness_gate(provider)

    assert gate["allowed"] is False
    assert provider.provider_calls_allowed is False
    assert "sandbox_ready_required" in gate["blocked_reasons"]
    assert "sandbox_secrets_missing" in gate["blocked_reasons"]


def test_production_readiness_fails_without_auth_env_and_secrets():
    environment = [
        EnvironmentReadinessCheck(
            id="env-auth",
            category="auth",
            check_name="operator auth configured",
            required=True,
            passed=False,
        ),
        EnvironmentReadinessCheck(
            id="env-vars",
            category="env",
            check_name="production env configured",
            required=True,
            passed=False,
        ),
        EnvironmentReadinessCheck(
            id="env-secrets",
            category="secrets",
            check_name="secrets configured outside repo",
            required=True,
            passed=False,
        ),
    ]
    providers = [ProviderSandboxReadinessCheck(id="provider-blocked")]
    hardening = [
        DeploymentHardeningCheck(
            id="hardening-auth",
            check_name="public exposure auth checklist",
            required=True,
            passed=False,
        )
    ]

    gate = production_readiness_gate(environment, providers, hardening)

    assert gate["production_ready"] is False
    assert "auth_checklist_missing" in gate["blocked_reasons"]
    assert "environment_variables_missing" in gate["blocked_reasons"]
    assert "secrets_configuration_missing" in gate["blocked_reasons"]
    assert gate["public_exposure_allowed"] is False
    assert gate["no_secrets_committed"] is True


def test_external_audit_export_requires_owner_approval():
    packet = AuditExportPacket(
        id="audit-external",
        requested_payload={"public_summary": "safe"},
        sanitized_payload={"public_summary": "safe"},
        safe_for_external_share=True,
        owner_approval_status="pending_owner",
    )

    gate = audit_export_gate(packet)

    assert gate["allowed"] is False
    assert "external_share_requires_owner_approval" in gate["blocked_reasons"]


def test_production_readiness_routes_render_backend():
    routes = [
        "/api/production-readiness",
        "/api/audit-exports",
        "/api/audit-exports/audit-export-001",
        "/api/evidence-attachments",
        "/api/provider-readiness",
        "/api/backups",
    ]
    with TestClient(app) as client:
        for route in routes:
            response = client.get(route)
            assert response.status_code == 200, route
