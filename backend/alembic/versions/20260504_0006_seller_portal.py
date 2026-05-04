"""controlled seller portal offer room

Revision ID: 20260504_0006
Revises: 20260504_0005
Create Date: 2026-05-04 18:00:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import SellerOfferPublication, SellerPortalResponse

revision = "20260504_0006"
down_revision = "20260504_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    SellerOfferPublication.__table__.create(bind=bind, checkfirst=True)
    SellerPortalResponse.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    SellerPortalResponse.__table__.drop(bind=bind, checkfirst=True)
    SellerOfferPublication.__table__.drop(bind=bind, checkfirst=True)
