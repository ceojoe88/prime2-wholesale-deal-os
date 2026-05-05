import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { formatCurrency, lostOptimizationDeals, staleFollowUpPatterns } from "@/lib/demo-data";

export default function OptimizationLostDealsPage() {
  const lostFees = lostOptimizationDeals.reduce((total, record) => total + record.projectedAssignmentFee, 0);

  return (
    <div className="page">
      <PageHeader
        eyebrow="Lost And Blocked Deals"
        title="Deal leakage review"
        description="Identify deals dying before contract-ready, weak scripts, stale follow-up patterns, buyer POF bottlenecks, and avoidable blockers."
      />

      <div className="metric-grid">
        <MetricCard label="Lost/blocked/stalled" value={String(lostOptimizationDeals.length)} detail="Records needing pattern review" />
        <MetricCard label="Projected fee leakage" value={formatCurrency(lostFees)} detail="At-risk estimate from source records" />
        <MetricCard label="Stale follow-up" value={String(staleFollowUpPatterns.length)} detail="Timing pattern to improve" />
        <MetricCard label="Guaranteed recovery" value="off" detail="No guaranteed outcome claims" />
      </div>

      <Section title="Lost Deal Records">
        <div className="record-list">
          {lostOptimizationDeals.map((record) => (
            <RecordCard
              key={record.id}
              title={`${record.id} / ${record.market} / ${record.conversionResult}`}
              meta={record.lostReason || record.blockers.join(", ")}
              right={<Pill tone={record.sourceRecordsPresent ? "gold" : "red"}>{record.sourceRecordsPresent ? "supported" : "missing"}</Pill>}
            >
              <div className="stack">
                <span>Projected: {formatCurrency(record.projectedAssignmentFee)}</span>
                <span className="record-meta">Blockers: {record.blockers.join(", ") || "none"}</span>
              </div>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}
