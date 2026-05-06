import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  buyerActivitySnapshots,
  comparableSaleRecords,
  marketEnrichmentRanking,
  marketProfiles,
  rentEstimateRecords,
  weakMarketWarnings
} from "@/lib/demo-data";

export default function MarketEnrichmentPage() {
  const topMarket = marketEnrichmentRanking[0];
  return (
    <div className="page">
      <PageHeader
        eyebrow="V26 Market Data Enrichment"
        title="Market truth and confidence"
        description="Prime 2 enriches zip-level strategy with manual or imported comps, rents, buyer activity, title friction, lead source evidence, and confidence scoring."
      />

      <div className="metric-grid">
        <MetricCard label="Markets" value={String(marketProfiles.length)} detail="Manual/imported evidence only" />
        <MetricCard label="Top market" value={topMarket.zipCode} detail={`${topMarket.marketHeatScore} heat score`} />
        <MetricCard label="Comp records" value={String(comparableSaleRecords.length)} detail="Recency and distance weighted" />
        <MetricCard label="Weak warnings" value={String(weakMarketWarnings.length)} detail="Missing or thin evidence" />
      </div>

      <Section title="Market Profiles">
        <div className="record-list">
          {marketEnrichmentRanking.map((market) => (
            <RecordCard
              key={market.marketId}
              title={`${market.city}, ${market.state} ${market.zipCode}`}
              meta={`${market.marketType} / ${market.evidenceBasis.length} source records`}
              right={<Link href={`/dashboard/market-enrichment/${market.marketId}`}><Pill tone={market.marketHeatScore >= 70 ? "green" : "gold"}>{market.marketHeatScore}</Pill></Link>}
            />
          ))}
        </div>
      </Section>

      <Section title="Work Areas">
        <div className="grid-three">
          <RecordCard title="Comps" meta={`${comparableSaleRecords.length} pricing evidence records`} right={<Link href="/dashboard/comps">Open</Link>} />
          <RecordCard title="Rent estimates" meta={`${rentEstimateRecords.length} rent range records`} right={<Link href="/dashboard/rent-estimates">Open</Link>} />
          <RecordCard title="Buyer activity" meta={`${buyerActivitySnapshots.length} demand snapshots`} right={<Link href="/dashboard/buyer-activity">Open</Link>} />
          <RecordCard title="Lead source ROI" meta="Estimate-only source quality" right={<Link href="/dashboard/lead-source-roi">Open</Link>} />
          <RecordCard title="Market ranking" meta="Heat and weak-market warnings" right={<Link href="/dashboard/market-ranking">Open</Link>} />
          <RecordCard title="Boundary" meta="No paid external data calls in this phase" right={<Pill tone="gold">manual</Pill>} />
        </div>
      </Section>
    </div>
  );
}

