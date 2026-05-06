import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { mobileBuyerQueue } from "@/lib/demo-data";

export default function MobileBuyersPage() {
  const verified = mobileBuyerQueue.filter((buyer) => buyer.proofOfFundsStatus === "verified");
  return (
    <div className="page">
      <PageHeader eyebrow="Mobile Buyers" title="Buyer check view" description="Review buyer reliability, POF posture, and quick response notes from the field without exposing internal spread logic." />
      <div className="metric-grid">
        <MetricCard label="Buyer queue" value={String(mobileBuyerQueue.length)} detail="Reliability sorted" />
        <MetricCard label="POF verified" value={String(verified.length)} detail="Buyer confidence input" />
        <MetricCard label="Response notes" value="draft" detail="Owner review only" />
        <MetricCard label="Bulk action" value="off" detail="One-record workflow" />
      </div>
      <Section title="Fast Buyer Snapshot">
        <div className="record-list">
          {mobileBuyerQueue.map((buyer) => (
            <RecordCard key={buyer.id} title={buyer.company} meta={`${buyer.propertyType} / closes in ${buyer.closingSpeedDays} days`} right={<Pill tone={buyer.proofOfFundsStatus === "verified" ? "green" : "gold"}>{buyer.proofOfFundsStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
