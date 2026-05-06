import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { arvConfidenceByDeal, deals, formatCurrency, getLead, learningSignals } from "@/lib/demo-data";

export default function UnderwritingPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Deal Underwriting"
        title="ARV, repairs, MAO, confidence"
        description="Underwriting stays conservative: ARV, repairs, buyer costs, desired profit, and target assignment fee drive the max allowable seller offer."
      />
      <Section title="Underwriting Grid">
        <table className="data-table">
          <thead>
            <tr>
              <th>Deal</th>
              <th>ARV</th>
              <th>Repairs</th>
              <th>Costs</th>
              <th>Buyer Profit</th>
              <th>MAO</th>
              <th>Confidence</th>
            </tr>
          </thead>
          <tbody>
            {deals.map((deal) => (
              <tr key={deal.id}>
                <td>{deal.id}<div className="record-meta">{getLead(deal.leadId)?.zipCode}</div></td>
                <td className="money">{formatCurrency(deal.arv)}</td>
                <td className="money">{formatCurrency(deal.repairs)}</td>
                <td className="money">{formatCurrency(deal.buyerCosts)}</td>
                <td className="money">{formatCurrency(deal.buyerDesiredProfit)}</td>
                <td className="money">{formatCurrency(deal.maxSellerOffer)}</td>
                <td><Pill tone={deal.confidenceScore >= 80 ? "green" : "gold"}>{deal.confidenceScore}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
      <Section title="ARV Confidence From Comps">
        <div className="grid-three">
          {arvConfidenceByDeal.slice(0, 6).map((record) => (
            <RecordCard key={record.dealId} title={record.dealId} meta={`${record.compCount} comp records / ${record.marketId}`} right={<Pill tone={record.arvConfidence >= 75 ? "green" : "gold"}>{record.arvConfidence}</Pill>} />
          ))}
        </div>
      </Section>
      <Section title="Similar Deal Warnings">
        <div className="grid-three">
          {learningSignals.filter((signal) => signal.signalType.includes("document") || signal.signalType.includes("buyer")).map((signal) => (
            <RecordCard key={signal.signalId} title={signal.signalType} meta={`${signal.explanation} Adjustment: ${signal.recommendedAdjustment}`} right={<Pill tone={signal.variance >= 50 ? "gold" : "green"}>{signal.variance}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
