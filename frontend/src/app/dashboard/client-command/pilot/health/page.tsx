import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientPilotHealthSnapshots } from "@/lib/demo-data";

export default function ClientCommandPilotHealthPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP12 Health" title="Pilot Health Snapshots" description="Controlled live posture requires CP9, CP10, and CP11 gates." />
      <Section title="Health Snapshots">
        <div className="record-list">
          {clientPilotHealthSnapshots.map((item) => (
            <RecordCard key={item.id} title={item.healthStatus} meta={`${item.clientSafeSummary} Blockers: ${item.blockReasons.join(", ")}.`} right={<Pill tone={item.healthStatus === "blocked" ? "red" : "gold"}>{item.planStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
