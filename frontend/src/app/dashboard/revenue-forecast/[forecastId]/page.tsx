import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  dealProbabilityRecords,
  formatCurrency,
  getDeal,
  getLead,
  getRevenueForecast,
  revenueForecastRecords
} from "@/lib/demo-data";

export function generateStaticParams() {
  return revenueForecastRecords.map((forecast) => ({ forecastId: forecast.id }));
}

export default async function RevenueForecastDetailPage({
  params
}: {
  params: Promise<{ forecastId: string }>;
}) {
  const { forecastId } = await params;
  const forecast = getRevenueForecast(forecastId);
  if (!forecast) notFound();

  return (
    <div className="page">
      <PageHeader
        eyebrow={forecast.confidenceLevel}
        title={`${forecast.forecastPeriod} forecast`}
        description="Forecast detail is estimate-only and tied to source records. It does not guarantee profit, revenue, close timing, or ROI."
      />

      <div className="metric-grid">
        <MetricCard label="Conservative" value={formatCurrency(forecast.conservativeForecast)} detail="Lower scenario estimate" />
        <MetricCard label="Base" value={formatCurrency(forecast.baseForecast)} detail="Probability-adjusted scenario" />
        <MetricCard label="Aggressive" value={formatCurrency(forecast.aggressiveForecast)} detail="Upper scenario estimate" />
        <MetricCard label="At-risk deals" value={String(forecast.dealsAtRisk.length)} detail="Blockers reduce confidence" />
      </div>

      <div className="grid-two">
        <Section title="Source Basis">
          <div className="record-list">
            {forecast.sourceBasis.map((source) => (
              <RecordCard key={source} title={source} meta="Forecast source reference" right={<Pill>source</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Deals At Risk">
          <div className="record-list">
            {forecast.dealsAtRisk.map((dealId) => {
              const deal = getDeal(dealId);
              const lead = deal ? getLead(deal.leadId) : undefined;
              return (
                <RecordCard key={dealId} title={dealId} meta={`${lead?.city ?? "Deal"} / ${lead?.propertyType ?? "property"}`} right={<Pill tone="gold">risk</Pill>} />
              );
            })}
          </div>
        </Section>
      </div>

      <Section title="Deal Probability Inputs">
        <table className="data-table">
          <thead>
            <tr>
              <th>Deal</th>
              <th>Probability</th>
              <th>Seller</th>
              <th>Buyer Demand</th>
              <th>POF</th>
              <th>Blockers</th>
            </tr>
          </thead>
          <tbody>
            {dealProbabilityRecords.map((record) => (
              <tr key={record.id}>
                <td>{record.dealId}</td>
                <td><Pill tone={record.probabilityScore >= 70 ? "green" : "gold"}>{record.probabilityScore}</Pill></td>
                <td>{record.sellerReadiness}</td>
                <td>{record.buyerDemand}</td>
                <td>{record.buyerPofStrength}</td>
                <td>{record.blockerSeverity}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
