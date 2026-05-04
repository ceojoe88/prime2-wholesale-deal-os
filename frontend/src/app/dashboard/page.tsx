import { DealTable } from "@/components/DealTable";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  activeDealRooms,
  assignmentFeeAttributions,
  assignmentReadyDealRooms,
  assignmentReadyRecords,
  blockedDealRooms,
  blockedDistributionPreps,
  buyerMatches,
  buyerInterests,
  buyerDemandProfiles,
  buyerReadyDealsFromDemand,
  buyerPortalBlockedDeals,
  buyerVisibleDeals,
  buyerPriorityPofGaps,
  buyerPofGaps,
  blockedCommunicationAttempts,
  closingNextBestActions,
  closingReadyDealRooms,
  communicationDrafts,
  communicationDraftsNeedingSafety,
  communicationDryRunsNeedingApproval,
  communicationRiskQueue,
  complianceRecords,
  contractReadyDeals,
  contractControls,
  contractPrepBlocked,
  contractPrepReady,
  dealEvidencePackets,
  dealsNeedingPriceAdjustment,
  distributionDraftsPendingApproval,
  dealsNeedingEvidenceOwnerReview,
  evidenceFeesAtRisk,
  divisions,
  fastestPathToContract,
  formatCurrency,
  hotDeals,
  hotSellerLeads,
  highReadinessNegotiations,
  highestDemandZipCodes,
  leads,
  offerReadyPackets,
  offerPackets,
  offerConversionDealsAtRisk,
  missingEvidencePackets,
  projected10kContractsReady,
  projectedAssignmentFeesAtRisk,
  projectedEvidenceAssignmentFees,
  projectedAssignmentTotal,
  reviewPacketBlocks,
  reviewPacketPrepReady,
  reviewPacketPreps,
  blockedSellerVisibilityOffers,
  sellerDocumentChecklistQueue,
  sellerInteractions,
  sellerPortalQuestions,
  sellerResponseQueue,
  sellerVisibleOffers,
  stalledNegotiations,
  staleSellerFollowUps,
  sentOrMockSentCommunicationAttempts,
  titleHandoffPackets,
  titleReviewCoordinations,
  titleReviewMissingItems,
  titleReviewOwnerApprovalNeeded,
  tenKDealsWithStrongBuyerDemand,
  fastCloseBuyerList,
  underContractDeals,
  verified10kAssignmentFeeOpportunities,
  verifiedAssignmentFees
} from "@/lib/demo-data";

