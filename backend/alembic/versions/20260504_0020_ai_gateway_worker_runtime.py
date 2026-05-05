"""ai gateway worker runtime

Revision ID: 20260504_0020
Revises: 20260504_0019
Create Date: 2026-05-04 00:20:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    AIAuditRecord,
    AICostLedger,
    AIRequestLog,
    AITemplate,
    WorkerHeartbeat,
    WorkerJob,
    WorkerJobLog,
)


revision = "20260504_0020"
down_revision = "20260504_0019"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    AITemplate.__table__.create(bind=bind, checkfirst=True)
    AIRequestLog.__table__.create(bind=bind, checkfirst=True)
    AIAuditRecord.__table__.create(bind=bind, checkfirst=True)
    AICostLedger.__table__.create(bind=bind, checkfirst=True)
    WorkerJob.__table__.create(bind=bind, checkfirst=True)
    WorkerJobLog.__table__.create(bind=bind, checkfirst=True)
    WorkerHeartbeat.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    WorkerHeartbeat.__table__.drop(bind=bind, checkfirst=True)
    WorkerJobLog.__table__.drop(bind=bind, checkfirst=True)
    WorkerJob.__table__.drop(bind=bind, checkfirst=True)
    AICostLedger.__table__.drop(bind=bind, checkfirst=True)
    AIAuditRecord.__table__.drop(bind=bind, checkfirst=True)
    AIRequestLog.__table__.drop(bind=bind, checkfirst=True)
    AITemplate.__table__.drop(bind=bind, checkfirst=True)

