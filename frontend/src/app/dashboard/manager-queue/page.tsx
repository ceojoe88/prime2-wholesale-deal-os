import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { divisions } from "@/lib/demo-data";

export default function ManagerQueuePage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Manager Queue"
        title="Active recommendations and risk"
        description="Queues are ranked for review, underwriting, compliance escalation, and draft-only seller or buyer preparation."
      />
      <Section title="Queue Board">
        <table className="data-table">
          <thead>
            <tr>
              <th>Manager</th>
              <th>Priority Queue</th>
              <th>Recommendation</th>
              <th>Risk</th>
              <th>Next</th>
            </tr>
          </thead>
          <tbody>
            {divisions.map((division) => (
              <tr key={division.id}>
                <td>{division.managerName}<div className="record-meta">{division.name}</div></td>
                <td>{division.priorityQueue.join(", ")}</td>
                <td>{division.activeRecommendations.join(" ")}</td>
                <td>{division.riskFlags.map((flag) => <Pill key={flag} tone="gold">{flag}</Pill>)}</td>
                <td>{division.nextBestAction}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
      <div className="grid-three">
        {divisions.slice(0, 3).map((division) => (
          <RecordCard key={division.id} title={division.priorityQueue[0]} meta={division.managerName} right={<Pill tone="gold">today</Pill>} />
        ))}
      </div>
    </div>
  );
}
