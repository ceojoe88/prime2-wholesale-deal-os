"""real lead import field testing

Revision ID: 20260504_0019
Revises: 20260504_0018
Create Date: 2026-05-04 00:19:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    FieldCallOutcome,
    LeadImportBatch,
    LeadImportRow,
    LeadQualityReview,
    PredictionFeedbackRecord,
    ScoringAdjustmentSuggestion,
)


revision = "20260504_0019"
down_revision = "20260504_0018"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    LeadImportBatch.__table__.create(bind=bind, checkfirst=True)
    LeadImportRow.__table__.create(bind=bind, checkfirst=True)
    LeadQualityReview.__table__.create(bind=bind, checkfirst=True)
    FieldCallOutcome.__table__.create(bind=bind, checkfirst=True)
    PredictionFeedbackRecord.__table__.create(bind=bind, checkfirst=True)
    ScoringAdjustmentSuggestion.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    ScoringAdjustmentSuggestion.__table__.drop(bind=bind, checkfirst=True)
    PredictionFeedbackRecord.__table__.drop(bind=bind, checkfirst=True)
    FieldCallOutcome.__table__.drop(bind=bind, checkfirst=True)
    LeadQualityReview.__table__.drop(bind=bind, checkfirst=True)
    LeadImportRow.__table__.drop(bind=bind, checkfirst=True)
    LeadImportBatch.__table__.drop(bind=bind, checkfirst=True)
