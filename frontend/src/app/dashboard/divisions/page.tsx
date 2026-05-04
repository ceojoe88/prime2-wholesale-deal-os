import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { divisions, agents } from "@/lib/demo-data";

export default function DivisionsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Divisions"
        title="Operating divisions"
        description="Each division has a manager, workload, active recommendations, risk flags, and a next best action."
      />
      <div className="grid-three">
        {divisions.map((division) => {
          const agentCount = agents.filter((agent) => agent.divisionId === division.id).length;
          return (
            <RecordCard
              key={division.id}
              title={division.name}
              meta={`Manager: ${division.managerName}`}
              right={<Pill>{agentCount} agents</Pill>}
            >
              <span className="record-meta">{division.nextBestAction}</span>
              <div className="pill-row">
                <Pill tone="gold">{division.workload} workload</Pill>
                <Link className="pill green" href={`/dashboard/divisions/${division.id}`}>open</Link>
              </div>
            </RecordCard>
          );
        })}
      </div>
    </div>
  );
}
