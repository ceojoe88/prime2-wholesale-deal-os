import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  agentPerformanceByScore,
  buyerPofBottleneckCount,
  formatCurrency,
  missingLearningEvidence,
  optimizationRecommendationsByImpact,
  optimizationSafetyCards,
  outcomeLearningRecords,
  scoringWeightChanges,
  strong10kLearningProbability
} from "@/lib/demo-data";

export default function OptimizationPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V15 Deal Flow Optimization"
        title="Optimization learning engine"
        description="Study which sources, markets, sellers, buyers, offers, and follow-ups create contract momentum and 10K+ assignment opportunities using source-backed deterministic scoring."
      />

      <div className="metric-grid">
        <MetricCard label="Learning records" value={String(outcomeLearningRecords.length)} detail="Closed, lost, blocked, and contract-ready outcomes" />
        <MetricCard label="10K+ probability" value={String(strong10kLearningProbability.length)} detail="Source-backed high-confidence records" />
        <MetricCard label="POF bottlenecks" value={String(buyerPofBottleneckCount)} detail="Buyer proof-of-funds stalls" />
        <MetricCard label="Weight changes" value={String(scoringWeightChanges.length)} detail="Explainable scoring updates logged" />
      </div>

      <Section title="Safety And Evidence">
        <div className="grid-three">
          {optimizationSafetyCards.map((card) => (
            <RecordCard
              key={card.label}
              title={card.label}
              meta={card.detail}
              right={<Pill tone={card.label === "Missing evidence" && card.value !== "0" ? "red" : "green"}>{card.value}</Pill>}
            />
          ))}
        </div>
      </Section>

      <div className="grid-two">
        <Section title="Top Recommendations">
          <div className="record-list">
            {optimizationRecommendationsByImpact.map((recommendation) => (
              <RecordCard
                key={recommendation.id}
                title={recommendation.target}
                meta={recommendation.recommendation}
                right={<Pill tone={recommendation.impactScore >= 85 ? "green" : "gold"}>{recommendation.impactScore}</Pill>}
              />
            ))}
          </div>
        </Section>
        <Section title="Agent Performance">
          <div className="record-list">
            {agentPerformanceByScore.slice(0, 5).map((score) => (
              <RecordCard
                key={score.id}
                title={score.divisionName}
                meta={score.explanation}
                right={<Pill tone={score.overallScore >= 85 ? "green" : "gold"}>{score.overallScore}</Pill>}
              />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Optimization Routes">
        <div className="grid-three">
          <RecordCard title="Patterns" meta="Best lead types, zips, buyers, and offer strategies" right={<Link href="/dashboard/optimization/patterns">Open</Link>} />
          <RecordCard title="Recommendations" meta="Explainable improvement queue" right={<Link href="/dashboard/optimization/recommendations">Open</Link>} />
          <RecordCard title="Agent Performance" meta="Division scoring" right={<Link href="/dashboard/optimization/agent-performance">Open</Link>} />
          <RecordCard title="Lost Deals" meta={`${missingLearningEvidence.length} missing-evidence item tracked`} right={<Link href="/dashboard/optimization/lost-deals">Open</Link>} />
          <RecordCard title="Source Quality" meta={`${formatCurrency(strong10kLearningProbability.reduce((total, record) => total + record.projectedAssignmentFee, 0))} projected in strong records`} right={<Link href="/dashboard/optimization/source-quality">Open</Link>} />
        </div>
      </Section>
    </div>
  );
}
