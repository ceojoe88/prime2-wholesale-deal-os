"""controlled live communication gate

Revision ID: 20260504_0005
Revises: 20260504_0004
Create Date: 2026-05-04 17:00:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    CommunicationApproval,
    CommunicationDraft,
    CommunicationDryRunReceipt,
    CommunicationSendAttempt,
)

revision = "20260504_0005"
down_revision = "20260504_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    CommunicationDraft.__table__.create(bind=bind, checkfirst=True)
    CommunicationDryRunReceipt.__table__.create(bind=bind, checkfirst=True)
    CommunicationApproval.__table__.create(bind=bind, checkfirst=True)
    CommunicationSendAttempt.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    CommunicationSendAttempt.__table__.drop(bind=bind, checkfirst=True)
    CommunicationApproval.__table__.drop(bind=bind, checkfirst=True)
    CommunicationDryRunReceipt.__table__.drop(bind=bind, checkfirst=True)
    CommunicationDraft.__table__.drop(bind=bind, checkfirst=True)
