"""deal flow optimization learning engine

Revision ID: 20260504_0015
Revises: 20260504_0014
Create Date: 2026-05-04 00:15:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    AgentPerformanceScore,
    OptimizationRecommendation,
    OutcomeLearningRecord,
    ScoringWeightChange,
)


revision = "20260504_0015"
down_revision = "20260504_0014"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    OutcomeLearningRecord.__table__.create(bind=bind, checkfirst=True)
    OptimizationRecommendation.__table__.create(bind=bind, checkfirst=True)
    AgentPerformanceScore.__table__.create(bind=bind, checkfirst=True)
    ScoringWeightChange.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    ScoringWeightChange.__table__.drop(bind=bind, checkfirst=True)
    AgentPerformanceScore.__table__.drop(bind=bind, checkfirst=True)
    OptimizationRecommendation.__table__.drop(bind=bind, checkfirst=True)
    OutcomeLearningRecord.__table__.drop(bind=bind, checkfirst=True)
