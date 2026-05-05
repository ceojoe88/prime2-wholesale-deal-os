import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  autoExecutionAttempts,
  autoExecutionBlockedAttempts,
  autoExecutionMockSentAttempts
} from "@/lib/demo-data";

export default function AutoExecutionAttemptsPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="V13 Attempts" title="Controlled execution attempts" description="Each attempt records the rule, template, source, recipient count, V5 gate status, provider readiness, idempotency, and audit status." />
      <div className="metric-grid">
        <MetricCard label="Attempts" value={String(autoExecutionAttempts.length)} detail="All V13 attempts" />
        <MetricCard label="Mock-sent" value={String(autoExecutionMockSentAttempts.length)} detail="Provider mode mock/dry-run" />
        <MetricCard label="Blocked" value={String(autoExecutionBlockedAttempts.length)} detail="No provider calls" />
        <MetricCard label="Bulk sends" value="0" detail="Single recipient only" />
      </div>
      <Section title="Attempt Ledger">
        <table className="data-table">
          <thead><tr><th>Attempt</th><th>Action</th><th>Source</th><th>Recipients</th><th>Status</th><th>V5 Gates</th><th>Provider</th><th>Blocks</th></tr></thead>
          <tbody>
            {autoExecutionAttempts.map((attempt) => (
              <tr key={attempt.id}>
                <td>{attempt.id}<div className="record-meta">{attempt.idempotencyKey}</div></td>
                <td>{attempt.actionType}</td>
                <td>{attempt.sourceRecordType}:{attempt.sourceRecordId}</td>
                <td>{attempt.recipientCount}</td>
                <td><Pill tone={attempt.attemptStatus === "blocked" ? "red" : "green"}>{attempt.attemptStatus}</Pill></td>
                <td>{attempt.v5SafetyPassed && attempt.v5DryRunReceiptExists && attempt.v5ApprovalRecorded ? "passed" : "n/a or blocked"}</td>
                <td><Pill tone={attempt.providerCalled ? "green" : "red"}>{attempt.providerCalled ? attempt.providerMode : "not called"}</Pill></td>
                <td>{attempt.blockedReasons.length ? attempt.blockedReasons.join(", ") : "clear"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
      <Section title="Execution Limits">
        <div className="grid-three">
          <RecordCard title="Idempotency" meta="Repeat keys return replay and do not duplicate provider calls." right={<Pill tone="green">enforced</Pill>} />
          <RecordCard title="One recipient" meta="Recipient count must equal one." right={<Pill tone="red">hard cap</Pill>} />
          <RecordCard title="V5 gates" meta="Safety, dry-run, approval, live flags, and provider readiness must pass." right={<Pill tone="gold">required</Pill>} />
        </div>
      </Section>
    </div>
  );
}
