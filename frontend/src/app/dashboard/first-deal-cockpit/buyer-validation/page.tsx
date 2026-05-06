import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { firstDealBuyerValidation, formatCurrency } from "@/lib/demo-data";

export default function FirstDealBuyerValidationPage() {
  const blocked = firstDealBuyerValidation.filter((row) => !row.validated);
  return (
    <div className="page">
      <PageHeader
        eyebrow="V31 Buyer Validation"
        title="Buyer validation checklist"
        description="Prime 2 checks buyer fit, POF status, response speed, reliability, margin strength, interest, and access requirements before contract-ready recommendations."
      />
      <div className="metric-grid">
        <MetricCard label="Validated" value={String(firstDealBuyerValidation.length - blocked.length)} detail="Buyer gate clear" />
        <MetricCard label="Blocked" value={String(blocked.length)} detail="POF, margin, price, or demand gaps" />
        <MetricCard label="Live buyer contact" value="off" detail="Use gated provider lanes only" />
        <MetricCard label="Buyer data" value="internal" detail="No seller portal exposure" />
      </div>
      <Section title="Validation Rows">
        <table className="data-table">
          <thead>
            <tr>
              <th>Deal</th>
              <th>Top Buyer</th>
              <th>POF</th>
              <th>Max Price</th>
              <th>Reliability</th>
              <th>Margin</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {firstDealBuyerValidation.map((row) => (
              <tr key={row.deal.id}>
                <td>{row.deal.id}</td>
                <td>{row.buyer?.company ?? "Need buyer match"}</td>
                <td>{row.buyer?.proofOfFundsStatus ?? "missing"}</td>
                <td>{row.buyer ? formatCurrency(row.buyer.maxPurchasePrice) : "missing"}</td>
                <td>{row.buyer?.reliabilityScore ?? 0}</td>
                <td>{row.priority?.buyerMarginStrength ?? 0}</td>
                <td><Pill tone={row.validated ? "green" : "red"}>{row.validated ? "validated" : "blocked"}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}

