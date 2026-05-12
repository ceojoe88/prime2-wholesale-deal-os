import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientPilotEscalations,
  clientPilotSupportActions,
  clientPilotSupportTickets
} from "@/lib/demo-data";

const workspaceId = "client-workspace-003";

export default function ClientCommandPilotSupportPage() {
  const tickets = clientPilotSupportTickets.filter((item) => item.workspaceId === workspaceId);
  const actions = clientPilotSupportActions.filter((item) => item.workspaceId === workspaceId);
  const escalations = clientPilotEscalations.filter((item) => item.workspaceId === workspaceId);

  return (
    <div className="page">
      <PageHeader
        eyebrow="CP12 Support"
        title="Admin Support Console"
        description="Admin support can review and route issues, but cannot force live actions."
      />

      <Section title="Support Tickets">
        <div className="record-list">
          {tickets.map((ticket) => (
            <RecordCard key={ticket.id} title={ticket.title} meta={ticket.summary} right={<Pill tone={ticket.priority === "high" || ticket.priority === "urgent" ? "red" : "gold"}>{ticket.status}</Pill>}>
              <p>{ticket.assignedTo}</p>
            </RecordCard>
          ))}
        </div>
      </Section>

      <Section title="Support Actions">
        <div className="record-list">
          {actions.map((action) => (
            <RecordCard key={action.id} title={action.ownerRole} meta={action.actionSummary} right={<Pill tone={action.clientVisible ? "green" : "gold"}>{action.actionStatus}</Pill>} />
          ))}
        </div>
      </Section>

      <Section title="Escalations">
        <div className="record-list">
          {escalations.map((escalation) => (
            <RecordCard key={escalation.id} title={escalation.escalationType} meta={escalation.escalationReason} right={<Pill tone={escalation.requiresHumanReview ? "gold" : "green"}>{escalation.escalationStatus}</Pill>}>
              <p>{`${escalation.sourceDomain} | ${escalation.sourceRecordId ?? "no source record"}`}</p>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}
