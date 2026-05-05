import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { getProviderAttempts, getProviderRegistry, providerRegistries } from "@/lib/demo-data";

export function generateStaticParams() {
  return providerRegistries.map((provider) => ({ providerId: provider.id }));
}

export default async function ProviderReadinessDetailPage({
  params
}: {
  params: Promise<{ providerId: string }>;
}) {
  const { providerId } = await params;
  const provider = getProviderRegistry(providerId);
  if (!provider) notFound();
  const attempts = getProviderAttempts(provider.id);

  return (
    <div className="page">
      <PageHeader
        eyebrow={provider.providerType}
        title={provider.providerName}
        description={provider.notes}
      />

      <div className="metric-grid">
        <MetricCard label="Mode" value={provider.providerMode} detail="Mock by default" />
        <MetricCard label="Credential" value={provider.credentialPresent ? "present" : "missing"} detail={provider.credentialReferenceMasked} />
        <MetricCard label="Live flag" value={provider.liveEnabled ? "on" : "off"} detail="Owner-gated even when enabled" />
        <MetricCard label="Network calls" value={provider.liveNetworkCallAllowed ? "allowed" : "blocked"} detail="V22 is readiness only" />
      </div>

      <div className="grid-two">
        <Section title="Readiness">
          <div className="record-list">
            <RecordCard title="Enabled" meta={provider.enabled ? "Provider is registered" : "Provider disabled"} right={<Pill tone={provider.enabled ? "green" : "red"}>{provider.enabled ? "yes" : "no"}</Pill>} />
            <RecordCard title="Sandbox flag" meta={provider.sandboxEnabled ? "Sandbox use can be evaluated" : "Sandbox use blocked"} right={<Pill tone={provider.sandboxEnabled ? "green" : "red"}>{provider.sandboxEnabled ? "on" : "off"}</Pill>} />
            <RecordCard title="Readiness" meta={provider.blockedReason || "No blocking reason recorded"} right={<Pill tone={provider.readinessStatus === "ready" ? "green" : "red"}>{provider.readinessStatus}</Pill>} />
          </div>
        </Section>
        <Section title="Attempts">
          <div className="record-list">
            {attempts.map((attempt) => (
              <RecordCard key={attempt.id} title={attempt.actionType} meta={`${attempt.sourceDomain} / ${attempt.mode}`} right={<Pill tone={attempt.attemptStatus === "blocked" ? "red" : "green"}>{attempt.attemptStatus}</Pill>} />
            ))}
            {attempts.length === 0 ? <RecordCard title="No attempts" meta="No provider attempt has been recorded for this provider." /> : null}
          </div>
        </Section>
      </div>
    </div>
  );
}

