"""buyer distribution acceleration engine

Revision ID: 20260504_0014
Revises: 20260504_0013
Create Date: 2026-05-05 00:10:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    BuyerAccelerationRecord,
    BuyerResponseRoute,
    BuyerSequencePrep,
    BuyerVelocityProfile,
)

revision = "20260504_0014"
down_revision = "20260504_0013"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    BuyerAccelerationRecord.__table__.create(bind=bind, checkfirst=True)
    BuyerSequencePrep.__table__.create(bind=bind, checkfirst=True)
    BuyerResponseRoute.__table__.create(bind=bind, checkfirst=True)
    BuyerVelocityProfile.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    BuyerVelocityProfile.__table__.drop(bind=bind, checkfirst=True)
    BuyerResponseRoute.__table__.drop(bind=bind, checkfirst=True)
    BuyerSequencePrep.__table__.drop(bind=bind, checkfirst=True)
    BuyerAccelerationRecord.__table__.drop(bind=bind, checkfirst=True)
