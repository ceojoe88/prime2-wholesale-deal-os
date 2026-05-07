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
  clientDealEvidencePackets,
  clientLeadCards,
  clientLeadDivisionEvents,
  clientLeadNextBestActions,
  clientMemphisScenarioCards,
  clientOfferReadinessGates,
  clientWorkspaces
} from "@/lib/demo-data";

export default function ClientCommandPage() {
  const acquisitionReviewCount = clientAppointmentReadinessReviews.filter((review) => review.requiresHumanReview).length;
  const blockedOffers = clientOfferReadinessGates.filter((gate) => gate.readinessStatus !== "ready_for_client_review").length;
  return (
    <div className="page">
      <PageHeader
        eyebrow="CP1-CP4 Client Command"
        title="Client-safe investor command workspace"
        description="A customer-facing command layer for lead intelligence, acquisition prep, underwriting review, missing evidence, and readiness gates without exposing internal Prime governance."
      />

      <div className="metric-grid">
        <MetricCard label="Client workspaces" value={String(clientWorkspaces.length)} detail="Tenant-safe command rooms" />
        <MetricCard label="Lead profiles" value={String(clientLeadCards.length)} detail="Client-safe lead intelligence" />
        <MetricCard label="Acquisition briefs" value={String(clientAcquisitionBriefs.length)} detail={`${acquisitionReviewCount} need review`} />
        <MetricCard label="Offer readiness" value={String(clientOfferReadinessGates.length)} detail={`${blockedOffers} blocked by evidence or review`} />
      </div>

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
            <RecordCard title="Client Workspace Guard" meta="Tenant-safe roles, client permissions, and sanitized workspace responses." right={<Pill tone="green">safe</Pill>} />
            <RecordCard title="Provider Boundary Guard" meta="No outbound provider actions or raw payload exposure in CP1-CP4." right={<Pill tone="red">locked</Pill>} />
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
          <RecordCard title="Permissions" meta={`${clientCommandPermissions.length} scoped permissions`} right={<Pill tone="gold">CP1</Pill>} />
          <RecordCard title="Lead Division" meta="Deterministic scoring" right={<Pill tone="gold">CP2</Pill>} />
        </div>
      </Section>
    </div>
  );
}
