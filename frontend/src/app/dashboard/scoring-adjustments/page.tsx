import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { pendingScoringAdjustments, scoringAdjustmentSuggestions } from "@/lib/demo-data";

export default function ScoringAdjustmentsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V19 Scoring Adjustments"
        title="Explainable scoring adjustment queue"
        description="Field outcomes can suggest deterministic scoring changes, but owner review is required and no black-box learning is used."
      />

      <div className="metric-grid">
        <MetricCard label="Suggestions" value={String(scoringAdjustmentSuggestions.length)} detail="Evidence-backed adjustments" />
        <MetricCard label="Pending review" value={String(pendingScoringAdjustments.length)} detail="Owner-controlled" />
        <MetricCard label="Applied automatically" value="0" detail="No autonomous score-weight changes" />
        <MetricCard label="Black-box ML" value="none" detail="Deterministic explanations only" />
      </div>

      <Section title="Adjustment Queue">
        <div className="record-list">
          {scoringAdjustmentSuggestions.map((suggestion) => (
            <RecordCard
              key={suggestion.id}
              title={suggestion.weightGroup}
              meta={`${suggestion.currentWeight} -> ${suggestion.recommendedWeight} | ${suggestion.explanation}`}
              right={<Pill tone={suggestion.applied ? "green" : "gold"}>{suggestion.ownerReviewStatus}</Pill>}
            />
          ))}
        </div>
      </Section>
    </div>
  );
}