export default function DashboardPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Wholesale Prime"
        title="Daily acquisition command"
        description="Hot opportunities, spread protection, buyer demand, and compliance risk are ranked for owner approval."
      />

      <div className="metric-grid">
        <MetricCard label="Active leads" value={String(leads.length)} detail="30 motivated seller records seeded" />
        <MetricCard label="Hot 10K+ targets" value={String(hotDeals.length)} detail="Owner review before offer prep" />
        <MetricCard label="Projected fees" value={formatCurrency(projectedAssignmentTotal)} detail="Across active demo deals" />
        <MetricCard label="Compliance alerts" value={String(complianceRecords.length)} detail="Blocked until reviewed" />
      </div>

      <div className="command-band">
        <strong>Wholesale Prime briefing</strong>
        <div className="pill-row">
          <Pill tone="green">{underContractDeals.length} under contract</Pill>
          <Pill tone="gold">{buyerMatches.length} draft buyer matches</Pill>
          <Pill tone="red">No live outreach in v1</Pill>
        </div>
        <span className="muted">
          Prioritize 10K+ spreads with verified buyer margin, then route compliance-risk examples before assignment packet prep.
        </span>
      </div>

      <div className="grid-two">
        <Section title="Top Deal Queue">
          <DealTable limit={5} />
        </Section>
        <Section title="Manager Load">
          <div className="record-list">
            {divisions.slice(0, 5).map((division) => (
              <RecordCard
                key={division.id}
                title={division.managerName}
                meta={division.name}
                right={<Pill tone={division.riskFlags.length ? "gold" : "green"}>{division.workload} active</Pill>}
              >
                <span className="record-meta">{division.nextBestAction}</span>
              </RecordCard>
            ))}
          </div>
        </Section>
      </div>

      <Section title="V2 Buyer Portal Gate">
        <div className="grid-three">
          <RecordCard title="Buyer-visible deals" meta={`${buyerVisibleDeals.length} sanitized deal rooms`} right={<Pill tone="green">visible</Pill>} />
          <RecordCard title="Buyer interest queue" meta={`${buyerInterests.length} draft intent records`} right={<Pill tone="gold">owner review</Pill>} />
          <RecordCard title="Blocked from portal" meta={`${buyerPortalBlockedDeals.length} deals have gate reasons`} right={<Pill tone="red">blocked</Pill>} />
        </div>
      </Section>

      <Section title="V3 Seller Acquisition Gate">
        <div className="grid-three">
          <RecordCard title="Seller temperature" meta={`${hotSellerLeads.length} hot sellers`} right={<Pill tone="red">hot</Pill>} />
          <RecordCard title="Follow-up urgency" meta={`${staleSellerFollowUps.length} stale or urgent follow-ups`} right={<Pill tone="gold">review</Pill>} />
          <RecordCard title="Offer readiness" meta={`${offerReadyPackets.length}/${offerPackets.length} packets ready`} right={<Pill tone="green">gated</Pill>} />
        </div>
        <div className="record-list">
          {sellerInteractions.slice(0, 3).map((interaction) => (
            <RecordCard key={interaction.id} title={interaction.nextBestSellerAction} meta={`${interaction.objectionStatus} / ${interaction.followUpUrgency}`} right={<Pill>{interaction.sellerTemperatureScore}</Pill>} />
          ))}
        </div>
      </Section>

      <Section title="V4 Contract and Title Control">
        <div className="grid-three">
          <RecordCard title="Contracts in prep" meta={`${contractControls.length} control records`} right={<Pill tone="gold">owner gated</Pill>} />
          <RecordCard title="Title handoff packets" meta={`${titleHandoffPackets.length} draft packets`} right={<Pill tone="red">no submission</Pill>} />
          <RecordCard title="Assignment-ready deals" meta={`${assignmentReadyRecords.length} cleared records`} right={<Pill tone="green">ready</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="Blocked contract prep" meta={`${contractPrepBlocked.length} records have gate reasons`} right={<Pill tone="red">blocked</Pill>} />
          <RecordCard title="Prep-ready controls" meta={`${contractPrepReady.length} records can be drafted`} right={<Pill tone="green">draft only</Pill>} />
          <RecordCard title="Buyer POF gaps" meta={`${buyerPofGaps.length} readiness records need POF review`} right={<Pill tone="gold">review</Pill>} />
        </div>
      </Section>

      <Section title="V5 Communication Gate">
        <div className="grid-three">
          <RecordCard title="Drafts needing safety" meta={`${communicationDraftsNeedingSafety.length}/${communicationDrafts.length} drafts need safety review`} right={<Pill tone="gold">check</Pill>} />
          <RecordCard title="Dry-runs needing approval" meta={`${communicationDryRunsNeedingApproval.length} receipts waiting for owner`} right={<Pill tone="gold">owner</Pill>} />
          <RecordCard title="Blocked attempts" meta={`${blockedCommunicationAttempts.length} audited with no provider call`} right={<Pill tone="red">blocked</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="Mock-sent attempts" meta={`${sentOrMockSentCommunicationAttempts.length} placeholder sends`} right={<Pill tone="green">mock</Pill>} />
          <RecordCard title="Communication risk queue" meta={`${communicationRiskQueue.length} risky drafts`} right={<Pill tone="red">risk</Pill>} />
          <RecordCard title="Global live flag" meta="Default off; no bulk campaigns or buyer blasts." right={<Pill tone="red">off</Pill>} />
        </div>
      </Section>

      <Section title="V6 Seller Offer Room">
        <div className="grid-three">
          <RecordCard title="Seller-visible offers" meta={`${sellerVisibleOffers.length} sanitized offer rooms`} right={<Pill tone="green">visible</Pill>} />
          <RecordCard title="Seller questions" meta={`${sellerPortalQuestions.length} questions need operator review`} right={<Pill tone="gold">review</Pill>} />
          <RecordCard title="Document checklist queue" meta={`${sellerDocumentChecklistQueue.length} offer checklists tracked`} right={<Pill>checklist</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="Seller response queue" meta={`${sellerResponseQueue.length} intake records pending review`} right={<Pill tone="gold">intake</Pill>} />
          <RecordCard title="Blocked seller visibility" meta={`${blockedSellerVisibilityOffers.length} offers blocked by gate reasons`} right={<Pill tone="red">blocked</Pill>} />
          <RecordCard title="Negotiation automation" meta="Off; no acceptance or status change from the portal." right={<Pill tone="red">off</Pill>} />
        </div>
      </Section>

      <Section title="V7 Unified Deal Room">
        <div className="grid-three">
          <RecordCard title="Active deal rooms" meta={`${activeDealRooms.length} internal coordination rooms`} right={<Pill>source truth</Pill>} />
          <RecordCard title="Closing-ready deals" meta={`${closingReadyDealRooms.length} rooms have all gates clear`} right={<Pill tone="green">ready</Pill>} />
          <RecordCard title="Blocked deals" meta={`${blockedDealRooms.length} rooms have blocker records`} right={<Pill tone="red">blocked</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="Assignment-ready rooms" meta={`${assignmentReadyDealRooms.length} tied to assignment readiness`} right={<Pill tone="green">ready</Pill>} />
          <RecordCard title="Next best actions" meta={`${closingNextBestActions.length} recommendations queued`} right={<Pill tone="gold">internal</Pill>} />
          <RecordCard title="Projected fees at risk" meta={formatCurrency(projectedAssignmentFeesAtRisk)} right={<Pill tone="red">at risk</Pill>} />
        </div>
      </Section>

      <Section title="V8 Evidence and Fee Attribution">
        <div className="grid-three">
          <RecordCard title="Evidence packets" meta={`${dealEvidencePackets.length} proof-backed packets`} right={<Pill>internal</Pill>} />
          <RecordCard title="Verified assignment fees" meta={formatCurrency(verifiedAssignmentFees)} right={<Pill tone="green">verified</Pill>} />
          <RecordCard title="Evidence fees at risk" meta={formatCurrency(evidenceFeesAtRisk)} right={<Pill tone="red">at risk</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="Missing evidence" meta={`${missingEvidencePackets.length} packets need source records`} right={<Pill tone="red">missing</Pill>} />
          <RecordCard title="Owner evidence review" meta={`${dealsNeedingEvidenceOwnerReview.length} packets need owner review`} right={<Pill tone="gold">review</Pill>} />
          <RecordCard title="10K+ verified opportunities" meta={`${verified10kAssignmentFeeOpportunities.length}/${assignmentFeeAttributions.length} attributed records`} right={<Pill tone="green">{formatCurrency(projectedEvidenceAssignmentFees)}</Pill>} />
        </div>
      </Section>

      <Section title="V9 Buyer Demand and Distribution Prep">
        <div className="grid-three">
          <RecordCard title="Buyer demand profiles" meta={`${buyerDemandProfiles.length} buyers scored for speed and fit`} right={<Pill tone="green">ranked</Pill>} />
          <RecordCard title="Highest-demand zip" meta={`${highestDemandZipCodes[0]?.zipCode ?? "n/a"} leads current buyer demand`} right={<Pill>{highestDemandZipCodes[0]?.demandScore ?? 0}</Pill>} />
          <RecordCard title="Fast-close buyers" meta={`${fastCloseBuyerList.length} verified buyers can close in 10 days or faster`} right={<Pill tone="green">fast</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="Distribution approvals" meta={`${distributionDraftsPendingApproval.length} one-buyer drafts need owner review`} right={<Pill tone="gold">draft</Pill>} />
          <RecordCard title="Distribution blocks" meta={`${blockedDistributionPreps.length} drafts blocked by safety or publication gates`} right={<Pill tone="red">blocked</Pill>} />
          <RecordCard title="Strong-demand 10K+ deals" meta={`${tenKDealsWithStrongBuyerDemand.length} deals protect spread with buyer fit`} right={<Pill tone="green">ready</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="Buyer-ready demand" meta={`${buyerReadyDealsFromDemand.length} deals have strong buyer fit and visible rooms`} right={<Pill tone="green">ready</Pill>} />
          <RecordCard title="Buyer priority POF gaps" meta={`${buyerPriorityPofGaps.length} rankings need POF refresh`} right={<Pill tone="gold">review</Pill>} />
          <RecordCard title="Bulk distribution" meta="Blocked; no campaigns, blasts, or automatic buyer outreach." right={<Pill tone="red">off</Pill>} />
        </div>
      </Section>

      <Section title="V10 Offer To Contract Conversion Gate">
        <div className="grid-three">
          <RecordCard title="Contract-ready deals" meta={`${contractReadyDeals.length} deals ready for external drafting review`} right={<Pill tone="green">ready</Pill>} />
          <RecordCard title="High readiness sellers" meta={`${highReadinessNegotiations.length} sellers score high or contract-ready`} right={<Pill tone="gold">seller ready</Pill>} />
          <RecordCard title="Stalled negotiations" meta={`${stalledNegotiations.length} records need safe next-move review`} right={<Pill tone="red">stalled</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="Price adjustments" meta={`${dealsNeedingPriceAdjustment.length} deals have safe-range adjustment recommendations`} right={<Pill tone="gold">review</Pill>} />
          <RecordCard title="Conversion risk gates" meta={`${offerConversionDealsAtRisk.length} contract-ready states have blockers`} right={<Pill tone="red">blocked</Pill>} />
          <RecordCard title="10K+ contracts ready" meta={`${projected10kContractsReady.length} conversion states preserve 10K+ projected spreads`} right={<Pill tone="green">10K+</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="Fastest path to contract" meta={fastestPathToContract[0]?.actions.join(", ") ?? "No conversion path queued"} right={<Pill tone="gold">recommend</Pill>} />
          <RecordCard title="Contract creation" meta="Blocked; readiness does not generate or execute contracts." right={<Pill tone="red">off</Pill>} />
          <RecordCard title="Negotiation automation" meta="Blocked; next moves are owner-reviewed recommendations only." right={<Pill tone="red">off</Pill>} />
        </div>
      </Section>

      <Section title="V11 Title Company Attorney Review Gate">
        <div className="grid-three">
          <RecordCard title="Review coordination records" meta={`${titleReviewCoordinations.length} title/attorney review records`} right={<Pill>internal</Pill>} />
          <RecordCard title="Review packet ready" meta={`${reviewPacketPrepReady.length}/${reviewPacketPreps.length} draft packets pass V10 review gates`} right={<Pill tone="green">draft</Pill>} />
          <RecordCard title="Blocked reviews" meta={`${reviewPacketBlocks.length} packets blocked before review prep`} right={<Pill tone="red">blocked</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="Missing items" meta={`${titleReviewMissingItems.length} records need documents or approvals`} right={<Pill tone="gold">queue</Pill>} />
          <RecordCard title="Owner approvals" meta={`${titleReviewOwnerApprovalNeeded.length} review records need owner approval`} right={<Pill tone="gold">owner</Pill>} />
          <RecordCard title="Title submission" meta="Blocked; no documents, title email, legal advice, or contract execution." right={<Pill tone="red">off</Pill>} />
        </div>
      </Section>
    </div>
  );
}
