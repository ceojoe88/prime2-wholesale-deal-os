import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientPilotLaunchChecklists } from "@/lib/demo-data";

export default function ClientCommandPilotLaunchChecklistPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP12 Launch Checklist" title="Pilot Launch Checklist" description="Pilot mode does not bypass source gates." />
      <Section title="Launch Checklists">
        <div className="record-list">
          {clientPilotLaunchChecklists.map((item) => (
            <RecordCard key={item.id} title={item.checklistStatus} meta={`${item.clientSafeSummary} Blockers: ${item.blockReasons.join(", ")}.`} right={<Pill tone={item.checklistStatus === "blocked" ? "red" : "green"}>{item.checklistStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
