"""semi autonomous operator mode

Revision ID: 20260504_0017
Revises: 20260504_0016
Create Date: 2026-05-04 00:17:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    AutonomousDailyOperatingReport,
    OperatorExceptionRecord,
    OperatorModeSetting,
    OwnerApprovalItem,
    SemiAutonomousCommandLoopRun,
    SystemTrustScore,
)


revision = "20260504_0017"
down_revision = "20260504_0016"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    OperatorModeSetting.__table__.create(bind=bind, checkfirst=True)
    SemiAutonomousCommandLoopRun.__table__.create(bind=bind, checkfirst=True)
    OwnerApprovalItem.__table__.create(bind=bind, checkfirst=True)
    OperatorExceptionRecord.__table__.create(bind=bind, checkfirst=True)
    AutonomousDailyOperatingReport.__table__.create(bind=bind, checkfirst=True)
    SystemTrustScore.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    SystemTrustScore.__table__.drop(bind=bind, checkfirst=True)
    AutonomousDailyOperatingReport.__table__.drop(bind=bind, checkfirst=True)
    OperatorExceptionRecord.__table__.drop(bind=bind, checkfirst=True)
    OwnerApprovalItem.__table__.drop(bind=bind, checkfirst=True)
    SemiAutonomousCommandLoopRun.__table__.drop(bind=bind, checkfirst=True)
    OperatorModeSetting.__table__.drop(bind=bind, checkfirst=True)
