import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  approvedPrimeMemoryContext,
  learningSignals,
  playbookRecommendations,
  primeMemoryItems,
  primeMemoryPatterns,
  scoringWeightRecommendations,
  topLearningInsights
} from "@/lib/demo-data";

export default function PrimeMemoryPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V27 Prime 2 Memory"
        title="Evidence-backed learning memory"
        description="Prime 2 stores sourced lessons about sellers, buyers, markets, documents, campaigns, and pricing so future recommendations stay explainable and auditable."
      />

      <div className="metric-grid">
        <MetricCard label="Memory items" value={String(primeMemoryItems.length)} detail="Source-cited records" />
        <MetricCard label="Approved context" value={String(approvedPrimeMemoryContext.length)} detail="AI context only" />
        <MetricCard label="Learning signals" value={String(learningSignals.length)} detail="Prediction versus outcome" />
        <MetricCard label="Weight recs" value={String(scoringWeightRecommendations.length)} detail="Owner review required" />
      </div>

      <Section title="Top Learning Insights">
        <div className="record-list">
          {topLearningInsights.map((memory) => (
            <RecordCard
              key={memory.memoryId}
              title={memory.summary}
              meta={`${memory.memoryType} / Evidence: ${memory.evidenceBasis.join(", ")}`}
              right={<Link href={`/dashboard/prime-memory/${memory.memoryId}`}><Pill tone="green">{memory.confidenceScore}</Pill></Link>}
            />
          ))}
        </div>
      </Section>

      <Section title="Pattern Counts">
        <div className="grid-three">
          <RecordCard title="Winning scripts" meta="Seller language that performed well" right={<Pill>{primeMemoryPatterns.winningScripts}</Pill>} />
          <RecordCard title="Weak sources" meta="Lead sources needing more proof" right={<Pill tone="gold">{primeMemoryPatterns.weakSources}</Pill>} />
          <RecordCard title="High-spread markets" meta="Market focus backed by deal evidence" right={<Pill>{primeMemoryPatterns.highSpreadMarkets}</Pill>} />
          <RecordCard title="Document patterns" meta="Review blockers to surface earlier" right={<Pill tone="gold">{primeMemoryPatterns.documentIssuePatterns}</Pill>} />
          <RecordCard title="Campaign patterns" meta="Approved playbook context" right={<Pill>{primeMemoryPatterns.campaignPatterns}</Pill>} />
          <RecordCard title="Playbooks" meta={`${playbookRecommendations.length} draft-only recommendations`} right={<Link href="/dashboard/playbook-recommendations">Open</Link>} />
        </div>
      </Section>
    </div>
  );
}

