import { DealTable } from "@/components/DealTable";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  activeDealRooms,
  automationRules,
  approvedAutoExecutionRules,
  approvedTemplateLibrary,
  autoExecutionAuditTrail,
  autoExecutionBlockedAttempts,
  autoExecutionMockSentAttempts,
  autonomousAgentTasks,
  autonomyEscalationQueue,
  autonomyLevel4Rules,
  autonomyOpenTasks,
  assignmentFeeAttributions,
  assignmentReadyDealRooms,
  assignmentReadyRecords,
  blockedDealRooms,
  blockedAutomationAttempts,
  blockedDistributionPreps,
  buyerAccelerationBlockedRecords,
  buyerAccelerationPofGaps,
  buyerAccelerationReadyDeals,
  buyerAccelerationRecords,
  buyerResponsesNeedingOwnerAction,
  buyerSequencesBlocked,
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
  dailyCommandBriefings,
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
  agentPerformanceByScore,
  leads,
  offerReadyPackets,
  offerPackets,
  offerConversionDealsAtRisk,
  missingEvidencePackets,
  projected10kContractsReady,
  projectedAssignmentFeesAtRisk,
  projectedEvidenceAssignmentFees,
  projectedAssignmentTotal,
  optimizationRecommendationsByImpact,
  outcomeLearningRecords,
  forecastSafetyCards,
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
  fastestBuyerVelocity,
  missingLearningEvidence,
  scoringWeightChanges,
  strong10kLearningProbability,
  pipelineProbabilityAdjustedRevenue,
  pipelineProjectedMonthlyRevenue,
  pipelineRevenueAtRisk,
  likely10kDealProbabilities,
  marketRanking,
  leadSpendRecommendations,
  activeOperatorMode,
  currentSystemTrustScore,
  pendingOwnerApprovals,
  operatorExceptionsOpen,
  criticalOperatorExceptions,
  operatorHardBoundaryCards,
  auditExportsReady,
  blockedProviderReadiness,
  evidenceAttachmentRecords,
  failedEnvironmentChecks,
  productionReady,
  safeBackupExports,
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

      <Section title="V12 Near-Autonomous Execution Engine">
        <div className="grid-three">
          <RecordCard title="Automation rules" meta={`${automationRules.length} rules govern Level 2-4 internal prep`} right={<Pill tone="green">guarded</Pill>} />
          <RecordCard title="Agent task queue" meta={`${autonomyOpenTasks.length}/${autonomousAgentTasks.length} tasks await internal review`} right={<Pill tone="gold">queue</Pill>} />
          <RecordCard title="Daily briefings" meta={`${dailyCommandBriefings.length} Wholesale Prime briefing record`} right={<Pill>brief</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="Escalation queue" meta={`${autonomyEscalationQueue.length} urgent recommendations require owner attention`} right={<Pill tone="red">owner</Pill>} />
          <RecordCard title="Blocked attempts" meta={`${blockedAutomationAttempts.length} live or unsafe attempts audited without provider calls`} right={<Pill tone="red">blocked</Pill>} />
          <RecordCard title="Level 4 / Level 5" meta={`${autonomyLevel4Rules.length} Level 4 owner-gated rule; Level 5 unavailable`} right={<Pill tone="gold">controlled</Pill>} />
        </div>
      </Section>

      <Section title="V13 Controlled Auto-Execution Gate">
        <div className="grid-three">
          <RecordCard title="Approved auto rules" meta={`${approvedAutoExecutionRules.length} rules can enter conditional workflow`} right={<Pill tone="green">approved</Pill>} />
          <RecordCard title="Template library" meta={`${approvedTemplateLibrary.length} approved templates are safety checked`} right={<Pill tone="green">safe</Pill>} />
          <RecordCard title="Mock-sent attempts" meta={`${autoExecutionMockSentAttempts.length} low-risk single-message attempt passed gates`} right={<Pill>mock</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="Blocked attempts" meta={`${autoExecutionBlockedAttempts.length} bulk, unsafe, or missing-gate attempts blocked`} right={<Pill tone="red">blocked</Pill>} />
          <RecordCard title="Audit records" meta={`${autoExecutionAuditTrail.length} auto-execution events recorded`} right={<Pill tone="gold">audit</Pill>} />
          <RecordCard title="Bulk campaigns" meta="Blocked; no buyer blasts, cold SMS, or legal/contract messages." right={<Pill tone="red">off</Pill>} />
        </div>
      </Section>

      <Section title="V14 Buyer Distribution Acceleration">
        <div className="grid-three">
          <RecordCard title="Acceleration records" meta={`${buyerAccelerationRecords.length} deal-level buyer speed snapshots`} right={<Pill>ranked</Pill>} />
          <RecordCard title="Controlled-ready deals" meta={`${buyerAccelerationReadyDeals.length} can enter one-recipient owner-approved distribution`} right={<Pill tone="green">ready</Pill>} />
          <RecordCard title="Fastest buyer velocity" meta={`${fastestBuyerVelocity[0] ? fastestBuyerVelocity[0].velocityScore : 0} top velocity score`} right={<Pill tone="green">speed</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="POF gaps routed" meta={`${buyerAccelerationPofGaps.length} buyer responses need POF review`} right={<Pill tone="gold">verify</Pill>} />
          <RecordCard title="Response owner queue" meta={`${buyerResponsesNeedingOwnerAction.length} buyer responses need owner action`} right={<Pill tone="gold">owner</Pill>} />
          <RecordCard title="Blocked acceleration" meta={`${buyerAccelerationBlockedRecords.length} records blocked by visibility, margin, compliance, or approvals`} right={<Pill tone="red">blocked</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="Blocked sequences" meta={`${buyerSequencesBlocked.length} draft sequences flagged by sanitizer`} right={<Pill tone="red">review</Pill>} />
          <RecordCard title="Controlled sends" meta="Require buyer-visible deal, sanitized sheet, V5/V13 gates, owner approval, and one recipient." right={<Pill tone="gold">gated</Pill>} />
          <RecordCard title="Bulk buyer blast" meta="Blocked; no campaigns, fake scarcity, seller data, or internal profit logic exposure." right={<Pill tone="red">off</Pill>} />
        </div>
      </Section>

      <Section title="V15 Deal Flow Optimization Learning">
        <div className="grid-three">
          <RecordCard title="Outcome learning records" meta={`${outcomeLearningRecords.length} closed, lost, blocked, and contract-ready outcomes`} right={<Pill>evidence</Pill>} />
          <RecordCard title="Strong 10K+ probability" meta={`${strong10kLearningProbability.length} source-backed high-confidence records`} right={<Pill tone="green">10K+</Pill>} />
          <RecordCard title="Optimization recommendations" meta={`${optimizationRecommendationsByImpact.length} explainable owner-review recommendations`} right={<Pill tone="gold">review</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="Agent performance" meta={`${agentPerformanceByScore.length} division groups scored deterministically`} right={<Pill tone="green">{agentPerformanceByScore[0]?.overallScore ?? 0}</Pill>} />
          <RecordCard title="Missing learning evidence" meta={`${missingLearningEvidence.length} records blocked from confidence claims`} right={<Pill tone={missingLearningEvidence.length ? "red" : "green"}>{missingLearningEvidence.length}</Pill>} />
          <RecordCard title="Scoring changes logged" meta={`${scoringWeightChanges.length} source-tied feedback-loop changes`} right={<Pill tone="gold">logged</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="Guaranteed revenue" meta="Blocked; recommendations are estimates and source-backed patterns only." right={<Pill tone="red">off</Pill>} />
          <RecordCard title="Unsupported ROI" meta="Blocked; no fake revenue or ROI claims." right={<Pill tone="red">off</Pill>} />
          <RecordCard title="Black-box ML" meta="Disabled; scoring is deterministic and explainable." right={<Pill tone="green">explainable</Pill>} />
        </div>
      </Section>

      <Section title="V16 Revenue Forecast and Market Scaling">
        <div className="grid-three">
          <RecordCard title="Projected pipeline" meta={formatCurrency(pipelineProjectedMonthlyRevenue)} right={<Pill tone="gold">estimate</Pill>} />
          <RecordCard title="Probability-adjusted revenue" meta={formatCurrency(pipelineProbabilityAdjustedRevenue)} right={<Pill tone="green">adjusted</Pill>} />
          <RecordCard title="Revenue at risk" meta={formatCurrency(pipelineRevenueAtRisk)} right={<Pill tone="red">risk</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="Likely 10K+ deals" meta={`${likely10kDealProbabilities.length} probability records above threshold`} right={<Pill tone="green">10K+</Pill>} />
          <RecordCard title="Top scaling market" meta={`${marketRanking[0]?.marketZip ?? "n/a"} / ${marketRanking[0]?.recommendedSpendLevel ?? "n/a"}`} right={<Pill>{marketRanking[0]?.scalingScore ?? 0}</Pill>} />
          <RecordCard title="Lead spend plans" meta={`${leadSpendRecommendations.length} evidence-backed spend recommendations`} right={<Pill tone="gold">owner</Pill>} />
        </div>
        <div className="grid-three">
          {forecastSafetyCards.slice(0, 3).map((card) => (
            <RecordCard key={card.label} title={card.label} meta={card.detail} right={<Pill tone={card.label === "Revenue at risk" ? "gold" : "green"}>{card.value}</Pill>} />
          ))}
        </div>
      </Section>

      <Section title="V17 Semi-Autonomous Operator Mode">
        <div className="grid-three">
          <RecordCard title="Operator mode" meta={`Current ${activeOperatorMode.currentMode}; default ${activeOperatorMode.defaultMode}`} right={<Pill tone="gold">owner</Pill>} />
          <RecordCard title="Approval console" meta={`${pendingOwnerApprovals.length} owner approvals queued`} right={<Pill tone="gold">pending</Pill>} />
          <RecordCard title="System trust" meta={currentSystemTrustScore.trustStatus} right={<Pill tone="green">{currentSystemTrustScore.overallTrustScore}</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="Open exceptions" meta={`${operatorExceptionsOpen.length} exceptions require attention`} right={<Pill tone="gold">queue</Pill>} />
          <RecordCard title="Critical exceptions" meta={`${criticalOperatorExceptions.length} high money/risk items`} right={<Pill tone="red">critical</Pill>} />
          <RecordCard title="Semi-autonomous bypass" meta="Blocked; high-risk actions remain owner-approved." right={<Pill tone="red">off</Pill>} />
        </div>
        <div className="grid-three">
          {operatorHardBoundaryCards.slice(0, 3).map((card) => (
            <RecordCard key={card.label} title={card.label} meta={card.detail} right={<Pill tone="red">{card.value}</Pill>} />
          ))}
        </div>
      </Section>

      <Section title="V18 Production Readiness and Audit Export">
        <div className="grid-three">
          <RecordCard title="Production readiness" meta={productionReady ? "All readiness gates clear" : "Auth, env, secrets, providers, or hardening still block production"} right={<Pill tone={productionReady ? "green" : "red"}>{productionReady ? "ready" : "blocked"}</Pill>} />
          <RecordCard title="Audit exports" meta={`${auditExportsReady.length} sanitized packets ready for owner review`} right={<Pill tone="green">sanitized</Pill>} />
          <RecordCard title="Evidence attachments" meta={`${evidenceAttachmentRecords.length} metadata-only source-linked records`} right={<Pill>linked</Pill>} />
        </div>
        <div className="grid-three">
          <RecordCard title="Backup metadata" meta={`${safeBackupExports.length} safe backup/export records`} right={<Pill tone="green">safe</Pill>} />
          <RecordCard title="Provider readiness" meta={`${blockedProviderReadiness.length} providers default blocked until sandbox gates pass`} right={<Pill tone="red">blocked</Pill>} />
          <RecordCard title="Environment blockers" meta={`${failedEnvironmentChecks.length} required auth/env/secret checks missing`} right={<Pill tone="red">review</Pill>} />
        </div>
      </Section>
    </div>
  );
}
