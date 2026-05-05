import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { workerJobLogs, workerJobs } from "@/lib/demo-data";

export default function WorkerJobsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V21 Worker Jobs"
        title="Queue and attempt ledger"
        description="Jobs are idempotent, retryable, and limited to prep, scheduling, routing, drafts, and escalation work."
      />

      <div className="metric-grid">
        <MetricCard label="Queue depth" value={String(workerJobs.length)} detail="Seeded runtime jobs" />
        <MetricCard label="Logs" value={String(workerJobLogs.length)} detail="Attempt ledger entries" />
        <MetricCard label="Provider calls" value="0" detail="No worker provider sends" />
        <MetricCard label="Idempotency" value="on" detail="Duplicate jobs blocked" />
      </div>

      <Section title="Worker Jobs">
        <table className="data-table">
          <thead>
            <tr>
              <th>Job</th>
              <th>Type</th>
              <th>Source</th>
              <th>Attempts</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {workerJobs.map((job) => (
              <tr key={job.id}>
                <td>{job.jobId}<div className="record-meta">{job.idempotencyKey}</div></td>
                <td>{job.jobType}</td>
                <td>{job.sourceRecord}</td>
                <td>{job.attempts}</td>
                <td><Pill tone={job.status === "failed" ? "red" : job.status === "completed" ? "green" : "gold"}>{job.status}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>

      <Section title="Recent Logs">
        <table className="data-table">
          <thead>
            <tr>
              <th>Log</th>
              <th>Job</th>
              <th>Event</th>
              <th>Provider</th>
            </tr>
          </thead>
          <tbody>
            {workerJobLogs.map((log) => (
              <tr key={log.id}>
                <td>{log.id}</td>
                <td>{log.jobId}</td>
                <td>{log.eventType}</td>
                <td><Pill tone={log.providerCalled ? "red" : "green"}>{log.providerCalled ? "called" : "none"}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}

