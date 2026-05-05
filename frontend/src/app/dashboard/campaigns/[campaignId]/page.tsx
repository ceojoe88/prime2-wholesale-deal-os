import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  campaignRuleRecords,
  getCampaignAttempts,
  getCampaignAudience,
  getCampaignPerformance,
  getCampaignRule,
  getCampaignSequence,
  getCampaignStops
} from "@/lib/demo-data";

export function generateStaticParams() {
  return campaignRuleRecords.map((campaign) => ({ campaignId: campaign.campaignId }));
}

export default async function CampaignDetailPage({
  params
}: {
  params: Promise<{ campaignId: string }>;
}) {
  const { campaignId } = await params;
  const campaign = getCampaignRule(campaignId);
  if (!campaign) notFound();
  const audience = getCampaignAudience(campaign.campaignId);
  const sequence = getCampaignSequence(campaign.campaignId);
  const attempts = getCampaignAttempts(campaign.campaignId);
  const stops = getCampaignStops(campaign.campaignId);
  const performance = getCampaignPerformance(campaign.campaignId)[0];

  return (
    <div className="page">
      <PageHeader
        eyebrow={campaign.status}
        title={campaign.name}
        description={`${campaign.campaignType} for ${campaign.audienceType} audience with owner approval status ${campaign.ownerApprovalStatus}.`}
      />

      <div className="metric-grid">
        <MetricCard label="Daily cap" value={String(campaign.maxRecipientsPerDay)} detail="Rate limit" />
        <MetricCard label="Audience" value={String(audience.length)} detail={`${audience.filter((row) => row.excluded).length} excluded`} />
        <MetricCard label="Steps" value={String(sequence.length)} detail="Draft-only" />
        <MetricCard label="Health" value={performance ? `${performance.campaignHealthScore}%` : "n/a"} detail="Estimate from queue state" />
      </div>

      <div className="grid-two">
        <Section title="Audience Preview">
          <div className="record-list">
            {audience.map((row) => (
              <RecordCard key={row.id} title={row.recipientId} meta={row.exclusionReasons.join(", ") || row.segmentName} right={<Pill tone={row.excluded ? "red" : "green"}>{row.inclusionStatus}</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Sequence Steps">
          <div className="record-list">
            {sequence.map((step) => (
              <RecordCard key={step.id} title={step.messagePurpose} meta={`${step.timingOffsetHours}h offset / ${step.stopCondition}`} right={<Pill tone={step.safetyStatus === "passed" ? "green" : "red"}>{step.approvalStatus}</Pill>} />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Activation Attempts">
        <div className="record-list">
          {attempts.map((attempt) => (
            <RecordCard key={attempt.id} title={attempt.attemptStatus} meta={attempt.blockedReasons.join(", ") || "All activation checks satisfied"} right={<Pill tone={attempt.attemptStatus === "active_controlled" ? "green" : "red"}>{attempt.oneRecipientPerEvent ? "single event" : "blocked"}</Pill>} />
          ))}
        </div>
      </Section>

      <Section title="Stop Events">
        <div className="record-list">
          {stops.map((event) => (
            <RecordCard key={event.id} title={event.eventType} meta={event.reason} right={<Pill tone="gold">{event.campaignPaused ? "paused" : "review"}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}

