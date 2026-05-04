"""buyer demand intelligence distribution prep

Revision ID: 20260504_0009
Revises: 20260504_0008
Create Date: 2026-05-04 21:00:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import BuyerDealPriority, BuyerDemandProfile, DealDistributionPrep

revision = "20260504_0009"
down_revision = "20260504_0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    BuyerDemandProfile.__table__.create(bind=bind, checkfirst=True)
    BuyerDealPriority.__table__.create(bind=bind, checkfirst=True)
    DealDistributionPrep.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    DealDistributionPrep.__table__.drop(bind=bind, checkfirst=True)
    BuyerDealPriority.__table__.drop(bind=bind, checkfirst=True)
    BuyerDemandProfile.__table__.drop(bind=bind, checkfirst=True)
