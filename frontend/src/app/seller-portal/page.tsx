import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { formatCurrency, sellerVisibleOffers } from "@/lib/demo-data";

const offer = sellerVisibleOffers[0];

export default function SellerPortalPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Invite-Gated"
        title="Controlled offer review room"
        description="This room shows a sanitized offer summary, timeline, document checklist, and intake-only questions for operator review."
      />
      <div className="metric-grid">
        <MetricCard label="Offer status" value={offer.offerStatus.replaceAll("_", " ")} detail="Operator controlled" />
        <MetricCard label="Offer amount" value={offer.offerAmount ? formatCurrency(offer.offerAmount) : "Review"} detail="Seller-facing amount" />
        <MetricCard label="Signing actions" value="Off" detail="Review room only" />
        <MetricCard label="Message intake" value="Draft" detail="Operator review required" />
      </div>
      <Section title="Offer Review Snapshot">
        <div className="grid-three">
          <RecordCard title="Property" meta={offer.propertyAddressSummary} right={<Pill tone="green">visible</Pill>} />
          <RecordCard title="Timeline" meta={offer.closingTimelineEstimate} right={<Pill tone="gold">estimate</Pill>} />
          <RecordCard title="Questions" meta="Notes are intake-only and do not accept, counter, or schedule automatically." right={<Pill>review</Pill>} />
        </div>
        <Link className="pill green" href="/seller-portal/offer">open offer details</Link>
      </Section>
    </div>
  );
}
