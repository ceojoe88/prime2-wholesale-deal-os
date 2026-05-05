import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { blockedProviderReadiness, providerSandboxReadinessChecks } from "@/lib/demo-data";

export default function ProviderReadinessPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V18 Provider Sandbox Readiness"
        title="Provider readiness checks"
        description="Email, SMS, and title coordination adapters remain mock or blocked until sandbox readiness, safety checks, dry runs, owner approvals, idempotency, and audit trails are all present."
      />

      <div className="metric-grid">
        <MetricCard label="Providers" value={String(providerSandboxReadinessChecks.length)} detail="Email, SMS, title placeholder" />
        <MetricCard label="Blocked" value={String(blockedProviderReadiness.length)} detail="Default safe state" />
        <MetricCard label="Live flags enabled" value="0" detail="No real provider calls" />
        <MetricCard label="Bulk send" value="off" detail="Campaigns remain blocked" />
      </div>

      <Section title="Provider Checks">
        <div className="record-list">
          {providerSandboxReadinessChecks.map((provider) => (
            <RecordCard
              key={provider.id}
              title={provider.providerName}
              meta={`${provider.mode} / ${provider.lastCheckedNotes}`}
              right={<Pill tone={provider.providerCallsAllowed ? "green" : "red"}>{provider.readinessStatus}</Pill>}
            />
          ))}
        </div>
      </Section>

      <Section title="Required Gates">
        <table className="data-table">
          <thead>
            <tr>
              <th>Provider</th>
              <th>Sandbox</th>
              <th>Secrets</th>
              <th>Safety</th>
              <th>Dry Run</th>
              <th>Owner</th>
            </tr>
          </thead>
          <tbody>
            {providerSandboxReadinessChecks.map((provider) => (
              <tr key={provider.id}>
                <td>{provider.providerType}</td>
                <td>{provider.sandboxReady ? "ready" : "missing"}</td>
                <td>{provider.secretsConfigured ? "configured" : "missing"}</td>
                <td>{provider.safetyCheckRequired ? "required" : "missing"}</td>
                <td>{provider.dryRunRequired ? "required" : "missing"}</td>
                <td>{provider.ownerApprovalRequired ? "required" : "missing"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
