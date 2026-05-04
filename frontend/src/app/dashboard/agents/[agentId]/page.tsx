import { notFound } from "next/navigation";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { agents, getAgent, getDivision } from "@/lib/demo-data";

export function generateStaticParams() {
  return agents.map((agent) => ({ agentId: agent.id }));
}

export default function AgentDetailPage({ params }: { params: { agentId: string } }) {
  const agent = getAgent(params.agentId);
  if (!agent) notFound();
  const division = getDivision(agent.divisionId);
  return (
    <div className="page">
      <PageHeader eyebrow={division?.name ?? "Agent"} title={agent.name} description={agent.currentFocus} />
      <div className="metric-grid">
        <div className="metric-card"><span>Mode</span><strong>Draft</strong><small>No live execution</small></div>
        <div className="metric-card"><span>Escalation</span><strong>Prime</strong><small>Wholesale Prime review</small></div>
        <div className="metric-card"><span>Approval</span><strong>Owner</strong><small>Required for real action</small></div>
        <div className="metric-card"><span>Risk</span><strong>{agent.riskFlags.length}</strong><small>Current flags</small></div>
      </div>
      <div className="grid-two">
        <Section title="Allowed Work">
          <div className="pill-row">
            {["analyze", "score", "draft", "recommend", "escalate", "flag risk", "prepare checklist"].map((item) => (
              <Pill key={item} tone="green">{item}</Pill>
            ))}
          </div>
        </Section>
        <Section title="Blocked Work">
          <div className="record-list">
            {["send SMS", "send email", "call seller", "contact buyer", "execute contract", "give legal advice"].map((item) => (
              <RecordCard key={item} title={item} right={<Pill tone="red">blocked</Pill>} />
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
