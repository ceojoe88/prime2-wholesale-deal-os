import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  assignmentFeeAttributions,
  formatCurrency,
  getAssignmentFeeAttribution,
  getDeal,
  getDealEvidencePacket,
  getLead
} from "@/lib/demo-data";

export function generateStaticParams() {
  return assignmentFeeAttributions.map((fee) => ({ feeId: fee.id }));
}

export default async function AssignmentFeeDetailPage({ params }: { params: Promise<{ feeId: string }> }) {
  const { feeId } = await params;
  const fee = getAssignmentFeeAttribution(feeId);
  if (!fee) notFound();
  const packet = getDealEvidencePacket(fee.evidencePacketId);
  const deal = getDeal(fee.dealId);
  const lead = deal ? getLead(deal.leadId) : undefined;
  const formulaFee = fee.buyerPurchasePrice - fee.sellerContractPrice;

  return (
    <div className="page">
      <PageHeader
        eyebrow={fee.verificationStatus}
        title={`${fee.id} / ${lead?.city ?? "Property"}, ${lead?.state ?? ""}`}
        description="Assignment fee attribution uses actual source numbers only. It does not make guaranteed profit, ROI, legal, or closing claims."
      />
      <div className="metric-grid">
        <MetricCard label="Projected fee" value={formatCurrency(fee.projectedAssignmentFee)} detail="Buyer price minus seller price" />
        <MetricCard label="Target fee" value={formatCurrency(fee.targetAssignmentFee)} detail={fee.projectedAssignmentFee >= fee.targetAssignmentFee ? "10K+ target met" : "Below target"} />
        <MetricCard label="Buyer margin" value={formatCurrency(fee.buyerMargin)} detail="Protected by underwriting snapshot" />
        <MetricCard label="Confidence" value={`${fee.confidenceScore}`} detail={fee.ownerReviewStatus} />
      </div>

      <div className="grid-two">
        <Section title="Source Formula">
          <table className="data-table">
            <tbody>
              <tr><th>Seller contract price</th><td className="money">{formatCurrency(fee.sellerContractPrice)}</td></tr>
              <tr><th>Buyer purchase price</th><td className="money">{formatCurrency(fee.buyerPurchasePrice)}</td></tr>
              <tr><th>Calculated fee</th><td className="money">{formatCurrency(formulaFee)}</td></tr>
              <tr><th>Stored projected fee</th><td className="money">{formatCurrency(fee.projectedAssignmentFee)}</td></tr>
              <tr><th>Formula match</th><td><Pill tone={formulaFee === fee.projectedAssignmentFee ? "green" : "red"}>{formulaFee === fee.projectedAssignmentFee ? "matched" : "blocked"}</Pill></td></tr>
            </tbody>
          </table>
        </Section>

        <Section title="Verification Gate">
          <div className="record-list">
            <RecordCard title="Evidence packet" meta={packet?.evidenceStatus ?? "missing"} right={<Pill tone={packet?.approved ? "green" : "gold"}>{fee.evidencePacketId}</Pill>} />
            <RecordCard title="Source records" meta={fee.sourceRecordsPresent ? "All required source records present" : "Missing source records"} right={<Pill tone={fee.sourceRecordsPresent ? "green" : "red"}>{fee.sourceRecordsPresent ? "present" : "missing"}</Pill>} />
            <RecordCard title="10K+ verified flag" meta="True only when verified and actual source formula is 10K+." right={<Pill tone={fee.verified10kOpportunity ? "green" : "gold"}>{fee.verified10kOpportunity ? "verified" : "not verified"}</Pill>} />
            <RecordCard title="Client-facing proof" meta="Blocked in V8." right={<Pill tone="red">off</Pill>} />
          </div>
        </Section>
      </div>

      <Section title="Attribution Basis">
        <div className="record-list">
          {fee.attributionBasis.map((basis) => (
            <RecordCard key={basis} title={basis} right={<Pill>source</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
