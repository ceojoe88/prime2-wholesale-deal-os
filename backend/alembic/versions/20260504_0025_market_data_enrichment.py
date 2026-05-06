"""market data enrichment

Revision ID: 20260504_0025
Revises: 20260504_0024
Create Date: 2026-05-04 00:25:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    BuyerActivitySnapshot,
    ComparableSaleRecord,
    LeadSourceROIRecord,
    MarketProfile,
    RentEstimateRecord,
)


revision = "20260504_0025"
down_revision = "20260504_0024"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    MarketProfile.__table__.create(bind=bind, checkfirst=True)
    ComparableSaleRecord.__table__.create(bind=bind, checkfirst=True)
    RentEstimateRecord.__table__.create(bind=bind, checkfirst=True)
    BuyerActivitySnapshot.__table__.create(bind=bind, checkfirst=True)
    LeadSourceROIRecord.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    LeadSourceROIRecord.__table__.drop(bind=bind, checkfirst=True)
    BuyerActivitySnapshot.__table__.drop(bind=bind, checkfirst=True)
    RentEstimateRecord.__table__.drop(bind=bind, checkfirst=True)
    ComparableSaleRecord.__table__.drop(bind=bind, checkfirst=True)
    MarketProfile.__table__.drop(bind=bind, checkfirst=True)
