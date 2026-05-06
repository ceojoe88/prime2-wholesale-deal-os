import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { primeMemoryItems } from "@/lib/demo-data";

export default function PrimeMemoryPatternsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Memory Patterns"
        title="Repeated lessons and risk patterns"
        description="Patterns are deterministic summaries of source-backed outcomes and do not rewrite scoring without owner approval."
      />
      <Section title="Detected Patterns">
        <div className="record-list">
          {primeMemoryItems.map((memory) => (
            <RecordCard key={memory.memoryId} title={memory.memoryType} meta={`${memory.summary} Evidence: ${memory.evidenceBasis.join(", ")}`} right={<Pill tone={memory.confidenceScore >= 80 ? "green" : "gold"}>{memory.confidenceScore}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}

