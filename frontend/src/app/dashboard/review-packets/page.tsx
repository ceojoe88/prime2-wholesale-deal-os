import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  getDeal,
  getLead,
  reviewPacketBlocks,
  reviewPacketPrepReady,
  reviewPacketPreps
} from "@/lib/demo-data";

export default function ReviewPacketsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V11 Review Packet Prep"
        title="Draft-only title review packets"
        description="Packet preparation organizes property, seller terms, buyer/assignment readiness, timeline, access, compliance, and document checklists without submission or legal execution."
      />
      <div className="metric-grid">
        <MetricCard label="Packets" value={String(reviewPacketPreps.length)} detail="Draft-only review packets" />
        <MetricCard label="Prep-ready" value={String(reviewPacketPrepReady.length)} detail="V10 and owner gates clear" />
        <MetricCard label="Blocked" value={String(reviewPacketBlocks.length)} detail="Needs review before packet prep" />
        <MetricCard label="Submitted" value="0" detail="Submission is blocked" />
      </div>

      <Section title="Review Packet Queue">
        <table className="data-table">
          <thead>
            <tr>
              <th>Packet</th>
              <th>Deal</th>
              <th>Property</th>
              <th>Timeline</th>
              <th>Status</th>
              <th>Blocks</th>
            </tr>
          </thead>
          <tbody>
            {reviewPacketPreps.map((packet) => {
              const deal = getDeal(packet.dealId);
              const lead = deal ? getLead(deal.leadId) : undefined;
              return (
                <tr key={packet.id}>
                  <td><Link href={`/dashboard/title-review/${packet.titleReviewCoordinationId}`}>{packet.id}</Link><div className="record-meta">{packet.titleReviewCoordinationId}</div></td>
                  <td>{packet.dealId}<div className="record-meta">{lead?.sellerName}</div></td>
                  <td>{packet.propertySummary.city}, {packet.propertySummary.state} {packet.propertySummary.zip}</td>
                  <td>{packet.closingTimeline}</td>
                  <td><Pill tone={packet.prepAllowed ? "green" : "red"}>{packet.packetStatus}</Pill></td>
                  <td>{packet.blockedReasons.length ? packet.blockedReasons.join(", ") : "clear"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>

      <div className="grid-two">
        <Section title="Ready Packet Contents">
          <div className="record-list">
            {reviewPacketPrepReady.map((packet) => (
              <RecordCard key={packet.id} title={packet.id} meta={`${packet.documentChecklist.length} document checklist items, ${packet.complianceChecklist.length} compliance confirmations`} right={<Pill tone="green">draft</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Hard Blocks">
          <div className="record-list">
            <RecordCard title="Title-company email" meta="Blocked; no live title handoff email in V11." right={<Pill tone="red">off</Pill>} />
            <RecordCard title="Attorney-client relationship" meta="Blocked; the app only tracks review reminders." right={<Pill tone="red">off</Pill>} />
            <RecordCard title="Closing guarantees" meta="Blocked; no guaranteed close language." right={<Pill tone="red">off</Pill>} />
          </div>
        </Section>
      </div>
    </div>
  );
}
