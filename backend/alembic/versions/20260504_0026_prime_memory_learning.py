"""prime memory learning

Revision ID: 20260504_0026
Revises: 20260504_0025
Create Date: 2026-05-04 00:26:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    LearningSignal,
    PlaybookRecommendation,
    PrimeMemoryItem,
    ScoringWeightRecommendation,
)


revision = "20260504_0026"
down_revision = "20260504_0025"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    PrimeMemoryItem.__table__.create(bind=bind, checkfirst=True)
    LearningSignal.__table__.create(bind=bind, checkfirst=True)
    ScoringWeightRecommendation.__table__.create(bind=bind, checkfirst=True)
    PlaybookRecommendation.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    PlaybookRecommendation.__table__.drop(bind=bind, checkfirst=True)
    ScoringWeightRecommendation.__table__.drop(bind=bind, checkfirst=True)
    LearningSignal.__table__.drop(bind=bind, checkfirst=True)
    PrimeMemoryItem.__table__.drop(bind=bind, checkfirst=True)
