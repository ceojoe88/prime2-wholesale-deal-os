import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { deals, formatCurrency, hotDeals } from "@/lib/demo-data";

export default function ProfitControlPage() {
  const belowTarget = deals.filter((deal) => deal.projectedAssignmentFee < 10000);
  return (
    <div className="page">
      <PageHeader
        eyebrow="Middle-Man Profit Control"
        title="Reasonable offers, protected spread"
        description="Max buyer purchase price equals ARV minus repairs, buyer costs, and buyer desired profit. Max seller offer subtracts the target assignment fee."
      />
      <div className="metric-grid">
        <MetricCard label="10K+ opportunities" value={String(hotDeals.length)} detail="Prioritized by Wholesale Prime" />
        <MetricCard label="Below target" value={String(belowTarget.length)} detail="Blocked or review-required" />
        <MetricCard label="Target fee" value={formatCurrency(10000)} detail="Owner-controlled v1 policy" />
        <MetricCard label="Buyer margin flags" value={String(deals.filter((deal) => deal.riskFlags.includes("buyer_margin_below_desired_profit")).length)} detail="Must be repaired" />
      </div>
      <div className="grid-two">
        <Section title="Offer Options">
          <table className="data-table">
            <thead>
              <tr>
                <th>Deal</th>
                <th>Conservative</th>
                <th>Standard</th>
                <th>Aggressive</th>
                <th>Reasonable</th>
              </tr>
            </thead>
            <tbody>
              {deals.map((deal) => (
                <tr key={deal.id}>
                  <td>{deal.id}</td>
                  <td className="money">{formatCurrency(deal.conservativeOffer)}</td>
                  <td className="money">{formatCurrency(deal.standardOffer)}</td>
                  <td className="money">{formatCurrency(deal.aggressiveOffer)}</td>
                  <td><Pill tone={deal.offerReasonablenessScore >= 80 ? "green" : "red"}>{deal.offerReasonablenessScore}</Pill></td>
                </tr>
              ))}
            </tbody>
          </table>
        </Section>
        <Section title="Risk Blocks">
          <div className="record-list">
            {deals.flatMap((deal) =>
              deal.riskFlags.map((flag) => <RecordCard key={`${deal.id}-${flag}`} title={flag} meta={deal.id} right={<Pill tone="red">blocked</Pill>} />)
            )}
          </div>
        </Section>
      </div>
    </div>
  );
}
