"""client command acquisition and underwriting layers

Revision ID: 20260506_0032
Revises: 20260505_0031
Create Date: 2026-05-06 00:32:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    ClientAcquisitionBrief,
    ClientAcquisitionDivisionEvent,
    ClientAppointmentReadinessReview,
    ClientDealEvidenceItem,
    ClientDealEvidencePacket,
    ClientFollowUpDraft,
    ClientObjectionResponseDraft,
    ClientOfferReadinessGate,
    ClientOfferScenario,
    ClientSellerQuestion,
    ClientSellerQuestionPlan,
    ClientUnderwritingDivisionEvent,
    ClientUnderwritingReview,
)


revision = "20260506_0032"
down_revision = "20260505_0031"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    ClientAcquisitionBrief.__table__.create(bind=bind, checkfirst=True)
    ClientSellerQuestionPlan.__table__.create(bind=bind, checkfirst=True)
    ClientSellerQuestion.__table__.create(bind=bind, checkfirst=True)
    ClientObjectionResponseDraft.__table__.create(bind=bind, checkfirst=True)
    ClientFollowUpDraft.__table__.create(bind=bind, checkfirst=True)
    ClientAppointmentReadinessReview.__table__.create(bind=bind, checkfirst=True)
    ClientAcquisitionDivisionEvent.__table__.create(bind=bind, checkfirst=True)
    ClientDealEvidencePacket.__table__.create(bind=bind, checkfirst=True)
    ClientDealEvidenceItem.__table__.create(bind=bind, checkfirst=True)
    ClientUnderwritingReview.__table__.create(bind=bind, checkfirst=True)
    ClientOfferScenario.__table__.create(bind=bind, checkfirst=True)
    ClientOfferReadinessGate.__table__.create(bind=bind, checkfirst=True)
    ClientUnderwritingDivisionEvent.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    ClientUnderwritingDivisionEvent.__table__.drop(bind=bind, checkfirst=True)
    ClientOfferReadinessGate.__table__.drop(bind=bind, checkfirst=True)
    ClientOfferScenario.__table__.drop(bind=bind, checkfirst=True)
    ClientUnderwritingReview.__table__.drop(bind=bind, checkfirst=True)
    ClientDealEvidenceItem.__table__.drop(bind=bind, checkfirst=True)
    ClientDealEvidencePacket.__table__.drop(bind=bind, checkfirst=True)
    ClientAcquisitionDivisionEvent.__table__.drop(bind=bind, checkfirst=True)
    ClientAppointmentReadinessReview.__table__.drop(bind=bind, checkfirst=True)
    ClientFollowUpDraft.__table__.drop(bind=bind, checkfirst=True)
    ClientObjectionResponseDraft.__table__.drop(bind=bind, checkfirst=True)
    ClientSellerQuestion.__table__.drop(bind=bind, checkfirst=True)
    ClientSellerQuestionPlan.__table__.drop(bind=bind, checkfirst=True)
    ClientAcquisitionBrief.__table__.drop(bind=bind, checkfirst=True)
