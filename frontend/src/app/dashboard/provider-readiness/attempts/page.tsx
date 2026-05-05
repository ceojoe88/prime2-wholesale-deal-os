import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { blockedProviderAttempts, providerAttemptAudits } from "@/lib/demo-data";

export default function ProviderAttemptsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Provider Attempt Audit"
        title="Provider attempts"
        description="Every provider attempt records readiness, idempotency, metadata hashes, blocked reasons, and the fact that no real network call was made."
      />

      <div className="metric-grid">
        <MetricCard label="Attempts" value={String(providerAttemptAudits.length)} detail="Audit ledger entries" />
        <MetricCard label="Blocked" value={String(blockedProviderAttempts.length)} detail="Recorded without provider call" />
        <MetricCard label="Provider calls" value="0" detail="No real network calls" />
        <MetricCard label="Idempotency" value="on" detail="One source/action/key" />
      </div>

      <Section title="Attempt Ledger">
        <div className="record-list">
          {providerAttemptAudits.map((attempt) => (
            <RecordCard
              key={attempt.id}
              title={`${attempt.providerName} / ${attempt.actionType}`}
              meta={`${attempt.sourceDomain} / ${attempt.mode} / ${attempt.idempotencyKey}`}
              right={<Pill tone={attempt.attemptStatus === "blocked" ? "red" : "green"}>{attempt.attemptStatus}</Pill>}
            />
          ))}
        </div>
      </Section>
    </div>
  );
}

