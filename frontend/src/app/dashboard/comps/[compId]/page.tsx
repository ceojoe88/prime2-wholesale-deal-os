import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { comparableSaleRecords, formatCurrency } from "@/lib/demo-data";

export function generateStaticParams() {
  return comparableSaleRecords.map((comp) => ({ compId: comp.compId }));
}

export default function CompDetailPage({ params }: { params: { compId: string } }) {
  const comp = comparableSaleRecords.find((item) => item.compId === params.compId);
  if (!comp) {
    notFound();
  }
  return (
    <div className="page">
      <PageHeader
        eyebrow="Comp Detail"
        title={comp.addressSummary}
        description="A single comp is treated as supporting evidence only; Prime 2 requires context before lifting ARV confidence."
      />
      <div className="metric-grid">
        <MetricCard label="Sale price" value={formatCurrency(comp.salePrice)} detail={comp.saleDate} />
        <MetricCard label="Distance" value={`${comp.distanceMiles} mi`} detail="Closer comps score higher" />
        <MetricCard label="Confidence" value={String(comp.confidenceScore)} detail={comp.source} />
        <MetricCard label="Linked deal" value={comp.dealId ?? "none"} detail={comp.marketId} />
      </div>
      <Section title="Review Notes">
        <div className="grid-two">
          <RecordCard title="Condition notes" meta={comp.conditionNotes} right={<Pill>evidence</Pill>} />
          <RecordCard title="Adjustment notes" meta={comp.adjustmentNotes} right={<Pill tone="gold">review</Pill>} />
        </div>
      </Section>
    </div>
  );
}

