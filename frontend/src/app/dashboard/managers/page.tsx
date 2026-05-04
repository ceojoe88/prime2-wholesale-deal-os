import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { divisions } from "@/lib/demo-data";

export default function ManagersPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Managers"
        title="Division manager roster"
        description="Manager-level accountability for responsibilities, priority queues, workload, recommendations, risk flags, and next best action."
      />
      <div className="grid-three">
        {divisions.map((division) => (
          <RecordCard
            key={division.id}
            title={division.managerName}
            meta={division.name}
            right={<Pill tone={division.riskFlags.length ? "gold" : "green"}>{division.workload} active</Pill>}
          >
            <span className="record-meta">{division.performanceNotes}</span>
            <div className="pill-row">
              {division.responsibilities.slice(0, 3).map((item) => <Pill key={item}>{item}</Pill>)}
            </div>
          </RecordCard>
        ))}
      </div>
    </div>
  );
}
