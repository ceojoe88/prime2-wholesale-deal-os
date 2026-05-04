import { notFound } from "next/navigation";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { formatCurrency, getDeal, getLead, getOfferPacket, offerPackets } from "@/lib/demo-data";

export function generateStaticParams() {
  return offerPackets.map((packet) => ({ packetId: packet.id }));
}

export default function OfferPacketDetailPage({ params }: { params: { packetId: string } }) {
  const packet = getOfferPacket(params.packetId);
  if (!packet) notFound();
  const deal = getDeal(packet.dealId);
  const lead = deal ? getLead(deal.leadId) : undefined;
  return (
    <div className="page">
      <PageHeader
        eyebrow={packet.packetStatus}
        title={`${packet.id} / ${lead?.sellerName ?? packet.dealId}`}
        description="Packet prep remains draft-only and cannot advance unless every gate is clear."
      />
      <div className="metric-grid">
        <div className="metric-card"><span>ARV</span><strong>{formatCurrency(deal?.arv ?? 0)}</strong><small>Required</small></div>
        <div className="metric-card"><span>Repairs</span><strong>{formatCurrency(deal?.repairs ?? 0)}</strong><small>Required</small></div>
        <div className="metric-card"><span>Max seller offer</span><strong>{formatCurrency(deal?.maxSellerOffer ?? 0)}</strong><small>Must be calculated</small></div>
        <div className="metric-card"><span>Approval</span><strong>{packet.packetPrepAllowed ? "ready" : "blocked"}</strong><small>{packet.approvalStatus}</small></div>
      </div>
      <div className="grid-two">
        <Section title="Gate Checklist">
          <div className="record-list">
            {[
              ["Underwriting complete", packet.underwritingComplete],
              ["Buyer margin protected", packet.buyerMarginProtected],
              ["Target assignment fee checked", packet.targetAssignmentFeeChecked],
              ["Compliance guard passed", packet.complianceGuardPassed],
              ["Owner approval recorded", packet.ownerApprovalRecorded]
            ].map(([label, passed]) => (
              <RecordCard key={String(label)} title={String(label)} right={<Pill tone={passed ? "green" : "red"}>{passed ? "passed" : "blocked"}</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Packet Status">
          <div className="record-list">
            <RecordCard title="Draft summary" meta={packet.draftSummary} right={<Pill tone="green">draft only</Pill>} />
            <RecordCard title="Blocked reasons" meta={packet.blockedReasons.length ? packet.blockedReasons.join(", ") : "No blocks"} right={<Pill tone={packet.packetPrepAllowed ? "green" : "red"}>{packet.packetStatus}</Pill>} />
            <RecordCard title="Real-world action" meta="No offer sent, no live outreach, no contract execution." right={<Pill tone="red">none</Pill>} />
          </div>
        </Section>
      </div>
    </div>
  );
}
