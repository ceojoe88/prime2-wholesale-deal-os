import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  blockedDistributionPreps,
  buyerPriorityPofGaps,
  buyerReadyDealsFromDemand,
  dealDistributionPreps,
  distributionDraftsPendingApproval,
  formatCurrency,
  getBuyer,
  getDeal,
  getLead,
  tenKDealsWithStrongBuyerDemand
} from "@/lib/demo-data";

export default function DealDistributionPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V9 Deal Distribution Prep"
        title="Draft-only buyer distribution"
        description="Prepare one-recipient buyer deal email drafts, SMS drafts, private deal sheets, call notes, and response trackers without live sends, bulk blasts, or seller data exposure."
      />
      <div className="metric-grid">
        <MetricCard label="Distribution drafts" value={String(dealDistributionPreps.length)} detail="Draft-only records" />
        <MetricCard label="Pending approval" value={String(distributionDraftsPendingApproval.length)} detail="Owner review required" />
        <MetricCard label="Blocked drafts" value={String(blockedDistributionPreps.length)} detail="Compliance, margin, or publication gate" />
        <MetricCard label="POF gaps" value={String(buyerPriorityPofGaps.length)} detail="Buyer ranking blockers" />
      </div>

      <div className="grid-two">
        <Section title="10K+ Deals With Strong Demand">
          <div className="record-list">
            {tenKDealsWithStrongBuyerDemand.map(({ deal, priority, buyer }) => (
              <RecordCard
                key={`${deal.id}-${priority.id}`}
                title={`${deal.id} / ${buyer?.company ?? priority.buyerId}`}
                meta={`Demand ${priority.priorityScore}, projected spread ${formatCurrency(deal.projectedAssignmentFee)}`}
                right={<Pill tone="green">strong</Pill>}
              />
            ))}
          </div>
        </Section>
        <Section title="Safety Boundary">
          <div className="record-list">
            <RecordCard title="Live buyer blasts" meta="Blocked. V9 prepares drafts only." right={<Pill tone="red">off</Pill>} />
            <RecordCard title="Bulk sends" meta="Blocked. One buyer, one deal, one source record." right={<Pill tone="red">off</Pill>} />
            <RecordCard title="Seller/private data" meta="Hidden from every buyer deal sheet." right={<Pill tone="green">sanitized</Pill>} />
            <RecordCard title="Contract execution" meta="No contract or closing action is performed." right={<Pill tone="red">off</Pill>} />
          </div>
        </Section>
      </div>

      <Section title="Distribution Prep Records">
        <table className="data-table">
          <thead>
            <tr>
              <th>Prep</th>
              <th>Deal</th>
              <th>Buyer</th>
              <th>Approval</th>
              <th>Status</th>
              <th>Blocks</th>
            </tr>
          </thead>
          <tbody>
            {dealDistributionPreps.map((prep) => {
              const deal = getDeal(prep.dealId);
              const lead = deal ? getLead(deal.leadId) : undefined;
              const buyer = getBuyer(prep.buyerId);
              return (
                <tr key={prep.id}>
                  <td><Link href={`/dashboard/deal-distribution/${prep.id}`}>{prep.id}</Link></td>
                  <td>{lead?.city}, {lead?.state}<div className="record-meta">{prep.dealId}</div></td>
                  <td>{buyer?.company}<div className="record-meta">{buyer?.proofOfFundsStatus}</div></td>
                  <td>{prep.approvalStatus}</td>
                  <td><Pill tone={prep.draftStatus === "blocked" ? "red" : "gold"}>{prep.draftStatus}</Pill></td>
                  <td>{prep.blockedReasons.length ? prep.blockedReasons.join(", ") : "clear"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>

      <Section title="Buyer-Ready Deals">
        <div className="record-list">
          {buyerReadyDealsFromDemand.map(({ deal, priority, buyer }) => (
            <RecordCard
              key={`${deal.id}-${priority.id}`}
              title={`${deal.id} / ${buyer?.company ?? priority.buyerId}`}
              meta={`Priority score ${priority.priorityScore}; draft distribution only`}
              right={<Pill tone="green">ready</Pill>}
            />
          ))}
        </div>
      </Section>
    </div>
  );
}
