import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  dealProbabilityRecords,
  forecastSafetyCards,
  formatCurrency,
  likely10kDealProbabilities,
  marketRanking,
  pipelineProbabilityAdjustedRevenue,
  pipelineProjectedMonthlyRevenue,
  pipelineRevenueAtRisk
} from "@/lib/demo-data";

export default function PipelineValuePage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V16 Pipeline Value"
        title="Pipeline value dashboard"
        description="Show projected monthly revenue, conservative/base/aggressive forecast context, 10K+ likely deals, revenue at risk, market ranking, spend recommendations, and evidence basis."
      />

      <div className="metric-grid">
        <MetricCard label="Projected" value={formatCurrency(pipelineProjectedMonthlyRevenue)} detail="Estimate-only projected assignment fees" />
        <MetricCard label="Adjusted" value={formatCurrency(pipelineProbabilityAdjustedRevenue)} detail="Probability-adjusted pipeline" />
        <MetricCard label="At risk" value={formatCurrency(pipelineRevenueAtRisk)} detail="Risk-adjusted gap" />
        <MetricCard label="10K+ likely" value={String(likely10kDealProbabilities.length)} detail="High probability source records" />
      </div>

      <Section title="Forecast Safety">
        <div className="grid-three">
          {forecastSafetyCards.map((card) => (
            <RecordCard key={card.label} title={card.label} meta={card.detail} right={<Pill tone={card.label === "Revenue at risk" ? "gold" : "green"}>{card.value}</Pill>} />
          ))}
        </div>
      </Section>

      <div className="grid-two">
        <Section title="Deal Probability">
          <div className="record-list">
            {dealProbabilityRecords.map((record) => (
              <RecordCard key={record.id} title={record.dealId} meta={`${record.probabilityBand}; sources ${record.sourceRecordIds.join(", ")}`} right={<Pill tone={record.probabilityScore >= 70 ? "green" : "gold"}>{record.probabilityScore}</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Market Ranking">
          <div className="record-list">
            {marketRanking.map((market) => (
              <RecordCard key={market.id} title={market.marketZip} meta={market.recommendedSpendLevel} right={<Pill>{market.scalingScore}</Pill>} />
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
