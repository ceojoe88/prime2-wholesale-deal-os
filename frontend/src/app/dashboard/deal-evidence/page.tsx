import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  dealEvidencePackets,
  dealsNeedingEvidenceOwnerReview,
  formatCurrency,
  getAssignmentFeeAttributionByPacket,
  getDeal,
  getLead,
  missingEvidencePackets,
  verified10kAssignmentFeeOpportunities
} from "@/lib/demo-data";

export default function DealEvidencePage() {
  const approvedPackets = dealEvidencePackets.filter((packet) => packet.approved);
  return (
    <div className="page">
      <PageHeader
        eyebrow="V8 Deal Evidence"
        title="Proof-backed evidence packets"
        description="Every projected or verified spread is tied to lead, seller, underwriting, buyer, POF, contract, title, communication, blocker, and compliance source records."
      />
      <div className="metric-grid">
        <MetricCard label="Evidence packets" value={String(dealEvidencePackets.length)} detail="Internal proof records" />
        <MetricCard label="Approved evidence" value={String(approvedPackets.length)} detail="Source records and owner review clear" />
        <MetricCard label="Missing evidence" value={String(missingEvidencePackets.length)} detail="Blocked until source records exist" />
        <MetricCard label="10K+ verified" value={String(verified10kAssignmentFeeOpportunities.length)} detail="Actual source-number opportunities" />
      </div>

      <Section title="Evidence Packet Queue">
        <table className="data-table">
          <thead>
            <tr>
              <th>Packet</th>
              <th>Property</th>
              <th>Source Proof</th>
              <th>POF / Compliance</th>
              <th>Evidence</th>
              <th>Attributed Fee</th>
            </tr>
          </thead>
          <tbody>
            {dealEvidencePackets.map((packet) => {
              const deal = getDeal(packet.dealId);
              const lead = deal ? getLead(deal.leadId) : undefined;
              const fee = getAssignmentFeeAttributionByPacket(packet.id);
              return (
                <tr key={packet.id}>
                  <td>
                    <Link href={`/dashboard/deal-evidence/${packet.id}`}>{packet.id}</Link>
                    <div className="record-meta">{packet.dealRoomId}</div>
                  </td>
                  <td>{lead?.city}, {lead?.state}<div className="record-meta">{packet.dealId}</div></td>
                  <td>
                    <div className="pill-row">
                      <Pill tone={packet.sourceRecordsPresent ? "green" : "red"}>{packet.sourceRecordsPresent ? "present" : "missing"}</Pill>
                      <Pill>{packet.leadSource}</Pill>
                    </div>
                  </td>
                  <td>
                    <div className="pill-row">
                      <Pill tone={packet.pofProofStatus === "verified" ? "green" : "gold"}>{packet.pofProofStatus}</Pill>
                      <Pill tone={packet.complianceReviewStatus === "approved" ? "green" : "red"}>{packet.complianceReviewStatus}</Pill>
                    </div>
                  </td>
                  <td><Pill tone={packet.approved ? "green" : packet.evidenceStatus === "owner_review_needed" ? "gold" : "red"}>{packet.evidenceStatus}</Pill></td>
                  <td className="money">{formatCurrency(fee?.projectedAssignmentFee ?? 0)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>

      <div className="grid-two">
        <Section title="Evidence Safety Guard">
          <div className="record-list">
            <RecordCard title="Unsupported profit claims" meta="Fake profit and unsupported ROI language are blocked." right={<Pill tone="red">blocked</Pill>} />
            <RecordCard title="Invented numbers" meta="Buyer and seller prices must come from source records." right={<Pill tone="red">blocked</Pill>} />
            <RecordCard title="Client-facing proof" meta="Evidence remains internal unless a future approval gate is added." right={<Pill tone="red">blocked</Pill>} />
            <RecordCard title="Closing guarantees" meta="Legal or closing guarantees are not allowed." right={<Pill tone="red">blocked</Pill>} />
          </div>
        </Section>
        <Section title="Owner Review Queue">
          <div className="record-list">
            {dealsNeedingEvidenceOwnerReview.map((packet) => (
              <RecordCard
                key={packet.id}
                title={packet.id}
                meta={`${packet.dealId} / ${packet.evidenceStatus}`}
                right={<Pill tone="gold">{packet.ownerReviewStatus}</Pill>}
              />
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
