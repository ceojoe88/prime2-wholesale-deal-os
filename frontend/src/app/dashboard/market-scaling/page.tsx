import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { formatCurrency, marketRanking, marketScalingScores } from "@/lib/demo-data";

export default function MarketScalingPage() {
  const topMarket = marketRanking[0];

  return (
    <div className="page">
      <PageHeader
        eyebrow="V16 Market Scaling"
        title="Market and zip scaling score"
        description="Rank where to spend time based on lead volume, hot lead percentage, buyer demand, average spread, conversion rate, title/compliance friction, competition risk, and source evidence."
      />

      <div className="metric-grid">
        <MetricCard label="Markets scored" value={String(marketScalingScores.length)} detail="Zip-level scoring records" />
        <MetricCard label="Top market" value={topMarket?.marketZip ?? "n/a"} detail={`${topMarket?.recommendedSpendLevel ?? "n/a"} recommendation`} />
        <MetricCard label="Top score" value={String(topMarket?.scalingScore ?? 0)} detail="Estimate-only ranking" />
        <MetricCard label="Unsupported spend" value="off" detail="Spend requires evidence and owner review" />
      </div>

      <Section title="Market Ranking">
        <div className="record-list">
          {marketRanking.map((market) => (
            <RecordCard
              key={market.id}
              title={market.marketZip}
              meta={`Lead volume ${market.leadVolume}, demand ${market.buyerDemand}, average spread ${formatCurrency(market.averageSpread)}`}
              right={<Pill tone={market.scalingScore >= 70 ? "green" : market.scalingScore >= 60 ? "gold" : "red"}>{market.scalingScore}</Pill>}
            >
              <span className="record-meta">Recommendation: {market.recommendedSpendLevel}; source basis {market.sourceRecordIds.join(", ")}</span>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}
