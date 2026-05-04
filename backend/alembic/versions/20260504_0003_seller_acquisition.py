"""seller acquisition follow-up gate

Revision ID: 20260504_0003
Revises: 20260504_0002
Create Date: 2026-05-04 15:00:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import OfferPacket, SellerInteraction

revision = "20260504_0003"
down_revision = "20260504_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    SellerInteraction.__table__.create(bind=bind, checkfirst=True)
    OfferPacket.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    OfferPacket.__table__.drop(bind=bind, checkfirst=True)
    SellerInteraction.__table__.drop(bind=bind, checkfirst=True)
