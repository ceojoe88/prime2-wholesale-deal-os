"""controlled auto execution gate

Revision ID: 20260504_0013
Revises: 20260504_0012
Create Date: 2026-05-04 23:45:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    ApprovedTemplate,
    AutoExecutionAttempt,
    AutoExecutionAuditRecord,
    AutoExecutionDryRun,
    AutoExecutionRule,
)

revision = "20260504_0013"
down_revision = "20260504_0012"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    ApprovedTemplate.__table__.create(bind=bind, checkfirst=True)
    AutoExecutionRule.__table__.create(bind=bind, checkfirst=True)
    AutoExecutionDryRun.__table__.create(bind=bind, checkfirst=True)
    AutoExecutionAttempt.__table__.create(bind=bind, checkfirst=True)
    AutoExecutionAuditRecord.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    AutoExecutionAuditRecord.__table__.drop(bind=bind, checkfirst=True)
    AutoExecutionAttempt.__table__.drop(bind=bind, checkfirst=True)
    AutoExecutionDryRun.__table__.drop(bind=bind, checkfirst=True)
    AutoExecutionRule.__table__.drop(bind=bind, checkfirst=True)
    ApprovedTemplate.__table__.drop(bind=bind, checkfirst=True)
