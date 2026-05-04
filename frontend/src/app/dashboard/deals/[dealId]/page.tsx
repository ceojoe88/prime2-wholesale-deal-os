import { notFound } from "next/navigation";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { buyerMatches, deals, formatCurrency, getBuyer, getDeal, getLead } from "@/lib/demo-data";

export function generateStaticParams() {
  return deals.map((deal) => ({ dealId: deal.id }));
}

export default function DealDetailPage({ params }: { params: { dealId: string } }) {
  const deal = getDeal(params.dealId);
  if (!deal) notFound();
  const lead = getLead(deal.leadId);
  const matches = buyerMatches.filter((match) => match.dealId === deal.id);
  return (
    <div className="page">
      <PageHeader
        eyebrow={deal.status}
        title={`${deal.id} / ${lead?.sellerName ?? "seller"}`}
        description="Owner approval is required before offer packet prep; compliance review is required before assignment packet prep."
      />
      <div className="metric-grid">
        <div className="metric-card"><span>ARV</span><strong>{formatCurrency(deal.arv)}</strong><small>Comp-backed assumption</small></div>
        <div className="metric-card"><span>Max seller offer</span><strong>{formatCurrency(deal.maxSellerOffer)}</strong><small>Protects 10K target</small></div>
        <div className="metric-card"><span>Buyer max price</span><strong>{formatCurrency(deal.maxBuyerPurchasePrice)}</strong><small>Protects buyer margin</small></div>
        <div className="metric-card"><span>Projected fee</span><strong>{formatCurrency(deal.projectedAssignmentFee)}</strong><small>{deal.hot ? "10K+ target" : "Review spread"}</small></div>
      </div>
      <div className="grid-two">
        <Section title="Profit Control">
          <table className="data-table">
            <tbody>
              <tr><th>Repairs</th><td className="money">{formatCurrency(deal.repairs)}</td></tr>
              <tr><th>Buyer costs</th><td className="money">{formatCurrency(deal.buyerCosts)}</td></tr>
              <tr><th>Buyer desired profit</th><td className="money">{formatCurrency(deal.buyerDesiredProfit)}</td></tr>
              <tr><th>Seller contract price</th><td className="money">{formatCurrency(deal.sellerContractPrice)}</td></tr>
              <tr><th>Buyer purchase price</th><td className="money">{formatCurrency(deal.buyerPurchasePrice)}</td></tr>
              <tr><th>Buyer margin</th><td className="money">{formatCurrency(deal.buyerMargin)}</td></tr>
            </tbody>
          </table>
        </Section>
        <Section title="Risk And Matches">
          <div className="record-list">
            <RecordCard title="Offer reasonableness" meta={`${deal.offerReasonablenessScore}/100`} right={<Pill tone={deal.offerReasonablenessScore >= 80 ? "green" : "red"}>score</Pill>} />
            <RecordCard title="Spread confidence" meta={`${deal.spreadConfidenceScore}/100`} right={<Pill tone={deal.spreadConfidenceScore >= 80 ? "green" : "gold"}>score</Pill>} />
            {matches.map((match) => {
              const buyer = getBuyer(match.buyerId);
              return <RecordCard key={match.id} title={buyer?.company ?? match.buyerId} meta={`Match score ${match.score}`} right={<Pill tone="green">draft</Pill>} />;
            })}
            {deal.riskFlags.map((flag) => <RecordCard key={flag} title={flag} right={<Pill tone="red">flag</Pill>} />)}
          </div>
        </Section>
      </div>
    </div>
  );
}
