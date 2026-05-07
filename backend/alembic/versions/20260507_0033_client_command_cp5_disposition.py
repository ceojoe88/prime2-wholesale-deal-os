"""client command buyer matching and disposition readiness

Revision ID: 20260507_0033
Revises: 20260506_0032
Create Date: 2026-05-07 00:33:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    ClientBuyerBuyBox,
    ClientBuyerConfidenceScore,
    ClientBuyerDemandEvidence,
    ClientBuyerOutreachDraft,
    ClientBuyerProfile,
    ClientDealBuyerMatch,
    ClientDispositionDivisionEvent,
    ClientDispositionReadinessGate,
)


revision = "20260507_0033"
down_revision = "20260506_0032"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    ClientBuyerProfile.__table__.create(bind=bind, checkfirst=True)
    ClientBuyerBuyBox.__table__.create(bind=bind, checkfirst=True)
    ClientBuyerConfidenceScore.__table__.create(bind=bind, checkfirst=True)
    ClientDealBuyerMatch.__table__.create(bind=bind, checkfirst=True)
    ClientBuyerDemandEvidence.__table__.create(bind=bind, checkfirst=True)
    ClientDispositionReadinessGate.__table__.create(bind=bind, checkfirst=True)
    ClientBuyerOutreachDraft.__table__.create(bind=bind, checkfirst=True)
    ClientDispositionDivisionEvent.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    ClientDispositionDivisionEvent.__table__.drop(bind=bind, checkfirst=True)
    ClientBuyerOutreachDraft.__table__.drop(bind=bind, checkfirst=True)
    ClientDispositionReadinessGate.__table__.drop(bind=bind, checkfirst=True)
    ClientBuyerDemandEvidence.__table__.drop(bind=bind, checkfirst=True)
    ClientDealBuyerMatch.__table__.drop(bind=bind, checkfirst=True)
    ClientBuyerConfidenceScore.__table__.drop(bind=bind, checkfirst=True)
    ClientBuyerBuyBox.__table__.drop(bind=bind, checkfirst=True)
    ClientBuyerProfile.__table__.drop(bind=bind, checkfirst=True)
