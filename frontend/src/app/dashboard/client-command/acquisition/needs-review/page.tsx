import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientAppointmentReadinessReviews, getClientLead } from "@/lib/demo-data";

export default function ClientCommandAcquisitionNeedsReviewPage() {
  const reviews = clientAppointmentReadinessReviews.filter((review) => review.requiresHumanReview);
  return (
    <div className="page">
      <PageHeader
        eyebrow="Acquisition Review Queue"
        title="Appointment readiness needs review"
        description="Readiness drops when motivation, contact, timeline, condition, asking price, or CP2 missing-data signals are not complete."
      />

      <div className="metric-grid">
        <MetricCard label="Needs review" value={String(reviews.length)} detail="Manager-gated" />
        <MetricCard label="Ready" value={String(clientAppointmentReadinessReviews.filter((review) => review.appointmentReady).length)} detail="Manual-use review only" />
        <MetricCard label="Outbound actions" value="0" detail="No provider action" />
        <MetricCard label="Human flags" value={String(reviews.length)} detail="Visible to client" />
      </div>

      <Section title="Readiness Blockers">
        <div className="record-list">
          {reviews.map((review) => {
            const lead = getClientLead(review.leadId);
            return (
              <RecordCard
                key={review.id}
                title={lead?.displayName ?? review.leadId}
                meta={review.recommendedNextStep}
                right={<Link href={`/dashboard/client-command/leads/${review.leadId}`}>View Details</Link>}
              >
                <p>{review.reasonSummary}</p>
                <div className="tag-row">
                  <Pill tone="red">{review.readinessScore}</Pill>
                  {review.missingRequirements.map((item) => (
                    <Pill key={item} tone="gold">{item}</Pill>
                  ))}
                </div>
              </RecordCard>
            );
          })}
        </div>
      </Section>
    </div>
  );
}
