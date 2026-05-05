import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  blockedProviderAttempts,
  blockedProviderRegistries,
  providerAttemptAudits,
  providerCredentialPosture,
  providerRegistries,
  providerWebhookReviewQueue
} from "@/lib/demo-data";

export default function ProviderReadinessPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V22 Provider Sandbox Readiness"
        title="Provider sandbox and credential gate"
        description="Prime 2 tracks provider registry, env-only credential posture, sandbox separation, readiness outcomes, attempts, and webhook review queues without making real provider calls."
      />

      <div className="metric-grid">
        <MetricCard label="Registered" value={String(providerRegistries.length)} detail="OpenAI, email, SMS, storage" />
        <MetricCard label="Blocked" value={String(blockedProviderRegistries.length)} detail="Missing credentials or live gates" />
        <MetricCard label="Attempts" value={String(providerAttemptAudits.length)} detail={`${blockedProviderAttempts.length} blocked safely`} />
        <MetricCard label="Stored secrets" value={String(providerCredentialPosture.storedSecretValues)} detail="Reference names only" />
      </div>

      <Section title="Provider Registry">
        <div className="record-list">
          {providerRegistries.map((provider) => (
            <RecordCard
              key={provider.id}
              title={provider.providerName}
              meta={`${provider.providerType} / ${provider.providerMode} / credential ${provider.credentialReferenceMasked}`}
              right={<Link href={`/dashboard/provider-readiness/${provider.id}`}><Pill tone={provider.readinessStatus === "ready" ? "green" : "red"}>{provider.readinessStatus}</Pill></Link>}
            />
          ))}
        </div>
      </Section>

      <Section title="Readiness Work Areas">
        <div className="grid-three">
          <RecordCard title="Attempts" meta="Blocked, mock, sandbox-ready, and approval-pending attempts" right={<Link href="/dashboard/provider-readiness/attempts">Open</Link>} />
          <RecordCard title="Webhooks" meta={`${providerWebhookReviewQueue.length} mock or sandbox events queued for review`} right={<Link href="/dashboard/provider-readiness/webhooks">Open</Link>} />
          <RecordCard title="Credentials" meta="Env-only posture and masked references" right={<Link href="/dashboard/provider-readiness/credentials">Open</Link>} />
        </div>
      </Section>

      <Section title="Hard Boundary">
        <table className="data-table">
          <thead>
            <tr>
              <th>Control</th>
              <th>Status</th>
              <th>Reason</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Default mode</td><td>mock</td><td>No real provider network path is active</td></tr>
            <tr><td>Live provider calls</td><td>disabled</td><td>Owner approval, live flags, readiness, and audit are still required</td></tr>
            <tr><td>Credential values</td><td>not stored</td><td>Only masked environment reference names are displayed</td></tr>
          </tbody>
        </table>
      </Section>
    </div>
  );
}

