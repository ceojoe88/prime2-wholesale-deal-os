import { notFound } from "next/navigation";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { buyerMatches, buyers, formatCurrency, getBuyer, getDeal } from "@/lib/demo-data";

export function generateStaticParams() {
  return buyers.map((buyer) => ({ buyerId: buyer.id }));
}

export default function BuyerDetailPage({ params }: { params: { buyerId: string } }) {
  const buyer = getBuyer(params.buyerId);
  if (!buyer) notFound();
  const matches = buyerMatches.filter((match) => match.buyerId === buyer.id);
  return (
    <div className="page">
      <PageHeader eyebrow="Cash Buyer" title={buyer.company} description={`${buyer.name} / ${buyer.targetZipCodes.join(", ")}`} />
      <div className="metric-grid">
        <div className="metric-card"><span>Max price</span><strong>{formatCurrency(buyer.maxPurchasePrice)}</strong><small>Buyer profile cap</small></div>
        <div className="metric-card"><span>POF</span><strong>{buyer.proofOfFundsStatus}</strong><small>Review status</small></div>
        <div className="metric-card"><span>Close speed</span><strong>{buyer.closingSpeedDays}d</strong><small>Reported capacity</small></div>
        <div className="metric-card"><span>Reliability</span><strong>{buyer.reliabilityScore}</strong><small>Past performance score</small></div>
      </div>
      <div className="grid-two">
        <Section title="Buyer Criteria">
          <div className="pill-row">
            {buyer.targetZipCodes.map((zip) => <Pill key={zip}>{zip}</Pill>)}
            <Pill tone="green">{buyer.propertyType}</Pill>
            <Pill>{buyer.phone}</Pill>
          </div>
        </Section>
        <Section title="Draft Matches">
          <div className="record-list">
            {matches.length ? matches.map((match) => {
              const deal = getDeal(match.dealId);
              return <RecordCard key={match.id} title={match.dealId} meta={`Projected fee ${formatCurrency(deal?.projectedAssignmentFee ?? 0)}`} right={<Pill tone="green">{match.score}</Pill>} />;
            }) : <RecordCard title="No current draft match" meta={buyer.pastPerformance} />}
          </div>
        </Section>
      </div>
    </div>
  );
}
