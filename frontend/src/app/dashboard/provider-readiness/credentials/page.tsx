import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { providerCredentialPosture, providerRegistries } from "@/lib/demo-data";

export default function ProviderCredentialsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Credential Posture"
        title="Env-only provider references"
        description="Provider credentials are represented by masked environment reference names only. Raw values are never stored, rendered, audited, or seeded."
      />

      <div className="metric-grid">
        <MetricCard label="References" value={String(providerCredentialPosture.envOnlyReferences)} detail="Masked names" />
        <MetricCard label="Missing" value={String(providerCredentialPosture.missingCredentials)} detail="Expected until sandbox setup" />
        <MetricCard label="Stored values" value={String(providerCredentialPosture.storedSecretValues)} detail="Must remain zero" />
        <MetricCard label="Live enabled" value={String(providerCredentialPosture.liveEnabled)} detail="Live stays blocked" />
      </div>

      <Section title="Masked References">
        <table className="data-table">
          <thead>
            <tr>
              <th>Provider</th>
              <th>Source</th>
              <th>Reference</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {providerRegistries.map((provider) => (
              <tr key={provider.id}>
                <td>{provider.providerName}</td>
                <td>{provider.credentialSource}</td>
                <td>{provider.credentialReferenceMasked}</td>
                <td><Pill tone={provider.credentialPresent ? "green" : "red"}>{provider.credentialPresent ? "present" : "missing"}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>

      <Section title="Credential Safety">
        <div className="grid-three">
          <RecordCard title="Raw values" meta="Never stored or displayed" right={<Pill tone="green">zero</Pill>} />
          <RecordCard title="Logs" meta="Attempt logs keep metadata hashes only" right={<Pill tone="green">sanitized</Pill>} />
          <RecordCard title="Seed data" meta="Reference names only" right={<Pill tone="green">safe</Pill>} />
        </div>
      </Section>
    </div>
  );
}

