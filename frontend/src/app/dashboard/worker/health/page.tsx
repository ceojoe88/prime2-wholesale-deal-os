import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { workerHeartbeat } from "@/lib/demo-data";

export default function WorkerHealthPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V21 Worker Health"
        title="Heartbeat monitor"
        description="The worker heartbeat surfaces stuck jobs, retry needs, and safety status without opening any live-action path."
      />

      <div className="metric-grid">
        <MetricCard label="Status" value={workerHeartbeat.status} detail={workerHeartbeat.workerName} />
        <MetricCard label="Active" value={workerHeartbeat.active ? "yes" : "no"} detail="Heartbeat present" />
        <MetricCard label="Stuck jobs" value={String(workerHeartbeat.stuckJobsDetected)} detail="Detected by age threshold" />
        <MetricCard label="Recovery" value={workerHeartbeat.recoveryRecommended ? "needed" : "clear"} detail="Retry manager watches failures" />
      </div>

      <Section title="Safety State">
        <div className="grid-three">
          {["live outreach", "contract execution", "title submission", "portal publishing", "payment handling", "bulk send"].map((item) => (
            <RecordCard key={item} title={item} meta="Unavailable to worker runtime" right={<Pill tone="red">off</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}

