import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientFeatureGateEvaluations,
  clientPlanAssignments,
  clientPlanFeatures,
  clientPlanUpgradeRecommendations
} from "@/lib/demo-data";

const workspaceId = "client-workspace-003";

export default function ClientCommandPlanFeaturesPage() {
  const assignment = clientPlanAssignments.find((item) => item.workspaceId === workspaceId);
  const features = clientPlanFeatures.filter((item) => item.planCode === assignment?.planCode);
  const gates = clientFeatureGateEvaluations.filter((item) => item.workspaceId === workspaceId);
  const recommendation = clientPlanUpgradeRecommendations.find((item) => item.workspaceId === workspaceId);

  return (
    <div className="page">
      <PageHeader
        eyebrow="CP9 Features"
        title="Plan Feature Gates"
        description="Feature visibility and plan-gated access for the assigned client workspace. This page stays in readiness and review mode only."
      />

      <Section title="Current Plan Features">
        <div className="record-list">
          {features.map((feature) => (
            <RecordCard
              key={feature.id}
              title={feature.featureName}
              meta={feature.featureSummary}
              right={<Pill tone={feature.allowed ? "green" : "gold"}>{feature.allowed ? "allowed" : "blocked"}</Pill>}
            />
          ))}
        </div>
      </Section>

      <Section title="Workspace Gate Evaluations">
        <div className="record-list">
          {gates.map((gate) => (
            <RecordCard
              key={gate.id}
              title={gate.featureKey}
              meta={gate.reasonSummary}
              right={<Pill tone={gate.gateStatus === "allowed" ? "green" : gate.gateStatus === "needs_review" ? "gold" : "red"}>{gate.gateStatus}</Pill>}
            >
              <p>{gate.requiredUpgradePlan ? `Recommended plan: ${gate.requiredUpgradePlan}` : "No plan upgrade is required for this feature gate."}</p>
            </RecordCard>
          ))}
        </div>
      </Section>

      <Section title="Upgrade Posture">
        <div className="grid-two">
          <RecordCard title="Upgrade Recommendation" meta={recommendation?.reasonSummary ?? "No upgrade recommendation recorded."} right={<Pill tone={recommendation ? "gold" : "green"}>{recommendation?.recommendedPlanCode ?? "clear"}</Pill>}>
            <p>{recommendation?.clientSafeSummary ?? "Feature access remains within the current plan posture."}</p>
          </RecordCard>
          <RecordCard title="Usage Pressure" meta="Signals that shape upgrade review" right={<Pill tone={recommendation?.usagePressure.length ? "gold" : "green"}>{recommendation?.usagePressure.length ?? 0}</Pill>}>
            <p>{recommendation?.usagePressure.join(", ") || "No active usage pressure is recorded."}</p>
          </RecordCard>
        </div>
      </Section>
    </div>
  );
}
