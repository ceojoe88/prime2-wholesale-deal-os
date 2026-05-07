import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientCommunicationApprovalGates } from "@/lib/demo-data";

export default function ClientCommandComplianceGatesPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP6 Gates" title="Communication Approval Gates" description="Manual-use approval only - no message has been sent." />
      <Section title="Communication Approval Gate">
        <div className="record-list">
          {clientCommunicationApprovalGates.map((gate) => (
            <RecordCard key={gate.id} title={gate.sourceDraftType} meta={gate.clientSafeSummary} right={<Pill tone={gate.gateStatus === "manual_use_allowed" ? "green" : "gold"}>{gate.gateStatus}</Pill>}>
              <p>Manual-use approval only - no message has been sent.</p>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}
