import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  bestLearningBuyerProfiles,
  bestLearningLeadTypes,
  bestLearningOfferStrategies,
  bestLearningZipCodes,
  buyerPofBottleneckCount,
  formatCurrency,
  lostOptimizationDeals,
  staleFollowUpPatterns,
  strong10kLearningProbability
} from "@/lib/demo-data";

export default function OptimizationPatternsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Pattern Detection"
        title="Explainable deal flow patterns"
        description="Deterministic pattern detection highlights best lead types, zip codes, buyer profiles, offer strategies, follow-up failures, POF bottlenecks, and deals dying before contract-ready."
      />

      <div className="metric-grid">
        <MetricCard label="Best zip" value={bestLearningZipCodes[0]?.value ?? "n/a"} detail="By success and verified fee evidence" />
        <MetricCard label="POF bottlenecks" value={String(buyerPofBottleneckCount)} detail="Buyer proof-of-funds blocks" />
        <MetricCard label="Stale follow-up" value={String(staleFollowUpPatterns.length)} detail="Patterns to tighten" />
        <MetricCard label="Strong 10K+" value={String(strong10kLearningProbability.length)} detail="High-confidence source-backed outcomes" />
      </div>

      <div className="grid-two">
        <Section title="Best Lead Types">
          <div className="record-list">
            {bestLearningLeadTypes.map((item) => (
              <RecordCard key={item.value} title={item.value} meta={`${item.recordCount} records / ${formatCurrency(item.verifiedAssignmentFee)} verified`} right={<Pill tone={item.successRate >= 50 ? "green" : "gold"}>{item.successRate}%</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Best Zip Codes">
          <div className="record-list">
            {bestLearningZipCodes.map((item) => (
              <RecordCard key={item.value} title={item.value} meta={`${item.recordCount} records / ${formatCurrency(item.projectedAssignmentFee)} projected`} right={<Pill tone={item.successRate >= 50 ? "green" : "gold"}>{item.successRate}%</Pill>} />
            ))}
          </div>
        </Section>
      </div>

      <div className="grid-two">
        <Section title="Buyer Profiles">
          <div className="record-list">
            {bestLearningBuyerProfiles.map((item) => (
              <RecordCard key={item.value} title={item.value} meta={`Sources: ${item.sourceRecordIds.join(", ")}`} right={<Pill>{item.successRate}%</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Offer Strategies">
          <div className="record-list">
            {bestLearningOfferStrategies.map((item) => (
              <RecordCard key={item.value} title={item.value} meta={`Verified ${formatCurrency(item.verifiedAssignmentFee)}`} right={<Pill>{item.successRate}%</Pill>} />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Deals Dying Before Contract-Ready">
        <div className="record-list">
          {lostOptimizationDeals.map((record) => (
            <RecordCard key={record.id} title={`${record.id} / ${record.conversionResult}`} meta={record.blockers.join(", ") || record.lostReason} right={<Pill tone="red">{record.confidenceScore}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
