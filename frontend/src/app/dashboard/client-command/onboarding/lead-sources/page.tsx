import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientLeadSourceSetups } from "@/lib/demo-data";

export default function ClientCommandOnboardingLeadSourcesPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP8 Lead Sources" title="Lead Source Setup" description="Setup records for lead sources and tracking. Setup record only - no provider sync or campaign launch occurred." />
      <Section title="Lead Source Setup Card">
        <div className="record-list">
          {clientLeadSourceSetups.map((source) => (
            <RecordCard key={source.id} title={source.sourceName} meta={source.notesSummary} right={<Pill tone={source.sourceStatus === "active_manual" ? "green" : "gold"}>{source.sourceStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
