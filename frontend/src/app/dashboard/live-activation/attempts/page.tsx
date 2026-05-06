import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { liveProviderActivationAttempts } from "@/lib/demo-data";

export default function LiveActivationAttemptsPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="Live Attempts" title="Idempotent attempt ledger" description="Attempts are one-action audit records. Duplicates are blocked by idempotency and provider responses are sanitized." />
      <div className="metric-grid">
        <MetricCard label="Attempts" value={String(liveProviderActivationAttempts.length)} detail="One-action records" />
        <MetricCard label="Provider calls" value="0" detail="Current demo state" />
        <MetricCard label="Executed actions" value="0" detail="Blocked until gates pass" />
        <MetricCard label="Duplicates" value={String(liveProviderActivationAttempts.filter((attempt) => attempt.duplicatePrevented).length)} detail="Idempotency guard" />
      </div>
      <Section title="Attempt Ledger">
        <div className="record-list">
          {liveProviderActivationAttempts.map((attempt) => (
            <RecordCard key={attempt.id} title={attempt.activationId} meta={attempt.blockedReasons.join(", ") || attempt.idempotencyKey} right={<Pill tone={attempt.attemptStatus === "blocked" ? "red" : "green"}>{attempt.attemptStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
