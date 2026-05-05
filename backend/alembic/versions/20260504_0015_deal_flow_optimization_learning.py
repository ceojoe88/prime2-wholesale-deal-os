"""deal flow optimization learning engine

Revision ID: 20260504_0015
Revises: 20260504_0014
Create Date: 2026-05-04 00:15:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260504_0015"
down_revision = "20260504_0014"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "outcome_learning_records",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("deal_id", sa.String(length=80), nullable=True),
        sa.Column("lead_source", sa.String(length=120), nullable=False),
        sa.Column("market", sa.String(length=120), nullable=False),
        sa.Column("seller_type", sa.String(length=120), nullable=False),
        sa.Column("buyer_type", sa.String(length=120), nullable=False),
        sa.Column("offer_strategy", sa.String(length=120), nullable=False),
        sa.Column("follow_up_type", sa.String(length=120), nullable=False),
        sa.Column("conversion_result", sa.String(length=120), nullable=False),
        sa.Column("projected_assignment_fee", sa.Integer(), nullable=False),
        sa.Column("verified_assignment_fee", sa.Integer(), nullable=False),
        sa.Column("time_to_contract_ready_days", sa.Integer(), nullable=True),
        sa.Column("blockers", sa.JSON(), nullable=False),
        sa.Column("lost_reason", sa.Text(), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("source_evidence_ids", sa.JSON(), nullable=False),
        sa.Column("source_records_present", sa.Boolean(), nullable=False),
        sa.Column("evidence_status", sa.String(length=80), nullable=False),
        sa.Column("unsupported_revenue_claim", sa.Boolean(), nullable=False),
        sa.Column("unsupported_roi_claim", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["deal_id"], ["deals.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "optimization_recommendations",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("recommendation_type", sa.String(length=120), nullable=False),
        sa.Column("target", sa.String(length=160), nullable=False),
        sa.Column("recommendation", sa.Text(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("source_record_ids", sa.JSON(), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("impact_score", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=80), nullable=False),
        sa.Column("owner_review_status", sa.String(length=80), nullable=False),
        sa.Column("guaranteed_revenue_claim_allowed", sa.Boolean(), nullable=False),
        sa.Column("unsupported_roi_claim_allowed", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "agent_performance_scores",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("division_name", sa.String(length=160), nullable=False),
        sa.Column("agent_group", sa.String(length=160), nullable=False),
        sa.Column("quality_score", sa.Float(), nullable=False),
        sa.Column("conversion_score", sa.Float(), nullable=False),
        sa.Column("accuracy_score", sa.Float(), nullable=False),
        sa.Column("effectiveness_score", sa.Float(), nullable=False),
        sa.Column("compliance_block_rate", sa.Float(), nullable=False),
        sa.Column("follow_up_score", sa.Float(), nullable=False),
        sa.Column("recommendation_accuracy", sa.Float(), nullable=False),
        sa.Column("overall_score", sa.Float(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("source_record_ids", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "scoring_weight_changes",
        sa.Column("id", sa.String(length=80), nullable=False),
        sa.Column("source_record_id", sa.String(length=120), nullable=False),
        sa.Column("weight_group", sa.String(length=120), nullable=False),
        sa.Column("previous_weight", sa.Float(), nullable=False),
        sa.Column("new_weight", sa.Float(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("logged_by", sa.String(length=120), nullable=False),
        sa.Column("owner_review_status", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("scoring_weight_changes")
    op.drop_table("agent_performance_scores")
    op.drop_table("optimization_recommendations")
    op.drop_table("outcome_learning_records")
