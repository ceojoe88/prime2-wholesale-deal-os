import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientBillingApprovals } from "@/lib/demo-data";

export default function ClientCommandBillingApprovalsPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP11 Approvals" title="Billing Approvals" description="Approval does not charge a card." />
      <Section title="Approval Records">
        <div className="record-list">
          {clientBillingApprovals.map((approval) => (
            <RecordCard key={approval.id} title={approval.approvedBy} meta={approval.reasonSummary} right={<Pill tone="green">{approval.approvalStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
