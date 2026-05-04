"""unified deal room closing coordination gate

Revision ID: 20260504_0007
Revises: 20260504_0006
Create Date: 2026-05-04 19:00:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import ClosingCoordinationChecklist, DealRoomBlocker, UnifiedDealRoom

revision = "20260504_0007"
down_revision = "20260504_0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    UnifiedDealRoom.__table__.create(bind=bind, checkfirst=True)
    ClosingCoordinationChecklist.__table__.create(bind=bind, checkfirst=True)
    DealRoomBlocker.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    DealRoomBlocker.__table__.drop(bind=bind, checkfirst=True)
    ClosingCoordinationChecklist.__table__.drop(bind=bind, checkfirst=True)
    UnifiedDealRoom.__table__.drop(bind=bind, checkfirst=True)
