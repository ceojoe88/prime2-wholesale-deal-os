import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  getPredictionFeedback,
  predictionFeedbackRecords,
  scoringAdjustmentSuggestions
} from "@/lib/demo-data";

export function generateStaticParams() {
  return predictionFeedbackRecords.map((record) => ({ feedbackId: record.id }));
}

export default async function FeedbackDetailPage({
  params
}: {
  params: Promise<{ feedbackId: string }>;
}) {
  const { feedbackId } = await params;
  const feedback = getPredictionFeedback(feedbackId);
  if (!feedback) notFound();
  const adjustments = scoringAdjustmentSuggestions.filter((item) => item.feedbackId === feedback.id);

  return (
    <div className="page">
      <PageHeader
        eyebrow={feedback.varianceReason}
        title={feedback.id}
        description="Feedback detail shows the evidence-backed reason for an adjustment suggestion. No black-box scoring or guaranteed result language is used."
      />

      <div className="metric-grid">
        <MetricCard label="Accuracy" value={`${feedback.accuracyScore}%`} detail={feedback.sourcePredictionType} />
        <MetricCard label="Lead" value={feedback.leadId ?? "none"} detail="Source record" />
        <MetricCard label="Outcome" value={feedback.actualResult} detail={feedback.callOutcomeId ?? "manual"} />
        <MetricCard label="Owner reviewed" value={feedback.ownerReviewed ? "yes" : "no"} detail="Adjustment remains gated" />
      </div>

      <Section title="Adjustment Basis">
        <div className="record-list">
          <RecordCard title="Prediction" meta={feedback.sourcePredictionValue} />
          <RecordCard title="Actual" meta={feedback.actualResult} />
          <RecordCard title="Recommendation" meta={feedback.recommendedScoringAdjustment} right={<Pill tone="gold">review</Pill>} />
          <RecordCard title="Explanation" meta={feedback.adjustmentExplanation} />
        </div>
      </Section>

      <Section title="Scoring Suggestions">
        <div className="grid-three">
          {adjustments.map((item) => (
            <RecordCard key={item.id} title={item.weightGroup} meta={`${item.currentWeight} -> ${item.recommendedWeight}`} right={<Pill>{item.ownerReviewStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
