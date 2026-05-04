import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import {
  assignmentReadinessRecords,
  assignmentReadyRecords,
  blockedAssignmentReadiness,
  buyerPofGaps,
  getBuyer,
  getContractControl,
  getDeal,
  getLead
} from "@/lib/demo-data";

export default function AssignmentReadinessPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Assignment Readiness Gate"
        title="Buyer, POF, compliance, and owner approval control"
        description="A deal is assignment-ready only when contract control exists, assignment is allowed, buyer match and interest are recorded, POF is verified, and approvals pass."
      />
      <div className="metric-grid">
        <MetricCard label="Readiness records" value={String(assignmentReadinessRecords.length)} detail="Internal checks" />
        <MetricCard label="Assignment-ready" value={String(assignmentReadyRecords.length)} detail="Gate clear" />
        <MetricCard label="Blocked" value={String(blockedAssignmentReadiness.length)} detail="Reason tracked" />
        <MetricCard label="POF gaps" value={String(buyerPofGaps.length)} detail="Buyer review needed" />
      </div>
      <Section title="Assignment Readiness Queue">
        <table className="data-table">
          <thead>
            <tr>
              <th>Record</th>
              <th>Deal</th>
              <th>Buyer</th>
              <th>Contract</th>
              <th>POF</th>
              <th>Readiness</th>
              <th>Blocks</th>
            </tr>
          </thead>
          <tbody>
            {assignmentReadinessRecords.map((record) => {
              const deal = getDeal(record.dealId);
              const lead = deal ? getLead(deal.leadId) : undefined;
              const buyer = record.buyerId ? getBuyer(record.buyerId) : undefined;
              const contract = getContractControl(record.contractControlId);
              return (
                <tr key={record.id}>
                  <td>{record.id}<div className="record-meta">{record.readinessStatus}</div></td>
                  <td>{record.dealId}<div className="record-meta">{lead?.city}, {lead?.state}</div></td>
                  <td>{buyer?.company ?? "missing"}<div className="record-meta">{record.buyerInterestId ?? "no interest"}</div></td>
                  <td><Pill tone={contract?.contractPrepAllowed ? "green" : "red"}>{contract?.contractPrepAllowed ? "ready" : "blocked"}</Pill></td>
                  <td><Pill tone={record.buyerPofStatus === "verified" ? "green" : "gold"}>{record.buyerPofStatus}</Pill></td>
                  <td><Pill tone={record.assignmentReady ? "green" : "red"}>{record.assignmentReady ? "ready" : "blocked"}</Pill></td>
                  <td>{record.blockedReasons.length ? record.blockedReasons.join(", ") : "clear"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
