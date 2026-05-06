import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { scoringWeightRecommendations } from "@/lib/demo-data";

export default function ScoringWeightRecommendationsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Scoring Weight Recommendations"
        title="Owner-reviewed scoring changes"
        description="Prime 2 recommends explainable weight adjustments from evidence, but never applies them automatically."
      />
      <Section title="Recommendations">
        <div className="record-list">
          {scoringWeightRecommendations.map((recommendation) => (
            <RecordCard
              key={recommendation.recommendationId}
              title={recommendation.scoringArea}
              meta={`${recommendation.currentWeight} to ${recommendation.suggestedWeight} / ${recommendation.reason}`}
              right={<Pill tone={recommendation.riskStatus === "low" ? "green" : "gold"}>{recommendation.ownerApprovalStatus}</Pill>}
            />
          ))}
        </div>
      </Section>
    </div>
  );
}

