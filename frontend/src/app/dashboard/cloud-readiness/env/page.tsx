import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { cloudEnvironmentChecks, failedCloudEnvironmentChecks } from "@/lib/demo-data";

export default function CloudReadinessEnvPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="Cloud Env" title="Environment validator" description="Prime 2 checks production env posture without exposing secret values or connection strings." />
      <div className="metric-grid">
        <MetricCard label="Checks" value={String(cloudEnvironmentChecks.length)} detail="Production profile" />
        <MetricCard label="Failed" value={String(failedCloudEnvironmentChecks.length)} detail="Fail-closed blockers" />
        <MetricCard label="Secrets exposed" value="0" detail="References only" />
        <MetricCard label="Provider flags" value="off" detail="Default cloud posture" />
      </div>
      <Section title="Environment Checks">
        <div className="record-list">
          {cloudEnvironmentChecks.map((check) => (
            <RecordCard key={check.id} title={check.checkName} meta={`${check.detail} ${check.remediation}`} right={<Pill tone={check.passed ? "green" : "red"}>{check.status}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
