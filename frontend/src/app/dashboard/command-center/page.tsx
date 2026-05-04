import { DealTable } from "@/components/DealTable";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { assignmentReadyRecords, buyerPofGaps, complianceRecords, contractPrepBlocked, deals, formatCurrency, hotDeals, hotSellerLeads, leads, offerPackets, sellerInteractions, staleSellerFollowUps, titleHandoffPackets } from "@/lib/demo-data";
import { buyerInterests, buyerPortalBlockedDeals, buyerVisibleDeals } from "@/lib/demo-data";

export default function CommandCenterPage() {
  const staleFollowUps = leads.filter((lead) => lead.stage === "follow_up");
  const needsUnderwriting = leads.filter((lead) => ["researched", "offer_needed"].includes(lead.stage));
  return (
    <div className="page">
      <PageHeader
        eyebrow="Operations Command"
        title="Ranked attention queue"
        description="Wholesale Prime routes hot deals, underwriting gaps, buyer-ready opportunities, stale follow-ups, and compliance blockers."
      />
      <div className="metric-grid">
        <MetricCard label="Top hot deals" value={String(hotDeals.length)} detail="Projected 10K+ assignment fees" />
        <MetricCard label="Underwriting queue" value={String(needsUnderwriting.length)} detail="Research or offer-needed leads" />
        <MetricCard label="Stale follow-ups" value={String(staleFollowUps.length)} detail="Draft-only touchpoint planning" />
        <MetricCard label="Risk blocks" value={String(complianceRecords.length)} detail="Owner plus compliance review" />
      </div>
      <div className="metric-grid">
        <MetricCard label="Hot sellers" value={String(hotSellerLeads.length)} detail="Seller temp and motivation" />
        <MetricCard label="Seller follow-ups" value={String(staleSellerFollowUps.length)} detail="Owner-reviewed drafts" />
        <MetricCard label="Objections tracked" value={String(sellerInteractions.length)} detail="Discovery records" />
        <MetricCard label="Offer packet blocks" value={String(offerPackets.filter((packet) => !packet.packetPrepAllowed).length)} detail="Approval status visible" />
      </div>
      <div className="metric-grid">
        <MetricCard label="Contract prep blocks" value={String(contractPrepBlocked.length)} detail="Accepted terms and approvals" />
        <MetricCard label="Title handoff packets" value={String(titleHandoffPackets.length)} detail="Draft-only packets" />
        <MetricCard label="Assignment-ready" value={String(assignmentReadyRecords.length)} detail="POF and compliance clear" />
        <MetricCard label="Buyer POF gaps" value={String(buyerPofGaps.length)} detail="Readiness blocked" />
      </div>
      <div className="grid-two">
        <Section title="Hot Opportunities">
          <DealTable limit={8} />
        </Section>
        <Section title="Next Best Actions">
          <div className="record-list">
            {[
              ["critical", "Review under-contract spreads", `${formatCurrency(deals[1].projectedAssignmentFee)} projected on deal-002`],
              ["critical", "Review buyer portal intent queue", `${buyerInterests.length} buyer intents need owner handling`],
              ["high", "Route inherited-property review", "Deal-005 needs authority and title review"],
              ["high", "Fix buyer margin exception", "Deal-006 is blocked by spread and margin risk"],
              ["high", "Review seller acquisition queue", `${hotSellerLeads.length} hot sellers need draft-only next steps`],
              ["high", "Clear contract prep blocks", `${contractPrepBlocked.length} contract controls need missing approval, compliance, or title items`],
              ["high", "Resolve buyer POF gaps", `${buyerPofGaps.length} readiness records need POF verification`],
              ["normal", "Review title handoff packets", `${titleHandoffPackets.length} title packets are draft-only and not submitted`],
              ["high", "Clear buyer portal publishing blocks", `${buyerPortalBlockedDeals.length} deals are blocked from buyer visibility`],
              ["normal", "Monitor visible deal rooms", `${buyerVisibleDeals.length} sanitized deals are currently visible`],
              ["normal", "Prepare draft follow-up notes", `${staleFollowUps.length} seller records need timing recommendations`]
            ].map(([priority, title, meta]) => (
              <RecordCard key={title} title={title} meta={meta} right={<Pill tone={priority === "critical" ? "red" : "gold"}>{priority}</Pill>} />
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
