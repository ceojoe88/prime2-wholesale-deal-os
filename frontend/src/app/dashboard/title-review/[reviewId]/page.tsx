import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  getContractReadyStateByDeal,
  getDeal,
  getLead,
  getReviewPacketPrepByReview,
  getTitleReviewCoordination,
  titleReviewCoordinations
} from "@/lib/demo-data";

export function generateStaticParams() {
  return titleReviewCoordinations.map((record) => ({ reviewId: record.id }));
}

export default async function TitleReviewDetailPage({ params }: { params: Promise<{ reviewId: string }> }) {
  const { reviewId } = await params;
  const record = getTitleReviewCoordination(reviewId);
  if (!record) notFound();
  const deal = getDeal(record.dealId);
  const lead = deal ? getLead(deal.leadId) : undefined;
  const state = getContractReadyStateByDeal(record.dealId);
  const packet = getReviewPacketPrepByReview(record.id);

  return (
    <div className="page">
      <PageHeader
        eyebrow={record.attorneyTitleReviewStatus}
        title={`${record.id} / ${lead?.city ?? "Property"}, ${lead?.state ?? ""}`}
        description="Coordinates title/attorney review preparation only. The system does not submit documents, send title-company email, create legal relationships, or execute contracts."
      />
      <div className="metric-grid">
        <MetricCard label="V10 status" value={state?.contractReady ? "ready" : "blocked"} detail={state?.readinessStatus ?? "missing"} />
        <MetricCard label="Numbers locked" value={state?.numbersLocked ? "yes" : "no"} detail="Required for packet prep" />
        <MetricCard label="Owner approval" value={record.ownerApprovalStatus} detail="Owner remains final approver" />
        <MetricCard label="Packet prep" value={record.packetPrepAllowed ? "allowed" : "blocked"} detail="Draft-only" />
      </div>

      <div className="grid-two">
        <Section title="Coordination Record">
          <div className="record-list">
            <RecordCard title="Title placeholder" meta={record.selectedTitleCompanyPlaceholder} right={<Pill tone="gold">placeholder</Pill>} />
            <RecordCard title="Required documents" meta={record.requiredDocuments.join(", ")} />
            <RecordCard title="Missing items" meta={record.missingItems.length ? record.missingItems.join(", ") : "none"} right={<Pill tone={record.missingItems.length ? "red" : "green"}>{record.missingItems.length}</Pill>} />
            <RecordCard title="Review notes" meta={record.reviewNotes} />
          </div>
        </Section>
        <Section title="Draft Packet Preview">
          <div className="record-list">
            <RecordCard title="Packet" meta={packet?.id ?? "missing"} right={<Pill tone={packet?.prepAllowed ? "green" : "red"}>{packet?.packetStatus ?? "missing"}</Pill>} />
            <RecordCard title="Closing timeline" meta={packet?.closingTimeline ?? "missing"} />
            <RecordCard title="Access notes" meta={packet?.accessNotes ?? "missing"} />
            <RecordCard title="Document checklist" meta={packet?.documentChecklist.join(", ") ?? "missing"} />
          </div>
        </Section>
      </div>

      <Section title="Blocked Actions">
        <div className="grid-three">
          <RecordCard title="Legal advice" meta="Blocked; only attorney/title review reminders are prepared." right={<Pill tone="red">off</Pill>} />
          <RecordCard title="Document submission" meta="Blocked; review packet is not sent or submitted." right={<Pill tone="red">off</Pill>} />
          <RecordCard title="Contract execution" meta="Blocked; no executable contract generation." right={<Pill tone="red">off</Pill>} />
        </div>
      </Section>
    </div>
  );
}
