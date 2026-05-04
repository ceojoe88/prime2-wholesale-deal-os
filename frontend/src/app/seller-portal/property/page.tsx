import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { sellerVisibleOffers } from "@/lib/demo-data";

const offer = sellerVisibleOffers[0];

export default function SellerPropertyPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Property"
        title="Property summary and access"
        description="Property details are limited to the approved address summary and access next step."
      />
      <div className="grid-two">
        <Section title="Property Summary">
          <div className="record-list">
            <RecordCard title="Address summary" meta={offer.propertyAddressSummary} right={<Pill tone="green">approved</Pill>} />
            <RecordCard title="Access next step" meta={offer.inspectionAccessNextStep} right={<Pill tone="gold">review</Pill>} />
          </div>
        </Section>
        <Section title="Access Preference Intake">
          <textarea rows={8} placeholder="Preferred access windows or condition notes" aria-label="Preferred access windows or condition notes" />
          <div className="pill-row">
            <button className="pill green" type="button">Record access preference</button>
            <Pill>operator review</Pill>
          </div>
        </Section>
      </div>
    </div>
  );
}
