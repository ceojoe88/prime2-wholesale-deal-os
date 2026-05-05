import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  fieldTestingAccuracy,
  pendingScoringAdjustments,
  predictionFeedbackRecords,
  predictionMisses
} from "@/lib/demo-data";

export default function FeedbackLoopPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V19 Prediction Feedback"
        title="Prediction versus reality"
        description="Prime 2 compares predicted motivation, contactability, 10K+ opportunity, buyer demand, and contract readiness against real field outcomes using deterministic explanations."
      />

      <div className="metric-grid">
        <MetricCard label="Feedback records" value={String(predictionFeedbackRecords.length)} detail="Source prediction versus actual" />
        <MetricCard label="Accuracy" value={`${fieldTestingAccuracy}%`} detail="Current field sample set" />
        <MetricCard label="Prediction misses" value={String(predictionMisses.length)} detail="Needs scoring review" />
        <MetricCard label="Adjustments" value={String(pendingScoringAdjustments.length)} detail="Owner review required" />
      </div>

      <Section title="Feedback Records">
        <div className="record-list">
          {predictionFeedbackRecords.map((record) => (
            <RecordCard
              key={record.id}
              title={record.sourcePredictionType}
              meta={`${record.sourcePredictionValue} -> ${record.actualResult}`}
              right={<Link href={`/dashboard/feedback-loop/${record.id}`}>{record.accuracyScore}%</Link>}
            />
          ))}
        </div>
      </Section>

      <Section title="Prediction Misses">
        <div className="grid-three">
          {predictionMisses.map((record) => (
            <RecordCard key={record.id} title={record.varianceReason} meta={record.recommendedScoringAdjustment} right={<Pill tone="gold">review</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
