import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { autoExecutionDryRunBlocks, autoExecutionDryRuns } from "@/lib/demo-data";

export default function AutoExecutionDryRunsPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="V13 Dry-Runs" title="Auto-execution dry-run receipts" description="Dry-runs prove template hash, safety result, provider mode, source record, and idempotency before any controlled attempt." />
      <div className="metric-grid">
        <MetricCard label="Dry-runs" value={String(autoExecutionDryRuns.length)} detail="Receipt records" />
        <MetricCard label="Safety passed" value={String(autoExecutionDryRuns.filter((run) => run.safetyPassed).length)} detail="Clear receipts" />
        <MetricCard label="Blocked" value={String(autoExecutionDryRunBlocks.length)} detail="Safety review required" />
        <MetricCard label="Provider mode" value="mock" detail="Dry-run only" />
      </div>
      <Section title="Dry-Run Ledger">
        <table className="data-table">
          <thead><tr><th>Dry-run</th><th>Rule</th><th>Template</th><th>Source</th><th>Recipient</th><th>Safety</th><th>Mode</th></tr></thead>
          <tbody>
            {autoExecutionDryRuns.map((dryRun) => (
              <tr key={dryRun.id}>
                <td>{dryRun.id}<div className="record-meta">{dryRun.idempotencyKey}</div></td>
                <td>{dryRun.ruleId}</td>
                <td>{dryRun.templateId}</td>
                <td>{dryRun.sourceRecordType}:{dryRun.sourceRecordId}</td>
                <td>{dryRun.recipientType}</td>
                <td><Pill tone={dryRun.safetyPassed ? "green" : "red"}>{dryRun.riskStatus}</Pill></td>
                <td>{dryRun.providerMode}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
