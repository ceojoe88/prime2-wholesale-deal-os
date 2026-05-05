"""revenue forecast market scaling engine

Revision ID: 20260504_0016
Revises: 20260504_0015
Create Date: 2026-05-04 00:16:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260504_0016"
down_revision = "20260504_0015"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "revenue_forecast_records",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("forecast_period", sa.String(length=120), nullable=False),
        sa.Column("projected_assignment_fees", sa.Integer(), nullable=False),
        sa.Column("verified_assignment_fees", sa.Integer(), nullable=False),
        sa.Column("probability_adjusted_revenue", sa.Integer(), nullable=False),
        sa.Column("conservative_forecast", sa.Integer(), nullable=False),
        sa.Column("base_forecast", sa.Integer(), nullable=False),
        sa.Column("aggressive_forecast", sa.Integer(), nullable=False),
        sa.Column("deals_at_risk", sa.JSON(), nullable=False),
        sa.Column("expected_close_window", sa.String(length=120), nullable=False),
        sa.Column("confidence_level", sa.String(length=80), nullable=False),
        sa.Column("source_basis", sa.JSON(), nullable=False),
        sa.Column("estimate_label", sa.String(length=160), nullable=False),
        sa.Column("guaranteed_revenue_claim_allowed", sa.Boolean(), nullable=False),
        sa.Column("unsupported_roi_claim_allowed", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "deal_probability_records",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("deal_id", sa.String(length=80), nullable=False),
        sa.Column("seller_readiness", sa.Float(), nullable=False),
        sa.Column("buyer_demand", sa.Float(), nullable=False),
        sa.Column("underwriting_confidence", sa.Float(), nullable=False),
        sa.Column("compliance_status_score", sa.Float(), nullable=False),
        sa.Column("title_review_readiness", sa.Float(), nullable=False),
        sa.Column("blocker_severity", sa.Float(), nullable=False),
        sa.Column("buyer_pof_strength", sa.Float(), nullable=False),
        sa.Column("communication_momentum", sa.Float(), nullable=False),
        sa.Column("probability_score", sa.Float(), nullable=False),
        sa.Column("probability_band", sa.String(length=80), nullable=False),
        sa.Column("source_record_ids", sa.JSON(), nullable=False),
        sa.Column("estimate_only", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["deal_id"], ["deals.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "market_scaling_scores",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("market_zip", sa.String(length=20), nullable=False),
        sa.Column("lead_volume", sa.Integer(), nullable=False),
        sa.Column("hot_lead_percentage", sa.Float(), nullable=False),
        sa.Column("buyer_demand", sa.Float(), nullable=False),
        sa.Column("average_spread", sa.Integer(), nullable=False),
        sa.Column("conversion_rate", sa.Float(), nullable=False),
        sa.Column("title_compliance_friction", sa.Float(), nullable=False),
        sa.Column("competition_risk", sa.Float(), nullable=False),
        sa.Column("recommended_spend_level", sa.String(length=80), nullable=False),
        sa.Column("scaling_score", sa.Float(), nullable=False),
        sa.Column("source_record_ids", sa.JSON(), nullable=False),
        sa.Column("estimate_only", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "lead_spend_plans",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("target_zip_codes", sa.JSON(), nullable=False),
        sa.Column("lead_types", sa.JSON(), nullable=False),
        sa.Column("max_monthly_spend", sa.Integer(), nullable=False),
        sa.Column("expected_deal_count", sa.Float(), nullable=False),
        sa.Column("expected_assignment_fee_low", sa.Integer(), nullable=False),
        sa.Column("expected_assignment_fee_high", sa.Integer(), nullable=False),
        sa.Column("break_even_assignment_target", sa.Integer(), nullable=False),
        sa.Column("evidence_basis", sa.JSON(), nullable=False),
        sa.Column("recommendation_status", sa.String(length=80), nullable=False),
        sa.Column("unsupported_spend_recommended", sa.Boolean(), nullable=False),
        sa.Column("estimate_only", sa.Boolean(), nullable=False),
        sa.Column("owner_review_status", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("lead_spend_plans")
    op.drop_table("market_scaling_scores")
    op.drop_table("deal_probability_records")
    op.drop_table("revenue_forecast_records")
