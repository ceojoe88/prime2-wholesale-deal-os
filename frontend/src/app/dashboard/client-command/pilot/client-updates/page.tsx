import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { getClientPilotClientSafeUpdates } from "@/lib/demo-data";

export default function ClientCommandPilotClientUpdatesPage() {
  const updates = getClientPilotClientSafeUpdates();

  return (
    <div className="page">
      <PageHeader eyebrow="CP12 Client Updates" title="Client-safe Pilot Updates" description="Client-safe updates hide internal governance, provider payloads, and admin notes." />
      <Section title="Client-safe Updates">
        <div className="record-list">
          {updates.map((item) => (
            <RecordCard key={item.id} title={item.updateTitle} meta={item.updateSummary} right={<Pill tone="green">{item.status}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
