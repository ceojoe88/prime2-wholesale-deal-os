export type Division = {
  id: string;
  name: string;
  managerName: string;
  responsibilities: string[];
  priorityQueue: string[];
  workload: number;
  activeRecommendations: string[];
  riskFlags: string[];
  performanceNotes: string;
  nextBestAction: string;
};

export type Agent = {
  id: string;
  name: string;
  divisionId: string;
  currentFocus: string;
  recommendation: string;
  riskFlags: string[];
};

export type Lead = {
  id: string;
  sellerName: string;
  address: string;
  city: string;
  state: string;
  zipCode: string;
  propertyType: string;
  sourceCategory: string;
  stage: string;
  askingPrice: number;
  estimatedEquity: number;
  opportunityScore: number;
  motivationScore: number;
  marketDemand: number;
  contactabilityScore: number;
  complianceRisk: number;
  nextBestAction: string;
};

export type Deal = {
  id: string;
  leadId: string;
  status: string;
  arv: number;
  repairs: number;
  buyerCosts: number;
  buyerDesiredProfit: number;
  maxBuyerPurchasePrice: number;
  maxSellerOffer: number;
  sellerContractPrice: number;
  buyerPurchasePrice: number;
  projectedAssignmentFee: number;
  buyerMargin: number;
  offerReasonablenessScore: number;
  spreadConfidenceScore: number;
  riskScore: number;
  confidenceScore: number;
  dealSpeedScore: number;
  conservativeOffer: number;
  standardOffer: number;
  aggressiveOffer: number;
  riskFlags: string[];
  hot: boolean;
  underContract: boolean;
};

export type Buyer = {
  id: string;
  name: string;
  company: string;
  email: string;
  phone: string;
  targetZipCodes: string[];
  maxPurchasePrice: number;
  propertyType: string;
  proofOfFundsStatus: string;
  closingSpeedDays: number;
  reliabilityScore: number;
  pastPerformance: string;
};

export type BuyerMatch = {
  id: string;
  dealId: string;
  buyerId: string;
  score: number;
  matchReasons: string[];
  riskFlags: string[];
  draftOnly: boolean;
};

export type BuyerPublication = {
  id: string;
  dealId: string;
  operatorMarkedVisible: boolean;
  complianceReviewed: boolean;
  sellerContractControlled: boolean;
  riskStatus: "low" | "medium" | "high";
  availabilityStatus: string;
  askingPrice: number | null;
  beds: number | null;
  baths: number | null;
  sqft: number | null;
  arvRange: { low: number | null; high: number | null };
  repairEstimateRange: { low: number | null; high: number | null };
  estimatedBuyerMargin: number | null;
  buyerMarginStatus: "strong" | "review" | "weak";
  photosPlaceholder: string[];
  accessInstructionsPlaceholder: string;
};

export type BuyerPortalDeal = {
  dealId: string;
  city: string;
  state: string;
  zipCode: string;
  propertyType: string;
  beds: number | null;
  baths: number | null;
  sqft: number | null;
  arvRange: { low: number | null; high: number | null };
  repairEstimateRange: { low: number | null; high: number | null };
  askingPrice: number | null;
  estimatedBuyerMargin: number | null;
  photosPlaceholder: string[];
  accessInstructionsPlaceholder: string;
  proofOfFundsStatus: string;
  availabilityStatus: string;
  offerInterestAction: {
    type: "draft_intent_only";
    contractExecutionAllowed: false;
    paymentCollectionAllowed: false;
  };
};

export type BuyerInterest = {
  id: string;
  buyerId: string;
  dealId: string;
  interestStatus: string;
  intendedOfferAmount: number | null;
  proofOfFundsStatus: string;
  notes: string;
  timestamp: string;
  draftOnly: true;
  contractExecutionAllowed: false;
};

export type BuyerDemandProfile = {
  id: string;
  buyerId: string;
  buyerActivityScore: number;
  zipCodeDemandScore: number;
  propertyTypeDemandScore: number;
  priceBandFitScore: number;
  closingSpeedScore: number;
  proofOfFundsStrength: number;
  reliabilityScore: number;
  lastEngagedDate: string;
  preferredSpreadMarginNotes: string;
  targetZipCodes: string[];
  propertyType: string;
  priceBand: string;
  active: boolean;
  draftOnly: true;
};

export type BuyerDealPriority = {
  id: string;
  dealId: string;
  buyerId: string;
  buyerDemandProfileId: string;
  targetAreaMatch: number;
  maxPriceFit: number;
  proofOfFundsScore: number;
  pastReliabilityScore: number;
  closingSpeedScore: number;
  dealTypeFit: number;
  buyerMarginStrength: number;
  priorityScore: number;
  rank: number;
  rankingReasons: string[];
  riskFlags: string[];
  recommendedNextStep: string;
  draftOnly: true;
  liveContactAllowed: false;
  buyerBlastAllowed: false;
  internalProfitLogicExposed: false;
};

export type SanitizedBuyerDealSheet = {
  propertySummary: {
    city: string;
    state: string;
    zipCode: string;
    propertyType: string;
    beds: number | null;
    baths: number | null;
    sqft: number | null;
  };
  askingPrice: number | null;
  arvRange: { low: number | null; high: number | null };
  repairEstimateRange: { low: number | null; high: number | null };
  buyerMarginEstimate: number | null;
  accessInstructionsPlaceholder: string;
  availabilityStatus: string;
  proofInspectionNotesPlaceholder: string;
};

export type DealDistributionPrep = {
  id: string;
  dealId: string;
  buyerId: string;
  buyerPriorityId: string;
  buyerDealPublicationId: string;
  buyerDealEmailDraft: string;
  buyerSmsDraft: string;
  privateDealSheetDraft: SanitizedBuyerDealSheet;
  buyerCallNotes: string;
  buyerResponseTracker: { status: string; operatorReview: string; timestamp: string }[];
  approvalStatus: string;
  draftStatus: string;
  safetyStatus: string;
  blockedReasons: string[];
  draftOnly: true;
  liveSendAllowed: false;
  bulkBlastAllowed: false;
  sellerPrivateDataExposed: false;
  assignmentFeeExposed: false;
  legalClosingGuaranteeAllowed: false;
};

export type OfferPositioningRecord = {
  id: string;
  dealId: string;
  offerPacketId: string;
  offerStrategyType: "cash-fast" | "as-is" | "investor-grade" | "flexible-close";
  sellerPainAlignment: string[];
  justificationSummary: { comps: string; repairs: string; timeline: string };
  anchorPrice: number;
  walkAwayPrice: number;
  idealContractPrice: number;
  concessionRange: { low: number; high: number };
  negotiationNotes: string;
  confidenceScore: number;
  ownerApprovalRecorded: boolean;
  safetyStatus: string;
  blockedReasons: string[];
  draftOnly: true;
  pressureTacticsAllowed: false;
  legalAdviceAllowed: false;
};

export type NegotiationRecord = {
  id: string;
  dealId: string;
  offerPositioningId: string;
  sellerInteractionId: string;
  sellerLastResponse: string;
  sellerObjections: string[];
  counterOffer: number | null;
  emotionalSignals: string[];
  negotiationStage: "initial" | "follow-up" | "negotiating" | "soft-accepted" | "verbally accepted" | "stalled";
  nextMoveRecommendation: string;
  motivationScore: number;
  priceAlignment: number;
  timelineAlignment: number;
  trustLevel: number;
  objectionResolution: number;
  contactConsistency: number;
  readinessScore: number;
  readinessLevel: "low readiness" | "medium readiness" | "high readiness" | "contract-ready";
  safetyStatus: string;
  blockedReasons: string[];
  draftOnly: true;
  automaticAcceptanceAllowed: false;
  liveNegotiationAutomationAllowed: false;
  pressureTacticsAllowed: false;
  legalAdviceAllowed: false;
};

export type ContractReadyState = {
  id: string;
  dealId: string;
  offerPositioningId: string;
  negotiationRecordId: string;
  readinessStatus: string;
  contractReady: boolean;
  readyForExternalDrafting: boolean;
  sellerLikelyToSign: boolean;
  numbersLocked: boolean;
  negotiationStabilized: boolean;
  underwritingComplete: boolean;
  profitControlValidated: boolean;
  buyerDemandConfirmed: boolean;
  compliancePassed: boolean;
  noRiskFlags: boolean;
  sellerReadinessHigh: boolean;
  ownerApprovalRecorded: boolean;
  blockedReasons: string[];
  fastestPathToContract: string[];
  projectedAssignmentFee: number;
  draftOnly: true;
  externalAttorneyTitleDraftingRequired: true;
  executableContractGenerated: false;
  contractExecutionAllowed: false;
  legalAdviceProvided: false;
  automaticAcceptanceAllowed: false;
  liveNegotiationAutomationAllowed: false;
};

export type TitleReviewCoordination = {
  id: string;
  dealId: string;
  contractReadyStateId: string;
  selectedTitleCompanyPlaceholder: string;
  attorneyTitleReviewStatus: string;
  requiredDocuments: string[];
  missingItems: string[];
  reviewNotes: string;
  ownerApprovalStatus: string;
  packetPrepAllowed: boolean;
  blockedReasons: string[];
  draftOnly: true;
  legalAdviceAllowed: false;
  contractExecutionAllowed: false;
  documentSubmissionAllowed: false;
  titleCompanyEmailSendAllowed: false;
  attorneyClientRelationshipClaimed: false;
  closingGuaranteeAllowed: false;
};

export type ReviewPacketPrep = {
  id: string;
  titleReviewCoordinationId: string;
  dealId: string;
  propertySummary: {
    city: string;
    state: string;
    zip: string;
    propertyType: string;
  };
  sellerTerms: Record<string, string | number | boolean>;
  buyerAssignmentReadinessSummary: Record<string, string | number | boolean>;
  closingTimeline: string;
  accessNotes: string;
  complianceChecklist: string[];
  documentChecklist: string[];
  packetStatus: string;
  prepAllowed: boolean;
  blockedReasons: string[];
  draftOnly: true;
  legalAdviceAllowed: false;
  contractExecutionAllowed: false;
  documentSubmissionAllowed: false;
  titleCompanyEmailSendAllowed: false;
  submittedToTitle: false;
  attorneyClientRelationshipClaimed: false;
  closingGuaranteeAllowed: false;
};

export type AutomationRule = {
  id: string;
  name: string;
  workflowType: string;
  autonomyLevel: number;
  triggerEvent: string;
  enabled: boolean;
  allowedActions: string[];
  blockedActions: string[];
  scheduleLabel: string;
  ownerApprovalRequired: boolean;
  safetyStatus: string;
  lastRunStatus: string;
  draftOnly: true;
  liveActionAllowed: false;
  level5Disabled: true;
  portalPublishAllowed: false;
  contractExecutionAllowed: false;
  titleSubmissionAllowed: false;
  paymentCollectionAllowed: false;
  notes: string;
};

export type SchedulerRun = {
  id: string;
  ruleId: string;
  workflowType: string;
  runStatus: string;
  scheduledFor: string;
  idempotencyKey: string;
  createdTasks: number;
  createdAttempts: number;
  escalationCreated: boolean;
  dailyBriefingCreated: boolean;
  summary: Record<string, string | number | boolean | string[]>;
  ownerApprovalRequired: boolean;
  autonomyLevel: number;
  idempotentReplay: boolean;
  realWorldActionTaken: false;
};

export type AutomationAttempt = {
  id: string;
  runId: string;
  actionType: string;
  sourceRecordType: string;
  sourceRecordId: string;
  attemptStatus: string;
  autonomyLevel: number;
  safetyResult: Record<string, string | number | boolean | string[]>;
  blockedReasons: string[];
  ownerApprovalRequired: boolean;
  ownerApprovalRecorded: boolean;
  providerCalled: false;
  realWorldActionTaken: false;
  idempotencyKey: string;
};

export type AutonomousAgentTask = {
  id: string;
  ruleId: string;
  runId: string;
  agentName: string;
  division: string;
  taskType: string;
  sourceRecordType: string;
  sourceRecordId: string;
  priority: string;
  status: string;
  recommendation: string;
  dueAt: string;
  idempotencyKey: string;
  ownerApprovalRequired: boolean;
  draftOnly: true;
  liveActionAllowed: false;
  readinessMarked: boolean;
};

export type AutomationEventTrigger = {
  id: string;
  ruleId: string;
  eventType: string;
  sourceRecordType: string;
  sourceRecordId: string;
  workflowType: string;
  payload: Record<string, string | number | boolean>;
  status: string;
  idempotencyKey: string;
  processed: boolean;
};

export type DailyCommandBriefing = {
  id: string;
  runId: string;
  briefingDate: string;
  generatedBy: string;
  hotDeals: { dealId: string; projectedAssignmentFee: number; dealSpeedScore: number }[];
  priorityActions: string[];
  managerQueue: { division: string; manager: string; nextBestAction: string }[];
  escalations: { id: string; severity: string; reason: string }[];
  safetySummary: Record<string, boolean>;
  ownerReviewItems: string[];
  draftOnly: true;
  legalAdviceAllowed: false;
  liveOutreachAllowed: false;
  portalPublishAllowed: false;
  titleSubmissionAllowed: false;
  contractExecutionAllowed: false;
};

export type AutonomyEscalation = {
  id: string;
  runId: string;
  dealId: string;
  leadId: string;
  escalationType: string;
  severity: string;
  reason: string;
  recommendedAction: string;
  status: string;
  ownerActionRequired: boolean;
  autonomyLevel: number;
  realWorldActionBlocked: true;
  idempotencyKey: string;
};

export type AutoExecutionRule = {
  id: string;
  ruleName: string;
  actionType: string;
  sourceType: string;
  allowedRecipientType: string;
  trigger: string;
  requiredConditions: string[];
  approvedTemplateId: string;
  autonomyLevel: number;
  liveFlagRequired: boolean;
  riskScore: number;
  ownerApprovalStatus: string;
  status: string;
  blockedReasons: string[];
  bulkSendAllowed: false;
  buyerBlastAllowed: false;
  legalContractMessageAllowed: false;
  coldSmsAllowed: false;
};

export type ApprovedTemplate = {
  id: string;
  templateName: string;
  templateType: string;
  channel: string;
  recipientType: string;
  subject: string;
  body: string;
  approved: boolean;
  safetyStatus: string;
  riskFlags: string[];
  requiresOptOut: boolean;
  includesOptOut: boolean;
  legalAdviceAllowed: false;
  pressureLanguageAllowed: false;
  fakeUrgencyAllowed: false;
  fakeBuyerClaimAllowed: false;
  draftOnlyDefault: true;
};

export type AutoExecutionDryRun = {
  id: string;
  ruleId: string;
  templateId: string;
  sourceRecordType: string;
  sourceRecordId: string;
  recipientType: string;
  recipientPlaceholder: string;
  subjectBodyHash: string;
  safetyPassed: boolean;
  riskStatus: string;
  providerMode: string;
  idempotencyKey: string;
  status: string;
};

export type AutoExecutionAttempt = {
  id: string;
  ruleId: string;
  templateId: string;
  dryRunId: string | null;
  actionType: string;
  sourceRecordType: string;
  sourceRecordId: string;
  recipientType: string;
  recipientCount: number;
  attemptStatus: string;
  blockedReasons: string[];
  ownerApprovalRecorded: boolean;
  v5SafetyPassed: boolean;
  v5DryRunReceiptExists: boolean;
  v5ApprovalRecorded: boolean;
  liveFlagsEnabled: boolean;
  providerReady: boolean;
  providerCalled: boolean;
  providerMode: string;
  idempotencyKey: string;
  auditRecordCreated: boolean;
};

export type AutoExecutionAuditRecord = {
  id: string;
  attemptId: string;
  ruleId: string;
  eventType: string;
  sourceRecordType: string;
  sourceRecordId: string;
  outcome: string;
  blockedReasons: string[];
  providerCalled: boolean;
  idempotencyKey: string;
};

export type BuyerAccelerationRecord = {
  id: string;
  dealId: string;
  buyerRankingSnapshot: { buyerId: string; rank: number; priorityScore: number }[];
  topBuyerList: string[];
  pofStatus: string;
  buyerReliability: number;
  buyerMarginStrength: number;
  distributionReadiness: string;
  ownerApprovalStatus: string;
  blockedReasons: string[];
  controlledSendAllowed: boolean;
  buyerVisible: boolean;
  sanitizedDealSheetReady: boolean;
  buyerMatchApproved: boolean;
  compliancePassed: boolean;
  v13GatePassed: boolean;
  v5GatePassed: boolean;
  bulkBlastAllowed: false;
};

export type BuyerSequencePrep = {
  id: string;
  dealId: string;
  buyerId: string;
  accelerationRecordId: string;
  firstBuyerNotice: string;
  buyerDetailFollowUp: string;
  pofRequest: string;
  viewingAccessCoordination: string;
  offerIntentFollowUp: string;
  deadlineReminder: string;
  safetyStatus: string;
  blockedReasons: string[];
  draftOnly: true;
  liveSendAllowed: false;
  bulkBlastAllowed: false;
  deceptiveScarcityAllowed: false;
  sellerPrivateDataExposed: false;
  internalProfitLogicExposed: false;
};

export type BuyerResponseRoute = {
  id: string;
  dealId: string;
  buyerId: string;
  responseType: string;
  routedStatus: string;
  ownerActionRequired: boolean;
  recommendedNextStep: string;
  pofGap: boolean;
  accessRequested: boolean;
  offerIntentRecorded: boolean;
  draftOnly: true;
  contractExecutionAllowed: false;
};

export type BuyerVelocityProfile = {
  id: string;
  buyerId: string;
  responseSpeed: number;
  pofStrength: number;
  closeHistory: number;
  priceFit: number;
  marketFit: number;
  reliability: number;
  previousIntentQuality: number;
  velocityScore: number;
  recommendedUse: string;
  draftOnly: true;
};

export type OutcomeLearningRecord = {
  id: string;
  dealId: string | null;
  leadSource: string;
  market: string;
  sellerType: string;
  buyerType: string;
  offerStrategy: string;
  followUpType: string;
  conversionResult: string;
  projectedAssignmentFee: number;
  verifiedAssignmentFee: number;
  timeToContractReadyDays: number | null;
  blockers: string[];
  lostReason: string;
  confidenceScore: number;
  sourceEvidenceIds: string[];
  sourceRecordsPresent: boolean;
  evidenceStatus: string;
  unsupportedRevenueClaim: boolean;
  unsupportedRoiClaim: boolean;
};

export type OptimizationRecommendation = {
  id: string;
  recommendationType: string;
  target: string;
  recommendation: string;
  explanation: string;
  sourceRecordIds: string[];
  confidenceScore: number;
  impactScore: number;
  status: string;
  ownerReviewStatus: string;
  guaranteedRevenueClaimAllowed: false;
  unsupportedRoiClaimAllowed: false;
};

export type AgentPerformanceScore = {
  id: string;
  divisionName: string;
  agentGroup: string;
  qualityScore: number;
  conversionScore: number;
  accuracyScore: number;
  effectivenessScore: number;
  complianceBlockRate: number;
  followUpScore: number;
  recommendationAccuracy: number;
  overallScore: number;
  explanation: string;
  sourceRecordIds: string[];
};

export type ScoringWeightChange = {
  id: string;
  sourceRecordId: string;
  weightGroup: string;
  previousWeight: number;
  newWeight: number;
  reason: string;
  explanation: string;
  loggedBy: string;
  ownerReviewStatus: string;
};

export type RevenueForecastRecord = {
  id: string;
  forecastPeriod: string;
  projectedAssignmentFees: number;
  verifiedAssignmentFees: number;
  probabilityAdjustedRevenue: number;
  conservativeForecast: number;
  baseForecast: number;
  aggressiveForecast: number;
  dealsAtRisk: string[];
  expectedCloseWindow: string;
  confidenceLevel: string;
  sourceBasis: string[];
  estimateLabel: string;
  guaranteedRevenueClaimAllowed: false;
  unsupportedRoiClaimAllowed: false;
};

export type DealProbabilityRecord = {
  id: string;
  dealId: string;
  sellerReadiness: number;
  buyerDemand: number;
  underwritingConfidence: number;
  complianceStatusScore: number;
  titleReviewReadiness: number;
  blockerSeverity: number;
  buyerPofStrength: number;
  communicationMomentum: number;
  probabilityScore: number;
  probabilityBand: string;
  sourceRecordIds: string[];
  estimateOnly: true;
};

export type MarketScalingScore = {
  id: string;
  marketZip: string;
  leadVolume: number;
  hotLeadPercentage: number;
  buyerDemand: number;
  averageSpread: number;
  conversionRate: number;
  titleComplianceFriction: number;
  competitionRisk: number;
  recommendedSpendLevel: string;
  scalingScore: number;
  sourceRecordIds: string[];
  estimateOnly: true;
};

export type LeadSpendPlan = {
  id: string;
  targetZipCodes: string[];
  leadTypes: string[];
  maxMonthlySpend: number;
  expectedDealCount: number;
  expectedAssignmentFeeLow: number;
  expectedAssignmentFeeHigh: number;
  breakEvenAssignmentTarget: number;
  evidenceBasis: string[];
  recommendationStatus: string;
  unsupportedSpendRecommended: boolean;
  estimateOnly: true;
  ownerReviewStatus: string;
};

export type OperatorModeSetting = {
  id: string;
  currentMode: "manual" | "assisted" | "near_autonomous" | "semi_autonomous";
  defaultMode: "manual" | "assisted" | "near_autonomous" | "semi_autonomous";
  semiAutonomousEnabled: boolean;
  ownerEnabled: boolean;
  maxAutonomyLevel: number;
  level5Disabled: true;
  highRiskRequiresApproval: true;
  liveActionsRequireGates: true;
  contractExecutionAllowed: false;
  titleSubmissionAllowed: false;
  bulkCampaignsAllowed: false;
  paymentHandlingAllowed: false;
};

export type SemiAutonomousCommandLoopRun = {
  id: string;
  modeSettingId: string;
  cycleStatus: string;
  scanSummary: Record<string, string | number | boolean>;
  scoreSummary: Record<string, string | number | boolean>;
  routeSummary: Record<string, string | number | boolean>;
  preparedItems: { type: string; source: string }[];
  gateChecks: { gate: string; passed: boolean }[];
  escalations: string[];
  approvalsWaiting: string[];
  outcomesLogged: string[];
  optimizedRecords: string[];
  highRiskActionsExecuted: false;
  contractsExecuted: false;
  titleSubmitted: false;
  bulkCampaignsSent: false;
  portalPublishWithoutApproval: false;
};

export type OwnerApprovalItem = {
  id: string;
  approvalType: string;
  sourceRecordType: string;
  sourceRecordId: string;
  title: string;
  riskLevel: string;
  approvalStatus: string;
  ownerRequired: true;
  readyForApproval: boolean;
  blockedReasons: string[];
  actionSummary: string;
  highRiskAction: boolean;
  executed: false;
};

export type OperatorExceptionRecord = {
  id: string;
  exceptionType: string;
  severity: string;
  sourceRecordType: string;
  sourceRecordId: string;
  reason: string;
  recommendedAction: string;
  ownerActionRequired: true;
  status: string;
};

export type AutonomousDailyOperatingReport = {
  id: string;
  reportDate: string;
  generatedBy: string;
  whatSystemDid: string[];
  whatPrepared: string[];
  whatBlocked: string[];
  needsOwnerApproval: string[];
  topMoneyActions: string[];
  topRiskActions: string[];
  projectedAssignmentFeeMovement: number;
  recommendedFocusToday: string[];
  draftOnly: true;
  highRiskActionsExecuted: false;
};

export type SystemTrustScore = {
  id: string;
  automationSuccessRate: number;
  blockedUnsafeActions: number;
  approvalQueueAgeHours: number;
  staleTasks: number;
  scoringConfidence: number;
  forecastConfidence: number;
  buyerResponseVelocity: number;
  sellerConversionVelocity: number;
  overallTrustScore: number;
  trustStatus: string;
  sourceRecordIds: string[];
};

export type ApprovalUxReview = {
  id: string;
  ownerApprovalItemId: string | null;
  approvalType: string;
  sourceRecordType: string;
  sourceRecordId: string;
  contextSummary: string;
  riskSummary: string;
  gateSummary: { gate: string; passed: boolean }[];
  confirmationPrompt: string;
  recommendedDecision: string;
  approvalStatus: string;
  ownerActionRequired: boolean;
  approvalIsNotExecution: boolean;
  blockedReasons: string[];
};

export type AuditExportPacket = {
  id: string;
  exportType: string;
  sourceRecordType: string;
  sourceRecordId: string;
  requestedBy: string;
  exportScope: string;
  sanitizedPayload: Record<string, string | number | boolean | string[]>;
  includedRecordIds: string[];
  omittedSensitiveFields: string[];
  internalFieldsRemoved: string[];
  exportStatus: string;
  ownerApprovalStatus: string;
  safeForExternalShare: boolean;
  containsRawPrivateData: boolean;
  legalAdviceIncluded: boolean;
  secretsIncluded: boolean;
  packetHash: string;
  retentionNotes: string;
  blockedReasons: string[];
};

export type EvidenceAttachmentRecord = {
  id: string;
  sourceRecordType: string;
  sourceRecordId: string;
  dealId: string | null;
  evidencePacketId: string | null;
  attachmentType: string;
  filenamePlaceholder: string;
  storageMode: string;
  sanitizedMetadata: Record<string, string | number | boolean>;
  containsSensitiveData: boolean;
  sourceLinkageVerified: boolean;
  sourceVerified: boolean;
  safeToExport: boolean;
  uploadStatus: string;
  operatorNotes: string;
  rawFilePathCommitted: boolean;
  blockedReasons: string[];
};

export type BackupExportRecord = {
  id: string;
  backupType: string;
  backupScope: string;
  storageTarget: string;
  includedTables: string[];
  excludedFields: string[];
  safeMetadata: Record<string, string | number | boolean | string[]>;
  backupStatus: string;
  containsRawPrivateData: boolean;
  safeMetadataOnly: boolean;
  filePathPlaceholder: string;
  restoreTestStatus: string;
  ownerApprovalStatus: string;
  blockedReasons: string[];
};

export type ProviderSandboxReadinessCheck = {
  id: string;
  providerType: string;
  providerName: string;
  mode: string;
  sandboxReady: boolean;
  secretsConfigured: boolean;
  liveFlagEnabled: boolean;
  safetyCheckRequired: boolean;
  dryRunRequired: boolean;
  ownerApprovalRequired: boolean;
  idempotencyRequired: boolean;
  auditTrailRequired: boolean;
  providerCallsAllowed: boolean;
  readinessStatus: string;
  blockedReasons: string[];
  lastCheckedNotes: string;
};

export type ProviderRegistry = {
  id: string;
  providerName: string;
  providerType: "openai" | "email" | "sms" | "crm" | "skip_trace" | "storage" | "webhook";
  providerMode: "mock" | "sandbox" | "live";
  enabled: boolean;
  sandboxEnabled: boolean;
  liveEnabled: boolean;
  credentialReferenceMasked: string;
  credentialPresent: boolean;
  credentialSource: "env";
  readinessStatus: string;
  blockedReason: string;
  ownerApprovalRequired: boolean;
  notes: string;
  rawSecretValueStored: false;
  liveNetworkCallAllowed: false;
};

export type ProviderAttemptAudit = {
  id: string;
  providerId: string | null;
  providerName: string;
  providerType: string;
  sourceDomain: string;
  actionType: string;
  mode: "mock" | "sandbox" | "live";
  attemptStatus: string;
  blockedReason: string;
  idempotencyKey: string;
  requestMetadataHash: string;
  providerCalled: false;
  realNetworkCallMade: false;
};

export type ProviderWebhookEvent = {
  id: string;
  providerType: string;
  eventType: string;
  receivedAt: string;
  mode: "mock" | "sandbox" | "live";
  signaturePresent: boolean;
  signatureValid: boolean;
  normalizedEventStatus: string;
  reviewTaskCreated: boolean;
  dealMutationAllowed: false;
  dealMutated: false;
  rawPayloadStored: false;
  blockedReason: string;
};

export type EnvironmentReadinessCheck = {
  id: string;
  category: string;
  checkName: string;
  required: boolean;
  passed: boolean;
  status: string;
  detail: string;
  remediation: string;
  blockedReasons: string[];
  preventsProduction: boolean;
};

export type DeploymentHardeningCheck = {
  id: string;
  area: string;
  checkName: string;
  required: boolean;
  passed: boolean;
  status: string;
  detail: string;
  remediation: string;
  ownerActionRequired: boolean;
  blockedReasons: string[];
};

export type SellerInteraction = {
  id: string;
  leadId: string;
  callNotes: string;
  motivationAnswers: Record<string, string>;
  askingPrice: number | null;
  timeline: string;
  propertyCondition: string;
  painPoints: string[];
  objections: string[];
  nextFollowUpDate: string;
  sellerTemperatureScore: number;
  objectionStatus: string;
  followUpUrgency: "hot" | "high" | "normal";
  nextBestSellerAction: string;
  draftOnly: true;
  liveOutreachAllowed: false;
};

export type OfferPacket = {
  id: string;
  dealId: string;
  packetStatus: string;
  ownerApprovalRecorded: boolean;
  complianceGuardPassed: boolean;
  buyerMarginProtected: boolean;
  targetAssignmentFeeChecked: boolean;
  underwritingComplete: boolean;
  packetPrepAllowed: boolean;
  blockedReasons: string[];
  approvalStatus: string;
  draftSummary: string;
  draftOnly: true;
  realWorldActionTaken: false;
};

export type ContractControlRecord = {
  id: string;
  leadId: string;
  dealId: string;
  offerPacketId: string;
  sellerAcceptedTerms: Record<string, string | number | boolean>;
  contractStatus: string;
  assignmentAllowedFlag: boolean;
  inspectionAccessNotes: string;
  earnestMoneyNotes: string;
  closingTimeline: string;
  titleCompanyPreference: string;
  requiredDocumentsChecklist: string[];
  ownerApprovalStatus: string;
  complianceReviewStatus: string;
  contractPrepAllowed: boolean;
  blockedReasons: string[];
  draftOnly: true;
  executableContractGenerated: false;
  liveSendingAllowed: false;
  titleSubmissionAllowed: false;
  automaticStatusChangeAllowed: false;
};

export type TitleHandoffPacket = {
  id: string;
  contractControlId: string;
  dealId: string;
  propertyDetails: {
    city: string;
    state: string;
    zip: string;
    propertyType: string;
  };
  sellerInfoPlaceholder: string;
  buyerEntityInfoPlaceholder: string;
  agreedPrice: number;
  closingTimeline: string;
  accessNotes: string;
  assignmentStatus: string;
  requiredDocumentChecklist: string[];
  attorneyTitleReviewReminder: string;
  packetStatus: string;
  draftOnly: true;
  titleSubmissionAllowed: false;
  submittedToTitle: false;
  legalAdviceProvided: false;
};

export type AssignmentReadinessRecord = {
  id: string;
  contractControlId: string;
  dealId: string;
  buyerId: string | null;
  buyerMatchId: string | null;
  buyerInterestId: string | null;
  readinessStatus: string;
  assignmentReady: boolean;
  blockedReasons: string[];
  assignmentAllowedConfirmed: boolean;
  buyerPofStatus: string;
  complianceReviewPassed: boolean;
  ownerApprovalRecorded: boolean;
  draftOnly: true;
  contractExecutionAllowed: false;
  titleSubmissionAllowed: false;
};

export type CommunicationDraft = {
  id: string;
  draftType: "seller_follow_up" | "buyer_interest_response" | "title_handoff_email" | "internal_owner_note";
  channel: "email" | "sms" | "internal";
  recipientType: string;
  recipientEmailPlaceholder: string;
  recipientPhonePlaceholder: string;
  sourceRecordType: string;
  sourceRecordId: string;
  subject: string;
  draftBody: string;
  status: string;
  safetyChecked: boolean;
  safetyPassed: boolean;
  ownerApprovalRecorded: boolean;
  communicationLiveFlagEnabled: boolean;
  providerReadiness: boolean;
  lastDryRunReceiptId: string | null;
  approvedDryRunReceiptId: string | null;
  riskStatus: "unchecked" | "clear" | "blocked";
  blockedReasons: string[];
  liveSendCount: number;
  draftOnly: true;
  bulkSendAllowed: false;
  campaignAllowed: false;
  autoFollowupAllowed: false;
  buyerBlastAllowed: false;
  titleSubmissionAllowed: false;
};

export type CommunicationDryRunReceipt = {
  id: string;
  draftId: string;
  recipient: string;
  subjectBodyHash: string;
  sourceRecordType: string;
  sourceRecordId: string;
  riskStatus: string;
  safetyResult: { allowed: boolean; riskFlags: string[]; reason: string };
  timestamp: string;
  providerMode: "mock/dry_run";
  idempotencyKey: string;
};

export type CommunicationApproval = {
  id: string;
  draftId: string;
  dryRunReceiptId: string;
  ownerApprovalRecorded: boolean;
  approvalStatus: string;
  approvalNotes: string;
  approvedBy: string;
  draftHashAtApproval: string;
};

export type CommunicationSendAttempt = {
  id: string;
  draftId: string;
  dryRunReceiptId: string | null;
  recipient: string;
  channel: string;
  providerMode: "mock/dry_run";
  attemptStatus: "blocked" | "mock_sent" | "sent";
  blockedReasons: string[];
  idempotencyKey: string;
  providerCalled: boolean;
  mockSent: boolean;
  liveSendRequested: boolean;
  bulkSendDetected: boolean;
};

export type SellerOfferPublication = {
  id: string;
  leadId: string;
  dealId: string;
  offerPacketId: string;
  contractControlId: string;
  portalVisibilityEnabled: boolean;
  offerStatus: string;
  offerAmount: number | null;
  closingTimelineEstimate: string;
  inspectionAccessNextStep: string;
  titleCompanyReviewStatus: string;
  documentChecklist: string[];
  operatorContactPlaceholder: string;
  offerLanguage: string;
  offerLanguageSafetyPassed: boolean;
  complianceCheckPassed: boolean;
  ownerApprovalRecorded: boolean;
  visibilityStatus: string;
  blockedReasons: string[];
  draftOnly: true;
  contractExecutionAllowed: false;
  liveNegotiationAutomationAllowed: false;
  legalAdviceProvided: false;
  buyerDataExposed: false;
  internalProfitLogicExposed: false;
};

export type SellerPortalOffer = {
  offerId: string;
  propertyAddressSummary: string;
  offerStatus: string;
  offerAmount: number | null;
  closingTimelineEstimate: string;
  inspectionAccessNextStep: string;
  titleCompanyReviewStatus: string;
  documentChecklist: string[];
  ownerOperatorContactPlaceholder: string;
  sellerQuestionsNotesAction: {
    type: "draft_intake_only";
    operatorReviewRequired: true;
    automaticNegotiationAllowed: false;
    offerAcceptanceExecutionAllowed: false;
    documentUploadIsPlaceholder: true;
  };
  portalVisibilityStatus: string;
};

export type SellerPortalResponse = {
  id: string;
  sellerOfferPublicationId: string;
  responseType: "seller_portal_note" | "offer_question" | "appointment_access_preference" | "document_upload_placeholder";
  sellerPortalNote: string;
  offerQuestion: string;
  appointmentAccessPreference: string;
  documentUploadPlaceholder: string;
  responseStatus: string;
  operatorReviewStatus: string;
  draftOnly: true;
  negotiationExecutionAllowed: false;
  contractExecutionAllowed: false;
  automaticAcceptanceAllowed: false;
};

export type UnifiedDealRoom = {
  id: string;
  dealId: string;
  contractControlId: string;
  sellerOfferPublicationId: string | null;
  buyerDealPublicationId: string | null;
  titleHandoffPacketId: string | null;
  assignmentReadinessRecordId: string | null;
  sellerPortalStatus: string;
  buyerPortalStatus: string;
  titleHandoffStatus: string;
  assignmentReadinessStatus: string;
  communicationStatus: string;
  complianceStatus: string;
  closingTimeline: string;
  blockers: string[];
  nextRequiredActions: string[];
  ownerApprovalStatus: string;
  coordinationStatus: "closing_ready" | "blocked";
  projectedAssignmentFeeAtRisk: number;
  draftOnly: true;
  legalExecutionAllowed: false;
  executableContractGenerated: false;
  titleSubmissionAllowed: false;
  paymentHandlingAllowed: false;
  automaticNegotiationAllowed: false;
};

export type ClosingCoordinationChecklist = {
  id: string;
  dealRoomId: string;
  sellerAcceptedOffer: boolean;
  contractPrepReady: boolean;
  buyerMatched: boolean;
  buyerPofVerified: boolean;
  assignmentAllowedConfirmed: boolean;
  titleHandoffPrepared: boolean;
  inspectionAccessCoordinated: boolean;
  sellerDocumentsRequested: boolean;
  buyerIntentRecorded: boolean;
  complianceReviewComplete: boolean;
  ownerApprovalComplete: boolean;
  readinessStatus: string;
  blockedReasons: string[];
  draftOnly: true;
  legalExecutionAllowed: false;
  titleSubmissionAllowed: false;
  paymentHandlingAllowed: false;
  automaticNegotiationAllowed: false;
};

export type DealRoomBlocker = {
  id: string;
  dealRoomId: string;
  dealId: string;
  blockerType: string;
  severity: "medium" | "high" | "critical";
  status: "open" | "resolved";
  source: string;
  detail: string;
  recommendation: string;
  blocksClosing: boolean;
  ownerActionRequired: boolean;
  resolved: boolean;
  draftOnly: true;
};

export type DealEvidencePacket = {
  id: string;
  dealRoomId: string;
  dealId: string;
  leadSource: string;
  sellerInteractionProof: Record<string, string | number | boolean | null>;
  underwritingSnapshot: Record<string, string | number | boolean>;
  buyerInterestProof: Record<string, string | number | boolean | null>;
  pofProofStatus: string;
  contractControlStatus: string;
  titleHandoffStatus: string;
  communicationReceipts: Record<string, string | number | boolean | string[]>[];
  blockerHistory: Record<string, string | boolean>[];
  complianceReviewStatus: string;
  sourceRecordsPresent: boolean;
  unsupportedProfitClaims: string[];
  evidenceStatus: "approved" | "owner_review_needed" | "blocked_missing_evidence";
  ownerReviewStatus: string;
  approved: boolean;
  sanitizedSummary: Record<string, unknown>;
  internalNotesSanitized: boolean;
  draftOnly: true;
  clientFacingProofAllowed: false;
  legalClosingGuaranteeAllowed: false;
};

export type AssignmentFeeAttribution = {
  id: string;
  dealRoomId: string;
  dealId: string;
  evidencePacketId: string;
  projectedAssignmentFee: number;
  targetAssignmentFee: number;
  sellerContractPrice: number;
  buyerPurchasePrice: number;
  buyerMargin: number;
  attributionBasis: string[];
  confidenceScore: number;
  verificationStatus: "verified" | "owner_review_needed" | "blocked" | "missing_evidence";
  ownerReviewStatus: string;
  sourceRecordsPresent: boolean;
  unsupportedProfitClaims: string[];
  verified10kOpportunity: boolean;
  draftOnly: true;
  clientFacingProofAllowed: false;
  legalClosingGuaranteeAllowed: false;
};

export const divisions: Division[] = [
  {
    id: "market-intelligence",
    name: "Market Intelligence Division",
    managerName: "Marisol Vega",
    responsibilities: ["Zip demand", "Comparable sales", "Rental demand", "Investor heat"],
    priorityQueue: ["75216 comps refresh", "Rental demand scan", "Investor heat review"],
    workload: 7,
    activeRecommendations: ["Refresh comps before offer packet prep."],
    riskFlags: ["thin_comps_in_two_zips"],
    performanceNotes: "Strong investor-demand read with conservative comp confidence.",
    nextBestAction: "Refresh comparable sale notes for the five hot opportunities."
  },
  {
    id: "lead-intelligence",
    name: "Lead Intelligence Division",
    managerName: "Elias Monroe",
    responsibilities: ["Motivation scoring", "List stacking", "Contactability confidence"],
    priorityQueue: ["Vacancy signal review", "Probate confidence check", "High-equity stack"],
    workload: 11,
    activeRecommendations: ["Move high-equity vacant leads to underwriting first."],
    riskFlags: ["probate_authority_unverified"],
    performanceNotes: "Opportunity scores are calibrated conservatively.",
    nextBestAction: "Confirm source confidence on inherited and probate records."
  },
  {
    id: "seller-acquisition",
    name: "Seller Acquisition Division",
    managerName: "Nadia Price",
    responsibilities: ["Seller scripts", "Motivation discovery", "Negotiation drafts"],
    priorityQueue: ["Offer explanation drafts", "Hot seller follow-ups", "Objection notes"],
    workload: 9,
    activeRecommendations: ["Use repair-backed offer explanations on offer_needed leads."],
    riskFlags: ["no_live_outreach"],
    performanceNotes: "All communication remains draft-only and owner-controlled.",
    nextBestAction: "Prepare draft call notes for under-contract examples."
  },
  {
    id: "deal-underwriting",
    name: "Deal Underwriting Division",
    managerName: "Theo Kim",
    responsibilities: ["ARV", "Repairs", "MAO", "Risk adjustment", "Confidence"],
    priorityQueue: ["Repair basis review", "ARV confidence scoring", "MAO refresh"],
    workload: 8,
    activeRecommendations: ["Hold low-confidence repair estimates out of offer prep."],
    riskFlags: ["repair_scope_missing_photos"],
    performanceNotes: "Conservative formulas protect buyer margin.",
    nextBestAction: "Re-run MAO on repair variance above 15%."
  },
  {
    id: "middle-man-profit-control",
    name: "Middle-Man Profit Control Division",
    managerName: "Rina Patel",
    responsibilities: ["Assignment fee", "Buyer margin", "Offer reasonableness", "Spread risk"],
    priorityQueue: ["10K spread checks", "Aggressive-offer risk", "Buyer margin exception"],
    workload: 6,
    activeRecommendations: ["Prioritize 10K+ spreads with clean buyer margin notes."],
    riskFlags: ["one_deal_below_target_assignment_fee"],
    performanceNotes: "Spread calculations are direct and auditable.",
    nextBestAction: "Escalate seller price above max seller offer."
  },
  {
    id: "buyer-disposition",
    name: "Buyer Disposition Division",
    managerName: "Cam Jordan",
    responsibilities: ["Buyer matching", "POF checks", "Reliability", "Draft buyer blasts"],
    priorityQueue: ["POF review", "Top buyer match", "Buyer demand strength"],
    workload: 5,
    activeRecommendations: ["Use verified POF buyers for under-contract opportunities."],
    riskFlags: ["two_buyers_need_pof_refresh"],
    performanceNotes: "Reliability and closing speed are weighted ahead of volume.",
    nextBestAction: "Prepare draft buyer match packet after compliance review."
  },
  {
    id: "contract-compliance",
    name: "Contract & Compliance Division",
    managerName: "Selene Hart",
    responsibilities: ["Purchase checklist", "Assignment checklist", "Disclosure guard"],
    priorityQueue: ["Assignment review", "Seller role disclosure", "Title prep"],
    workload: 7,
    activeRecommendations: ["Block assignment prep until confirmations are checked."],
    riskFlags: ["state_specific_review_required"],
    performanceNotes: "Guardrails block execution-like actions by default.",
    nextBestAction: "Review the three compliance-risk examples."
  },
  {
    id: "follow-up",
    name: "Follow-Up Division",
    managerName: "Ivy Chen",
    responsibilities: ["Hot reminders", "Stale recovery", "Next-contact timing"],
    priorityQueue: ["Hot lead reminders", "Stale lead recovery", "Next contact timing"],
    workload: 10,
    activeRecommendations: ["Call-window recommendations require owner approval before action."],
    riskFlags: ["stale_leads_need_owner_review"],
    performanceNotes: "Follow-up cadence stays draft-only.",
    nextBestAction: "Move three warm leads into seller-followup priority."
  },
  {
    id: "operations-command",
    name: "Operations Command Division",
    managerName: "Damon Reed",
    responsibilities: ["Daily briefing", "Attention queue", "KPI", "Risk escalation"],
    priorityQueue: ["Daily briefing", "Attention queue", "KPI review"],
    workload: 6,
    activeRecommendations: ["Keep owner approval gates visible on high-risk actions."],
    riskFlags: ["owner_review_backlog"],
    performanceNotes: "Executive routing is clear and action-oriented.",
    nextBestAction: "Summarize top five actions for the owner."
  }
];

export const agentTeams: Record<string, string[]> = {
  "market-intelligence": [
    "Zip Code Demand Agent",
    "Comparable Sales Research Agent",
    "Rental Demand Agent",
    "Investor Activity Agent",
    "Market Heat Agent"
  ],
  "lead-intelligence": [
    "Distressed Property Agent",
    "Absentee Owner Agent",
    "Probate Lead Agent",
    "Tax Delinquent Agent",
    "Vacancy Signal Agent",
    "List Stacking Agent",
    "Contactability Agent"
  ],
  "seller-acquisition": [
    "Seller Script Agent",
    "Motivation Discovery Agent",
    "Objection Handling Agent",
    "Negotiation Prep Agent",
    "Offer Explanation Agent",
    "Seller Temperature Agent"
  ],
  "deal-underwriting": [
    "ARV Agent",
    "Repair Estimate Agent",
    "MAO Agent",
    "Risk Adjustment Agent",
    "Deal Confidence Agent"
  ],
  "middle-man-profit-control": [
    "Assignment Fee Agent",
    "Buyer Margin Protection Agent",
    "Seller Offer Reasonableness Agent",
    "Spread Optimization Agent",
    "Conservative Offer Agent",
    "Aggressive Offer Risk Agent"
  ],
  "buyer-disposition": [
    "Cash Buyer Match Agent",
    "Buyer Criteria Agent",
    "Buyer Reliability Agent",
    "Proof of Funds Agent",
    "Deal Blast Draft Agent",
    "Buyer Demand Agent"
  ],
  "contract-compliance": [
    "Purchase Agreement Checklist Agent",
    "Assignment Agreement Checklist Agent",
    "Title Company Prep Agent",
    "Disclosure Guard Agent",
    "State Compliance Risk Agent",
    "Misrepresentation Guard Agent"
  ],
  "follow-up": [
    "Follow-Up Priority Agent",
    "Stale Lead Recovery Agent",
    "Hot Lead Reminder Agent",
    "Seller Touchpoint Agent",
    "Next Contact Timing Agent"
  ],
  "operations-command": [
    "Daily Briefing Agent",
    "Attention Queue Agent",
    "KPI Agent",
    "Risk Escalation Agent",
    "Deal Commander Agent"
  ]
};

const slug = (value: string) => value.toLowerCase().replace(/&/g, "and").replace(/\s+/g, "-");

export const agents: Agent[] = Object.entries(agentTeams).flatMap(([divisionId, names]) =>
  names.map((name) => ({
    id: slug(name),
    name,
    divisionId,
    currentFocus: `${name} is reviewing active queues for ${divisionId.replace(/-/g, " ")}.`,
    recommendation: "Recommend, draft, score, escalate, or flag risk only.",
    riskFlags: []
  }))
);

const leadRows = [
  ["lead-001", "Angela Ruiz", "4127 Bonnie View Rd", "Dallas", "TX", "75216", "single_family", "vacant", "offer_needed", 146000, 92000, 83, 89, 91, 74, 14],
  ["lead-002", "Milton Graves", "918 E Ann Arbor Ave", "Dallas", "TX", "75216", "single_family", "tax delinquent", "under_contract", 118000, 76000, 84, 92, 88, 69, 12],
  ["lead-003", "Patrice Nolan", "226 W Louisiana Ave", "Dallas", "TX", "75224", "single_family", "absentee owner", "negotiating", 188000, 121000, 77, 80, 84, 71, 18],
  ["lead-004", "Dennis Shaw", "5803 Pineland Dr", "Arlington", "TX", "76017", "single_family", "tired landlord", "follow_up", 135000, 88000, 73, 76, 77, 80, 15],
  ["lead-005", "Carmen Ellis", "1430 Stella Ave", "Dallas", "TX", "75216", "duplex", "inherited", "offer_needed", 231000, 158000, 81, 86, 90, 64, 28],
  ["lead-006", "Robert Gaines", "709 W 10th St", "Dallas", "TX", "75208", "single_family", "code violation", "researched", 164000, 91000, 71, 74, 80, 58, 35],
  ["lead-007", "Monica Bell", "3012 Alabama Ave", "Fort Worth", "TX", "76104", "single_family", "pre-foreclosure", "offer_sent", 99000, 62000, 82, 91, 82, 65, 22],
  ["lead-008", "Isaac Vaughn", "1846 Proctor St", "Dallas", "TX", "75208", "single_family", "probate", "under_contract", 171000, 109000, 76, 84, 86, 60, 46],
  ["lead-009", "Tanya Moss", "6451 Lazy River Dr", "Dallas", "TX", "75241", "single_family", "high equity", "new_lead", 125000, 98000, 64, 64, 75, 72, 10],
  ["lead-010", "Victor Hall", "7522 S Westmoreland Rd", "Dallas", "TX", "75237", "single_family", "driving for dollars", "contacted", 112000, 67000, 66, 69, 79, 76, 19],
  ["lead-011", "Naomi Finch", "330 Rosemont Ave", "Dallas", "TX", "75208", "single_family", "county records", "new_lead", 202000, 131000, 62, 58, 83, 55, 12],
  ["lead-012", "Owen Pierce", "2705 Kathleen Ave", "Dallas", "TX", "75216", "single_family", "absentee owner", "follow_up", 132000, 84000, 71, 72, 89, 84, 13],
  ["lead-013", "Bianca Rowe", "4509 Tacoma St", "Dallas", "TX", "75216", "single_family", "vacant", "researched", 101000, 73000, 73, 78, 88, 62, 16],
  ["lead-014", "Harold Banks", "1815 Woodin Blvd", "Dallas", "TX", "75216", "single_family", "tax delinquent", "dead", 97000, 34000, 47, 44, 70, 35, 25],
  ["lead-015", "Erica Stanley", "1022 E Arlington Ave", "Fort Worth", "TX", "76104", "duplex", "tired landlord", "negotiating", 155000, 97000, 72, 75, 78, 74, 17],
  ["lead-016", "Gerald Cooper", "6707 Umphress Rd", "Dallas", "TX", "75217", "single_family", "code violation", "offer_needed", 119000, 82000, 77, 82, 81, 57, 30],
  ["lead-017", "Janet Ford", "2409 Wilhurt Ave", "Dallas", "TX", "75216", "single_family", "high equity", "researched", 143000, 112000, 66, 66, 87, 61, 11],
  ["lead-018", "Marcus Lee", "3930 W Illinois Ave", "Dallas", "TX", "75211", "single_family", "vacant", "follow_up", 150000, 96000, 75, 79, 82, 70, 14],
  ["lead-019", "Yvette Cruz", "5215 Bexar St", "Dallas", "TX", "75215", "single_family", "probate", "new_lead", 138000, 101000, 68, 73, 80, 49, 44],
  ["lead-020", "Caleb Morris", "8731 Diceman Dr", "Dallas", "TX", "75218", "single_family", "inherited", "contacted", 246000, 174000, 65, 63, 76, 66, 21],
  ["lead-021", "Lucia Hunt", "1115 E Baltimore Ave", "Fort Worth", "TX", "76104", "single_family", "pre-foreclosure", "follow_up", 103000, 69000, 80, 88, 79, 59, 24],
  ["lead-022", "Arthur Mills", "3726 Waldorf Dr", "Dallas", "TX", "75229", "single_family", "absentee owner", "researched", 310000, 210000, 62, 55, 70, 52, 9],
  ["lead-023", "Maya Flores", "4920 Bernal Dr", "Dallas", "TX", "75212", "single_family", "driving for dollars", "new_lead", 122000, 82000, 67, 68, 84, 73, 16],
  ["lead-024", "Frankie Brooks", "8406 Jennie Lee Ln", "Dallas", "TX", "75227", "single_family", "county records", "contacted", 128000, 79000, 61, 61, 74, 68, 12],
  ["lead-025", "Helena Stone", "609 W Boyce Ave", "Fort Worth", "TX", "76115", "single_family", "tax delinquent", "offer_sent", 108000, 69000, 78, 83, 77, 64, 22],
  ["lead-026", "Quinn Davis", "1528 Garrison St", "Dallas", "TX", "75216", "single_family", "vacant", "follow_up", 116000, 88000, 70, 70, 86, 56, 15],
  ["lead-027", "Sofia Nguyen", "2119 Bickers St", "Dallas", "TX", "75212", "duplex", "tired landlord", "researched", 172000, 118000, 74, 77, 83, 72, 18],
  ["lead-028", "Eddie Ramos", "4157 Copeland St", "Dallas", "TX", "75210", "single_family", "code violation", "new_lead", 96000, 59000, 69, 71, 73, 48, 31],
  ["lead-029", "Ruth Wallace", "9712 Brockbank Dr", "Dallas", "TX", "75220", "single_family", "high equity", "follow_up", 274000, 195000, 62, 57, 68, 60, 10],
  ["lead-030", "Jon Price", "3611 Easter Ave", "Dallas", "TX", "75216", "single_family", "probate", "researched", 129000, 93000, 70, 74, 87, 50, 42]
] as const;

export const leads: Lead[] = leadRows.map((row) => ({
  id: row[0],
  sellerName: row[1],
  address: row[2],
  city: row[3],
  state: row[4],
  zipCode: row[5],
  propertyType: row[6],
  sourceCategory: row[7],
  stage: row[8],
  askingPrice: row[9],
  estimatedEquity: row[10],
  opportunityScore: row[11],
  motivationScore: row[12],
  marketDemand: row[13],
  contactabilityScore: row[14],
  complianceRisk: row[15],
  nextBestAction: "Research, score, draft, or escalate based on stage."
}));

export const buyers: Buyer[] = [
  { id: "buyer-001", name: "Jules Avery", company: "Avery Cash Homes", email: "jules@example.test", phone: "214-555-0101", targetZipCodes: ["75216", "75224", "75208"], maxPurchasePrice: 210000, propertyType: "single_family", proofOfFundsStatus: "verified", closingSpeedDays: 10, reliabilityScore: 94, pastPerformance: "Closed three assignments within 12 days." },
  { id: "buyer-002", name: "Priya Shah", company: "Oakline Investments", email: "priya@example.test", phone: "214-555-0102", targetZipCodes: ["75216", "75241"], maxPurchasePrice: 150000, propertyType: "single_family", proofOfFundsStatus: "verified", closingSpeedDays: 7, reliabilityScore: 91, pastPerformance: "Fast closings and clean title deposits." },
  { id: "buyer-003", name: "Marcus Wade", company: "Wade Urban Renewal", email: "marcus@example.test", phone: "817-555-0103", targetZipCodes: ["76104", "76115"], maxPurchasePrice: 140000, propertyType: "single_family", proofOfFundsStatus: "needs_refresh", closingSpeedDays: 14, reliabilityScore: 82, pastPerformance: "Reliable, POF refresh needed this month." },
  { id: "buyer-004", name: "Simone Clark", company: "Clark Bridge Capital", email: "simone@example.test", phone: "214-555-0104", targetZipCodes: ["75216", "75208", "75212"], maxPurchasePrice: 260000, propertyType: "duplex", proofOfFundsStatus: "verified", closingSpeedDays: 12, reliabilityScore: 88, pastPerformance: "Prefers duplexes and inherited property discounts." },
  { id: "buyer-005", name: "Leo Martin", company: "Northline Rehabs", email: "leo@example.test", phone: "972-555-0105", targetZipCodes: ["75229", "75220", "75218"], maxPurchasePrice: 360000, propertyType: "single_family", proofOfFundsStatus: "verified", closingSpeedDays: 21, reliabilityScore: 78, pastPerformance: "Strong capital, slower closing operations." },
  { id: "buyer-006", name: "Adriana Cole", company: "Cole Equity Homes", email: "adriana@example.test", phone: "469-555-0106", targetZipCodes: ["75211", "75212", "75210"], maxPurchasePrice: 175000, propertyType: "single_family", proofOfFundsStatus: "verified", closingSpeedDays: 9, reliabilityScore: 86, pastPerformance: "Good at rougher repair scopes." },
  { id: "buyer-007", name: "Malik Stone", company: "Stone Porch Properties", email: "malik@example.test", phone: "214-555-0107", targetZipCodes: ["75217", "75227"], maxPurchasePrice: 135000, propertyType: "single_family", proofOfFundsStatus: "unverified", closingSpeedDays: 16, reliabilityScore: 74, pastPerformance: "Responsive but POF not yet reviewed." },
  { id: "buyer-008", name: "Tessa Young", company: "Southcrest Buyers", email: "tessa@example.test", phone: "817-555-0108", targetZipCodes: ["76104", "75216"], maxPurchasePrice: 120000, propertyType: "any", proofOfFundsStatus: "verified", closingSpeedDays: 8, reliabilityScore: 83, pastPerformance: "Buys small single-family and light duplex deals." },
  { id: "buyer-009", name: "Grant Miller", company: "Miller Rental Group", email: "grant@example.test", phone: "214-555-0109", targetZipCodes: ["75237", "75241"], maxPurchasePrice: 125000, propertyType: "single_family", proofOfFundsStatus: "verified", closingSpeedDays: 18, reliabilityScore: 80, pastPerformance: "Rental buyer; needs clean rent comps." },
  { id: "buyer-010", name: "Keisha King", company: "King Cash Acquisitions", email: "keisha@example.test", phone: "972-555-0110", targetZipCodes: ["75215", "75216", "75210"], maxPurchasePrice: 155000, propertyType: "single_family", proofOfFundsStatus: "needs_refresh", closingSpeedDays: 11, reliabilityScore: 81, pastPerformance: "Good demand, requires disclosure review before draft blast." }
];

export const deals: Deal[] = [
  { id: "deal-001", leadId: "lead-001", status: "offer_needed", arv: 275000, repairs: 45000, buyerCosts: 12000, buyerDesiredProfit: 45000, maxBuyerPurchasePrice: 173000, maxSellerOffer: 163000, sellerContractPrice: 151000, buyerPurchasePrice: 166000, projectedAssignmentFee: 15000, buyerMargin: 52000, offerReasonablenessScore: 92, spreadConfidenceScore: 88, riskScore: 15, confidenceScore: 88, dealSpeedScore: 39, conservativeOffer: 153220, standardOffer: 163000, aggressiveOffer: 169520, riskFlags: [], hot: true, underContract: false },
  { id: "deal-002", leadId: "lead-002", status: "under_contract", arv: 210000, repairs: 32000, buyerCosts: 9000, buyerDesiredProfit: 35000, maxBuyerPurchasePrice: 134000, maxSellerOffer: 124000, sellerContractPrice: 112000, buyerPurchasePrice: 127000, projectedAssignmentFee: 15000, buyerMargin: 42000, offerReasonablenessScore: 92, spreadConfidenceScore: 88, riskScore: 12, confidenceScore: 91, dealSpeedScore: 42, conservativeOffer: 116560, standardOffer: 124000, aggressiveOffer: 128960, riskFlags: [], hot: true, underContract: true },
  { id: "deal-003", leadId: "lead-003", status: "negotiating", arv: 340000, repairs: 65000, buyerCosts: 15000, buyerDesiredProfit: 55000, maxBuyerPurchasePrice: 205000, maxSellerOffer: 195000, sellerContractPrice: 180000, buyerPurchasePrice: 193000, projectedAssignmentFee: 13000, buyerMargin: 67000, offerReasonablenessScore: 92, spreadConfidenceScore: 88, riskScore: 18, confidenceScore: 84, dealSpeedScore: 32, conservativeOffer: 183300, standardOffer: 195000, aggressiveOffer: 202800, riskFlags: [], hot: true, underContract: false },
  { id: "deal-004", leadId: "lead-004", status: "follow_up", arv: 185000, repairs: 28000, buyerCosts: 8000, buyerDesiredProfit: 30000, maxBuyerPurchasePrice: 119000, maxSellerOffer: 109000, sellerContractPrice: 100000, buyerPurchasePrice: 111000, projectedAssignmentFee: 11000, buyerMargin: 38000, offerReasonablenessScore: 92, spreadConfidenceScore: 88, riskScore: 20, confidenceScore: 79, dealSpeedScore: 31, conservativeOffer: 102460, standardOffer: 109000, aggressiveOffer: 113360, riskFlags: [], hot: true, underContract: false },
  { id: "deal-005", leadId: "lead-005", status: "offer_needed", arv: 425000, repairs: 90000, buyerCosts: 20000, buyerDesiredProfit: 70000, maxBuyerPurchasePrice: 245000, maxSellerOffer: 235000, sellerContractPrice: 220000, buyerPurchasePrice: 235000, projectedAssignmentFee: 15000, buyerMargin: 80000, offerReasonablenessScore: 92, spreadConfidenceScore: 88, riskScore: 35, confidenceScore: 76, dealSpeedScore: 27, conservativeOffer: 220900, standardOffer: 235000, aggressiveOffer: 244400, riskFlags: ["seller_authority_unverified"], hot: true, underContract: false },
  { id: "deal-006", leadId: "lead-006", status: "researched", arv: 260000, repairs: 70000, buyerCosts: 12000, buyerDesiredProfit: 40000, maxBuyerPurchasePrice: 138000, maxSellerOffer: 128000, sellerContractPrice: 132000, buyerPurchasePrice: 140000, projectedAssignmentFee: 8000, buyerMargin: 38000, offerReasonablenessScore: 64, spreadConfidenceScore: 30, riskScore: 48, confidenceScore: 62, dealSpeedScore: 16, conservativeOffer: 120320, standardOffer: 128000, aggressiveOffer: 133120, riskFlags: ["projected_assignment_fee_below_target", "buyer_margin_below_desired_profit", "seller_offer_exceeds_margin_safe_max"], hot: false, underContract: false },
  { id: "deal-007", leadId: "lead-007", status: "offer_sent", arv: 155000, repairs: 30000, buyerCosts: 8000, buyerDesiredProfit: 25000, maxBuyerPurchasePrice: 92000, maxSellerOffer: 82000, sellerContractPrice: 75000, buyerPurchasePrice: 84000, projectedAssignmentFee: 9000, buyerMargin: 33000, offerReasonablenessScore: 92, spreadConfidenceScore: 62, riskScore: 24, confidenceScore: 67, dealSpeedScore: 31, conservativeOffer: 77080, standardOffer: 82000, aggressiveOffer: 85280, riskFlags: ["projected_assignment_fee_below_target"], hot: false, underContract: false },
  { id: "deal-008", leadId: "lead-008", status: "under_contract", arv: 310000, repairs: 55000, buyerCosts: 14000, buyerDesiredProfit: 50000, maxBuyerPurchasePrice: 191000, maxSellerOffer: 181000, sellerContractPrice: 168000, buyerPurchasePrice: 180000, projectedAssignmentFee: 12000, buyerMargin: 61000, offerReasonablenessScore: 92, spreadConfidenceScore: 88, riskScore: 58, confidenceScore: 66, dealSpeedScore: 18, conservativeOffer: 170140, standardOffer: 181000, aggressiveOffer: 188240, riskFlags: ["probate_authority_unverified", "assignment_fee_disclosure_review"], hot: false, underContract: true }
];

export const buyerMatches: BuyerMatch[] = [
  { id: "match-001", dealId: "deal-001", buyerId: "buyer-001", score: 98.92, matchReasons: ["target_zip_match", "price_capacity_match", "property_type_match", "proof_of_funds_verified", "fast_close"], riskFlags: [], draftOnly: true },
  { id: "match-002", dealId: "deal-002", buyerId: "buyer-002", score: 98.38, matchReasons: ["target_zip_match", "price_capacity_match", "property_type_match", "proof_of_funds_verified", "fast_close"], riskFlags: [], draftOnly: true },
  { id: "match-003", dealId: "deal-005", buyerId: "buyer-004", score: 97.84, matchReasons: ["target_zip_match", "price_capacity_match", "property_type_match", "proof_of_funds_verified", "fast_close"], riskFlags: [], draftOnly: true }
];

export const complianceRecords = [
  { id: "compliance-001", dealId: "deal-005", title: "Inherited property authority review", riskWarnings: ["seller_authority_unverified", "state_specific_review_required"], blockedActions: ["prepare_assignment_packet", "execute_contract"] },
  { id: "compliance-002", dealId: "deal-006", title: "Buyer margin protection exception", riskWarnings: ["seller_offer_exceeds_margin_safe_max", "buyer_margin_below_desired_profit"], blockedActions: ["prepare_offer_packet", "buyer_blast_execute"] },
  { id: "compliance-003", dealId: "deal-008", title: "Assignment and role disclosure review", riskWarnings: ["probate_authority_unverified", "assignment_fee_disclosure_review"], blockedActions: ["prepare_assignment_packet", "execute_contract"] }
];

export const buyerPublications: BuyerPublication[] = [
  { id: "publication-001", dealId: "deal-001", operatorMarkedVisible: true, complianceReviewed: true, sellerContractControlled: true, riskStatus: "low", availabilityStatus: "available", askingPrice: 166000, beds: 3, baths: 2, sqft: 1420, arvRange: { low: 263000, high: 287000 }, repairEstimateRange: { low: 39000, high: 51000 }, estimatedBuyerMargin: 52000, buyerMarginStatus: "strong", photosPlaceholder: ["Exterior photo placeholder", "Kitchen photo placeholder", "Mechanical photo placeholder"], accessInstructionsPlaceholder: "Access instructions available after owner review of buyer intent and proof of funds." },
  { id: "publication-002", dealId: "deal-002", operatorMarkedVisible: true, complianceReviewed: true, sellerContractControlled: true, riskStatus: "low", availabilityStatus: "available", askingPrice: 127000, beds: 3, baths: 1.5, sqft: 1285, arvRange: { low: 201000, high: 219000 }, repairEstimateRange: { low: 28000, high: 36000 }, estimatedBuyerMargin: 42000, buyerMarginStatus: "strong", photosPlaceholder: ["Exterior photo placeholder", "Kitchen photo placeholder", "Mechanical photo placeholder"], accessInstructionsPlaceholder: "Access instructions available after owner review of buyer intent and proof of funds." },
  { id: "publication-003", dealId: "deal-003", operatorMarkedVisible: true, complianceReviewed: true, sellerContractControlled: true, riskStatus: "medium", availabilityStatus: "available", askingPrice: 193000, beds: 4, baths: 2, sqft: 1840, arvRange: { low: 326000, high: 354000 }, repairEstimateRange: { low: 58000, high: 72000 }, estimatedBuyerMargin: 67000, buyerMarginStatus: "strong", photosPlaceholder: ["Exterior photo placeholder", "Kitchen photo placeholder", "Mechanical photo placeholder"], accessInstructionsPlaceholder: "Access instructions available after owner review of buyer intent and proof of funds." },
  { id: "publication-004", dealId: "deal-004", operatorMarkedVisible: true, complianceReviewed: true, sellerContractControlled: false, riskStatus: "medium", availabilityStatus: "blocked", askingPrice: 111000, beds: 3, baths: 2, sqft: 1315, arvRange: { low: 176000, high: 194000 }, repairEstimateRange: { low: 24000, high: 33000 }, estimatedBuyerMargin: 38000, buyerMarginStatus: "strong", photosPlaceholder: ["Exterior photo placeholder"], accessInstructionsPlaceholder: "Blocked pending control confirmation." },
  { id: "publication-005", dealId: "deal-005", operatorMarkedVisible: true, complianceReviewed: false, sellerContractControlled: true, riskStatus: "high", availabilityStatus: "blocked", askingPrice: 235000, beds: 4, baths: 2.5, sqft: 2260, arvRange: { low: 405000, high: 445000 }, repairEstimateRange: { low: 80000, high: 102000 }, estimatedBuyerMargin: 80000, buyerMarginStatus: "strong", photosPlaceholder: ["Exterior photo placeholder"], accessInstructionsPlaceholder: "Blocked pending compliance review." },
  { id: "publication-006", dealId: "deal-006", operatorMarkedVisible: true, complianceReviewed: true, sellerContractControlled: true, riskStatus: "high", availabilityStatus: "blocked", askingPrice: 140000, beds: 3, baths: 1, sqft: 1180, arvRange: { low: 248000, high: 272000 }, repairEstimateRange: { low: 64000, high: 78000 }, estimatedBuyerMargin: 38000, buyerMarginStatus: "weak", photosPlaceholder: ["Exterior photo placeholder"], accessInstructionsPlaceholder: "Blocked pending buyer margin repair." },
  { id: "publication-007", dealId: "deal-007", operatorMarkedVisible: false, complianceReviewed: false, sellerContractControlled: true, riskStatus: "medium", availabilityStatus: "draft", askingPrice: 84000, beds: 2, baths: 1, sqft: 980, arvRange: { low: 148000, high: 162000 }, repairEstimateRange: { low: 26000, high: 34000 }, estimatedBuyerMargin: 33000, buyerMarginStatus: "weak", photosPlaceholder: ["Exterior photo placeholder"], accessInstructionsPlaceholder: "Draft only." },
  { id: "publication-008", dealId: "deal-008", operatorMarkedVisible: true, complianceReviewed: false, sellerContractControlled: true, riskStatus: "high", availabilityStatus: "blocked", askingPrice: 180000, beds: 4, baths: 2, sqft: 1710, arvRange: { low: 296000, high: 324000 }, repairEstimateRange: { low: 48000, high: 62000 }, estimatedBuyerMargin: 61000, buyerMarginStatus: "strong", photosPlaceholder: ["Exterior photo placeholder"], accessInstructionsPlaceholder: "Blocked pending compliance review." }
];

export const buyerInterests: BuyerInterest[] = [
  { id: "interest-001", buyerId: "buyer-001", dealId: "deal-001", interestStatus: "owner_review_needed", intendedOfferAmount: 166000, proofOfFundsStatus: "verified", notes: "Buyer intent recorded as draft only; no contract or payment action.", timestamp: "2026-05-04T14:05:00Z", draftOnly: true, contractExecutionAllowed: false },
  { id: "interest-002", buyerId: "buyer-002", dealId: "deal-002", interestStatus: "proof_of_funds_verified", intendedOfferAmount: 127000, proofOfFundsStatus: "verified", notes: "Owner review needed before any external follow-up.", timestamp: "2026-05-04T14:08:00Z", draftOnly: true, contractExecutionAllowed: false },
  { id: "interest-003", buyerId: "buyer-003", dealId: "deal-003", interestStatus: "proof_of_funds_needed", intendedOfferAmount: 193000, proofOfFundsStatus: "needs_refresh", notes: "POF refresh required; buyer interest is non-binding.", timestamp: "2026-05-04T14:11:00Z", draftOnly: true, contractExecutionAllowed: false },
  { id: "interest-004", buyerId: "buyer-003", dealId: "deal-001", interestStatus: "proof_of_funds_needed", intendedOfferAmount: 166000, proofOfFundsStatus: "needs_refresh", notes: "V4 readiness example: buyer intent exists but POF refresh blocks assignment readiness.", timestamp: "2026-05-04T14:18:00Z", draftOnly: true, contractExecutionAllowed: false },
  { id: "interest-005", buyerId: "buyer-004", dealId: "deal-005", interestStatus: "owner_review_needed", intendedOfferAmount: 235000, proofOfFundsStatus: "verified", notes: "V4 readiness example: buyer intent exists while compliance review remains blocked.", timestamp: "2026-05-04T14:21:00Z", draftOnly: true, contractExecutionAllowed: false }
];

export const sellerInteractions: SellerInteraction[] = [
  { id: "seller-interaction-001", leadId: "lead-001", callNotes: "Seller wants a clean as-is option and asked how repairs affect price.", motivationAnswers: { whySell: "Vacant property is hard to maintain", timeline: "Would like clarity this week", decisionMaker: "Seller is primary decision maker" }, askingPrice: 146000, timeline: "7-14 days", propertyCondition: "Deferred exterior maintenance, dated kitchen, HVAC age unknown.", painPoints: ["vacancy", "maintenance", "uncertain repairs"], objections: ["wants to understand offer math"], nextFollowUpDate: "2026-05-03", sellerTemperatureScore: 91, objectionStatus: "pricing_needs_explanation", followUpUrgency: "hot", nextBestSellerAction: "Prepare draft offer explanation after owner review.", draftOnly: true, liveOutreachAllowed: false },
  { id: "seller-interaction-002", leadId: "lead-002", callNotes: "Seller is open to assignment process after role is explained clearly.", motivationAnswers: { whySell: "Tax pressure and property fatigue", timeline: "Fast but wants clear next steps", decisionMaker: "Seller plus spouse" }, askingPrice: 118000, timeline: "under 10 days", propertyCondition: "Moderate repairs, roof age needs confirmation.", painPoints: ["tax pressure", "time", "repair uncertainty"], objections: ["needs role disclosure in plain language"], nextFollowUpDate: "2026-05-04", sellerTemperatureScore: 94, objectionStatus: "role_disclosure_needed", followUpUrgency: "hot", nextBestSellerAction: "Draft assignment role explanation for compliance review.", draftOnly: true, liveOutreachAllowed: false },
  { id: "seller-interaction-003", leadId: "lead-003", callNotes: "Seller has a higher price expectation but will review repair-backed logic.", motivationAnswers: { whySell: "Absentee ownership burden", timeline: "30 days", decisionMaker: "Seller only" }, askingPrice: 188000, timeline: "30 days", propertyCondition: "Cosmetic updates plus possible plumbing work.", painPoints: ["distance", "tenant turnover", "pricing uncertainty"], objections: ["price expectation"], nextFollowUpDate: "2026-05-02", sellerTemperatureScore: 79, objectionStatus: "price_gap", followUpUrgency: "high", nextBestSellerAction: "Draft objection response with no pressure.", draftOnly: true, liveOutreachAllowed: false },
  { id: "seller-interaction-004", leadId: "lead-005", callNotes: "Inherited property seller needs authority and title path clarified before offer.", motivationAnswers: { whySell: "Family wants to settle property decision", timeline: "2-4 weeks", decisionMaker: "Multiple heirs possible" }, askingPrice: 231000, timeline: "2-4 weeks", propertyCondition: "Large repair scope, occupancy status needs confirmation.", painPoints: ["inheritance complexity", "repair scope", "family coordination"], objections: ["authority questions"], nextFollowUpDate: "2026-05-06", sellerTemperatureScore: 82, objectionStatus: "authority_review", followUpUrgency: "high", nextBestSellerAction: "Escalate to compliance before offer packet.", draftOnly: true, liveOutreachAllowed: false },
  { id: "seller-interaction-005", leadId: "lead-007", callNotes: "Seller is stressed by timeline and needs a calm follow-up.", motivationAnswers: { whySell: "Payment pressure", timeline: "urgent", decisionMaker: "Seller only" }, askingPrice: 99000, timeline: "urgent but unverified", propertyCondition: "Small house, repairs likely moderate.", painPoints: ["payment pressure", "uncertainty", "time"], objections: ["needs closing confidence"], nextFollowUpDate: "2026-05-01", sellerTemperatureScore: 88, objectionStatus: "closing_confidence", followUpUrgency: "hot", nextBestSellerAction: "Draft calm follow-up; avoid urgency or guarantees.", draftOnly: true, liveOutreachAllowed: false },
  { id: "seller-interaction-006", leadId: "lead-008", callNotes: "Probate path and disclosure review must be clarified before assignment prep.", motivationAnswers: { whySell: "Estate administration", timeline: "depends on title", decisionMaker: "Representative authority needs confirmation" }, askingPrice: 171000, timeline: "title-dependent", propertyCondition: "Repairs likely heavy but ARV supports continued review.", painPoints: ["probate", "title", "repair scope"], objections: ["authority and paperwork"], nextFollowUpDate: "2026-05-05", sellerTemperatureScore: 76, objectionStatus: "compliance_review", followUpUrgency: "normal", nextBestSellerAction: "Hold until compliance review is complete.", draftOnly: true, liveOutreachAllowed: false }
];

export const offerPackets: OfferPacket[] = [
  { id: "packet-001", dealId: "deal-001", packetStatus: "draft_ready", ownerApprovalRecorded: true, complianceGuardPassed: true, buyerMarginProtected: true, targetAssignmentFeeChecked: true, underwritingComplete: true, packetPrepAllowed: true, blockedReasons: [], approvalStatus: "owner_approved_draft_ready", draftSummary: "Draft offer packet may be prepared for owner review only.", draftOnly: true, realWorldActionTaken: false },
  { id: "packet-002", dealId: "deal-003", packetStatus: "blocked", ownerApprovalRecorded: false, complianceGuardPassed: true, buyerMarginProtected: true, targetAssignmentFeeChecked: true, underwritingComplete: true, packetPrepAllowed: false, blockedReasons: ["owner_approval_not_recorded"], approvalStatus: "owner_review_required", draftSummary: "Owner approval needed before offer packet prep.", draftOnly: true, realWorldActionTaken: false },
  { id: "packet-003", dealId: "deal-005", packetStatus: "blocked", ownerApprovalRecorded: true, complianceGuardPassed: false, buyerMarginProtected: true, targetAssignmentFeeChecked: true, underwritingComplete: true, packetPrepAllowed: false, blockedReasons: ["compliance_guard_not_passed"], approvalStatus: "blocked", draftSummary: "Inherited-property authority review blocks offer packet prep.", draftOnly: true, realWorldActionTaken: false },
  { id: "packet-004", dealId: "deal-006", packetStatus: "blocked", ownerApprovalRecorded: true, complianceGuardPassed: true, buyerMarginProtected: false, targetAssignmentFeeChecked: false, underwritingComplete: true, packetPrepAllowed: false, blockedReasons: ["buyer_margin_not_protected", "target_assignment_fee_not_checked"], approvalStatus: "blocked", draftSummary: "Buyer margin and target assignment fee fail the gate.", draftOnly: true, realWorldActionTaken: false },
  { id: "packet-005", dealId: "deal-007", packetStatus: "blocked", ownerApprovalRecorded: true, complianceGuardPassed: true, buyerMarginProtected: true, targetAssignmentFeeChecked: false, underwritingComplete: true, packetPrepAllowed: false, blockedReasons: ["target_assignment_fee_not_checked"], approvalStatus: "blocked", draftSummary: "Projected assignment fee is below target.", draftOnly: true, realWorldActionTaken: false }
];

const contractChecklist = [
  "seller accepted terms captured",
  "property details verified",
  "assignment language review required",
  "seller role disclosure reminder",
  "attorney/title review reminder"
];

export const contractControls: ContractControlRecord[] = [
  { id: "contract-001", leadId: "lead-001", dealId: "deal-001", offerPacketId: "packet-001", sellerAcceptedTerms: { price: 151000, closingTimeline: "14-21 days", sellerAcknowledgesDraftOnly: true }, contractStatus: "prep_review", assignmentAllowedFlag: true, inspectionAccessNotes: "Access instructions are placeholders until owner confirms next step.", earnestMoneyNotes: "EMD amount to be reviewed by owner and title/attorney before any action.", closingTimeline: "14-21 days", titleCompanyPreference: "Owner-selected investor-friendly title company placeholder", requiredDocumentsChecklist: contractChecklist, ownerApprovalStatus: "approved", complianceReviewStatus: "approved", contractPrepAllowed: true, blockedReasons: [], draftOnly: true, executableContractGenerated: false, liveSendingAllowed: false, titleSubmissionAllowed: false, automaticStatusChangeAllowed: false },
  { id: "contract-002", leadId: "lead-003", dealId: "deal-003", offerPacketId: "packet-002", sellerAcceptedTerms: { price: 180000, closingTimeline: "30 days", sellerAcknowledgesDraftOnly: true }, contractStatus: "prep_review", assignmentAllowedFlag: true, inspectionAccessNotes: "Seller will review access options after owner approval.", earnestMoneyNotes: "Draft-only EMD note; no funds are collected in V4.", closingTimeline: "30 days", titleCompanyPreference: "Title preference pending owner confirmation", requiredDocumentsChecklist: contractChecklist, ownerApprovalStatus: "pending", complianceReviewStatus: "approved", contractPrepAllowed: false, blockedReasons: ["offer_packet_not_approved", "owner_approval_not_recorded"], draftOnly: true, executableContractGenerated: false, liveSendingAllowed: false, titleSubmissionAllowed: false, automaticStatusChangeAllowed: false },
  { id: "contract-003", leadId: "lead-005", dealId: "deal-005", offerPacketId: "packet-003", sellerAcceptedTerms: { price: 220000, closingTimeline: "21-30 days", sellerAcknowledgesDraftOnly: true }, contractStatus: "prep_review", assignmentAllowedFlag: false, inspectionAccessNotes: "Access blocked until authority and compliance review clear.", earnestMoneyNotes: "No EMD action until title/attorney review.", closingTimeline: "21-30 days", titleCompanyPreference: "Missing title company preference", requiredDocumentsChecklist: [...contractChecklist, "missing seller authority documentation"], ownerApprovalStatus: "approved", complianceReviewStatus: "pending", contractPrepAllowed: false, blockedReasons: ["compliance_guard_not_passed"], draftOnly: true, executableContractGenerated: false, liveSendingAllowed: false, titleSubmissionAllowed: false, automaticStatusChangeAllowed: false },
  { id: "contract-004", leadId: "lead-006", dealId: "deal-006", offerPacketId: "packet-004", sellerAcceptedTerms: {}, contractStatus: "blocked", assignmentAllowedFlag: false, inspectionAccessNotes: "No accepted terms; contract prep blocked.", earnestMoneyNotes: "No EMD action.", closingTimeline: "", titleCompanyPreference: "", requiredDocumentsChecklist: [...contractChecklist, "missing seller accepted terms", "missing title company preference"], ownerApprovalStatus: "approved", complianceReviewStatus: "approved", contractPrepAllowed: false, blockedReasons: ["seller_accepted_terms_missing", "buyer_margin_not_protected", "offer_packet_not_approved"], draftOnly: true, executableContractGenerated: false, liveSendingAllowed: false, titleSubmissionAllowed: false, automaticStatusChangeAllowed: false },
  { id: "contract-005", leadId: "lead-007", dealId: "deal-007", offerPacketId: "packet-005", sellerAcceptedTerms: { price: 75000, closingTimeline: "10-14 days", sellerAcknowledgesDraftOnly: true }, contractStatus: "prep_review", assignmentAllowedFlag: true, inspectionAccessNotes: "Access notes held for owner review; no live scheduling.", earnestMoneyNotes: "No EMD action; target assignment fee remains below threshold.", closingTimeline: "10-14 days", titleCompanyPreference: "Title preference pending compliance review", requiredDocumentsChecklist: contractChecklist, ownerApprovalStatus: "approved", complianceReviewStatus: "approved", contractPrepAllowed: false, blockedReasons: ["offer_packet_not_approved"], draftOnly: true, executableContractGenerated: false, liveSendingAllowed: false, titleSubmissionAllowed: false, automaticStatusChangeAllowed: false }
];

export const titleHandoffPackets: TitleHandoffPacket[] = [
  { id: "title-001", contractControlId: "contract-001", dealId: "deal-001", propertyDetails: { city: "Dallas", state: "TX", zip: "75216", propertyType: "single_family" }, sellerInfoPlaceholder: "Seller info placeholder; verify before any title-company contact.", buyerEntityInfoPlaceholder: "Buyer/entity info placeholder; owner must confirm before use.", agreedPrice: 151000, closingTimeline: "14-21 days", accessNotes: "Access notes remain placeholders until owner-approved next step.", assignmentStatus: "assignment_allowed_reviewed", requiredDocumentChecklist: contractChecklist, attorneyTitleReviewReminder: "Attorney/title review required before any real-world contract or handoff action.", packetStatus: "draft_ready", draftOnly: true, titleSubmissionAllowed: false, submittedToTitle: false, legalAdviceProvided: false },
  { id: "title-002", contractControlId: "contract-002", dealId: "deal-003", propertyDetails: { city: "Dallas", state: "TX", zip: "75224", propertyType: "single_family" }, sellerInfoPlaceholder: "Seller info placeholder; owner approval is still pending.", buyerEntityInfoPlaceholder: "Buyer/entity info placeholder; no title submission.", agreedPrice: 180000, closingTimeline: "30 days", accessNotes: "Access instructions require owner review.", assignmentStatus: "owner_review_required", requiredDocumentChecklist: contractChecklist, attorneyTitleReviewReminder: "Attorney/title review reminder only; no legal advice.", packetStatus: "blocked_owner_review", draftOnly: true, titleSubmissionAllowed: false, submittedToTitle: false, legalAdviceProvided: false },
  { id: "title-003", contractControlId: "contract-003", dealId: "deal-005", propertyDetails: { city: "Dallas", state: "TX", zip: "75216", propertyType: "duplex" }, sellerInfoPlaceholder: "Seller authority placeholder; heirs/title path must be reviewed.", buyerEntityInfoPlaceholder: "Buyer/entity info placeholder; blocked until compliance clears.", agreedPrice: 220000, closingTimeline: "21-30 days", accessNotes: "Access blocked until compliance review.", assignmentStatus: "compliance_blocked", requiredDocumentChecklist: [...contractChecklist, "missing seller authority documentation"], attorneyTitleReviewReminder: "Attorney/title review required before any title route is selected.", packetStatus: "blocked_compliance", draftOnly: true, titleSubmissionAllowed: false, submittedToTitle: false, legalAdviceProvided: false }
];

export const titleReviewCoordinations: TitleReviewCoordination[] = [
  { id: "title-review-001", dealId: "deal-001", contractReadyStateId: "contract-ready-001", selectedTitleCompanyPlaceholder: "Owner-selected investor-friendly title company placeholder", attorneyTitleReviewStatus: "packet_ready", requiredDocuments: contractChecklist, missingItems: [], reviewNotes: "Coordinate attorney/title review only after owner confirms draft packet readiness. No document submission.", ownerApprovalStatus: "approved", packetPrepAllowed: true, blockedReasons: [], draftOnly: true, legalAdviceAllowed: false, contractExecutionAllowed: false, documentSubmissionAllowed: false, titleCompanyEmailSendAllowed: false, attorneyClientRelationshipClaimed: false, closingGuaranteeAllowed: false },
  { id: "title-review-002", dealId: "deal-003", contractReadyStateId: "contract-ready-002", selectedTitleCompanyPlaceholder: "Title preference pending owner confirmation", attorneyTitleReviewStatus: "blocked", requiredDocuments: contractChecklist, missingItems: ["owner approval", "V10 contract-ready clearance"], reviewNotes: "Keep review packet blocked until owner approval and V10 conversion gates clear.", ownerApprovalStatus: "pending", packetPrepAllowed: false, blockedReasons: ["owner_approval_not_recorded", "v10_contract_ready_not_cleared", "seller_acceptance_readiness_not_high"], draftOnly: true, legalAdviceAllowed: false, contractExecutionAllowed: false, documentSubmissionAllowed: false, titleCompanyEmailSendAllowed: false, attorneyClientRelationshipClaimed: false, closingGuaranteeAllowed: false },
  { id: "title-review-003", dealId: "deal-005", contractReadyStateId: "contract-ready-003", selectedTitleCompanyPlaceholder: "Missing title company preference", attorneyTitleReviewStatus: "blocked", requiredDocuments: [...contractChecklist, "seller authority documentation"], missingItems: ["seller authority documentation", "compliance review"], reviewNotes: "Inherited-property authority review blocks title/attorney coordination packet prep.", ownerApprovalStatus: "approved", packetPrepAllowed: false, blockedReasons: ["v10_contract_ready_not_cleared", "compliance_not_passed", "numbers_not_locked"], draftOnly: true, legalAdviceAllowed: false, contractExecutionAllowed: false, documentSubmissionAllowed: false, titleCompanyEmailSendAllowed: false, attorneyClientRelationshipClaimed: false, closingGuaranteeAllowed: false },
  { id: "title-review-004", dealId: "deal-006", contractReadyStateId: "contract-ready-004", selectedTitleCompanyPlaceholder: "Title preference held until profit/risk review clears", attorneyTitleReviewStatus: "blocked", requiredDocuments: [...contractChecklist, "seller accepted terms", "locked numbers"], missingItems: ["locked numbers", "seller acceptance readiness"], reviewNotes: "Profit control and readiness blocks prevent attorney/title review packet prep.", ownerApprovalStatus: "approved", packetPrepAllowed: false, blockedReasons: ["v10_contract_ready_not_cleared", "numbers_not_locked", "seller_acceptance_readiness_not_high"], draftOnly: true, legalAdviceAllowed: false, contractExecutionAllowed: false, documentSubmissionAllowed: false, titleCompanyEmailSendAllowed: false, attorneyClientRelationshipClaimed: false, closingGuaranteeAllowed: false }
];

const titleReviewComplianceChecklist = [
  "contract reviewed by attorney/title company",
  "seller understands role",
  "buyer understands assignment",
  "assignment fee disclosure reviewed",
  "no legal advice provided",
  "no misrepresentation"
];

export const reviewPacketPreps: ReviewPacketPrep[] = [
  { id: "review-packet-001", titleReviewCoordinationId: "title-review-001", dealId: "deal-001", propertySummary: { city: "Dallas", state: "TX", zip: "75216", propertyType: "single_family" }, sellerTerms: { price: 151000, closingTimeline: "14-21 days", acceptedTermsRecorded: true }, buyerAssignmentReadinessSummary: { assignmentAllowed: true, buyerPofStatus: "verified", assignmentReadiness: "assignment_ready" }, closingTimeline: "14-21 days", accessNotes: "Access notes are placeholders until owner confirms the next step.", complianceChecklist: titleReviewComplianceChecklist, documentChecklist: contractChecklist, packetStatus: "draft_ready", prepAllowed: true, blockedReasons: [], draftOnly: true, legalAdviceAllowed: false, contractExecutionAllowed: false, documentSubmissionAllowed: false, titleCompanyEmailSendAllowed: false, submittedToTitle: false, attorneyClientRelationshipClaimed: false, closingGuaranteeAllowed: false },
  { id: "review-packet-002", titleReviewCoordinationId: "title-review-002", dealId: "deal-003", propertySummary: { city: "Dallas", state: "TX", zip: "75224", propertyType: "single_family" }, sellerTerms: { price: 180000, closingTimeline: "30 days", acceptedTermsRecorded: true }, buyerAssignmentReadinessSummary: { assignmentAllowed: true, buyerPofStatus: "verified", assignmentReadiness: "blocked" }, closingTimeline: "30 days", accessNotes: "Access instructions require owner review.", complianceChecklist: titleReviewComplianceChecklist, documentChecklist: contractChecklist, packetStatus: "blocked", prepAllowed: false, blockedReasons: ["owner_approval_not_recorded", "v10_contract_ready_not_cleared"], draftOnly: true, legalAdviceAllowed: false, contractExecutionAllowed: false, documentSubmissionAllowed: false, titleCompanyEmailSendAllowed: false, submittedToTitle: false, attorneyClientRelationshipClaimed: false, closingGuaranteeAllowed: false },
  { id: "review-packet-003", titleReviewCoordinationId: "title-review-003", dealId: "deal-005", propertySummary: { city: "Dallas", state: "TX", zip: "75216", propertyType: "duplex" }, sellerTerms: { price: 220000, closingTimeline: "21-30 days", acceptedTermsRecorded: true }, buyerAssignmentReadinessSummary: { assignmentAllowed: false, buyerPofStatus: "verified", assignmentReadiness: "blocked" }, closingTimeline: "21-30 days", accessNotes: "Access blocked until compliance review clears.", complianceChecklist: titleReviewComplianceChecklist, documentChecklist: [...contractChecklist, "seller authority documentation"], packetStatus: "blocked", prepAllowed: false, blockedReasons: ["compliance_not_passed", "v10_contract_ready_not_cleared"], draftOnly: true, legalAdviceAllowed: false, contractExecutionAllowed: false, documentSubmissionAllowed: false, titleCompanyEmailSendAllowed: false, submittedToTitle: false, attorneyClientRelationshipClaimed: false, closingGuaranteeAllowed: false }
];

const autonomousBlockedActions = [
  "send_sms",
  "send_email",
  "call_seller",
  "contact_buyer",
  "buyer_blast_execute",
  "bulk_send",
  "execute_contract",
  "submit_to_title_company",
  "publish_buyer_portal",
  "publish_seller_portal",
  "collect_payment",
  "give_legal_advice"
];

export const automationRules: AutomationRule[] = [
  { id: "rule-new-lead-intake", name: "New Lead Intake", workflowType: "new_lead_intake", autonomyLevel: 2, triggerEvent: "lead_imported", enabled: true, allowedActions: ["score_leads", "update_priority_queues", "create_agent_task"], blockedActions: autonomousBlockedActions, scheduleLabel: "event-triggered", ownerApprovalRequired: false, safetyStatus: "guarded", lastRunStatus: "completed", draftOnly: true, liveActionAllowed: false, level5Disabled: true, portalPublishAllowed: false, contractExecutionAllowed: false, titleSubmissionAllowed: false, paymentCollectionAllowed: false, notes: "Scores and routes new leads internally only." },
  { id: "rule-hot-deal-acceleration", name: "Hot Deal Acceleration", workflowType: "hot_deal_acceleration", autonomyLevel: 3, triggerEvent: "deal_speed_score_high", enabled: true, allowedActions: ["create_next_best_action", "create_follow_up_draft", "create_blocker_record", "escalate_urgent_deal"], blockedActions: autonomousBlockedActions, scheduleLabel: "every 30 minutes while active", ownerApprovalRequired: false, safetyStatus: "guarded", lastRunStatus: "completed", draftOnly: true, liveActionAllowed: false, level5Disabled: true, portalPublishAllowed: false, contractExecutionAllowed: false, titleSubmissionAllowed: false, paymentCollectionAllowed: false, notes: "Creates drafts, blockers, and owner escalations without outreach." },
  { id: "rule-buyer-demand-refresh", name: "Buyer Demand Refresh", workflowType: "buyer_demand_refresh", autonomyLevel: 2, triggerEvent: "buyer_queue_refresh", enabled: true, allowedActions: ["refresh_buyer_demand", "create_buyer_distribution_draft", "update_priority_queues"], blockedActions: autonomousBlockedActions, scheduleLabel: "twice daily", ownerApprovalRequired: false, safetyStatus: "guarded", lastRunStatus: "completed", draftOnly: true, liveActionAllowed: false, level5Disabled: true, portalPublishAllowed: false, contractExecutionAllowed: false, titleSubmissionAllowed: false, paymentCollectionAllowed: false, notes: "Refreshes buyer fit and prepares one-recipient drafts only." },
  { id: "rule-contract-readiness", name: "Contract Readiness", workflowType: "contract_readiness", autonomyLevel: 3, triggerEvent: "gates_passed", enabled: true, allowedActions: ["mark_internal_readiness", "create_offer_packet_draft", "create_evidence_packet"], blockedActions: autonomousBlockedActions, scheduleLabel: "event-triggered", ownerApprovalRequired: false, safetyStatus: "guarded", lastRunStatus: "completed", draftOnly: true, liveActionAllowed: false, level5Disabled: true, portalPublishAllowed: false, contractExecutionAllowed: false, titleSubmissionAllowed: false, paymentCollectionAllowed: false, notes: "Marks internal readiness states only when gates pass." },
  { id: "rule-daily-command-briefing", name: "Daily Command Briefing", workflowType: "daily_command_briefing", autonomyLevel: 3, triggerEvent: "daily_schedule", enabled: true, allowedActions: ["create_daily_briefing", "create_manager_queue"], blockedActions: autonomousBlockedActions, scheduleLabel: "daily 7:00 AM", ownerApprovalRequired: false, safetyStatus: "guarded", lastRunStatus: "completed", draftOnly: true, liveActionAllowed: false, level5Disabled: true, portalPublishAllowed: false, contractExecutionAllowed: false, titleSubmissionAllowed: false, paymentCollectionAllowed: false, notes: "Creates internal Prime 2 briefings and owner queues." },
  { id: "rule-controlled-live-review", name: "Controlled Live Action Review", workflowType: "controlled_live_action_review", autonomyLevel: 4, triggerEvent: "owner_requested_live_review", enabled: true, allowedActions: ["controlled_live_action_review"], blockedActions: autonomousBlockedActions, scheduleLabel: "manual owner approval only", ownerApprovalRequired: true, safetyStatus: "owner_approval_required", lastRunStatus: "not_run", draftOnly: true, liveActionAllowed: false, level5Disabled: true, portalPublishAllowed: false, contractExecutionAllowed: false, titleSubmissionAllowed: false, paymentCollectionAllowed: false, notes: "Level 4 can queue review only; execution stays behind owner and provider gates." }
];

export const schedulerRuns: SchedulerRun[] = [
  { id: "run-new-lead-001", ruleId: "rule-new-lead-intake", workflowType: "new_lead_intake", runStatus: "completed", scheduledFor: "2026-05-04T13:00:00Z", idempotencyKey: "seed:new-lead-intake:2026-05-04", createdTasks: 2, createdAttempts: 1, escalationCreated: false, dailyBriefingCreated: false, summary: { leadIds: "lead-001, lead-002", realWorldActionTaken: false }, ownerApprovalRequired: false, autonomyLevel: 2, idempotentReplay: false, realWorldActionTaken: false },
  { id: "run-hot-deal-001", ruleId: "rule-hot-deal-acceleration", workflowType: "hot_deal_acceleration", runStatus: "completed", scheduledFor: "2026-05-04T13:00:00Z", idempotencyKey: "seed:hot-deal-acceleration:deal-001", createdTasks: 2, createdAttempts: 1, escalationCreated: true, dailyBriefingCreated: false, summary: { dealId: "deal-001", escalation: "hot_10k_spread" }, ownerApprovalRequired: false, autonomyLevel: 3, idempotentReplay: false, realWorldActionTaken: false },
  { id: "run-buyer-demand-001", ruleId: "rule-buyer-demand-refresh", workflowType: "buyer_demand_refresh", runStatus: "completed", scheduledFor: "2026-05-04T13:00:00Z", idempotencyKey: "seed:buyer-demand-refresh:2026-05-04", createdTasks: 1, createdAttempts: 1, escalationCreated: false, dailyBriefingCreated: false, summary: { buyersRefreshed: 10, buyerBlastsSent: 0 }, ownerApprovalRequired: false, autonomyLevel: 2, idempotentReplay: false, realWorldActionTaken: false },
  { id: "run-contract-readiness-001", ruleId: "rule-contract-readiness", workflowType: "contract_readiness", runStatus: "completed", scheduledFor: "2026-05-04T13:00:00Z", idempotencyKey: "seed:contract-readiness:deal-001", createdTasks: 2, createdAttempts: 1, escalationCreated: false, dailyBriefingCreated: false, summary: { dealId: "deal-001", internalReadinessMarked: true }, ownerApprovalRequired: false, autonomyLevel: 3, idempotentReplay: false, realWorldActionTaken: false },
  { id: "run-daily-briefing-001", ruleId: "rule-daily-command-briefing", workflowType: "daily_command_briefing", runStatus: "completed", scheduledFor: "2026-05-04T13:00:00Z", idempotencyKey: "seed:daily-briefing:2026-05-04", createdTasks: 1, createdAttempts: 1, escalationCreated: false, dailyBriefingCreated: true, summary: { briefingId: "daily-briefing-001", recommendationsOnly: true }, ownerApprovalRequired: false, autonomyLevel: 3, idempotentReplay: false, realWorldActionTaken: false }
];

export const automationAttempts: AutomationAttempt[] = [
  { id: "attempt-score-leads-001", runId: "run-new-lead-001", actionType: "score_leads", sourceRecordType: "lead", sourceRecordId: "lead-001", attemptStatus: "prepared", autonomyLevel: 2, safetyResult: { allowed: true, realWorldActionAllowed: false }, blockedReasons: [], ownerApprovalRequired: false, ownerApprovalRecorded: false, providerCalled: false, realWorldActionTaken: false, idempotencyKey: "seed:attempt-score-leads-001" },
  { id: "attempt-hot-deal-nba-001", runId: "run-hot-deal-001", actionType: "create_next_best_action", sourceRecordType: "deal", sourceRecordId: "deal-001", attemptStatus: "prepared", autonomyLevel: 3, safetyResult: { allowed: true, realWorldActionAllowed: false }, blockedReasons: [], ownerApprovalRequired: false, ownerApprovalRecorded: false, providerCalled: false, realWorldActionTaken: false, idempotencyKey: "seed:attempt-hot-deal-nba-001" },
  { id: "attempt-buyer-demand-001", runId: "run-buyer-demand-001", actionType: "refresh_buyer_demand", sourceRecordType: "deal", sourceRecordId: "deal-001", attemptStatus: "prepared", autonomyLevel: 2, safetyResult: { allowed: true, realWorldActionAllowed: false }, blockedReasons: [], ownerApprovalRequired: false, ownerApprovalRecorded: false, providerCalled: false, realWorldActionTaken: false, idempotencyKey: "seed:attempt-buyer-demand-001" },
  { id: "attempt-readiness-001", runId: "run-contract-readiness-001", actionType: "mark_internal_readiness", sourceRecordType: "deal", sourceRecordId: "deal-001", attemptStatus: "prepared", autonomyLevel: 3, safetyResult: { allowed: true, realWorldActionAllowed: false }, blockedReasons: [], ownerApprovalRequired: false, ownerApprovalRecorded: false, providerCalled: false, realWorldActionTaken: false, idempotencyKey: "seed:attempt-readiness-001" },
  { id: "attempt-briefing-001", runId: "run-daily-briefing-001", actionType: "create_daily_briefing", sourceRecordType: "system", sourceRecordId: "wholesale-prime", attemptStatus: "prepared", autonomyLevel: 3, safetyResult: { allowed: true, realWorldActionAllowed: false }, blockedReasons: [], ownerApprovalRequired: false, ownerApprovalRecorded: false, providerCalled: false, realWorldActionTaken: false, idempotencyKey: "seed:attempt-briefing-001" },
  { id: "attempt-blocked-send-sms", runId: "run-hot-deal-001", actionType: "send_sms", sourceRecordType: "deal", sourceRecordId: "deal-001", attemptStatus: "blocked", autonomyLevel: 3, safetyResult: { allowed: false, realWorldActionAllowed: false }, blockedReasons: ["send_sms"], ownerApprovalRequired: false, ownerApprovalRecorded: false, providerCalled: false, realWorldActionTaken: false, idempotencyKey: "seed:blocked:send_sms" },
  { id: "attempt-blocked-buyer-blast-execute", runId: "run-hot-deal-001", actionType: "buyer_blast_execute", sourceRecordType: "deal", sourceRecordId: "deal-001", attemptStatus: "blocked", autonomyLevel: 3, safetyResult: { allowed: false, realWorldActionAllowed: false }, blockedReasons: ["buyer_blast_execute"], ownerApprovalRequired: false, ownerApprovalRecorded: false, providerCalled: false, realWorldActionTaken: false, idempotencyKey: "seed:blocked:buyer_blast_execute" },
  { id: "attempt-blocked-execute-contract", runId: "run-hot-deal-001", actionType: "execute_contract", sourceRecordType: "deal", sourceRecordId: "deal-001", attemptStatus: "blocked", autonomyLevel: 3, safetyResult: { allowed: false, realWorldActionAllowed: false }, blockedReasons: ["execute_contract"], ownerApprovalRequired: false, ownerApprovalRecorded: false, providerCalled: false, realWorldActionTaken: false, idempotencyKey: "seed:blocked:execute_contract" },
  { id: "attempt-blocked-submit-to-title-company", runId: "run-hot-deal-001", actionType: "submit_to_title_company", sourceRecordType: "deal", sourceRecordId: "deal-001", attemptStatus: "blocked", autonomyLevel: 3, safetyResult: { allowed: false, realWorldActionAllowed: false }, blockedReasons: ["submit_to_title_company"], ownerApprovalRequired: false, ownerApprovalRecorded: false, providerCalled: false, realWorldActionTaken: false, idempotencyKey: "seed:blocked:submit_to_title_company" },
  { id: "attempt-blocked-publish-buyer-portal", runId: "run-hot-deal-001", actionType: "publish_buyer_portal", sourceRecordType: "deal", sourceRecordId: "deal-001", attemptStatus: "blocked", autonomyLevel: 3, safetyResult: { allowed: false, realWorldActionAllowed: false }, blockedReasons: ["publish_buyer_portal"], ownerApprovalRequired: true, ownerApprovalRecorded: false, providerCalled: false, realWorldActionTaken: false, idempotencyKey: "seed:blocked:publish_buyer_portal" }
];

export const autonomousAgentTasks: AutonomousAgentTask[] = [
  { id: "auto-task-001", ruleId: "rule-new-lead-intake", runId: "run-new-lead-001", agentName: "Attention Queue Agent", division: "Operations Command Division", taskType: "lead_scoring", sourceRecordType: "lead", sourceRecordId: "lead-001", priority: "high", status: "queued_for_internal_review", recommendation: "Refresh motivation, equity, contactability, and data confidence; route missing repair inputs.", dueAt: "2026-05-04T16:00:00Z", idempotencyKey: "seed:auto-task-001", ownerApprovalRequired: false, draftOnly: true, liveActionAllowed: false, readinessMarked: false },
  { id: "auto-task-002", ruleId: "rule-new-lead-intake", runId: "run-new-lead-001", agentName: "KPI Agent", division: "Operations Command Division", taskType: "priority_queue_update", sourceRecordType: "lead", sourceRecordId: "lead-002", priority: "high", status: "queued_for_internal_review", recommendation: "Move the inherited vacant lead into the offer-needed review queue.", dueAt: "2026-05-04T16:00:00Z", idempotencyKey: "seed:auto-task-002", ownerApprovalRequired: false, draftOnly: true, liveActionAllowed: false, readinessMarked: false },
  { id: "auto-task-003", ruleId: "rule-hot-deal-acceleration", runId: "run-hot-deal-001", agentName: "Seller Script Agent", division: "Seller Acquisition Division", taskType: "follow_up_draft", sourceRecordType: "lead", sourceRecordId: "lead-001", priority: "critical", status: "draft_ready_for_owner", recommendation: "Prepare safe follow-up language explaining the as-is offer basis without pressure or fake buyer claims.", dueAt: "2026-05-04T16:00:00Z", idempotencyKey: "seed:auto-task-003", ownerApprovalRequired: true, draftOnly: true, liveActionAllowed: false, readinessMarked: false },
  { id: "auto-task-004", ruleId: "rule-buyer-demand-refresh", runId: "run-buyer-demand-001", agentName: "Buyer Demand Agent", division: "Buyer Disposition Division", taskType: "buyer_distribution_draft", sourceRecordType: "deal", sourceRecordId: "deal-001", priority: "high", status: "draft_ready_for_owner", recommendation: "Create one-buyer sanitized deal sheet draft for the highest-ranked verified buyer only.", dueAt: "2026-05-04T16:00:00Z", idempotencyKey: "seed:auto-task-004", ownerApprovalRequired: true, draftOnly: true, liveActionAllowed: false, readinessMarked: false },
  { id: "auto-task-005", ruleId: "rule-contract-readiness", runId: "run-contract-readiness-001", agentName: "Offer Explanation Agent", division: "Seller Acquisition Division", taskType: "offer_packet_draft", sourceRecordType: "deal", sourceRecordId: "deal-001", priority: "high", status: "draft_ready_for_owner", recommendation: "Assemble offer packet draft after checking underwriting, buyer margin, target spread, compliance, and owner approval.", dueAt: "2026-05-04T16:00:00Z", idempotencyKey: "seed:auto-task-005", ownerApprovalRequired: true, draftOnly: true, liveActionAllowed: false, readinessMarked: false },
  { id: "auto-task-006", ruleId: "rule-contract-readiness", runId: "run-contract-readiness-001", agentName: "Deal Confidence Agent", division: "Deal Underwriting Division", taskType: "contract_readiness", sourceRecordType: "deal", sourceRecordId: "deal-001", priority: "high", status: "readiness_marked_internal", recommendation: "Mark contract-ready only as internal readiness for external attorney/title drafting review.", dueAt: "2026-05-04T16:00:00Z", idempotencyKey: "seed:auto-task-006", ownerApprovalRequired: true, draftOnly: true, liveActionAllowed: false, readinessMarked: true },
  { id: "auto-task-007", ruleId: "rule-hot-deal-acceleration", runId: "run-hot-deal-001", agentName: "Risk Escalation Agent", division: "Operations Command Division", taskType: "blocker_record", sourceRecordType: "deal", sourceRecordId: "deal-005", priority: "critical", status: "queued_for_internal_review", recommendation: "Create blocker for missing seller authority and compliance review before title or portal movement.", dueAt: "2026-05-04T16:00:00Z", idempotencyKey: "seed:auto-task-007", ownerApprovalRequired: true, draftOnly: true, liveActionAllowed: false, readinessMarked: false },
  { id: "auto-task-008", ruleId: "rule-daily-command-briefing", runId: "run-daily-briefing-001", agentName: "Daily Briefing Agent", division: "Operations Command Division", taskType: "daily_briefing", sourceRecordType: "system", sourceRecordId: "wholesale-prime", priority: "normal", status: "completed", recommendation: "Publish internal command briefing to the owner dashboard only.", dueAt: "2026-05-04T16:00:00Z", idempotencyKey: "seed:auto-task-008", ownerApprovalRequired: false, draftOnly: true, liveActionAllowed: false, readinessMarked: false }
];

export const automationEventTriggers: AutomationEventTrigger[] = [
  { id: "auto-trigger-001", ruleId: "rule-new-lead-intake", eventType: "lead_imported", sourceRecordType: "lead", sourceRecordId: "lead-001", workflowType: "new_lead_intake", payload: { source: "driving_for_dollars", csvReady: true }, status: "processed", idempotencyKey: "seed:auto-trigger-001", processed: true },
  { id: "auto-trigger-002", ruleId: "rule-hot-deal-acceleration", eventType: "deal_speed_score_high", sourceRecordType: "deal", sourceRecordId: "deal-001", workflowType: "hot_deal_acceleration", payload: { projectedAssignmentFee: 17000, dealSpeedScore: 93 }, status: "processed", idempotencyKey: "seed:auto-trigger-002", processed: true },
  { id: "auto-trigger-003", ruleId: "rule-buyer-demand-refresh", eventType: "buyer_queue_refresh", sourceRecordType: "buyer", sourceRecordId: "buyer-001", workflowType: "buyer_demand_refresh", payload: { pofStatus: "verified", closingSpeedScore: 92 }, status: "processed", idempotencyKey: "seed:auto-trigger-003", processed: true },
  { id: "auto-trigger-004", ruleId: "rule-contract-readiness", eventType: "gates_passed", sourceRecordType: "deal", sourceRecordId: "deal-001", workflowType: "contract_readiness", payload: { contractReady: true, ownerApprovalRecorded: true }, status: "processed", idempotencyKey: "seed:auto-trigger-004", processed: true },
  { id: "auto-trigger-005", ruleId: "rule-daily-command-briefing", eventType: "daily_schedule", sourceRecordType: "system", sourceRecordId: "wholesale-prime", workflowType: "daily_command_briefing", payload: { localTime: "07:00" }, status: "processed", idempotencyKey: "seed:auto-trigger-005", processed: true }
];

export const dailyCommandBriefings: DailyCommandBriefing[] = [
  { id: "daily-briefing-001", runId: "run-daily-briefing-001", briefingDate: "2026-05-04", generatedBy: "Prime 2", hotDeals: [{ dealId: "deal-001", projectedAssignmentFee: 17000, dealSpeedScore: 93 }, { dealId: "deal-003", projectedAssignmentFee: 15000, dealSpeedScore: 90 }, { dealId: "deal-005", projectedAssignmentFee: 18000, dealSpeedScore: 87 }], priorityActions: ["Review hot deal escalation for deal-001.", "Resolve seller authority blocker on deal-005 before title movement.", "Approve or reject draft-only buyer distribution packet for deal-001.", "Keep all live outreach, contracts, title submission, and portal publishing owner-gated."], managerQueue: [{ division: "Operations Command Division", manager: "Sofia Grant", nextBestAction: "Review escalations and blocked automation attempts." }, { division: "Buyer Disposition Division", manager: "Darius Cole", nextBestAction: "Verify POF gaps before any distribution draft review." }], escalations: [{ id: "auto-escalation-001", severity: "critical", reason: "Hot 10K+ spread needs owner review." }], safetySummary: { autonomousLiveOutreach: false, autonomousBuyerBlasts: false, autonomousContractExecution: false, autonomousTitleSubmission: false, autonomousPortalPublishing: false, level5Available: false }, ownerReviewItems: ["Owner approval remains required for Level 4.", "Blocked attempts were recorded without provider calls.", "No binding commitments were created."], draftOnly: true, legalAdviceAllowed: false, liveOutreachAllowed: false, portalPublishAllowed: false, titleSubmissionAllowed: false, contractExecutionAllowed: false }
];

export const autonomyEscalations: AutonomyEscalation[] = [
  { id: "auto-escalation-001", runId: "run-hot-deal-001", dealId: "deal-001", leadId: "lead-001", escalationType: "hot_deal_acceleration", severity: "critical", reason: "Deal-001 protects a 10K+ spread and has verified buyer demand, but owner review is still required before any real-world move.", recommendedAction: "Review seller follow-up draft, buyer POF, compliance status, and owner approvals.", status: "open", ownerActionRequired: true, autonomyLevel: 3, realWorldActionBlocked: true, idempotencyKey: "seed:auto-escalation-001" },
  { id: "auto-escalation-002", runId: "run-hot-deal-001", dealId: "deal-005", leadId: "lead-005", escalationType: "compliance_blocker", severity: "high", reason: "Inherited property path needs seller authority and compliance review before title, portal, or assignment readiness movement.", recommendedAction: "Resolve compliance blocker and missing seller documents; do not publish or submit anything.", status: "open", ownerActionRequired: true, autonomyLevel: 3, realWorldActionBlocked: true, idempotencyKey: "seed:auto-escalation-002" }
];

export const approvedTemplates: ApprovedTemplate[] = [
  { id: "template-seller-followup-safe", templateName: "Approved Seller Follow-Up Draft", templateType: "seller_follow_up", channel: "sms", recipientType: "seller", subject: "", body: "Hi {{seller_first_name}}, this is a draft follow-up for owner review. We can talk through the as-is offer basis when convenient. Reply STOP to opt out.", approved: true, safetyStatus: "approved", riskFlags: [], requiresOptOut: true, includesOptOut: true, legalAdviceAllowed: false, pressureLanguageAllowed: false, fakeUrgencyAllowed: false, fakeBuyerClaimAllowed: false, draftOnlyDefault: true },
  { id: "template-buyer-response-safe", templateName: "Approved Buyer Interest Response", templateType: "buyer_response", channel: "email", recipientType: "buyer", subject: "Draft response on deal interest", body: "Thanks for the interest. The owner will review proof of funds and deal-room details before any next step. This is not a contract or commitment.", approved: true, safetyStatus: "approved", riskFlags: [], requiresOptOut: false, includesOptOut: false, legalAdviceAllowed: false, pressureLanguageAllowed: false, fakeUrgencyAllowed: false, fakeBuyerClaimAllowed: false, draftOnlyDefault: true },
  { id: "template-internal-reminder", templateName: "Internal Owner Reminder", templateType: "internal_reminder", channel: "internal", recipientType: "owner", subject: "Review queued deal action", body: "Internal reminder: review the gated action, dry-run receipt, safety result, and idempotency record before approval.", approved: true, safetyStatus: "approved", riskFlags: [], requiresOptOut: false, includesOptOut: false, legalAdviceAllowed: false, pressureLanguageAllowed: false, fakeUrgencyAllowed: false, fakeBuyerClaimAllowed: false, draftOnlyDefault: true },
  { id: "template-title-review-coordination", templateName: "Title Review Coordination Draft", templateType: "title_review_coordination", channel: "email", recipientType: "internal", subject: "Draft title review coordination", body: "Draft-only coordination note: confirm required documents, owner approval, and attorney/title review reminder before any external action.", approved: true, safetyStatus: "approved", riskFlags: [], requiresOptOut: false, includesOptOut: false, legalAdviceAllowed: false, pressureLanguageAllowed: false, fakeUrgencyAllowed: false, fakeBuyerClaimAllowed: false, draftOnlyDefault: true },
  { id: "template-unsafe-pressure", templateName: "Blocked Pressure Example", templateType: "seller_follow_up", channel: "sms", recipientType: "seller", subject: "", body: "You must sign now. This is your last chance and we already have a buyer.", approved: false, safetyStatus: "blocked", riskFlags: ["pressure_language", "fake_urgency", "fake_buyer_claim", "missing_sms_opt_out"], requiresOptOut: true, includesOptOut: false, legalAdviceAllowed: false, pressureLanguageAllowed: false, fakeUrgencyAllowed: false, fakeBuyerClaimAllowed: false, draftOnlyDefault: true }
];

export const autoExecutionRules: AutoExecutionRule[] = [
  { id: "auto-rule-internal-reminder", ruleName: "Create Internal Owner Reminder", actionType: "internal_reminder", sourceType: "autonomy_escalation", allowedRecipientType: "owner", trigger: "escalation_created", requiredConditions: ["source_record_exists", "template_approved"], approvedTemplateId: "template-internal-reminder", autonomyLevel: 3, liveFlagRequired: false, riskScore: 5, ownerApprovalStatus: "approved", status: "approved", blockedReasons: [], bulkSendAllowed: false, buyerBlastAllowed: false, legalContractMessageAllowed: false, coldSmsAllowed: false },
  { id: "auto-rule-seller-followup-draft", ruleName: "Approved Seller Follow-Up Draft", actionType: "seller_follow_up_draft", sourceType: "seller_interaction", allowedRecipientType: "seller", trigger: "follow_up_due", requiredConditions: ["template_approved", "seller_source_tied", "owner_review_queue"], approvedTemplateId: "template-seller-followup-safe", autonomyLevel: 3, liveFlagRequired: false, riskScore: 18, ownerApprovalStatus: "approved", status: "approved", blockedReasons: [], bulkSendAllowed: false, buyerBlastAllowed: false, legalContractMessageAllowed: false, coldSmsAllowed: false },
  { id: "auto-rule-buyer-response-send", ruleName: "Approved Low-Risk Buyer Response Send", actionType: "low_risk_single_message_send", sourceType: "buyer_interest", allowedRecipientType: "buyer", trigger: "buyer_interest_received", requiredConditions: ["template_approved", "v5_safety_passed", "v5_dry_run_receipt", "v5_owner_approval", "live_flags_enabled", "provider_ready", "single_recipient"], approvedTemplateId: "template-buyer-response-safe", autonomyLevel: 4, liveFlagRequired: true, riskScore: 22, ownerApprovalStatus: "approved", status: "approved", blockedReasons: [], bulkSendAllowed: false, buyerBlastAllowed: false, legalContractMessageAllowed: false, coldSmsAllowed: false },
  { id: "auto-rule-blocked-bulk", ruleName: "Blocked Buyer Blast Example", actionType: "buyer_blast", sourceType: "deal_distribution", allowedRecipientType: "buyer", trigger: "hot_deal_created", requiredConditions: ["blocked_by_design"], approvedTemplateId: "template-buyer-response-safe", autonomyLevel: 4, liveFlagRequired: true, riskScore: 90, ownerApprovalStatus: "pending", status: "blocked", blockedReasons: ["buyer_blast_blocked"], bulkSendAllowed: false, buyerBlastAllowed: false, legalContractMessageAllowed: false, coldSmsAllowed: false }
];

export const autoExecutionDryRuns: AutoExecutionDryRun[] = [
  { id: "auto-dryrun-001", ruleId: "auto-rule-buyer-response-send", templateId: "template-buyer-response-safe", sourceRecordType: "buyer_interest", sourceRecordId: "interest-001", recipientType: "buyer", recipientPlaceholder: "buyer-email-placeholder", subjectBodyHash: "hash-auto-buyer-safe", safetyPassed: true, riskStatus: "clear", providerMode: "mock/dry_run", idempotencyKey: "seed:auto-execution-dryrun-001", status: "created" },
  { id: "auto-dryrun-002", ruleId: "auto-rule-seller-followup-draft", templateId: "template-unsafe-pressure", sourceRecordType: "seller_interaction", sourceRecordId: "seller-interaction-005", recipientType: "seller", recipientPlaceholder: "seller-phone-placeholder", subjectBodyHash: "hash-auto-pressure-blocked", safetyPassed: false, riskStatus: "blocked", providerMode: "mock/dry_run", idempotencyKey: "seed:auto-execution-dryrun-002", status: "blocked" }
];

export const autoExecutionAttempts: AutoExecutionAttempt[] = [
  { id: "auto-attempt-001", ruleId: "auto-rule-internal-reminder", templateId: "template-internal-reminder", dryRunId: null, actionType: "internal_reminder", sourceRecordType: "autonomy_escalation", sourceRecordId: "auto-escalation-001", recipientType: "owner", recipientCount: 1, attemptStatus: "completed_internal", blockedReasons: [], ownerApprovalRecorded: true, v5SafetyPassed: false, v5DryRunReceiptExists: false, v5ApprovalRecorded: false, liveFlagsEnabled: false, providerReady: false, providerCalled: false, providerMode: "internal", idempotencyKey: "seed:auto-attempt-001", auditRecordCreated: true },
  { id: "auto-attempt-002", ruleId: "auto-rule-buyer-response-send", templateId: "template-buyer-response-safe", dryRunId: "auto-dryrun-001", actionType: "low_risk_single_message_send", sourceRecordType: "buyer_interest", sourceRecordId: "interest-001", recipientType: "buyer", recipientCount: 1, attemptStatus: "mock_sent", blockedReasons: [], ownerApprovalRecorded: true, v5SafetyPassed: true, v5DryRunReceiptExists: true, v5ApprovalRecorded: true, liveFlagsEnabled: true, providerReady: true, providerCalled: true, providerMode: "mock/dry_run", idempotencyKey: "seed:auto-attempt-002", auditRecordCreated: true },
  { id: "auto-attempt-003", ruleId: "auto-rule-blocked-bulk", templateId: "template-buyer-response-safe", dryRunId: null, actionType: "buyer_blast", sourceRecordType: "deal_distribution", sourceRecordId: "distribution-001", recipientType: "buyer", recipientCount: 12, attemptStatus: "blocked", blockedReasons: ["action_not_allowed_for_auto_execution", "single_recipient_required", "risk_score_too_high"], ownerApprovalRecorded: false, v5SafetyPassed: false, v5DryRunReceiptExists: false, v5ApprovalRecorded: false, liveFlagsEnabled: false, providerReady: false, providerCalled: false, providerMode: "blocked", idempotencyKey: "seed:auto-attempt-003", auditRecordCreated: true }
];

export const autoExecutionAuditRecords: AutoExecutionAuditRecord[] = [
  { id: "auto-audit-001", attemptId: "auto-attempt-001", ruleId: "auto-rule-internal-reminder", eventType: "internal_reminder_created", sourceRecordType: "autonomy_escalation", sourceRecordId: "auto-escalation-001", outcome: "completed_internal", blockedReasons: [], providerCalled: false, idempotencyKey: "seed:auto-audit-001" },
  { id: "auto-audit-002", attemptId: "auto-attempt-002", ruleId: "auto-rule-buyer-response-send", eventType: "single_execution_attempt", sourceRecordType: "buyer_interest", sourceRecordId: "interest-001", outcome: "mock_sent", blockedReasons: [], providerCalled: true, idempotencyKey: "seed:auto-audit-002" },
  { id: "auto-audit-003", attemptId: "auto-attempt-003", ruleId: "auto-rule-blocked-bulk", eventType: "blocked_execution_attempt", sourceRecordType: "deal_distribution", sourceRecordId: "distribution-001", outcome: "blocked", blockedReasons: ["action_not_allowed_for_auto_execution", "single_recipient_required"], providerCalled: false, idempotencyKey: "seed:auto-audit-003" }
];

export const buyerAccelerationRecords: BuyerAccelerationRecord[] = [
  {
    id: "buyer-accel-001",
    dealId: "deal-001",
    buyerRankingSnapshot: [
      { buyerId: "buyer-001", rank: 1, priorityScore: 96 },
      { buyerId: "buyer-002", rank: 2, priorityScore: 89 }
    ],
    topBuyerList: ["buyer-001", "buyer-002"],
    pofStatus: "verified",
    buyerReliability: 94,
    buyerMarginStrength: 92,
    distributionReadiness: "ready",
    ownerApprovalStatus: "approved",
    blockedReasons: [],
    controlledSendAllowed: true,
    buyerVisible: true,
    sanitizedDealSheetReady: true,
    buyerMatchApproved: true,
    compliancePassed: true,
    v13GatePassed: true,
    v5GatePassed: true,
    bulkBlastAllowed: false
  },
  {
    id: "buyer-accel-002",
    dealId: "deal-003",
    buyerRankingSnapshot: [{ buyerId: "buyer-001", rank: 1, priorityScore: 87 }],
    topBuyerList: ["buyer-001"],
    pofStatus: "pof_request_allowed",
    buyerReliability: 90,
    buyerMarginStrength: 86,
    distributionReadiness: "ready",
    ownerApprovalStatus: "approved",
    blockedReasons: [],
    controlledSendAllowed: true,
    buyerVisible: true,
    sanitizedDealSheetReady: true,
    buyerMatchApproved: true,
    compliancePassed: true,
    v13GatePassed: true,
    v5GatePassed: true,
    bulkBlastAllowed: false
  },
  {
    id: "buyer-accel-003",
    dealId: "deal-005",
    buyerRankingSnapshot: [{ buyerId: "buyer-004", rank: 1, priorityScore: 84 }],
    topBuyerList: ["buyer-004"],
    pofStatus: "verified",
    buyerReliability: 88,
    buyerMarginStrength: 62,
    distributionReadiness: "blocked",
    ownerApprovalStatus: "pending",
    blockedReasons: ["deal_not_buyer_visible", "compliance_not_passed", "buyer_margin_weak", "owner_approval_not_recorded"],
    controlledSendAllowed: false,
    buyerVisible: false,
    sanitizedDealSheetReady: false,
    buyerMatchApproved: true,
    compliancePassed: false,
    v13GatePassed: false,
    v5GatePassed: false,
    bulkBlastAllowed: false
  }
];

const safeBuyerNotice = "Draft: a sanitized deal room is available for owner-approved review. This is informational only.";

export const buyerSequencePreps: BuyerSequencePrep[] = [
  {
    id: "buyer-sequence-001",
    dealId: "deal-001",
    buyerId: "buyer-001",
    accelerationRecordId: "buyer-accel-001",
    firstBuyerNotice: safeBuyerNotice,
    buyerDetailFollowUp: "Draft: confirm whether the sanitized ARV range, repair range, and asking price fit your buy box.",
    pofRequest: "Draft: please provide current proof-of-funds status before any access coordination.",
    viewingAccessCoordination: "Draft: access instructions are placeholders until owner review clears.",
    offerIntentFollowUp: "Draft: submit non-binding offer intent for owner review only.",
    deadlineReminder: "Draft reminder: owner is reviewing interest; no scarcity or guarantee is implied.",
    safetyStatus: "approved",
    blockedReasons: [],
    draftOnly: true,
    liveSendAllowed: false,
    bulkBlastAllowed: false,
    deceptiveScarcityAllowed: false,
    sellerPrivateDataExposed: false,
    internalProfitLogicExposed: false
  },
  {
    id: "buyer-sequence-002",
    dealId: "deal-003",
    buyerId: "buyer-001",
    accelerationRecordId: "buyer-accel-002",
    firstBuyerNotice: safeBuyerNotice,
    buyerDetailFollowUp: "Draft: review sanitized repair notes and price fit.",
    pofRequest: "Draft: POF refresh requested before access review.",
    viewingAccessCoordination: "Draft: viewing/access request will be routed to owner.",
    offerIntentFollowUp: "Draft: offer intent remains non-binding until owner review.",
    deadlineReminder: "Draft reminder: availability may change after owner review; no urgency claim.",
    safetyStatus: "approved",
    blockedReasons: [],
    draftOnly: true,
    liveSendAllowed: false,
    bulkBlastAllowed: false,
    deceptiveScarcityAllowed: false,
    sellerPrivateDataExposed: false,
    internalProfitLogicExposed: false
  },
  {
    id: "buyer-sequence-003",
    dealId: "deal-005",
    buyerId: "buyer-004",
    accelerationRecordId: "buyer-accel-003",
    firstBuyerNotice: "Blocked draft: exposes seller private data and internal spread logic.",
    buyerDetailFollowUp: "Blocked draft: unsafe internal details must be removed before any owner review.",
    pofRequest: "Draft: request POF after sanitizer and compliance clear.",
    viewingAccessCoordination: "Blocked until buyer-visible gate clears.",
    offerIntentFollowUp: "Blocked until safety review clears.",
    deadlineReminder: "Blocked draft: misleading urgency removed.",
    safetyStatus: "blocked",
    blockedReasons: ["seller_private_data", "internal_profit_logic", "deceptive_scarcity"],
    draftOnly: true,
    liveSendAllowed: false,
    bulkBlastAllowed: false,
    deceptiveScarcityAllowed: false,
    sellerPrivateDataExposed: false,
    internalProfitLogicExposed: false
  }
];

export const buyerResponseRoutes: BuyerResponseRoute[] = [
  { id: "buyer-route-001", dealId: "deal-001", buyerId: "buyer-001", responseType: "buyer_interested", routedStatus: "owner_review_queue", ownerActionRequired: true, recommendedNextStep: "Review buyer interest and verified POF before access coordination.", pofGap: false, accessRequested: false, offerIntentRecorded: true, draftOnly: true, contractExecutionAllowed: false },
  { id: "buyer-route-002", dealId: "deal-003", buyerId: "buyer-001", responseType: "needs_pof", routedStatus: "pof_request_queue", ownerActionRequired: true, recommendedNextStep: "Send approved POF request draft only after V13/V5 gates.", pofGap: true, accessRequested: false, offerIntentRecorded: false, draftOnly: true, contractExecutionAllowed: false },
  { id: "buyer-route-003", dealId: "deal-001", buyerId: "buyer-002", responseType: "wants_showing_access", routedStatus: "access_review_queue", ownerActionRequired: true, recommendedNextStep: "Coordinate access placeholder after owner review.", pofGap: false, accessRequested: true, offerIntentRecorded: false, draftOnly: true, contractExecutionAllowed: false },
  { id: "buyer-route-004", dealId: "deal-005", buyerId: "buyer-004", responseType: "asks_for_repair_details", routedStatus: "blocked_compliance_queue", ownerActionRequired: true, recommendedNextStep: "Resolve buyer visibility and compliance blocks before any draft response.", pofGap: false, accessRequested: false, offerIntentRecorded: false, draftOnly: true, contractExecutionAllowed: false }
];

export const buyerVelocityProfiles: BuyerVelocityProfile[] = [
  { id: "buyer-velocity-001", buyerId: "buyer-001", responseSpeed: 95, pofStrength: 96, closeHistory: 93, priceFit: 91, marketFit: 94, reliability: 94, previousIntentQuality: 90, velocityScore: 94, recommendedUse: "fast_close_priority", draftOnly: true },
  { id: "buyer-velocity-002", buyerId: "buyer-002", responseSpeed: 90, pofStrength: 93, closeHistory: 88, priceFit: 85, marketFit: 90, reliability: 91, previousIntentQuality: 86, velocityScore: 89, recommendedUse: "fast_close_priority", draftOnly: true },
  { id: "buyer-velocity-003", buyerId: "buyer-004", responseSpeed: 82, pofStrength: 92, closeHistory: 86, priceFit: 84, marketFit: 90, reliability: 88, previousIntentQuality: 82, velocityScore: 87, recommendedUse: "targeted_follow_up", draftOnly: true },
  { id: "buyer-velocity-004", buyerId: "buyer-007", responseSpeed: 72, pofStrength: 30, closeHistory: 70, priceFit: 66, marketFit: 72, reliability: 74, previousIntentQuality: 66, velocityScore: 65, recommendedUse: "pof_or_fit_review", draftOnly: true }
];

export const outcomeLearningRecords: OutcomeLearningRecord[] = [
  { id: "learning-001", dealId: "deal-001", leadSource: "absentee owner", market: "75216", sellerType: "tired_landlord", buyerType: "fast_close_verified_pof", offerStrategy: "cash-fast", followUpType: "seller_call_then_offer_explanation", conversionResult: "contract_ready", projectedAssignmentFee: 24000, verifiedAssignmentFee: 24000, timeToContractReadyDays: 5, blockers: [], lostReason: "", confidenceScore: 93, sourceEvidenceIds: ["evidence-001", "fee-001", "buyer-accel-001"], sourceRecordsPresent: true, evidenceStatus: "supported", unsupportedRevenueClaim: false, unsupportedRoiClaim: false },
  { id: "learning-002", dealId: "deal-003", leadSource: "high equity", market: "75224", sellerType: "timeline_driven", buyerType: "verified_pof_value_add", offerStrategy: "flexible-close", followUpType: "pof_request_then_detail_follow_up", conversionResult: "contract_ready", projectedAssignmentFee: 18000, verifiedAssignmentFee: 0, timeToContractReadyDays: 7, blockers: ["buyer_pof_gap"], lostReason: "", confidenceScore: 82, sourceEvidenceIds: ["evidence-002", "buyer-accel-002"], sourceRecordsPresent: true, evidenceStatus: "supported", unsupportedRevenueClaim: false, unsupportedRoiClaim: false },
  { id: "learning-003", dealId: "deal-005", leadSource: "probate", market: "75216", sellerType: "inherited_property", buyerType: "duplex_buyer", offerStrategy: "as-is", followUpType: "slow_document_follow_up", conversionResult: "blocked", projectedAssignmentFee: 15000, verifiedAssignmentFee: 0, timeToContractReadyDays: null, blockers: ["seller_document_missing", "compliance_review_missing"], lostReason: "", confidenceScore: 64, sourceEvidenceIds: ["evidence-003", "buyer-accel-003"], sourceRecordsPresent: true, evidenceStatus: "supported", unsupportedRevenueClaim: false, unsupportedRoiClaim: false },
  { id: "learning-004", dealId: "deal-006", leadSource: "driving for dollars", market: "75211", sellerType: "price_focused", buyerType: "repair_heavy_single_family", offerStrategy: "investor-grade", followUpType: "stale_follow_up", conversionResult: "lost", projectedAssignmentFee: 7000, verifiedAssignmentFee: 0, timeToContractReadyDays: null, blockers: ["stale_follow_up", "weak_buyer_margin"], lostReason: "seller_price_misalignment", confidenceScore: 58, sourceEvidenceIds: ["negotiation-004"], sourceRecordsPresent: true, evidenceStatus: "supported", unsupportedRevenueClaim: false, unsupportedRoiClaim: false },
  { id: "learning-005", dealId: "deal-002", leadSource: "tax delinquent", market: "76104", sellerType: "urgent_timeline", buyerType: "fast_small_deal_buyer", offerStrategy: "cash-fast", followUpType: "hot_lead_call_script", conversionResult: "assigned", projectedAssignmentFee: 13000, verifiedAssignmentFee: 13000, timeToContractReadyDays: 4, blockers: [], lostReason: "", confidenceScore: 89, sourceEvidenceIds: ["fee-002", "contract-ready-002"], sourceRecordsPresent: true, evidenceStatus: "supported", unsupportedRevenueClaim: false, unsupportedRoiClaim: false },
  { id: "learning-006", dealId: "deal-007", leadSource: "vacant", market: "75217", sellerType: "low_contactability", buyerType: "unverified_pof", offerStrategy: "aggressive_offer", followUpType: "generic_sms_draft", conversionResult: "stalled", projectedAssignmentFee: 11000, verifiedAssignmentFee: 0, timeToContractReadyDays: null, blockers: ["buyer_pof_gap", "low_contactability"], lostReason: "contact_consistency_missing", confidenceScore: 46, sourceEvidenceIds: [], sourceRecordsPresent: false, evidenceStatus: "blocked", unsupportedRevenueClaim: false, unsupportedRoiClaim: false }
];

export const optimizationRecommendations: OptimizationRecommendation[] = [
  { id: "optimization-rec-001", recommendationType: "focus_market", target: "75216 absentee/high-equity leads", recommendation: "Prioritize 75216 absentee-owner and high-equity leads before expanding colder lists.", explanation: "learning-001 and learning-003 show 75216 produces strong source-backed 10K+ opportunities with visible blockers.", sourceRecordIds: ["learning-001", "learning-003"], confidenceScore: 87, impactScore: 91, status: "draft_recommendation", ownerReviewStatus: "pending_review", guaranteedRevenueClaimAllowed: false, unsupportedRoiClaimAllowed: false },
  { id: "optimization-rec-002", recommendationType: "buyer_segment_to_target", target: "fast_close_verified_pof", recommendation: "Route controlled distribution prep first to verified POF buyers with strong response speed.", explanation: "Buyer acceleration and learning records show fast-close verified POF buyers remove POF blockers and shorten readiness time.", sourceRecordIds: ["learning-001", "learning-002", "buyer-velocity-001"], confidenceScore: 85, impactScore: 88, status: "draft_recommendation", ownerReviewStatus: "pending_review", guaranteedRevenueClaimAllowed: false, unsupportedRoiClaimAllowed: false },
  { id: "optimization-rec-003", recommendationType: "script_improvement", target: "generic_sms_draft", recommendation: "Replace generic SMS-style follow-up with property-specific owner-reviewed call notes and offer-basis explanation.", explanation: "learning-004 and learning-006 show stale or generic follow-up correlates with low contact consistency and lost/stalled outcomes.", sourceRecordIds: ["learning-004", "learning-006"], confidenceScore: 78, impactScore: 76, status: "draft_recommendation", ownerReviewStatus: "pending_review", guaranteedRevenueClaimAllowed: false, unsupportedRoiClaimAllowed: false },
  { id: "optimization-rec-004", recommendationType: "deal_type_to_avoid", target: "weak-margin aggressive offers", recommendation: "Avoid aggressive offers when buyer margin strength is below threshold and seller price alignment is weak.", explanation: "Weak margin and missing POF stalled before contract-ready; aggressive positioning should be downweighted.", sourceRecordIds: ["learning-004", "learning-006"], confidenceScore: 74, impactScore: 72, status: "draft_recommendation", ownerReviewStatus: "pending_review", guaranteedRevenueClaimAllowed: false, unsupportedRoiClaimAllowed: false }
];

export const agentPerformanceScores: AgentPerformanceScore[] = [
  { id: "agent-performance-001", divisionName: "Lead Intelligence Division", agentGroup: "List Stacking + Contactability Agents", qualityScore: 88, conversionScore: 82, accuracyScore: 86, effectivenessScore: 84, complianceBlockRate: 12, followUpScore: 80, recommendationAccuracy: 84, overallScore: 84, explanation: "Strong source quality when contactability and stacking evidence are present.", sourceRecordIds: ["learning-001", "learning-002", "learning-005"] },
  { id: "agent-performance-002", divisionName: "Seller Acquisition Division", agentGroup: "Motivation Discovery + Offer Explanation Agents", qualityScore: 84, conversionScore: 78, accuracyScore: 82, effectivenessScore: 80, complianceBlockRate: 10, followUpScore: 76, recommendationAccuracy: 81, overallScore: 81, explanation: "Offer explanation performs well; stale follow-up needs tighter priority.", sourceRecordIds: ["learning-001", "learning-004", "learning-006"] },
  { id: "agent-performance-003", divisionName: "Deal Underwriting Division", agentGroup: "ARV + Repair + MAO Agents", qualityScore: 91, conversionScore: 84, accuracyScore: 90, effectivenessScore: 86, complianceBlockRate: 8, followUpScore: 75, recommendationAccuracy: 88, overallScore: 87, explanation: "Underwriting accuracy is strongest when evidence packets are complete.", sourceRecordIds: ["learning-001", "learning-002", "learning-005"] },
  { id: "agent-performance-004", divisionName: "Buyer Disposition Division", agentGroup: "Buyer Demand + Buyer Reliability Agents", qualityScore: 89, conversionScore: 86, accuracyScore: 86, effectivenessScore: 88, complianceBlockRate: 9, followUpScore: 82, recommendationAccuracy: 87, overallScore: 87, explanation: "Verified POF routing and buyer velocity improve disposition speed.", sourceRecordIds: ["learning-001", "learning-002", "buyer-velocity-001"] },
  { id: "agent-performance-005", divisionName: "Contract & Compliance Division", agentGroup: "Disclosure Guard + State Risk Agents", qualityScore: 86, conversionScore: 72, accuracyScore: 88, effectivenessScore: 78, complianceBlockRate: 18, followUpScore: 74, recommendationAccuracy: 84, overallScore: 80, explanation: "Blocks are appropriate but inherited-property documentation gaps slow conversion.", sourceRecordIds: ["learning-003", "learning-004"] }
];

export const scoringWeightChanges: ScoringWeightChange[] = [
  { id: "weight-change-001", sourceRecordId: "learning-001", weightGroup: "opportunity_score.market_demand", previousWeight: 0.18, newWeight: 0.21, reason: "Evidence-backed 10K+ conversion in high-demand 75216 segment.", explanation: "Increase is deterministic and tied to learning-001 evidence.", loggedBy: "Prime 2", ownerReviewStatus: "pending_review" },
  { id: "weight-change-002", sourceRecordId: "learning-006", weightGroup: "buyer_ranking.pof_strength", previousWeight: 0.18, newWeight: 0.22, reason: "POF gaps show repeated stalls before contract-ready.", explanation: "Buyer ranking should prioritize proof-of-funds strength before access routing.", loggedBy: "Prime 2", ownerReviewStatus: "pending_review" },
  { id: "weight-change-003", sourceRecordId: "learning-004", weightGroup: "follow_up_priority.staleness_penalty", previousWeight: 0.12, newWeight: 0.17, reason: "Stale follow-up pattern correlates with lost seller price alignment.", explanation: "Follow-up priority should escalate stale high-fit leads sooner.", loggedBy: "Prime 2", ownerReviewStatus: "pending_review" }
];

export const revenueForecastRecords: RevenueForecastRecord[] = [
  { id: "forecast-2026-05", forecastPeriod: "May 2026", projectedAssignmentFees: 81000, verifiedAssignmentFees: 37000, probabilityAdjustedRevenue: 54800, conservativeForecast: 41100, baseForecast: 54800, aggressiveForecast: 64664, dealsAtRisk: ["deal-005", "deal-006", "deal-007"], expectedCloseWindow: "2026-05-10 to 2026-05-31", confidenceLevel: "medium_high", sourceBasis: ["fee-001", "fee-002", "learning-001", "learning-002", "probability-001"], estimateLabel: "Estimate only; not guaranteed revenue.", guaranteedRevenueClaimAllowed: false, unsupportedRoiClaimAllowed: false },
  { id: "forecast-2026-06", forecastPeriod: "June 2026", projectedAssignmentFees: 62000, verifiedAssignmentFees: 0, probabilityAdjustedRevenue: 36500, conservativeForecast: 27375, baseForecast: 36500, aggressiveForecast: 43070, dealsAtRisk: ["deal-006", "deal-007"], expectedCloseWindow: "2026-06-01 to 2026-06-30", confidenceLevel: "medium", sourceBasis: ["learning-003", "learning-005", "market-scale-001"], estimateLabel: "Estimate only; not guaranteed revenue.", guaranteedRevenueClaimAllowed: false, unsupportedRoiClaimAllowed: false }
];

export const dealProbabilityRecords: DealProbabilityRecord[] = [
  { id: "probability-001", dealId: "deal-001", sellerReadiness: 92, buyerDemand: 94, underwritingConfidence: 90, complianceStatusScore: 92, titleReviewReadiness: 86, blockerSeverity: 5, buyerPofStrength: 96, communicationMomentum: 88, probabilityScore: 89, probabilityBand: "high_estimate", sourceRecordIds: ["learning-001", "title-review-001", "buyer-accel-001"], estimateOnly: true },
  { id: "probability-002", dealId: "deal-003", sellerReadiness: 84, buyerDemand: 87, underwritingConfidence: 84, complianceStatusScore: 82, titleReviewReadiness: 72, blockerSeverity: 18, buyerPofStrength: 78, communicationMomentum: 80, probabilityScore: 73, probabilityBand: "base_estimate", sourceRecordIds: ["learning-002", "buyer-accel-002"], estimateOnly: true },
  { id: "probability-003", dealId: "deal-005", sellerReadiness: 72, buyerDemand: 84, underwritingConfidence: 78, complianceStatusScore: 48, titleReviewReadiness: 42, blockerSeverity: 44, buyerPofStrength: 88, communicationMomentum: 58, probabilityScore: 54, probabilityBand: "conservative_estimate", sourceRecordIds: ["learning-003", "title-review-003"], estimateOnly: true },
  { id: "probability-004", dealId: "deal-006", sellerReadiness: 48, buyerDemand: 68, underwritingConfidence: 62, complianceStatusScore: 64, titleReviewReadiness: 38, blockerSeverity: 55, buyerPofStrength: 60, communicationMomentum: 42, probabilityScore: 42, probabilityBand: "conservative_estimate", sourceRecordIds: ["learning-004"], estimateOnly: true }
];

export const marketScalingScores: MarketScalingScore[] = [
  { id: "market-scale-001", marketZip: "75216", leadVolume: 42, hotLeadPercentage: 38, buyerDemand: 94, averageSpread: 21000, conversionRate: 28, titleComplianceFriction: 18, competitionRisk: 42, recommendedSpendLevel: "increase_selectively", scalingScore: 70, sourceRecordIds: ["learning-001", "learning-003", "buyer-demand-001"], estimateOnly: true },
  { id: "market-scale-002", marketZip: "75224", leadVolume: 24, hotLeadPercentage: 31, buyerDemand: 86, averageSpread: 18000, conversionRate: 22, titleComplianceFriction: 22, competitionRisk: 48, recommendedSpendLevel: "hold_or_test", scalingScore: 62, sourceRecordIds: ["learning-002", "buyer-accel-002"], estimateOnly: true },
  { id: "market-scale-003", marketZip: "75217", leadVolume: 18, hotLeadPercentage: 14, buyerDemand: 70, averageSpread: 11000, conversionRate: 11, titleComplianceFriction: 35, competitionRisk: 54, recommendedSpendLevel: "avoid_or_research", scalingScore: 45, sourceRecordIds: ["learning-006"], estimateOnly: true }
];

export const leadSpendPlans: LeadSpendPlan[] = [
  { id: "lead-spend-001", targetZipCodes: ["75216", "75224"], leadTypes: ["absentee owner", "high equity", "tax delinquent"], maxMonthlySpend: 1800, expectedDealCount: 1.4, expectedAssignmentFeeLow: 13000, expectedAssignmentFeeHigh: 24000, breakEvenAssignmentTarget: 10000, evidenceBasis: ["market-scale-001", "learning-001", "learning-002"], recommendationStatus: "owner_review_required", unsupportedSpendRecommended: false, estimateOnly: true, ownerReviewStatus: "pending_review" },
  { id: "lead-spend-002", targetZipCodes: ["75217"], leadTypes: ["vacant"], maxMonthlySpend: 0, expectedDealCount: 0.2, expectedAssignmentFeeLow: 0, expectedAssignmentFeeHigh: 11000, breakEvenAssignmentTarget: 10000, evidenceBasis: ["market-scale-003", "learning-006"], recommendationStatus: "avoid_or_research", unsupportedSpendRecommended: false, estimateOnly: true, ownerReviewStatus: "pending_review" }
];

export const operatorModeSettings: OperatorModeSetting[] = [
  { id: "operator-mode-default", currentMode: "near_autonomous", defaultMode: "near_autonomous", semiAutonomousEnabled: false, ownerEnabled: false, maxAutonomyLevel: 4, level5Disabled: true, highRiskRequiresApproval: true, liveActionsRequireGates: true, contractExecutionAllowed: false, titleSubmissionAllowed: false, bulkCampaignsAllowed: false, paymentHandlingAllowed: false },
  { id: "operator-mode-ready", currentMode: "semi_autonomous", defaultMode: "near_autonomous", semiAutonomousEnabled: true, ownerEnabled: true, maxAutonomyLevel: 4, level5Disabled: true, highRiskRequiresApproval: true, liveActionsRequireGates: true, contractExecutionAllowed: false, titleSubmissionAllowed: false, bulkCampaignsAllowed: false, paymentHandlingAllowed: false }
];

export const semiAutonomousCommandLoopRuns: SemiAutonomousCommandLoopRun[] = [
  { id: "operator-loop-001", modeSettingId: "operator-mode-ready", cycleStatus: "prepared_waiting_approvals", scanSummary: { hotDeals: 5, buyerResponses: 4, forecastRisk: 26200 }, scoreSummary: { topDeal: "deal-001", topProbability: 89, trustScore: 82 }, routeSummary: { approvals: 9, exceptions: 4, dailyReport: "operator-report-001" }, preparedItems: [{ type: "buyer_distribution", source: "buyer-accel-001" }, { type: "title_review_packet", source: "title-review-001" }, { type: "forecast_spend_recommendation", source: "lead-spend-001" }], gateChecks: [{ gate: "owner_approval_required", passed: true }, { gate: "level_5_disabled", passed: true }, { gate: "contract_execution_blocked", passed: true }, { gate: "title_submission_blocked", passed: true }], escalations: ["operator-exception-001", "operator-exception-002"], approvalsWaiting: ["approval-001", "approval-002", "approval-006"], outcomesLogged: ["learning-001", "forecast-2026-05"], optimizedRecords: ["optimization-rec-001", "weight-change-001"], highRiskActionsExecuted: false, contractsExecuted: false, titleSubmitted: false, bulkCampaignsSent: false, portalPublishWithoutApproval: false }
];

export const ownerApprovalItems: OwnerApprovalItem[] = [
  { id: "approval-001", approvalType: "seller_follow_up_live_send", sourceRecordType: "communication_draft", sourceRecordId: "comm-draft-001", title: "Approve seller follow-up live send", riskLevel: "medium", approvalStatus: "pending_owner", ownerRequired: true, readyForApproval: true, blockedReasons: [], actionSummary: "One seller follow-up draft passed safety and dry-run; approval still required.", highRiskAction: true, executed: false },
  { id: "approval-002", approvalType: "buyer_response_live_send", sourceRecordType: "auto_execution_attempt", sourceRecordId: "auto-attempt-002", title: "Approve buyer response mock/live gate", riskLevel: "medium", approvalStatus: "pending_owner", ownerRequired: true, readyForApproval: true, blockedReasons: [], actionSummary: "Single buyer response remains one-recipient and V5/V13 gated.", highRiskAction: true, executed: false },
  { id: "approval-003", approvalType: "offer_packet_prep", sourceRecordType: "offer_packet", sourceRecordId: "packet-001", title: "Approve offer packet prep", riskLevel: "medium", approvalStatus: "pending_owner", ownerRequired: true, readyForApproval: true, blockedReasons: [], actionSummary: "Underwriting and compliance gates are clear for draft packet prep.", highRiskAction: false, executed: false },
  { id: "approval-004", approvalType: "contract_ready_status", sourceRecordType: "contract_ready_state", sourceRecordId: "contract-ready-001", title: "Approve contract-ready state", riskLevel: "high", approvalStatus: "pending_owner", ownerRequired: true, readyForApproval: true, blockedReasons: [], actionSummary: "Marks external drafting readiness only; no contract is generated.", highRiskAction: true, executed: false },
  { id: "approval-005", approvalType: "title_review_packet", sourceRecordType: "review_packet", sourceRecordId: "review-packet-001", title: "Approve title review packet prep", riskLevel: "high", approvalStatus: "pending_owner", ownerRequired: true, readyForApproval: true, blockedReasons: [], actionSummary: "Draft review packet only; no title submission or email send.", highRiskAction: true, executed: false },
  { id: "approval-006", approvalType: "buyer_distribution", sourceRecordType: "buyer_acceleration", sourceRecordId: "buyer-accel-001", title: "Approve controlled buyer distribution", riskLevel: "medium", approvalStatus: "pending_owner", ownerRequired: true, readyForApproval: true, blockedReasons: [], actionSummary: "One buyer, sanitized sheet, no blast, V5/V13 gates present.", highRiskAction: true, executed: false },
  { id: "approval-007", approvalType: "portal_visibility", sourceRecordType: "buyer_deal_publication", sourceRecordId: "publication-001", title: "Approve portal visibility", riskLevel: "medium", approvalStatus: "pending_owner", ownerRequired: true, readyForApproval: false, blockedReasons: ["final_owner_visibility_review_missing"], actionSummary: "Portal publish remains blocked until explicit owner visibility approval.", highRiskAction: true, executed: false },
  { id: "approval-008", approvalType: "forecast_spend_recommendation", sourceRecordType: "lead_spend_plan", sourceRecordId: "lead-spend-001", title: "Approve lead spend estimate", riskLevel: "medium", approvalStatus: "pending_owner", ownerRequired: true, readyForApproval: true, blockedReasons: [], actionSummary: "Spend plan is evidence-backed and estimate-labeled.", highRiskAction: false, executed: false },
  { id: "approval-009", approvalType: "automation_rule_activation", sourceRecordType: "auto_execution_rule", sourceRecordId: "auto-rule-buyer-response-send", title: "Approve automation rule activation", riskLevel: "high", approvalStatus: "pending_owner", ownerRequired: true, readyForApproval: true, blockedReasons: [], actionSummary: "Level 4 remains owner-approved and one-recipient only.", highRiskAction: true, executed: false }
];

export const operatorExceptionRecords: OperatorExceptionRecord[] = [
  { id: "operator-exception-001", exceptionType: "high_profit_potential", severity: "critical", sourceRecordType: "deal", sourceRecordId: "deal-001", reason: "High probability 10K+ spread with buyer demand and title readiness.", recommendedAction: "Review approvals for buyer distribution and title review packet.", ownerActionRequired: true, status: "open" },
  { id: "operator-exception-002", exceptionType: "high_compliance_risk", severity: "critical", sourceRecordType: "deal", sourceRecordId: "deal-005", reason: "Inherited-property documentation and compliance blockers remain unresolved.", recommendedAction: "Resolve compliance blocker before any portal or assignment readiness action.", ownerActionRequired: true, status: "open" },
  { id: "operator-exception-003", exceptionType: "buyer_ready_to_offer", severity: "high", sourceRecordType: "buyer_response_route", sourceRecordId: "buyer-route-001", reason: "Buyer interest is recorded and POF is verified.", recommendedAction: "Review buyer intent and access coordination queue.", ownerActionRequired: true, status: "open" },
  { id: "operator-exception-004", exceptionType: "forecast_risk", severity: "medium", sourceRecordType: "revenue_forecast", sourceRecordId: "forecast-2026-05", reason: "Revenue at risk remains tied to blocked deals and lower probability records.", recommendedAction: "Clear POF and compliance blockers before increasing spend.", ownerActionRequired: true, status: "open" }
];

export const autonomousDailyOperatingReports: AutonomousDailyOperatingReport[] = [
  { id: "operator-report-001", reportDate: "2026-05-04", generatedBy: "Prime 2", whatSystemDid: ["Scanned hot deals, buyer velocity, forecast risk, and approval queues.", "Updated internal readiness, optimization, and forecast summaries."], whatPrepared: ["Buyer distribution approval queue", "Title review packet approval queue", "Lead spend estimate review"], whatBlocked: ["Portal publishing without owner approval", "Contract execution", "Title submission", "Bulk buyer campaign"], needsOwnerApproval: ["approval-001", "approval-004", "approval-006", "approval-008"], topMoneyActions: ["Review deal-001 controlled buyer distribution", "Resolve deal-003 POF gap", "Approve 75216 lead spend estimate", "Review verified 10K+ evidence records", "Clear title review packet for deal-001"], topRiskActions: ["Resolve deal-005 inherited-property compliance blocker", "Review portal visibility approvals", "Inspect automation rule activation", "Clear title/review missing items", "Keep Level 5 disabled"], projectedAssignmentFeeMovement: 12500, recommendedFocusToday: ["Protect deal-001 spread and buyer margin", "Clear approval queue items with no blocked reasons", "Do not increase spend until forecast blockers are reviewed"], draftOnly: true, highRiskActionsExecuted: false }
];

export const systemTrustScores: SystemTrustScore[] = [
  { id: "trust-001", automationSuccessRate: 86, blockedUnsafeActions: 9, approvalQueueAgeHours: 6, staleTasks: 2, scoringConfidence: 84, forecastConfidence: 78, buyerResponseVelocity: 88, sellerConversionVelocity: 76, overallTrustScore: 82, trustStatus: "strong_guarded", sourceRecordIds: ["operator-loop-001", "auto-audit-003", "forecast-2026-05"] }
];

export const approvalUxReviews: ApprovalUxReview[] = [
  { id: "approval-ux-001", ownerApprovalItemId: "approval-006", approvalType: "buyer_distribution", sourceRecordType: "buyer_acceleration", sourceRecordId: "buyer-accel-001", contextSummary: "One buyer, sanitized deal sheet, verified POF, no bulk blast.", riskSummary: "Live communication remains blocked until V5/V13 gates and owner approval.", gateSummary: [{ gate: "sanitized_deal_sheet", passed: true }, { gate: "bulk_send_blocked", passed: true }, { gate: "owner_approval_required", passed: true }], confirmationPrompt: "Approve preparation only; this does not send buyer communication.", recommendedDecision: "review_ready", approvalStatus: "pending_owner", ownerActionRequired: true, approvalIsNotExecution: true, blockedReasons: [] },
  { id: "approval-ux-002", ownerApprovalItemId: "approval-007", approvalType: "portal_visibility", sourceRecordType: "buyer_deal_publication", sourceRecordId: "publication-001", contextSummary: "Portal visibility needs explicit owner review before any external exposure.", riskSummary: "Publishing is blocked until owner visibility approval is recorded.", gateSummary: [{ gate: "portal_visibility_enabled", passed: false }, { gate: "seller_private_data_hidden", passed: true }], confirmationPrompt: "Review sanitizer and blocked reasons before enabling visibility.", recommendedDecision: "hold", approvalStatus: "blocked", ownerActionRequired: true, approvalIsNotExecution: true, blockedReasons: ["final_owner_visibility_review_missing"] },
  { id: "approval-ux-003", ownerApprovalItemId: "approval-008", approvalType: "forecast_spend_recommendation", sourceRecordType: "lead_spend_plan", sourceRecordId: "lead-spend-001", contextSummary: "Lead spend estimate is evidence-backed and labeled as an estimate.", riskSummary: "No guaranteed profit or unsupported ROI language is present.", gateSummary: [{ gate: "estimate_label_present", passed: true }, { gate: "source_basis_present", passed: true }], confirmationPrompt: "Approve the spend recommendation for operator planning only.", recommendedDecision: "review_ready", approvalStatus: "pending_owner", ownerActionRequired: true, approvalIsNotExecution: true, blockedReasons: [] }
];

export const auditExportPackets: AuditExportPacket[] = [
  { id: "audit-export-001", exportType: "deal_evidence_audit", sourceRecordType: "deal_evidence_packet", sourceRecordId: "evidence-001", requestedBy: "Owner", exportScope: "internal_owner_review", sanitizedPayload: { deal_id: "deal-001", city: "Dallas", state: "TX", projected_assignment_fee: 17000, evidence_ids: ["evidence-001", "fee-001"], compliance_summary: "Owner review required before external use." }, includedRecordIds: ["evidence-001", "fee-001", "contract-001"], omittedSensitiveFields: ["seller_name", "seller_phone"], internalFieldsRemoved: ["assignment_fee_logic", "lead_source", "seller_contract_price"], exportStatus: "ready_for_owner_review", ownerApprovalStatus: "pending_owner", safeForExternalShare: false, containsRawPrivateData: false, legalAdviceIncluded: false, secretsIncluded: false, packetHash: "audit-hash-001", retentionNotes: "Internal owner audit packet only; sanitize before any external use.", blockedReasons: [] },
  { id: "audit-export-002", exportType: "approval_audit", sourceRecordType: "owner_approval_item", sourceRecordId: "approval-006", requestedBy: "Owner", exportScope: "internal_owner_review", sanitizedPayload: { approval_id: "approval-006", action: "controlled buyer distribution review", risk_summary: "One-recipient gate present; no bulk blast." }, includedRecordIds: ["approval-006", "buyer-accel-001", "auto-attempt-002"], omittedSensitiveFields: ["buyer_name", "buyer_email"], internalFieldsRemoved: ["internal_notes"], exportStatus: "ready_for_owner_review", ownerApprovalStatus: "pending_owner", safeForExternalShare: false, containsRawPrivateData: false, legalAdviceIncluded: false, secretsIncluded: false, packetHash: "audit-hash-002", retentionNotes: "Approval history packet uses redacted recipient placeholders.", blockedReasons: [] }
];

export const evidenceAttachmentRecords: EvidenceAttachmentRecord[] = [
  { id: "attachment-001", sourceRecordType: "deal_evidence_packet", sourceRecordId: "evidence-001", dealId: "deal-001", evidencePacketId: "evidence-001", attachmentType: "underwriting_snapshot", filenamePlaceholder: "underwriting-snapshot-deal-001.pdf", storageMode: "local_placeholder", sanitizedMetadata: { pages: 3, redacted: true, source: "underwriting" }, containsSensitiveData: false, sourceLinkageVerified: true, sourceVerified: true, safeToExport: true, uploadStatus: "placeholder_only", operatorNotes: "Metadata only; no file bytes committed.", rawFilePathCommitted: false, blockedReasons: [] },
  { id: "attachment-002", sourceRecordType: "seller_interaction", sourceRecordId: "seller-interaction-001", dealId: "deal-001", evidencePacketId: "evidence-001", attachmentType: "seller_interaction_proof", filenamePlaceholder: "seller-call-notes-redacted.txt", storageMode: "local_placeholder", sanitizedMetadata: { redacted: true, contactDataRemoved: true }, containsSensitiveData: true, sourceLinkageVerified: true, sourceVerified: true, safeToExport: false, uploadStatus: "placeholder_only", operatorNotes: "Sensitive seller details stay internal unless separately sanitized.", rawFilePathCommitted: false, blockedReasons: [] },
  { id: "attachment-003", sourceRecordType: "buyer_interest", sourceRecordId: "interest-001", dealId: "deal-001", evidencePacketId: "evidence-001", attachmentType: "pof_placeholder", filenamePlaceholder: "pof-status-placeholder.pdf", storageMode: "local_placeholder", sanitizedMetadata: { pofStatus: "verified", documentBytesStored: false }, containsSensitiveData: true, sourceLinkageVerified: true, sourceVerified: true, safeToExport: false, uploadStatus: "placeholder_only", operatorNotes: "POF proof status only; no financial document stored in repo.", rawFilePathCommitted: false, blockedReasons: [] }
];

export const backupExportRecords: BackupExportRecord[] = [
  { id: "backup-001", backupType: "metadata_snapshot", backupScope: "operator_local", storageTarget: "local_export_placeholder", includedTables: ["deals", "deal_evidence_packets", "assignment_fee_attributions", "owner_approval_items"], excludedFields: ["seller_name", "seller_phone", "buyer_email", "buyer_phone", "api_key", "provider_secret", "internal_notes"], safeMetadata: { includedTableCount: 4, containsRawPrivateData: false, safeMetadataOnly: true }, backupStatus: "prepared", containsRawPrivateData: false, safeMetadataOnly: true, filePathPlaceholder: "exports/backup-001.metadata.json", restoreTestStatus: "not_tested", ownerApprovalStatus: "pending_owner", blockedReasons: [] },
  { id: "backup-002", backupType: "audit_index", backupScope: "audit_records_only", storageTarget: "local_export_placeholder", includedTables: ["audit_export_packets", "auto_execution_audit_records", "communication_send_attempts"], excludedFields: ["recipient", "seller_phone", "buyer_email", "provider_secret"], safeMetadata: { includedTableCount: 3, containsRawPrivateData: false, safeMetadataOnly: true }, backupStatus: "prepared", containsRawPrivateData: false, safeMetadataOnly: true, filePathPlaceholder: "exports/backup-002.metadata.json", restoreTestStatus: "not_tested", ownerApprovalStatus: "pending_owner", blockedReasons: [] }
];

export const providerSandboxReadinessChecks: ProviderSandboxReadinessCheck[] = [
  { id: "provider-ready-001", providerType: "email", providerName: "Email adapter sandbox", mode: "mock", sandboxReady: false, secretsConfigured: false, liveFlagEnabled: false, safetyCheckRequired: true, dryRunRequired: true, ownerApprovalRequired: true, idempotencyRequired: true, auditTrailRequired: true, providerCallsAllowed: false, readinessStatus: "blocked", blockedReasons: ["sandbox_ready_required", "sandbox_secrets_missing"], lastCheckedNotes: "Default remains mock until sandbox credentials are configured outside the repo." },
  { id: "provider-ready-002", providerType: "sms", providerName: "SMS adapter sandbox", mode: "mock", sandboxReady: false, secretsConfigured: false, liveFlagEnabled: false, safetyCheckRequired: true, dryRunRequired: true, ownerApprovalRequired: true, idempotencyRequired: true, auditTrailRequired: true, providerCallsAllowed: false, readinessStatus: "blocked", blockedReasons: ["sandbox_ready_required", "sandbox_secrets_missing"], lastCheckedNotes: "SMS remains blocked; opt-out and sandbox provider checks required." },
  { id: "provider-ready-003", providerType: "title_review", providerName: "Title coordination placeholder", mode: "mock", sandboxReady: false, secretsConfigured: false, liveFlagEnabled: false, safetyCheckRequired: true, dryRunRequired: true, ownerApprovalRequired: true, idempotencyRequired: true, auditTrailRequired: true, providerCallsAllowed: false, readinessStatus: "blocked", blockedReasons: ["sandbox_ready_required", "sandbox_secrets_missing"], lastCheckedNotes: "No title-company submission integration exists in V18." }
];

export const providerRegistries: ProviderRegistry[] = [
  { id: "provider-openai-mock", providerName: "OpenAI controlled gateway", providerType: "openai", providerMode: "mock", enabled: true, sandboxEnabled: false, liveEnabled: false, credentialReferenceMasked: "OPE***KEY", credentialPresent: false, credentialSource: "env", readinessStatus: "ready", blockedReason: "", ownerApprovalRequired: true, notes: "Mock mode only; env reference is metadata and no provider call is made.", rawSecretValueStored: false, liveNetworkCallAllowed: false },
  { id: "provider-email-sandbox", providerName: "Email sandbox adapter", providerType: "email", providerMode: "sandbox", enabled: true, sandboxEnabled: true, liveEnabled: false, credentialReferenceMasked: "EMA***KEY", credentialPresent: false, credentialSource: "env", readinessStatus: "missing_credentials", blockedReason: "credential_env_value_missing", ownerApprovalRequired: true, notes: "Sandbox use requires env-only credential presence and communication gates.", rawSecretValueStored: false, liveNetworkCallAllowed: false },
  { id: "provider-sms-live", providerName: "SMS provider live placeholder", providerType: "sms", providerMode: "live", enabled: true, sandboxEnabled: true, liveEnabled: false, credentialReferenceMasked: "SMS***KEY", credentialPresent: false, credentialSource: "env", readinessStatus: "blocked", blockedReason: "live_flag_required, owner_approval_required_for_live", ownerApprovalRequired: true, notes: "Live SMS remains unavailable unless explicit live flag, owner approval, readiness, and audit gates pass.", rawSecretValueStored: false, liveNetworkCallAllowed: false },
  { id: "provider-storage-mock", providerName: "Storage export placeholder", providerType: "storage", providerMode: "mock", enabled: true, sandboxEnabled: false, liveEnabled: false, credentialReferenceMasked: "STO***KEY", credentialPresent: false, credentialSource: "env", readinessStatus: "ready", blockedReason: "", ownerApprovalRequired: true, notes: "Metadata-only storage readiness; no file provider call path exists in V22.", rawSecretValueStored: false, liveNetworkCallAllowed: false }
];

export const providerAttemptAudits: ProviderAttemptAudit[] = [
  { id: "provider-attempt-seed-001", providerId: "provider-email-sandbox", providerName: "Email sandbox adapter", providerType: "email", sourceDomain: "communications", actionType: "seller_follow_up_dry_run", mode: "sandbox", attemptStatus: "blocked", blockedReason: "credential_env_value_missing", idempotencyKey: "seed:provider-attempt:email:001", requestMetadataHash: "seed-email-metadata-hash", providerCalled: false, realNetworkCallMade: false },
  { id: "provider-attempt-seed-002", providerId: "provider-openai-mock", providerName: "OpenAI controlled gateway", providerType: "openai", sourceDomain: "ai_gateway", actionType: "deal_summary_template", mode: "mock", attemptStatus: "mock_success", blockedReason: "", idempotencyKey: "seed:provider-attempt:openai:001", requestMetadataHash: "seed-openai-metadata-hash", providerCalled: false, realNetworkCallMade: false }
];

export const providerWebhookEvents: ProviderWebhookEvent[] = [
  { id: "provider-webhook-seed-001", providerType: "crm", eventType: "mock_lead_status", receivedAt: "2026-05-04T14:00:00Z", mode: "mock", signaturePresent: false, signatureValid: false, normalizedEventStatus: "review_queued", reviewTaskCreated: true, dealMutationAllowed: false, dealMutated: false, rawPayloadStored: false, blockedReason: "" },
  { id: "provider-webhook-seed-002", providerType: "sms", eventType: "live_like_delivery_status", receivedAt: "2026-05-04T14:05:00Z", mode: "live", signaturePresent: false, signatureValid: false, normalizedEventStatus: "blocked", reviewTaskCreated: false, dealMutationAllowed: false, dealMutated: false, rawPayloadStored: false, blockedReason: "unsigned_live_like_webhook_rejected" }
];

export const environmentReadinessChecks: EnvironmentReadinessCheck[] = [
  { id: "env-ready-001", category: "auth", checkName: "operator auth configured", required: true, passed: false, status: "missing", detail: "Production auth is not configured; private local mode remains the only safe mode.", remediation: "Add authenticated owner-only access before any production exposure.", blockedReasons: ["operator_auth_missing"], preventsProduction: true },
  { id: "env-ready-002", category: "env", checkName: "production environment variables configured", required: true, passed: false, status: "missing", detail: "Required production environment variables are not confirmed.", remediation: "Define production env values outside git and verify startup checks.", blockedReasons: ["production_env_missing"], preventsProduction: true },
  { id: "env-ready-003", category: "secrets", checkName: "provider secrets configured outside repo", required: true, passed: false, status: "missing", detail: "No provider secrets are committed or configured for production.", remediation: "Use a secret manager or deployment environment variables; never commit secrets.", blockedReasons: ["provider_secrets_missing"], preventsProduction: true },
  { id: "env-ready-004", category: "database", checkName: "postgres ready migration path", required: true, passed: true, status: "passed", detail: "SQLAlchemy/Alembic migration path remains Postgres-ready.", remediation: "", blockedReasons: [], preventsProduction: false },
  { id: "env-ready-005", category: "private_mode", checkName: "private operator mode preserved", required: true, passed: true, status: "passed", detail: "No public signup or client portal exposure is registered.", remediation: "", blockedReasons: [], preventsProduction: false }
];

export const deploymentHardeningChecks: DeploymentHardeningCheck[] = [
  { id: "hardening-001", area: "auth", checkName: "public exposure auth checklist", required: true, passed: false, status: "blocked", detail: "Do not expose the app publicly until owner auth, session policy, and HTTPS are configured.", remediation: "Add owner-only authentication and deploy behind HTTPS before public networking.", ownerActionRequired: true, blockedReasons: ["auth_required_before_public_exposure"] },
  { id: "hardening-002", area: "secrets", checkName: "secret scanning and env isolation", required: true, passed: false, status: "open", detail: "Secrets must live outside source control and pass pre-deploy scanning.", remediation: "Enable secret scanning and document provider env names without values.", ownerActionRequired: true, blockedReasons: ["secret_scanning_not_confirmed"] },
  { id: "hardening-003", area: "audit", checkName: "audit export redaction review", required: true, passed: true, status: "passed", detail: "Audit export packets remove sensitive and internal fields by default.", remediation: "", ownerActionRequired: false, blockedReasons: [] },
  { id: "hardening-004", area: "providers", checkName: "sandbox provider only", required: true, passed: true, status: "passed", detail: "Provider checks default blocked and never call live providers in V18.", remediation: "", ownerActionRequired: false, blockedReasons: [] },
  { id: "hardening-005", area: "backup", checkName: "backup metadata safe mode", required: true, passed: true, status: "passed", detail: "Backup records expose safe metadata only and exclude private fields.", remediation: "", ownerActionRequired: false, blockedReasons: [] }
];

export const assignmentReadinessRecords: AssignmentReadinessRecord[] = [
  { id: "assignment-ready-001", contractControlId: "contract-001", dealId: "deal-001", buyerId: "buyer-001", buyerMatchId: "match-001", buyerInterestId: "interest-001", readinessStatus: "assignment_ready", assignmentReady: true, blockedReasons: [], assignmentAllowedConfirmed: true, buyerPofStatus: "verified", complianceReviewPassed: true, ownerApprovalRecorded: true, draftOnly: true, contractExecutionAllowed: false, titleSubmissionAllowed: false },
  { id: "assignment-ready-002", contractControlId: "contract-001", dealId: "deal-001", buyerId: "buyer-003", buyerMatchId: "match-001", buyerInterestId: "interest-004", readinessStatus: "blocked", assignmentReady: false, blockedReasons: ["buyer_pof_not_verified"], assignmentAllowedConfirmed: true, buyerPofStatus: "needs_refresh", complianceReviewPassed: true, ownerApprovalRecorded: true, draftOnly: true, contractExecutionAllowed: false, titleSubmissionAllowed: false },
  { id: "assignment-ready-003", contractControlId: "contract-003", dealId: "deal-005", buyerId: "buyer-004", buyerMatchId: "match-003", buyerInterestId: "interest-005", readinessStatus: "blocked", assignmentReady: false, blockedReasons: ["assignment_allowed_not_confirmed", "compliance_review_not_passed", "contract_control_not_ready"], assignmentAllowedConfirmed: false, buyerPofStatus: "verified", complianceReviewPassed: false, ownerApprovalRecorded: true, draftOnly: true, contractExecutionAllowed: false, titleSubmissionAllowed: false },
  { id: "assignment-ready-004", contractControlId: "contract-002", dealId: "deal-003", buyerId: "buyer-001", buyerMatchId: null, buyerInterestId: "interest-003", readinessStatus: "blocked", assignmentReady: false, blockedReasons: ["buyer_match_missing", "contract_control_not_ready", "owner_approval_not_recorded"], assignmentAllowedConfirmed: true, buyerPofStatus: "verified", complianceReviewPassed: true, ownerApprovalRecorded: false, draftOnly: true, contractExecutionAllowed: false, titleSubmissionAllowed: false }
];

export const communicationDrafts: CommunicationDraft[] = [
  { id: "comm-draft-001", draftType: "seller_follow_up", channel: "sms", recipientType: "seller", recipientEmailPlaceholder: "", recipientPhonePlaceholder: "seller-phone-placeholder-lead-001", sourceRecordType: "seller_interaction", sourceRecordId: "seller-interaction-001", subject: "", draftBody: "Hi Angela, this is a draft follow-up for owner review. We can talk through the as-is offer basis when it is convenient. Reply STOP to opt out.", status: "dry_run_ready", safetyChecked: true, safetyPassed: true, ownerApprovalRecorded: false, communicationLiveFlagEnabled: false, providerReadiness: false, lastDryRunReceiptId: "dryrun-001", approvedDryRunReceiptId: null, riskStatus: "clear", blockedReasons: [], liveSendCount: 0, draftOnly: true, bulkSendAllowed: false, campaignAllowed: false, autoFollowupAllowed: false, buyerBlastAllowed: false, titleSubmissionAllowed: false },
  { id: "comm-draft-002", draftType: "buyer_interest_response", channel: "email", recipientType: "buyer", recipientEmailPlaceholder: "jules@example.test", recipientPhonePlaceholder: "", sourceRecordType: "buyer_interest", sourceRecordId: "interest-001", subject: "Draft response on Dallas deal interest", draftBody: "Thanks for the draft interest. The owner will review proof of funds and deal-room details before any next step. This is not a contract or commitment.", status: "owner_approved_waiting_live_flags", safetyChecked: true, safetyPassed: true, ownerApprovalRecorded: true, communicationLiveFlagEnabled: false, providerReadiness: true, lastDryRunReceiptId: "dryrun-002", approvedDryRunReceiptId: "dryrun-002", riskStatus: "clear", blockedReasons: [], liveSendCount: 0, draftOnly: true, bulkSendAllowed: false, campaignAllowed: false, autoFollowupAllowed: false, buyerBlastAllowed: false, titleSubmissionAllowed: false },
  { id: "comm-draft-003", draftType: "title_handoff_email", channel: "email", recipientType: "title_company", recipientEmailPlaceholder: "title-company-placeholder@example.test", recipientPhonePlaceholder: "", sourceRecordType: "title_handoff_packet", sourceRecordId: "title-002", subject: "Draft title handoff packet for owner review", draftBody: "Draft only: attached packet placeholders need owner and attorney/title review before any title-company submission or external message.", status: "safety_needed", safetyChecked: false, safetyPassed: false, ownerApprovalRecorded: false, communicationLiveFlagEnabled: false, providerReadiness: false, lastDryRunReceiptId: null, approvedDryRunReceiptId: null, riskStatus: "unchecked", blockedReasons: [], liveSendCount: 0, draftOnly: true, bulkSendAllowed: false, campaignAllowed: false, autoFollowupAllowed: false, buyerBlastAllowed: false, titleSubmissionAllowed: false },
  { id: "comm-draft-004", draftType: "internal_owner_note", channel: "internal", recipientType: "owner", recipientEmailPlaceholder: "owner", recipientPhonePlaceholder: "", sourceRecordType: "contract_control", sourceRecordId: "contract-001", subject: "Owner note: communication gate review", draftBody: "Review dry-run receipts, safety results, recipient source tie, and live flags before authorizing any one-off communication.", status: "draft", safetyChecked: true, safetyPassed: true, ownerApprovalRecorded: false, communicationLiveFlagEnabled: false, providerReadiness: true, lastDryRunReceiptId: null, approvedDryRunReceiptId: null, riskStatus: "clear", blockedReasons: [], liveSendCount: 0, draftOnly: true, bulkSendAllowed: false, campaignAllowed: false, autoFollowupAllowed: false, buyerBlastAllowed: false, titleSubmissionAllowed: false },
  { id: "comm-draft-005", draftType: "seller_follow_up", channel: "sms", recipientType: "seller", recipientEmailPlaceholder: "", recipientPhonePlaceholder: "seller-phone-placeholder-lead-007", sourceRecordType: "seller_interaction", sourceRecordId: "seller-interaction-005", subject: "", draftBody: "You must sign now. This is your last chance and we already have a buyer.", status: "blocked_safety", safetyChecked: true, safetyPassed: false, ownerApprovalRecorded: false, communicationLiveFlagEnabled: false, providerReadiness: false, lastDryRunReceiptId: "dryrun-003", approvedDryRunReceiptId: null, riskStatus: "blocked", blockedReasons: ["pressure_language", "fake_buyer_claim", "missing_sms_opt_out"], liveSendCount: 0, draftOnly: true, bulkSendAllowed: false, campaignAllowed: false, autoFollowupAllowed: false, buyerBlastAllowed: false, titleSubmissionAllowed: false },
  { id: "comm-draft-006", draftType: "buyer_interest_response", channel: "email", recipientType: "buyer", recipientEmailPlaceholder: "priya@example.test", recipientPhonePlaceholder: "", sourceRecordType: "buyer_interest", sourceRecordId: "interest-002", subject: "Updated buyer response after dry-run", draftBody: "The owner updated this draft after the dry-run, so it must be dry-run again before any approval can be used.", status: "changed_after_dry_run", safetyChecked: true, safetyPassed: true, ownerApprovalRecorded: true, communicationLiveFlagEnabled: true, providerReadiness: true, lastDryRunReceiptId: "dryrun-004", approvedDryRunReceiptId: "dryrun-004", riskStatus: "clear", blockedReasons: [], liveSendCount: 0, draftOnly: true, bulkSendAllowed: false, campaignAllowed: false, autoFollowupAllowed: false, buyerBlastAllowed: false, titleSubmissionAllowed: false }
];

export const communicationDryRunReceipts: CommunicationDryRunReceipt[] = [
  { id: "dryrun-001", draftId: "comm-draft-001", recipient: "seller-phone-placeholder-lead-001", subjectBodyHash: "hash-sms-safe", sourceRecordType: "seller_interaction", sourceRecordId: "seller-interaction-001", riskStatus: "clear", safetyResult: { allowed: true, riskFlags: [], reason: "Communication draft passed safety checks." }, timestamp: "2026-05-04T15:15:00Z", providerMode: "mock/dry_run", idempotencyKey: "idem-dryrun-001" },
  { id: "dryrun-002", draftId: "comm-draft-002", recipient: "jules@example.test", subjectBodyHash: "hash-buyer-safe", sourceRecordType: "buyer_interest", sourceRecordId: "interest-001", riskStatus: "clear", safetyResult: { allowed: true, riskFlags: [], reason: "Communication draft passed safety checks." }, timestamp: "2026-05-04T15:20:00Z", providerMode: "mock/dry_run", idempotencyKey: "idem-dryrun-002" },
  { id: "dryrun-003", draftId: "comm-draft-005", recipient: "seller-phone-placeholder-lead-007", subjectBodyHash: "hash-sms-blocked", sourceRecordType: "seller_interaction", sourceRecordId: "seller-interaction-005", riskStatus: "blocked", safetyResult: { allowed: false, riskFlags: ["fake_buyer_claim", "missing_sms_opt_out", "pressure_language"], reason: "Communication draft blocked by safety checks." }, timestamp: "2026-05-04T15:25:00Z", providerMode: "mock/dry_run", idempotencyKey: "idem-dryrun-003" },
  { id: "dryrun-004", draftId: "comm-draft-006", recipient: "priya@example.test", subjectBodyHash: "outdated-dry-run-hash", sourceRecordType: "buyer_interest", sourceRecordId: "interest-002", riskStatus: "stale", safetyResult: { allowed: true, riskFlags: [], reason: "Communication draft passed safety checks." }, timestamp: "2026-05-04T15:30:00Z", providerMode: "mock/dry_run", idempotencyKey: "idem-dryrun-004" }
];

export const communicationApprovals: CommunicationApproval[] = [
  { id: "comm-approval-001", draftId: "comm-draft-002", dryRunReceiptId: "dryrun-002", ownerApprovalRecorded: true, approvalStatus: "approved", approvalNotes: "Owner approved one-off mock-send eligibility; global live flag remains disabled.", approvedBy: "Owner", draftHashAtApproval: "hash-buyer-safe" },
  { id: "comm-approval-002", draftId: "comm-draft-006", dryRunReceiptId: "dryrun-004", ownerApprovalRecorded: true, approvalStatus: "stale_after_draft_change", approvalNotes: "Approval is stale because the draft changed after dry-run.", approvedBy: "Owner", draftHashAtApproval: "outdated-dry-run-hash" }
];

export const communicationSendAttempts: CommunicationSendAttempt[] = [
  { id: "comm-attempt-001", draftId: "comm-draft-002", dryRunReceiptId: "dryrun-002", recipient: "jules@example.test", channel: "email", providerMode: "mock/dry_run", attemptStatus: "blocked", blockedReasons: ["global_live_flag_disabled", "communication_live_flag_disabled"], idempotencyKey: "idem-dryrun-002", providerCalled: false, mockSent: false, liveSendRequested: true, bulkSendDetected: false },
  { id: "comm-attempt-002", draftId: "comm-draft-005", dryRunReceiptId: "dryrun-003", recipient: "seller-phone-placeholder-lead-007", channel: "sms", providerMode: "mock/dry_run", attemptStatus: "blocked", blockedReasons: ["safety_not_passed"], idempotencyKey: "idem-dryrun-003", providerCalled: false, mockSent: false, liveSendRequested: true, bulkSendDetected: false }
];

const sellerDocumentChecklist = [
  "property details summary reviewed",
  "offer amount summary reviewed",
  "access preference placeholder",
  "title company review reminder",
  "seller questions intake available"
];

export const sellerOfferPublications: SellerOfferPublication[] = [
  { id: "seller-offer-001", leadId: "lead-001", dealId: "deal-001", offerPacketId: "packet-001", contractControlId: "contract-001", portalVisibilityEnabled: true, offerStatus: "owner_approved_offer_ready", offerAmount: 151000, closingTimelineEstimate: "14-21 days after owner-approved next steps", inspectionAccessNextStep: "Share preferred access windows for operator review.", titleCompanyReviewStatus: "Title/attorney review reminder active; no submission from portal.", documentChecklist: sellerDocumentChecklist, operatorContactPlaceholder: "Owner/operator contact placeholder for questions.", offerLanguage: "The offer summary is ready for review. There is no pressure to decide in the portal, and questions are routed for operator review.", offerLanguageSafetyPassed: true, complianceCheckPassed: true, ownerApprovalRecorded: true, visibilityStatus: "visible", blockedReasons: [], draftOnly: true, contractExecutionAllowed: false, liveNegotiationAutomationAllowed: false, legalAdviceProvided: false, buyerDataExposed: false, internalProfitLogicExposed: false },
  { id: "seller-offer-002", leadId: "lead-003", dealId: "deal-003", offerPacketId: "packet-002", contractControlId: "contract-002", portalVisibilityEnabled: true, offerStatus: "owner_review_required", offerAmount: 180000, closingTimelineEstimate: "30 days after owner approval", inspectionAccessNextStep: "Access options pending owner approval.", titleCompanyReviewStatus: "Title review pending owner approval.", documentChecklist: sellerDocumentChecklist, operatorContactPlaceholder: "Owner/operator contact placeholder.", offerLanguage: "Owner review is still required before this offer can be shown.", offerLanguageSafetyPassed: true, complianceCheckPassed: true, ownerApprovalRecorded: false, visibilityStatus: "blocked", blockedReasons: ["owner_approval_not_recorded"], draftOnly: true, contractExecutionAllowed: false, liveNegotiationAutomationAllowed: false, legalAdviceProvided: false, buyerDataExposed: false, internalProfitLogicExposed: false },
  { id: "seller-offer-003", leadId: "lead-005", dealId: "deal-005", offerPacketId: "packet-003", contractControlId: "contract-003", portalVisibilityEnabled: true, offerStatus: "review_blocked", offerAmount: 220000, closingTimelineEstimate: "21-30 days after review clears", inspectionAccessNextStep: "Access is held until review clears.", titleCompanyReviewStatus: "Review required before seller-facing visibility.", documentChecklist: [...sellerDocumentChecklist, "authority documentation placeholder"], operatorContactPlaceholder: "Owner/operator contact placeholder.", offerLanguage: "This offer summary remains blocked until review is complete.", offerLanguageSafetyPassed: true, complianceCheckPassed: false, ownerApprovalRecorded: true, visibilityStatus: "blocked", blockedReasons: ["compliance_check_not_passed"], draftOnly: true, contractExecutionAllowed: false, liveNegotiationAutomationAllowed: false, legalAdviceProvided: false, buyerDataExposed: false, internalProfitLogicExposed: false },
  { id: "seller-offer-004", leadId: "lead-007", dealId: "deal-007", offerPacketId: "packet-005", contractControlId: "contract-005", portalVisibilityEnabled: false, offerStatus: "draft_only", offerAmount: 75000, closingTimelineEstimate: "10-14 days after gate review", inspectionAccessNextStep: "Access notes held internally.", titleCompanyReviewStatus: "Review pending.", documentChecklist: sellerDocumentChecklist, operatorContactPlaceholder: "Owner/operator contact placeholder.", offerLanguage: "Draft-only offer summary is not visible yet.", offerLanguageSafetyPassed: true, complianceCheckPassed: true, ownerApprovalRecorded: true, visibilityStatus: "draft", blockedReasons: ["portal_visibility_not_enabled"], draftOnly: true, contractExecutionAllowed: false, liveNegotiationAutomationAllowed: false, legalAdviceProvided: false, buyerDataExposed: false, internalProfitLogicExposed: false },
  { id: "seller-offer-005", leadId: "lead-006", dealId: "deal-006", offerPacketId: "packet-004", contractControlId: "contract-004", portalVisibilityEnabled: true, offerStatus: "blocked_safety", offerAmount: 132000, closingTimelineEstimate: "Held until safety review clears", inspectionAccessNextStep: "No portal action while blocked.", titleCompanyReviewStatus: "Review blocked.", documentChecklist: sellerDocumentChecklist, operatorContactPlaceholder: "Owner/operator contact placeholder.", offerLanguage: "You must sign now. This is your last chance and no attorney needed.", offerLanguageSafetyPassed: false, complianceCheckPassed: true, ownerApprovalRecorded: true, visibilityStatus: "blocked", blockedReasons: ["offer_language_safety_not_passed"], draftOnly: true, contractExecutionAllowed: false, liveNegotiationAutomationAllowed: false, legalAdviceProvided: false, buyerDataExposed: false, internalProfitLogicExposed: false }
];

export const sellerPortalResponses: SellerPortalResponse[] = [
  { id: "seller-response-001", sellerOfferPublicationId: "seller-offer-001", responseType: "seller_portal_note", sellerPortalNote: "Seller asked for a plain-language explanation of next steps.", offerQuestion: "", appointmentAccessPreference: "", documentUploadPlaceholder: "", responseStatus: "received_for_operator_review", operatorReviewStatus: "pending_review", draftOnly: true, negotiationExecutionAllowed: false, contractExecutionAllowed: false, automaticAcceptanceAllowed: false },
  { id: "seller-response-002", sellerOfferPublicationId: "seller-offer-001", responseType: "offer_question", sellerPortalNote: "", offerQuestion: "Can the closing timeline be closer to three weeks if access is easy?", appointmentAccessPreference: "", documentUploadPlaceholder: "", responseStatus: "received_for_operator_review", operatorReviewStatus: "pending_review", draftOnly: true, negotiationExecutionAllowed: false, contractExecutionAllowed: false, automaticAcceptanceAllowed: false },
  { id: "seller-response-003", sellerOfferPublicationId: "seller-offer-001", responseType: "appointment_access_preference", sellerPortalNote: "", offerQuestion: "", appointmentAccessPreference: "Weekday afternoons are easiest for access review.", documentUploadPlaceholder: "", responseStatus: "received_for_operator_review", operatorReviewStatus: "reviewed", draftOnly: true, negotiationExecutionAllowed: false, contractExecutionAllowed: false, automaticAcceptanceAllowed: false },
  { id: "seller-response-004", sellerOfferPublicationId: "seller-offer-001", responseType: "document_upload_placeholder", sellerPortalNote: "", offerQuestion: "", appointmentAccessPreference: "", documentUploadPlaceholder: "Seller plans to provide payoff statement placeholder after operator review.", responseStatus: "placeholder_only", operatorReviewStatus: "pending_review", draftOnly: true, negotiationExecutionAllowed: false, contractExecutionAllowed: false, automaticAcceptanceAllowed: false }
];

export const unifiedDealRooms: UnifiedDealRoom[] = [
  { id: "deal-room-001", dealId: "deal-001", contractControlId: "contract-001", sellerOfferPublicationId: "seller-offer-001", buyerDealPublicationId: "publication-001", titleHandoffPacketId: "title-001", assignmentReadinessRecordId: "assignment-ready-001", sellerPortalStatus: "visible", buyerPortalStatus: "visible", titleHandoffStatus: "draft_ready", assignmentReadinessStatus: "assignment_ready", communicationStatus: "ready", complianceStatus: "complete", closingTimeline: "14-21 days", blockers: [], nextRequiredActions: [], ownerApprovalStatus: "approved", coordinationStatus: "closing_ready", projectedAssignmentFeeAtRisk: 0, draftOnly: true, legalExecutionAllowed: false, executableContractGenerated: false, titleSubmissionAllowed: false, paymentHandlingAllowed: false, automaticNegotiationAllowed: false },
  { id: "deal-room-002", dealId: "deal-003", contractControlId: "contract-002", sellerOfferPublicationId: "seller-offer-002", buyerDealPublicationId: "publication-003", titleHandoffPacketId: "title-002", assignmentReadinessRecordId: "assignment-ready-004", sellerPortalStatus: "blocked", buyerPortalStatus: "visible", titleHandoffStatus: "blocked_owner_review", assignmentReadinessStatus: "blocked", communicationStatus: "pending", complianceStatus: "complete", closingTimeline: "30 days", blockers: ["missing_owner_approval", "communication_draft_pending"], nextRequiredActions: ["update closing timeline", "approve communication dry-run"], ownerApprovalStatus: "pending", coordinationStatus: "blocked", projectedAssignmentFeeAtRisk: 13000, draftOnly: true, legalExecutionAllowed: false, executableContractGenerated: false, titleSubmissionAllowed: false, paymentHandlingAllowed: false, automaticNegotiationAllowed: false },
  { id: "deal-room-003", dealId: "deal-005", contractControlId: "contract-003", sellerOfferPublicationId: "seller-offer-003", buyerDealPublicationId: "publication-005", titleHandoffPacketId: "title-003", assignmentReadinessRecordId: "assignment-ready-003", sellerPortalStatus: "blocked", buyerPortalStatus: "blocked", titleHandoffStatus: "blocked_compliance", assignmentReadinessStatus: "blocked", communicationStatus: "missing", complianceStatus: "pending", closingTimeline: "21-30 days", blockers: ["missing_compliance_review", "assignment_not_confirmed", "missing_seller_document", "title_handoff_incomplete", "communication_draft_pending"], nextRequiredActions: ["resolve compliance blocker", "review assignment readiness", "review seller response", "prepare title handoff", "approve communication dry-run"], ownerApprovalStatus: "approved", coordinationStatus: "blocked", projectedAssignmentFeeAtRisk: 15000, draftOnly: true, legalExecutionAllowed: false, executableContractGenerated: false, titleSubmissionAllowed: false, paymentHandlingAllowed: false, automaticNegotiationAllowed: false },
  { id: "deal-room-004", dealId: "deal-006", contractControlId: "contract-004", sellerOfferPublicationId: "seller-offer-005", buyerDealPublicationId: "publication-006", titleHandoffPacketId: null, assignmentReadinessRecordId: null, sellerPortalStatus: "blocked", buyerPortalStatus: "blocked", titleHandoffStatus: "missing", assignmentReadinessStatus: "blocked", communicationStatus: "missing", complianceStatus: "complete", closingTimeline: "", blockers: ["missing_buyer_pof", "missing_seller_document", "weak_buyer_margin", "high_risk_language", "assignment_not_confirmed", "title_handoff_incomplete", "communication_draft_pending"], nextRequiredActions: ["verify buyer POF", "review seller response", "review assignment readiness", "resolve compliance blocker", "prepare title handoff", "approve communication dry-run"], ownerApprovalStatus: "approved", coordinationStatus: "blocked", projectedAssignmentFeeAtRisk: 8000, draftOnly: true, legalExecutionAllowed: false, executableContractGenerated: false, titleSubmissionAllowed: false, paymentHandlingAllowed: false, automaticNegotiationAllowed: false }
];

export const closingCoordinationChecklists: ClosingCoordinationChecklist[] = [
  { id: "closing-checklist-001", dealRoomId: "deal-room-001", sellerAcceptedOffer: true, contractPrepReady: true, buyerMatched: true, buyerPofVerified: true, assignmentAllowedConfirmed: true, titleHandoffPrepared: true, inspectionAccessCoordinated: true, sellerDocumentsRequested: true, buyerIntentRecorded: true, complianceReviewComplete: true, ownerApprovalComplete: true, readinessStatus: "checklist_complete", blockedReasons: [], draftOnly: true, legalExecutionAllowed: false, titleSubmissionAllowed: false, paymentHandlingAllowed: false, automaticNegotiationAllowed: false },
  { id: "closing-checklist-002", dealRoomId: "deal-room-002", sellerAcceptedOffer: true, contractPrepReady: false, buyerMatched: false, buyerPofVerified: true, assignmentAllowedConfirmed: true, titleHandoffPrepared: true, inspectionAccessCoordinated: true, sellerDocumentsRequested: true, buyerIntentRecorded: true, complianceReviewComplete: true, ownerApprovalComplete: false, readinessStatus: "blocked", blockedReasons: ["contract_prep_ready", "buyer_matched", "owner_approval_complete"], draftOnly: true, legalExecutionAllowed: false, titleSubmissionAllowed: false, paymentHandlingAllowed: false, automaticNegotiationAllowed: false },
  { id: "closing-checklist-003", dealRoomId: "deal-room-003", sellerAcceptedOffer: true, contractPrepReady: false, buyerMatched: true, buyerPofVerified: true, assignmentAllowedConfirmed: false, titleHandoffPrepared: false, inspectionAccessCoordinated: false, sellerDocumentsRequested: false, buyerIntentRecorded: true, complianceReviewComplete: false, ownerApprovalComplete: true, readinessStatus: "blocked", blockedReasons: ["contract_prep_ready", "assignment_allowed_confirmed", "title_handoff_prepared", "inspection_access_coordinated", "seller_documents_requested", "compliance_review_complete"], draftOnly: true, legalExecutionAllowed: false, titleSubmissionAllowed: false, paymentHandlingAllowed: false, automaticNegotiationAllowed: false },
  { id: "closing-checklist-004", dealRoomId: "deal-room-004", sellerAcceptedOffer: false, contractPrepReady: false, buyerMatched: false, buyerPofVerified: false, assignmentAllowedConfirmed: false, titleHandoffPrepared: false, inspectionAccessCoordinated: false, sellerDocumentsRequested: false, buyerIntentRecorded: false, complianceReviewComplete: true, ownerApprovalComplete: true, readinessStatus: "blocked", blockedReasons: ["seller_accepted_offer", "contract_prep_ready", "buyer_matched", "buyer_pof_verified", "assignment_allowed_confirmed", "title_handoff_prepared", "inspection_access_coordinated", "seller_documents_requested", "buyer_intent_recorded"], draftOnly: true, legalExecutionAllowed: false, titleSubmissionAllowed: false, paymentHandlingAllowed: false, automaticNegotiationAllowed: false }
];

export const dealRoomBlockers: DealRoomBlocker[] = [
  { id: "deal-blocker-001", dealRoomId: "deal-room-002", dealId: "deal-003", blockerType: "missing_owner_approval", severity: "critical", status: "open", source: "closing_coordination_gate", detail: "Owner approval is required for real-world coordination steps.", recommendation: "update closing timeline", blocksClosing: true, ownerActionRequired: true, resolved: false, draftOnly: true },
  { id: "deal-blocker-002", dealRoomId: "deal-room-002", dealId: "deal-003", blockerType: "communication_draft_pending", severity: "medium", status: "open", source: "closing_coordination_gate", detail: "Communication draft still needs safety or dry-run review.", recommendation: "approve communication dry-run", blocksClosing: true, ownerActionRequired: false, resolved: false, draftOnly: true },
  { id: "deal-blocker-003", dealRoomId: "deal-room-003", dealId: "deal-005", blockerType: "missing_compliance_review", severity: "critical", status: "open", source: "closing_coordination_gate", detail: "Compliance review must be complete before closing coordination can clear.", recommendation: "resolve compliance blocker", blocksClosing: true, ownerActionRequired: true, resolved: false, draftOnly: true },
  { id: "deal-blocker-004", dealRoomId: "deal-room-003", dealId: "deal-005", blockerType: "assignment_not_confirmed", severity: "high", status: "open", source: "closing_coordination_gate", detail: "Assignment allowed status must be confirmed.", recommendation: "review assignment readiness", blocksClosing: true, ownerActionRequired: false, resolved: false, draftOnly: true },
  { id: "deal-blocker-005", dealRoomId: "deal-room-003", dealId: "deal-005", blockerType: "title_handoff_incomplete", severity: "high", status: "open", source: "closing_coordination_gate", detail: "Title handoff packet is missing or incomplete.", recommendation: "prepare title handoff", blocksClosing: true, ownerActionRequired: false, resolved: false, draftOnly: true },
  { id: "deal-blocker-006", dealRoomId: "deal-room-003", dealId: "deal-005", blockerType: "missing_seller_document", severity: "medium", status: "open", source: "closing_coordination_gate", detail: "Seller document or access item still needs operator review.", recommendation: "review seller response", blocksClosing: true, ownerActionRequired: false, resolved: false, draftOnly: true },
  { id: "deal-blocker-007", dealRoomId: "deal-room-004", dealId: "deal-006", blockerType: "missing_buyer_pof", severity: "high", status: "open", source: "closing_coordination_gate", detail: "Buyer proof of funds must be verified before assignment readiness.", recommendation: "verify buyer POF", blocksClosing: true, ownerActionRequired: false, resolved: false, draftOnly: true },
  { id: "deal-blocker-008", dealRoomId: "deal-room-004", dealId: "deal-006", blockerType: "weak_buyer_margin", severity: "critical", status: "open", source: "closing_coordination_gate", detail: "Buyer margin is below the protected threshold.", recommendation: "review assignment readiness", blocksClosing: true, ownerActionRequired: true, resolved: false, draftOnly: true },
  { id: "deal-blocker-009", dealRoomId: "deal-room-004", dealId: "deal-006", blockerType: "high_risk_language", severity: "critical", status: "open", source: "closing_coordination_gate", detail: "Unsafe language is present in a seller or communication record.", recommendation: "resolve compliance blocker", blocksClosing: true, ownerActionRequired: true, resolved: false, draftOnly: true }
];

const sourceFormulaBasis = [
  "seller_contract_price:deal.sellerContractPrice",
  "buyer_purchase_price:deal.buyerPurchasePrice",
  "assignment_fee:buyer_purchase_price_minus_seller_contract_price",
  "buyer_margin:arv_minus_repairs_minus_buyer_costs_minus_buyer_purchase_price"
];

export const dealEvidencePackets: DealEvidencePacket[] = [
  {
    id: "evidence-001",
    dealRoomId: "deal-room-001",
    dealId: "deal-001",
    leadSource: "vacant",
    sellerInteractionProof: { sellerInteractionId: "seller-interaction-001", sellerAcceptanceRecorded: true, acceptedTermsRecordId: "contract-001" },
    underwritingSnapshot: { arv: 275000, repairs: 45000, buyerCosts: 6000, buyerDesiredProfit: 6000, sellerContractPrice: 151000, buyerPurchasePrice: 166000, projectedAssignmentFee: 15000 },
    buyerInterestProof: { buyerInterestId: "interest-001", interestStatus: "owner_review_needed", intendedOfferAmount: 166000, draftOnly: true, contractExecutionAllowed: false },
    pofProofStatus: "verified",
    contractControlStatus: "prep_review",
    titleHandoffStatus: "draft_ready",
    communicationReceipts: [
      { draftId: "comm-draft-001", sourceRecordId: "seller-interaction-001", dryRunReceipts: ["dryrun-001"], safetyPassed: true, providerMode: "mock/dry_run" },
      { draftId: "comm-draft-002", sourceRecordId: "interest-001", dryRunReceipts: ["dryrun-002"], safetyPassed: true, providerMode: "mock/dry_run" }
    ],
    blockerHistory: [],
    complianceReviewStatus: "approved",
    sourceRecordsPresent: true,
    unsupportedProfitClaims: [],
    evidenceStatus: "approved",
    ownerReviewStatus: "owner_approved",
    approved: true,
    sanitizedSummary: { sourceRecords: ["contract-001", "interest-001", "seller-interaction-001"], internalNotesRemoved: true },
    internalNotesSanitized: true,
    draftOnly: true,
    clientFacingProofAllowed: false,
    legalClosingGuaranteeAllowed: false
  },
  {
    id: "evidence-002",
    dealRoomId: "deal-room-002",
    dealId: "deal-003",
    leadSource: "absentee owner",
    sellerInteractionProof: { sellerInteractionId: "seller-interaction-003", sellerAcceptanceRecorded: true, acceptedTermsRecordId: "contract-002" },
    underwritingSnapshot: { arv: 340000, repairs: 65000, buyerCosts: 7500, buyerDesiredProfit: 7500, sellerContractPrice: 180000, buyerPurchasePrice: 193000, projectedAssignmentFee: 13000 },
    buyerInterestProof: { buyerInterestId: "interest-003", interestStatus: "proof_of_funds_needed", intendedOfferAmount: 193000, draftOnly: true, contractExecutionAllowed: false },
    pofProofStatus: "needs_refresh",
    contractControlStatus: "prep_review",
    titleHandoffStatus: "blocked_owner_review",
    communicationReceipts: [
      { draftId: "comm-draft-003", sourceRecordId: "title-002", dryRunReceipts: [], safetyPassed: false, providerMode: "mock/dry_run" }
    ],
    blockerHistory: [
      { blockerId: "deal-blocker-001", blockerType: "missing_owner_approval", status: "open", resolved: false },
      { blockerId: "deal-blocker-002", blockerType: "communication_draft_pending", status: "open", resolved: false }
    ],
    complianceReviewStatus: "approved",
    sourceRecordsPresent: true,
    unsupportedProfitClaims: [],
    evidenceStatus: "owner_review_needed",
    ownerReviewStatus: "pending_review",
    approved: false,
    sanitizedSummary: { sourceRecords: ["contract-002", "interest-003", "seller-interaction-003"], internalNotesRemoved: true },
    internalNotesSanitized: true,
    draftOnly: true,
    clientFacingProofAllowed: false,
    legalClosingGuaranteeAllowed: false
  },
  {
    id: "evidence-003",
    dealRoomId: "deal-room-003",
    dealId: "deal-005",
    leadSource: "probate",
    sellerInteractionProof: { sellerInteractionId: "seller-interaction-005", sellerAcceptanceRecorded: true, acceptedTermsRecordId: "contract-003" },
    underwritingSnapshot: { arv: 425000, repairs: 90000, buyerCosts: 10000, buyerDesiredProfit: 10000, sellerContractPrice: 220000, buyerPurchasePrice: 235000, projectedAssignmentFee: 15000 },
    buyerInterestProof: { buyerInterestId: "interest-005", interestStatus: "owner_review_needed", intendedOfferAmount: 235000, draftOnly: true, contractExecutionAllowed: false },
    pofProofStatus: "verified",
    contractControlStatus: "prep_review",
    titleHandoffStatus: "blocked_compliance",
    communicationReceipts: [],
    blockerHistory: [
      { blockerId: "deal-blocker-003", blockerType: "missing_compliance_review", status: "open", resolved: false },
      { blockerId: "deal-blocker-004", blockerType: "assignment_not_confirmed", status: "open", resolved: false }
    ],
    complianceReviewStatus: "pending",
    sourceRecordsPresent: true,
    unsupportedProfitClaims: [],
    evidenceStatus: "blocked_missing_evidence",
    ownerReviewStatus: "pending_review",
    approved: false,
    sanitizedSummary: { sourceRecords: ["contract-003", "interest-005", "seller-interaction-005"], internalNotesRemoved: true },
    internalNotesSanitized: true,
    draftOnly: true,
    clientFacingProofAllowed: false,
    legalClosingGuaranteeAllowed: false
  },
  {
    id: "evidence-004",
    dealRoomId: "deal-room-004",
    dealId: "deal-006",
    leadSource: "tax delinquent",
    sellerInteractionProof: { sellerInteractionId: null, sellerAcceptanceRecorded: false, acceptedTermsRecordId: "contract-004" },
    underwritingSnapshot: { arv: 260000, repairs: 70000, buyerCosts: 6000, buyerDesiredProfit: 6000, sellerContractPrice: 132000, buyerPurchasePrice: 140000, projectedAssignmentFee: 8000 },
    buyerInterestProof: { buyerInterestId: null, interestStatus: "missing", intendedOfferAmount: null, draftOnly: true, contractExecutionAllowed: false },
    pofProofStatus: "missing",
    contractControlStatus: "blocked",
    titleHandoffStatus: "missing",
    communicationReceipts: [],
    blockerHistory: [
      { blockerId: "deal-blocker-007", blockerType: "missing_buyer_pof", status: "open", resolved: false },
      { blockerId: "deal-blocker-008", blockerType: "weak_buyer_margin", status: "open", resolved: false },
      { blockerId: "deal-blocker-009", blockerType: "high_risk_language", status: "open", resolved: false }
    ],
    complianceReviewStatus: "approved",
    sourceRecordsPresent: false,
    unsupportedProfitClaims: [],
    evidenceStatus: "blocked_missing_evidence",
    ownerReviewStatus: "owner_approved",
    approved: false,
    sanitizedSummary: { sourceRecords: ["contract-004"], internalNotesRemoved: true },
    internalNotesSanitized: true,
    draftOnly: true,
    clientFacingProofAllowed: false,
    legalClosingGuaranteeAllowed: false
  }
];

export const assignmentFeeAttributions: AssignmentFeeAttribution[] = [
  { id: "fee-001", dealRoomId: "deal-room-001", dealId: "deal-001", evidencePacketId: "evidence-001", projectedAssignmentFee: 15000, targetAssignmentFee: 10000, sellerContractPrice: 151000, buyerPurchasePrice: 166000, buyerMargin: 58000, attributionBasis: ["deal:deal-001", "deal_room:deal-room-001", "contract_control:contract-001", "buyer_interest:interest-001", "evidence_packet:evidence-001", ...sourceFormulaBasis], confidenceScore: 92, verificationStatus: "verified", ownerReviewStatus: "owner_approved", sourceRecordsPresent: true, unsupportedProfitClaims: [], verified10kOpportunity: true, draftOnly: true, clientFacingProofAllowed: false, legalClosingGuaranteeAllowed: false },
  { id: "fee-002", dealRoomId: "deal-room-002", dealId: "deal-003", evidencePacketId: "evidence-002", projectedAssignmentFee: 13000, targetAssignmentFee: 10000, sellerContractPrice: 180000, buyerPurchasePrice: 193000, buyerMargin: 74500, attributionBasis: ["deal:deal-003", "deal_room:deal-room-002", "contract_control:contract-002", "buyer_interest:interest-003", "evidence_packet:evidence-002", ...sourceFormulaBasis], confidenceScore: 64, verificationStatus: "owner_review_needed", ownerReviewStatus: "pending_review", sourceRecordsPresent: true, unsupportedProfitClaims: [], verified10kOpportunity: false, draftOnly: true, clientFacingProofAllowed: false, legalClosingGuaranteeAllowed: false },
  { id: "fee-003", dealRoomId: "deal-room-003", dealId: "deal-005", evidencePacketId: "evidence-003", projectedAssignmentFee: 15000, targetAssignmentFee: 10000, sellerContractPrice: 220000, buyerPurchasePrice: 235000, buyerMargin: 90000, attributionBasis: ["deal:deal-005", "deal_room:deal-room-003", "contract_control:contract-003", "buyer_interest:interest-005", "evidence_packet:evidence-003", ...sourceFormulaBasis], confidenceScore: 25, verificationStatus: "blocked", ownerReviewStatus: "pending_review", sourceRecordsPresent: true, unsupportedProfitClaims: [], verified10kOpportunity: false, draftOnly: true, clientFacingProofAllowed: false, legalClosingGuaranteeAllowed: false },
  { id: "fee-004", dealRoomId: "deal-room-004", dealId: "deal-006", evidencePacketId: "evidence-004", projectedAssignmentFee: 8000, targetAssignmentFee: 10000, sellerContractPrice: 132000, buyerPurchasePrice: 140000, buyerMargin: 44000, attributionBasis: ["deal:deal-006", "deal_room:deal-room-004", "contract_control:contract-004", "evidence_packet:evidence-004", ...sourceFormulaBasis], confidenceScore: 17, verificationStatus: "missing_evidence", ownerReviewStatus: "owner_approved", sourceRecordsPresent: false, unsupportedProfitClaims: [], verified10kOpportunity: false, draftOnly: true, clientFacingProofAllowed: false, legalClosingGuaranteeAllowed: false }
];

function sanitizedDistributionSheet(dealId: string): SanitizedBuyerDealSheet {
  const deal = deals.find((item) => item.id === dealId);
  const lead = deal ? leads.find((item) => item.id === deal.leadId) : undefined;
  const publication = buyerPublications.find((item) => item.dealId === dealId);
  if (!deal || !lead || !publication) {
    throw new Error("Missing distribution sheet source data.");
  }
  return {
    propertySummary: {
      city: lead.city,
      state: lead.state,
      zipCode: lead.zipCode,
      propertyType: lead.propertyType,
      beds: publication.beds,
      baths: publication.baths,
      sqft: publication.sqft
    },
    askingPrice: publication.askingPrice,
    arvRange: publication.arvRange,
    repairEstimateRange: publication.repairEstimateRange,
    buyerMarginEstimate: publication.estimatedBuyerMargin,
    accessInstructionsPlaceholder: publication.accessInstructionsPlaceholder,
    availabilityStatus: publication.availabilityStatus,
    proofInspectionNotesPlaceholder: "POF verification and inspection/access notes placeholder only."
  };
}

export const buyerDemandProfiles: BuyerDemandProfile[] = [
  { id: "buyer-demand-001", buyerId: "buyer-001", buyerActivityScore: 96, zipCodeDemandScore: 94, propertyTypeDemandScore: 93, priceBandFitScore: 95, closingSpeedScore: 95, proofOfFundsStrength: 100, reliabilityScore: 94, lastEngagedDate: "2026-05-03", preferredSpreadMarginNotes: "Prefers 30K+ buyer margin with fast assignment review.", targetZipCodes: ["75216", "75224", "75208"], propertyType: "single_family", priceBand: "0-210000", active: true, draftOnly: true },
  { id: "buyer-demand-002", buyerId: "buyer-002", buyerActivityScore: 92, zipCodeDemandScore: 89, propertyTypeDemandScore: 91, priceBandFitScore: 96, closingSpeedScore: 100, proofOfFundsStrength: 100, reliabilityScore: 91, lastEngagedDate: "2026-05-04", preferredSpreadMarginNotes: "Fast close buyer; strongest below 150K asking price.", targetZipCodes: ["75216", "75241"], propertyType: "single_family", priceBand: "0-150000", active: true, draftOnly: true },
  { id: "buyer-demand-003", buyerId: "buyer-003", buyerActivityScore: 78, zipCodeDemandScore: 74, propertyTypeDemandScore: 82, priceBandFitScore: 84, closingSpeedScore: 84, proofOfFundsStrength: 58, reliabilityScore: 82, lastEngagedDate: "2026-04-29", preferredSpreadMarginNotes: "Needs POF refresh before any owner-approved response.", targetZipCodes: ["76104", "76115"], propertyType: "single_family", priceBand: "0-140000", active: true, draftOnly: true },
  { id: "buyer-demand-004", buyerId: "buyer-004", buyerActivityScore: 88, zipCodeDemandScore: 92, propertyTypeDemandScore: 86, priceBandFitScore: 86, closingSpeedScore: 86, proofOfFundsStrength: 100, reliabilityScore: 88, lastEngagedDate: "2026-05-01", preferredSpreadMarginNotes: "Best for duplex or larger inherited-property margins.", targetZipCodes: ["75216", "75208", "75212"], propertyType: "duplex", priceBand: "0-260000", active: true, draftOnly: true },
  { id: "buyer-demand-005", buyerId: "buyer-005", buyerActivityScore: 72, zipCodeDemandScore: 78, propertyTypeDemandScore: 70, priceBandFitScore: 66, closingSpeedScore: 66, proofOfFundsStrength: 100, reliabilityScore: 78, lastEngagedDate: "2026-04-22", preferredSpreadMarginNotes: "High price capacity but slower closing coordination.", targetZipCodes: ["75229", "75220", "75218"], propertyType: "single_family", priceBand: "0-360000", active: true, draftOnly: true },
  { id: "buyer-demand-006", buyerId: "buyer-006", buyerActivityScore: 85, zipCodeDemandScore: 84, propertyTypeDemandScore: 87, priceBandFitScore: 95, closingSpeedScore: 95, proofOfFundsStrength: 100, reliabilityScore: 86, lastEngagedDate: "2026-05-02", preferredSpreadMarginNotes: "Good fit for repair-heavy south Dallas single-family deals.", targetZipCodes: ["75211", "75212", "75210"], propertyType: "single_family", priceBand: "0-175000", active: true, draftOnly: true },
  { id: "buyer-demand-007", buyerId: "buyer-007", buyerActivityScore: 69, zipCodeDemandScore: 70, propertyTypeDemandScore: 72, priceBandFitScore: 66, closingSpeedScore: 66, proofOfFundsStrength: 25, reliabilityScore: 74, lastEngagedDate: "2026-04-20", preferredSpreadMarginNotes: "Responsive but POF verification is still missing.", targetZipCodes: ["75217", "75227"], propertyType: "single_family", priceBand: "0-135000", active: true, draftOnly: true },
  { id: "buyer-demand-008", buyerId: "buyer-008", buyerActivityScore: 82, zipCodeDemandScore: 76, propertyTypeDemandScore: 80, priceBandFitScore: 98, closingSpeedScore: 98, proofOfFundsStrength: 100, reliabilityScore: 83, lastEngagedDate: "2026-05-03", preferredSpreadMarginNotes: "Fast small-deal buyer; price ceiling limits larger opportunities.", targetZipCodes: ["76104", "75216"], propertyType: "any", priceBand: "0-120000", active: true, draftOnly: true },
  { id: "buyer-demand-009", buyerId: "buyer-009", buyerActivityScore: 75, zipCodeDemandScore: 79, propertyTypeDemandScore: 73, priceBandFitScore: 70, closingSpeedScore: 70, proofOfFundsStrength: 100, reliabilityScore: 80, lastEngagedDate: "2026-04-25", preferredSpreadMarginNotes: "Rental buyer with clean POF and moderate close speed.", targetZipCodes: ["75237", "75241"], propertyType: "single_family", priceBand: "0-125000", active: true, draftOnly: true },
  { id: "buyer-demand-010", buyerId: "buyer-010", buyerActivityScore: 80, zipCodeDemandScore: 81, propertyTypeDemandScore: 83, priceBandFitScore: 92, closingSpeedScore: 92, proofOfFundsStrength: 58, reliabilityScore: 81, lastEngagedDate: "2026-04-28", preferredSpreadMarginNotes: "Good demand in 75216 after POF refresh and disclosure review.", targetZipCodes: ["75215", "75216", "75210"], propertyType: "single_family", priceBand: "0-155000", active: true, draftOnly: true }
];

export const buyerDealPriorities: BuyerDealPriority[] = [
  { id: "priority-001", dealId: "deal-001", buyerId: "buyer-001", buyerDemandProfileId: "buyer-demand-001", targetAreaMatch: 100, maxPriceFit: 100, proofOfFundsScore: 100, pastReliabilityScore: 94, closingSpeedScore: 95, dealTypeFit: 100, buyerMarginStrength: 100, priorityScore: 98.34, rank: 1, rankingReasons: ["target_area_match", "max_price_fit", "proof_of_funds_verified", "fast_close", "buyer_margin_strong"], riskFlags: [], recommendedNextStep: "Prepare one-buyer distribution draft for owner review.", draftOnly: true, liveContactAllowed: false, buyerBlastAllowed: false, internalProfitLogicExposed: false },
  { id: "priority-002", dealId: "deal-001", buyerId: "buyer-004", buyerDemandProfileId: "buyer-demand-004", targetAreaMatch: 100, maxPriceFit: 100, proofOfFundsScore: 100, pastReliabilityScore: 88, closingSpeedScore: 86, dealTypeFit: 45, buyerMarginStrength: 100, priorityScore: 90.4, rank: 2, rankingReasons: ["target_area_match", "max_price_fit", "proof_of_funds_verified", "buyer_margin_strong"], riskFlags: ["property_type_fit_review"], recommendedNextStep: "Review property-type fit before buyer response draft.", draftOnly: true, liveContactAllowed: false, buyerBlastAllowed: false, internalProfitLogicExposed: false },
  { id: "priority-003", dealId: "deal-001", buyerId: "buyer-010", buyerDemandProfileId: "buyer-demand-010", targetAreaMatch: 100, maxPriceFit: 25, proofOfFundsScore: 58, pastReliabilityScore: 81, closingSpeedScore: 92, dealTypeFit: 100, buyerMarginStrength: 100, priorityScore: 75.5, rank: 3, rankingReasons: ["target_area_match", "deal_type_fit", "buyer_margin_strong"], riskFlags: ["proof_of_funds_gap", "max_price_gap"], recommendedNextStep: "POF and price fit review required.", draftOnly: true, liveContactAllowed: false, buyerBlastAllowed: false, internalProfitLogicExposed: false },
  { id: "priority-004", dealId: "deal-002", buyerId: "buyer-002", buyerDemandProfileId: "buyer-demand-002", targetAreaMatch: 100, maxPriceFit: 100, proofOfFundsScore: 100, pastReliabilityScore: 91, closingSpeedScore: 100, dealTypeFit: 100, buyerMarginStrength: 86, priorityScore: 97.32, rank: 1, rankingReasons: ["target_area_match", "max_price_fit", "proof_of_funds_verified", "fast_close"], riskFlags: [], recommendedNextStep: "Prepare one-buyer distribution draft for owner review.", draftOnly: true, liveContactAllowed: false, buyerBlastAllowed: false, internalProfitLogicExposed: false },
  { id: "priority-005", dealId: "deal-002", buyerId: "buyer-008", buyerDemandProfileId: "buyer-demand-008", targetAreaMatch: 100, maxPriceFit: 25, proofOfFundsScore: 100, pastReliabilityScore: 83, closingSpeedScore: 98, dealTypeFit: 100, buyerMarginStrength: 86, priorityScore: 82.56, rank: 2, rankingReasons: ["target_area_match", "proof_of_funds_verified", "fast_close"], riskFlags: ["max_price_gap"], recommendedNextStep: "Price capacity blocks distribution until reviewed.", draftOnly: true, liveContactAllowed: false, buyerBlastAllowed: false, internalProfitLogicExposed: false },
  { id: "priority-006", dealId: "deal-003", buyerId: "buyer-003", buyerDemandProfileId: "buyer-demand-003", targetAreaMatch: 100, maxPriceFit: 25, proofOfFundsScore: 58, pastReliabilityScore: 82, closingSpeedScore: 84, dealTypeFit: 100, buyerMarginStrength: 100, priorityScore: 74.42, rank: 1, rankingReasons: ["target_area_match", "deal_type_fit", "buyer_margin_strong"], riskFlags: ["proof_of_funds_gap", "max_price_gap"], recommendedNextStep: "POF refresh required before any buyer response draft.", draftOnly: true, liveContactAllowed: false, buyerBlastAllowed: false, internalProfitLogicExposed: false },
  { id: "priority-007", dealId: "deal-003", buyerId: "buyer-005", buyerDemandProfileId: "buyer-demand-005", targetAreaMatch: 35, maxPriceFit: 100, proofOfFundsScore: 100, pastReliabilityScore: 78, closingSpeedScore: 66, dealTypeFit: 100, buyerMarginStrength: 100, priorityScore: 78.1, rank: 2, rankingReasons: ["max_price_fit", "proof_of_funds_verified", "buyer_margin_strong"], riskFlags: ["target_area_mismatch"], recommendedNextStep: "Area mismatch review before distribution prep.", draftOnly: true, liveContactAllowed: false, buyerBlastAllowed: false, internalProfitLogicExposed: false },
  { id: "priority-008", dealId: "deal-005", buyerId: "buyer-004", buyerDemandProfileId: "buyer-demand-004", targetAreaMatch: 100, maxPriceFit: 100, proofOfFundsScore: 100, pastReliabilityScore: 88, closingSpeedScore: 86, dealTypeFit: 100, buyerMarginStrength: 100, priorityScore: 96.4, rank: 1, rankingReasons: ["target_area_match", "max_price_fit", "proof_of_funds_verified", "buyer_margin_strong"], riskFlags: [], recommendedNextStep: "Hold distribution until compliance clears high-risk publication.", draftOnly: true, liveContactAllowed: false, buyerBlastAllowed: false, internalProfitLogicExposed: false },
  { id: "priority-009", dealId: "deal-005", buyerId: "buyer-005", buyerDemandProfileId: "buyer-demand-005", targetAreaMatch: 35, maxPriceFit: 100, proofOfFundsScore: 100, pastReliabilityScore: 78, closingSpeedScore: 66, dealTypeFit: 100, buyerMarginStrength: 100, priorityScore: 78.1, rank: 2, rankingReasons: ["max_price_fit", "proof_of_funds_verified", "buyer_margin_strong"], riskFlags: ["target_area_mismatch"], recommendedNextStep: "Area mismatch review before distribution prep.", draftOnly: true, liveContactAllowed: false, buyerBlastAllowed: false, internalProfitLogicExposed: false },
  { id: "priority-010", dealId: "deal-006", buyerId: "buyer-006", buyerDemandProfileId: "buyer-demand-006", targetAreaMatch: 35, maxPriceFit: 100, proofOfFundsScore: 100, pastReliabilityScore: 86, closingSpeedScore: 95, dealTypeFit: 100, buyerMarginStrength: 86, priorityScore: 84.42, rank: 1, rankingReasons: ["max_price_fit", "proof_of_funds_verified", "fast_close"], riskFlags: ["target_area_mismatch"], recommendedNextStep: "Review margin exception before distribution prep.", draftOnly: true, liveContactAllowed: false, buyerBlastAllowed: false, internalProfitLogicExposed: false },
  { id: "priority-011", dealId: "deal-006", buyerId: "buyer-010", buyerDemandProfileId: "buyer-demand-010", targetAreaMatch: 35, maxPriceFit: 100, proofOfFundsScore: 58, pastReliabilityScore: 81, closingSpeedScore: 92, dealTypeFit: 100, buyerMarginStrength: 86, priorityScore: 77.34, rank: 2, rankingReasons: ["max_price_fit", "deal_type_fit"], riskFlags: ["target_area_mismatch", "proof_of_funds_gap"], recommendedNextStep: "POF refresh and margin review required.", draftOnly: true, liveContactAllowed: false, buyerBlastAllowed: false, internalProfitLogicExposed: false },
  { id: "priority-012", dealId: "deal-008", buyerId: "buyer-005", buyerDemandProfileId: "buyer-demand-005", targetAreaMatch: 35, maxPriceFit: 100, proofOfFundsScore: 100, pastReliabilityScore: 78, closingSpeedScore: 66, dealTypeFit: 100, buyerMarginStrength: 100, priorityScore: 78.1, rank: 1, rankingReasons: ["max_price_fit", "proof_of_funds_verified", "buyer_margin_strong"], riskFlags: ["target_area_mismatch"], recommendedNextStep: "Compliance and area fit review before draft distribution.", draftOnly: true, liveContactAllowed: false, buyerBlastAllowed: false, internalProfitLogicExposed: false }
];

export const dealDistributionPreps: DealDistributionPrep[] = [
  { id: "distribution-001", dealId: "deal-001", buyerId: "buyer-001", buyerPriorityId: "priority-001", buyerDealPublicationId: "publication-001", buyerDealEmailDraft: "Draft for Jules: Dallas 75216 single-family opportunity with asking price, ARV range, repair estimate range, and access placeholder. Owner review required before any send.", buyerSmsDraft: "Draft only: Dallas 75216 deal sheet ready for owner review. Reply path and send are disabled until approval.", privateDealSheetDraft: sanitizedDistributionSheet("deal-001"), buyerCallNotes: "Prepare one-buyer call note after POF confirmation; no live call placed.", buyerResponseTracker: [{ status: "draft_prepared", operatorReview: "pending", timestamp: "2026-05-04T12:00:00Z" }], approvalStatus: "owner_review_needed", draftStatus: "draft_ready", safetyStatus: "passed", blockedReasons: [], draftOnly: true, liveSendAllowed: false, bulkBlastAllowed: false, sellerPrivateDataExposed: false, assignmentFeeExposed: false, legalClosingGuaranteeAllowed: false },
  { id: "distribution-002", dealId: "deal-002", buyerId: "buyer-002", buyerPriorityId: "priority-004", buyerDealPublicationId: "publication-002", buyerDealEmailDraft: "Draft for Priya: controlled Dallas opportunity with asking price and inspection placeholder. No contract action or title submission.", buyerSmsDraft: "Draft only: 75216 deal sheet can be reviewed after owner approval.", privateDealSheetDraft: sanitizedDistributionSheet("deal-002"), buyerCallNotes: "Buyer is fast-close and POF verified; record interest only after owner review.", buyerResponseTracker: [{ status: "ready_for_owner_review", operatorReview: "pending", timestamp: "2026-05-04T12:15:00Z" }], approvalStatus: "owner_review_needed", draftStatus: "draft_ready", safetyStatus: "passed", blockedReasons: [], draftOnly: true, liveSendAllowed: false, bulkBlastAllowed: false, sellerPrivateDataExposed: false, assignmentFeeExposed: false, legalClosingGuaranteeAllowed: false },
  { id: "distribution-003", dealId: "deal-003", buyerId: "buyer-003", buyerPriorityId: "priority-006", buyerDealPublicationId: "publication-003", buyerDealEmailDraft: "Draft for Marcus: Fort Worth deal sheet with POF refresh reminder and safe access placeholder.", buyerSmsDraft: "Draft only: Fort Worth deal sheet is available after POF refresh and owner review.", privateDealSheetDraft: sanitizedDistributionSheet("deal-003"), buyerCallNotes: "POF refresh blocks priority response; no live outreach.", buyerResponseTracker: [{ status: "pof_needed", operatorReview: "pending", timestamp: "2026-05-04T12:30:00Z" }], approvalStatus: "owner_review_needed", draftStatus: "draft_ready", safetyStatus: "passed", blockedReasons: [], draftOnly: true, liveSendAllowed: false, bulkBlastAllowed: false, sellerPrivateDataExposed: false, assignmentFeeExposed: false, legalClosingGuaranteeAllowed: false },
  { id: "distribution-004", dealId: "deal-005", buyerId: "buyer-004", buyerPriorityId: "priority-008", buyerDealPublicationId: "publication-005", buyerDealEmailDraft: "Draft held: larger Dallas opportunity requires compliance clearance before any buyer-facing deal sheet.", buyerSmsDraft: "Draft only and blocked pending compliance review.", privateDealSheetDraft: sanitizedDistributionSheet("deal-005"), buyerCallNotes: "Strong buyer fit but buyer portal publication is blocked by compliance risk.", buyerResponseTracker: [{ status: "blocked_compliance", operatorReview: "pending", timestamp: "2026-05-04T12:45:00Z" }], approvalStatus: "blocked_compliance_review", draftStatus: "blocked", safetyStatus: "passed", blockedReasons: ["buyer_publication_missing_compliance_review", "buyer_publication_risk_status_high"], draftOnly: true, liveSendAllowed: false, bulkBlastAllowed: false, sellerPrivateDataExposed: false, assignmentFeeExposed: false, legalClosingGuaranteeAllowed: false }
];

export const offerPositioningRecords: OfferPositioningRecord[] = [
  { id: "positioning-001", dealId: "deal-001", offerPacketId: "packet-001", offerStrategyType: "as-is", sellerPainAlignment: ["vacancy", "maintenance", "repair uncertainty"], justificationSummary: { comps: "ARV range supported by nearby renovated single-family sales.", repairs: "Repair basis includes exterior, kitchen, and mechanical reserves.", timeline: "Seller asked for clarity this week and prefers a clean as-is path." }, anchorPrice: 148000, walkAwayPrice: 163000, idealContractPrice: 151000, concessionRange: { low: 1500, high: 4000 }, negotiationNotes: "Lead with repair-backed as-is certainty and keep concessions inside safe max seller offer.", confidenceScore: 91, ownerApprovalRecorded: true, safetyStatus: "passed", blockedReasons: [], draftOnly: true, pressureTacticsAllowed: false, legalAdviceAllowed: false },
  { id: "positioning-002", dealId: "deal-003", offerPacketId: "packet-002", offerStrategyType: "flexible-close", sellerPainAlignment: ["absentee ownership", "tenant turnover", "pricing gap"], justificationSummary: { comps: "ARV range needs seller-friendly explanation with documented repair basis.", repairs: "Cosmetic updates plus possible plumbing reserve.", timeline: "Seller has 30-day timeline and is price-focused." }, anchorPrice: 176000, walkAwayPrice: 195000, idealContractPrice: 180000, concessionRange: { low: 2500, high: 6000 }, negotiationNotes: "Use flexible close as value; owner approval still required before conversion.", confidenceScore: 82, ownerApprovalRecorded: false, safetyStatus: "passed", blockedReasons: [], draftOnly: true, pressureTacticsAllowed: false, legalAdviceAllowed: false },
  { id: "positioning-003", dealId: "deal-005", offerPacketId: "packet-003", offerStrategyType: "investor-grade", sellerPainAlignment: ["inherited property", "authority review", "larger repair scope"], justificationSummary: { comps: "Higher ARV requires authority and compliance review before conversion.", repairs: "Large repair reserve protects buyer margin.", timeline: "Seller is open but review blockers remain." }, anchorPrice: 214000, walkAwayPrice: 235000, idealContractPrice: 220000, concessionRange: { low: 3000, high: 7000 }, negotiationNotes: "Do not convert until compliance authority review clears.", confidenceScore: 74, ownerApprovalRecorded: true, safetyStatus: "passed", blockedReasons: [], draftOnly: true, pressureTacticsAllowed: false, legalAdviceAllowed: false },
  { id: "positioning-004", dealId: "deal-006", offerPacketId: "packet-004", offerStrategyType: "cash-fast", sellerPainAlignment: ["repair burden", "uncertain pricing"], justificationSummary: { comps: "ARV needs repair validation before price movement.", repairs: "High repair estimate compresses safe offer range.", timeline: "Timeline not stable enough for conversion." }, anchorPrice: 124000, walkAwayPrice: 128000, idealContractPrice: 126000, concessionRange: { low: 0, high: 2000 }, negotiationNotes: "Hold position or disengage because profit control is below target.", confidenceScore: 48, ownerApprovalRecorded: true, safetyStatus: "passed", blockedReasons: [], draftOnly: true, pressureTacticsAllowed: false, legalAdviceAllowed: false },
  { id: "positioning-005", dealId: "deal-007", offerPacketId: "packet-005", offerStrategyType: "cash-fast", sellerPainAlignment: ["small property", "fast answer preference"], justificationSummary: { comps: "Small single-family spread is below target but may be useful for practice queue.", repairs: "Repair reserve leaves limited assignment room.", timeline: "Seller has not stabilized response yet." }, anchorPrice: 72000, walkAwayPrice: 82000, idealContractPrice: 75000, concessionRange: { low: 500, high: 1500 }, negotiationNotes: "Use as follow-up candidate only; conversion is blocked by target assignment fee.", confidenceScore: 58, ownerApprovalRecorded: true, safetyStatus: "passed", blockedReasons: [], draftOnly: true, pressureTacticsAllowed: false, legalAdviceAllowed: false }
];

export const negotiationRecords: NegotiationRecord[] = [
  { id: "negotiation-001", dealId: "deal-001", offerPositioningId: "positioning-001", sellerInteractionId: "seller-interaction-001", sellerLastResponse: "Seller said the as-is explanation makes sense and asked for the written next-step checklist.", sellerObjections: ["wants clear repair basis"], counterOffer: 153000, emotionalSignals: ["motivated", "timeline-driven"], negotiationStage: "soft-accepted", nextMoveRecommendation: "Move to verbal agreement after owner confirms the final external drafting path.", motivationScore: 92, priceAlignment: 90, timelineAlignment: 88, trustLevel: 86, objectionResolution: 86, contactConsistency: 90, readinessScore: 88.92, readinessLevel: "contract-ready", safetyStatus: "passed", blockedReasons: [], draftOnly: true, automaticAcceptanceAllowed: false, liveNegotiationAutomationAllowed: false, pressureTacticsAllowed: false, legalAdviceAllowed: false },
  { id: "negotiation-002", dealId: "deal-003", offerPositioningId: "positioning-002", sellerInteractionId: "seller-interaction-003", sellerLastResponse: "Seller is open to reviewing the repair-backed price but wants a higher number.", sellerObjections: ["price expectation"], counterOffer: 190000, emotionalSignals: ["price-focused", "hesitant"], negotiationStage: "negotiating", nextMoveRecommendation: "Adjust price within safe range only after owner review.", motivationScore: 78, priceAlignment: 72, timelineAlignment: 70, trustLevel: 76, objectionResolution: 68, contactConsistency: 78, readinessScore: 73.8, readinessLevel: "medium readiness", safetyStatus: "passed", blockedReasons: [], draftOnly: true, automaticAcceptanceAllowed: false, liveNegotiationAutomationAllowed: false, pressureTacticsAllowed: false, legalAdviceAllowed: false },
  { id: "negotiation-003", dealId: "deal-005", offerPositioningId: "positioning-003", sellerInteractionId: "seller-interaction-004", sellerLastResponse: "Seller likes the number but authority documents are still unresolved.", sellerObjections: ["authority documentation", "title review"], counterOffer: 224000, emotionalSignals: ["motivated", "hesitant"], negotiationStage: "verbally accepted", nextMoveRecommendation: "Resolve compliance blocker before any contract-ready marking.", motivationScore: 88, priceAlignment: 84, timelineAlignment: 82, trustLevel: 80, objectionResolution: 62, contactConsistency: 82, readinessScore: 80.6, readinessLevel: "high readiness", safetyStatus: "passed", blockedReasons: [], draftOnly: true, automaticAcceptanceAllowed: false, liveNegotiationAutomationAllowed: false, pressureTacticsAllowed: false, legalAdviceAllowed: false },
  { id: "negotiation-004", dealId: "deal-006", offerPositioningId: "positioning-004", sellerInteractionId: "seller-interaction-006", sellerLastResponse: "Seller stopped responding after the repair range was discussed.", sellerObjections: ["price expectation", "repair disagreement"], counterOffer: 145000, emotionalSignals: ["stalled", "price-focused"], negotiationStage: "stalled", nextMoveRecommendation: "Disengage unless price moves back inside safe range.", motivationScore: 52, priceAlignment: 35, timelineAlignment: 44, trustLevel: 50, objectionResolution: 30, contactConsistency: 38, readinessScore: 42.72, readinessLevel: "low readiness", safetyStatus: "passed", blockedReasons: [], draftOnly: true, automaticAcceptanceAllowed: false, liveNegotiationAutomationAllowed: false, pressureTacticsAllowed: false, legalAdviceAllowed: false },
  { id: "negotiation-005", dealId: "deal-007", offerPositioningId: "positioning-005", sellerInteractionId: "seller-interaction-005", sellerLastResponse: "Seller asked for a higher offer and has not confirmed timeline.", sellerObjections: ["price expectation", "timeline unknown"], counterOffer: 84000, emotionalSignals: ["hesitant"], negotiationStage: "follow-up", nextMoveRecommendation: "Hold position and explain repair basis without pressure.", motivationScore: 68, priceAlignment: 58, timelineAlignment: 54, trustLevel: 64, objectionResolution: 52, contactConsistency: 66, readinessScore: 60.28, readinessLevel: "medium readiness", safetyStatus: "passed", blockedReasons: [], draftOnly: true, automaticAcceptanceAllowed: false, liveNegotiationAutomationAllowed: false, pressureTacticsAllowed: false, legalAdviceAllowed: false }
];

export const contractReadyStates: ContractReadyState[] = [
  { id: "contract-ready-001", dealId: "deal-001", offerPositioningId: "positioning-001", negotiationRecordId: "negotiation-001", readinessStatus: "contract_ready", contractReady: true, readyForExternalDrafting: true, sellerLikelyToSign: true, numbersLocked: true, negotiationStabilized: true, underwritingComplete: true, profitControlValidated: true, buyerDemandConfirmed: true, compliancePassed: true, noRiskFlags: true, sellerReadinessHigh: true, ownerApprovalRecorded: true, blockedReasons: [], fastestPathToContract: ["move to verbal agreement", "prepare external attorney/title drafting request"], projectedAssignmentFee: 15000, draftOnly: true, externalAttorneyTitleDraftingRequired: true, executableContractGenerated: false, contractExecutionAllowed: false, legalAdviceProvided: false, automaticAcceptanceAllowed: false, liveNegotiationAutomationAllowed: false },
  { id: "contract-ready-002", dealId: "deal-003", offerPositioningId: "positioning-002", negotiationRecordId: "negotiation-002", readinessStatus: "blocked", contractReady: false, readyForExternalDrafting: false, sellerLikelyToSign: false, numbersLocked: true, negotiationStabilized: false, underwritingComplete: true, profitControlValidated: false, buyerDemandConfirmed: false, compliancePassed: true, noRiskFlags: true, sellerReadinessHigh: false, ownerApprovalRecorded: false, blockedReasons: ["owner_approval_not_recorded", "buyer_demand_not_confirmed", "seller_readiness_not_high", "profit_control_not_validated"], fastestPathToContract: ["handle objection X", "adjust price within safe range", "confirm buyer demand before contract-ready state", "request owner approval review"], projectedAssignmentFee: 13000, draftOnly: true, externalAttorneyTitleDraftingRequired: true, executableContractGenerated: false, contractExecutionAllowed: false, legalAdviceProvided: false, automaticAcceptanceAllowed: false, liveNegotiationAutomationAllowed: false },
  { id: "contract-ready-003", dealId: "deal-005", offerPositioningId: "positioning-003", negotiationRecordId: "negotiation-003", readinessStatus: "blocked", contractReady: false, readyForExternalDrafting: false, sellerLikelyToSign: true, numbersLocked: false, negotiationStabilized: true, underwritingComplete: true, profitControlValidated: false, buyerDemandConfirmed: true, compliancePassed: false, noRiskFlags: false, sellerReadinessHigh: true, ownerApprovalRecorded: true, blockedReasons: ["compliance_not_passed", "risk_flags_present", "profit_control_not_validated"], fastestPathToContract: ["resolve compliance blocker", "disengage"], projectedAssignmentFee: 15000, draftOnly: true, externalAttorneyTitleDraftingRequired: true, executableContractGenerated: false, contractExecutionAllowed: false, legalAdviceProvided: false, automaticAcceptanceAllowed: false, liveNegotiationAutomationAllowed: false },
  { id: "contract-ready-004", dealId: "deal-006", offerPositioningId: "positioning-004", negotiationRecordId: "negotiation-004", readinessStatus: "blocked", contractReady: false, readyForExternalDrafting: false, sellerLikelyToSign: false, numbersLocked: false, negotiationStabilized: false, underwritingComplete: true, profitControlValidated: false, buyerDemandConfirmed: false, compliancePassed: true, noRiskFlags: false, sellerReadinessHigh: false, ownerApprovalRecorded: true, blockedReasons: ["profit_control_not_validated", "buyer_demand_not_confirmed", "risk_flags_present", "seller_readiness_not_high"], fastestPathToContract: ["send updated offer explanation", "confirm buyer demand before contract-ready state", "disengage"], projectedAssignmentFee: 8000, draftOnly: true, externalAttorneyTitleDraftingRequired: true, executableContractGenerated: false, contractExecutionAllowed: false, legalAdviceProvided: false, automaticAcceptanceAllowed: false, liveNegotiationAutomationAllowed: false },
  { id: "contract-ready-005", dealId: "deal-007", offerPositioningId: "positioning-005", negotiationRecordId: "negotiation-005", readinessStatus: "blocked", contractReady: false, readyForExternalDrafting: false, sellerLikelyToSign: false, numbersLocked: false, negotiationStabilized: false, underwritingComplete: true, profitControlValidated: false, buyerDemandConfirmed: false, compliancePassed: true, noRiskFlags: false, sellerReadinessHigh: false, ownerApprovalRecorded: true, blockedReasons: ["profit_control_not_validated", "buyer_demand_not_confirmed", "risk_flags_present", "seller_readiness_not_high"], fastestPathToContract: ["handle objection X", "adjust price within safe range", "confirm buyer demand before contract-ready state", "disengage"], projectedAssignmentFee: 9000, draftOnly: true, externalAttorneyTitleDraftingRequired: true, executableContractGenerated: false, contractExecutionAllowed: false, legalAdviceProvided: false, automaticAcceptanceAllowed: false, liveNegotiationAutomationAllowed: false }
];

export const money = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0
});

export function formatCurrency(value: number) {
  return money.format(value);
}

export function getLead(id: string) {
  return leads.find((lead) => lead.id === id);
}

export function getDeal(id: string) {
  return deals.find((deal) => deal.id === id);
}

export function getBuyer(id: string) {
  return buyers.find((buyer) => buyer.id === id);
}

export function getDivision(id: string) {
  return divisions.find((division) => division.id === id);
}

export function getAgent(id: string) {
  return agents.find((agent) => agent.id === id);
}

export function getBuyerPublication(dealId: string) {
  return buyerPublications.find((publication) => publication.dealId === dealId);
}

export function getSellerInteraction(leadId: string) {
  return sellerInteractions.find((interaction) => interaction.leadId === leadId);
}

export function getOfferPacket(packetId: string) {
  return offerPackets.find((packet) => packet.id === packetId);
}

export function getOfferPacketByDeal(dealId: string) {
  return offerPackets.find((packet) => packet.dealId === dealId);
}

export function getContractControl(contractId: string) {
  return contractControls.find((contract) => contract.id === contractId);
}

export function getContractControlByDeal(dealId: string) {
  return contractControls.find((contract) => contract.dealId === dealId);
}

export function getTitleHandoffPacket(packetId: string) {
  return titleHandoffPackets.find((packet) => packet.id === packetId);
}

export function getTitleReviewCoordination(reviewId: string) {
  return titleReviewCoordinations.find((record) => record.id === reviewId);
}

export function getTitleReviewCoordinationByDeal(dealId: string) {
  return titleReviewCoordinations.find((record) => record.dealId === dealId);
}

export function getReviewPacketPrep(packetId: string) {
  return reviewPacketPreps.find((packet) => packet.id === packetId);
}

export function getReviewPacketPrepByReview(reviewId: string) {
  return reviewPacketPreps.find((packet) => packet.titleReviewCoordinationId === reviewId);
}

export function getAssignmentReadinessRecord(recordId: string) {
  return assignmentReadinessRecords.find((record) => record.id === recordId);
}

export function getCommunicationDraft(draftId: string) {
  return communicationDrafts.find((draft) => draft.id === draftId);
}

export function getCommunicationDryRun(receiptId: string) {
  return communicationDryRunReceipts.find((receipt) => receipt.id === receiptId);
}

export function getCommunicationApproval(approvalId: string) {
  return communicationApprovals.find((approval) => approval.id === approvalId);
}

export function getSellerOfferPublication(offerId: string) {
  return sellerOfferPublications.find((offer) => offer.id === offerId);
}

export function sellerOfferBlockReasons(publication: SellerOfferPublication) {
  const packet = getOfferPacket(publication.offerPacketId);
  const contract = getContractControl(publication.contractControlId);
  const reasons: string[] = [];
  if (!publication.portalVisibilityEnabled) reasons.push("portal_visibility_not_enabled");
  if (!packet?.packetPrepAllowed || packet.approvalStatus !== "owner_approved_draft_ready") reasons.push("offer_packet_not_approved");
  if (!publication.complianceCheckPassed || !packet?.complianceGuardPassed || contract?.complianceReviewStatus !== "approved") reasons.push("compliance_check_not_passed");
  if (!publication.ownerApprovalRecorded || !packet?.ownerApprovalRecorded || contract?.ownerApprovalStatus !== "approved") reasons.push("owner_approval_not_recorded");
  if (!contract?.contractPrepAllowed || !["prep_review", "draft_prep_ready", "controlled_review", "seller_terms_recorded"].includes(contract?.contractStatus ?? "")) reasons.push("contract_control_status_not_valid");
  if (!publication.offerLanguageSafetyPassed) reasons.push("offer_language_safety_not_passed");
  if (publication.contractExecutionAllowed) reasons.push("contract_execution_enabled");
  if (publication.liveNegotiationAutomationAllowed) reasons.push("live_negotiation_automation_enabled");
  if (publication.legalAdviceProvided) reasons.push("legal_advice_flagged");
  if (publication.buyerDataExposed) reasons.push("buyer_data_exposed");
  if (publication.internalProfitLogicExposed) reasons.push("internal_profit_logic_exposed");
  return [...new Set(reasons)].sort();
}

export function isSellerVisible(publication: SellerOfferPublication) {
  return sellerOfferBlockReasons(publication).length === 0;
}

export function sanitizeSellerOffer(publication: SellerOfferPublication): SellerPortalOffer {
  const lead = getLead(publication.leadId);
  if (!lead || !isSellerVisible(publication)) {
    throw new Error("Offer is not seller-visible.");
  }
  return {
    offerId: publication.id,
    propertyAddressSummary: `${lead.address}, ${lead.city}, ${lead.state} ${lead.zipCode}`,
    offerStatus: publication.offerStatus,
    offerAmount: publication.offerAmount,
    closingTimelineEstimate: publication.closingTimelineEstimate,
    inspectionAccessNextStep: publication.inspectionAccessNextStep,
    titleCompanyReviewStatus: publication.titleCompanyReviewStatus,
    documentChecklist: publication.documentChecklist,
    ownerOperatorContactPlaceholder: publication.operatorContactPlaceholder,
    sellerQuestionsNotesAction: {
      type: "draft_intake_only",
      operatorReviewRequired: true,
      automaticNegotiationAllowed: false,
      offerAcceptanceExecutionAllowed: false,
      documentUploadIsPlaceholder: true
    },
    portalVisibilityStatus: "visible"
  };
}

export function sellerDrafts(lead: Lead, interaction?: SellerInteraction) {
  return {
    callScriptDraft: `Confirm the ${lead.city}, ${lead.state} property details, ask what changed for the seller, listen for timeline and condition, then explain that any offer needs owner review.`,
    smsDraft: `Hi ${lead.sellerName}, this is a draft note for owner review. I wanted to follow up on the property and see if it still makes sense to discuss a possible as-is offer.`,
    emailDraft: `Subject: Property follow-up\n\nThis is a draft for owner review. Before any offer is discussed, we would verify condition, timeline, and repair assumptions.`,
    objectionResponseDraft: "Acknowledge the concern, avoid pressure, and explain that price depends on verified ARV, repairs, costs, and buyer margin.",
    offerExplanationDraft: `Current asking reference is ${formatCurrency(interaction?.askingPrice ?? lead.askingPrice)}. Any offer packet must pass underwriting, compliance, and owner approval gates.`,
    followUpSequenceDraft: ["Owner reviews notes", "Draft check-in on condition and timeline", "Draft offer-basis explanation", "Draft close-the-loop note"],
    draftOnly: true,
    liveOutreachAllowed: false
  };
}

export function buyerPortalBlockReasons(publication: BuyerPublication) {
  const deal = getDeal(publication.dealId);
  const reasons: string[] = [];
  if (!deal) reasons.push("missing_internal_deal");
  if (!publication.operatorMarkedVisible) reasons.push("operator_has_not_marked_buyer_visible");
  if (!deal?.arv || publication.arvRange.low === null || publication.arvRange.high === null) reasons.push("missing_arv");
  if (!deal?.repairs || publication.repairEstimateRange.low === null || publication.repairEstimateRange.high === null) reasons.push("missing_repair_estimate");
  if (!publication.askingPrice) reasons.push("missing_asking_price");
  if (!publication.complianceReviewed) reasons.push("missing_compliance_review");
  if (!publication.sellerContractControlled) reasons.push("seller_contract_not_marked_controlled");
  if (publication.riskStatus === "high" || (deal?.riskScore ?? 0) >= 45) reasons.push("risk_status_high");
  if (!publication.estimatedBuyerMargin || publication.estimatedBuyerMargin < 25000 || publication.buyerMarginStatus === "weak") reasons.push("buyer_margin_weak");
  return [...new Set(reasons)].sort();
}

export function isBuyerVisible(publication: BuyerPublication) {
  return buyerPortalBlockReasons(publication).length === 0;
}

export function sanitizeBuyerDeal(publication: BuyerPublication, buyer: Buyer = buyers[0]): BuyerPortalDeal {
  const deal = getDeal(publication.dealId);
  const lead = deal ? getLead(deal.leadId) : undefined;
  if (!deal || !lead || !isBuyerVisible(publication)) {
    throw new Error("Deal is not buyer-visible.");
  }
  return {
    dealId: deal.id,
    city: lead.city,
    state: lead.state,
    zipCode: lead.zipCode,
    propertyType: lead.propertyType,
    beds: publication.beds,
    baths: publication.baths,
    sqft: publication.sqft,
    arvRange: publication.arvRange,
    repairEstimateRange: publication.repairEstimateRange,
    askingPrice: publication.askingPrice,
    estimatedBuyerMargin: publication.estimatedBuyerMargin,
    photosPlaceholder: publication.photosPlaceholder,
    accessInstructionsPlaceholder: publication.accessInstructionsPlaceholder,
    proofOfFundsStatus: buyer.proofOfFundsStatus,
    availabilityStatus: publication.availabilityStatus,
    offerInterestAction: {
      type: "draft_intent_only",
      contractExecutionAllowed: false,
      paymentCollectionAllowed: false
    }
  };
}

export const hotDeals = deals.filter((deal) => deal.hot);
export const underContractDeals = deals.filter((deal) => deal.underContract);
export const projectedAssignmentTotal = deals.reduce(
  (total, deal) => total + deal.projectedAssignmentFee,
  0
);
export const buyerVisibleDeals = buyerPublications
  .filter(isBuyerVisible)
  .map((publication) => sanitizeBuyerDeal(publication));
export const buyerPortalBlockedDeals = buyerPublications
  .filter((publication) => !isBuyerVisible(publication))
  .map((publication) => ({
    dealId: publication.dealId,
    blockedReasons: buyerPortalBlockReasons(publication)
  }));
export const hotSellerLeads = leads.filter((lead) => {
  const interaction = getSellerInteraction(lead.id);
  return lead.opportunityScore >= 80 || (interaction?.sellerTemperatureScore ?? 0) >= 80;
});
export const staleSellerFollowUps = sellerInteractions.filter(
  (interaction) => interaction.nextFollowUpDate < "2026-05-04"
);
export const offerNeededLeads = leads.filter((lead) => lead.stage === "offer_needed");
export const negotiationStageLeads = leads.filter((lead) => lead.stage === "negotiating");
export const underContractCandidates = leads.filter(
  (lead) => ["offer_sent", "negotiating"].includes(lead.stage) && lead.opportunityScore >= 72
);
export const offerReadyPackets = offerPackets.filter((packet) => packet.packetPrepAllowed);
export const contractPrepReady = contractControls.filter((contract) => contract.contractPrepAllowed);
export const contractPrepBlocked = contractControls.filter((contract) => !contract.contractPrepAllowed);
export const assignmentReadyRecords = assignmentReadinessRecords.filter(
  (record) => record.assignmentReady
);
export const blockedAssignmentReadiness = assignmentReadinessRecords.filter(
  (record) => !record.assignmentReady
);
export const buyerPofGaps = assignmentReadinessRecords.filter(
  (record) => record.buyerPofStatus !== "verified"
);
export const communicationDraftsNeedingSafety = communicationDrafts.filter(
  (draft) => !draft.safetyChecked
);
export const communicationDryRunsNeedingApproval = communicationDryRunReceipts.filter(
  (receipt) =>
    receipt.safetyResult.allowed &&
    !communicationApprovals.some(
      (approval) => approval.dryRunReceiptId === receipt.id && approval.ownerApprovalRecorded
    )
);
export const blockedCommunicationAttempts = communicationSendAttempts.filter(
  (attempt) => attempt.attemptStatus === "blocked"
);
export const sentOrMockSentCommunicationAttempts = communicationSendAttempts.filter(
  (attempt) => ["sent", "mock_sent"].includes(attempt.attemptStatus)
);
export const communicationRiskQueue = communicationDrafts.filter(
  (draft) => draft.riskStatus === "blocked" || draft.blockedReasons.length > 0
);
export const sellerVisibleOffers = sellerOfferPublications
  .filter(isSellerVisible)
  .map((publication) => sanitizeSellerOffer(publication));
export const blockedSellerVisibilityOffers = sellerOfferPublications
  .filter((publication) => !isSellerVisible(publication))
  .map((publication) => ({
    offerId: publication.id,
    dealId: publication.dealId,
    blockedReasons: sellerOfferBlockReasons(publication)
  }));
export const sellerPortalQuestions = sellerPortalResponses.filter(
  (response) => response.responseType === "offer_question"
);
export const sellerDocumentChecklistQueue = sellerOfferPublications.filter(
  (publication) => publication.documentChecklist.length > 0
);
export const sellerResponseQueue = sellerPortalResponses.filter(
  (response) => response.operatorReviewStatus !== "reviewed"
);
export const activeDealRooms = unifiedDealRooms;
export const closingReadyDealRooms = unifiedDealRooms.filter(
  (room) => room.coordinationStatus === "closing_ready"
);
export const blockedDealRooms = unifiedDealRooms.filter(
  (room) => room.coordinationStatus !== "closing_ready"
);
export const assignmentReadyDealRooms = unifiedDealRooms.filter(
  (room) => room.assignmentReadinessStatus === "assignment_ready"
);
export const projectedAssignmentFeesAtRisk = blockedDealRooms.reduce(
  (total, room) => total + room.projectedAssignmentFeeAtRisk,
  0
);
export const closingNextBestActions = unifiedDealRooms.flatMap((room) =>
  room.nextRequiredActions.map((action) => ({
    dealRoomId: room.id,
    dealId: room.dealId,
    action,
    recommendationOnly: true,
    legalExecutionAllowed: false,
    titleSubmissionAllowed: false,
    paymentHandlingAllowed: false,
    automaticNegotiationAllowed: false
  }))
);

export function getUnifiedDealRoom(id: string) {
  return unifiedDealRooms.find((room) => room.id === id);
}

export function getUnifiedDealRoomByDeal(dealId: string) {
  return unifiedDealRooms.find((room) => room.dealId === dealId);
}

export function getClosingCoordinationChecklist(dealRoomId: string) {
  return closingCoordinationChecklists.find((checklist) => checklist.dealRoomId === dealRoomId);
}

export function getDealRoomBlockers(dealRoomId: string) {
  return dealRoomBlockers.filter((blocker) => blocker.dealRoomId === dealRoomId);
}

export function getDealEvidencePacket(packetId: string) {
  return dealEvidencePackets.find((packet) => packet.id === packetId);
}

export function getDealEvidencePacketByRoom(dealRoomId: string) {
  return dealEvidencePackets.find((packet) => packet.dealRoomId === dealRoomId);
}

export function getAssignmentFeeAttribution(feeId: string) {
  return assignmentFeeAttributions.find((fee) => fee.id === feeId);
}

export function getAssignmentFeeAttributionByPacket(packetId: string) {
  return assignmentFeeAttributions.find((fee) => fee.evidencePacketId === packetId);
}

export const projectedEvidenceAssignmentFees = assignmentFeeAttributions.reduce(
  (total, fee) => total + fee.projectedAssignmentFee,
  0
);
export const verifiedAssignmentFees = assignmentFeeAttributions
  .filter((fee) => fee.verificationStatus === "verified")
  .reduce((total, fee) => total + fee.projectedAssignmentFee, 0);
export const evidenceFeesAtRisk = assignmentFeeAttributions
  .filter((fee) => fee.verificationStatus !== "verified" && fee.projectedAssignmentFee > 0)
  .reduce((total, fee) => total + fee.projectedAssignmentFee, 0);
export const missingEvidencePackets = dealEvidencePackets.filter(
  (packet) =>
    !packet.sourceRecordsPresent ||
    packet.evidenceStatus === "blocked_missing_evidence" ||
    packet.unsupportedProfitClaims.length > 0
);
export const dealsNeedingEvidenceOwnerReview = dealEvidencePackets.filter(
  (packet) => packet.evidenceStatus === "owner_review_needed" || packet.ownerReviewStatus !== "owner_approved"
);
export const verified10kAssignmentFeeOpportunities = assignmentFeeAttributions.filter(
  (fee) =>
    fee.verified10kOpportunity &&
    fee.projectedAssignmentFee === fee.buyerPurchasePrice - fee.sellerContractPrice
);

export function getBuyerDemandProfile(buyerId: string) {
  return buyerDemandProfiles.find((profile) => profile.buyerId === buyerId || profile.id === buyerId);
}

export function getBuyerDealPriority(priorityId: string) {
  return buyerDealPriorities.find((priority) => priority.id === priorityId);
}

export function getBuyerDealPrioritiesForDeal(dealId: string) {
  return buyerDealPriorities
    .filter((priority) => priority.dealId === dealId)
    .sort((first, second) => first.rank - second.rank);
}

export function getDealDistributionPrep(distributionId: string) {
  return dealDistributionPreps.find((prep) => prep.id === distributionId);
}

export function getDealDistributionPrepsForBuyer(buyerId: string) {
  return dealDistributionPreps.filter((prep) => prep.buyerId === buyerId);
}

export const highestDemandZipCodes = Object.values(
  buyerDemandProfiles.reduce<Record<string, { zipCode: string; demandScore: number; buyerCount: number }>>(
    (acc, profile) => {
      profile.targetZipCodes.forEach((zipCode) => {
        const current = acc[zipCode] ?? { zipCode, demandScore: 0, buyerCount: 0 };
        current.demandScore += profile.zipCodeDemandScore;
        current.buyerCount += 1;
        acc[zipCode] = current;
      });
      return acc;
    },
    {}
  )
)
  .map((item) => ({ ...item, demandScore: Math.round(item.demandScore / item.buyerCount) }))
  .sort((first, second) => second.demandScore - first.demandScore || second.buyerCount - first.buyerCount);

export const bestBuyersForHotDeals = hotDeals
  .map((deal) => {
    const priority = getBuyerDealPrioritiesForDeal(deal.id)[0];
    return priority ? { deal, priority, buyer: getBuyer(priority.buyerId) } : null;
  })
  .filter((item): item is { deal: Deal; priority: BuyerDealPriority; buyer: Buyer | undefined } => Boolean(item));

export const distributionDraftsPendingApproval = dealDistributionPreps.filter(
  (prep) => prep.approvalStatus !== "owner_approved"
);

export const fastCloseBuyerList = buyerDemandProfiles
  .map((profile) => ({ profile, buyer: getBuyer(profile.buyerId) }))
  .filter((item) => item.buyer?.proofOfFundsStatus === "verified" && (item.buyer?.closingSpeedDays ?? 99) <= 10)
  .sort(
    (first, second) =>
      (first.buyer?.closingSpeedDays ?? 99) - (second.buyer?.closingSpeedDays ?? 99) ||
      second.profile.reliabilityScore - first.profile.reliabilityScore
  );

export const buyerPriorityPofGaps = buyerDealPriorities.filter((priority) => {
  const buyer = getBuyer(priority.buyerId);
  return buyer?.proofOfFundsStatus !== "verified";
});

export const buyerReadyDealsFromDemand = bestBuyersForHotDeals.filter(
  ({ priority, buyer }) =>
    priority.priorityScore >= 85 &&
    buyer?.proofOfFundsStatus === "verified" &&
    getBuyerPublication(priority.dealId)?.availabilityStatus === "available"
);

export const tenKDealsWithStrongBuyerDemand = bestBuyersForHotDeals.filter(
  ({ deal, priority }) =>
    deal.projectedAssignmentFee >= 10000 &&
    priority.priorityScore >= 85 &&
    priority.riskFlags.length === 0
);

export const blockedDistributionPreps = dealDistributionPreps.filter(
  (prep) => prep.blockedReasons.length > 0 || prep.draftStatus === "blocked"
);

export function getOfferPositioningRecord(positioningId: string) {
  return offerPositioningRecords.find((record) => record.id === positioningId);
}

export function getOfferPositioningByDeal(dealId: string) {
  return offerPositioningRecords.find((record) => record.dealId === dealId);
}

export function getNegotiationRecord(recordId: string) {
  return negotiationRecords.find((record) => record.id === recordId);
}

export function getNegotiationByDeal(dealId: string) {
  return negotiationRecords.find((record) => record.dealId === dealId);
}

export function getContractReadyStateByDeal(dealId: string) {
  return contractReadyStates.find((state) => state.dealId === dealId);
}

export const contractReadyDeals = contractReadyStates.filter((state) => state.contractReady);
export const highReadinessNegotiations = negotiationRecords.filter((record) =>
  ["high readiness", "contract-ready"].includes(record.readinessLevel)
);
export const stalledNegotiations = negotiationRecords.filter(
  (record) => record.negotiationStage === "stalled"
);
export const dealsNeedingPriceAdjustment = negotiationRecords.filter(
  (record) =>
    record.counterOffer !== null &&
    record.sellerObjections.some((objection) => objection.includes("price"))
);
export const offerConversionDealsAtRisk = contractReadyStates.filter(
  (state) => state.blockedReasons.length > 0
);
export const fastestPathToContract = contractReadyStates.map((state) => ({
  dealId: state.dealId,
  stateId: state.id,
  actions: state.fastestPathToContract,
  blockedReasons: state.blockedReasons
}));
export const projected10kContractsReady = contractReadyDeals.filter((state) => {
  return state.projectedAssignmentFee >= 10000;
});

export const titleReviewReadyRecords = titleReviewCoordinations.filter(
  (record) => record.packetPrepAllowed
);
export const blockedTitleReviewCoordinations = titleReviewCoordinations.filter(
  (record) => !record.packetPrepAllowed || record.blockedReasons.length > 0
);
export const reviewPacketPrepReady = reviewPacketPreps.filter((packet) => packet.prepAllowed);
export const reviewPacketBlocks = reviewPacketPreps.filter(
  (packet) => !packet.prepAllowed || packet.blockedReasons.length > 0
);
export const titleReviewMissingItems = titleReviewCoordinations.filter(
  (record) => record.missingItems.length > 0
);
export const titleReviewOwnerApprovalNeeded = titleReviewCoordinations.filter(
  (record) => record.ownerApprovalStatus !== "approved"
);

export const autonomyEnabledRules = automationRules.filter((rule) => rule.enabled);
export const autonomyLevel4Rules = automationRules.filter((rule) => rule.autonomyLevel === 4);
export const autonomyLevel5Disabled = automationRules.every((rule) => rule.level5Disabled);
export const blockedAutomationAttempts = automationAttempts.filter(
  (attempt) => attempt.attemptStatus === "blocked" || attempt.blockedReasons.length > 0
);
export const autonomousLiveOutreachBlocks = blockedAutomationAttempts.filter((attempt) =>
  ["send_sms", "send_email", "call_seller", "contact_buyer", "buyer_blast_execute", "bulk_send"].includes(attempt.actionType)
);
export const autonomyOpenTasks = autonomousAgentTasks.filter(
  (task) => task.status !== "completed"
);
export const autonomyDraftTasks = autonomousAgentTasks.filter((task) =>
  ["follow_up_draft", "buyer_distribution_draft", "offer_packet_draft", "daily_briefing"].includes(task.taskType)
);
export const autonomyOwnerApprovalTasks = autonomousAgentTasks.filter(
  (task) => task.ownerApprovalRequired
);
export const autonomyEscalationQueue = autonomyEscalations.filter(
  (escalation) => escalation.status === "open"
);
export const autonomyCriticalEscalations = autonomyEscalationQueue.filter(
  (escalation) => escalation.severity === "critical"
);
export const latestAutonomyDailyBriefing = dailyCommandBriefings[0];
export const autonomySafetyBoundaryCards = [
  { label: "Live outreach", value: "off", detail: `${autonomousLiveOutreachBlocks.length} blocked attempts recorded` },
  { label: "Portal publishing", value: "off", detail: "Buyer/seller portal visibility remains operator-gated" },
  { label: "Contracts/title", value: "off", detail: "No execution, no title submission, no review packet send" },
  { label: "Level 5", value: "disabled", detail: autonomyLevel5Disabled ? "Unavailable in V12" : "Review configuration" }
];

export const approvedAutoExecutionRules = autoExecutionRules.filter(
  (rule) => rule.status === "approved" && rule.ownerApprovalStatus === "approved"
);
export const approvedTemplateLibrary = approvedTemplates.filter((template) => template.approved);
export const blockedAutoExecutionRules = autoExecutionRules.filter(
  (rule) => rule.status !== "approved" || rule.blockedReasons.length > 0
);
export const autoExecutionBlockedAttempts = autoExecutionAttempts.filter(
  (attempt) => attempt.attemptStatus === "blocked" || attempt.blockedReasons.length > 0
);
export const autoExecutionMockSentAttempts = autoExecutionAttempts.filter(
  (attempt) => attempt.attemptStatus === "mock_sent"
);
export const autoExecutionDryRunBlocks = autoExecutionDryRuns.filter(
  (dryRun) => !dryRun.safetyPassed || dryRun.riskStatus === "blocked"
);
export const autoExecutionAuditTrail = autoExecutionAuditRecords;
export const autoExecutionSafetyCards = [
  { label: "Approved rules", value: String(approvedAutoExecutionRules.length), detail: "Rule and owner approval required" },
  { label: "Approved templates", value: String(approvedTemplateLibrary.length), detail: "Template safety required" },
  { label: "Blocked attempts", value: String(autoExecutionBlockedAttempts.length), detail: "Bulk/blast/unsafe paths audited" },
  { label: "Bulk send", value: "off", detail: "Single recipient only" }
];

export function getBuyerAccelerationRecordByDeal(dealId: string) {
  return buyerAccelerationRecords.find((record) => record.dealId === dealId);
}

export function getBuyerSequencesForDeal(dealId: string) {
  return buyerSequencePreps.filter((sequence) => sequence.dealId === dealId);
}

export function getBuyerResponseRoutesForDeal(dealId: string) {
  return buyerResponseRoutes.filter((route) => route.dealId === dealId);
}

export const buyerAccelerationReadyDeals = buyerAccelerationRecords.filter(
  (record) => record.controlledSendAllowed
);
export const buyerAccelerationBlockedRecords = buyerAccelerationRecords.filter(
  (record) => record.blockedReasons.length > 0
);
export const buyerSequencesBlocked = buyerSequencePreps.filter(
  (sequence) => sequence.safetyStatus === "blocked" || sequence.blockedReasons.length > 0
);
export const buyerResponsesNeedingOwnerAction = buyerResponseRoutes.filter(
  (route) => route.ownerActionRequired
);
export const buyerAccelerationPofGaps = buyerResponseRoutes.filter((route) => route.pofGap);
export const fastestBuyerVelocity = [...buyerVelocityProfiles].sort(
  (first, second) => second.velocityScore - first.velocityScore
);
export const controlledDistributionAttempts = buyerAccelerationRecords.map((record) => ({
  dealId: record.dealId,
  status: record.controlledSendAllowed ? "ready_for_owner_approved_single_send" : "blocked",
  blockedReasons: record.blockedReasons,
  bulkBlastAllowed: record.bulkBlastAllowed,
  v13GatePassed: record.v13GatePassed,
  v5GatePassed: record.v5GatePassed
}));
export const topBuyerForTenKDeals = buyerAccelerationReadyDeals
  .map((record) => {
    const deal = getDeal(record.dealId);
    const buyerId = record.topBuyerList[0];
    return deal && deal.projectedAssignmentFee >= 10000
      ? { record, deal, buyer: getBuyer(buyerId) }
      : null;
  })
  .filter((item): item is { record: BuyerAccelerationRecord; deal: Deal; buyer: Buyer | undefined } => Boolean(item));
export const buyerAccelerationSafetyCards = [
  { label: "Bulk blast", value: "off", detail: "No campaigns or buyer blasts" },
  { label: "Controlled sends", value: String(buyerAccelerationReadyDeals.length), detail: "Require V5/V13 gates and owner approval" },
  { label: "POF gaps", value: String(buyerAccelerationPofGaps.length), detail: "Routed before access or offer intent follow-up" },
  { label: "Blocked records", value: String(buyerAccelerationBlockedRecords.length), detail: "Sanitizer, margin, or compliance gaps" }
];

function summarizeLearningBy(key: keyof OutcomeLearningRecord) {
  const grouped = outcomeLearningRecords.reduce<Record<string, OutcomeLearningRecord[]>>((acc, record) => {
    const value = String(record[key] ?? "unknown");
    acc[value] = [...(acc[value] ?? []), record];
    return acc;
  }, {});
  return Object.entries(grouped)
    .map(([value, records]) => {
      const successes = records.filter((record) =>
        ["contract_ready", "assigned", "closed_verified"].includes(record.conversionResult)
      );
      return {
        value,
        recordCount: records.length,
        successCount: successes.length,
        successRate: Math.round((successes.length / records.length) * 100),
        projectedAssignmentFee: records.reduce((total, record) => total + record.projectedAssignmentFee, 0),
        verifiedAssignmentFee: records.reduce((total, record) => total + record.verifiedAssignmentFee, 0),
        sourceRecordIds: records.map((record) => record.id)
      };
    })
    .sort((first, second) => second.successRate - first.successRate || second.verifiedAssignmentFee - first.verifiedAssignmentFee);
}

export const bestLearningLeadTypes = summarizeLearningBy("leadSource");
export const bestLearningZipCodes = summarizeLearningBy("market");
export const bestLearningBuyerProfiles = summarizeLearningBy("buyerType");
export const bestLearningOfferStrategies = summarizeLearningBy("offerStrategy");
export const lostOptimizationDeals = outcomeLearningRecords.filter((record) =>
  ["lost", "stalled", "blocked"].includes(record.conversionResult)
);
export const staleFollowUpPatterns = outcomeLearningRecords.filter((record) =>
  record.blockers.includes("stale_follow_up")
);
export const buyerPofBottleneckCount = outcomeLearningRecords.filter((record) =>
  record.blockers.includes("buyer_pof_gap")
).length;
export const strong10kLearningProbability = outcomeLearningRecords.filter(
  (record) =>
    record.projectedAssignmentFee >= 10000 &&
    record.sourceRecordsPresent &&
    record.confidenceScore >= 75
);
export const missingLearningEvidence = outcomeLearningRecords.filter(
  (record) => !record.sourceRecordsPresent || record.sourceEvidenceIds.length === 0
);
export const optimizationRecommendationsByImpact = [...optimizationRecommendations].sort(
  (first, second) => second.impactScore - first.impactScore || second.confidenceScore - first.confidenceScore
);
export const agentPerformanceByScore = [...agentPerformanceScores].sort(
  (first, second) => second.overallScore - first.overallScore
);
export const optimizationSafetyCards = [
  { label: "Source evidence", value: String(outcomeLearningRecords.length - missingLearningEvidence.length), detail: "Learning records supported by source IDs" },
  { label: "Missing evidence", value: String(missingLearningEvidence.length), detail: "Blocked from influencing confidence claims" },
  { label: "Recommendations", value: String(optimizationRecommendations.length), detail: "Explainable and owner-reviewed" },
  { label: "Scoring changes", value: String(scoringWeightChanges.length), detail: "Deterministic changes logged" }
];

export function getRevenueForecast(forecastId: string) {
  return revenueForecastRecords.find((forecast) => forecast.id === forecastId);
}

export function getAuditExportPacket(exportId: string) {
  return auditExportPackets.find((packet) => packet.id === exportId);
}

export function getProviderRegistry(providerId: string) {
  return providerRegistries.find((provider) => provider.id === providerId);
}

export function getProviderAttempts(providerId: string) {
  return providerAttemptAudits.filter((attempt) => attempt.providerId === providerId);
}

export const revenueForecastByPeriod = [...revenueForecastRecords];
export const pipelineProjectedMonthlyRevenue = revenueForecastRecords.reduce(
  (total, forecast) => total + forecast.projectedAssignmentFees,
  0
);
export const pipelineProbabilityAdjustedRevenue = revenueForecastRecords.reduce(
  (total, forecast) => total + forecast.probabilityAdjustedRevenue,
  0
);
export const pipelineRevenueAtRisk = revenueForecastRecords.reduce(
  (total, forecast) => total + forecast.projectedAssignmentFees - forecast.probabilityAdjustedRevenue,
  0
);
export const likely10kDealProbabilities = dealProbabilityRecords.filter(
  (record) => record.probabilityScore >= 70
);
export const marketRanking = [...marketScalingScores].sort(
  (first, second) => second.scalingScore - first.scalingScore
);
export const leadSpendRecommendations = leadSpendPlans.filter(
  (plan) => !plan.unsupportedSpendRecommended && plan.evidenceBasis.length > 0
);
export const unsupportedLeadSpendPlans = leadSpendPlans.filter(
  (plan) => plan.unsupportedSpendRecommended || plan.evidenceBasis.length === 0
);
export const forecastSafetyCards = [
  { label: "Forecast label", value: "estimate", detail: "No guaranteed profit or revenue" },
  { label: "Adjusted pipeline", value: formatCurrency(pipelineProbabilityAdjustedRevenue), detail: "Probability-adjusted from source records" },
  { label: "Revenue at risk", value: formatCurrency(pipelineRevenueAtRisk), detail: "Projected fees behind probability/risk gaps" },
  { label: "Spend plans", value: String(leadSpendRecommendations.length), detail: "Evidence-backed and owner-reviewed" }
];

export const activeOperatorMode = operatorModeSettings.find(
  (setting) => setting.currentMode === "semi_autonomous"
) ?? operatorModeSettings[0];
export const pendingOwnerApprovals = ownerApprovalItems.filter(
  (item) => item.approvalStatus === "pending_owner"
);
export const readyOwnerApprovals = ownerApprovalItems.filter((item) => item.readyForApproval);
export const blockedOwnerApprovals = ownerApprovalItems.filter(
  (item) => item.blockedReasons.length > 0
);
export const operatorExceptionsOpen = operatorExceptionRecords.filter(
  (exception) => exception.status === "open"
);
export const criticalOperatorExceptions = operatorExceptionsOpen.filter(
  (exception) => exception.severity === "critical"
);
export const latestOperatorDailyReport = autonomousDailyOperatingReports[0];
export const currentSystemTrustScore = systemTrustScores[0];
export const operatorHardBoundaryCards = [
  { label: "Contracts", value: "off", detail: "No execution or executable contract generation" },
  { label: "Title submission", value: "off", detail: "No automatic title-company submission" },
  { label: "Bulk campaigns", value: "off", detail: "No buyer blasts or bulk sends" },
  { label: "Level 5", value: "disabled", detail: "Unavailable even in semi-autonomous mode" },
  { label: "Payments", value: "off", detail: "No payment handling" },
  { label: "Portal publishing", value: "approval", detail: "Explicit owner approval required" }
];
export const operatorApprovalAggregates = ownerApprovalItems.reduce<Record<string, number>>(
  (acc, item) => {
    acc[item.approvalType] = (acc[item.approvalType] ?? 0) + 1;
    return acc;
  },
  {}
);
export const productionReadinessBlockedReasons = [
  ...environmentReadinessChecks.flatMap((check) => check.blockedReasons),
  ...deploymentHardeningChecks.flatMap((check) => check.blockedReasons),
  ...providerSandboxReadinessChecks.flatMap((check) => check.blockedReasons)
];
export const productionReady = productionReadinessBlockedReasons.length === 0;
export const blockedProviderReadiness = providerSandboxReadinessChecks.filter(
  (check) => !check.providerCallsAllowed
);
export const blockedProviderRegistries = providerRegistries.filter(
  (provider) => provider.readinessStatus !== "ready"
);
export const providerCredentialPosture = {
  storedSecretValues: providerRegistries.filter((provider) => provider.rawSecretValueStored).length,
  envOnlyReferences: providerRegistries.length,
  missingCredentials: providerRegistries.filter((provider) => !provider.credentialPresent).length,
  liveEnabled: providerRegistries.filter((provider) => provider.liveEnabled).length
};
export const blockedProviderAttempts = providerAttemptAudits.filter(
  (attempt) => attempt.attemptStatus === "blocked"
);
export const providerWebhookReviewQueue = providerWebhookEvents.filter(
  (event) => event.normalizedEventStatus === "review_queued"
);
export const auditExportsReady = auditExportPackets.filter(
  (packet) => packet.exportStatus === "ready_for_owner_review"
);
export const sensitiveAttachments = evidenceAttachmentRecords.filter(
  (attachment) => attachment.containsSensitiveData
);
export const safeBackupExports = backupExportRecords.filter(
  (backup) => backup.safeMetadataOnly && !backup.containsRawPrivateData
);
export const failedEnvironmentChecks = environmentReadinessChecks.filter(
  (check) => check.required && !check.passed
);
export const failedHardeningChecks = deploymentHardeningChecks.filter(
  (check) => check.required && !check.passed
);
export const approvalUxReady = approvalUxReviews.filter(
  (review) => review.recommendedDecision === "review_ready"
);

export type LeadImportBatch = {
  id: string;
  batchName: string;
  sourceFilename: string;
  status: string;
  rowCount: number;
  approvedRowCount: number;
  blockedRowCount: number;
  duplicateRowCount: number;
  committedRowCount: number;
  createdLeadsCount: number;
  safetyNotes: string[];
  liveOutreachAllowed: false;
  bulkOutreachAllowed: false;
  autoPortalPublishAllowed: false;
};

export type LeadImportRow = {
  id: string;
  batchId: string;
  rowNumber: number;
  ownerName: string;
  ownerPhone: string;
  ownerEmail: string;
  propertyAddress: string;
  propertyCity: string;
  propertyState: string;
  propertyZip: string;
  leadSource: string;
  leadType: string;
  estimatedValue: number | null;
  estimatedEquity: number | null;
  rowStatus: "approved" | "blocked" | "committed" | "needs_review";
  approvedForCommit: boolean;
  blockedReasons: string[];
  lowConfidenceFlags: string[];
  dataConfidence: number;
  liveOutreachAllowed: false;
  bulkOutreachAllowed: false;
  autoPortalPublishAllowed: false;
};

export type LeadQualityReview = {
  id: string;
  leadId: string | null;
  importRowId: string | null;
  batchId: string | null;
  checks: Record<string, boolean>;
  dataQualityScore: number;
  contactabilityScore: number;
  distressSignalConfidence: number;
  equityConfidence: number;
  importConfidence: number;
  recommendedNextAction: "research_more" | "underwrite_now" | "call_priority" | "skip_for_now" | "duplicate_review";
  blockedReasons: string[];
  reviewedBy: string;
  draftOnly: true;
  liveOutreachAllowed: false;
};

export type FieldCallOutcome = {
  id: string;
  leadId: string;
  callDatetime: string;
  contactResult: string;
  motivationNotes: string;
  askingPrice: number | null;
  timeline: string;
  propertyConditionNotes: string;
  sellerObjections: string[];
  sellerTemperature: number;
  nextFollowUpDate: string | null;
  operatorNotes: string;
  prime2NextRecommendation: string;
  doNotContact: boolean;
  outreachEligibilityStatus: string;
  escalationCreated: boolean;
  internalTaskCreated: boolean;
  liveCallRecorded: false;
  liveOutreachAllowed: false;
};

export type CallIntelligenceSession = {
  id: string;
  leadId: string;
  callOutcomeId: string | null;
  inputType: string;
  analysisStatus: string;
  ownerReviewStatus: string;
  sellerMotivationReason: string;
  urgencyTimeline: string;
  askingPrice: number | null;
  propertyCondition: string;
  repairClues: string[];
  occupancyStatus: string;
  decisionMakerStatus: string;
  trustLevel: number;
  priceFlexibility: number;
  followUpPreference: string;
  doNotContactDetected: boolean;
  legalComplianceRedFlags: string[];
  nextBestAction: string;
  callQualityScore: number;
  confidenceScore: number;
  motivationScoreDelta: number;
  contactabilityScoreDelta: number;
  sellerTemperatureUpdate: number;
  contractReadinessInfluence: number;
  riskScoreInfluence: number;
  complianceEscalationCreated: boolean;
  prime2EscalationCreated: boolean;
  followUpTaskCreated: boolean;
  draftOfferExplanationCreated: boolean;
  deterministicFallbackUsed: true;
  liveResponseGenerated: false;
};

export type SellerSignalExtraction = {
  id: string;
  sessionId: string;
  signalType: string;
  signalValue: string;
  confidenceScore: number;
  transcriptBasis: string;
};

export type CallObjectionRecord = {
  id: string;
  sessionId: string;
  objectionType: string;
  safeResponseDraft: string;
  riskLevel: "low" | "medium" | "high";
  requiredData: string[];
  nextAction: string;
  ownerReviewRequired: true;
  draftOnly: true;
  liveResponseAllowed: false;
};

export type CallFollowUpRecommendation = {
  id: string;
  sessionId: string;
  followUpType: string;
  recommendedTiming: string;
  draftMessageSummary: string;
  ownerReviewRequired: true;
  liveSendAllowed: false;
};

export type PredictionFeedbackRecord = {
  id: string;
  leadId: string | null;
  dealId: string | null;
  callOutcomeId: string | null;
  sourcePredictionType: string;
  sourcePredictionValue: string;
  actualResult: string;
  accuracyScore: number;
  varianceReason: string;
  recommendedScoringAdjustment: string;
  adjustmentExplanation: string;
  ownerReviewed: boolean;
  sourceRecordIds: string[];
  deterministicAdjustment: true;
  unsupportedProfitClaimBlocked: true;
  legalAdviceAllowed: false;
};

export type ScoringAdjustmentSuggestion = {
  id: string;
  feedbackId: string;
  weightGroup: string;
  currentWeight: number;
  recommendedWeight: number;
  adjustmentDelta: number;
  reason: string;
  explanation: string;
  ownerReviewStatus: string;
  applied: boolean;
  deterministic: true;
};

export const leadImportBatches: LeadImportBatch[] = [
  {
    id: "lead-import-001",
    batchName: "Field test absentee-vacant upload",
    sourceFilename: "field-test-absentee-vacant.csv",
    status: "preview_ready",
    rowCount: 4,
    approvedRowCount: 2,
    blockedRowCount: 2,
    duplicateRowCount: 1,
    committedRowCount: 0,
    createdLeadsCount: 0,
    safetyNotes: [
      "Preview only; no imported row triggered live outreach.",
      "Approved rows require explicit commit and remain operator-controlled."
    ],
    liveOutreachAllowed: false,
    bulkOutreachAllowed: false,
    autoPortalPublishAllowed: false
  }
];

export const leadImportRows: LeadImportRow[] = [
  {
    id: "lead-import-001-row-001",
    batchId: "lead-import-001",
    rowNumber: 1,
    ownerName: "Marcus Bell",
    ownerPhone: "2145551198",
    ownerEmail: "marcus.bell@example.test",
    propertyAddress: "3811 Fernwood Ave",
    propertyCity: "Dallas",
    propertyState: "TX",
    propertyZip: "75216",
    leadSource: "absentee owner",
    leadType: "vacant high equity",
    estimatedValue: 241000,
    estimatedEquity: 126000,
    rowStatus: "approved",
    approvedForCommit: true,
    blockedReasons: [],
    lowConfidenceFlags: [],
    dataConfidence: 88,
    liveOutreachAllowed: false,
    bulkOutreachAllowed: false,
    autoPortalPublishAllowed: false
  },
  {
    id: "lead-import-001-row-002",
    batchId: "lead-import-001",
    rowNumber: 2,
    ownerName: "Tanya Brooks",
    ownerPhone: "",
    ownerEmail: "tanya.brooks@example.test",
    propertyAddress: "922 Carson St",
    propertyCity: "Mesquite",
    propertyState: "TX",
    propertyZip: "75149",
    leadSource: "tired landlord",
    leadType: "rental fatigue",
    estimatedValue: 205000,
    estimatedEquity: 91000,
    rowStatus: "approved",
    approvedForCommit: true,
    blockedReasons: [],
    lowConfidenceFlags: ["missing_phone"],
    dataConfidence: 78,
    liveOutreachAllowed: false,
    bulkOutreachAllowed: false,
    autoPortalPublishAllowed: false
  },
  {
    id: "lead-import-001-row-003",
    batchId: "lead-import-001",
    rowNumber: 3,
    ownerName: "Address Missing",
    ownerPhone: "9725552201",
    ownerEmail: "",
    propertyAddress: "",
    propertyCity: "Dallas",
    propertyState: "TX",
    propertyZip: "75216",
    leadSource: "vacant",
    leadType: "vacant",
    estimatedValue: null,
    estimatedEquity: null,
    rowStatus: "blocked",
    approvedForCommit: false,
    blockedReasons: ["missing_property_address"],
    lowConfidenceFlags: ["missing_email", "missing_valuation_data"],
    dataConfidence: 22,
    liveOutreachAllowed: false,
    bulkOutreachAllowed: false,
    autoPortalPublishAllowed: false
  },
  {
    id: "lead-import-001-row-004",
    batchId: "lead-import-001",
    rowNumber: 4,
    ownerName: "Rosa Delgado",
    ownerPhone: "2145551198",
    ownerEmail: "rosa.delgado@example.test",
    propertyAddress: "3811 Fernwood Ave",
    propertyCity: "Dallas",
    propertyState: "TX",
    propertyZip: "75216",
    leadSource: "absentee owner",
    leadType: "duplicate",
    estimatedValue: 241000,
    estimatedEquity: 126000,
    rowStatus: "blocked",
    approvedForCommit: false,
    blockedReasons: ["duplicate_property_owner_phone"],
    lowConfidenceFlags: [],
    dataConfidence: 55,
    liveOutreachAllowed: false,
    bulkOutreachAllowed: false,
    autoPortalPublishAllowed: false
  }
];

export const leadQualityReviews: LeadQualityReview[] = [
  {
    id: "qa-lead-import-001-row-001",
    leadId: null,
    importRowId: "lead-import-001-row-001",
    batchId: "lead-import-001",
    checks: { missingPhone: false, missingPropertyAddress: false, duplicateProperty: false },
    dataQualityScore: 96,
    contactabilityScore: 90,
    distressSignalConfidence: 50,
    equityConfidence: 80,
    importConfidence: 82,
    recommendedNextAction: "call_priority",
    blockedReasons: [],
    reviewedBy: "Prime 2",
    draftOnly: true,
    liveOutreachAllowed: false
  },
  {
    id: "qa-lead-import-001-row-002",
    leadId: null,
    importRowId: "lead-import-001-row-002",
    batchId: "lead-import-001",
    checks: { missingPhone: true, missingPropertyAddress: false, duplicateProperty: false },
    dataQualityScore: 86,
    contactabilityScore: 40,
    distressSignalConfidence: 50,
    equityConfidence: 80,
    importConfidence: 68,
    recommendedNextAction: "research_more",
    blockedReasons: [],
    reviewedBy: "Prime 2",
    draftOnly: true,
    liveOutreachAllowed: false
  },
  {
    id: "qa-lead-import-001-row-003",
    leadId: null,
    importRowId: "lead-import-001-row-003",
    batchId: "lead-import-001",
    checks: { missingPhone: false, missingPropertyAddress: true, duplicateProperty: false },
    dataQualityScore: 42,
    contactabilityScore: 75,
    distressSignalConfidence: 40,
    equityConfidence: 25,
    importConfidence: 44,
    recommendedNextAction: "skip_for_now",
    blockedReasons: ["missing_property_address"],
    reviewedBy: "Prime 2",
    draftOnly: true,
    liveOutreachAllowed: false
  },
  {
    id: "qa-lead-import-001-row-004",
    leadId: null,
    importRowId: "lead-import-001-row-004",
    batchId: "lead-import-001",
    checks: { missingPhone: false, missingPropertyAddress: false, duplicateProperty: true },
    dataQualityScore: 66,
    contactabilityScore: 85,
    distressSignalConfidence: 50,
    equityConfidence: 80,
    importConfidence: 66,
    recommendedNextAction: "duplicate_review",
    blockedReasons: ["duplicate_property_owner_phone"],
    reviewedBy: "Prime 2",
    draftOnly: true,
    liveOutreachAllowed: false
  }
];

export const fieldCallOutcomes: FieldCallOutcome[] = [
  {
    id: "call-outcome-001",
    leadId: "lead-001",
    callDatetime: "2026-05-04T18:30:00Z",
    contactResult: "motivated",
    motivationNotes: "Seller confirmed repair fatigue and asked for an as-is explanation.",
    askingPrice: 158000,
    timeline: "Would like a clear written option this week.",
    propertyConditionNotes: "Roof age and interior updates need review.",
    sellerObjections: ["wants repair basis", "needs timing clarity"],
    sellerTemperature: 84,
    nextFollowUpDate: "2026-05-05T15:00:00Z",
    operatorNotes: "Field call outcome only; no system call was made.",
    prime2NextRecommendation: "Escalate to seller acquisition for draft-only offer explanation.",
    doNotContact: false,
    outreachEligibilityStatus: "owner_review_required",
    escalationCreated: true,
    internalTaskCreated: true,
    liveCallRecorded: false,
    liveOutreachAllowed: false
  },
  {
    id: "call-outcome-002",
    leadId: "lead-006",
    callDatetime: "2026-05-04T18:30:00Z",
    contactResult: "wrong_number",
    motivationNotes: "Number reached unrelated party.",
    askingPrice: null,
    timeline: "",
    propertyConditionNotes: "",
    sellerObjections: [],
    sellerTemperature: 0,
    nextFollowUpDate: null,
    operatorNotes: "Research contact data before any additional owner-approved outreach.",
    prime2NextRecommendation: "Lower contactability and route to lead QA research.",
    doNotContact: false,
    outreachEligibilityStatus: "research_contact_info",
    escalationCreated: false,
    internalTaskCreated: false,
    liveCallRecorded: false,
    liveOutreachAllowed: false
  },
  {
    id: "call-outcome-003",
    leadId: "lead-008",
    callDatetime: "2026-05-04T18:30:00Z",
    contactResult: "do_not_contact",
    motivationNotes: "Seller requested no future contact.",
    askingPrice: null,
    timeline: "",
    propertyConditionNotes: "",
    sellerObjections: ["do not contact"],
    sellerTemperature: 0,
    nextFollowUpDate: null,
    operatorNotes: "Do-not-contact boundary recorded.",
    prime2NextRecommendation: "Block future live outreach eligibility for this lead.",
    doNotContact: true,
    outreachEligibilityStatus: "blocked_do_not_contact",
    escalationCreated: false,
    internalTaskCreated: false,
    liveCallRecorded: false,
    liveOutreachAllowed: false
  }
];

export const callIntelligenceSessions: CallIntelligenceSession[] = [
  { id: "call-intel-001", leadId: "lead-001", callOutcomeId: "call-outcome-001", inputType: "manual_call_notes", analysisStatus: "analyzed", ownerReviewStatus: "pending_review", sellerMotivationReason: "repair fatigue and as-is interest", urgencyTimeline: "this week", askingPrice: 158000, propertyCondition: "roof, interior updates", repairClues: ["roof", "interior updates"], occupancyStatus: "occupied", decisionMakerStatus: "owner_decision_maker", trustLevel: 78, priceFlexibility: 66, followUpPreference: "owner_review", doNotContactDetected: false, legalComplianceRedFlags: [], nextBestAction: "escalate motivated seller for seller acquisition review", callQualityScore: 88, confidenceScore: 82, motivationScoreDelta: 18, contactabilityScoreDelta: 12, sellerTemperatureUpdate: 84, contractReadinessInfluence: 40, riskScoreInfluence: 5, complianceEscalationCreated: false, prime2EscalationCreated: true, followUpTaskCreated: true, draftOfferExplanationCreated: true, deterministicFallbackUsed: true, liveResponseGenerated: false },
  { id: "call-intel-002", leadId: "lead-008", callOutcomeId: "call-outcome-003", inputType: "pasted_transcript", analysisStatus: "analyzed", ownerReviewStatus: "pending_review", sellerMotivationReason: "seller requested no future contact", urgencyTimeline: "none", askingPrice: null, propertyCondition: "condition not discussed", repairClues: [], occupancyStatus: "unknown", decisionMakerStatus: "unknown", trustLevel: 20, priceFlexibility: 0, followUpPreference: "do_not_contact", doNotContactDetected: true, legalComplianceRedFlags: [], nextBestAction: "do not contact; retain record for owner and compliance review", callQualityScore: 42, confidenceScore: 90, motivationScoreDelta: 0, contactabilityScoreDelta: -60, sellerTemperatureUpdate: 0, contractReadinessInfluence: 0, riskScoreInfluence: 20, complianceEscalationCreated: false, prime2EscalationCreated: false, followUpTaskCreated: false, draftOfferExplanationCreated: false, deterministicFallbackUsed: true, liveResponseGenerated: false },
  { id: "call-intel-003", leadId: "lead-003", callOutcomeId: null, inputType: "manual_call_notes", analysisStatus: "analyzed", ownerReviewStatus: "pending_review", sellerMotivationReason: "seller asked for title/contract meaning", urgencyTimeline: "30 days", askingPrice: 170000, propertyCondition: "repairs", repairClues: ["repairs"], occupancyStatus: "unknown", decisionMakerStatus: "needs family input", trustLevel: 58, priceFlexibility: 45, followUpPreference: "owner_review", doNotContactDetected: false, legalComplianceRedFlags: ["attorney", "title"], nextBestAction: "route title questions to compliance review reminder", callQualityScore: 76, confidenceScore: 78, motivationScoreDelta: 6, contactabilityScoreDelta: 8, sellerTemperatureUpdate: 62, contractReadinessInfluence: 10, riskScoreInfluence: 30, complianceEscalationCreated: true, prime2EscalationCreated: false, followUpTaskCreated: false, draftOfferExplanationCreated: true, deterministicFallbackUsed: true, liveResponseGenerated: false }
];

export const sellerSignalExtractions: SellerSignalExtraction[] = [
  { id: "seller-signal-001", sessionId: "call-intel-001", signalType: "motivation", signalValue: "repair fatigue", confidenceScore: 82, transcriptBasis: "roof age and interior updates" },
  { id: "seller-signal-002", sessionId: "call-intel-001", signalType: "timeline", signalValue: "this week", confidenceScore: 80, transcriptBasis: "written option this week" },
  { id: "seller-signal-003", sessionId: "call-intel-002", signalType: "do_not_contact", signalValue: "true", confidenceScore: 95, transcriptBasis: "do not contact me again" },
  { id: "seller-signal-004", sessionId: "call-intel-003", signalType: "title_question", signalValue: "qualified review needed", confidenceScore: 88, transcriptBasis: "title and contract terms require an attorney" }
];

export const callObjectionRecords: CallObjectionRecord[] = [
  { id: "call-objection-001", sessionId: "call-intel-001", objectionType: "wants_repairs_considered", safeResponseDraft: "Draft only: acknowledge repair concerns and let the owner review documented repair evidence before deciding next steps.", riskLevel: "medium", requiredData: ["repair estimate", "condition notes"], nextAction: "review repair basis", ownerReviewRequired: true, draftOnly: true, liveResponseAllowed: false },
  { id: "call-objection-002", sessionId: "call-intel-003", objectionType: "wants_title_explanation", safeResponseDraft: "Draft only: route title questions to qualified review before any answer is relied upon.", riskLevel: "high", requiredData: ["attorney/title review reminder"], nextAction: "compliance escalation", ownerReviewRequired: true, draftOnly: true, liveResponseAllowed: false }
];

export const callFollowUpRecommendations: CallFollowUpRecommendation[] = [
  { id: "call-follow-up-001", sessionId: "call-intel-001", followUpType: "offer_explanation_review", recommendedTiming: "owner review today", draftMessageSummary: "Prepare draft-only as-is offer explanation from existing underwriting.", ownerReviewRequired: true, liveSendAllowed: false },
  { id: "call-follow-up-002", sessionId: "call-intel-003", followUpType: "compliance_review", recommendedTiming: "before any seller response", draftMessageSummary: "Route title/attorney question to review reminder; do not answer with legal guidance.", ownerReviewRequired: true, liveSendAllowed: false }
];

export type DocumentIntelligenceFile = {
  id: string;
  sourceDealId: string | null;
  sourceLeadId: string | null;
  sourceBuyerId: string | null;
  uploadedBy: string;
  originalFilename: string;
  fileType: string;
  storageReference: string;
  documentType: string;
  status: string;
  classificationConfidence: number;
  extractedSummary: string;
  extractedPrice: number | null;
  extractedBuyerName: string;
  extractedSellerName: string;
  extractedPropertyAddress: string;
  extractedEffectiveDate: string;
  extractedClosingDate: string;
  extractedSignatureStatus: string;
  extractedAssignmentLanguagePresent: boolean;
  extractedPofAmount: number | null;
  riskStatus: string;
  ownerReviewStatus: string;
  rawTextStored: boolean;
  fullTextHidden: true;
  portalPublishAllowed: false;
  legalAdviceProvided: false;
  executableContractGenerated: false;
};

export type DocumentIssueFlag = {
  id: string;
  documentId: string;
  issueType: string;
  severity: "low" | "medium" | "high";
  sourceField: string;
  explanation: string;
  recommendedNextAction: string;
  ownerReviewRequired: true;
  complianceReviewRequired: boolean;
  externalReviewReminder: boolean;
  resolved: boolean;
};

export type DocumentReviewTask = {
  id: string;
  documentId: string;
  taskType: string;
  assignedTo: string;
  status: string;
  priority: "low" | "normal" | "high";
  reason: string;
  recommendedNextAction: string;
  ownerReviewRequired: true;
  liveSendAllowed: false;
  legalReviewExternalOnly: boolean;
};

export type DocumentEvidenceLink = {
  id: string;
  documentId: string;
  dealEvidencePacketId: string | null;
  sourceRecordType: string;
  sourceRecordId: string;
  linkageStatus: string;
  sanitizedForExport: true;
  portalPublishAllowed: false;
};

export const documentIntelligenceFiles: DocumentIntelligenceFile[] = [
  { id: "doc-intel-001", sourceDealId: "deal-001", sourceLeadId: "lead-001", sourceBuyerId: null, uploadedBy: "Owner", originalFilename: "deal-001-purchase-agreement-draft.txt", fileType: "text", storageReference: "local-placeholder/doc-001", documentType: "purchase_agreement", status: "needs_review", classificationConfidence: 92, extractedSummary: "Purchase agreement draft with missing signature and title company.", extractedPrice: 140000, extractedBuyerName: "Prime 2 Acquisitions LLC", extractedSellerName: "Angela Morris", extractedPropertyAddress: "1420 Cedar Crest Ave, Dallas, TX 75216", extractedEffectiveDate: "05/08/2026", extractedClosingDate: "05/30/2026", extractedSignatureStatus: "missing", extractedAssignmentLanguagePresent: true, extractedPofAmount: null, riskStatus: "needs_review", ownerReviewStatus: "pending_review", rawTextStored: true, fullTextHidden: true, portalPublishAllowed: false, legalAdviceProvided: false, executableContractGenerated: false },
  { id: "doc-intel-002", sourceDealId: "deal-001", sourceLeadId: null, sourceBuyerId: "buyer-001", uploadedBy: "Owner", originalFilename: "buyer-001-pof-letter.txt", fileType: "text", storageReference: "local-placeholder/doc-002", documentType: "proof_of_funds", status: "needs_review", classificationConfidence: 90, extractedSummary: "POF amount is below buyer purchase price and needs follow-up.", extractedPrice: null, extractedBuyerName: "Jules Carter", extractedSellerName: "", extractedPropertyAddress: "", extractedEffectiveDate: "", extractedClosingDate: "", extractedSignatureStatus: "signed", extractedAssignmentLanguagePresent: false, extractedPofAmount: 145000, riskStatus: "high", ownerReviewStatus: "pending_review", rawTextStored: true, fullTextHidden: true, portalPublishAllowed: false, legalAdviceProvided: false, executableContractGenerated: false },
  { id: "doc-intel-003", sourceDealId: "deal-005", sourceLeadId: "lead-005", sourceBuyerId: null, uploadedBy: "Owner", originalFilename: "assignment-language-review.txt", fileType: "text", storageReference: "local-placeholder/doc-003", documentType: "assignment_agreement", status: "needs_review", classificationConfidence: 84, extractedSummary: "Assignment agreement language needs external review reminder.", extractedPrice: 210000, extractedBuyerName: "Buyer Entity Placeholder", extractedSellerName: "Robert Fields", extractedPropertyAddress: "5218 Bexar St, Dallas, TX 75215", extractedEffectiveDate: "05/10/2026", extractedClosingDate: "", extractedSignatureStatus: "unknown", extractedAssignmentLanguagePresent: false, extractedPofAmount: null, riskStatus: "high", ownerReviewStatus: "pending_review", rawTextStored: true, fullTextHidden: true, portalPublishAllowed: false, legalAdviceProvided: false, executableContractGenerated: false }
];

export const documentIssueFlags: DocumentIssueFlag[] = [
  { id: "doc-issue-001", documentId: "doc-intel-001", issueType: "missing_signature", severity: "high", sourceField: "signature_status", explanation: "Purchase agreement draft is not signed and cannot be treated as controlled execution.", recommendedNextAction: "Owner review and external review reminder before relying on the file.", ownerReviewRequired: true, complianceReviewRequired: true, externalReviewReminder: true, resolved: false },
  { id: "doc-issue-002", documentId: "doc-intel-002", issueType: "pof_amount_below_buyer_offer", severity: "high", sourceField: "pof_amount", explanation: "POF amount is below the buyer purchase price on the deal record.", recommendedNextAction: "Queue buyer POF follow-up through gated communication drafts.", ownerReviewRequired: true, complianceReviewRequired: true, externalReviewReminder: false, resolved: false },
  { id: "doc-issue-003", documentId: "doc-intel-003", issueType: "assignment_language_missing", severity: "high", sourceField: "assignment_language_present", explanation: "Assignment language was not detected and must be externally reviewed before assignment readiness.", recommendedNextAction: "Route to title/attorney external review reminder.", ownerReviewRequired: true, complianceReviewRequired: true, externalReviewReminder: true, resolved: false }
];

export const documentReviewTasks: DocumentReviewTask[] = [
  { id: "doc-review-001", documentId: "doc-intel-001", taskType: "title_attorney_external_review_reminder", assignedTo: "Prime 2", status: "open", priority: "high", reason: "Missing signature and title company data.", recommendedNextAction: "Prepare reminder only; no document submission.", ownerReviewRequired: true, liveSendAllowed: false, legalReviewExternalOnly: true },
  { id: "doc-review-002", documentId: "doc-intel-002", taskType: "buyer_pof_follow_up", assignedTo: "Owner", status: "open", priority: "high", reason: "POF is below buyer purchase price.", recommendedNextAction: "Ask for updated POF only through gated drafts.", ownerReviewRequired: true, liveSendAllowed: false, legalReviewExternalOnly: false },
  { id: "doc-review-003", documentId: "doc-intel-003", taskType: "compliance_review", assignedTo: "Prime 2", status: "open", priority: "high", reason: "Assignment language is missing or unclear.", recommendedNextAction: "Create external review reminder; no legal conclusion.", ownerReviewRequired: true, liveSendAllowed: false, legalReviewExternalOnly: true }
];

export const documentEvidenceLinks: DocumentEvidenceLink[] = [
  { id: "doc-evidence-001", documentId: "doc-intel-001", dealEvidencePacketId: "evidence-001", sourceRecordType: "deal", sourceRecordId: "deal-001", linkageStatus: "linked", sanitizedForExport: true, portalPublishAllowed: false },
  { id: "doc-evidence-002", documentId: "doc-intel-002", dealEvidencePacketId: "evidence-001", sourceRecordType: "buyer", sourceRecordId: "buyer-001", linkageStatus: "linked", sanitizedForExport: true, portalPublishAllowed: false },
  { id: "doc-evidence-003", documentId: "doc-intel-003", dealEvidencePacketId: "evidence-003", sourceRecordType: "deal", sourceRecordId: "deal-005", linkageStatus: "linked", sanitizedForExport: true, portalPublishAllowed: false }
];

export const predictionFeedbackRecords: PredictionFeedbackRecord[] = [
  {
    id: "feedback-001",
    leadId: "lead-001",
    dealId: "deal-001",
    callOutcomeId: "call-outcome-001",
    sourcePredictionType: "predicted_motivation",
    sourcePredictionValue: "high motivation",
    actualResult: "motivated",
    accuracyScore: 92,
    varianceReason: "prediction_matched",
    recommendedScoringAdjustment: "maintain motivation weighting",
    adjustmentExplanation: "High motivation prediction matched seller field outcome.",
    ownerReviewed: false,
    sourceRecordIds: ["lead-001", "deal-001", "call-outcome-001"],
    deterministicAdjustment: true,
    unsupportedProfitClaimBlocked: true,
    legalAdviceAllowed: false
  },
  {
    id: "feedback-002",
    leadId: "lead-006",
    dealId: null,
    callOutcomeId: "call-outcome-002",
    sourcePredictionType: "predicted_contactability",
    sourcePredictionValue: "high contactability",
    actualResult: "wrong_number",
    accuracyScore: 40,
    varianceReason: "contactability_overstated",
    recommendedScoringAdjustment: "reduce phone confidence unless recent verification exists",
    adjustmentExplanation: "Actual field outcome showed weaker contactability than the imported data predicted.",
    ownerReviewed: false,
    sourceRecordIds: ["lead-006", "call-outcome-002"],
    deterministicAdjustment: true,
    unsupportedProfitClaimBlocked: true,
    legalAdviceAllowed: false
  }
];

export const scoringAdjustmentSuggestions: ScoringAdjustmentSuggestion[] = [
  {
    id: "adjustment-feedback-001",
    feedbackId: "feedback-001",
    weightGroup: "motivation",
    currentWeight: 0.18,
    recommendedWeight: 0.18,
    adjustmentDelta: 0,
    reason: "prediction_matched",
    explanation: "Maintain weight because the prediction matched real seller response.",
    ownerReviewStatus: "pending_review",
    applied: false,
    deterministic: true
  },
  {
    id: "adjustment-feedback-002",
    feedbackId: "feedback-002",
    weightGroup: "contactability",
    currentWeight: 0.1,
    recommendedWeight: 0.08,
    adjustmentDelta: -0.02,
    reason: "contactability_overstated",
    explanation: "Reduce contactability confidence for unverified phone data until confirmed by field outcomes.",
    ownerReviewStatus: "pending_review",
    applied: false,
    deterministic: true
  }
];

export function getLeadImportBatch(batchId: string) {
  return leadImportBatches.find((batch) => batch.id === batchId);
}

export function getLeadQaReview(leadId: string) {
  return leadQualityReviews.find((review) => review.leadId === leadId || review.importRowId === leadId);
}

export function getCallOutcome(outcomeId: string) {
  return fieldCallOutcomes.find((outcome) => outcome.id === outcomeId);
}

export function getCallIntelligenceSession(sessionId: string) {
  return callIntelligenceSessions.find((session) => session.id === sessionId);
}

export function getCallSignals(sessionId: string) {
  return sellerSignalExtractions.filter((signal) => signal.sessionId === sessionId);
}

export function getCallObjections(sessionId: string) {
  return callObjectionRecords.filter((objection) => objection.sessionId === sessionId);
}

export function getCallFollowUps(sessionId: string) {
  return callFollowUpRecommendations.filter((followUp) => followUp.sessionId === sessionId);
}

export function getDocumentIntelligenceFile(documentId: string) {
  return documentIntelligenceFiles.find((document) => document.id === documentId);
}

export function getDocumentIssues(documentId: string) {
  return documentIssueFlags.filter((issue) => issue.documentId === documentId);
}

export function getDocumentReviewTasks(documentId: string) {
  return documentReviewTasks.filter((task) => task.documentId === documentId);
}

export function getDocumentEvidenceLinks(documentId: string) {
  return documentEvidenceLinks.filter((link) => link.documentId === documentId);
}

export function getPredictionFeedback(feedbackId: string) {
  return predictionFeedbackRecords.find((record) => record.id === feedbackId);
}

export const blockedLeadImportRows = leadImportRows.filter((row) => row.blockedReasons.length > 0);
export const approvedLeadImportRows = leadImportRows.filter((row) => row.rowStatus === "approved");
export const lowConfidenceQaReviews = leadQualityReviews.filter((review) => review.importConfidence < 60 || review.blockedReasons.length > 0);
export const callPriorityQaReviews = leadQualityReviews.filter((review) => review.recommendedNextAction === "call_priority");
export const researchMoreQaReviews = leadQualityReviews.filter((review) => review.recommendedNextAction === "research_more");
export const motivatedFieldOutcomes = fieldCallOutcomes.filter((outcome) =>
  ["motivated", "offer_requested", "appointment_set"].includes(outcome.contactResult)
);
export const doNotContactOutcomes = fieldCallOutcomes.filter((outcome) => outcome.doNotContact);
export const highMotivationCallSessions = callIntelligenceSessions.filter(
  (session) => session.motivationScoreDelta >= 15 || session.sellerTemperatureUpdate >= 75
);
export const dncCallSessions = callIntelligenceSessions.filter((session) => session.doNotContactDetected);
export const complianceCallEscalations = callIntelligenceSessions.filter(
  (session) => session.complianceEscalationCreated || session.legalComplianceRedFlags.length > 0
);
export const callQualityAverage = Math.round(
  callIntelligenceSessions.reduce((total, session) => total + session.callQualityScore, 0) /
    callIntelligenceSessions.length
);
export const documentsNeedingReview = documentIntelligenceFiles.filter(
  (document) => document.ownerReviewStatus === "pending_review"
);
export const documentMissingSignatures = documentIntelligenceFiles.filter(
  (document) => document.extractedSignatureStatus !== "signed"
);
export const documentPriceMismatches = documentIssueFlags.filter(
  (issue) => issue.issueType === "mismatched_purchase_price"
);
export const documentPofIssues = documentIssueFlags.filter((issue) =>
  issue.issueType.includes("pof")
);
export const documentAssignmentWarnings = documentIssueFlags.filter((issue) =>
  issue.issueType.includes("assignment")
);
export const documentExternalReviewTasks = documentReviewTasks.filter(
  (task) => task.legalReviewExternalOnly
);
export const predictionMisses = predictionFeedbackRecords.filter((record) => record.accuracyScore < 70);
export const pendingScoringAdjustments = scoringAdjustmentSuggestions.filter((suggestion) => suggestion.ownerReviewStatus === "pending_review");
export const fieldTestingAccuracy = Math.round(
  predictionFeedbackRecords.reduce((total, record) => total + record.accuracyScore, 0) /
    predictionFeedbackRecords.length
);
export const firstDealCandidates = leadQualityReviews
  .filter((review) => ["call_priority", "underwrite_now"].includes(review.recommendedNextAction))
  .sort((first, second) => second.importConfidence - first.importConfidence);
export const v19SafetyCards = [
  { label: "Live outreach", value: "off", detail: "CSV imports cannot trigger SMS, email, or calls" },
  { label: "Bulk actions", value: "off", detail: "No campaigns or mass follow-up from imported rows" },
  { label: "Bad rows", value: String(blockedLeadImportRows.length), detail: "Visible with reasons before commit" },
  { label: "DNC records", value: String(doNotContactOutcomes.length), detail: "Future live outreach eligibility blocked" }
];

export type AITemplateRecord = {
  id: string;
  requestType: string;
  templateName: string;
  templateVersion: string;
  templateSections: string[];
  safetyStatus: string;
  usesSystemDataOnly: boolean;
  canInventNumbers: boolean;
};

export type AIRequestRecord = {
  id: string;
  requestType: string;
  model: string;
  tokenEstimate: number;
  costEstimate: number;
  safetyStatus: string;
  blockedReason: string;
  providerMode: string;
  realProviderCalled: boolean;
  legalAdviceAllowed: boolean;
  contractGenerationAllowed: boolean;
  financialCalculationOverrideAllowed: boolean;
};

export type AIAuditRecord = {
  id: string;
  requestId: string;
  eventType: string;
  safetyStatus: string;
  blockedReason: string;
  providerMode: string;
  realProviderCalled: boolean;
};

export type AICostLedgerRecord = {
  id: string;
  requestId: string;
  period: string;
  tokenEstimate: number;
  costEstimate: number;
  monthlyTotalAfter: number;
  monthlyCap: number;
  capStatus: string;
};

export type WorkerJobRecord = {
  id: string;
  jobId: string;
  jobType: string;
  sourceRecord: string;
  status: "pending" | "running" | "completed" | "failed";
  attempts: number;
  idempotencyKey: string;
  errorMessage: string;
  priority: string;
  liveActionAllowed: boolean;
  contractExecutionAllowed: boolean;
  titleSubmissionAllowed: boolean;
  portalPublishAllowed: boolean;
  paymentHandlingAllowed: boolean;
  bulkSendAllowed: boolean;
};

export type WorkerJobLogRecord = {
  id: string;
  jobId: string;
  jobType: string;
  eventType: string;
  status: string;
  message: string;
  providerCalled: boolean;
  realWorldActionTaken: boolean;
};

export type WorkerHeartbeatRecord = {
  id: string;
  workerName: string;
  status: string;
  active: boolean;
  stuckJobsDetected: number;
  recoveryRecommended: boolean;
  liveActionAllowed: boolean;
};

export const aiTemplates: AITemplateRecord[] = [
  {
    id: "ai-template-seller-script-v20",
    requestType: "seller_script_draft",
    templateName: "Seller script draft",
    templateVersion: "v20.1",
    templateSections: ["intro", "empathy", "property question", "soft close"],
    safetyStatus: "approved",
    usesSystemDataOnly: true,
    canInventNumbers: false
  },
  {
    id: "ai-template-buyer-message-v20",
    requestType: "buyer_message_draft",
    templateName: "Buyer message draft",
    templateVersion: "v20.1",
    templateSections: ["deal summary", "system numbers", "CTA"],
    safetyStatus: "approved",
    usesSystemDataOnly: true,
    canInventNumbers: false
  },
  {
    id: "ai-template-daily-briefing-v20",
    requestType: "daily_briefing",
    templateName: "Prime 2 daily briefing",
    templateVersion: "v20.1",
    templateSections: ["hot deals", "approval queue", "blockers", "safe actions"],
    safetyStatus: "approved",
    usesSystemDataOnly: true,
    canInventNumbers: false
  },
  {
    id: "ai-template-call-intelligence-v23",
    requestType: "call_intelligence_extraction",
    templateName: "Call intelligence extraction",
    templateVersion: "v23.1",
    templateSections: ["seller signals", "objections", "risk flags", "next action"],
    safetyStatus: "approved",
    usesSystemDataOnly: true,
    canInventNumbers: false
  }
];

export const aiRequestLogs: AIRequestRecord[] = [
  {
    id: "ai-request-001",
    requestType: "deal_summary",
    model: "prime2-controlled-template",
    tokenEstimate: 142,
    costEstimate: 0,
    safetyStatus: "approved",
    blockedReason: "",
    providerMode: "mock/dry_run",
    realProviderCalled: false,
    legalAdviceAllowed: false,
    contractGenerationAllowed: false,
    financialCalculationOverrideAllowed: false
  },
  {
    id: "ai-request-002",
    requestType: "contract_generation",
    model: "prime2-controlled-template",
    tokenEstimate: 32,
    costEstimate: 0,
    safetyStatus: "blocked",
    blockedReason: "blocked_request_type",
    providerMode: "mock/dry_run",
    realProviderCalled: false,
    legalAdviceAllowed: false,
    contractGenerationAllowed: false,
    financialCalculationOverrideAllowed: false
  }
];

export const aiAuditRecords: AIAuditRecord[] = [
  {
    id: "ai-audit-001",
    requestId: "ai-request-001",
    eventType: "ai_response_approved",
    safetyStatus: "approved",
    blockedReason: "",
    providerMode: "mock/dry_run",
    realProviderCalled: false
  },
  {
    id: "ai-audit-002",
    requestId: "ai-request-002",
    eventType: "ai_response_blocked",
    safetyStatus: "blocked",
    blockedReason: "blocked_request_type",
    providerMode: "mock/dry_run",
    realProviderCalled: false
  }
];

export const aiCostLedgers: AICostLedgerRecord[] = [
  {
    id: "ai-cost-001",
    requestId: "ai-request-001",
    period: "2026-05",
    tokenEstimate: 142,
    costEstimate: 0,
    monthlyTotalAfter: 0,
    monthlyCap: 25,
    capStatus: "within_cap"
  },
  {
    id: "ai-cost-002",
    requestId: "ai-request-002",
    period: "2026-05",
    tokenEstimate: 32,
    costEstimate: 0,
    monthlyTotalAfter: 0,
    monthlyCap: 25,
    capStatus: "within_cap"
  }
];

export const workerJobs: WorkerJobRecord[] = [
  {
    id: "worker-job-seed-001",
    jobId: "job-001",
    jobType: "lead_scoring_refresh",
    sourceRecord: "leads",
    status: "completed",
    attempts: 1,
    idempotencyKey: "seed:lead-scoring:2026050413",
    errorMessage: "",
    priority: "high",
    liveActionAllowed: false,
    contractExecutionAllowed: false,
    titleSubmissionAllowed: false,
    portalPublishAllowed: false,
    paymentHandlingAllowed: false,
    bulkSendAllowed: false
  },
  {
    id: "worker-job-seed-002",
    jobId: "job-002",
    jobType: "automation_rule_evaluation",
    sourceRecord: "automation_rules",
    status: "pending",
    attempts: 0,
    idempotencyKey: "seed:automation:202605041305",
    errorMessage: "",
    priority: "normal",
    liveActionAllowed: false,
    contractExecutionAllowed: false,
    titleSubmissionAllowed: false,
    portalPublishAllowed: false,
    paymentHandlingAllowed: false,
    bulkSendAllowed: false
  },
  {
    id: "worker-job-seed-003",
    jobId: "job-003",
    jobType: "call_analysis",
    sourceRecord: "call-intel-001",
    status: "completed",
    attempts: 1,
    idempotencyKey: "seed:call-analysis:call-intel-001",
    errorMessage: "",
    priority: "high",
    liveActionAllowed: false,
    contractExecutionAllowed: false,
    titleSubmissionAllowed: false,
    portalPublishAllowed: false,
    paymentHandlingAllowed: false,
    bulkSendAllowed: false
  }
];

export const workerJobLogs: WorkerJobLogRecord[] = [
  {
    id: "worker-log-001",
    jobId: "job-001",
    jobType: "lead_scoring_refresh",
    eventType: "job_completed",
    status: "completed",
    message: "Lead scoring refresh completed as internal prep.",
    providerCalled: false,
    realWorldActionTaken: false
  },
  {
    id: "worker-log-002",
    jobId: "job-002",
    jobType: "automation_rule_evaluation",
    eventType: "job_enqueued",
    status: "pending",
    message: "Automation rule check queued with no live action path.",
    providerCalled: false,
    realWorldActionTaken: false
  },
  {
    id: "worker-log-003",
    jobId: "job-003",
    jobType: "call_analysis",
    eventType: "job_completed",
    status: "completed",
    message: "Call intelligence analysis completed as internal prep.",
    providerCalled: false,
    realWorldActionTaken: false
  }
];

export const workerHeartbeat: WorkerHeartbeatRecord = {
  id: "worker-heartbeat-001",
  workerName: "prime2-worker",
  status: "healthy",
  active: true,
  stuckJobsDetected: 0,
  recoveryRecommended: false,
  liveActionAllowed: false
};

export const blockedAiRequests = aiRequestLogs.filter((request) => request.safetyStatus === "blocked");
export const approvedAiTemplates = aiTemplates.filter((template) => template.safetyStatus === "approved");
export const pendingWorkerJobs = workerJobs.filter((job) => job.status === "pending");
export const failedWorkerJobs = workerJobs.filter((job) => job.status === "failed");
export const completedWorkerJobs = workerJobs.filter((job) => job.status === "completed");
