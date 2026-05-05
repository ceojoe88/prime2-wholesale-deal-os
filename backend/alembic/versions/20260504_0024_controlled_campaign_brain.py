"""controlled campaign brain

Revision ID: 20260504_0024
Revises: 20260504_0023
Create Date: 2026-05-04 00:24:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    CampaignActivationAttempt,
    CampaignAudiencePreview,
    CampaignPerformanceRecord,
    CampaignRuleRecord,
    CampaignSequenceStep,
    CampaignStopEvent,
)


revision = "20260504_0024"
down_revision = "20260504_0023"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    CampaignRuleRecord.__table__.create(bind=bind, checkfirst=True)
    CampaignAudiencePreview.__table__.create(bind=bind, checkfirst=True)
    CampaignSequenceStep.__table__.create(bind=bind, checkfirst=True)
    CampaignActivationAttempt.__table__.create(bind=bind, checkfirst=True)
    CampaignStopEvent.__table__.create(bind=bind, checkfirst=True)
    CampaignPerformanceRecord.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    CampaignPerformanceRecord.__table__.drop(bind=bind, checkfirst=True)
    CampaignStopEvent.__table__.drop(bind=bind, checkfirst=True)
    CampaignActivationAttempt.__table__.drop(bind=bind, checkfirst=True)
    CampaignSequenceStep.__table__.drop(bind=bind, checkfirst=True)
    CampaignAudiencePreview.__table__.drop(bind=bind, checkfirst=True)
    CampaignRuleRecord.__table__.drop(bind=bind, checkfirst=True)
