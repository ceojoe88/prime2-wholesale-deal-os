"""semi autonomous operator mode

Revision ID: 20260504_0017
Revises: 20260504_0016
Create Date: 2026-05-04 00:17:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260504_0017"
down_revision = "20260504_0016"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "operator_mode_settings",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("current_mode", sa.String(length=80), nullable=False),
        sa.Column("default_mode", sa.String(length=80), nullable=False),
        sa.Column("semi_autonomous_enabled", sa.Boolean(), nullable=False),
        sa.Column("owner_enabled", sa.Boolean(), nullable=False),
        sa.Column("max_autonomy_level", sa.Integer(), nullable=False),
        sa.Column("level_5_disabled", sa.Boolean(), nullable=False),
        sa.Column("high_risk_requires_approval", sa.Boolean(), nullable=False),
        sa.Column("live_actions_require_gates", sa.Boolean(), nullable=False),
        sa.Column("contract_execution_allowed", sa.Boolean(), nullable=False),
        sa.Column("title_submission_allowed", sa.Boolean(), nullable=False),
        sa.Column("bulk_campaigns_allowed", sa.Boolean(), nullable=False),
        sa.Column("payment_handling_allowed", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "semi_autonomous_command_loop_runs",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("mode_setting_id", sa.String(length=80), nullable=False),
        sa.Column("cycle_status", sa.String(length=80), nullable=False),
        sa.Column("scan_summary", sa.JSON(), nullable=False),
        sa.Column("score_summary", sa.JSON(), nullable=False),
        sa.Column("route_summary", sa.JSON(), nullable=False),
        sa.Column("prepared_items", sa.JSON(), nullable=False),
        sa.Column("gate_checks", sa.JSON(), nullable=False),
        sa.Column("escalations", sa.JSON(), nullable=False),
        sa.Column("approvals_waiting", sa.JSON(), nullable=False),
        sa.Column("outcomes_logged", sa.JSON(), nullable=False),
        sa.Column("optimized_records", sa.JSON(), nullable=False),
        sa.Column("high_risk_actions_executed", sa.Boolean(), nullable=False),
        sa.Column("contracts_executed", sa.Boolean(), nullable=False),
        sa.Column("title_submitted", sa.Boolean(), nullable=False),
        sa.Column("bulk_campaigns_sent", sa.Boolean(), nullable=False),
        sa.Column("portal_publish_without_approval", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["mode_setting_id"], ["operator_mode_settings.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "owner_approval_items",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("approval_type", sa.String(length=120), nullable=False),
        sa.Column("source_record_type", sa.String(length=120), nullable=False),
        sa.Column("source_record_id", sa.String(length=120), nullable=False),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("risk_level", sa.String(length=80), nullable=False),
        sa.Column("approval_status", sa.String(length=80), nullable=False),
        sa.Column("owner_required", sa.Boolean(), nullable=False),
        sa.Column("ready_for_approval", sa.Boolean(), nullable=False),
        sa.Column("blocked_reasons", sa.JSON(), nullable=False),
        sa.Column("action_summary", sa.Text(), nullable=False),
        sa.Column("high_risk_action", sa.Boolean(), nullable=False),
        sa.Column("executed", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "operator_exception_records",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("exception_type", sa.String(length=120), nullable=False),
        sa.Column("severity", sa.String(length=80), nullable=False),
        sa.Column("source_record_type", sa.String(length=120), nullable=False),
        sa.Column("source_record_id", sa.String(length=120), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("recommended_action", sa.Text(), nullable=False),
        sa.Column("owner_action_required", sa.Boolean(), nullable=False),
        sa.Column("status", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "autonomous_daily_operating_reports",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("report_date", sa.String(length=40), nullable=False),
        sa.Column("generated_by", sa.String(length=120), nullable=False),
        sa.Column("what_system_did", sa.JSON(), nullable=False),
        sa.Column("what_prepared", sa.JSON(), nullable=False),
        sa.Column("what_blocked", sa.JSON(), nullable=False),
        sa.Column("needs_owner_approval", sa.JSON(), nullable=False),
        sa.Column("top_money_actions", sa.JSON(), nullable=False),
        sa.Column("top_risk_actions", sa.JSON(), nullable=False),
        sa.Column("projected_assignment_fee_movement", sa.Integer(), nullable=False),
        sa.Column("recommended_focus_today", sa.JSON(), nullable=False),
        sa.Column("draft_only", sa.Boolean(), nullable=False),
        sa.Column("high_risk_actions_executed", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "system_trust_scores",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("automation_success_rate", sa.Float(), nullable=False),
        sa.Column("blocked_unsafe_actions", sa.Integer(), nullable=False),
        sa.Column("approval_queue_age_hours", sa.Float(), nullable=False),
        sa.Column("stale_tasks", sa.Integer(), nullable=False),
        sa.Column("scoring_confidence", sa.Float(), nullable=False),
        sa.Column("forecast_confidence", sa.Float(), nullable=False),
        sa.Column("buyer_response_velocity", sa.Float(), nullable=False),
        sa.Column("seller_conversion_velocity", sa.Float(), nullable=False),
        sa.Column("overall_trust_score", sa.Float(), nullable=False),
        sa.Column("trust_status", sa.String(length=80), nullable=False),
        sa.Column("source_record_ids", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("system_trust_scores")
    op.drop_table("autonomous_daily_operating_reports")
    op.drop_table("operator_exception_records")
    op.drop_table("owner_approval_items")
    op.drop_table("semi_autonomous_command_loop_runs")
    op.drop_table("operator_mode_settings")
