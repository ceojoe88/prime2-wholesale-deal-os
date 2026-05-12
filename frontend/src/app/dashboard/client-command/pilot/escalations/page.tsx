import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientPilotEscalations } from "@/lib/demo-data";

export default function ClientCommandPilotEscalationsPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP12 Escalations" title="Pilot Escalations" description="Controlled live posture requires CP9, CP10, and CP11 gates." />
      <Section title="Escalation Queue">
        <div className="record-list">
          {clientPilotEscalations.map((item) => (
            <RecordCard key={item.id} title={item.escalationType} meta={item.escalationReason} right={<Pill tone="red">{item.escalationStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
