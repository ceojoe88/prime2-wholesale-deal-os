"""controlled live provider activation

Revision ID: 20260504_0029
Revises: 20260504_0028
Create Date: 2026-05-04 00:29:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    LiveProviderActivation,
    LiveProviderActivationAttempt,
    LiveProviderAuditEvent,
    LiveProviderBlockedAttempt,
)


revision = "20260504_0029"
down_revision = "20260504_0028"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    LiveProviderActivation.__table__.create(bind=bind, checkfirst=True)
    LiveProviderActivationAttempt.__table__.create(bind=bind, checkfirst=True)
    LiveProviderBlockedAttempt.__table__.create(bind=bind, checkfirst=True)
    LiveProviderAuditEvent.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    LiveProviderAuditEvent.__table__.drop(bind=bind, checkfirst=True)
    LiveProviderBlockedAttempt.__table__.drop(bind=bind, checkfirst=True)
    LiveProviderActivationAttempt.__table__.drop(bind=bind, checkfirst=True)
    LiveProviderActivation.__table__.drop(bind=bind, checkfirst=True)
