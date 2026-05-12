import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientPilotHealthSnapshots } from "@/lib/demo-data";

export default function ClientCommandPilotBlockedPage() {
  const blocked = clientPilotHealthSnapshots.filter((item) => item.healthStatus === "blocked");

  return (
    <div className="page">
      <PageHeader eyebrow="CP12 Blocked" title="Blocked Pilot Workspaces" description="Pilot mode does not bypass source gates." />
      <Section title="Blocked Workspaces">
        <div className="record-list">
          {blocked.map((item) => (
            <RecordCard key={item.id} title={item.healthStatus} meta={item.blockReasons.join(", ")} right={<Pill tone="red">{item.workspaceId}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
