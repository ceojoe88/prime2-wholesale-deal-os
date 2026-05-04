import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { sellerVisibleOffers } from "@/lib/demo-data";

const offer = sellerVisibleOffers[0];

export default function SellerTimelinePage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Timeline"
        title="Estimated closing path"
        description="Timeline items are estimates and placeholders for review. The portal does not schedule or change status automatically."
      />
      <div className="metric-grid">
        <MetricCard label="Offer status" value={offer.offerStatus.replaceAll("_", " ")} detail="Owner controlled" />
        <MetricCard label="Timeline estimate" value={offer.closingTimelineEstimate} detail="Subject to review" />
        <MetricCard label="Title review" value="Reminder" detail="No submission from portal" />
        <MetricCard label="Auto scheduling" value="Off" detail="Intake only" />
      </div>
      <Section title="Next Steps">
        <div className="record-list">
          <RecordCard title="Review offer summary" meta="Read the displayed offer amount and property summary." right={<Pill tone="green">visible</Pill>} />
          <RecordCard title="Share access preference" meta={offer.inspectionAccessNextStep} right={<Pill tone="gold">intake</Pill>} />
          <RecordCard title="Title review reminder" meta={offer.titleCompanyReviewStatus} right={<Pill>placeholder</Pill>} />
        </div>
      </Section>
    </div>
  );
}
