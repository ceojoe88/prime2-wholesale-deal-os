"""real deal execution pack

Revision ID: 20260504_0030
Revises: 20260504_0029
Create Date: 2026-05-04 00:30:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import RealDealExecutionBatch


revision = "20260504_0030"
down_revision = "20260504_0029"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    RealDealExecutionBatch.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    RealDealExecutionBatch.__table__.drop(bind=bind, checkfirst=True)
