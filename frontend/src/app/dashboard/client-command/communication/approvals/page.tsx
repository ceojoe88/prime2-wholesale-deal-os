import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientCommunicationSendApprovals,
  clientCommunicationLiveReadinessChecks
} from "@/lib/demo-data";

const workspaceId = "client-workspace-003";

export default function ClientCommandCommunicationApprovalsPage() {
  const approvals = clientCommunicationSendApprovals.filter((item) => item.workspaceId === workspaceId);
  const readinessChecks = clientCommunicationLiveReadinessChecks.filter((item) => item.workspaceId === workspaceId);

  return (
    <div className="page">
      <PageHeader
        eyebrow="CP10 Approvals"
        title="Communication Approvals"
        description="Approval review for future live communication posture. Approval does not send a message."
      />

      <Section title="Approval Records">
        <div className="record-list">
          {approvals.map((approval) => (
            <RecordCard key={approval.id} title={approval.approvedBy} meta={approval.reasonSummary} right={<Pill tone={approval.approvalStatus === "approved" ? "green" : approval.approvalStatus === "pending" ? "gold" : "red"}>{approval.approvalStatus}</Pill>} />
          ))}
        </div>
      </Section>

      <Section title="Blocking Context">
        <div className="record-list">
          {readinessChecks.map((check) => (
            <RecordCard key={check.id} title={check.sourceDraftType} meta={check.blockReasons.join(", ") || "No blocking reasons recorded."} right={<Pill tone={check.approvalPresent ? "green" : "gold"}>{check.approvalPresent ? "approval present" : "approval missing"}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
