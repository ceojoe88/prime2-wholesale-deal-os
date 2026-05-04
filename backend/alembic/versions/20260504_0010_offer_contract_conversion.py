"""offer to contract conversion gate

Revision ID: 20260504_0010
Revises: 20260504_0009
Create Date: 2026-05-04 22:00:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import ContractReadyState, NegotiationRecord, OfferPositioningRecord

revision = "20260504_0010"
down_revision = "20260504_0009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    OfferPositioningRecord.__table__.create(bind=bind, checkfirst=True)
    NegotiationRecord.__table__.create(bind=bind, checkfirst=True)
    ContractReadyState.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    ContractReadyState.__table__.drop(bind=bind, checkfirst=True)
    NegotiationRecord.__table__.drop(bind=bind, checkfirst=True)
    OfferPositioningRecord.__table__.drop(bind=bind, checkfirst=True)
