import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { optimizationRecommendationsByImpact } from "@/lib/demo-data";

export default function OptimizationRecommendationsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Optimization Recommendations"
        title="Explainable improvement queue"
        description="Recommendations can focus markets, tune offer ranges, prioritize lead types, adjust follow-up timing, target buyer segments, avoid weak deal types, or improve scripts."
      />

      <div className="metric-grid">
        <MetricCard label="Recommendations" value={String(optimizationRecommendationsByImpact.length)} detail="Every item references source records" />
        <MetricCard label="Owner review" value={String(optimizationRecommendationsByImpact.filter((item) => item.ownerReviewStatus !== "reviewed").length)} detail="No autonomous spend or strategy changes" />
        <MetricCard label="Revenue guarantees" value="off" detail="Estimates only; no guaranteed profit" />
        <MetricCard label="Unsupported ROI" value="off" detail="Blocked by safety guard" />
      </div>

      <Section title="Recommendation Queue">
        <div className="record-list">
          {optimizationRecommendationsByImpact.map((recommendation) => (
            <RecordCard
              key={recommendation.id}
              title={`${recommendation.recommendationType}: ${recommendation.target}`}
              meta={recommendation.recommendation}
              right={<Pill tone={recommendation.impactScore >= 85 ? "green" : "gold"}>{recommendation.impactScore}</Pill>}
            >
              <div className="stack">
                <span>{recommendation.explanation}</span>
                <span className="record-meta">Source records: {recommendation.sourceRecordIds.join(", ")}</span>
              </div>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}
