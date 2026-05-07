import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientOfferReadinessGates,
  clientUnderwritingReviews,
  formatCurrency,
  getClientLead
} from "@/lib/demo-data";

export default function ClientCommandUnderwritingReadyReviewPage() {
  const ready = clientOfferReadinessGates.filter((gate) => gate.readinessStatus === "ready_for_client_review");
  return (
    <div className="page">
      <PageHeader
        eyebrow="Underwriting Ready Review"
        title="Offer readiness queue"
        description="Decision support only — no contract or offer has been sent."
      />

      <div className="metric-grid">
        <MetricCard label="Ready records" value={String(ready.length)} detail="Human review still required" />
        <MetricCard label="Contracts" value="0" detail="No contract generated" />
        <MetricCard label="Offers sent" value="0" detail="No offer has been sent" />
        <MetricCard label="Provider actions" value="0" detail="No external provider call" />
      </div>

      <Section title="Ready For Client Review">
        <div className="record-list">
          {ready.map((gate) => {
            const lead = getClientLead(gate.leadId);
            const review = clientUnderwritingReviews.find((item) => item.id === gate.underwritingReviewId);
            return (
              <RecordCard
                key={gate.id}
                title={lead?.displayName ?? gate.leadId}
                meta={gate.recommendedNextStep}
                right={<Link href={`/dashboard/client-command/leads/${gate.leadId}`}>View Details</Link>}
              >
                <div className="tag-row">
                  <Pill tone="green">{gate.readinessStatus}</Pill>
                  <Pill tone="gold">Human Review Needed</Pill>
                  <Pill tone="green">{review?.maxAllowableOffer ? formatCurrency(review.maxAllowableOffer) : "MAO missing"}</Pill>
                </div>
              </RecordCard>
            );
          })}
        </div>
      </Section>
    </div>
  );
}
