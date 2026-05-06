"""mobile operator mode

Revision ID: 20260504_0027
Revises: 20260504_0026
Create Date: 2026-05-04 00:27:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import MobileApprovalAttempt, MobileOfflineDraft, MobileOperatorNote


revision = "20260504_0027"
down_revision = "20260504_0026"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    MobileOperatorNote.__table__.create(bind=bind, checkfirst=True)
    MobileOfflineDraft.__table__.create(bind=bind, checkfirst=True)
    MobileApprovalAttempt.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    MobileApprovalAttempt.__table__.drop(bind=bind, checkfirst=True)
    MobileOfflineDraft.__table__.drop(bind=bind, checkfirst=True)
    MobileOperatorNote.__table__.drop(bind=bind, checkfirst=True)
