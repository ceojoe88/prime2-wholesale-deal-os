import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  assignmentFeeAttributions,
  evidenceFeesAtRisk,
  formatCurrency,
  getDeal,
  getLead,
  projectedEvidenceAssignmentFees,
  verified10kAssignmentFeeOpportunities,
  verifiedAssignmentFees
} from "@/lib/demo-data";

export default function AssignmentFeesPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V8 Assignment Fee Attribution"
        title="Source-number assignment fee control"
        description="Projected and verified assignment fees are attributed to seller contract price, buyer purchase price, buyer margin, buyer interest, and evidence packet records."
      />
      <div className="metric-grid">
        <MetricCard label="Projected fees" value={formatCurrency(projectedEvidenceAssignmentFees)} detail="All V8 attribution records" />
        <MetricCard label="Verified fees" value={formatCurrency(verifiedAssignmentFees)} detail="Approved evidence only" />
        <MetricCard label="Fees at risk" value={formatCurrency(evidenceFeesAtRisk)} detail="Missing review or proof" />
        <MetricCard label="10K+ verified" value={String(verified10kAssignmentFeeOpportunities.length)} detail="Actual formula verified" />
      </div>

      <Section title="Assignment Fee Attributions">
        <table className="data-table">
          <thead>
            <tr>
              <th>Attribution</th>
              <th>Property</th>
              <th>Seller / Buyer Price</th>
              <th>Projected Fee</th>
              <th>Buyer Margin</th>
              <th>Verification</th>
            </tr>
          </thead>
          <tbody>
            {assignmentFeeAttributions.map((fee) => {
              const deal = getDeal(fee.dealId);
              const lead = deal ? getLead(deal.leadId) : undefined;
              return (
                <tr key={fee.id}>
                  <td>
                    <Link href={`/dashboard/assignment-fees/${fee.id}`}>{fee.id}</Link>
                    <div className="record-meta">{fee.evidencePacketId}</div>
                  </td>
                  <td>{lead?.city}, {lead?.state}<div className="record-meta">{fee.dealId}</div></td>
                  <td className="money">{formatCurrency(fee.sellerContractPrice)} / {formatCurrency(fee.buyerPurchasePrice)}</td>
                  <td className="money">{formatCurrency(fee.projectedAssignmentFee)}</td>
                  <td className="money">{formatCurrency(fee.buyerMargin)}</td>
                  <td><Pill tone={fee.verificationStatus === "verified" ? "green" : fee.verificationStatus === "owner_review_needed" ? "gold" : "red"}>{fee.verificationStatus}</Pill></td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>

      <div className="grid-two">
        <Section title="10K+ Verified Opportunities">
          <div className="record-list">
            {verified10kAssignmentFeeOpportunities.map((fee) => (
              <RecordCard
                key={fee.id}
                title={fee.id}
                meta={`${fee.dealId}: ${formatCurrency(fee.buyerPurchasePrice)} - ${formatCurrency(fee.sellerContractPrice)}`}
                right={<Pill tone="green">{formatCurrency(fee.projectedAssignmentFee)}</Pill>}
              />
            ))}
          </div>
        </Section>
        <Section title="Attribution Guard">
          <div className="record-list">
            <RecordCard title="Formula lock" meta="Projected fee must equal buyer purchase price minus seller contract price." right={<Pill tone="green">source</Pill>} />
            <RecordCard title="Unsupported claims" meta="Guaranteed profit, unsupported ROI, invented numbers, and closing guarantees are blocked." right={<Pill tone="red">blocked</Pill>} />
            <RecordCard title="Owner review" meta="Unapproved evidence stays at risk even when the spread is above 10K." right={<Pill tone="gold">review</Pill>} />
          </div>
        </Section>
      </div>
    </div>
  );
}
