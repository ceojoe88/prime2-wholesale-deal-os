import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { buyers, formatCurrency } from "@/lib/demo-data";

export default function BuyersPage() {
  const verified = buyers.filter((buyer) => buyer.proofOfFundsStatus === "verified");
  return (
    <div className="page">
      <PageHeader
        eyebrow="Buyer Disposition"
        title="Cash buyer command board"
        description="Buyer profiles support matching by area, price, property type, spread, reliability, closing speed, and proof of funds."
      />
      <div className="metric-grid">
        <MetricCard label="Cash buyers" value={String(buyers.length)} detail="Seeded buyer profiles" />
        <MetricCard label="Verified POF" value={String(verified.length)} detail="Eligible for priority matching" />
        <MetricCard label="Fastest close" value={`${Math.min(...buyers.map((buyer) => buyer.closingSpeedDays))}d`} detail="Demo closing speed" />
        <MetricCard label="Top capacity" value={formatCurrency(Math.max(...buyers.map((buyer) => buyer.maxPurchasePrice)))} detail="Max purchase price" />
      </div>
      <Section title="Buyer Profiles">
        <table className="data-table">
          <thead>
            <tr>
              <th>Buyer</th>
              <th>Zip Criteria</th>
              <th>Max Price</th>
              <th>POF</th>
              <th>Close</th>
              <th>Reliability</th>
            </tr>
          </thead>
          <tbody>
            {buyers.map((buyer) => (
              <tr key={buyer.id}>
                <td><Link href={`/dashboard/buyers/${buyer.id}`}>{buyer.name}</Link><div className="record-meta">{buyer.company}</div></td>
                <td>{buyer.targetZipCodes.join(", ")}</td>
                <td className="money">{formatCurrency(buyer.maxPurchasePrice)}</td>
                <td><Pill tone={buyer.proofOfFundsStatus === "verified" ? "green" : "gold"}>{buyer.proofOfFundsStatus}</Pill></td>
                <td>{buyer.closingSpeedDays} days</td>
                <td>{buyer.reliabilityScore}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
