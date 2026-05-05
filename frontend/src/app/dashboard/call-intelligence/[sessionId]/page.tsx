import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  callIntelligenceSessions,
  getCallFollowUps,
  getCallIntelligenceSession,
  getCallObjections,
  getCallSignals
} from "@/lib/demo-data";

export function generateStaticParams() {
  return callIntelligenceSessions.map((session) => ({ sessionId: session.id }));
}

export default async function CallIntelligenceDetailPage({
  params
}: {
  params: Promise<{ sessionId: string }>;
}) {
  const { sessionId } = await params;
  const session = getCallIntelligenceSession(sessionId);
  if (!session) notFound();
  const signals = getCallSignals(session.id);
  const objections = getCallObjections(session.id);
  const followUps = getCallFollowUps(session.id);

  return (
    <div className="page">
      <PageHeader
        eyebrow={session.ownerReviewStatus}
        title={session.id}
        description={session.nextBestAction}
      />

      <div className="metric-grid">
        <MetricCard label="Motivation delta" value={`+${session.motivationScoreDelta}`} detail={session.sellerMotivationReason} />
        <MetricCard label="Temperature" value={String(session.sellerTemperatureUpdate)} detail="Seller temperature update" />
        <MetricCard label="Risk influence" value={String(session.riskScoreInfluence)} detail={session.legalComplianceRedFlags.join(", ") || "clear"} />
        <MetricCard label="Live response" value={session.liveResponseGenerated ? "generated" : "none"} detail="Draft-only path" />
      </div>

      <div className="grid-two">
        <Section title="Extracted Signals">
          <div className="record-list">
            {signals.map((signal) => (
              <RecordCard key={signal.id} title={signal.signalType} meta={signal.transcriptBasis} right={<Pill>{signal.signalValue}</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Objections">
          <div className="record-list">
            {objections.map((objection) => (
              <RecordCard key={objection.id} title={objection.objectionType} meta={objection.nextAction} right={<Pill tone={objection.riskLevel === "high" ? "red" : "gold"}>{objection.riskLevel}</Pill>} />
            ))}
            {objections.length === 0 ? <RecordCard title="No objections" meta="No structured objection was detected." /> : null}
          </div>
        </Section>
      </div>

      <Section title="Follow-Up Recommendations">
        <div className="record-list">
          {followUps.map((followUp) => (
            <RecordCard key={followUp.id} title={followUp.followUpType} meta={followUp.draftMessageSummary} right={<Pill tone="green">{followUp.recommendedTiming}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
