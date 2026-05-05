import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  blockedLeadImportRows,
  callPriorityQaReviews,
  fieldTestingAccuracy,
  firstDealCandidates,
  pendingScoringAdjustments,
  predictionMisses,
  researchMoreQaReviews
} from "@/lib/demo-data";

export default function FieldBriefingPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Prime 2 Field Briefing"
        title="Daily field-testing briefing"
        description="Prime 2 summarizes real import QA, field-call outcomes, prediction misses, and first-deal candidates while keeping all real-world actions owner-controlled."
      />

      <div className="metric-grid">
        <MetricCard label="Blocked rows" value={String(blockedLeadImportRows.length)} detail="Bad import rows" />
        <MetricCard label="Call priority" value={String(callPriorityQaReviews.length)} detail="Top seller calls to review" />
        <MetricCard label="Prediction misses" value={String(predictionMisses.length)} detail={`${fieldTestingAccuracy}% current accuracy`} />
        <MetricCard label="Adjustments" value={String(pendingScoringAdjustments.length)} detail="Owner review queue" />
      </div>

      <div className="grid-two">
        <Section title="Top Call-Priority Leads">
          <div className="record-list">
            {callPriorityQaReviews.map((review) => (
              <RecordCard key={review.id} title={review.importRowId ?? review.id} meta={`Import confidence ${review.importConfidence}`} right={<Pill tone="green">priority</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Research More">
          <div className="record-list">
            {researchMoreQaReviews.map((review) => (
              <RecordCard key={review.id} title={review.importRowId ?? review.id} meta={`Contactability ${review.contactabilityScore}`} right={<Pill tone="gold">research</Pill>} />
            ))}
          </div>
        </Section>
      </div>

      <Section title="First-Deal Candidate List">
        <div className="grid-three">
          {firstDealCandidates.map((candidate) => (
            <RecordCard key={candidate.id} title={candidate.importRowId ?? candidate.id} meta={`Next action: ${candidate.recommendedNextAction}`} right={<Pill>{candidate.importConfidence}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
