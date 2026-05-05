import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { callObjectionRecords } from "@/lib/demo-data";

export default function CallIntelligenceObjectionsPage() {
  const highRisk = callObjectionRecords.filter((objection) => objection.riskLevel === "high");

  return (
    <div className="page">
      <PageHeader
        eyebrow="Objection Intelligence"
        title="Seller objection queue"
        description="Objections produce safe response drafts, required data, risk levels, and next actions for owner review only."
      />

      <div className="metric-grid">
        <MetricCard label="Objections" value={String(callObjectionRecords.length)} detail="Structured from notes" />
        <MetricCard label="High risk" value={String(highRisk.length)} detail="Escalated before response" />
        <MetricCard label="Draft-only" value="100%" detail="No live response path" />
        <MetricCard label="Owner review" value="required" detail="Every response draft" />
      </div>

      <Section title="Objection Records">
        <div className="record-list">
          {callObjectionRecords.map((objection) => (
            <RecordCard key={objection.id} title={objection.objectionType} meta={objection.safeResponseDraft} right={<Pill tone={objection.riskLevel === "high" ? "red" : "gold"}>{objection.riskLevel}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
