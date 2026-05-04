import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { formatCurrency, sellerVisibleOffers } from "@/lib/demo-data";

const offer = sellerVisibleOffers[0];

export default function SellerOfferPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Offer Review"
        title="Offer status and next steps"
        description="The offer room only displays approved external-facing information. Questions are captured for operator review."
      />
      <div className="metric-grid">
        <MetricCard label="Offer amount" value={offer.offerAmount ? formatCurrency(offer.offerAmount) : "Review"} detail="Approved display amount" />
        <MetricCard label="Offer status" value={offer.offerStatus.replaceAll("_", " ")} detail="Visible after gate review" />
        <MetricCard label="Room status" value={offer.portalVisibilityStatus} detail="Invite access only" />
        <MetricCard label="Automation" value="Off" detail="No counters or acceptance flow" />
      </div>
      <div className="grid-two">
        <Section title="Offer Summary">
          <table className="data-table">
            <tbody>
              <tr><th>Property</th><td>{offer.propertyAddressSummary}</td></tr>
              <tr><th>Offer amount</th><td className="money">{offer.offerAmount ? formatCurrency(offer.offerAmount) : "Under review"}</td></tr>
              <tr><th>Timeline estimate</th><td>{offer.closingTimelineEstimate}</td></tr>
              <tr><th>Review status</th><td>{offer.titleCompanyReviewStatus}</td></tr>
            </tbody>
          </table>
        </Section>
        <Section title="Questions Intake">
          <div className="record-list">
            <RecordCard title="Owner/operator contact" meta={offer.ownerOperatorContactPlaceholder} right={<Pill>placeholder</Pill>} />
            <RecordCard title="Question form" meta="Saves a note for operator review only." right={<Pill tone="gold">draft intake</Pill>}>
              <textarea rows={5} placeholder="Questions or notes for review" aria-label="Questions or notes for review" />
              <button className="pill green" type="button">Record draft note</button>
            </RecordCard>
          </div>
        </Section>
      </div>
    </div>
  );
}
