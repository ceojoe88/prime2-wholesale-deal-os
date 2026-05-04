import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  automationAttempts,
  blockedAutomationAttempts,
  schedulerRuns
} from "@/lib/demo-data";

export default function AutonomyRunsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V12 Scheduler Runtime"
        title="Run and attempt ledgers"
        description="Scheduler runs, idempotency keys, prepared attempts, and blocked real-world attempts are recorded for operator audit."
      />

      <div className="metric-grid">
        <MetricCard label="Runs" value={String(schedulerRuns.length)} detail="Seeded scheduler executions" />
        <MetricCard label="Attempts" value={String(automationAttempts.length)} detail="Prepared or blocked" />
        <MetricCard label="Blocked attempts" value={String(blockedAutomationAttempts.length)} detail="No provider calls" />
        <MetricCard label="Real actions" value="0" detail="None taken by autonomy" />
      </div>

      <Section title="Scheduler Runs">
        <table className="data-table">
          <thead>
            <tr>
              <th>Run</th>
              <th>Workflow</th>
              <th>Level</th>
              <th>Tasks</th>
              <th>Attempts</th>
              <th>Escalation</th>
              <th>Idempotency</th>
            </tr>
          </thead>
          <tbody>
            {schedulerRuns.map((run) => (
              <tr key={run.id}>
                <td>{run.id}<div className="record-meta">{run.runStatus}</div></td>
                <td>{run.workflowType}</td>
                <td><Pill tone={run.autonomyLevel === 4 ? "gold" : "green"}>L{run.autonomyLevel}</Pill></td>
                <td>{run.createdTasks}</td>
                <td>{run.createdAttempts}</td>
                <td><Pill tone={run.escalationCreated ? "red" : "green"}>{run.escalationCreated ? "created" : "none"}</Pill></td>
                <td>{run.idempotencyKey}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>

      <div className="grid-two">
        <Section title="Blocked Attempts">
          <div className="record-list">
            {blockedAutomationAttempts.map((attempt) => (
              <RecordCard key={attempt.id} title={attempt.actionType} meta={attempt.blockedReasons.join(", ")} right={<Pill tone="red">blocked</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Audit Controls">
          <div className="record-list">
            <RecordCard title="Idempotency" meta="One workflow key creates one run and prevents duplicate task creation." right={<Pill tone="green">enforced</Pill>} />
            <RecordCard title="Provider calls" meta="Blocked attempts record audit rows with providerCalled=false." right={<Pill tone="red">off</Pill>} />
            <RecordCard title="Real-world action" meta="Scheduler runs cannot send, publish, submit, execute, or collect." right={<Pill tone="red">blocked</Pill>} />
          </div>
        </Section>
      </div>
    </div>
  );
}
