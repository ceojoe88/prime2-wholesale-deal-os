import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientCommunicationProviderProfiles } from "@/lib/demo-data";

export default function ClientCommandCommunicationProvidersPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP10 Providers" title="Communication Providers" description="Blocked by default unless compliance, plan, approval, and live flags pass." />
      <Section title="Provider Profiles">
        <div className="record-list">
          {clientCommunicationProviderProfiles.map((provider) => (
            <RecordCard
              key={provider.id}
              title={provider.providerName}
              meta={`${provider.clientSafeSummary} Mode: ${provider.providerMode}.`}
              right={<Pill tone={provider.enabled ? "green" : "red"}>{provider.channel}</Pill>}
            />
          ))}
        </div>
      </Section>
    </div>
  );
}
