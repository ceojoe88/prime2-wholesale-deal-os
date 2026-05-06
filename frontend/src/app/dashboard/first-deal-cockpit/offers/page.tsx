import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { firstDealOfferBoard, formatCurrency } from "@/lib/demo-data";

export default function FirstDealOffersPage() {
  const ready = firstDealOfferBoard.filter((offer) => offer.decisionStatus === "ready_for_owner_review");
  return (
    <div className="page">
      <PageHeader
        eyebrow="V31 Offer Decision Board"
        title="Owner offer decision queue"
        description="Prime 2 surfaces ARV, repairs, buyer costs, buyer max price, max seller offer, protected spread, reasonableness notes, and owner review status."
      />
      <div className="metric-grid">
        <MetricCard label="Offer rows" value={String(firstDealOfferBoard.length)} detail="System-numbered only" />
        <MetricCard label="Owner ready" value={String(ready.length)} detail="Review before seller-facing action" />
        <MetricCard label="Blocked" value={String(firstDealOfferBoard.length - ready.length)} detail="Data, margin, or review gaps" />
        <MetricCard label="Live outreach" value="off" detail="Draft and decision support only" />
      </div>
      <Section title="Offer Decisions">
        <table className="data-table">
          <thead>
            <tr>
              <th>Deal</th>
              <th>ARV / Repairs</th>
              <th>Buyer Max</th>
              <th>Max Seller</th>
              <th>Offer Options</th>
              <th>Margin</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {firstDealOfferBoard.map(({ deal, lead, decisionStatus, blockedReasons, buyerMarginImpact }) => (
              <tr key={deal.id}>
                <td>{deal.id}<div className="record-meta">{lead?.city}, {lead?.state}</div></td>
                <td>{formatCurrency(deal.arv)} / {formatCurrency(deal.repairs)}</td>
                <td>{formatCurrency(deal.maxBuyerPurchasePrice)}</td>
                <td>{formatCurrency(deal.maxSellerOffer)}</td>
                <td>{formatCurrency(deal.conservativeOffer)} / {formatCurrency(deal.standardOffer)} / {formatCurrency(deal.aggressiveOffer)}</td>
                <td>{formatCurrency(buyerMarginImpact)}</td>
                <td><Pill tone={blockedReasons.length ? "gold" : "green"}>{decisionStatus}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}

