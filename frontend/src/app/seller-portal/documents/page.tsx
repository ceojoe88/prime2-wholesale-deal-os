import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { sellerVisibleOffers } from "@/lib/demo-data";

const offer = sellerVisibleOffers[0];

export default function SellerDocumentsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Documents"
        title="Checklist and upload placeholders"
        description="Checklist items are review prompts. Upload controls are placeholders and do not transmit files in this version."
      />
      <div className="grid-two">
        <Section title="Document Checklist">
          <div className="record-list">
            {offer.documentChecklist.map((item) => (
              <RecordCard key={item} title={item} meta="Review queue item" right={<Pill tone="gold">pending</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Placeholder Upload">
          <RecordCard
            title="Document upload placeholder"
            meta="Records that a document may be provided after operator review. No file upload occurs here."
            right={<Pill>placeholder</Pill>}
          >
            <button className="pill green" type="button">Record document note</button>
          </RecordCard>
        </Section>
      </div>
    </div>
  );
}
