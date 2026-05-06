import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { primeMemoryItems } from "@/lib/demo-data";

export function generateStaticParams() {
  return primeMemoryItems.map((memory) => ({ memoryId: memory.memoryId }));
}

export default function PrimeMemoryDetailPage({ params }: { params: { memoryId: string } }) {
  const memory = primeMemoryItems.find((item) => item.memoryId === params.memoryId);
  if (!memory) {
    notFound();
  }
  return (
    <div className="page">
      <PageHeader
        eyebrow="Memory Detail"
        title={memory.memoryType}
        description="Memory detail keeps source evidence visible internally while hiding strategy from portal-safe projections."
      />
      <div className="metric-grid">
        <MetricCard label="Confidence" value={String(memory.confidenceScore)} detail={memory.status} />
        <MetricCard label="Impact" value={memory.impactArea} detail={memory.sourceDomain} />
        <MetricCard label="Evidence" value={String(memory.evidenceBasis.length)} detail="Source records required" />
        <MetricCard label="External exposure" value="off" detail="Internal strategy hidden" />
      </div>
      <Section title="Memory Summary">
        <div className="grid-two">
          <RecordCard title="Summary" meta={memory.summary} right={<Pill tone={memory.ownerApproved ? "green" : "gold"}>{memory.ownerApproved ? "approved" : "review"}</Pill>} />
          <RecordCard title="Evidence basis" meta={memory.evidenceBasis.join(", ")} right={<Pill>cited</Pill>} />
        </div>
      </Section>
    </div>
  );
}

