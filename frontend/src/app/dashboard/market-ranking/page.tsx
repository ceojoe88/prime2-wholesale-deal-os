import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { marketEnrichmentRanking, weakMarketWarnings } from "@/lib/demo-data";

export default function MarketRankingPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Market Ranking"
        title="Heat and weak-market warnings"
        description="Prime 2 ranks markets by demand, investor activity, lead quality, spread potential, competition, title friction, and evidence confidence."
      />
      <div className="grid-two">
        <Section title="Ranked Markets">
          <div className="record-list">
            {marketEnrichmentRanking.map((market, index) => (
              <RecordCard key={market.marketId} title={`${index + 1}. ${market.zipCode}`} meta={`${market.city} / confidence ${market.confidenceScore}`} right={<Link href={`/dashboard/market-enrichment/${market.marketId}`}><Pill tone={market.marketHeatScore >= 70 ? "green" : "gold"}>{market.marketHeatScore}</Pill></Link>} />
            ))}
          </div>
        </Section>
        <Section title="Weak-Market Warnings">
          <div className="record-list">
            {weakMarketWarnings.map((market) => (
              <RecordCard key={market.marketId} title={market.zipCode} meta="More comp, buyer, or source evidence needed before scaling." right={<Pill tone="gold">research</Pill>} />
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
