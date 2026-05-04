import { notFound } from "next/navigation";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { buyerVisibleDeals, formatCurrency } from "@/lib/demo-data";

export function generateStaticParams() {
  return buyerVisibleDeals.map((deal) => ({ dealId: deal.dealId }));
}

export default function BuyerDealRoomPage({ params }: { params: { dealId: string } }) {
  const deal = buyerVisibleDeals.find((item) => item.dealId === params.dealId);
  if (!deal) notFound();
  return (
    <div className="page">
      <PageHeader
        eyebrow="Buyer Deal Room"
        title={`${deal.city}, ${deal.state} ${deal.zipCode}`}
        description="This room shows sanitized deal information only. The interest button records a non-binding draft intent for owner review."
      />
      <div className="metric-grid">
        <div className="metric-card"><span>Asking price</span><strong>{formatCurrency(deal.askingPrice ?? 0)}</strong><small>Buyer-facing price</small></div>
        <div className="metric-card"><span>Buyer margin</span><strong>{formatCurrency(deal.estimatedBuyerMargin ?? 0)}</strong><small>Estimated after repairs and costs</small></div>
        <div className="metric-card"><span>Proof of funds</span><strong>{deal.proofOfFundsStatus}</strong><small>Buyer profile status</small></div>
        <div className="metric-card"><span>Availability</span><strong>{deal.availabilityStatus}</strong><small>Operator controlled</small></div>
      </div>
      <div className="grid-two">
        <Section title="Property Snapshot">
          <table className="data-table">
            <tbody>
              <tr><th>Property type</th><td>{deal.propertyType}</td></tr>
              <tr><th>Beds / baths</th><td>{deal.beds} / {deal.baths}</td></tr>
              <tr><th>Sqft</th><td>{deal.sqft}</td></tr>
              <tr><th>ARV range</th><td className="money">{formatCurrency(deal.arvRange.low ?? 0)} to {formatCurrency(deal.arvRange.high ?? 0)}</td></tr>
              <tr><th>Repair estimate</th><td className="money">{formatCurrency(deal.repairEstimateRange.low ?? 0)} to {formatCurrency(deal.repairEstimateRange.high ?? 0)}</td></tr>
            </tbody>
          </table>
        </Section>
        <Section title="Access And Intent">
          <div className="record-list">
            <RecordCard title="Photos" meta={deal.photosPlaceholder.join(" / ")} right={<Pill>placeholder</Pill>} />
            <RecordCard title="Access instructions" meta={deal.accessInstructionsPlaceholder} right={<Pill tone="gold">review</Pill>} />
            <RecordCard title="Offer interest" meta="Records draft intent only; no contract, no payment, no execution." right={<Pill tone="green">draft intent</Pill>}>
              <button className="pill green" type="button">Record draft interest</button>
            </RecordCard>
          </div>
        </Section>
      </div>
    </div>
  );
}
