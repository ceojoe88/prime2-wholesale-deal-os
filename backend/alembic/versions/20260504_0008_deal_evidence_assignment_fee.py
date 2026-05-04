"""deal evidence assignment fee attribution

Revision ID: 20260504_0008
Revises: 20260504_0007
Create Date: 2026-05-04 20:00:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import AssignmentFeeAttribution, DealEvidencePacket

revision = "20260504_0008"
down_revision = "20260504_0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    DealEvidencePacket.__table__.create(bind=bind, checkfirst=True)
    AssignmentFeeAttribution.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    AssignmentFeeAttribution.__table__.drop(bind=bind, checkfirst=True)
    DealEvidencePacket.__table__.drop(bind=bind, checkfirst=True)
