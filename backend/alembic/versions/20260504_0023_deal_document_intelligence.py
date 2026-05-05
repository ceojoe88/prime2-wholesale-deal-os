"""deal document intelligence

Revision ID: 20260504_0023
Revises: 20260504_0022
Create Date: 2026-05-04 00:23:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    DocumentClassificationResult,
    DocumentEvidenceLink,
    DocumentExtractedFields,
    DocumentIntelligenceFile,
    DocumentIssueFlag,
    DocumentReviewTask,
)


revision = "20260504_0023"
down_revision = "20260504_0022"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    DocumentIntelligenceFile.__table__.create(bind=bind, checkfirst=True)
    DocumentClassificationResult.__table__.create(bind=bind, checkfirst=True)
    DocumentExtractedFields.__table__.create(bind=bind, checkfirst=True)
    DocumentIssueFlag.__table__.create(bind=bind, checkfirst=True)
    DocumentReviewTask.__table__.create(bind=bind, checkfirst=True)
    DocumentEvidenceLink.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    DocumentEvidenceLink.__table__.drop(bind=bind, checkfirst=True)
    DocumentReviewTask.__table__.drop(bind=bind, checkfirst=True)
    DocumentIssueFlag.__table__.drop(bind=bind, checkfirst=True)
    DocumentExtractedFields.__table__.drop(bind=bind, checkfirst=True)
    DocumentClassificationResult.__table__.drop(bind=bind, checkfirst=True)
    DocumentIntelligenceFile.__table__.drop(bind=bind, checkfirst=True)
