"""title attorney review coordination gate

Revision ID: 20260504_0011
Revises: 20260504_0010
Create Date: 2026-05-04 23:00:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import ReviewPacketPrep, TitleReviewCoordination

revision = "20260504_0011"
down_revision = "20260504_0010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    TitleReviewCoordination.__table__.create(bind=bind, checkfirst=True)
    ReviewPacketPrep.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    ReviewPacketPrep.__table__.drop(bind=bind, checkfirst=True)
    TitleReviewCoordination.__table__.drop(bind=bind, checkfirst=True)
