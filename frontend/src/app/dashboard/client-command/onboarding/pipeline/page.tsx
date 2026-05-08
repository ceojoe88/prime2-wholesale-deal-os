import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientPipelineSetups, clientPipelineStageTemplates, getClientPipelineSetup } from "@/lib/demo-data";

export default function ClientCommandOnboardingPipelinePage() {
  const pipeline = getClientPipelineSetup();
  return (
    <div className="page">
      <PageHeader eyebrow="CP8 Pipeline" title="Pipeline Setup" description="Default full-deal-loop stages with manager ownership for controlled/manual Prime2 operation." />
      <Section title="Pipeline Setup Card">
        <div className="grid-two">
          <RecordCard title={pipeline?.pipelineName ?? "Prime2 Full Deal Loop"} meta={pipeline?.clientSafeSummary ?? "Create Pipeline"} right={<Pill tone="green">{pipeline?.setupStatus ?? "draft"}</Pill>} />
          <RecordCard title="Stage count" meta="Default full deal loop" right={<Pill tone="gold">{String(clientPipelineSetups[0]?.stageCount ?? 0)}</Pill>} />
        </div>
      </Section>
      <Section title="Pipeline Stages">
        <div className="record-list">
          {clientPipelineStageTemplates.map((stage) => (
            <RecordCard key={stage.id} title={`${stage.stageOrder}. ${stage.stageName}`} meta={(stage.requiredBeforeNext ?? []).join(", ") || "No required predecessor"} right={<Pill tone="gold">{stage.managerOwner}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
