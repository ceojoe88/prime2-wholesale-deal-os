import { notFound } from "next/navigation";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { agents, divisions, getDivision } from "@/lib/demo-data";

export function generateStaticParams() {
  return divisions.map((division) => ({ divisionId: division.id }));
}

export default function DivisionDetailPage({ params }: { params: { divisionId: string } }) {
  const division = getDivision(params.divisionId);
  if (!division) notFound();
  const divisionAgents = agents.filter((agent) => agent.divisionId === division.id);
  return (
    <div className="page">
      <PageHeader eyebrow="Division Manager" title={division.name} description={division.performanceNotes} />
      <div className="metric-grid">
        <div className="metric-card"><span>Manager</span><strong>{division.managerName}</strong><small>Accountable queue owner</small></div>
        <div className="metric-card"><span>Workload</span><strong>{division.workload}</strong><small>Active queued items</small></div>
        <div className="metric-card"><span>Agents</span><strong>{divisionAgents.length}</strong><small>Analysis-only expert team</small></div>
        <div className="metric-card"><span>Risk flags</span><strong>{division.riskFlags.length}</strong><small>Escalate before action</small></div>
      </div>
      <div className="grid-two">
        <Section title="Priority Queue">
          <div className="record-list">
            {division.priorityQueue.map((item) => <RecordCard key={item} title={item} right={<Pill tone="gold">queued</Pill>} />)}
          </div>
        </Section>
        <Section title="Expert Agents">
          <div className="record-list">
            {divisionAgents.map((agent) => <RecordCard key={agent.id} title={agent.name} meta={agent.recommendation} />)}
          </div>
        </Section>
      </div>
    </div>
  );
}
