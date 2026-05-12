import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientPlanUpgradeRecommendations } from "@/lib/demo-data";

export default function ClientCommandPlansUpgradeRecommendationsPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP9 Upgrade" title="Upgrade Recommendations" description="Feature access is controlled by plan, readiness, and safety gates." />
      <Section title="Recommendations">
        <div className="record-list">
          {clientPlanUpgradeRecommendations.map((recommendation) => (
            <RecordCard
              key={recommendation.id}
              title={`${recommendation.currentPlanCode} to ${recommendation.recommendedPlanCode}`}
              meta={recommendation.reasonSummary}
              right={<Pill tone="gold">{recommendation.recommendedPlanCode}</Pill>}
            >
              <div className="tag-row">
                {recommendation.blockedFeatures.map((feature) => (
                  <Pill key={feature} tone="red">{feature}</Pill>
                ))}
              </div>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}
