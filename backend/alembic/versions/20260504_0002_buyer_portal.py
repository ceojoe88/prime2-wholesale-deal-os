"""buyer portal publishing and interest records

Revision ID: 20260504_0002
Revises: 20260504_0001
Create Date: 2026-05-04 14:00:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import BuyerDealPublication, BuyerInterest

revision = "20260504_0002"
down_revision = "20260504_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    BuyerDealPublication.__table__.create(bind=bind, checkfirst=True)
    BuyerInterest.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    BuyerInterest.__table__.drop(bind=bind, checkfirst=True)
    BuyerDealPublication.__table__.drop(bind=bind, checkfirst=True)
