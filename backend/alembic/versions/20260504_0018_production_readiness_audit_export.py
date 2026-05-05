"""production readiness audit export

Revision ID: 20260504_0018
Revises: 20260504_0017
Create Date: 2026-05-04 00:18:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    ApprovalUxReview,
    AuditExportPacket,
    BackupExportRecord,
    DeploymentHardeningCheck,
    EnvironmentReadinessCheck,
    EvidenceAttachmentRecord,
    ProviderSandboxReadinessCheck,
)


revision = "20260504_0018"
down_revision = "20260504_0017"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    ApprovalUxReview.__table__.create(bind=bind, checkfirst=True)
    AuditExportPacket.__table__.create(bind=bind, checkfirst=True)
    EvidenceAttachmentRecord.__table__.create(bind=bind, checkfirst=True)
    BackupExportRecord.__table__.create(bind=bind, checkfirst=True)
    ProviderSandboxReadinessCheck.__table__.create(bind=bind, checkfirst=True)
    EnvironmentReadinessCheck.__table__.create(bind=bind, checkfirst=True)
    DeploymentHardeningCheck.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    DeploymentHardeningCheck.__table__.drop(bind=bind, checkfirst=True)
    EnvironmentReadinessCheck.__table__.drop(bind=bind, checkfirst=True)
    ProviderSandboxReadinessCheck.__table__.drop(bind=bind, checkfirst=True)
    BackupExportRecord.__table__.drop(bind=bind, checkfirst=True)
    EvidenceAttachmentRecord.__table__.drop(bind=bind, checkfirst=True)
    AuditExportPacket.__table__.drop(bind=bind, checkfirst=True)
    ApprovalUxReview.__table__.drop(bind=bind, checkfirst=True)
