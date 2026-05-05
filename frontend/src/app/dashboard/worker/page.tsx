import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  completedWorkerJobs,
  failedWorkerJobs,
  pendingWorkerJobs,
  workerHeartbeat,
  workerJobs
} from "@/lib/demo-data";

export default function WorkerRuntimePage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V21 Worker Runtime"
        title="Background autonomy engine"
        description="Prime 2 can schedule, queue, retry, and ledger internal prep jobs continuously while live outreach, title, contracts, portals, and payments remain blocked."
      />

      <div className="metric-grid">
        <MetricCard label="Jobs" value={String(workerJobs.length)} detail={`${pendingWorkerJobs.length} pending`} />
        <MetricCard label="Completed" value={String(completedWorkerJobs.length)} detail="Internal prep only" />
        <MetricCard label="Failed" value={String(failedWorkerJobs.length)} detail="Escalated for review" />
        <MetricCard label="Heartbeat" value={workerHeartbeat.status} detail="Worker monitor" />
      </div>

      <Section title="Scheduler Cadence">
        <div className="grid-three">
          <RecordCard title="Every 5 min" meta="Automation checks" right={<Pill>queued</Pill>} />
          <RecordCard title="Hourly" meta="Scoring refresh" right={<Pill>guarded</Pill>} />
          <RecordCard title="Daily" meta="Briefing and forecast" right={<Pill>internal</Pill>} />
        </div>
      </Section>

      <Section title="Worker Routes">
        <div className="grid-three">
          <RecordCard title="Jobs" meta="Queue, status, retries, idempotency" right={<Link href="/dashboard/worker/jobs">Open</Link>} />
          <RecordCard title="Health" meta="Heartbeat and stuck job detection" right={<Link href="/dashboard/worker/health">Open</Link>} />
        </div>
      </Section>
    </div>
  );
}

