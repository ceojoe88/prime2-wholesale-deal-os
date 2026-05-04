import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  formatCurrency,
  getDeal,
  getLead,
  getNegotiationRecord,
  getOfferPositioningRecord,
  negotiationRecords
} from "@/lib/demo-data";

export function generateStaticParams() {
  return negotiationRecords.map((record) => ({ recordId: record.id }));
}

export default async function NegotiationDetailPage({ params }: { params: Promise<{ recordId: string }> }) {
  const { recordId } = await params;
  const record = getNegotiationRecord(recordId);
  if (!record) notFound();
  const deal = getDeal(record.dealId);
  const lead = deal ? getLead(deal.leadId) : undefined;
  const positioning = getOfferPositioningRecord(record.offerPositioningId);

  return (
    <div className="page">
      <PageHeader
        eyebrow={record.negotiationStage}
        title={`${record.id} / ${lead?.city ?? "Property"}, ${lead?.state ?? ""}`}
        description="Negotiation tracking records seller response state and next move recommendations only. No acceptance, send, or contract action happens here."
      />
      <div className="metric-grid">
        <MetricCard label="Readiness score" value={String(record.readinessScore)} detail={record.readinessLevel} />
        <MetricCard label="Motivation" value={String(record.motivationScore)} detail="Acceptance readiness input" />
        <MetricCard label="Price alignment" value={String(record.priceAlignment)} detail={record.counterOffer ? formatCurrency(record.counterOffer) : "No counter"} />
        <MetricCard label="Trust level" value={String(record.trustLevel)} detail="No pressure tactics" />
      </div>

      <div className="grid-two">
        <Section title="Seller Response">
          <div className="record-list">
            <RecordCard title="Last response" meta={record.sellerLastResponse} right={<Pill>{record.negotiationStage}</Pill>} />
            <RecordCard title="Objections" meta={record.sellerObjections.join(", ")} />
            <RecordCard title="Emotional signals" meta={record.emotionalSignals.join(", ")} />
            <RecordCard title="Next move" meta={record.nextMoveRecommendation} right={<Pill tone="green">internal</Pill>} />
          </div>
        </Section>
        <Section title="Offer Position">
          <div className="record-list">
            <RecordCard title="Strategy" meta={positioning?.offerStrategyType ?? "missing"} right={<Pill>{positioning?.confidenceScore ?? 0}</Pill>} />
            <RecordCard title="Ideal contract price" meta={formatCurrency(positioning?.idealContractPrice ?? 0)} />
            <RecordCard title="Walk-away price" meta={formatCurrency(positioning?.walkAwayPrice ?? 0)} />
            <RecordCard title="Live automation" meta="Disabled for negotiation records." right={<Pill tone="red">off</Pill>} />
          </div>
        </Section>
      </div>

      <Section title="Readiness Inputs">
        <div className="grid-three">
          <RecordCard title="Timeline alignment" meta={String(record.timelineAlignment)} right={<Pill>{record.timelineAlignment}</Pill>} />
          <RecordCard title="Objection resolution" meta={String(record.objectionResolution)} right={<Pill>{record.objectionResolution}</Pill>} />
          <RecordCard title="Contact consistency" meta={String(record.contactConsistency)} right={<Pill>{record.contactConsistency}</Pill>} />
        </div>
      </Section>
    </div>
  );
}
