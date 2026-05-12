import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientPilotEscalations, clientPilotSupportActions, clientPilotSupportTickets } from "@/lib/demo-data";

export default function ClientCommandPilotSupportConsolePage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP12 Support Console" title="Pilot Support Console" description="Client-safe updates hide internal governance, provider payloads, and admin notes." />
      <Section title="Support Console">
        <div className="record-list">
          {clientPilotSupportTickets.map((ticket) => (
            <RecordCard key={ticket.id} title={ticket.title} meta={ticket.summary} right={<Pill tone="gold">{ticket.ticketType}</Pill>} />
          ))}
          {clientPilotSupportActions.map((action) => (
            <RecordCard key={action.id} title={action.ownerRole} meta={action.actionSummary} right={<Pill tone="green">{action.actionStatus}</Pill>} />
          ))}
          {clientPilotEscalations.map((escalation) => (
            <RecordCard key={escalation.id} title={escalation.escalationType} meta={escalation.escalationReason} right={<Pill tone="red">{escalation.escalationStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
