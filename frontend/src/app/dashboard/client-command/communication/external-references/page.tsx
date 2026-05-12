import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientCommunicationExternalMessageReferences } from "@/lib/demo-data";

export default function ClientCommandCommunicationExternalReferencesPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP10 External References" title="External Message References" description="Controlled single-message gate - no bulk campaigns." />
      <Section title="External References">
        <div className="record-list">
          {clientCommunicationExternalMessageReferences.length ? (
            clientCommunicationExternalMessageReferences.map((reference) => (
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
            <RecordCard title="No external references" meta="Blocked by default unless compliance, plan, approval, and live flags pass." right={<Pill tone="gold">none</Pill>} />
          )}
        </div>
      </Section>
    </div>
  );
}
