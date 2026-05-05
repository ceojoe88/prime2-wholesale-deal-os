import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { campaignAudiencePreviews } from "@/lib/demo-data";

export default function CampaignSegmentsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Audience Segmentation"
        title="Preview segments and exclusions"
        description="Seller and buyer segments are previewed before activation, with DNC, quality, compliance, consent, and weak-margin exclusions visible to the owner."
      />
      <Section title="Audience Preview">
        <div className="record-list">
          {campaignAudiencePreviews.map((row) => (
            <RecordCard key={row.id} title={row.recipientId} meta={row.exclusionReasons.join(", ") || row.segmentName} right={<Pill tone={row.excluded ? "red" : "green"}>{row.inclusionStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}

