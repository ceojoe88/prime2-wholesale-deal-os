import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  callPriorityQaReviews,
  leadQualityReviews,
  lowConfidenceQaReviews,
  researchMoreQaReviews
} from "@/lib/demo-data";

export default function LeadQaPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V19 Lead QA"
        title="Lead quality assurance"
        description="Imported leads receive data quality, contactability, distress, equity, and import-confidence scores before the operator decides the next field action."
      />

      <div className="metric-grid">
        <MetricCard label="QA records" value={String(leadQualityReviews.length)} detail="Import and committed lead checks" />
        <MetricCard label="Call priority" value={String(callPriorityQaReviews.length)} detail="High-confidence rows" />
        <MetricCard label="Research more" value={String(researchMoreQaReviews.length)} detail="Contact or source gaps" />
        <MetricCard label="Low confidence" value={String(lowConfidenceQaReviews.length)} detail="Blocked or weak records" />
      </div>

      <Section title="Quality Queue">
        <div className="record-list">
          {leadQualityReviews.map((review) => (
            <RecordCard
              key={review.id}
              title={review.importRowId ?? review.leadId ?? review.id}
              meta={`Import ${review.importConfidence} | data ${review.dataQualityScore} | contact ${review.contactabilityScore}`}
              right={<Pill tone={review.blockedReasons.length ? "red" : "gold"}>{review.recommendedNextAction}</Pill>}
            />
          ))}
        </div>
      </Section>

      <Section title="Blocked Reasons">
        <div className="grid-three">
          {lowConfidenceQaReviews.map((review) => (
            <RecordCard key={review.id} title={review.id} meta={review.blockedReasons.join(", ") || "low confidence / research needed"} right={<Pill tone="red">review</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
