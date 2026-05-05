"""call intelligence layer

Revision ID: 20260504_0022
Revises: 20260504_0021
Create Date: 2026-05-04 00:22:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    CallFollowUpRecommendation,
    CallIntelligenceSession,
    CallObjectionRecord,
    CallTranscriptInput,
    SellerSignalExtraction,
)


revision = "20260504_0022"
down_revision = "20260504_0021"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    CallIntelligenceSession.__table__.create(bind=bind, checkfirst=True)
    CallTranscriptInput.__table__.create(bind=bind, checkfirst=True)
    SellerSignalExtraction.__table__.create(bind=bind, checkfirst=True)
    CallObjectionRecord.__table__.create(bind=bind, checkfirst=True)
    CallFollowUpRecommendation.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    CallFollowUpRecommendation.__table__.drop(bind=bind, checkfirst=True)
    CallObjectionRecord.__table__.drop(bind=bind, checkfirst=True)
    SellerSignalExtraction.__table__.drop(bind=bind, checkfirst=True)
    CallTranscriptInput.__table__.drop(bind=bind, checkfirst=True)
    CallIntelligenceSession.__table__.drop(bind=bind, checkfirst=True)

