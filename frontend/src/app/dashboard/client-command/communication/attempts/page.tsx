import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientCommunicationSendAttempts } from "@/lib/demo-data";

const workspaceId = "client-workspace-003";

export default function ClientCommandCommunicationAttemptsPage() {
  const attempts = clientCommunicationSendAttempts.filter((item) => item.workspaceId === workspaceId);

  return (
    <div className="page">
      <PageHeader
        eyebrow="CP10 Attempts"
        title="Communication Send Attempts"
        description="Single-message send attempts with idempotent and audited blocking posture. Live send is single-message, idempotent, and audited."
      />

      <Section title="Attempt Ledger">
        <div className="record-list">
          {attempts.map((attempt) => (
            <RecordCard key={attempt.id} title={attempt.channel} meta={attempt.requestSummary} right={<Pill tone={attempt.attemptStatus === "blocked" ? "red" : "green"}>{attempt.attemptStatus}</Pill>}>
              <p>{attempt.blockReasons.join(", ") || "No blocking reasons recorded."}</p>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}
