import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientPilotWorkspaceEnrollments } from "@/lib/demo-data";

export default function ClientCommandPilotEnrollmentsPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP12 Enrollments" title="Pilot Enrollments" description="Pilot mode does not bypass source gates." />
      <Section title="Workspace Enrollments">
        <div className="record-list">
          {clientPilotWorkspaceEnrollments.map((item) => (
            <RecordCard key={item.id} title={item.pilotMode} meta={item.clientSafeSummary} right={<Pill tone="green">{item.enrollmentStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
