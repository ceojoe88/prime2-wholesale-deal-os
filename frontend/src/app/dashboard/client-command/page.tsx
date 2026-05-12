import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientActivationBlockers,
  clientCommandPermissions,
  clientCommandSafetyCards,
  clientAcquisitionBriefs,
  clientAppointmentReadinessReviews,
  clientBuyerProfiles,
  clientComplianceSetupChecklists,
  clientCommunicationApprovalGates,
  clientComplianceReadinessPlaceholders,
  clientFirstWeeklyCycleReadinessRecords,
  clientGoLiveReadinessGates,
  clientSafeContactStatuses,
  clientPlanCatalogEntries,
  clientPlanLimits,
  clientPlanAssignments,
  clientFeatureGateEvaluations,
  clientUsageCounters,
  clientPlanUpgradeRecommendations,
  clientCommunicationLiveReadinessChecks,
  clientCommunicationDryRunReceipts,
  clientCommunicationSendApprovals,
  clientCommunicationSendAttempts,
  clientBillingReadinessRecords,
  clientBillingProviderProfiles,
  clientBillingCustomerProfiles,
  clientBillingReadinessChecks,
  clientCheckoutDryRunReceipts,
  clientBillingApprovals,
  clientBillingAttempts,
  clientBillingLedgerEntries,
  clientPilotPrograms,
  clientPilotWorkspaceEnrollments,
  clientPilotOperatingModes,
  clientPilotHealthSnapshots,
  clientPilotSupportTickets,
  clientPilotSupportActions,
  clientPilotEscalations,
  clientPilotClientSafeUpdates,
  clientPilotLaunchChecklists,
  clientPilotRiskReviews,
  clientDealBuyerMatches,
  clientDispositionReadinessGates,
  clientDealEvidencePackets,
  clientLeadCards,
  clientLeadDivisionEvents,
  clientLeadNextBestActions,
  clientOnboardingReports,
  clientOnboardingTasks,
  clientMemphisScenarioCards,
  clientOfferReadinessGates,
  clientWorkspaceReadinessScores,
  clientWeeklyBottlenecks,
  clientWeeklyCommandReports,
  clientWeeklyRecommendedActions,
  clientWorkspaces
} from "@/lib/demo-data";

