import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { communicationApprovals, communicationDryRunsNeedingApproval } from "@/lib/demo-data";

export default function CommunicationApprovalsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Owner Approval Gate"
        title="Approval records tied to dry-runs"
        description="Owner approval is valid only for an unchanged draft, one dry-run receipt, one recipient, and one source record."
      />
      <div className="metric-grid">
        <MetricCard label="Approvals" value={String(communicationApprovals.length)} detail="Owner records" />
        <MetricCard label="Pending" value={String(communicationDryRunsNeedingApproval.length)} detail="Dry-runs waiting" />
        <MetricCard label="Stale" value={String(communicationApprovals.filter((approval) => approval.approvalStatus.includes("stale")).length)} detail="Draft changed" />
        <MetricCard label="Global live" value="off" detail="Default disabled" />
      </div>
      <Section title="Approval Log">
        <table className="data-table">
          <thead><tr><th>Approval</th><th>Draft</th><th>Dry-run</th><th>Status</th><th>Approved By</th><th>Notes</th></tr></thead>
          <tbody>
            {communicationApprovals.map((approval) => (
              <tr key={approval.id}>
                <td>{approval.id}</td>
                <td>{approval.draftId}</td>
                <td>{approval.dryRunReceiptId}</td>
                <td><Pill tone={approval.approvalStatus.includes("stale") ? "red" : "green"}>{approval.approvalStatus}</Pill></td>
                <td>{approval.approvedBy}</td>
                <td>{approval.approvalNotes}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
