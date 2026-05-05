"""revenue forecast market scaling engine

Revision ID: 20260504_0016
Revises: 20260504_0015
Create Date: 2026-05-04 00:16:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    DealProbabilityRecord,
    LeadSpendPlan,
    MarketScalingScore,
    RevenueForecastRecord,
)


revision = "20260504_0016"
down_revision = "20260504_0015"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    RevenueForecastRecord.__table__.create(bind=bind, checkfirst=True)
    DealProbabilityRecord.__table__.create(bind=bind, checkfirst=True)
    MarketScalingScore.__table__.create(bind=bind, checkfirst=True)
    LeadSpendPlan.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    LeadSpendPlan.__table__.drop(bind=bind, checkfirst=True)
    MarketScalingScore.__table__.drop(bind=bind, checkfirst=True)
    DealProbabilityRecord.__table__.drop(bind=bind, checkfirst=True)
    RevenueForecastRecord.__table__.drop(bind=bind, checkfirst=True)
