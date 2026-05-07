"""client command workspace and lead intelligence

Revision ID: 20260505_0031
Revises: 20260504_0030
Create Date: 2026-05-05 00:31:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    ClientLeadDivisionEvent,
    ClientLeadIntelligenceScore,
    ClientLeadMissingDataItem,
    ClientLeadNextBestAction,
    ClientLeadProfile,
    ClientWorkspace,
    ClientWorkspaceMember,
    ClientWorkspaceRole,
)


revision = "20260505_0031"
down_revision = "20260504_0030"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    ClientWorkspace.__table__.create(bind=bind, checkfirst=True)
    ClientWorkspaceRole.__table__.create(bind=bind, checkfirst=True)
    ClientWorkspaceMember.__table__.create(bind=bind, checkfirst=True)
    ClientLeadProfile.__table__.create(bind=bind, checkfirst=True)
    ClientLeadIntelligenceScore.__table__.create(bind=bind, checkfirst=True)
    ClientLeadNextBestAction.__table__.create(bind=bind, checkfirst=True)
    ClientLeadMissingDataItem.__table__.create(bind=bind, checkfirst=True)
    ClientLeadDivisionEvent.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    ClientLeadDivisionEvent.__table__.drop(bind=bind, checkfirst=True)
    ClientLeadMissingDataItem.__table__.drop(bind=bind, checkfirst=True)
    ClientLeadNextBestAction.__table__.drop(bind=bind, checkfirst=True)
    ClientLeadIntelligenceScore.__table__.drop(bind=bind, checkfirst=True)
    ClientLeadProfile.__table__.drop(bind=bind, checkfirst=True)
    ClientWorkspaceMember.__table__.drop(bind=bind, checkfirst=True)
    ClientWorkspaceRole.__table__.drop(bind=bind, checkfirst=True)
    ClientWorkspace.__table__.drop(bind=bind, checkfirst=True)
