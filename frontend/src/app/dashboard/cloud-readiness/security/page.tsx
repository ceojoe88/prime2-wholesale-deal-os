import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { cloudEnvironmentChecks, cloudProductionProfile, cloudReadinessBlockedReasons } from "@/lib/demo-data";

export default function CloudReadinessSecurityPage() {
  const securityChecks = cloudEnvironmentChecks.filter((check) => check.category === "security" || check.category === "secrets");
  return (
    <div className="page">
      <PageHeader eyebrow="Cloud Security" title="Private exposure security gate" description="Auth, CORS, debug mode, secret references, and provider flags must be safe before private cloud readiness can pass." />
      <div className="metric-grid">
        <MetricCard label="Profile" value={cloudProductionProfile.readinessStatus} detail="Production status" />
        <MetricCard label="Security checks" value={String(securityChecks.length)} detail="Required controls" />
        <MetricCard label="Secret values" value="masked" detail="Never stored or displayed" />
        <MetricCard label="Public launch" value="blocked" detail="Auth checklist required" />
      </div>
      <Section title="Security Controls">
        <div className="record-list">
          {securityChecks.map((check) => (
            <RecordCard key={check.id} title={check.checkName} meta={check.remediation} right={<Pill tone={check.passed ? "green" : "red"}>{check.status}</Pill>} />
          ))}
        </div>
      </Section>
      <Section title="Security Blockers">
        <div className="grid-three">
          {cloudReadinessBlockedReasons.map((reason) => (
            <RecordCard key={reason} title={reason} meta="Clear before private hosting" right={<Pill tone="red">blocked</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
