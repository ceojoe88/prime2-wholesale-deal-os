import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";

export default function DocumentUploadPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Document Intake"
        title="Metadata and text review intake"
        description="Document intake supports manual metadata, pasted text extraction, and storage-reference placeholders while keeping file content internal and review-only."
      />
      <div className="metric-grid">
        <MetricCard label="Binary upload" value="placeholder" detail="Metadata path only" />
        <MetricCard label="Portal visibility" value="off" detail="No document intake auto-publishes" />
        <MetricCard label="Review state" value="owner queue" detail="Prime 2 routes issues" />
        <MetricCard label="External review" value="reminder" detail="Qualified review stays outside the app" />
      </div>
      <Section title="Intake Fields">
        <div className="grid-three">
          <RecordCard title="Document type" meta="Purchase, assignment, POF, title, seller, buyer, repairs, comps, or other" right={<Pill>required</Pill>} />
          <RecordCard title="Source linkage" meta="Deal, lead, buyer, and evidence packet references" right={<Pill>required</Pill>} />
          <RecordCard title="Pasted text" meta="Used for deterministic extraction and never shown externally" right={<Pill tone="gold">internal</Pill>} />
        </div>
      </Section>
    </div>
  );
}

