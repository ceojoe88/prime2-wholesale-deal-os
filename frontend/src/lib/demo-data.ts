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
  { id: "interest-003", buyerId: "buyer-003", dealId: "deal-003", interestStatus: "proof_of_funds_needed", intendedOfferAmount: 193000, proofOfFundsStatus: "needs_refresh", notes: "POF refresh required; buyer interest is non-binding.", timestamp: "2026-05-04T14:11:00Z", draftOnly: true, contractExecutionAllowed: false }
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
