import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  blockedLeadImportRows,
  doNotContactOutcomes,
  fieldTestingAccuracy,
  firstDealCandidates,
  motivatedFieldOutcomes,
  pendingScoringAdjustments,
  predictionMisses
} from "@/lib/demo-data";

export default function FieldTestingPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V19 Field Testing Loop"
        title="Real lead field testing"
        description="Prime 2 turns real CSV lead data and operator call outcomes into QA queues, first-deal candidates, prediction feedback, and explainable scoring adjustments."
      />

      <div className="metric-grid">
        <MetricCard label="Bad rows" value={String(blockedLeadImportRows.length)} detail="Blocked before commit" />
        <MetricCard label="Motivated sellers" value={String(motivatedFieldOutcomes.length)} detail="Escalated internally" />
        <MetricCard label="Prediction accuracy" value={`${fieldTestingAccuracy}%`} detail="Field samples only" />
        <MetricCard label="Scoring queue" value={String(pendingScoringAdjustments.length)} detail="Owner-reviewed changes" />
      </div>

      <Section title="Field Testing Routes">
        <div className="grid-three">
          <RecordCard title="Lead Imports" meta="CSV preview, row status, commit gate" right={<Link href="/dashboard/lead-imports">Open</Link>} />
          <RecordCard title="Lead QA" meta="Quality and contactability scoring" right={<Link href="/dashboard/lead-qa">Open</Link>} />
          <RecordCard title="Call Outcomes" meta="Manual seller conversation results" right={<Link href="/dashboard/call-outcomes">Open</Link>} />
          <RecordCard title="Feedback Loop" meta={`${predictionMisses.length} prediction misses`} right={<Link href="/dashboard/feedback-loop">Open</Link>} />
          <RecordCard title="Adjustments" meta="Explainable scoring changes" right={<Link href="/dashboard/scoring-adjustments">Open</Link>} />
          <RecordCard title="Field Briefing" meta="Prime 2 daily field queue" right={<Link href="/dashboard/field-briefing">Open</Link>} />
        </div>
      </Section>

      <Section title="First-Deal Candidates">
        <div className="record-list">
          {firstDealCandidates.map((candidate) => (
            <RecordCard key={candidate.id} title={candidate.importRowId ?? candidate.id} meta={`Import confidence ${candidate.importConfidence}`} right={<Pill>{candidate.recommendedNextAction}</Pill>} />
          ))}
        </div>
      </Section>

      <Section title="Do-Not-Contact Boundary">
        <div className="grid-three">
          {doNotContactOutcomes.map((outcome) => (
            <RecordCard key={outcome.id} title={outcome.leadId} meta={outcome.prime2NextRecommendation} right={<Pill tone="red">blocked</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
