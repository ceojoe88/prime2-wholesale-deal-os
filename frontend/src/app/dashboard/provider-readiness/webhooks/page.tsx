import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { providerWebhookEvents, providerWebhookReviewQueue } from "@/lib/demo-data";

export default function ProviderWebhooksPage() {
  const blocked = providerWebhookEvents.filter((event) => event.normalizedEventStatus === "blocked");

  return (
    <div className="page">
      <PageHeader
        eyebrow="Webhook Receiver Skeleton"
        title="Webhook review queue"
        description="Mock and sandbox webhook payload metadata can be recorded for review. Events never mutate deals automatically, and unsigned live-like payloads are blocked."
      />

      <div className="metric-grid">
        <MetricCard label="Events" value={String(providerWebhookEvents.length)} detail="Metadata hashes only" />
        <MetricCard label="Review queue" value={String(providerWebhookReviewQueue.length)} detail="Manual review tasks" />
        <MetricCard label="Blocked" value={String(blocked.length)} detail="Unsigned live-like payloads" />
        <MetricCard label="Deal mutation" value="off" detail="No automatic changes" />
      </div>

      <Section title="Webhook Events">
        <div className="record-list">
          {providerWebhookEvents.map((event) => (
            <RecordCard
              key={event.id}
              title={`${event.providerType} / ${event.eventType}`}
              meta={`${event.mode} / signature ${event.signaturePresent ? "present" : "missing"} / deal mutated: ${event.dealMutated ? "yes" : "no"}`}
              right={<Pill tone={event.normalizedEventStatus === "blocked" ? "red" : "green"}>{event.normalizedEventStatus}</Pill>}
            />
          ))}
        </div>
      </Section>
    </div>
  );
}

