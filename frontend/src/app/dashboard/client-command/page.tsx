import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientCommandPermissions,
  clientCommandSafetyCards,
  clientAcquisitionBriefs,
  clientAppointmentReadinessReviews,
  clientBuyerProfiles,
  clientCommunicationApprovalGates,
  clientComplianceReadinessPlaceholders,
  clientSafeContactStatuses,
  clientDealBuyerMatches,
  clientDispositionReadinessGates,
  clientDealEvidencePackets,
  clientLeadCards,
  clientLeadDivisionEvents,
  clientLeadNextBestActions,
  clientMemphisScenarioCards,
  clientOfferReadinessGates,
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
  return (
    <div className="page">
      <PageHeader
        eyebrow="CP1-CP7 Client Command"
        title="Client-safe investor command workspace"
        description="A customer-facing command layer for lead intelligence, acquisition prep, underwriting review, buyer matching, compliance readiness, and weekly reporting without exposing internal Prime governance."
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
            <RecordCard title="Client Workspace Guard" meta="Tenant-safe roles, client permissions, and sanitized workspace responses." right={<Pill tone="green">safe</Pill>} />
            <RecordCard title="Provider Boundary Guard" meta="No outbound provider actions or raw payload exposure in CP1-CP7." right={<Pill tone="red">locked</Pill>} />
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
          <RecordCard title="Permissions" meta={`${clientCommandPermissions.length} scoped permissions`} right={<Pill tone="gold">CP1</Pill>} />
          <RecordCard title="Lead Division" meta="Deterministic scoring" right={<Pill tone="gold">CP2</Pill>} />
        </div>
      </Section>
    </div>
  );
}
