import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  bestBuyersForHotDeals,
  buyerDealPriorities,
  buyerPriorityPofGaps,
  buyerReadyDealsFromDemand,
  fastCloseBuyerList,
  formatCurrency,
  getBuyer,
  getDeal,
  getLead,
  tenKDealsWithStrongBuyerDemand
} from "@/lib/demo-data";

export default function BuyerPriorityPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V9 Buyer Priority Ranking"
        title="Most likely buyers to close fast"
        description="Rank buyers per deal by area match, price fit, POF, reliability, close speed, deal type, and buyer margin strength. Recommendations remain internal only."
      />
      <div className="metric-grid">
        <MetricCard label="Priority records" value={String(buyerDealPriorities.length)} detail="Per-deal buyer scoring" />
        <MetricCard label="POF gaps" value={String(buyerPriorityPofGaps.length)} detail="Must clear before live consideration" />
        <MetricCard label="Fast-close buyers" value={String(fastCloseBuyerList.length)} detail="Verified and ten days or faster" />
        <MetricCard label="10K+ strong demand" value={String(tenKDealsWithStrongBuyerDemand.length)} detail="Hot spread plus buyer fit" />
      </div>

      <div className="grid-two">
        <Section title="Best Buyer Per Hot Deal">
          <div className="record-list">
            {bestBuyersForHotDeals.map(({ deal, priority, buyer }) => (
              <RecordCard
                key={`${deal.id}-${priority.id}`}
                title={`${deal.id} / ${buyer?.company ?? priority.buyerId}`}
                meta={`${priority.rankingReasons.join(", ")}; projected spread ${formatCurrency(deal.projectedAssignmentFee)}`}
                right={<Pill tone={priority.priorityScore >= 90 ? "green" : "gold"}>{priority.priorityScore}</Pill>}
              />
            ))}
          </div>
        </Section>
        <Section title="Readiness Limits">
          <div className="record-list">
            <RecordCard title="Recommendations only" meta="Buyer ranking does not send, negotiate, or execute." right={<Pill tone="green">internal</Pill>} />
            <RecordCard title="Fake competition" meta="Unsupported scarcity and fake offer language are blocked." right={<Pill tone="red">blocked</Pill>} />
            <RecordCard title="Buyer-ready deals" meta={`${buyerReadyDealsFromDemand.length} hot records have visible publication plus strong buyer fit.`} right={<Pill tone="green">{buyerReadyDealsFromDemand.length}</Pill>} />
          </div>
        </Section>
      </div>

      <Section title="Priority Ranking Matrix">
        <table className="data-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Deal</th>
              <th>Buyer</th>
              <th>Area / Price</th>
              <th>POF / Close</th>
              <th>Margin</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            {buyerDealPriorities
              .slice()
              .sort((first, second) => first.dealId.localeCompare(second.dealId) || first.rank - second.rank)
              .map((priority) => {
                const buyer = getBuyer(priority.buyerId);
                const deal = getDeal(priority.dealId);
                const lead = deal ? getLead(deal.leadId) : undefined;
                return (
                  <tr key={priority.id}>
                    <td>{priority.rank}</td>
                    <td>{priority.dealId}<div className="record-meta">{lead?.zipCode} {lead?.propertyType}</div></td>
                    <td>{buyer?.company}<div className="record-meta">{buyer?.proofOfFundsStatus}</div></td>
                    <td>{priority.targetAreaMatch} / {priority.maxPriceFit}</td>
                    <td>{priority.proofOfFundsScore} / {priority.closingSpeedScore}</td>
                    <td>{priority.buyerMarginStrength}</td>
                    <td><Pill tone={priority.priorityScore >= 85 ? "green" : "gold"}>{priority.priorityScore}</Pill></td>
                  </tr>
                );
              })}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
