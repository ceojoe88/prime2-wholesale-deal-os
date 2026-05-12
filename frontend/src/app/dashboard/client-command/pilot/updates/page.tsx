import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientPilotClientSafeUpdates,
  clientPilotEvents,
  clientPilotOutcomeCheckpoints
} from "@/lib/demo-data";

const workspaceId = "client-workspace-003";

export default function ClientCommandPilotUpdatesPage() {
  const updates = clientPilotClientSafeUpdates.filter((item) => item.workspaceId === workspaceId);
  const checkpoints = clientPilotOutcomeCheckpoints.filter((item) => item.workspaceId === workspaceId);
  const events = clientPilotEvents.filter((item) => item.workspaceId === workspaceId);

  return (
    <div className="page">
      <PageHeader
        eyebrow="CP12 Updates"
        title="Client-Safe Pilot Updates"
        description="Client-safe updates hide internal governance, provider payloads, and admin notes."
      />

      <Section title="Client-Safe Updates">
        <div className="record-list">
          {updates.map((update) => (
            <RecordCard key={update.id} title={update.updateTitle} meta={update.updateSummary} right={<Pill tone={update.hidesAdminNotes ? "green" : "gold"}>{update.status}</Pill>}>
              <p>{update.clientSafeSummary}</p>
            </RecordCard>
          ))}
        </div>
      </Section>

      <Section title="Outcome Checkpoints">
        <div className="record-list">
          {checkpoints.map((checkpoint) => (
            <RecordCard key={checkpoint.id} title={checkpoint.checkpointName} meta={checkpoint.summary} right={<Pill tone="green">{checkpoint.checkpointStatus}</Pill>} />
          ))}
        </div>
      </Section>

      <Section title="Visible Pilot Events">
        <div className="record-list">
          {events.map((event) => (
            <RecordCard key={event.id} title={event.eventType} meta={event.eventSummary} right={<Pill tone={event.clientVisible ? "green" : "gold"}>{event.clientVisible ? "visible" : "hidden"}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
