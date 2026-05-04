import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { agents, getDivision } from "@/lib/demo-data";

export default function AgentsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Expert Teams"
        title="Analysis-only agent roster"
        description="Agents may analyze, score, draft, recommend, escalate, flag risk, and prepare checklists. Execution-like actions are blocked."
      />
      <div className="grid-three">
        {agents.map((agent) => (
          <RecordCard
            key={agent.id}
            title={agent.name}
            meta={getDivision(agent.divisionId)?.name}
            right={<Pill tone="green">active</Pill>}
          >
            <span className="record-meta">{agent.currentFocus}</span>
            <Link className="pill green" href={`/dashboard/agents/${agent.id}`}>open</Link>
          </RecordCard>
        ))}
      </div>
    </div>
  );
}
