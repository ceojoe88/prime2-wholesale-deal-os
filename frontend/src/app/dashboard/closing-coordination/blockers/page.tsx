import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { dealRoomBlockers, getDeal, getLead } from "@/lib/demo-data";

export default function ClosingCoordinationBlockersPage() {
  const openBlockers = dealRoomBlockers.filter((blocker) => !blocker.resolved);
  const criticalBlockers = openBlockers.filter((blocker) => blocker.severity === "critical");
  const ownerActionBlockers = openBlockers.filter((blocker) => blocker.ownerActionRequired);
  return (
    <div className="page">
      <PageHeader
        eyebrow="Blocker Engine"
        title="Closing coordination blocker queue"
        description="Missing POF, seller documents, owner approvals, compliance review, title handoff, and unsafe language issues are tracked as internal blockers only."
      />
      <div className="metric-grid">
        <MetricCard label="Open blockers" value={String(openBlockers.length)} detail="Active coordination gaps" />
        <MetricCard label="Critical" value={String(criticalBlockers.length)} detail="Owner or compliance priority" />
        <MetricCard label="Owner action" value={String(ownerActionBlockers.length)} detail="Human approval required" />
        <MetricCard label="Resolved" value={String(dealRoomBlockers.length - openBlockers.length)} detail="Cleared blockers" />
      </div>
      <Section title="Blocker Records">
        <table className="data-table">
          <thead>
            <tr>
              <th>Blocker</th>
              <th>Deal Room</th>
              <th>Property</th>
              <th>Severity</th>
              <th>Recommendation</th>
              <th>Owner</th>
            </tr>
          </thead>
          <tbody>
            {dealRoomBlockers.map((blocker) => {
              const deal = getDeal(blocker.dealId);
              const lead = deal ? getLead(deal.leadId) : undefined;
              return (
                <tr key={blocker.id}>
                  <td>{blocker.blockerType}<div className="record-meta">{blocker.detail}</div></td>
                  <td><Link href={`/dashboard/deal-room/${blocker.dealRoomId}`}>{blocker.dealRoomId}</Link><div className="record-meta">{blocker.source}</div></td>
                  <td>{lead?.city}, {lead?.state}<div className="record-meta">{blocker.dealId}</div></td>
                  <td><Pill tone={blocker.severity === "critical" ? "red" : "gold"}>{blocker.severity}</Pill></td>
                  <td>{blocker.recommendation}<div className="record-meta">recommendation only</div></td>
                  <td><Pill tone={blocker.ownerActionRequired ? "red" : "default"}>{blocker.ownerActionRequired ? "required" : "not required"}</Pill></td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
