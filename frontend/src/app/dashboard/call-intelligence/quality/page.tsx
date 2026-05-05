import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { callIntelligenceSessions, callQualityAverage } from "@/lib/demo-data";

export default function CallIntelligenceQualityPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Call Quality"
        title="Conversation capture score"
        description="Quality score tracks whether the operator captured motivation, condition, timeline, price, decision maker, next step, and avoided unsafe language."
      />

      <div className="metric-grid">
        <MetricCard label="Average" value={`${callQualityAverage}%`} detail="Across analyzed calls" />
        <MetricCard label="Sessions" value={String(callIntelligenceSessions.length)} detail="Quality records" />
        <MetricCard label="Audio capture" value="off" detail="Text-only V23" />
        <MetricCard label="Live response" value="off" detail="Analysis only" />
      </div>

      <Section title="Quality Records">
        <div className="record-list">
          {callIntelligenceSessions.map((session) => (
            <RecordCard key={session.id} title={session.id} meta={session.nextBestAction} right={<Pill tone={session.callQualityScore >= 75 ? "green" : "gold"}>{session.callQualityScore}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
