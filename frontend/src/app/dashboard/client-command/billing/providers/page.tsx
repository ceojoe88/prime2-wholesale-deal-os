import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientBillingProviderProfiles } from "@/lib/demo-data";

export default function ClientCommandBillingProvidersPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP11 Providers" title="Billing Providers" description="Stripe/live provider execution is disabled by default." />
      <Section title="Provider Profiles">
        <div className="record-list">
          {clientBillingProviderProfiles.map((provider) => (
            <RecordCard
              key={provider.id}
              title={provider.providerName}
              meta={`${provider.clientSafeSummary} Mode: ${provider.providerMode}.`}
              right={<Pill tone={provider.enabled ? "green" : "red"}>{provider.providerMode}</Pill>}
            />
          ))}
        </div>
      </Section>
    </div>
  );
}
