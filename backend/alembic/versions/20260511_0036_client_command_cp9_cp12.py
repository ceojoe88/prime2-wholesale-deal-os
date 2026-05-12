"""client command cp9 cp10 cp11 cp12

Revision ID: 20260511_0036
Revises: 20260507_0035
Create Date: 2026-05-11 22:05:00.000000
"""

from __future__ import annotations

from alembic import op

from app.models import (
    ClientBillingApproval,
    ClientBillingAttempt,
    ClientBillingCustomerProfile,
    ClientBillingExternalReference,
    ClientBillingGateEvent,
    ClientBillingLedgerEntry,
    ClientBillingLiveFlag,
    ClientBillingProviderProfile,
    ClientBillingReadinessCheck,
    ClientBillingReadinessRecord,
    ClientBillingWebhookEventPlaceholder,
    ClientCheckoutDryRunReceipt,
    ClientCommunicationDryRunReceipt,
    ClientCommunicationExternalMessageReference,
    ClientCommunicationGateEvent,
    ClientCommunicationIdempotencyRecord,
    ClientCommunicationLiveFlag,
    ClientCommunicationLiveReadinessCheck,
    ClientCommunicationProviderProfile,
    ClientCommunicationSendApproval,
    ClientCommunicationSendAttempt,
    ClientFeatureGateEvaluation,
    ClientPilotAdminNote,
    ClientPilotClientSafeUpdate,
    ClientPilotEscalation,
    ClientPilotEvent,
    ClientPilotHealthSnapshot,
    ClientPilotLaunchChecklist,
    ClientPilotOperatingMode,
    ClientPilotOutcomeCheckpoint,
    ClientPilotProgram,
    ClientPilotRiskReview,
    ClientPilotSupportAction,
    ClientPilotSupportTicket,
    ClientPilotWorkspaceEnrollment,
    ClientPlanCatalog,
    ClientPlanFeature,
    ClientPlanGateEvent,
    ClientPlanLimit,
    ClientPlanUpgradeRecommendation,
    ClientSeatUsageRecord,
    ClientSubscriptionPlaceholder,
    ClientUsageCounter,
    ClientWorkspacePlanAssignment,
)


revision = "20260511_0036"
down_revision = "20260507_0035"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    ClientPlanCatalog.__table__.create(bind=bind, checkfirst=True)
    ClientPlanFeature.__table__.create(bind=bind, checkfirst=True)
    ClientPlanLimit.__table__.create(bind=bind, checkfirst=True)
    ClientWorkspacePlanAssignment.__table__.create(bind=bind, checkfirst=True)
    ClientFeatureGateEvaluation.__table__.create(bind=bind, checkfirst=True)
    ClientUsageCounter.__table__.create(bind=bind, checkfirst=True)
    ClientSeatUsageRecord.__table__.create(bind=bind, checkfirst=True)
    ClientPlanUpgradeRecommendation.__table__.create(bind=bind, checkfirst=True)
    ClientBillingReadinessRecord.__table__.create(bind=bind, checkfirst=True)
    ClientSubscriptionPlaceholder.__table__.create(bind=bind, checkfirst=True)
    ClientPlanGateEvent.__table__.create(bind=bind, checkfirst=True)
    ClientCommunicationProviderProfile.__table__.create(bind=bind, checkfirst=True)
    ClientCommunicationLiveReadinessCheck.__table__.create(bind=bind, checkfirst=True)
    ClientCommunicationDryRunReceipt.__table__.create(bind=bind, checkfirst=True)
    ClientCommunicationSendApproval.__table__.create(bind=bind, checkfirst=True)
    ClientCommunicationSendAttempt.__table__.create(bind=bind, checkfirst=True)
    ClientCommunicationExternalMessageReference.__table__.create(bind=bind, checkfirst=True)
    ClientCommunicationIdempotencyRecord.__table__.create(bind=bind, checkfirst=True)
    ClientCommunicationLiveFlag.__table__.create(bind=bind, checkfirst=True)
    ClientCommunicationGateEvent.__table__.create(bind=bind, checkfirst=True)
    ClientBillingProviderProfile.__table__.create(bind=bind, checkfirst=True)
    ClientBillingLiveFlag.__table__.create(bind=bind, checkfirst=True)
    ClientBillingCustomerProfile.__table__.create(bind=bind, checkfirst=True)
    ClientBillingReadinessCheck.__table__.create(bind=bind, checkfirst=True)
    ClientCheckoutDryRunReceipt.__table__.create(bind=bind, checkfirst=True)
    ClientBillingApproval.__table__.create(bind=bind, checkfirst=True)
    ClientBillingAttempt.__table__.create(bind=bind, checkfirst=True)
    ClientBillingExternalReference.__table__.create(bind=bind, checkfirst=True)
    ClientBillingWebhookEventPlaceholder.__table__.create(bind=bind, checkfirst=True)
    ClientBillingLedgerEntry.__table__.create(bind=bind, checkfirst=True)
    ClientBillingGateEvent.__table__.create(bind=bind, checkfirst=True)
    ClientPilotProgram.__table__.create(bind=bind, checkfirst=True)
    ClientPilotWorkspaceEnrollment.__table__.create(bind=bind, checkfirst=True)
    ClientPilotOperatingMode.__table__.create(bind=bind, checkfirst=True)
    ClientPilotHealthSnapshot.__table__.create(bind=bind, checkfirst=True)
    ClientPilotSupportTicket.__table__.create(bind=bind, checkfirst=True)
    ClientPilotSupportAction.__table__.create(bind=bind, checkfirst=True)
    ClientPilotEscalation.__table__.create(bind=bind, checkfirst=True)
    ClientPilotAdminNote.__table__.create(bind=bind, checkfirst=True)
    ClientPilotClientSafeUpdate.__table__.create(bind=bind, checkfirst=True)
    ClientPilotLaunchChecklist.__table__.create(bind=bind, checkfirst=True)
    ClientPilotRiskReview.__table__.create(bind=bind, checkfirst=True)
    ClientPilotOutcomeCheckpoint.__table__.create(bind=bind, checkfirst=True)
    ClientPilotEvent.__table__.create(bind=bind, checkfirst=True)


