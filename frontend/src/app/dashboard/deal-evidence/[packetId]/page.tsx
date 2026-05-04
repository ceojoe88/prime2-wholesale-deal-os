import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  dealEvidencePackets,
  formatCurrency,
  getAssignmentFeeAttributionByPacket,
  getDeal,
  getDealEvidencePacket,
  getLead
} from "@/lib/demo-data";

export function generateStaticParams() {
  return dealEvidencePackets.map((packet) => ({ packetId: packet.id }));
}

export default async function DealEvidenceDetailPage({ params }: { params: Promise<{ packetId: string }> }) {
  const { packetId } = await params;
  const packet = getDealEvidencePacket(packetId);
  if (!packet) notFound();
  const fee = getAssignmentFeeAttributionByPacket(packet.id);
  const deal = getDeal(packet.dealId);
  const lead = deal ? getLead(deal.leadId) : undefined;

  return (
    <div className="page">
      <PageHeader
        eyebrow={packet.evidenceStatus}
        title={`${packet.id} / ${lead?.city ?? "Property"}, ${lead?.state ?? ""}`}
        description="This packet proves the deal snapshot from source records only. It excludes internal notes and cannot become client-facing proof without a future approval gate."
      />
      <div className="metric-grid">
        <MetricCard label="Source records" value={packet.sourceRecordsPresent ? "present" : "missing"} detail={packet.leadSource} />
        <MetricCard label="POF proof" value={packet.pofProofStatus} detail="Buyer evidence status" />
        <MetricCard label="Compliance" value={packet.complianceReviewStatus} detail="Review status" />
        <MetricCard label="Attributed fee" value={formatCurrency(fee?.projectedAssignmentFee ?? 0)} detail={fee?.verificationStatus ?? "missing"} />
      </div>

      <div className="grid-two">
        <Section title="Source Proof">
          <div className="record-list">
            <RecordCard title="Seller interaction proof" meta={String(packet.sellerInteractionProof.sellerInteractionId ?? "missing")} right={<Pill tone={packet.sellerInteractionProof.sellerAcceptanceRecorded ? "green" : "red"}>{packet.sellerInteractionProof.sellerAcceptanceRecorded ? "accepted" : "missing"}</Pill>} />
            <RecordCard title="Buyer interest proof" meta={String(packet.buyerInterestProof.buyerInterestId ?? "missing")} right={<Pill tone={packet.buyerInterestProof.buyerInterestId ? "green" : "red"}>{packet.buyerInterestProof.interestStatus}</Pill>} />
            <RecordCard title="Contract control" meta={packet.contractControlStatus} right={<Pill>{String(packet.sellerInteractionProof.acceptedTermsRecordId ?? "missing")}</Pill>} />
            <RecordCard title="Title handoff" meta={packet.titleHandoffStatus} />
          </div>
        </Section>

        <Section title="Underwriting Snapshot">
          <table className="data-table">
            <tbody>
              <tr><th>ARV</th><td className="money">{formatCurrency(Number(packet.underwritingSnapshot.arv ?? 0))}</td></tr>
              <tr><th>Repairs</th><td className="money">{formatCurrency(Number(packet.underwritingSnapshot.repairs ?? 0))}</td></tr>
              <tr><th>Buyer costs</th><td className="money">{formatCurrency(Number(packet.underwritingSnapshot.buyerCosts ?? 0))}</td></tr>
              <tr><th>Seller contract price</th><td className="money">{formatCurrency(Number(packet.underwritingSnapshot.sellerContractPrice ?? 0))}</td></tr>
              <tr><th>Buyer purchase price</th><td className="money">{formatCurrency(Number(packet.underwritingSnapshot.buyerPurchasePrice ?? 0))}</td></tr>
            </tbody>
          </table>
        </Section>
      </div>

      <Section title="Receipts And Blockers">
        <div className="grid-two">
          <div className="record-list">
            {packet.communicationReceipts.length ? packet.communicationReceipts.map((receipt) => (
              <RecordCard key={String(receipt.draftId)} title={String(receipt.draftId)} meta={`Source ${receipt.sourceRecordId}; dry-runs ${Array.isArray(receipt.dryRunReceipts) ? receipt.dryRunReceipts.join(", ") || "none" : "none"}`} right={<Pill tone={receipt.safetyPassed ? "green" : "gold"}>{receipt.providerMode}</Pill>} />
            )) : <RecordCard title="No communication receipts" meta="No communication dry-run proof is tied to this packet yet." />}
          </div>
          <div className="record-list">
            {packet.blockerHistory.length ? packet.blockerHistory.map((blocker) => (
              <RecordCard key={String(blocker.blockerId)} title={String(blocker.blockerType)} meta={String(blocker.status)} right={<Pill tone={blocker.resolved ? "green" : "red"}>{blocker.resolved ? "resolved" : "open"}</Pill>} />
            )) : <RecordCard title="No blocker history" meta="Current evidence packet has no open blockers." right={<Pill tone="green">clear</Pill>} />}
          </div>
        </div>
      </Section>

      <Section title="Sanitization">
        <div className="grid-three">
          <RecordCard title="Internal notes" meta="Call notes, motivations, objections, and private recommendations are stripped." right={<Pill tone="green">sanitized</Pill>} />
          <RecordCard title="Client-facing proof" meta="Blocked in V8." right={<Pill tone="red">off</Pill>} />
          <RecordCard title="Legal/closing guarantees" meta="Blocked in V8." right={<Pill tone="red">off</Pill>} />
        </div>
      </Section>
    </div>
  );
}
