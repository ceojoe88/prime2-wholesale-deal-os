import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientPilotPrograms } from "@/lib/demo-data";

export default function ClientCommandPilotProgramsPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP12 Programs" title="Pilot Programs" description="Pilot mode does not bypass source gates." />
      <Section title="Programs">
        <div className="record-list">
          {clientPilotPrograms.map((program) => (
            <RecordCard key={program.id} title={program.programName} meta={program.clientSafeSummary} right={<Pill tone="green">{program.programStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
