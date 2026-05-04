import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { buyerVisibleDeals, formatCurrency } from "@/lib/demo-data";

export default function BuyerPortalDealsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Sanitized Deals"
        title="Buyer-visible opportunities"
        description="Deal cards show only buyer-facing property, price, range, margin, access, and availability fields."
      />
      <Section title="Deal Table">
        <table className="data-table">
          <thead>
            <tr>
              <th>Market</th>
              <th>Property</th>
              <th>ARV Range</th>
              <th>Repairs</th>
              <th>Asking</th>
              <th>Buyer Margin</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {buyerVisibleDeals.map((deal) => (
              <tr key={deal.dealId}>
                <td><Link href={`/buyer-portal/deals/${deal.dealId}`}>{deal.city}, {deal.state}</Link><div className="record-meta">{deal.zipCode}</div></td>
                <td>{deal.propertyType}<div className="record-meta">{deal.beds} bd / {deal.baths} ba / {deal.sqft} sqft</div></td>
                <td className="money">{formatCurrency(deal.arvRange.low ?? 0)} to {formatCurrency(deal.arvRange.high ?? 0)}</td>
                <td className="money">{formatCurrency(deal.repairEstimateRange.low ?? 0)} to {formatCurrency(deal.repairEstimateRange.high ?? 0)}</td>
                <td className="money">{formatCurrency(deal.askingPrice ?? 0)}</td>
                <td className="money">{formatCurrency(deal.estimatedBuyerMargin ?? 0)}</td>
                <td><Pill tone="green">{deal.availabilityStatus}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
