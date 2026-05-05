import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  callFollowUpRecommendations,
  callIntelligenceSessions,
  callObjectionRecords,
  callQualityAverage,
  complianceCallEscalations,
  dncCallSessions,
  highMotivationCallSessions
} from "@/lib/demo-data";

export default function CallIntelligencePage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V23 Call Intelligence"
        title="Seller conversation intelligence"
        description="Prime 2 converts manual call notes and pasted transcripts into structured seller signals, objections, DNC detection, quality scores, and draft-only next actions."
      />

      <div className="metric-grid">
        <MetricCard label="Analyzed calls" value={String(callIntelligenceSessions.length)} detail="Manual notes and transcripts" />
        <MetricCard label="High motivation" value={String(highMotivationCallSessions.length)} detail="Escalated for owner review" />
        <MetricCard label="DNC detected" value={String(dncCallSessions.length)} detail="Outreach eligibility blocked" />
        <MetricCard label="Quality" value={`${callQualityAverage}%`} detail="Conversation capture score" />
      </div>

      <Section title="Recent Sessions">
        <div className="record-list">
          {callIntelligenceSessions.map((session) => (
            <RecordCard
              key={session.id}
              title={session.id}
              meta={`${session.sellerMotivationReason} / ${session.urgencyTimeline}`}
              right={<Link href={`/dashboard/call-intelligence/${session.id}`}><Pill tone={session.doNotContactDetected ? "red" : "green"}>{session.analysisStatus}</Pill></Link>}
            />
          ))}
        </div>
      </Section>

      <Section title="Work Queues">
        <div className="grid-three">
          <RecordCard title="New Analysis" meta="Manual notes or pasted transcript intake" right={<Link href="/dashboard/call-intelligence/new">Open</Link>} />
          <RecordCard title="Objections" meta={`${callObjectionRecords.length} draft-only responses`} right={<Link href="/dashboard/call-intelligence/objections">Open</Link>} />
          <RecordCard title="Follow-Ups" meta={`${callFollowUpRecommendations.length} owner-reviewed recommendations`} right={<Link href="/dashboard/call-intelligence/follow-ups">Open</Link>} />
          <RecordCard title="Quality" meta="Capture score trends" right={<Link href="/dashboard/call-intelligence/quality">Open</Link>} />
          <RecordCard title="Compliance Escalations" meta={`${complianceCallEscalations.length} title/review questions`} right={<Pill tone="red">review</Pill>} />
          <RecordCard title="Live Calling" meta="Not available in this layer" right={<Pill tone="red">off</Pill>} />
        </div>
      </Section>
    </div>
  );
}

