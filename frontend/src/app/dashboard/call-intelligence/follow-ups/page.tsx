import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { callFollowUpRecommendations } from "@/lib/demo-data";

export default function CallIntelligenceFollowUpsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Follow-Up Intelligence"
        title="Draft-only seller follow-ups"
        description="Follow-up recommendations are scheduling and drafting guidance. They do not send messages or create automatic touchpoints."
      />

      <div className="metric-grid">
        <MetricCard label="Recommendations" value={String(callFollowUpRecommendations.length)} detail="Owner review queue" />
        <MetricCard label="Live sends" value="0" detail="Disabled in V23" />
        <MetricCard label="Auto sequence" value="off" detail="No automatic follow-up chain" />
        <MetricCard label="Review" value="required" detail="Before any next step" />
      </div>

      <Section title="Follow-Up Queue">
        <div className="record-list">
          {callFollowUpRecommendations.map((followUp) => (
            <RecordCard key={followUp.id} title={followUp.followUpType} meta={followUp.draftMessageSummary} right={<Pill tone="green">{followUp.recommendedTiming}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}

