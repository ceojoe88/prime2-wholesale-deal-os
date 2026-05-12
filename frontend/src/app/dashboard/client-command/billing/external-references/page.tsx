import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientBillingExternalReferences } from "@/lib/demo-data";

export default function ClientCommandBillingExternalReferencesPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP11 External References" title="Billing External References" description="Stripe/live provider execution is disabled by default." />
      <Section title="External References">
        <div className="record-list">
          {clientBillingExternalReferences.length ? (
            clientBillingExternalReferences.map((reference) => (
              <RecordCard
                key={reference.id}
                title={reference.externalReference}
                meta={reference.responseMetadataSummary}
                right={<Pill tone="green">{reference.providerMode}</Pill>}
              >
                <p>{reference.externalStatus}</p>
              </RecordCard>
            ))
          ) : (
            <RecordCard title="No external references" meta="Billing gate only - no payment occurs unless all billing gates pass." right={<Pill tone="gold">none</Pill>} />
          )}
        </div>
      </Section>
    </div>
  );
}
