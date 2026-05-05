import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import {
  blockedOwnerApprovals,
  operatorApprovalAggregates,
  ownerApprovalItems,
  pendingOwnerApprovals,
  readyOwnerApprovals
} from "@/lib/demo-data";

export default function OperatorApprovalsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Owner Approval Console"
        title="Unified approvals"
        description="Approve or review seller sends, buyer sends, offer packet prep, contract-ready status, title review packets, buyer distribution, portal visibility, forecast spend, and automation activation."
      />

      <div className="metric-grid">
        <MetricCard label="Pending" value={String(pendingOwnerApprovals.length)} detail="Owner action required" />
        <MetricCard label="Ready" value={String(readyOwnerApprovals.length)} detail="No current blockers" />
        <MetricCard label="Blocked" value={String(blockedOwnerApprovals.length)} detail="Resolve gate reasons first" />
        <MetricCard label="Executed" value="0" detail="Console never executes actions" />
      </div>

      <Section title="Approval Records">
        <table className="data-table">
          <thead>
            <tr>
              <th>Approval</th>
              <th>Type</th>
              <th>Risk</th>
              <th>Ready</th>
              <th>Blocks</th>
            </tr>
          </thead>
          <tbody>
            {ownerApprovalItems.map((item) => (
              <tr key={item.id}>
                <td>{item.title}<div className="record-meta">{item.sourceRecordType}: {item.sourceRecordId}</div></td>
                <td>{item.approvalType}</td>
                <td><Pill tone={item.riskLevel === "high" ? "red" : "gold"}>{item.riskLevel}</Pill></td>
                <td><Pill tone={item.readyForApproval ? "green" : "red"}>{item.readyForApproval ? "yes" : "no"}</Pill></td>
                <td>{item.blockedReasons.length ? item.blockedReasons.join(", ") : "clear"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>

      <Section title="Approval Types">
        <div className="grid-three">
          {Object.entries(operatorApprovalAggregates).map(([type, count]) => (
            <div className="record-card" key={type}><div className="record-head"><h3>{type}</h3><Pill>{count}</Pill></div></div>
          ))}
        </div>
      </Section>
    </div>
  );
}
