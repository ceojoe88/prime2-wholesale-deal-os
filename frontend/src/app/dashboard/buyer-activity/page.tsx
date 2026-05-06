import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { buyerActivitySnapshots, formatCurrency } from "@/lib/demo-data";

export default function BuyerActivityPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Buyer Activity"
        title="Market demand snapshots"
        description="Buyer activity snapshots improve buyer-demand confidence using active buyers, POF strength, closing speed, response velocity, and recent interest."
      />
      <div className="metric-grid">
        <MetricCard label="Snapshots" value={String(buyerActivitySnapshots.length)} detail="Market-level demand records" />
        <MetricCard label="Active buyers" value={String(buyerActivitySnapshots.reduce((total, row) => total + row.activeBuyerCount, 0))} detail="Across tracked markets" />
        <MetricCard label="POF verified" value={String(buyerActivitySnapshots.reduce((total, row) => total + row.pofVerifiedBuyerCount, 0))} detail="Evidence-backed demand" />
        <MetricCard label="Fast close" value={String(buyerActivitySnapshots.reduce((total, row) => total + row.fastCloseBuyerCount, 0))} detail="Closing-speed signal" />
      </div>
      <Section title="Snapshots">
        <div className="record-list">
          {buyerActivitySnapshots.map((snapshot) => (
            <RecordCard key={snapshot.id} title={snapshot.marketId} meta={`${snapshot.activeBuyerCount} active / avg max ${formatCurrency(snapshot.averageBuyerMaxPrice)} / velocity ${snapshot.buyerResponseVelocity}`} right={<Pill tone={snapshot.demandConfidence >= 70 ? "green" : "gold"}>{snapshot.demandConfidence}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}

