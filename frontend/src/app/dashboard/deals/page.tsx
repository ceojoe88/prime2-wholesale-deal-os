import { DealTable } from "@/components/DealTable";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Section } from "@/components/Section";
import { deals, formatCurrency, hotDeals, underContractDeals } from "@/lib/demo-data";

export default function DealsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Deals"
        title="Active acquisition-to-assignment pipeline"
        description="Deals show ARV, repair assumptions, buyer max price, seller max offer, projected assignment fee, margin, confidence, and risk."
      />
      <div className="metric-grid">
        <MetricCard label="Active deals" value={String(deals.length)} detail="Seeded underwriting records" />
        <MetricCard label="10K+ hot deals" value={String(hotDeals.length)} detail="Middle-man target protected" />
        <MetricCard label="Under contract" value={String(underContractDeals.length)} detail="Compliance review before assignment" />
        <MetricCard label="Highest spread" value={formatCurrency(Math.max(...deals.map((deal) => deal.projectedAssignmentFee)))} detail="Projected assignment fee" />
      </div>
      <Section title="Deal Board">
        <DealTable />
      </Section>
    </div>
  );
}
