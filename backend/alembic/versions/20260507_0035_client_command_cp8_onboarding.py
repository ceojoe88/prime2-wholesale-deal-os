"""client command onboarding wizard and activation readiness

Revision ID: 20260507_0035
Revises: 20260507_0034
Create Date: 2026-05-07 22:15:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    ClientActivationBlocker,
    ClientBuyerListSetup,
    ClientBusinessProfile,
    ClientComplianceSetupChecklist,
    ClientFirstLeadImportChecklist,
    ClientFirstWeeklyCycleReadiness,
    ClientGoLiveReadinessGate,
    ClientLeadSourceSetup,
    ClientMarketSetup,
    ClientOnboardingManagerEvent,
    ClientOnboardingReport,
    ClientOnboardingTask,
    ClientOnboardingTimelineEvent,
    ClientPipelineSetup,
    ClientPipelineStageTemplate,
    ClientStrategyProfile,
    ClientTeamSetupChecklist,
    ClientWorkspaceReadinessScore,
)


revision = "20260507_0035"
down_revision = "20260507_0034"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    ClientBusinessProfile.__table__.create(bind=bind, checkfirst=True)
    ClientStrategyProfile.__table__.create(bind=bind, checkfirst=True)
    ClientMarketSetup.__table__.create(bind=bind, checkfirst=True)
    ClientPipelineSetup.__table__.create(bind=bind, checkfirst=True)
    ClientPipelineStageTemplate.__table__.create(bind=bind, checkfirst=True)
    ClientLeadSourceSetup.__table__.create(bind=bind, checkfirst=True)
    ClientBuyerListSetup.__table__.create(bind=bind, checkfirst=True)
    ClientTeamSetupChecklist.__table__.create(bind=bind, checkfirst=True)
    ClientComplianceSetupChecklist.__table__.create(bind=bind, checkfirst=True)
    ClientFirstLeadImportChecklist.__table__.create(bind=bind, checkfirst=True)
    ClientWorkspaceReadinessScore.__table__.create(bind=bind, checkfirst=True)
    ClientActivationBlocker.__table__.create(bind=bind, checkfirst=True)
    ClientGoLiveReadinessGate.__table__.create(bind=bind, checkfirst=True)
    ClientOnboardingTask.__table__.create(bind=bind, checkfirst=True)
    ClientOnboardingTimelineEvent.__table__.create(bind=bind, checkfirst=True)
    ClientFirstWeeklyCycleReadiness.__table__.create(bind=bind, checkfirst=True)
    ClientOnboardingReport.__table__.create(bind=bind, checkfirst=True)
    ClientOnboardingManagerEvent.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    ClientOnboardingManagerEvent.__table__.drop(bind=bind, checkfirst=True)
    ClientOnboardingReport.__table__.drop(bind=bind, checkfirst=True)
    ClientFirstWeeklyCycleReadiness.__table__.drop(bind=bind, checkfirst=True)
    ClientOnboardingTimelineEvent.__table__.drop(bind=bind, checkfirst=True)
    ClientOnboardingTask.__table__.drop(bind=bind, checkfirst=True)
    ClientGoLiveReadinessGate.__table__.drop(bind=bind, checkfirst=True)
    ClientActivationBlocker.__table__.drop(bind=bind, checkfirst=True)
    ClientWorkspaceReadinessScore.__table__.drop(bind=bind, checkfirst=True)
    ClientFirstLeadImportChecklist.__table__.drop(bind=bind, checkfirst=True)
    ClientComplianceSetupChecklist.__table__.drop(bind=bind, checkfirst=True)
    ClientTeamSetupChecklist.__table__.drop(bind=bind, checkfirst=True)
    ClientBuyerListSetup.__table__.drop(bind=bind, checkfirst=True)
    ClientLeadSourceSetup.__table__.drop(bind=bind, checkfirst=True)
    ClientPipelineStageTemplate.__table__.drop(bind=bind, checkfirst=True)
    ClientPipelineSetup.__table__.drop(bind=bind, checkfirst=True)
    ClientMarketSetup.__table__.drop(bind=bind, checkfirst=True)
    ClientStrategyProfile.__table__.drop(bind=bind, checkfirst=True)
    ClientBusinessProfile.__table__.drop(bind=bind, checkfirst=True)
