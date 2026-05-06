import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { mobileApprovalAttempts, mobileApprovalQueue } from "@/lib/demo-data";

export default function MobileApprovalsPage() {
  const blocked = mobileApprovalAttempts.filter((attempt) => attempt.blockedReasons.length > 0);
  return (
    <div className="page">
      <PageHeader eyebrow="Mobile Approvals" title="Quick approval review" description="Mobile approval checks show gate status and blocked reasons; approval here never executes a provider or contract action." />
      <div className="metric-grid">
        <MetricCard label="Owner queue" value={String(mobileApprovalQueue.length)} detail="Pending review" />
        <MetricCard label="Mobile attempts" value={String(mobileApprovalAttempts.length)} detail="Audit records" />
        <MetricCard label="Blocked" value={String(blocked.length)} detail="Missing gates" />
        <MetricCard label="Execution" value="off" detail="Approval is not execution" />
      </div>
      <Section title="Approval Queue">
        <div className="record-list">
          {mobileApprovalQueue.map((approval) => (
            <RecordCard key={approval.id} title={approval.title} meta={approval.actionSummary} right={<Pill tone={approval.readyForApproval ? "green" : "red"}>{approval.approvalStatus}</Pill>} />
          ))}
        </div>
      </Section>
      <Section title="Mobile Gate Attempts">
        <div className="record-list">
          {mobileApprovalAttempts.map((attempt) => (
            <RecordCard key={attempt.id} title={attempt.approvalType} meta={attempt.blockedReasons.join(", ") || "Ready for owner review only"} right={<Pill tone={attempt.blockedReasons.length ? "red" : "green"}>{attempt.approvalStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
