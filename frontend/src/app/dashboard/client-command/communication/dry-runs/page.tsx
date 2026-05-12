import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientCommunicationDryRunReceipts,
  clientCommunicationLiveReadinessChecks
} from "@/lib/demo-data";

const workspaceId = "client-workspace-003";

export default function ClientCommandCommunicationDryRunsPage() {
  const dryRuns = clientCommunicationDryRunReceipts.filter((item) => item.workspaceId === workspaceId);
  const readinessChecks = clientCommunicationLiveReadinessChecks.filter((item) => item.workspaceId === workspaceId);

  return (
    <div className="page">
      <PageHeader
        eyebrow="CP10 Dry Runs"
        title="Communication Dry Runs"
        description="Dry-run receipts for single-message communication review. Dry run does not send a message."
      />

      <Section title="Dry-Run Receipts">
        <div className="record-list">
          {dryRuns.map((receipt) => (
            <RecordCard key={receipt.id} title={receipt.sourceDraftType} meta={receipt.dryRunSummary} right={<Pill tone="green">{receipt.status}</Pill>}>
              <p>{`${receipt.channel} | ${receipt.idempotencyKey}`}</p>
            </RecordCard>
          ))}
        </div>
      </Section>

      <Section title="Readiness Context">
        <div className="record-list">
          {readinessChecks.map((check) => (
            <RecordCard key={check.id} title={check.sourceDraftType} meta={check.blockReasons.join(", ") || "No blocking reasons recorded."} right={<Pill tone={check.readinessStatus === "ready" ? "green" : "red"}>{check.readinessStatus}</Pill>}>
              <p>{`${check.cp6StatusSnapshot} | ${check.cp9GateSnapshot} | ${check.cp8ReadinessSnapshot}`}</p>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}
