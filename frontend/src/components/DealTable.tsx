import Link from "next/link";
import { deals, formatCurrency, getLead } from "@/lib/demo-data";
import { Pill } from "@/components/Pill";

export function DealTable({ limit }: { limit?: number }) {
  const rows = typeof limit === "number" ? deals.slice(0, limit) : deals;
  return (
    <table className="data-table">
      <thead>
        <tr>
          <th>Deal</th>
          <th>Seller / Zip</th>
          <th>Max Seller</th>
          <th>Buyer Max</th>
          <th>Spread</th>
          <th>Risk</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((deal) => {
          const lead = getLead(deal.leadId);
          return (
            <tr key={deal.id}>
              <td>
                <Link href={`/dashboard/deals/${deal.id}`}>{deal.id}</Link>
                <div className="record-meta">{deal.status}</div>
              </td>
              <td>
                {lead?.sellerName}
                <div className="record-meta">{lead?.zipCode}</div>
              </td>
              <td className="money">{formatCurrency(deal.maxSellerOffer)}</td>
              <td className="money">{formatCurrency(deal.maxBuyerPurchasePrice)}</td>
              <td className="money">{formatCurrency(deal.projectedAssignmentFee)}</td>
              <td>
                {deal.hot ? <Pill tone="green">10K target</Pill> : <Pill tone="gold">review</Pill>}
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