export default function ClientCommandPage() {
  const acquisitionReviewCount = clientAppointmentReadinessReviews.filter((review) => review.requiresHumanReview).length;
  const blockedOffers = clientOfferReadinessGates.filter((gate) => gate.readinessStatus !== "ready_for_client_review").length;
  const strongMatches = clientDealBuyerMatches.filter((match) => match.matchStatus === "strong_match").length;
  const dispositionReady = clientDispositionReadinessGates.filter((gate) => gate.readinessStatus === "ready_for_client_review").length;
  const dispositionBlocked = clientDispositionReadinessGates.filter((gate) => gate.readinessStatus !== "ready_for_client_review").length;
  const buyerDemandNeeded = clientDispositionReadinessGates.filter((gate) => gate.blockReasons.includes("buyer_demand_evidence_missing")).length;
  const blockedContacts = clientSafeContactStatuses.filter((status) => status.status === "blocked").length;
  const complianceNeedsReview = clientSafeContactStatuses.filter((status) => ["needs_review", "missing_consent"].includes(status.status)).length;
  const safeManualUse = clientSafeContactStatuses.filter((status) => status.status === "safe_for_manual_use").length;
  const latestReport = clientWeeklyCommandReports[0];
  const topBottleneck = clientWeeklyBottlenecks[0];
  const nextReportAction = clientWeeklyRecommendedActions[0];
  const onboardingReadiness = clientWorkspaceReadinessScores[0];
  const onboardingGate = clientGoLiveReadinessGates[0];
  const onboardingBlocker = clientActivationBlockers[0];
  const onboardingTask = clientOnboardingTasks[0];
  const firstWeeklyCycle = clientFirstWeeklyCycleReadinessRecords[0];
  const onboardingReport = clientOnboardingReports[0];
  const complianceSetup = clientComplianceSetupChecklists[0];
  const activePlanAssignment = clientPlanAssignments[0];
  const activePlanLimits = clientPlanLimits.find((limit) => limit.planCode === activePlanAssignment?.planCode);
  const billingFeatureGate = clientFeatureGateEvaluations.find((gate) => gate.featureKey === "billing");
  const pilotFeatureGate = clientFeatureGateEvaluations.find((gate) => gate.featureKey === "pilot_mode");
  const blockedFeatureGates = clientFeatureGateEvaluations.filter((gate) => gate.gateStatus !== "allowed").length;
  const usageCounter = clientUsageCounters[0];
  const planUpgrade = clientPlanUpgradeRecommendations[0];
  const blockedCommunicationReadiness = clientCommunicationLiveReadinessChecks.filter((check) => check.readinessStatus === "blocked").length;
  const blockedCommunicationAttempts = clientCommunicationSendAttempts.filter((attempt) => attempt.attemptStatus === "blocked").length;
  const memphisCommunicationGate = clientCommunicationLiveReadinessChecks.find((check) => check.id === "client-comm-readiness-memphis-lead-002") ?? clientCommunicationLiveReadinessChecks[0];
  const billingReadiness = clientBillingReadinessRecords[0];
  const billingCustomer = clientBillingCustomerProfiles[0];
  const billingCheck = clientBillingReadinessChecks[0];
  const blockedBillingAttempts = clientBillingAttempts.filter((attempt) => attempt.attemptStatus === "blocked").length;
  const pilotEnrollment = clientPilotWorkspaceEnrollments[0];
  const pilotMode = clientPilotOperatingModes[0];
  const pilotHealth = clientPilotHealthSnapshots[0];
  const pilotAction = clientPilotSupportActions[0];
  const pilotUpdate = clientPilotClientSafeUpdates[0];
  const pilotLaunch = clientPilotLaunchChecklists[0];
  const pilotRisk = clientPilotRiskReviews[0];
  return (
    <div className="page">
      <PageHeader
        eyebrow="CP1-CP12 Client Command"
        title="Client-safe investor command workspace"
        description="A customer-facing command layer for lead intelligence, acquisition prep, underwriting review, buyer matching, compliance readiness, weekly reporting, onboarding, plan gates, controlled communication, billing safety, and pilot health without exposing internal Prime governance."
      />

      <div className="metric-grid">
        <MetricCard label="Client workspaces" value={String(clientWorkspaces.length)} detail="Tenant-safe command rooms" />
        <MetricCard label="Lead profiles" value={String(clientLeadCards.length)} detail="Client-safe lead intelligence" />
        <MetricCard label="Acquisition briefs" value={String(clientAcquisitionBriefs.length)} detail={`${acquisitionReviewCount} need review`} />
        <MetricCard label="Offer readiness" value={String(clientOfferReadinessGates.length)} detail={`${blockedOffers} blocked by evidence or review`} />
      </div>

      <Section title="CP5 Disposition Panel">
        <div className="metric-grid">
          <MetricCard label="Buyer profiles" value={String(clientBuyerProfiles.length)} detail="Client-safe demo buyers" />
          <MetricCard label="Strong matches" value={String(strongMatches)} detail="Deterministic buy box fit" />
          <MetricCard label="Disposition ready" value={String(dispositionReady)} detail="Manual review only" />
          <MetricCard label="Blocked disposition" value={String(dispositionBlocked)} detail={`${buyerDemandNeeded} need buyer demand evidence`} />
        </div>
      </Section>

      <Section title="CP6 Compliance Panel">
        <div className="metric-grid">
          <MetricCard label="Blocked contacts" value={String(blockedContacts)} detail="Opt-out or blocked manual-use status" />
          <MetricCard label="Needs review" value={String(complianceNeedsReview)} detail="Consent or channel review required" />
          <MetricCard label="Safe manual use" value={String(safeManualUse)} detail="Readiness check only" />
          <MetricCard label="Manual-use gates" value={String(clientCommunicationApprovalGates.length)} detail={`${clientComplianceReadinessPlaceholders.length} placeholders tracked`} />
        </div>
      </Section>

      <Section title="CP7 Weekly Report Panel">
        <div className="metric-grid">
          <MetricCard label="Latest report" value={latestReport?.reportStatus ?? "none"} detail={latestReport?.reportWeekEnd ?? "Not generated"} />
          <MetricCard label="Top bottleneck" value={topBottleneck?.bottleneckType ?? "clear"} detail={topBottleneck?.recommendedFix ?? "No weekly bottlenecks"} />
          <MetricCard label="Next report action" value={nextReportAction?.priority ?? "none"} detail={nextReportAction?.actionSummary ?? "No weekly action"} />
          <MetricCard label="Memphis weekly reports" value={String(clientWeeklyCommandReports.length)} detail="Client-safe weekly summaries" />
        </div>
      </Section>

      <Section title="CP8 Onboarding Panel">
        <div className="metric-grid">
          <MetricCard label="Workspace readiness" value={String(onboardingReadiness?.readinessScore ?? 0)} detail={onboardingReadiness?.readinessStatus ?? "not_started"} />
          <MetricCard label="Activation gate" value={onboardingGate?.gateStatus ?? "not_ready"} detail={onboardingGate?.approvedScope ?? "manual review required"} />
          <MetricCard label="Top blocker" value={onboardingBlocker?.severity ?? "clear"} detail={onboardingBlocker?.blockerSummary ?? "No onboarding blockers"} />
          <MetricCard label="First weekly cycle" value={firstWeeklyCycle?.readyForFirstWeeklyCycle ? "ready" : "review"} detail={firstWeeklyCycle?.recommendedNextStep ?? "Check weekly-cycle readiness"} />
        </div>
      </Section>

      <Section title="CP9 Plans Panel">
        <div className="metric-grid">
          <MetricCard label="Plan catalog" value={String(clientPlanCatalogEntries.length)} detail="Client-safe pricing placeholders only" />
          <MetricCard label="Active plan" value={activePlanAssignment?.planName ?? "unassigned"} detail={activePlanAssignment?.clientSafeSummary ?? "Plan gate pending"} />
          <MetricCard label="Blocked features" value={String(blockedFeatureGates)} detail={planUpgrade?.reasonSummary ?? "No blocked features"} />
          <MetricCard label="Usage footprint" value={`${usageCounter?.leadsCount ?? 0} leads`} detail={`${usageCounter?.buyersCount ?? 0} buyers / ${usageCounter?.usersCount ?? 0} users`} />
        </div>
        <div className="grid-two">
          <RecordCard title="Memphis plan gate" meta={planUpgrade?.clientSafeSummary ?? "Feature access is controlled by plan, readiness, and safety gates."} right={<Link href="/dashboard/client-command/plans">Open Plans</Link>}>
            <p>{planUpgrade?.reasonSummary ?? "No upgrade review is queued."}</p>
            <div className="tag-row">
              <Pill tone="green">No Live Billing</Pill>
              <Pill tone={activePlanLimits?.pilotModeAllowed ? "green" : "gold"}>{activePlanLimits?.pilotModeAllowed ? "Pilot gated" : "Pilot blocked"}</Pill>
            </div>
          </RecordCard>
          <RecordCard title="Feature gate boundary" meta={billingFeatureGate?.reasonSummary ?? "Feature gates stay deterministic and non-live."} right={<Pill tone="red">{blockedFeatureGates} blocked</Pill>}>
            <p>{pilotFeatureGate?.reasonSummary ?? "Pilot mode never bypasses source-domain gates."}</p>
          </RecordCard>
        </div>
      </Section>

      <Section title="CP10 Communication Panel">
        <div className="metric-grid">
          <MetricCard label="Readiness checks" value={String(clientCommunicationLiveReadinessChecks.length)} detail={`${blockedCommunicationReadiness} blocked by gates`} />
          <MetricCard label="Dry-run receipts" value={String(clientCommunicationDryRunReceipts.length)} detail="Dry run does not send a message." />
          <MetricCard label="Approvals" value={String(clientCommunicationSendApprovals.length)} detail="Approval does not send a message." />
          <MetricCard label="Attempt log" value={String(clientCommunicationSendAttempts.length)} detail={`${blockedCommunicationAttempts} blocked single-send attempts`} />
        </div>
        <div className="grid-two">
          <RecordCard title="Memphis communication gate" meta={memphisCommunicationGate?.blockReasons.join(", ") ?? "Communication readiness is blocked until every gate clears."} right={<Link href="/dashboard/client-command/communication">Open Queue</Link>}>
            <p>{memphisCommunicationGate?.noLiveSend ? "Live communication remains manual-only until readiness, dry-run, approval, and live-flag gates all clear." : "Communication review is ready for manual follow-through."}</p>
            <div className="tag-row">
              <Pill tone="green">Manual Only</Pill>
              <Pill tone="red">No Live Send</Pill>
            </div>
          </RecordCard>
          <RecordCard title="Controlled send lane" meta={clientCommunicationDryRunReceipts[0]?.dryRunSummary ?? "Dry runs stay mock-only."} right={<Link href="/dashboard/client-command/communication/dry-runs">Open Dry-Runs</Link>}>
            <p>{clientCommunicationSendApprovals[0]?.reasonSummary ?? "Owner approval is tied to one unchanged draft and one receipt."}</p>
          </RecordCard>
        </div>
      </Section>

      <Section title="CP11 Billing Panel">
        <div className="metric-grid">
          <MetricCard label="Billing readiness" value={billingReadiness?.readinessStatus ?? "not_started"} detail={billingReadiness?.notesSummary ?? "No billing readiness record"} />
          <MetricCard label="Provider profiles" value={String(clientBillingProviderProfiles.length)} detail="Mock billing providers only" />
          <MetricCard label="Checkout dry-runs" value={String(clientCheckoutDryRunReceipts.length)} detail="Dry run stays non-collecting." />
          <MetricCard label="Blocked attempts" value={String(blockedBillingAttempts)} detail={`${clientBillingLedgerEntries.length} ledger entries tracked`} />
        </div>
        <div className="grid-two">
          <RecordCard title="Billing guard" meta={billingCheck?.blockReasons.join(", ") ?? "Billing gates remain blocked until readiness clears."} right={<Link href="/dashboard/client-command/billing">Open Billing</Link>}>
            <p>{clientBillingAttempts[0]?.requestSummary ?? "Billing gate only - no payment occurs unless all billing gates pass."}</p>
            <div className="tag-row">
              <Pill tone="green">No Payment</Pill>
              <Pill tone="green">Dry-Run Only</Pill>
            </div>
          </RecordCard>
          <RecordCard title="Customer data boundary" meta={billingCustomer?.clientSafeSummary ?? "No raw card data is stored."} right={<Pill tone="green">{clientBillingApprovals[0]?.approvalStatus ?? "review"}</Pill>}>
            <p>{clientBillingProviderProfiles[0]?.clientSafeSummary ?? "Billing readiness only - no live billing action occurred."}</p>
          </RecordCard>
        </div>
      </Section>

      <Section title="CP12 Pilot Panel">
        <div className="metric-grid">
          <MetricCard label="Pilot programs" value={String(clientPilotPrograms.length)} detail={`${clientPilotWorkspaceEnrollments.length} workspace enrollment`} />
          <MetricCard label="Operating posture" value={pilotMode?.operatingPosture ?? "manual_only"} detail={pilotMode?.reasonSummary ?? "Pilot posture is manual-only"} />
          <MetricCard label="Support tickets" value={String(clientPilotSupportTickets.length)} detail={`${clientPilotEscalations.length} escalations open`} />
          <MetricCard label="Launch status" value={pilotLaunch?.checklistStatus ?? "blocked"} detail={`${pilotLaunch?.blockReasons.length ?? 0} blockers still open`} />
        </div>
        <div className="grid-two">
          <RecordCard title="Memphis pilot health" meta={pilotHealth?.clientSafeSummary ?? "Pilot mode does not bypass source gates."} right={<Link href="/dashboard/client-command/pilot">Open Pilot</Link>}>
            <p>{pilotUpdate?.updateSummary ?? "Pilot updates stay client-safe and hide admin notes."}</p>
            <div className="tag-row">
              <Pill tone="green">{pilotEnrollment?.pilotMode ?? "beta_pilot"}</Pill>
              <Pill tone="gold">{pilotHealth?.healthStatus ?? "watch"}</Pill>
            </div>
          </RecordCard>
          <RecordCard title="Pilot risk boundary" meta={pilotLaunch?.clientSafeSummary ?? "Pilot launch checklist does not bypass source gates."} right={<Link href="/dashboard/client-command/pilot/launch-checklist">Open Launch Checklist</Link>}>
            <p>{pilotRisk?.summary ?? "Controlled live posture requires CP9, CP10, and CP11 gates."}</p>
            <p>{pilotAction?.actionSummary ?? "Keep pilot in manual-only posture until blockers clear."}</p>
          </RecordCard>
        </div>
      </Section>

      <Section title="Memphis Demo Scenario">
        <div className="record-list">
          {clientMemphisScenarioCards.map((card) => (
            <RecordCard
              key={card.leadId}
              title={card.label}
              meta={card.summary}
              right={<Link href={`/dashboard/client-command/leads/${card.leadId}`}>View Details</Link>}
            >
              <div className="tag-row">
                <Pill tone={card.tone}>{card.status}</Pill>
                <Pill tone="green">client-safe</Pill>
              </div>
            </RecordCard>
          ))}
        </div>
      </Section>

      <Section title="Client Safety Boundary">
        <div className="metric-grid">
          {clientCommandSafetyCards.map((card) => (
            <RecordCard key={card.label} title={card.label} meta={card.detail} right={<Pill tone="red">{card.value}</Pill>} />
          ))}
        </div>
      </Section>

      <div className="grid-two">
        <Section title="AI Division Cards">
          <div className="record-list">
            <RecordCard title="Lead Intelligence Division" meta="Scores motivation, urgency, equity, distress, contactability, probability, and missing data." right={<Pill tone="green">active</Pill>} />
            <RecordCard title="Acquisition Manager" meta="Builds seller conversation briefs, question plans, manual drafts, and appointment readiness." right={<Pill tone="green">CP3</Pill>} />
            <RecordCard title="Underwriting Manager" meta="Checks evidence, ARV, repairs, MAO, scenarios, and offer readiness." right={<Pill tone="green">CP4</Pill>} />
            <RecordCard title="Disposition Manager" meta="Ranks buyer fit, buy box evidence, and disposition readiness without buyer contact." right={<Pill tone="green">CP5</Pill>} />
            <RecordCard title="Compliance Manager" meta="Tracks consent, opt-outs, safe manual-use status, and message risk without any provider checks." right={<Pill tone="green">CP6</Pill>} />
            <RecordCard title="Client Success Manager" meta="Builds weekly rollups, bottlenecks, and next-week action plans without ROI or revenue guarantees." right={<Pill tone="green">CP7</Pill>} />
            <RecordCard title="Onboarding Manager" meta="Tracks client setup, activation blockers, manual-operation readiness, and first weekly-cycle readiness." right={<Pill tone="green">CP8</Pill>} />
            <RecordCard title="Plan Access Manager" meta="Evaluates plan catalog, feature gates, usage limits, and upgrade recommendations without live billing." right={<Pill tone="green">CP9</Pill>} />
            <RecordCard title="Communication Control Manager" meta="Tracks readiness checks, dry-runs, approvals, and blocked single-send attempts without live sends." right={<Pill tone="green">CP10</Pill>} />
            <RecordCard title="Billing Guard Manager" meta="Maintains billing readiness placeholders, blocked checkout attempts, and no-card-data boundaries." right={<Pill tone="green">CP11</Pill>} />
            <RecordCard title="Pilot Operations Manager" meta="Summarizes pilot health, launch blockers, support actions, and client-safe updates without bypassing gates." right={<Pill tone="green">CP12</Pill>} />
            <RecordCard title="Client Workspace Guard" meta="Tenant-safe roles, client permissions, and sanitized workspace responses." right={<Pill tone="green">safe</Pill>} />
            <RecordCard title="Provider Boundary Guard" meta="No outbound provider actions or raw payload exposure in CP1-CP12." right={<Pill tone="red">locked</Pill>} />
          </div>
        </Section>
        <Section title="Lead Intelligence Manager">
          <div className="record-list">
            {clientLeadDivisionEvents.map((event) => (
              <RecordCard key={event.id} title={event.managerStatus} meta={event.eventSummary} right={<Pill tone={event.safeForClient ? "green" : "red"}>{event.divisionName}</Pill>} />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Command Links">
        <div className="grid-three">
          <RecordCard title="Workspaces" meta="Client workspace foundation" right={<Link href="/dashboard/client-command/workspaces">Open</Link>} />
          <RecordCard title="Leads" meta="Lead intelligence profiles" right={<Link href="/dashboard/client-command/leads">Open</Link>} />
          <RecordCard title="Hot Lead Board" meta="Highest priority records" right={<Link href="/dashboard/client-command/hot-leads">Open</Link>} />
          <RecordCard title="Next Actions" meta={`${clientLeadNextBestActions.length} client-safe recommendations`} right={<Link href="/dashboard/client-command/next-actions">Open</Link>} />
          <RecordCard title="Acquisition" meta="Briefs, question plans, and review queue" right={<Link href="/dashboard/client-command/acquisition">Open</Link>} />
          <RecordCard title="Underwriting" meta={`${clientDealEvidencePackets.length} evidence packets`} right={<Link href="/dashboard/client-command/underwriting">Open</Link>} />
          <RecordCard title="Disposition" meta="Buyer matching and disposition readiness" right={<Link href="/dashboard/client-command/disposition">Open</Link>} />
          <RecordCard title="Compliance" meta="Consent, opt-out, and manual-use approval gates" right={<Link href="/dashboard/client-command/compliance">Open</Link>} />
          <RecordCard title="Reports" meta="Weekly command reports and bottlenecks" right={<Link href="/dashboard/client-command/reports">Open</Link>} />
          <RecordCard title="Onboarding" meta={onboardingReport?.reportTitle ?? "Workspace activation readiness"} right={<Link href="/dashboard/client-command/onboarding">Open</Link>} />
          <RecordCard title="Plans" meta={`${activePlanAssignment?.planName ?? "Plan"} with ${blockedFeatureGates} blocked feature gates`} right={<Link href="/dashboard/client-command/plans">Open</Link>} />
          <RecordCard title="Communication" meta={`${blockedCommunicationReadiness} blocked readiness checks`} right={<Link href="/dashboard/client-command/communication">Open</Link>} />
          <RecordCard title="Billing" meta={billingReadiness?.notesSummary ?? "Billing readiness placeholders only"} right={<Link href="/dashboard/client-command/billing">Open</Link>} />
          <RecordCard title="Pilot" meta={pilotUpdate?.updateTitle ?? "Pilot readiness update"} right={<Link href="/dashboard/client-command/pilot">Open</Link>} />
          <RecordCard title="Permissions" meta={`${clientCommandPermissions.length} scoped permissions`} right={<Pill tone="gold">CP1</Pill>} />
          <RecordCard title="Lead Division" meta="Deterministic scoring" right={<Pill tone="gold">CP2</Pill>} />
        </div>
      </Section>

      <Section title="CP8 Readiness Detail">
        <div className="grid-two">
          <RecordCard title="Onboarding Manager" meta={onboardingReport?.clientSafeSummary ?? "Client-safe onboarding report - no revenue, ROI, or deal outcome is guaranteed."} right={<Pill tone="gold">{onboardingGate?.approvedScope ?? "manual only"}</Pill>}>
            <p>{onboardingReadiness?.recommendedNextStep ?? "Calculate readiness to see the next onboarding step."}</p>
            <div className="tag-row">
              <Pill tone="green">Manual Operation Only</Pill>
              <Pill tone="green">No Live Actions</Pill>
            </div>
          </RecordCard>
          <RecordCard title="Memphis demo onboarding status" meta={onboardingTask?.taskTitle ?? "Review activation board"} right={<Pill tone={firstWeeklyCycle?.readyForFirstWeeklyCycle ? "green" : "gold"}>{firstWeeklyCycle?.readyForFirstWeeklyCycle ? "weekly cycle ready" : "setup review"}</Pill>}>
            <p>{complianceSetup?.recommendedNextStep ?? "Readiness checklist only - no DNC provider check or 10DLC live registration occurred."}</p>
          </RecordCard>
        </div>
      </Section>
    </div>
  );
}
