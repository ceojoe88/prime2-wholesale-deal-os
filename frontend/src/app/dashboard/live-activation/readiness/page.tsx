import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { blockedLiveProviderActivations, liveProviderActivations, readyLiveProviderActivations } from "@/lib/demo-data";

export default function LiveActivationReadinessPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="Live Readiness" title="Provider lane readiness" description="Readiness combines V5/V13/V20/V22/V25/V29 gates, dry-run hashes, live flags, provider posture, and owner approval." />
      <div className="metric-grid">
        <MetricCard label="Total lanes" value={String(liveProviderActivations.length)} detail="Configured provider paths" />
        <MetricCard label="Ready lanes" value={String(readyLiveProviderActivations.length)} detail="All gates passed" />
        <MetricCard label="Blocked lanes" value={String(blockedLiveProviderActivations.length)} detail="Fail-closed" />
        <MetricCard label="Bulk paths" value="off" detail="One-action event model" />
      </div>
      <Section title="Blocked Readiness">
        <div className="record-list">
          {blockedLiveProviderActivations.map((activation) => (
            <RecordCard key={activation.id} title={activation.providerName} meta={activation.blockedReasons.join(", ")} right={<Pill tone="red">blocked</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
