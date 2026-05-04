import { notFound } from "next/navigation";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { formatCurrency, getContractControl, getLead, getTitleHandoffPacket, titleHandoffPackets } from "@/lib/demo-data";

export function generateStaticParams() {
  return titleHandoffPackets.map((packet) => ({ packetId: packet.id }));
}

export default function TitleHandoffDetailPage({ params }: { params: { packetId: string } }) {
  const packet = getTitleHandoffPacket(params.packetId);
  if (!packet) notFound();
  const contract = getContractControl(packet.contractControlId);
  const lead = contract ? getLead(contract.leadId) : undefined;

  return (
    <div className="page">
      <PageHeader
        eyebrow={packet.packetStatus}
        title={`${packet.id} / ${lead?.sellerName ?? packet.dealId}`}
        description="This packet is a handoff-prep workspace only: placeholders, checklist items, and review reminders stay internal until the owner approves next steps."
      />
      <div className="metric-grid">
        <div className="metric-card"><span>Agreed price</span><strong>{formatCurrency(packet.agreedPrice)}</strong><small>From accepted terms</small></div>
        <div className="metric-card"><span>Closing timeline</span><strong>{packet.closingTimeline}</strong><small>Draft timeline</small></div>
        <div className="metric-card"><span>Title submission</span><strong>blocked</strong><small>V4 boundary</small></div>
        <div className="metric-card"><span>Draft mode</span><strong>{packet.draftOnly ? "on" : "off"}</strong><small>No live action</small></div>
      </div>
      <div className="grid-two">
        <Section title="Packet Fields">
          <div className="record-list">
            <RecordCard title="Property" meta={`${packet.propertyDetails.city}, ${packet.propertyDetails.state} ${packet.propertyDetails.zip} / ${packet.propertyDetails.propertyType}`} />
            <RecordCard title="Seller placeholder" meta={packet.sellerInfoPlaceholder} />
            <RecordCard title="Buyer/entity placeholder" meta={packet.buyerEntityInfoPlaceholder} />
            <RecordCard title="Access notes" meta={packet.accessNotes} />
          </div>
        </Section>
        <Section title="Review Guard">
          <div className="record-list">
            <RecordCard title="Assignment status" meta={packet.assignmentStatus} />
            <RecordCard title="Review reminder" meta={packet.attorneyTitleReviewReminder} />
            <RecordCard title="Submission status" meta="No title company submission exists in V4." right={<Pill tone="red">blocked</Pill>} />
            <RecordCard title="Executable document" meta="No executable legal contract is generated." right={<Pill tone="red">none</Pill>} />
          </div>
        </Section>
      </div>
      <Section title="Document Checklist">
        <div className="tag-row">
          {packet.requiredDocumentChecklist.map((item) => <span className="tag" key={item}>{item}</span>)}
        </div>
      </Section>
    </div>
  );
}
