import { DealTable } from "@/components/DealTable";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  activeDealRooms,
  approvedAutoExecutionRules,
  approvedTemplateLibrary,
  autoExecutionAuditTrail,
  autoExecutionBlockedAttempts,
  automationRules,
  autonomousAgentTasks,
  autonomyEscalationQueue,
  autonomyLevel4Rules,
  autonomyOpenTasks,
  assignmentFeeAttributions,
  assignmentReadyDealRooms,
  assignmentReadyRecords,
  blockedCommunicationAttempts,
  blockedDealRooms,
  blockedAutomationAttempts,
  blockedSellerVisibilityOffers,
  contractReadyDeals,
  buyerInterests,
  buyerDemandProfiles,
  buyerReadyDealsFromDemand,
  buyerPofGaps,
  buyerPortalBlockedDeals,
  buyerPriorityPofGaps,
  buyerVisibleDeals,
  closingNextBestActions,
  closingReadyDealRooms,
  communicationDraftsNeedingSafety,
  communicationDryRunsNeedingApproval,
  complianceRecords,
  contractPrepBlocked,
  dailyCommandBriefings,
  dealEvidencePackets,
  dealsNeedingPriceAdjustment,
  blockedDistributionPreps,
  dealsNeedingEvidenceOwnerReview,
  distributionDraftsPendingApproval,
  deals,
  evidenceFeesAtRisk,
  fastestPathToContract,
  fastCloseBuyerList,
  fastestBuyerVelocity,
  formatCurrency,
  hotDeals,
  hotSellerLeads,
  highReadinessNegotiations,
  highestDemandZipCodes,
  leads,
  offerPackets,
  offerConversionDealsAtRisk,
  missingEvidencePackets,
  projected10kContractsReady,
  projectedAssignmentFeesAtRisk,
  projectedEvidenceAssignmentFees,
  reviewPacketBlocks,
  reviewPacketPrepReady,
  reviewPacketPreps,
  sellerDocumentChecklistQueue,
  sellerInteractions,
  sellerPortalQuestions,
  sellerResponseQueue,
  sellerVisibleOffers,
  stalledNegotiations,
  staleSellerFollowUps,
  titleHandoffPackets,
  titleReviewCoordinations,
  titleReviewMissingItems,
  titleReviewOwnerApprovalNeeded,
  tenKDealsWithStrongBuyerDemand,
  verified10kAssignmentFeeOpportunities,
  verifiedAssignmentFees,
  buyerAccelerationBlockedRecords,
  buyerAccelerationPofGaps,
  buyerAccelerationReadyDeals,
  buyerResponsesNeedingOwnerAction,
  buyerSequencesBlocked
} from "@/lib/demo-data";

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
      <div className="metric-grid">
        <MetricCard label="Comm safety queue" value={String(communicationDraftsNeedingSafety.length)} detail="Drafts needing check" />
        <MetricCard label="Comm approvals" value={String(communicationDryRunsNeedingApproval.length)} detail="Dry-runs waiting" />
        <MetricCard label="Blocked comms" value={String(blockedCommunicationAttempts.length)} detail="No provider calls" />
        <MetricCard label="Live flag" value="off" detail="Default controlled mode" />
      </div>
      <div className="metric-grid">
        <MetricCard label="Seller-visible offers" value={String(sellerVisibleOffers.length)} detail="Sanitized offer rooms" />
        <MetricCard label="Seller questions" value={String(sellerPortalQuestions.length)} detail="Operator review" />
        <MetricCard label="Seller docs" value={String(sellerDocumentChecklistQueue.length)} detail="Checklist queue" />
        <MetricCard label="Seller gate blocks" value={String(blockedSellerVisibilityOffers.length)} detail="Visibility reasons" />
      </div>
      <div className="metric-grid">
        <MetricCard label="Deal rooms" value={String(activeDealRooms.length)} detail="Unified coordination records" />
        <MetricCard label="Closing-ready" value={String(closingReadyDealRooms.length)} detail="Buyer, seller, title, compliance clear" />
        <MetricCard label="Blocked rooms" value={String(blockedDealRooms.length)} detail="Blocker engine queue" />
        <MetricCard label="Fees at risk" value={formatCurrency(projectedAssignmentFeesAtRisk)} detail="Projected spreads behind blockers" />
      </div>
      <div className="metric-grid">
        <MetricCard label="Evidence packets" value={String(dealEvidencePackets.length)} detail="Proof-backed deal records" />
        <MetricCard label="Verified fees" value={formatCurrency(verifiedAssignmentFees)} detail="Approved evidence only" />
        <MetricCard label="Evidence fee risk" value={formatCurrency(evidenceFeesAtRisk)} detail="Missing proof or review" />
        <MetricCard label="10K+ verified" value={String(verified10kAssignmentFeeOpportunities.length)} detail="Actual source-number flag" />
      </div>
      <div className="metric-grid">
        <MetricCard label="Buyer demand profiles" value={String(buyerDemandProfiles.length)} detail="V9 buyer intelligence records" />
        <MetricCard label="Fast-close buyers" value={String(fastCloseBuyerList.length)} detail="Verified POF, 10 days or faster" />
        <MetricCard label="Distribution approvals" value={String(distributionDraftsPendingApproval.length)} detail="Drafts waiting on owner review" />
        <MetricCard label="10K+ strong demand" value={String(tenKDealsWithStrongBuyerDemand.length)} detail="Buyer fit plus source-number spread" />
      </div>
      <div className="metric-grid">
        <MetricCard label="Contract-ready" value={String(contractReadyDeals.length)} detail="External drafting-ready only" />
        <MetricCard label="High readiness sellers" value={String(highReadinessNegotiations.length)} detail="Acceptance score above threshold" />
        <MetricCard label="Stalled negotiations" value={String(stalledNegotiations.length)} detail="Needs owner positioning review" />
        <MetricCard label="10K+ contracts ready" value={String(projected10kContractsReady.length)} detail="Projected spreads protected" />
      </div>
      <div className="metric-grid">
        <MetricCard label="Title review records" value={String(titleReviewCoordinations.length)} detail="Attorney/title coordination" />
        <MetricCard label="Review packets ready" value={String(reviewPacketPrepReady.length)} detail="Draft-only packets" />
        <MetricCard label="Review packet blocks" value={String(reviewPacketBlocks.length)} detail="No submission before gates" />
        <MetricCard label="Review missing items" value={String(titleReviewMissingItems.length)} detail="Documents or approvals" />
      </div>
      <div className="metric-grid">
        <MetricCard label="Autonomy rules" value={String(automationRules.length)} detail="Level 2-4 guarded workflows" />
        <MetricCard label="Autonomy tasks" value={`${autonomyOpenTasks.length}/${autonomousAgentTasks.length}`} detail="Open internal prep queue" />
        <MetricCard label="Autonomy escalations" value={String(autonomyEscalationQueue.length)} detail="Owner review recommendations" />
        <MetricCard label="Automation blocks" value={String(blockedAutomationAttempts.length)} detail="Audited no-execution attempts" />
      </div>
      <div className="metric-grid">
        <MetricCard label="Auto-exec rules" value={String(approvedAutoExecutionRules.length)} detail="Approved controlled rules" />
        <MetricCard label="Auto templates" value={String(approvedTemplateLibrary.length)} detail="Approved safe templates" />
        <MetricCard label="Auto-exec blocks" value={String(autoExecutionBlockedAttempts.length)} detail="Bulk/unsafe paths blocked" />
        <MetricCard label="Auto audit" value={String(autoExecutionAuditTrail.length)} detail="Attempt audit records" />
      </div>
      <div className="metric-grid">
        <MetricCard label="Buyer acceleration ready" value={String(buyerAccelerationReadyDeals.length)} detail="Controlled one-recipient distribution" />
        <MetricCard label="Buyer acceleration blocks" value={String(buyerAccelerationBlockedRecords.length)} detail="Visibility, margin, approval, or compliance" />
        <MetricCard label="Buyer POF response gaps" value={String(buyerAccelerationPofGaps.length)} detail="Routed before access or offer intent" />
        <MetricCard label="Top buyer velocity" value={String(fastestBuyerVelocity[0]?.velocityScore ?? 0)} detail="Fast-close ranking score" />
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
              ["high", "Clear communication safety queue", `${communicationDraftsNeedingSafety.length} drafts need safety checks before dry-run`],
              ["high", "Review communication approvals", `${communicationDryRunsNeedingApproval.length} dry-run receipts need owner approval`],
              ["normal", "Inspect blocked communication attempts", `${blockedCommunicationAttempts.length} blocked attempts were audited without provider calls`],
              ["high", "Review seller offer room questions", `${sellerResponseQueue.length} seller intake records need operator review`],
              ["high", "Clear seller visibility blocks", `${blockedSellerVisibilityOffers.length} seller offers blocked by approval, review, or safety gates`],
              ["critical", "Resolve closing coordination blockers", `${blockedDealRooms.length} unified rooms are blocked`],
              ["high", "Review closing-ready deal rooms", `${closingReadyDealRooms.length} room can move with owner-controlled next steps`],
              ["high", "Protect fees at risk", `${formatCurrency(projectedAssignmentFeesAtRisk)} projected assignment fees sit behind blockers`],
              ["normal", "Review coordination recommendations", `${closingNextBestActions.length} next best actions are internal recommendations only`],
              ["normal", "Monitor assignment-ready rooms", `${assignmentReadyDealRooms.length} room is assignment-ready inside V7 coordination`],
              ["critical", "Review evidence-backed fees", `${formatCurrency(projectedEvidenceAssignmentFees)} projected across ${assignmentFeeAttributions.length} attribution records`],
              ["high", "Clear missing evidence", `${missingEvidencePackets.length} packets need source-record support`],
              ["high", "Approve evidence review queue", `${dealsNeedingEvidenceOwnerReview.length} packets need owner evidence review`],
              ["normal", "Protect verified assignment fees", `${formatCurrency(verifiedAssignmentFees)} currently verified from source numbers`],
              ["critical", "Review buyer demand ranking", `${highestDemandZipCodes[0]?.zipCode ?? "n/a"} is the current highest-demand zip`],
              ["high", "Approve distribution drafts", `${distributionDraftsPendingApproval.length} buyer distribution drafts need owner review`],
              ["high", "Resolve buyer ranking POF gaps", `${buyerPriorityPofGaps.length} priority records need POF refresh or verification`],
              ["high", "Review buyer-ready demand", `${buyerReadyDealsFromDemand.length} deals have strong buyer demand and visible deal rooms`],
              ["normal", "Monitor fast-close buyer list", `${fastCloseBuyerList.length} verified buyers can close in 10 days or faster`],
              ["high", "Clear blocked distribution preps", `${blockedDistributionPreps.length} drafts are blocked by compliance or publication gates`],
              ["critical", "Review contract-ready conversion queue", `${contractReadyDeals.length} deals are ready for external drafting review`],
              ["high", "Clear stalled negotiations", `${stalledNegotiations.length} negotiations need a safer next move`],
              ["high", "Review price adjustments", `${dealsNeedingPriceAdjustment.length} deals have adjustment recommendations inside safe range`],
              ["high", "Protect 10K+ contract-ready opportunities", `${projected10kContractsReady.length} ready states preserve a 10K+ projected fee`],
              ["high", "Clear offer conversion risk gates", `${offerConversionDealsAtRisk.length} conversion states have blockers before contract-ready`],
              ["normal", "Review fastest path to contract", fastestPathToContract[0]?.actions.join(", ") ?? "No conversion path queued"],
              ["high", "Prepare title review packets", `${reviewPacketPrepReady.length}/${reviewPacketPreps.length} review packets are draft-ready`],
              ["high", "Clear title review missing items", `${titleReviewMissingItems.length} title/attorney review records need missing items resolved`],
              ["high", "Review title approval queue", `${titleReviewOwnerApprovalNeeded.length} review records need owner approval`],
              ["normal", "Inspect title review blocks", `${reviewPacketBlocks.length} packets remain blocked with no document submission`],
              ["critical", "Review autonomy escalations", `${autonomyEscalationQueue.length} autonomous escalations require owner attention`],
              ["high", "Clear autonomy task queue", `${autonomyOpenTasks.length}/${autonomousAgentTasks.length} tasks are internal prep only`],
              ["high", "Inspect blocked automation attempts", `${blockedAutomationAttempts.length} attempts were blocked with no provider calls or execution`],
              ["normal", "Review daily command briefing", `${dailyCommandBriefings.length} Wholesale Prime briefing generated by V12`],
              ["normal", "Check Level 4 approvals", `${autonomyLevel4Rules.length} controlled live-action review rule remains owner-gated`],
              ["critical", "Review controlled auto-execution blocks", `${autoExecutionBlockedAttempts.length} V13 attempts blocked before provider action`],
              ["high", "Approve auto-execution templates", `${approvedTemplateLibrary.length} templates currently approved for rule matching`],
              ["normal", "Inspect auto-execution audit", `${autoExecutionAuditTrail.length} attempts and reminders have audit records`],
              ["critical", "Review buyer acceleration queue", `${buyerAccelerationReadyDeals.length} deals are ready for controlled one-buyer distribution`],
              ["high", "Resolve buyer acceleration blocks", `${buyerAccelerationBlockedRecords.length} deals have sanitizer, margin, approval, or compliance blocks`],
              ["high", "Route buyer POF gaps", `${buyerAccelerationPofGaps.length} buyer responses require proof-of-funds handling`],
              ["normal", "Inspect buyer sequence safety", `${buyerSequencesBlocked.length} buyer sequence drafts need sanitizer review`],
              ["normal", "Review buyer response owner queue", `${buyerResponsesNeedingOwnerAction.length} buyer responses need owner action`],
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
