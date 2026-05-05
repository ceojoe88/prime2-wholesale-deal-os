import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { campaignPerformanceRecords, campaignStopConditionEvents } from "@/lib/demo-data";

export default function CampaignPerformancePage() {
  const queued = campaignPerformanceRecords.reduce((total, record) => total + record.recipientsQueued, 0);
  const prepared = campaignPerformanceRecords.reduce((total, record) => total + record.messagesPrepared, 0);
  const blocked = campaignPerformanceRecords.reduce((total, record) => total + record.attemptsBlocked, 0);
  return (
    <div className="page">
      <PageHeader
        eyebrow="Campaign Performance"
        title="Controlled campaign health"
        description="Performance tracks prepared messages, dry-runs, approvals, blocked attempts, responses, DNC events, and conversion signals without revenue claims."
      />
      <div className="metric-grid">
        <MetricCard label="Recipients queued" value={String(queued)} detail="Preview-approved only" />
        <MetricCard label="Messages prepared" value={String(prepared)} detail="Draft and dry-run path" />
        <MetricCard label="Blocked attempts" value={String(blocked)} detail="Audited safely" />
        <MetricCard label="Stop events" value={String(campaignStopConditionEvents.length)} detail="Automatic pause triggers" />
      </div>
      <Section title="Performance Records">
        <div className="record-list">
          {campaignPerformanceRecords.map((record) => (
            <RecordCard key={record.id} title={record.campaignId} meta={`health ${record.campaignHealthScore}% / responses ${record.responsesReceived} / DNC ${record.dncEvents}`} right={<Pill tone={record.campaignHealthScore > 70 ? "green" : "gold"}>estimate</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
