import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { cloudMonitoringSnapshot } from "@/lib/demo-data";

export default function CloudReadinessMonitoringPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="Cloud Monitoring" title="Monitoring readiness" description="Health, readiness, worker heartbeat, provider posture, cost-cap status, failed jobs, and blocked actions are summarized for private operations." />
      <div className="metric-grid">
        <MetricCard label="Health" value={cloudMonitoringSnapshot.healthStatus} detail="Backend health summary" />
        <MetricCard label="Readiness" value={cloudMonitoringSnapshot.readinessStatus} detail="Production gate result" />
        <MetricCard label="Worker" value={cloudMonitoringSnapshot.workerHeartbeatStatus} detail="Heartbeat monitor" />
        <MetricCard label="Blocked actions" value={String(cloudMonitoringSnapshot.blockedActionCount)} detail="Audit signal" />
      </div>
      <Section title="Monitoring Signals">
        <div className="grid-three">
          <RecordCard title="Provider readiness" meta={cloudMonitoringSnapshot.providerReadinessStatus} right={<Pill tone="red">review</Pill>} />
          <RecordCard title="AI cost cap" meta={cloudMonitoringSnapshot.aiCostCapStatus} right={<Pill tone="green">tracked</Pill>} />
          <RecordCard title="Failed jobs" meta={String(cloudMonitoringSnapshot.failedJobCount)} right={<Pill tone={cloudMonitoringSnapshot.failedJobCount ? "red" : "green"}>{cloudMonitoringSnapshot.failedJobCount}</Pill>} />
        </div>
      </Section>
    </div>
  );
}
