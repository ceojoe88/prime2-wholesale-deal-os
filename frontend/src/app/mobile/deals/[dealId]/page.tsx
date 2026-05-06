import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { deals, formatCurrency, getDeal, getLead } from "@/lib/demo-data";

export function generateStaticParams() {
  return deals.map((deal) => ({ dealId: deal.id }));
}

export default function MobileDealDetailPage({ params }: { params: { dealId: string } }) {
  const deal = getDeal(params.dealId);
  if (!deal) notFound();
  const lead = getLead(deal.leadId);
  return (
    <div className="page">
      <PageHeader eyebrow="Mobile Deal" title={deal.id} description={`${lead?.city ?? "Market"}, ${lead?.state ?? ""} / ${deal.status}`} />
      <div className="metric-grid">
        <MetricCard label="Projected fee" value={formatCurrency(deal.projectedAssignmentFee)} detail="System record only" />
        <MetricCard label="Buyer margin" value={formatCurrency(deal.buyerMargin)} detail="Protected before action" />
        <MetricCard label="Max buyer price" value={formatCurrency(deal.maxBuyerPurchasePrice)} detail="From underwriting" />
        <MetricCard label="Risk score" value={String(deal.riskScore)} detail="Owner review signal" />
      </div>
      <div className="grid-two">
        <Section title="Deal Facts">
          <table className="data-table">
            <tbody>
              <tr><th>ARV</th><td className="money">{formatCurrency(deal.arv)}</td></tr>
              <tr><th>Repairs</th><td className="money">{formatCurrency(deal.repairs)}</td></tr>
              <tr><th>Max seller offer</th><td className="money">{formatCurrency(deal.maxSellerOffer)}</td></tr>
              <tr><th>Status</th><td>{deal.status}</td></tr>
            </tbody>
          </table>
        </Section>
        <Section title="Mobile Boundaries">
          <div className="record-list">
            <RecordCard title="Terms" meta="View-only in field mode; source records remain authoritative" right={<Pill tone="gold">locked</Pill>} />
            <RecordCard title="Portal visibility" meta="Requires owner gate outside quick capture" right={<Pill tone="red">off</Pill>} />
            <RecordCard title="Contract prep" meta="External review workflow remains separate" right={<Pill tone="red">off</Pill>} />
          </div>
        </Section>
      </div>
    </div>
  );
}
