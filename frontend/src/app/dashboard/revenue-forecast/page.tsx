import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  forecastSafetyCards,
  formatCurrency,
  likely10kDealProbabilities,
  marketEnrichmentRanking,
  pipelineProbabilityAdjustedRevenue,
  pipelineProjectedMonthlyRevenue,
  pipelineRevenueAtRisk,
  revenueForecastRecords
} from "@/lib/demo-data";

export default function RevenueForecastPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V16 Revenue Forecast"
        title="Pipeline revenue forecast"
        description="Forecast assignment revenue using evidence, buyer demand, market heat, conversion probability, title readiness, blocker severity, POF strength, and verified or pending assignment fees."
      />

      <div className="metric-grid">
        <MetricCard label="Projected monthly" value={formatCurrency(pipelineProjectedMonthlyRevenue)} detail="Estimate only across forecast periods" />
        <MetricCard label="Probability-adjusted" value={formatCurrency(pipelineProbabilityAdjustedRevenue)} detail="Weighted by deal probability" />
        <MetricCard label="Revenue at risk" value={formatCurrency(pipelineRevenueAtRisk)} detail="Behind blockers or lower confidence" />
        <MetricCard label="Likely 10K+ deals" value={String(likely10kDealProbabilities.length)} detail="Source-backed probability records" />
      </div>

      <Section title="Forecast Guardrails">
        <div className="grid-three">
          {forecastSafetyCards.map((card) => (
            <RecordCard key={card.label} title={card.label} meta={card.detail} right={<Pill tone={card.label === "Revenue at risk" ? "gold" : "green"}>{card.value}</Pill>} />
          ))}
        </div>
      </Section>

      <Section title="Market Confidence Basis">
        <div className="grid-three">
          {marketEnrichmentRanking.slice(0, 3).map((market) => (
            <RecordCard key={market.marketId} title={market.zipCode} meta={`${market.city} / confidence ${market.confidenceScore} / heat ${market.marketHeatScore}`} right={<Pill tone={market.confidenceScore >= 70 ? "green" : "gold"}>estimate</Pill>} />
          ))}
        </div>
      </Section>

      <Section title="Forecast Records">
        <table className="data-table">
          <thead>
            <tr>
              <th>Period</th>
              <th>Projected</th>
              <th>Verified</th>
              <th>Adjusted</th>
              <th>Window</th>
              <th>Confidence</th>
            </tr>
          </thead>
          <tbody>
            {revenueForecastRecords.map((forecast) => (
              <tr key={forecast.id}>
                <td><Link href={`/dashboard/revenue-forecast/${forecast.id}`}>{forecast.forecastPeriod}</Link><div className="record-meta">{forecast.estimateLabel}</div></td>
                <td>{formatCurrency(forecast.projectedAssignmentFees)}</td>
                <td>{formatCurrency(forecast.verifiedAssignmentFees)}</td>
                <td>{formatCurrency(forecast.probabilityAdjustedRevenue)}</td>
                <td>{forecast.expectedCloseWindow}</td>
                <td><Pill tone={forecast.confidenceLevel.includes("high") ? "green" : "gold"}>{forecast.confidenceLevel}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
