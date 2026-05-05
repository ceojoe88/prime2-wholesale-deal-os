import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { aiTemplates } from "@/lib/demo-data";

export default function AiTemplatesPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V20 AI Templates"
        title="Approved prompt library"
        description="AI output is routed through versioned templates that use system data only and cannot invent financial numbers."
      />

      <div className="metric-grid">
        <MetricCard label="Templates" value={String(aiTemplates.length)} detail="Active controlled prompts" />
        <MetricCard label="System data only" value="yes" detail="No invented ARV, repair, or margin numbers" />
        <MetricCard label="Numbers override" value="off" detail="Calculations remain system-owned" />
        <MetricCard label="Versioning" value="v20.1" detail="Template library baseline" />
      </div>

      <Section title="Template Library">
        <div className="grid-three">
          {aiTemplates.map((template) => (
            <RecordCard
              key={template.id}
              title={template.templateName}
              meta={`${template.requestType} / ${template.templateSections.join(", ")}`}
              right={<Pill tone={template.safetyStatus === "approved" ? "green" : "red"}>{template.templateVersion}</Pill>}
            />
          ))}
        </div>
      </Section>
    </div>
  );
}

