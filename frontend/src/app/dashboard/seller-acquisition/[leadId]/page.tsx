import { notFound } from "next/navigation";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { formatCurrency, getLead, getOfferPacketByDeal, getSellerInteraction, leads, sellerDrafts, deals } from "@/lib/demo-data";

export function generateStaticParams() {
  return leads.map((lead) => ({ leadId: lead.id }));
}

export default function SellerAcquisitionDetailPage({ params }: { params: { leadId: string } }) {
  const lead = getLead(params.leadId);
  if (!lead) notFound();
  const interaction = getSellerInteraction(lead.id);
  const leadDeal = deals.find((deal) => deal.leadId === lead.id);
  const packet = leadDeal ? getOfferPacketByDeal(leadDeal.id) : undefined;
  const drafts = sellerDrafts(lead, interaction);
  return (
    <div className="page">
      <PageHeader eyebrow={lead.stage} title={lead.sellerName} description={`${lead.address}, ${lead.city}, ${lead.state} ${lead.zipCode}`} />
      <div className="metric-grid">
        <div className="metric-card"><span>Seller temp</span><strong>{interaction?.sellerTemperatureScore ?? lead.motivationScore}</strong><small>Discovery signal</small></div>
        <div className="metric-card"><span>Asking price</span><strong>{formatCurrency(interaction?.askingPrice ?? lead.askingPrice)}</strong><small>Seller stated or lead record</small></div>
        <div className="metric-card"><span>Follow-up</span><strong>{interaction?.followUpUrgency ?? "normal"}</strong><small>{interaction?.nextFollowUpDate ?? "needs date"}</small></div>
        <div className="metric-card"><span>Packet status</span><strong>{packet?.approvalStatus ?? "not started"}</strong><small>Owner gate required</small></div>
      </div>
      <div className="grid-two">
        <Section title="Interaction Record">
          <div className="record-list">
            <RecordCard title="Call notes" meta={interaction?.callNotes ?? "Capture discovery notes before offer prep."} />
            <RecordCard title="Condition" meta={interaction?.propertyCondition ?? "Needs condition discovery."} />
            <RecordCard title="Pain points" meta={interaction?.painPoints.join(", ") ?? "Needs discovery."} />
            <RecordCard title="Objections" meta={interaction?.objections.join(", ") ?? "Needs discovery."} right={<Pill tone="gold">{interaction?.objectionStatus ?? "unknown"}</Pill>} />
          </div>
        </Section>
        <Section title="Draft Engine">
          <div className="record-list">
            <RecordCard title="Call script draft" meta={drafts.callScriptDraft} right={<Pill tone="green">draft</Pill>} />
            <RecordCard title="SMS draft" meta={drafts.smsDraft} right={<Pill tone="green">draft</Pill>} />
            <RecordCard title="Email draft" meta={drafts.emailDraft} right={<Pill tone="green">draft</Pill>} />
            <RecordCard title="Offer explanation draft" meta={drafts.offerExplanationDraft} right={<Pill tone="green">draft</Pill>} />
          </div>
        </Section>
      </div>
    </div>
  );
}
