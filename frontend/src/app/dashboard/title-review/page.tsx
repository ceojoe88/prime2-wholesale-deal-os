import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  blockedTitleReviewCoordinations,
  getDeal,
  getLead,
  reviewPacketPrepReady,
  titleReviewCoordinations,
  titleReviewMissingItems,
  titleReviewOwnerApprovalNeeded,
  titleReviewReadyRecords
} from "@/lib/demo-data";

export default function TitleReviewPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V11 Title/Attorney Review"
        title="Review coordination gate"
        description="Prepare attorney/title review coordination for contract-ready deals without submitting documents, sending title-company email, giving legal advice, or executing contracts."
      />
      <div className="metric-grid">
        <MetricCard label="Review records" value={String(titleReviewCoordinations.length)} detail="Internal coordination only" />
        <MetricCard label="Packet-ready" value={String(titleReviewReadyRecords.length)} detail="V10 gates cleared" />
        <MetricCard label="Missing items" value={String(titleReviewMissingItems.length)} detail="Documents or approvals needed" />
        <MetricCard label="Title submission" value="off" detail="No document submission" />
      </div>

      <Section title="Review Coordination Queue">
        <table className="data-table">
          <thead>
            <tr>
              <th>Review</th>
              <th>Deal</th>
              <th>Title Placeholder</th>
              <th>Status</th>
              <th>Owner</th>
              <th>Blocks</th>
            </tr>
          </thead>
          <tbody>
            {titleReviewCoordinations.map((record) => {
              const deal = getDeal(record.dealId);
              const lead = deal ? getLead(deal.leadId) : undefined;
              return (
                <tr key={record.id}>
                  <td><Link href={`/dashboard/title-review/${record.id}`}>{record.id}</Link></td>
                  <td>{record.dealId}<div className="record-meta">{lead?.city}, {lead?.state}</div></td>
                  <td>{record.selectedTitleCompanyPlaceholder}</td>
                  <td><Pill tone={record.packetPrepAllowed ? "green" : "red"}>{record.attorneyTitleReviewStatus}</Pill></td>
                  <td><Pill tone={record.ownerApprovalStatus === "approved" ? "green" : "gold"}>{record.ownerApprovalStatus}</Pill></td>
                  <td>{record.blockedReasons.length ? record.blockedReasons.join(", ") : "clear"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>

      <div className="grid-two">
        <Section title="Blocked Reviews">
          <div className="record-list">
            {blockedTitleReviewCoordinations.map((record) => (
              <RecordCard key={record.id} title={record.id} meta={record.blockedReasons.join(", ")} right={<Pill tone="red">{record.missingItems.length} missing</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Gate Summary">
          <div className="record-list">
            <RecordCard title="Review packets ready" meta={`${reviewPacketPrepReady.length} draft packet can be prepared for review`} right={<Pill tone="green">draft</Pill>} />
            <RecordCard title="Owner approval needed" meta={`${titleReviewOwnerApprovalNeeded.length} review record needs owner approval`} right={<Pill tone="gold">owner</Pill>} />
            <RecordCard title="Execution boundary" meta="Contract execution, title submission, title-company email, and legal advice remain blocked." right={<Pill tone="red">blocked</Pill>} />
          </div>
        </Section>
      </div>
    </div>
  );
}
