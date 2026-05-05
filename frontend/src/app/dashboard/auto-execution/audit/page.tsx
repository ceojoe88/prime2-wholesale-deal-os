import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { autoExecutionAuditTrail } from "@/lib/demo-data";

export default function AutoExecutionAuditPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="V13 Audit" title="Auto-execution audit trail" description="Every internal reminder, mock-send, and blocked attempt creates an audit record with source, outcome, reasons, provider-call status, and idempotency." />
      <div className="metric-grid">
        <MetricCard label="Audit records" value={String(autoExecutionAuditTrail.length)} detail="Attempt-level audit trail" />
        <MetricCard label="Provider calls" value={String(autoExecutionAuditTrail.filter((record) => record.providerCalled).length)} detail="Mock/dry-run mode only" />
        <MetricCard label="Blocked audits" value={String(autoExecutionAuditTrail.filter((record) => record.outcome === "blocked").length)} detail="Unsafe paths recorded" />
        <MetricCard label="Missing audit" value="0" detail="Seeded attempts audited" />
      </div>
      <Section title="Audit Records">
        <table className="data-table">
          <thead><tr><th>Audit</th><th>Attempt</th><th>Event</th><th>Source</th><th>Outcome</th><th>Provider</th><th>Blocks</th></tr></thead>
          <tbody>
            {autoExecutionAuditTrail.map((record) => (
              <tr key={record.id}>
                <td>{record.id}<div className="record-meta">{record.idempotencyKey}</div></td>
                <td>{record.attemptId}</td>
                <td>{record.eventType}</td>
                <td>{record.sourceRecordType}:{record.sourceRecordId}</td>
                <td><Pill tone={record.outcome === "blocked" ? "red" : "green"}>{record.outcome}</Pill></td>
                <td><Pill tone={record.providerCalled ? "green" : "red"}>{record.providerCalled ? "mock" : "none"}</Pill></td>
                <td>{record.blockedReasons.length ? record.blockedReasons.join(", ") : "clear"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
