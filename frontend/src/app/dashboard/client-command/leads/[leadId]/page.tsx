import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientLeadDivisionEvents,
  clientLeadMissingDataItems,
  clientLeadNextBestActions,
  clientLeadProfiles,
  clientLeadScores,
  formatCurrency,
  getClientLead,
  getClientLeadScore
} from "@/lib/demo-data";

export function generateStaticParams() {
  return clientLeadProfiles.map((lead) => ({ leadId: lead.id }));
}

export default function ClientLeadDetailPage({ params }: { params: { leadId: string } }) {
  const lead = getClientLead(params.leadId);
  const score = getClientLeadScore(params.leadId);
  if (!lead || !score) {
    notFound();
  }
  const missing = clientLeadMissingDataItems.filter((item) => item.leadId === lead.id);
  const actions = clientLeadNextBestActions.filter((item) => item.leadId === lead.id);
  const events = clientLeadDivisionEvents.filter((item) => item.leadId === lead.id);

  return (
    <div className="page">
      <PageHeader
        eyebrow="Client Lead Detail"
        title={lead.displayName}
        description="Sanitized client lead intelligence with scoring reasons, missing data, next action, confidence, and human-review status."
      />

      <div className="metric-grid">
        <MetricCard label="Priority" value={String(score.finalPriorityScore)} detail={score.recommendedNextAction} />
        <MetricCard label="Probability" value={String(score.dealProbabilityScore)} detail="Deterministic CP2 score" />
        <MetricCard label="Confidence" value={score.confidenceLevel} detail={score.requiresHumanReview ? "Human review required" : "Client-safe queue"} />
        <MetricCard label="Estimated equity" value={formatCurrency(lead.estimatedEquity)} detail={`${lead.estimatedEquityPercent}% signal`} />
      </div>

      <Section title="Lead Intelligence Score">
        <div className="grid-three">
          <RecordCard title="Motivation" meta={score.reasonSummary} right={<Pill tone="gold">{score.motivationScore}</Pill>} />
          <RecordCard title="Urgency" meta="Timeline-based urgency signal" right={<Pill tone="gold">{score.urgencyScore}</Pill>} />
          <RecordCard title="Equity" meta={`${lead.estimatedEquityPercent}% estimated equity`} right={<Pill tone="green">{score.equitySignalScore}</Pill>} />
          <RecordCard title="Distress" meta={lead.distressSignals.join(", ") || "none"} right={<Pill tone="gold">{score.distressSignalScore}</Pill>} />
          <RecordCard title="Contactability" meta={lead.contactChannelsPresent.join(", ") || "missing"} right={<Pill tone="gold">{score.contactabilityScore}</Pill>} />
          <RecordCard title="Missing Data" meta={`${missing.length} checklist items`} right={<Pill tone={missing.length ? "red" : "green"}>{score.missingDataScore}</Pill>} />
        </div>
      </Section>

      <Section title="Missing Data Checklist">
        <div className="record-list">
          {missing.length === 0 ? (
            <RecordCard title="No blocking missing data" meta="This lead has the required CP2 readiness fields." right={<Pill tone="green">clear</Pill>} />
          ) : (
            missing.map((item) => (
              <RecordCard key={item.id} title={item.fieldName} meta={item.reason} right={<Pill tone={item.severity === "high" ? "red" : "gold"}>{item.resolutionStatus}</Pill>} />
            ))
          )}
        </div>
      </Section>

      <div className="grid-two">
        <Section title="Recommended Next Action">
          <div className="record-list">
            {actions.map((action) => (
              <RecordCard key={action.id} title={action.actionLabel} meta={action.reason} right={<Pill tone={action.requiresHumanReview ? "gold" : "green"}>{action.confidenceLevel}</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Division Events">
          <div className="record-list">
            {events.map((event) => (
              <RecordCard key={event.id} title={event.managerStatus} meta={event.eventSummary} right={<Pill tone="green">{event.eventType}</Pill>} />
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
