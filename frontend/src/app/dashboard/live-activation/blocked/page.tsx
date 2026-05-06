import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { blockedLiveProviderActivations, liveProviderBlockedAttempts } from "@/lib/demo-data";

export default function LiveActivationBlockedPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="Live Blocked" title="Blocked activation queue" description="Prime 2 records blocked provider lanes and blocked attempts without making provider calls." />
      <div className="metric-grid">
        <MetricCard label="Blocked lanes" value={String(blockedLiveProviderActivations.length)} detail="Readiness or safety gaps" />
        <MetricCard label="Blocked attempts" value={String(liveProviderBlockedAttempts.length)} detail="Audited without provider call" />
        <MetricCard label="Provider called" value="0" detail="Blocked attempts stop first" />
        <MetricCard label="Audit logged" value="yes" detail="Every block is visible" />
      </div>
      <div className="grid-two">
        <Section title="Blocked Lanes">
          <div className="record-list">
            {blockedLiveProviderActivations.map((activation) => (
              <RecordCard key={activation.id} title={activation.providerName} meta={activation.blockedReasons.join(", ")} right={<Pill tone="red">blocked</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Blocked Attempts">
          <div className="record-list">
            {liveProviderBlockedAttempts.map((attempt) => (
              <RecordCard key={attempt.id} title={attempt.actionType} meta={attempt.reason} right={<Pill tone="red">logged</Pill>} />
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
