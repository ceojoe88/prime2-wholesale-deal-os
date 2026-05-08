import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { getClientWorkspaceReadinessScore } from "@/lib/demo-data";

export default function ClientCommandOnboardingReadinessPage() {
  const score = getClientWorkspaceReadinessScore();
  return (
    <div className="page">
      <PageHeader eyebrow="CP8 Readiness" title="Workspace Readiness Score" description="Weighted readiness scoring for manual Prime2 operation only." />
      <Section title="Workspace Readiness Score Card">
        <div className="grid-two">
          <RecordCard title="Overall readiness" meta={score?.recommendedNextStep ?? "Calculate Readiness"} right={<Pill tone="green">{String(score?.readinessScore ?? 0)}</Pill>} />
          <RecordCard title="Manual-operation status" meta="Manual operation readiness only - no live communication, provider execution, billing, contracts, or campaigns are enabled." right={<Pill tone="gold">{score?.readinessStatus ?? "not_started"}</Pill>} />
          <RecordCard title="Setup subscores" meta={`Business ${score?.businessProfileScore ?? 0} | Market ${score?.marketSetupScore ?? 0} | Pipeline ${score?.pipelineSetupScore ?? 0}`} right={<Pill tone="gold">core</Pill>} />
          <RecordCard title="Execution subscores" meta={`Leads ${score?.leadImportScore ?? 0} | Buyers ${score?.buyerSetupScore ?? 0} | Compliance ${score?.complianceSetupScore ?? 0}`} right={<Pill tone="gold">ops</Pill>} />
        </div>
      </Section>
    </div>
  );
}
