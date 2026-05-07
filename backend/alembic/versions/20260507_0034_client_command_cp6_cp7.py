"""client command compliance gate and weekly reports

Revision ID: 20260507_0034
Revises: 20260507_0033
Create Date: 2026-05-07 18:30:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    ClientCommunicationApprovalGate,
    ClientComplianceDivisionEvent,
    ClientComplianceReadinessPlaceholder,
    ClientContactConsentRecord,
    ClientContactOptOutRecord,
    ClientMessageRiskReview,
    ClientSafeContactStatus,
    ClientWeeklyBottleneck,
    ClientWeeklyCommandReport,
    ClientWeeklyDivisionSummary,
    ClientWeeklyLeadStatusRollup,
    ClientWeeklyRecommendedAction,
    ClientWeeklyReportEvent,
    ClientWeeklyReportMetricSnapshot,
)


revision = "20260507_0034"
down_revision = "20260507_0033"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    ClientContactConsentRecord.__table__.create(bind=bind, checkfirst=True)
    ClientContactOptOutRecord.__table__.create(bind=bind, checkfirst=True)
    ClientSafeContactStatus.__table__.create(bind=bind, checkfirst=True)
    ClientMessageRiskReview.__table__.create(bind=bind, checkfirst=True)
    ClientCommunicationApprovalGate.__table__.create(bind=bind, checkfirst=True)
    ClientComplianceReadinessPlaceholder.__table__.create(bind=bind, checkfirst=True)
    ClientComplianceDivisionEvent.__table__.create(bind=bind, checkfirst=True)
    ClientWeeklyCommandReport.__table__.create(bind=bind, checkfirst=True)
    ClientWeeklyReportMetricSnapshot.__table__.create(bind=bind, checkfirst=True)
    ClientWeeklyLeadStatusRollup.__table__.create(bind=bind, checkfirst=True)
    ClientWeeklyBottleneck.__table__.create(bind=bind, checkfirst=True)
    ClientWeeklyRecommendedAction.__table__.create(bind=bind, checkfirst=True)
    ClientWeeklyDivisionSummary.__table__.create(bind=bind, checkfirst=True)
    ClientWeeklyReportEvent.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    ClientWeeklyReportEvent.__table__.drop(bind=bind, checkfirst=True)
    ClientWeeklyDivisionSummary.__table__.drop(bind=bind, checkfirst=True)
    ClientWeeklyRecommendedAction.__table__.drop(bind=bind, checkfirst=True)
    ClientWeeklyBottleneck.__table__.drop(bind=bind, checkfirst=True)
    ClientWeeklyLeadStatusRollup.__table__.drop(bind=bind, checkfirst=True)
    ClientWeeklyReportMetricSnapshot.__table__.drop(bind=bind, checkfirst=True)
    ClientWeeklyCommandReport.__table__.drop(bind=bind, checkfirst=True)
    ClientComplianceDivisionEvent.__table__.drop(bind=bind, checkfirst=True)
    ClientComplianceReadinessPlaceholder.__table__.drop(bind=bind, checkfirst=True)
    ClientCommunicationApprovalGate.__table__.drop(bind=bind, checkfirst=True)
    ClientMessageRiskReview.__table__.drop(bind=bind, checkfirst=True)
    ClientSafeContactStatus.__table__.drop(bind=bind, checkfirst=True)
    ClientContactOptOutRecord.__table__.drop(bind=bind, checkfirst=True)
    ClientContactConsentRecord.__table__.drop(bind=bind, checkfirst=True)
