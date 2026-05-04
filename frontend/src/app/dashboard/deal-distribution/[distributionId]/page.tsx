import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  dealDistributionPreps,
  formatCurrency,
  getBuyer,
  getBuyerDealPriority,
  getDeal,
  getDealDistributionPrep,
  getLead
} from "@/lib/demo-data";

export function generateStaticParams() {
  return dealDistributionPreps.map((prep) => ({ distributionId: prep.id }));
}

export default async function DealDistributionDetailPage({
  params
}: {
  params: Promise<{ distributionId: string }>;
}) {
  const { distributionId } = await params;
  const prep = getDealDistributionPrep(distributionId);
  if (!prep) notFound();
  const deal = getDeal(prep.dealId);
  const lead = deal ? getLead(deal.leadId) : undefined;
  const buyer = getBuyer(prep.buyerId);
  const priority = getBuyerDealPriority(prep.buyerPriorityId);
  const sheet = prep.privateDealSheetDraft;

  return (
    <div className="page">
      <PageHeader
        eyebrow={prep.draftStatus}
        title={`${prep.id} / ${buyer?.company ?? prep.buyerId}`}
        description="Distribution prep is draft-only. The sanitized deal sheet hides seller data, lead source, assignment logic, internal spread strategy, and compliance internals."
      />
      <div className="metric-grid">
        <MetricCard label="Priority score" value={String(priority?.priorityScore ?? 0)} detail={`Rank ${priority?.rank ?? "n/a"}`} />
        <MetricCard label="Asking price" value={formatCurrency(sheet.askingPrice ?? 0)} detail="Buyer-facing asking price" />
        <MetricCard label="Buyer margin" value={formatCurrency(sheet.buyerMarginEstimate ?? 0)} detail="Estimated range-based margin" />
        <MetricCard label="Live send" value="off" detail="No provider action in V9" />
      </div>

      <div className="grid-two">
        <Section title="Sanitized Deal Sheet">
          <table className="data-table">
            <tbody>
              <tr><th>Property</th><td>{sheet.propertySummary.city}, {sheet.propertySummary.state} {sheet.propertySummary.zipCode}</td></tr>
              <tr><th>Type</th><td>{sheet.propertySummary.propertyType}</td></tr>
              <tr><th>Beds / Baths / Sqft</th><td>{sheet.propertySummary.beds} / {sheet.propertySummary.baths} / {sheet.propertySummary.sqft}</td></tr>
              <tr><th>ARV range</th><td className="money">{formatCurrency(sheet.arvRange.low ?? 0)} - {formatCurrency(sheet.arvRange.high ?? 0)}</td></tr>
              <tr><th>Repair range</th><td className="money">{formatCurrency(sheet.repairEstimateRange.low ?? 0)} - {formatCurrency(sheet.repairEstimateRange.high ?? 0)}</td></tr>
              <tr><th>Availability</th><td>{sheet.availabilityStatus}</td></tr>
              <tr><th>Access</th><td>{sheet.accessInstructionsPlaceholder}</td></tr>
              <tr><th>Proof / inspection notes</th><td>{sheet.proofInspectionNotesPlaceholder}</td></tr>
            </tbody>
          </table>
        </Section>
        <Section title="Distribution Gate">
          <div className="record-list">
            <RecordCard title="Seller/private exposure" meta="No seller identity, contact, source, motivation, or notes." right={<Pill tone="green">hidden</Pill>} />
            <RecordCard title="Live send" meta={prep.liveSendAllowed ? "Enabled" : "Disabled"} right={<Pill tone="red">off</Pill>} />
            <RecordCard title="Bulk send" meta={prep.bulkBlastAllowed ? "Enabled" : "Disabled"} right={<Pill tone="red">off</Pill>} />
            <RecordCard title="Approval" meta={prep.approvalStatus} right={<Pill tone="gold">owner</Pill>} />
            <RecordCard title="Blocks" meta={prep.blockedReasons.length ? prep.blockedReasons.join(", ") : "No distribution blockers"} right={<Pill tone={prep.blockedReasons.length ? "red" : "green"}>{prep.blockedReasons.length}</Pill>} />
          </div>
        </Section>
      </div>

      <Section title="Draft Assets">
        <div className="record-list">
          <RecordCard title="Buyer email draft" meta={prep.buyerDealEmailDraft} right={<Pill>draft</Pill>} />
          <RecordCard title="Buyer SMS draft" meta={prep.buyerSmsDraft} right={<Pill>draft</Pill>} />
          <RecordCard title="Buyer call notes" meta={prep.buyerCallNotes} right={<Pill>notes</Pill>} />
          <RecordCard title="Source deal" meta={`${lead?.city ?? "Property"} ${deal?.id ?? prep.dealId}`} right={<Pill>{prep.dealId}</Pill>} />
        </div>
      </Section>
    </div>
  );
}
