import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientSubscriptionPlaceholders } from "@/lib/demo-data";

export default function ClientCommandPlansSubscriptionPlaceholderPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP9 Subscription Placeholder" title="Subscription Placeholder" description="Plan gate only - no payment has been collected." />
      <Section title="Placeholder Records">
        <div className="record-list">
          {clientSubscriptionPlaceholders.map((record) => (
            <RecordCard
              key={record.id}
              title={record.planCode}
              meta={`${record.clientSafeSummary} Billing contact: ${record.billingContactEmail}.`}
              right={<Pill tone="gold">{record.placeholderStatus}</Pill>}
            />
          ))}
        </div>
      </Section>
    </div>
  );
}
