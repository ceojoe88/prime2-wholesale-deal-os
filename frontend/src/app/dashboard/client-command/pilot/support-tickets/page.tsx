import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientPilotSupportTickets } from "@/lib/demo-data";

export default function ClientCommandPilotSupportTicketsPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP12 Tickets" title="Pilot Support Tickets" description="Admin support can review and route issues, but cannot force live actions." />
      <Section title="Support Tickets">
        <div className="record-list">
          {clientPilotSupportTickets.map((ticket) => (
            <RecordCard key={ticket.id} title={ticket.title} meta={ticket.summary} right={<Pill tone="gold">{ticket.priority}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
