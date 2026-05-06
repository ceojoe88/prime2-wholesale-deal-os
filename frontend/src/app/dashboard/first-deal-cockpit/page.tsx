import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  firstDealCallPriorityLeads,
  firstDealCoachCards,
  firstDealContractReadyChecklist,
  firstDealEvidenceRecords,
  firstDealExecutionBatch,
  firstDealOfferBoard,
  firstDealSafetyCards,
  firstDealTopImportedLeads,
  formatCurrency
} from "@/lib/demo-data";

export default function FirstDealCockpitPage() {
  const motivated = firstDealExecutionBatch.motivatedSellers;
  const ownerOffers = firstDealOfferBoard.filter((offer) => offer.decisionStatus === "ready_for_owner_review");
  const tenKCandidates = firstDealEvidenceRecords.filter(
    (record) => record.projectedAssignmentFee >= firstDealExecutionBatch.targetAssignmentFee
  );
  return (
    <div className="page">
      <PageHeader
        eyebrow="V31 First Deal Cockpit"
        title="First real deal execution board"
        description="Prime 2 guides the owner through lead import, QA, seller calls, underwriting, offer review, buyer validation, external review prep, evidence, and field-test learning."
      />
      <div className="metric-grid">
        <MetricCard label="Batch status" value={firstDealExecutionBatch.batchStatus} detail={firstDealExecutionBatch.batchName} />
        <MetricCard label="Call-priority leads" value={String(firstDealCallPriorityLeads.length)} detail="Top owner-call targets" />
        <MetricCard label="Motivated sellers" value={String(motivated)} detail="From logged outcomes" />
        <MetricCard label="10K candidates" value={String(tenKCandidates.length)} detail="Projected, evidence-gated" />
      </div>

      <Section title="Safety Boundary">
        <div className="metric-grid">
          {firstDealSafetyCards.map((card) => (
            <RecordCard key={card.label} title={card.label} meta={card.detail} right={<Pill tone={card.value === "off" ? "red" : "gold"}>{card.value}</Pill>} />
          ))}
        </div>
      </Section>

      <div className="grid-two">
        <Section title="Execution Flow">
          <div className="record-list">
            <RecordCard title="Seller Calls" meta={`${firstDealExecutionBatch.callsCompleted} logged outcomes`} right={<Link href="/dashboard/first-deal-cockpit/calls">Open</Link>} />
            <RecordCard title="Offer Decisions" meta={`${ownerOffers.length} ready for owner review`} right={<Link href="/dashboard/first-deal-cockpit/offers">Open</Link>} />
            <RecordCard title="Buyer Validation" meta="POF, price fit, reliability, margin" right={<Link href="/dashboard/first-deal-cockpit/buyer-validation">Open</Link>} />
            <RecordCard title="Contract-Ready Prep" meta={`${firstDealContractReadyChecklist.filter((item) => item.state.contractReady).length} external-process candidates`} right={<Link href="/dashboard/first-deal-cockpit/contract-ready">Open</Link>} />
            <RecordCard title="Evidence Tracker" meta={formatCurrency(firstDealExecutionBatch.projectedAssignmentFees)} right={<Link href="/dashboard/first-deal-cockpit/evidence">Open</Link>} />
            <RecordCard title="Field-Test Report" meta="Batch learning and next-batch recommendations" right={<Link href="/dashboard/first-deal-cockpit/report">Open</Link>} />
          </div>
        </Section>
        <Section title="Prime 2 Execution Coach">
          <div className="record-list">
            {firstDealCoachCards.map((card) => (
              <RecordCard key={card.title} title={card.title} meta={card.detail} right={<Pill tone={card.tone}>{card.tone === "green" ? "ready" : "review"}</Pill>} />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Top Imported Leads">
        <table className="data-table">
          <thead>
            <tr>
              <th>Lead</th>
              <th>Property</th>
              <th>QA</th>
              <th>Contact</th>
              <th>Next Action</th>
            </tr>
          </thead>
          <tbody>
            {firstDealTopImportedLeads.slice(0, 10).map((lead) => (
              <tr key={lead.id}>
                <td>{lead.ownerName}<div className="record-meta">{lead.leadSource}</div></td>
                <td>{lead.property}</td>
                <td><Pill tone={lead.qaScore >= 80 ? "green" : "gold"}>{lead.qaScore}</Pill></td>
                <td>{lead.contactabilityScore}</td>
                <td>{lead.recommendedNextAction}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
