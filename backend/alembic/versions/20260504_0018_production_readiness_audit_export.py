"""production readiness audit export

Revision ID: 20260504_0018
Revises: 20260504_0017
Create Date: 2026-05-04 00:18:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260504_0018"
down_revision = "20260504_0017"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "approval_ux_reviews",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("owner_approval_item_id", sa.String(length=80), nullable=True),
        sa.Column("approval_type", sa.String(length=120), nullable=False),
        sa.Column("source_record_type", sa.String(length=120), nullable=False),
        sa.Column("source_record_id", sa.String(length=120), nullable=False),
        sa.Column("context_summary", sa.Text(), nullable=False),
        sa.Column("risk_summary", sa.Text(), nullable=False),
        sa.Column("gate_summary", sa.JSON(), nullable=False),
        sa.Column("confirmation_prompt", sa.Text(), nullable=False),
        sa.Column("recommended_decision", sa.String(length=80), nullable=False),
        sa.Column("approval_status", sa.String(length=80), nullable=False),
        sa.Column("owner_action_required", sa.Boolean(), nullable=False),
        sa.Column("approval_is_not_execution", sa.Boolean(), nullable=False),
        sa.Column("blocked_reasons", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["owner_approval_item_id"], ["owner_approval_items.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "audit_export_packets",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("export_type", sa.String(length=120), nullable=False),
        sa.Column("source_record_type", sa.String(length=120), nullable=False),
        sa.Column("source_record_id", sa.String(length=120), nullable=False),
        sa.Column("requested_by", sa.String(length=120), nullable=False),
        sa.Column("export_scope", sa.String(length=120), nullable=False),
        sa.Column("requested_payload", sa.JSON(), nullable=False),
        sa.Column("sanitized_payload", sa.JSON(), nullable=False),
        sa.Column("included_record_ids", sa.JSON(), nullable=False),
        sa.Column("omitted_sensitive_fields", sa.JSON(), nullable=False),
        sa.Column("internal_fields_removed", sa.JSON(), nullable=False),
        sa.Column("export_status", sa.String(length=80), nullable=False),
        sa.Column("owner_approval_status", sa.String(length=80), nullable=False),
        sa.Column("safe_for_external_share", sa.Boolean(), nullable=False),
        sa.Column("contains_raw_private_data", sa.Boolean(), nullable=False),
        sa.Column("legal_advice_included", sa.Boolean(), nullable=False),
        sa.Column("secrets_included", sa.Boolean(), nullable=False),
        sa.Column("packet_hash", sa.String(length=128), nullable=False),
        sa.Column("retention_notes", sa.Text(), nullable=False),
        sa.Column("blocked_reasons", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "evidence_attachment_records",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("source_record_type", sa.String(length=120), nullable=False),
        sa.Column("source_record_id", sa.String(length=120), nullable=False),
        sa.Column("deal_id", sa.String(length=80), nullable=True),
        sa.Column("evidence_packet_id", sa.String(length=80), nullable=True),
        sa.Column("attachment_type", sa.String(length=120), nullable=False),
        sa.Column("filename_placeholder", sa.String(length=180), nullable=False),
        sa.Column("storage_mode", sa.String(length=80), nullable=False),
        sa.Column("sanitized_metadata", sa.JSON(), nullable=False),
        sa.Column("contains_sensitive_data", sa.Boolean(), nullable=False),
        sa.Column("source_linkage_verified", sa.Boolean(), nullable=False),
        sa.Column("source_verified", sa.Boolean(), nullable=False),
        sa.Column("safe_to_export", sa.Boolean(), nullable=False),
        sa.Column("upload_status", sa.String(length=80), nullable=False),
        sa.Column("operator_notes", sa.Text(), nullable=False),
        sa.Column("raw_file_path_committed", sa.Boolean(), nullable=False),
        sa.Column("blocked_reasons", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["deal_id"], ["deals.id"]),
        sa.ForeignKeyConstraint(["evidence_packet_id"], ["deal_evidence_packets.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "backup_export_records",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("backup_type", sa.String(length=120), nullable=False),
        sa.Column("backup_scope", sa.String(length=120), nullable=False),
        sa.Column("storage_target", sa.String(length=160), nullable=False),
        sa.Column("included_tables", sa.JSON(), nullable=False),
        sa.Column("excluded_fields", sa.JSON(), nullable=False),
        sa.Column("generated_metadata", sa.JSON(), nullable=False),
        sa.Column("safe_metadata", sa.JSON(), nullable=False),
        sa.Column("backup_status", sa.String(length=80), nullable=False),
        sa.Column("contains_raw_private_data", sa.Boolean(), nullable=False),
        sa.Column("safe_metadata_only", sa.Boolean(), nullable=False),
        sa.Column("file_path_placeholder", sa.String(length=200), nullable=False),
        sa.Column("restore_test_status", sa.String(length=80), nullable=False),
        sa.Column("owner_approval_status", sa.String(length=80), nullable=False),
        sa.Column("blocked_reasons", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "provider_sandbox_readiness_checks",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("provider_type", sa.String(length=80), nullable=False),
        sa.Column("provider_name", sa.String(length=120), nullable=False),
        sa.Column("mode", sa.String(length=80), nullable=False),
        sa.Column("sandbox_ready", sa.Boolean(), nullable=False),
        sa.Column("secrets_configured", sa.Boolean(), nullable=False),
        sa.Column("live_flag_enabled", sa.Boolean(), nullable=False),
        sa.Column("safety_check_required", sa.Boolean(), nullable=False),
        sa.Column("dry_run_required", sa.Boolean(), nullable=False),
        sa.Column("owner_approval_required", sa.Boolean(), nullable=False),
        sa.Column("idempotency_required", sa.Boolean(), nullable=False),
        sa.Column("audit_trail_required", sa.Boolean(), nullable=False),
        sa.Column("provider_calls_allowed", sa.Boolean(), nullable=False),
        sa.Column("readiness_status", sa.String(length=80), nullable=False),
        sa.Column("blocked_reasons", sa.JSON(), nullable=False),
        sa.Column("last_checked_notes", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "environment_readiness_checks",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("check_name", sa.String(length=160), nullable=False),
        sa.Column("required", sa.Boolean(), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False),
        sa.Column("status", sa.String(length=80), nullable=False),
        sa.Column("detail", sa.Text(), nullable=False),
        sa.Column("remediation", sa.Text(), nullable=False),
        sa.Column("blocked_reasons", sa.JSON(), nullable=False),
        sa.Column("prevents_production", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "deployment_hardening_checks",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("area", sa.String(length=80), nullable=False),
        sa.Column("check_name", sa.String(length=160), nullable=False),
        sa.Column("required", sa.Boolean(), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False),
        sa.Column("status", sa.String(length=80), nullable=False),
        sa.Column("detail", sa.Text(), nullable=False),
        sa.Column("remediation", sa.Text(), nullable=False),
        sa.Column("owner_action_required", sa.Boolean(), nullable=False),
        sa.Column("blocked_reasons", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("deployment_hardening_checks")
    op.drop_table("environment_readiness_checks")
    op.drop_table("provider_sandbox_readiness_checks")
    op.drop_table("backup_export_records")
    op.drop_table("evidence_attachment_records")
    op.drop_table("audit_export_packets")
    op.drop_table("approval_ux_reviews")
