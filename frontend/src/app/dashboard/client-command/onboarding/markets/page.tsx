import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientMarketSetups } from "@/lib/demo-data";

export default function ClientCommandOnboardingMarketsPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP8 Markets" title="Market Setup" description="Configured market coverage for the client workspace. No live provider data is used here." />
      <Section title="Market Setup Card">
        <div className="record-list">
          {clientMarketSetups.map((market) => (
            <RecordCard key={market.id} title={market.marketName} meta={`${market.counties.join(", ")} | ${market.zipCodes.join(", ")}`} right={<Pill tone="green">{market.marketStatus}</Pill>}>
              <p>{market.marketNotesSummary}</p>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}
