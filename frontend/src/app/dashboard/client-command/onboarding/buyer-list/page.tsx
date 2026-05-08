import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { getClientBuyerListSetup } from "@/lib/demo-data";

export default function ClientCommandOnboardingBuyerListPage() {
  const setup = getClientBuyerListSetup();
  return (
    <div className="page">
      <PageHeader eyebrow="CP8 Buyer List" title="Buyer List Setup" description="Buyer setup only - no buyer has been contacted." />
      <Section title="Buyer List Setup Card">
        <div className="grid-two">
          <RecordCard title="Buyer list readiness" meta={setup?.recommendedNextStep ?? "Review Buyer List Setup"} right={<Pill tone="green">{setup?.setupStatus ?? "not_started"}</Pill>} />
          <RecordCard title="Buyer counts" meta={`${setup?.buyerCount ?? 0} buyers | ${setup?.activeBuyerCount ?? 0} active | ${setup?.clearBuyBoxCount ?? 0} clear buy boxes`} right={<Pill tone="gold">{setup?.verifiedOrStatedFundingCount ?? 0} funded</Pill>} />
        </div>
      </Section>
    </div>
  );
}
