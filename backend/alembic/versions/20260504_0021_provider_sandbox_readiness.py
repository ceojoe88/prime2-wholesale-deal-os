"""provider sandbox readiness gate

Revision ID: 20260504_0021
Revises: 20260504_0020
Create Date: 2026-05-04 00:21:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import ProviderAttemptAudit, ProviderRegistry, ProviderWebhookEvent


revision = "20260504_0021"
down_revision = "20260504_0020"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    ProviderRegistry.__table__.create(bind=bind, checkfirst=True)
    ProviderAttemptAudit.__table__.create(bind=bind, checkfirst=True)
    ProviderWebhookEvent.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    ProviderWebhookEvent.__table__.drop(bind=bind, checkfirst=True)
    ProviderAttemptAudit.__table__.drop(bind=bind, checkfirst=True)
    ProviderRegistry.__table__.drop(bind=bind, checkfirst=True)

