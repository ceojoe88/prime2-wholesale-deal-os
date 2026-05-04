import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { sellerPortalResponses, sellerVisibleOffers } from "@/lib/demo-data";

const offer = sellerVisibleOffers[0];

export default function SellerMessagesPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Messages"
        title="Questions and notes intake"
        description="Messages are saved for operator review. The room does not negotiate, accept, send external messages, or change offer status automatically."
      />
      <div className="grid-two">
        <Section title="New Note">
          <div className="record-list">
            <RecordCard title="Offer question" meta={offer.ownerOperatorContactPlaceholder} right={<Pill tone="gold">review</Pill>}>
              <textarea rows={7} placeholder="Question for operator review" aria-label="Question for operator review" />
              <button className="pill green" type="button">Record question</button>
            </RecordCard>
          </div>
        </Section>
        <Section title="Recent Intake">
          <div className="record-list">
            {sellerPortalResponses.map((response) => (
              <RecordCard
                key={response.id}
                title={response.responseType.replaceAll("_", " ")}
                meta={response.offerQuestion || response.sellerPortalNote || response.appointmentAccessPreference || response.documentUploadPlaceholder}
                right={<Pill tone={response.operatorReviewStatus === "reviewed" ? "green" : "gold"}>{response.operatorReviewStatus}</Pill>}
              />
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
