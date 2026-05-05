import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { aiAuditRecords } from "@/lib/demo-data";

export default function AiAuditPage() {
  const blocked = aiAuditRecords.filter((record) => record.safetyStatus === "blocked");

  return (
    <div className="page">
      <PageHeader
        eyebrow="V20 AI Audit"
        title="AI safety audit trail"
        description="Every AI request records request type, safety outcome, blocked reason, cost estimate, provider mode, and response hash."
      />

      <div className="metric-grid">
        <MetricCard label="Audit records" value={String(aiAuditRecords.length)} detail="Immutable review entries" />
        <MetricCard label="Blocked" value={String(blocked.length)} detail="Rejected before release" />
        <MetricCard label="Provider calls" value="0" detail="Mock mode only" />
        <MetricCard label="Owner safety" value="on" detail="High-risk output stays blocked" />
      </div>

      <Section title="Audit Records">
        <table className="data-table">
          <thead>
            <tr>
              <th>Audit</th>
              <th>Request</th>
              <th>Event</th>
              <th>Status</th>
              <th>Provider</th>
            </tr>
          </thead>
          <tbody>
            {aiAuditRecords.map((record) => (
              <tr key={record.id}>
                <td>{record.id}</td>
                <td>{record.requestId}</td>
                <td>{record.eventType}</td>
                <td><Pill tone={record.safetyStatus === "blocked" ? "red" : "green"}>{record.safetyStatus}</Pill></td>
                <td>{record.providerMode}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}

