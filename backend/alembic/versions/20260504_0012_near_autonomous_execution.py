"""near autonomous execution engine

Revision ID: 20260504_0012
Revises: 20260504_0011
Create Date: 2026-05-04 23:30:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    AutomationAttempt,
    AutomationEventTrigger,
    AutomationRule,
    AutonomousAgentTask,
    AutonomyEscalation,
    DailyCommandBriefing,
    SchedulerRun,
)

revision = "20260504_0012"
down_revision = "20260504_0011"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    AutomationRule.__table__.create(bind=bind, checkfirst=True)
    SchedulerRun.__table__.create(bind=bind, checkfirst=True)
    AutomationAttempt.__table__.create(bind=bind, checkfirst=True)
    AutonomousAgentTask.__table__.create(bind=bind, checkfirst=True)
    AutomationEventTrigger.__table__.create(bind=bind, checkfirst=True)
    DailyCommandBriefing.__table__.create(bind=bind, checkfirst=True)
    AutonomyEscalation.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    AutonomyEscalation.__table__.drop(bind=bind, checkfirst=True)
    DailyCommandBriefing.__table__.drop(bind=bind, checkfirst=True)
    AutomationEventTrigger.__table__.drop(bind=bind, checkfirst=True)
    AutonomousAgentTask.__table__.drop(bind=bind, checkfirst=True)
    AutomationAttempt.__table__.drop(bind=bind, checkfirst=True)
    SchedulerRun.__table__.drop(bind=bind, checkfirst=True)
    AutomationRule.__table__.drop(bind=bind, checkfirst=True)
