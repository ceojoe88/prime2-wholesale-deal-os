import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  bestLearningLeadTypes,
  formatCurrency,
  missingLearningEvidence,
  outcomeLearningRecords,
  scoringWeightChanges
} from "@/lib/demo-data";

export default function OptimizationSourceQualityPage() {
  const supported = outcomeLearningRecords.length - missingLearningEvidence.length;

  return (
    <div className="page">
      <PageHeader
        eyebrow="Source Quality Feedback Loop"
        title="Source quality and weight changes"
        description="Closed, lost, blocked, and contract-ready outcomes update opportunity scoring, buyer ranking, follow-up priority, market heat, and source quality through logged deterministic weight changes."
      />

      <div className="metric-grid">
        <MetricCard label="Supported records" value={String(supported)} detail="Evidence-backed learning records" />
        <MetricCard label="Missing evidence" value={String(missingLearningEvidence.length)} detail="Blocked from confidence claims" />
        <MetricCard label="Weight changes" value={String(scoringWeightChanges.length)} detail="Logged and owner-reviewable" />
        <MetricCard label="Black-box scoring" value="off" detail="Every change explains source basis" />
      </div>

      <div className="grid-two">
        <Section title="Lead Source Quality">
          <div className="record-list">
            {bestLearningLeadTypes.map((item) => (
              <RecordCard key={item.value} title={item.value} meta={`${item.recordCount} records / ${formatCurrency(item.projectedAssignmentFee)} projected`} right={<Pill tone={item.successRate >= 50 ? "green" : "gold"}>{item.successRate}%</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Logged Weight Changes">
          <div className="record-list">
            {scoringWeightChanges.map((change) => (
              <RecordCard
                key={change.id}
                title={change.weightGroup}
                meta={change.reason}
                right={<Pill tone="gold">{change.previousWeight} to {change.newWeight}</Pill>}
              >
                <span className="record-meta">{change.explanation}</span>
              </RecordCard>
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
