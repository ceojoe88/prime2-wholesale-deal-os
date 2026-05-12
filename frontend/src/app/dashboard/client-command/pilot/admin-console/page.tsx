import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientPilotEscalations, clientPilotHealthSnapshots, clientPilotPrograms, clientPilotSupportTickets } from "@/lib/demo-data";

export default function ClientCommandPilotAdminConsolePage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP12 Admin Console" title="Pilot Admin Console" description="Admin support can review and route issues, but cannot force live actions." />
      <Section title="Admin Console">
        <div className="grid-two">
          <RecordCard title="Programs" meta={`Pilot programs: ${clientPilotPrograms.length}.`} right={<Pill tone="green">{clientPilotPrograms.length}</Pill>} />
          <RecordCard title="Health Snapshots" meta={`Pilot health snapshots: ${clientPilotHealthSnapshots.length}.`} right={<Pill tone="gold">{clientPilotHealthSnapshots.length}</Pill>} />
          <RecordCard title="Support Tickets" meta={`Open pilot issues: ${clientPilotSupportTickets.length}.`} right={<Pill tone="gold">{clientPilotSupportTickets.length}</Pill>} />
          <RecordCard title="Escalations" meta={`Escalations in queue: ${clientPilotEscalations.length}.`} right={<Pill tone="red">{clientPilotEscalations.length}</Pill>} />
        </div>
      </Section>
    </div>
  );
}
