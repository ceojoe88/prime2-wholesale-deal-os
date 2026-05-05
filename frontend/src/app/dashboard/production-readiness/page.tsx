import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  approvalUxReady,
  auditExportsReady,
  blockedProviderReadiness,
  failedEnvironmentChecks,
  failedHardeningChecks,
  productionReady,
  productionReadinessBlockedReasons,
  providerSandboxReadinessChecks
} from "@/lib/demo-data";

export default function ProductionReadinessPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V18 Production Readiness"
        title="Production readiness gate"
        description="Operator readiness, approvals, audit exports, safe attachments, backups, provider sandbox status, and deployment hardening are reviewed before any real-use exposure."
      />

      <div className="metric-grid">
        <MetricCard label="Production status" value={productionReady ? "ready" : "blocked"} detail="Auth, env, secrets, provider, and hardening gates" />
        <MetricCard label="Failed env checks" value={String(failedEnvironmentChecks.length)} detail="Auth, env, and secrets must pass" />
        <MetricCard label="Provider blockers" value={String(blockedProviderReadiness.length)} detail="Default mock/sandbox readiness" />
        <MetricCard label="Audit exports" value={String(auditExportsReady.length)} detail="Sanitized owner review packets" />
      </div>

      <Section title="Blocked Reasons">
        <div className="grid-three">
          {productionReadinessBlockedReasons.map((reason) => (
            <RecordCard key={reason} title={reason} meta="Prevents unsafe production readiness" right={<Pill tone="red">blocked</Pill>} />
          ))}
        </div>
      </Section>

      <div className="grid-two">
        <Section title="Approval UX">
          <div className="record-list">
            {approvalUxReady.map((review) => (
              <RecordCard key={review.id} title={review.approvalType} meta={review.contextSummary} right={<Pill tone="green">ready</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Provider Readiness">
          <div className="record-list">
            {providerSandboxReadinessChecks.map((provider) => (
              <RecordCard key={provider.id} title={provider.providerName} meta={provider.lastCheckedNotes} right={<Pill tone={provider.providerCallsAllowed ? "green" : "red"}>{provider.readinessStatus}</Pill>} />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Readiness Routes">
        <div className="grid-three">
          <RecordCard title="Audit Exports" meta="Sanitized export packet review" right={<Link href="/dashboard/audit-exports">Open</Link>} />
          <RecordCard title="Evidence Attachments" meta="Source-linked attachment metadata" right={<Link href="/dashboard/evidence-attachments">Open</Link>} />
          <RecordCard title="Provider Readiness" meta="Sandbox and gate checks" right={<Link href="/dashboard/provider-readiness">Open</Link>} />
          <RecordCard title="Backups" meta="Metadata-only backup exports" right={<Link href="/dashboard/backups">Open</Link>} />
          <RecordCard title="Hardening" meta={`${failedHardeningChecks.length} items still open`} right={<Pill tone="gold">review</Pill>} />
        </div>
      </Section>
    </div>
  );
}
