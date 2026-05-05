import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { getLeadQaReview, leadQualityReviews } from "@/lib/demo-data";

export function generateStaticParams() {
  return leadQualityReviews.map((review) => ({ leadId: review.leadId ?? review.importRowId ?? review.id }));
}

export default async function LeadQaDetailPage({
  params
}: {
  params: Promise<{ leadId: string }>;
}) {
  const { leadId } = await params;
  const review = getLeadQaReview(leadId);
  if (!review) notFound();

  return (
    <div className="page">
      <PageHeader
        eyebrow={review.recommendedNextAction}
        title={review.importRowId ?? review.leadId ?? review.id}
        description="QA detail keeps the operator focused on evidence quality and next action. Live outreach remains unavailable from QA."
      />

      <div className="metric-grid">
        <MetricCard label="Data quality" value={String(review.dataQualityScore)} detail="Missing and conflicting fields" />
        <MetricCard label="Contactability" value={String(review.contactabilityScore)} detail="Phone/email confidence" />
        <MetricCard label="Distress confidence" value={String(review.distressSignalConfidence)} detail="Flag evidence strength" />
        <MetricCard label="Import confidence" value={String(review.importConfidence)} detail={review.reviewedBy} />
      </div>

      <Section title="Checks">
        <div className="grid-three">
          {Object.entries(review.checks).map(([check, value]) => (
            <RecordCard key={check} title={check} meta={value ? "Needs attention" : "Clear"} right={<Pill tone={value ? "red" : "green"}>{String(value)}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