def downgrade() -> None:
    bind = op.get_bind()
    ClientPilotEvent.__table__.drop(bind=bind, checkfirst=True)
    ClientPilotOutcomeCheckpoint.__table__.drop(bind=bind, checkfirst=True)
    ClientPilotRiskReview.__table__.drop(bind=bind, checkfirst=True)
    ClientPilotLaunchChecklist.__table__.drop(bind=bind, checkfirst=True)
    ClientPilotClientSafeUpdate.__table__.drop(bind=bind, checkfirst=True)
    ClientPilotAdminNote.__table__.drop(bind=bind, checkfirst=True)
    ClientPilotEscalation.__table__.drop(bind=bind, checkfirst=True)
    ClientPilotSupportAction.__table__.drop(bind=bind, checkfirst=True)
    ClientPilotSupportTicket.__table__.drop(bind=bind, checkfirst=True)
    ClientPilotHealthSnapshot.__table__.drop(bind=bind, checkfirst=True)
    ClientPilotOperatingMode.__table__.drop(bind=bind, checkfirst=True)
    ClientPilotWorkspaceEnrollment.__table__.drop(bind=bind, checkfirst=True)
    ClientPilotProgram.__table__.drop(bind=bind, checkfirst=True)
    ClientBillingGateEvent.__table__.drop(bind=bind, checkfirst=True)
    ClientBillingLedgerEntry.__table__.drop(bind=bind, checkfirst=True)
    ClientBillingWebhookEventPlaceholder.__table__.drop(bind=bind, checkfirst=True)
    ClientBillingExternalReference.__table__.drop(bind=bind, checkfirst=True)
    ClientBillingAttempt.__table__.drop(bind=bind, checkfirst=True)
    ClientBillingApproval.__table__.drop(bind=bind, checkfirst=True)
    ClientCheckoutDryRunReceipt.__table__.drop(bind=bind, checkfirst=True)
    ClientBillingReadinessCheck.__table__.drop(bind=bind, checkfirst=True)
    ClientBillingCustomerProfile.__table__.drop(bind=bind, checkfirst=True)
    ClientBillingLiveFlag.__table__.drop(bind=bind, checkfirst=True)
    ClientBillingProviderProfile.__table__.drop(bind=bind, checkfirst=True)
    ClientCommunicationGateEvent.__table__.drop(bind=bind, checkfirst=True)
    ClientCommunicationLiveFlag.__table__.drop(bind=bind, checkfirst=True)
    ClientCommunicationIdempotencyRecord.__table__.drop(bind=bind, checkfirst=True)
    ClientCommunicationExternalMessageReference.__table__.drop(bind=bind, checkfirst=True)
    ClientCommunicationSendAttempt.__table__.drop(bind=bind, checkfirst=True)
    ClientCommunicationSendApproval.__table__.drop(bind=bind, checkfirst=True)
    ClientCommunicationDryRunReceipt.__table__.drop(bind=bind, checkfirst=True)
    ClientCommunicationLiveReadinessCheck.__table__.drop(bind=bind, checkfirst=True)
    ClientCommunicationProviderProfile.__table__.drop(bind=bind, checkfirst=True)
    ClientPlanGateEvent.__table__.drop(bind=bind, checkfirst=True)
    ClientSubscriptionPlaceholder.__table__.drop(bind=bind, checkfirst=True)
    ClientBillingReadinessRecord.__table__.drop(bind=bind, checkfirst=True)
    ClientPlanUpgradeRecommendation.__table__.drop(bind=bind, checkfirst=True)
    ClientSeatUsageRecord.__table__.drop(bind=bind, checkfirst=True)
    ClientUsageCounter.__table__.drop(bind=bind, checkfirst=True)
    ClientFeatureGateEvaluation.__table__.drop(bind=bind, checkfirst=True)
    ClientWorkspacePlanAssignment.__table__.drop(bind=bind, checkfirst=True)
    ClientPlanLimit.__table__.drop(bind=bind, checkfirst=True)
    ClientPlanFeature.__table__.drop(bind=bind, checkfirst=True)
    ClientPlanCatalog.__table__.drop(bind=bind, checkfirst=True)
