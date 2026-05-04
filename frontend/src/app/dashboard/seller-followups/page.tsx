import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { leads } from "@/lib/demo-data";

export default function SellerFollowupsPage() {
  const followupLeads = leads.filter((lead) => ["follow_up", "offer_sent", "negotiating", "contacted"].includes(lead.stage));
  return (
    <div className="page">
      <PageHeader
        eyebrow="Follow-Up Division"
        title="Seller follow-up priority"
        description="Touchpoints are draft-only. The owner controls every real-world contact."
      />
      <div className="grid-three">
        {followupLeads.map((lead) => (
          <RecordCard
            key={lead.id}
            title={lead.sellerName}
            meta={`${lead.stage} / ${lead.sourceCategory} / ${lead.zipCode}`}
            right={<Pill tone={lead.opportunityScore >= 75 ? "green" : "gold"}>{lead.opportunityScore}</Pill>}
          >
            <div className="pill-row">
              <Pill>follow-up plan</Pill>
              <Pill>offer explanation</Pill>
              <Pill tone="red">no live outreach</Pill>
            </div>
          </RecordCard>
        ))}
      </div>
    </div>
  );
}
