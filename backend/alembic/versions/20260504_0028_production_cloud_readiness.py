"""production cloud readiness

Revision ID: 20260504_0028
Revises: 20260504_0027
Create Date: 2026-05-04 00:28:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    CloudBackupReadinessRecord,
    CloudDeploymentProfile,
    CloudEnvironmentCheck,
    CloudMonitoringSnapshot,
)


revision = "20260504_0028"
down_revision = "20260504_0027"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    CloudDeploymentProfile.__table__.create(bind=bind, checkfirst=True)
    CloudEnvironmentCheck.__table__.create(bind=bind, checkfirst=True)
    CloudBackupReadinessRecord.__table__.create(bind=bind, checkfirst=True)
    CloudMonitoringSnapshot.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    CloudMonitoringSnapshot.__table__.drop(bind=bind, checkfirst=True)
    CloudBackupReadinessRecord.__table__.drop(bind=bind, checkfirst=True)
    CloudEnvironmentCheck.__table__.drop(bind=bind, checkfirst=True)
    CloudDeploymentProfile.__table__.drop(bind=bind, checkfirst=True)
