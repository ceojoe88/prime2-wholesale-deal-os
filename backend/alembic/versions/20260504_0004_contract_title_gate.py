"""contract control title handoff gate

Revision ID: 20260504_0004
Revises: 20260504_0003
Create Date: 2026-05-04 16:00:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import AssignmentReadinessRecord, ContractControl, TitleHandoffPacket

revision = "20260504_0004"
down_revision = "20260504_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    ContractControl.__table__.create(bind=bind, checkfirst=True)
    TitleHandoffPacket.__table__.create(bind=bind, checkfirst=True)
    AssignmentReadinessRecord.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    AssignmentReadinessRecord.__table__.drop(bind=bind, checkfirst=True)
    TitleHandoffPacket.__table__.drop(bind=bind, checkfirst=True)
    ContractControl.__table__.drop(bind=bind, checkfirst=True)
