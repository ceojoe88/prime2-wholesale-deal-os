import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientAcquisitionBriefs,
  clientAppointmentReadinessReviews,
  clientFollowUpDrafts,
  clientSellerQuestionPlans
} from "@/lib/demo-data";

export default function ClientCommandAcquisitionPage() {
  const needsReview = clientAppointmentReadinessReviews.filter((review) => review.requiresHumanReview);
  return (
    <div className="page">
      <PageHeader
        eyebrow="CP3 Acquisition AI Team"
        title="Acquisition Manager command"
        description="Client-safe seller preparation with briefs, question plans, manual draft queues, and appointment readiness. Nothing is sent or placed from this workspace."
      />

      <div className="metric-grid">
        <MetricCard label="Briefs" value={String(clientAcquisitionBriefs.length)} detail="Seller conversation prep" />
        <MetricCard label="Question plans" value={String(clientSellerQuestionPlans.length)} detail="Manual discovery guidance" />
        <MetricCard label="Manual drafts" value={String(clientFollowUpDrafts.length)} detail="No message has been sent" />
        <MetricCard label="Needs review" value={String(needsReview.length)} detail="Human review flags" />
      </div>

      <Section title="Acquisition Division Cards">
        <div className="grid-three">
          <RecordCard title="Acquisition Manager" meta="Prepares client-safe seller conversation guidance." right={<Pill tone="green">active</Pill>} />
          <RecordCard title="Appointment Readiness" meta="Drops readiness when motivation, contact, timeline, condition, or price data is missing." right={<Pill tone="gold">gated</Pill>} />
          <RecordCard title="Safety Boundary" meta="Drafts are manual-use only and provider-free." right={<Pill tone="red">locked</Pill>} />
        </div>
      </Section>

      <Section title="Acquisition Work Queue">
        <div className="grid-three">
          <RecordCard title="Briefs" meta="Call prep summaries and tone guidance" right={<Link href="/dashboard/client-command/acquisition/briefs">View Details</Link>} />
          <RecordCard title="Needs Review" meta="Appointment-readiness blockers" right={<Link href="/dashboard/client-command/acquisition/needs-review">View Details</Link>} />
          <RecordCard title="Lead Detail" meta="CP2, CP3, and CP4 sections live on each lead page" right={<Link href="/dashboard/client-command/leads">View Details</Link>} />
        </div>
      </Section>
    </div>
  );
}
