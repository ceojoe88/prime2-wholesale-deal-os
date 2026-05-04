from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.domain.buyer_matching import score_buyer_match
from app.domain.buyer_portal import update_publication_gate
from app.domain.communications import (
    communication_hash,
    idempotency_key_for,
    validate_communication_safety,
)
from app.domain.closing_coordination import sync_deal_room
from app.domain.compliance import REQUIRED_CONFIRMATIONS
from app.domain.contract_control import update_assignment_readiness, update_contract_prep_gate
from app.domain.deal_evidence import sync_assignment_fee_attribution, sync_evidence_packet
from app.domain.profit_control import ProfitControlInput, calculate_profit_control
from app.domain.rules import ANALYSIS_ONLY_ACTIONS, BLOCKED_ACTIONS
from app.domain.scoring import calculate_lead_opportunity, deal_speed_score
from app.domain.seller_acquisition import update_offer_packet_gate
from app.domain.seller_portal import (
    update_seller_visibility_gate,
    validate_seller_portal_language,
)
from app.models import (
    Agent,
    AssignmentFeeAttribution,
    AssignmentReadinessRecord,
    Buyer,
    BuyerDealPublication,
    BuyerInterest,
    BuyerMatch,
    ClosingCoordinationChecklist,
    ComplianceRecord,
    CommunicationApproval,
    CommunicationDraft,
    CommunicationDryRunReceipt,
    CommunicationSendAttempt,
    ContractControl,
    Deal,
    DealEvidencePacket,
    DealRoomBlocker,
    Division,
    Lead,
    OfferPacket,
    SellerInteraction,
    SellerOfferPublication,
    SellerPortalResponse,
    TitleHandoffPacket,
    UnifiedDealRoom,
)


DIVISION_DEFINITIONS = [
    {
        "id": "market-intelligence",
        "name": "Market Intelligence Division",
        "manager_name": "Marisol Vega",
        "responsibilities": [
            "Track zip demand and investor activity",
            "Summarize comparable sale evidence",
            "Flag overheated or thin buyer markets",
        ],
        "priority_queue": ["75216 comps refresh", "Rental demand scan", "Investor heat review"],
        "workload": 7,
        "active_recommendations": [
            "Give Dallas south-side zip codes priority only when buyer demand is verified."
        ],
        "risk_flags": ["thin_comps_in_two_zips"],
        "performance_notes": "Strong read on investor clusters and rent-to-ARV pressure.",
        "next_best_action": "Refresh comparable sale notes for the five hot opportunities.",
    },
    {
        "id": "lead-intelligence",
        "name": "Lead Intelligence Division",
        "manager_name": "Elias Monroe",
        "responsibilities": [
            "Score seller motivation and distress signals",
            "Stack list sources without paid API calls",
            "Flag missing data and contactability gaps",
        ],
        "priority_queue": ["Vacancy signal review", "Probate confidence check", "High-equity stack"],
        "workload": 11,
        "active_recommendations": ["Move high-equity vacant leads to underwriting before new imports."],
        "risk_flags": ["probate_authority_unverified"],
        "performance_notes": "Opportunity scores are calibrated conservatively.",
        "next_best_action": "Confirm source confidence on inherited and probate records.",
    },
    {
        "id": "seller-acquisition",
        "name": "Seller Acquisition Division",
        "manager_name": "Nadia Price",
        "responsibilities": [
            "Prepare seller scripts and draft-only touchpoints",
            "Surface motivation and objection notes",
            "Keep seller communication non-pressuring and owner-approved",
        ],
        "priority_queue": ["Offer explanation drafts", "Hot seller follow-ups", "Objection notes"],
        "workload": 9,
        "active_recommendations": ["Use repair-backed offer explanations on all offer_needed leads."],
        "risk_flags": ["no_live_outreach"],
        "performance_notes": "Strong draft quality; all outreach remains owner-controlled.",
        "next_best_action": "Prepare draft call notes for the two under-contract examples.",
    },
    {
        "id": "deal-underwriting",
        "name": "Deal Underwriting Division",
        "manager_name": "Theo Kim",
        "responsibilities": [
            "Estimate ARV, repairs, costs, MAO, confidence, and risk",
            "Require evidence for valuation assumptions",
            "Escalate gaps before any offer packet prep",
        ],
        "priority_queue": ["Repair basis review", "ARV confidence scoring", "MAO refresh"],
        "workload": 8,
        "active_recommendations": ["Hold low-confidence repair estimates out of offer prep."],
        "risk_flags": ["repair_scope_missing_photos"],
        "performance_notes": "Conservative formulas protect buyer margin.",
        "next_best_action": "Re-run MAO on deals with repair variance above 15%.",
    },
    {
        "id": "middle-man-profit-control",
        "name": "Middle-Man Profit Control Division",
        "manager_name": "Rina Patel",
        "responsibilities": [
            "Protect target assignment fee",
            "Keep seller offer ranges reasonable",
            "Block spreads that destroy buyer margin",
        ],
        "priority_queue": ["10K spread checks", "Aggressive-offer risk", "Buyer margin exception"],
        "workload": 6,
        "active_recommendations": ["Prioritize deals with 10K+ spread and clean buyer margin notes."],
        "risk_flags": ["one_deal_below_target_assignment_fee"],
        "performance_notes": "Spread calculations are direct and auditable.",
        "next_best_action": "Escalate any seller contract price above max seller offer.",
    },
    {
        "id": "buyer-disposition",
        "name": "Buyer Disposition Division",
        "manager_name": "Cam Jordan",
        "responsibilities": [
            "Rank cash buyer fit",
            "Check proof-of-funds status and reliability",
            "Prepare draft-only buyer blast content",
        ],
        "priority_queue": ["POF review", "Top buyer match", "Buyer demand strength"],
        "workload": 5,
        "active_recommendations": ["Use only verified POF buyers for under-contract opportunities."],
        "risk_flags": ["two_buyers_need_pof_refresh"],
        "performance_notes": "Reliability and closing speed are weighted ahead of broad blasts.",
        "next_best_action": "Prepare draft buyer match packet for deal-002 after compliance review.",
    },
    {
        "id": "contract-compliance",
        "name": "Contract & Compliance Division",
        "manager_name": "Selene Hart",
        "responsibilities": [
            "Prepare purchase and assignment checklists",
            "Flag state and disclosure risk",
            "Require attorney/title review reminders",
        ],
        "priority_queue": ["Assignment review", "Seller role disclosure", "Title prep"],
        "workload": 7,
        "active_recommendations": ["Block assignment packet prep until all confirmations are checked."],
        "risk_flags": ["state_specific_review_required"],
        "performance_notes": "Guardrails block execution-like actions by default.",
        "next_best_action": "Review the three compliance-risk examples before any packet prep.",
    },
    {
        "id": "follow-up",
        "name": "Follow-Up Division",
        "manager_name": "Ivy Chen",
        "responsibilities": [
            "Rank stale and hot follow-ups",
            "Prepare next-contact timing recommendations",
            "Keep touchpoints draft-only",
        ],
        "priority_queue": ["Hot lead reminders", "Stale lead recovery", "Next contact timing"],
        "workload": 10,
        "active_recommendations": ["Call-window recommendations require owner approval before action."],
        "risk_flags": ["stale_leads_need_owner_review"],
        "performance_notes": "Follow-up cadence is strong without automating outreach.",
        "next_best_action": "Move three warm leads into seller-followup priority.",
    },
    {
        "id": "operations-command",
        "name": "Operations Command Division",
        "manager_name": "Damon Reed",
        "responsibilities": [
            "Coordinate daily briefings and KPI readouts",
            "Route deals to the right division",
            "Escalate risk to Wholesale Prime and Owner",
        ],
        "priority_queue": ["Daily briefing", "Attention queue", "KPI review"],
        "workload": 6,
        "active_recommendations": ["Keep owner approval gates visible on all high-risk actions."],
        "risk_flags": ["owner_review_backlog"],
        "performance_notes": "Executive routing is clear and action-oriented.",
        "next_best_action": "Summarize top five actions for the owner.",
    },
]


AGENT_TEAMS = {
    "market-intelligence": [
        "Zip Code Demand Agent",
        "Comparable Sales Research Agent",
        "Rental Demand Agent",
        "Investor Activity Agent",
        "Market Heat Agent",
    ],
    "lead-intelligence": [
        "Distressed Property Agent",
        "Absentee Owner Agent",
        "Probate Lead Agent",
        "Tax Delinquent Agent",
        "Vacancy Signal Agent",
        "List Stacking Agent",
        "Contactability Agent",
    ],
    "seller-acquisition": [
        "Seller Script Agent",
        "Motivation Discovery Agent",
        "Objection Handling Agent",
        "Negotiation Prep Agent",
        "Offer Explanation Agent",
        "Seller Temperature Agent",
    ],
    "deal-underwriting": [
        "ARV Agent",
        "Repair Estimate Agent",
        "MAO Agent",
        "Risk Adjustment Agent",
        "Deal Confidence Agent",
    ],
    "middle-man-profit-control": [
        "Assignment Fee Agent",
        "Buyer Margin Protection Agent",
        "Seller Offer Reasonableness Agent",
        "Spread Optimization Agent",
        "Conservative Offer Agent",
        "Aggressive Offer Risk Agent",
    ],
    "buyer-disposition": [
        "Cash Buyer Match Agent",
        "Buyer Criteria Agent",
        "Buyer Reliability Agent",
        "Proof of Funds Agent",
        "Deal Blast Draft Agent",
        "Buyer Demand Agent",
    ],
    "contract-compliance": [
        "Purchase Agreement Checklist Agent",
        "Assignment Agreement Checklist Agent",
        "Title Company Prep Agent",
        "Disclosure Guard Agent",
        "State Compliance Risk Agent",
        "Misrepresentation Guard Agent",
    ],
    "follow-up": [
        "Follow-Up Priority Agent",
        "Stale Lead Recovery Agent",
        "Hot Lead Reminder Agent",
        "Seller Touchpoint Agent",
        "Next Contact Timing Agent",
    ],
    "operations-command": [
        "Daily Briefing Agent",
        "Attention Queue Agent",
        "KPI Agent",
        "Risk Escalation Agent",
        "Deal Commander Agent",
    ],
}


LEAD_ROWS = [
    ("lead-001", "Angela Ruiz", "4127 Bonnie View Rd", "Dallas", "TX", "75216", "single_family", "vacant", "offer_needed", 146000, 92000, 89, 83, 82, 77, 74, 86, 79, 91, 14),
    ("lead-002", "Milton Graves", "918 E Ann Arbor Ave", "Dallas", "TX", "75216", "single_family", "tax delinquent", "under_contract", 118000, 76000, 92, 88, 78, 84, 69, 90, 76, 88, 12),
    ("lead-003", "Patrice Nolan", "226 W Louisiana Ave", "Dallas", "TX", "75224", "single_family", "absentee owner", "negotiating", 188000, 121000, 80, 68, 86, 65, 71, 72, 82, 84, 18),
    ("lead-004", "Dennis Shaw", "5803 Pineland Dr", "Arlington", "TX", "76017", "single_family", "tired landlord", "follow_up", 135000, 88000, 76, 72, 81, 61, 80, 70, 78, 77, 15),
    ("lead-005", "Carmen Ellis", "1430 Stella Ave", "Dallas", "TX", "75216", "duplex", "inherited", "offer_needed", 231000, 158000, 86, 82, 88, 73, 64, 81, 72, 90, 28),
    ("lead-006", "Robert Gaines", "709 W 10th St", "Dallas", "TX", "75208", "single_family", "code violation", "researched", 164000, 91000, 74, 79, 72, 59, 58, 66, 69, 80, 35),
    ("lead-007", "Monica Bell", "3012 Alabama Ave", "Fort Worth", "TX", "76104", "single_family", "pre-foreclosure", "offer_sent", 99000, 62000, 91, 90, 70, 89, 65, 88, 75, 82, 22),
    ("lead-008", "Isaac Vaughn", "1846 Proctor St", "Dallas", "TX", "75208", "single_family", "probate", "under_contract", 171000, 109000, 84, 80, 82, 68, 60, 76, 66, 86, 46),
    ("lead-009", "Tanya Moss", "6451 Lazy River Dr", "Dallas", "TX", "75241", "single_family", "high equity", "new_lead", 125000, 98000, 64, 50, 90, 44, 72, 54, 70, 75, 10),
    ("lead-010", "Victor Hall", "7522 S Westmoreland Rd", "Dallas", "TX", "75237", "single_family", "driving for dollars", "contacted", 112000, 67000, 69, 74, 66, 58, 76, 63, 62, 79, 19),
    ("lead-011", "Naomi Finch", "330 Rosemont Ave", "Dallas", "TX", "75208", "single_family", "county records", "new_lead", 202000, 131000, 58, 41, 85, 36, 55, 49, 73, 83, 12),
    ("lead-012", "Owen Pierce", "2705 Kathleen Ave", "Dallas", "TX", "75216", "single_family", "absentee owner", "follow_up", 132000, 84000, 72, 61, 79, 57, 84, 68, 77, 89, 13),
    ("lead-013", "Bianca Rowe", "4509 Tacoma St", "Dallas", "TX", "75216", "single_family", "vacant", "researched", 101000, 73000, 78, 84, 74, 64, 62, 71, 68, 88, 16),
    ("lead-014", "Harold Banks", "1815 Woodin Blvd", "Dallas", "TX", "75216", "single_family", "tax delinquent", "dead", 97000, 34000, 44, 52, 39, 48, 35, 39, 60, 70, 25),
    ("lead-015", "Erica Stanley", "1022 E Arlington Ave", "Fort Worth", "TX", "76104", "duplex", "tired landlord", "negotiating", 155000, 97000, 75, 70, 82, 62, 74, 68, 74, 78, 17),
    ("lead-016", "Gerald Cooper", "6707 Umphress Rd", "Dallas", "TX", "75217", "single_family", "code violation", "offer_needed", 119000, 82000, 82, 86, 76, 71, 57, 79, 67, 81, 30),
    ("lead-017", "Janet Ford", "2409 Wilhurt Ave", "Dallas", "TX", "75216", "single_family", "high equity", "researched", 143000, 112000, 66, 49, 92, 42, 61, 53, 78, 87, 11),
    ("lead-018", "Marcus Lee", "3930 W Illinois Ave", "Dallas", "TX", "75211", "single_family", "vacant", "follow_up", 150000, 96000, 79, 83, 80, 67, 70, 75, 71, 82, 14),
    ("lead-019", "Yvette Cruz", "5215 Bexar St", "Dallas", "TX", "75215", "single_family", "probate", "new_lead", 138000, 101000, 73, 76, 85, 55, 49, 62, 58, 80, 44),
    ("lead-020", "Caleb Morris", "8731 Diceman Dr", "Dallas", "TX", "75218", "single_family", "inherited", "contacted", 246000, 174000, 63, 54, 88, 40, 66, 57, 65, 76, 21),
    ("lead-021", "Lucia Hunt", "1115 E Baltimore Ave", "Fort Worth", "TX", "76104", "single_family", "pre-foreclosure", "follow_up", 103000, 69000, 88, 89, 71, 85, 59, 84, 70, 79, 24),
    ("lead-022", "Arthur Mills", "3726 Waldorf Dr", "Dallas", "TX", "75229", "single_family", "absentee owner", "researched", 310000, 210000, 55, 38, 91, 34, 52, 46, 80, 70, 9),
    ("lead-023", "Maya Flores", "4920 Bernal Dr", "Dallas", "TX", "75212", "single_family", "driving for dollars", "new_lead", 122000, 82000, 68, 72, 73, 50, 73, 61, 64, 84, 16),
    ("lead-024", "Frankie Brooks", "8406 Jennie Lee Ln", "Dallas", "TX", "75227", "single_family", "county records", "contacted", 128000, 79000, 61, 45, 77, 38, 68, 51, 70, 74, 12),
    ("lead-025", "Helena Stone", "609 W Boyce Ave", "Fort Worth", "TX", "76115", "single_family", "tax delinquent", "offer_sent", 108000, 69000, 83, 86, 73, 74, 64, 80, 72, 77, 22),
    ("lead-026", "Quinn Davis", "1528 Garrison St", "Dallas", "TX", "75216", "single_family", "vacant", "follow_up", 116000, 88000, 70, 81, 84, 58, 56, 65, 62, 86, 15),
    ("lead-027", "Sofia Nguyen", "2119 Bickers St", "Dallas", "TX", "75212", "duplex", "tired landlord", "researched", 172000, 118000, 77, 67, 83, 59, 72, 70, 76, 83, 18),
    ("lead-028", "Eddie Ramos", "4157 Copeland St", "Dallas", "TX", "75210", "single_family", "code violation", "new_lead", 96000, 59000, 71, 85, 68, 63, 48, 66, 61, 73, 31),
    ("lead-029", "Ruth Wallace", "9712 Brockbank Dr", "Dallas", "TX", "75220", "single_family", "high equity", "follow_up", 274000, 195000, 57, 42, 90, 35, 60, 47, 79, 68, 10),
    ("lead-030", "Jon Price", "3611 Easter Ave", "Dallas", "TX", "75216", "single_family", "probate", "researched", 129000, 93000, 74, 78, 82, 56, 50, 63, 63, 87, 42),
]


BUYER_ROWS = [
    ("buyer-001", "Jules Avery", "Avery Cash Homes", "jules@example.test", "214-555-0101", ["75216", "75224", "75208"], 210000, "single_family", "verified", 10, 94, "Closed three assignments within 12 days.", "assignment"),
    ("buyer-002", "Priya Shah", "Oakline Investments", "priya@example.test", "214-555-0102", ["75216", "75241"], 150000, "single_family", "verified", 7, 91, "Fast closings and clean title deposits.", "assignment"),
    ("buyer-003", "Marcus Wade", "Wade Urban Renewal", "marcus@example.test", "817-555-0103", ["76104", "76115"], 140000, "single_family", "needs_refresh", 14, 82, "Reliable, POF refresh needed this month.", "assignment"),
    ("buyer-004", "Simone Clark", "Clark Bridge Capital", "simone@example.test", "214-555-0104", ["75216", "75208", "75212"], 260000, "duplex", "verified", 12, 88, "Prefers duplexes and inherited property discounts.", "assignment"),
    ("buyer-005", "Leo Martin", "Northline Rehabs", "leo@example.test", "972-555-0105", ["75229", "75220", "75218"], 360000, "single_family", "verified", 21, 78, "Strong capital, slower closing operations.", "assignment"),
    ("buyer-006", "Adriana Cole", "Cole Equity Homes", "adriana@example.test", "469-555-0106", ["75211", "75212", "75210"], 175000, "single_family", "verified", 9, 86, "Good at rougher repair scopes.", "assignment"),
    ("buyer-007", "Malik Stone", "Stone Porch Properties", "malik@example.test", "214-555-0107", ["75217", "75227"], 135000, "single_family", "unverified", 16, 74, "Responsive but POF not yet reviewed.", "assignment"),
    ("buyer-008", "Tessa Young", "Southcrest Buyers", "tessa@example.test", "817-555-0108", ["76104", "75216"], 120000, "any", "verified", 8, 83, "Buys small single-family and light duplex deals.", "assignment"),
    ("buyer-009", "Grant Miller", "Miller Rental Group", "grant@example.test", "214-555-0109", ["75237", "75241"], 125000, "single_family", "verified", 18, 80, "Rental buyer; needs clean rent comps.", "assignment"),
    ("buyer-010", "Keisha King", "King Cash Acquisitions", "keisha@example.test", "972-555-0110", ["75215", "75216", "75210"], 155000, "single_family", "needs_refresh", 11, 81, "Good demand, requires disclosure review before draft blast.", "assignment"),
]


DEAL_ROWS = [
    ("deal-001", "lead-001", "offer_needed", 275000, 45000, 6000, 6000, 45000, 151000, 166000, 15, 88, False, True),
    ("deal-002", "lead-002", "under_contract", 210000, 32000, 4500, 4500, 35000, 112000, 127000, 12, 91, True, True),
    ("deal-003", "lead-003", "negotiating", 340000, 65000, 7500, 7500, 55000, 180000, 193000, 18, 84, False, True),
    ("deal-004", "lead-004", "follow_up", 185000, 28000, 4000, 4000, 30000, 100000, 111000, 20, 79, False, True),
    ("deal-005", "lead-005", "offer_needed", 425000, 90000, 10000, 10000, 70000, 220000, 235000, 35, 76, False, True),
    ("deal-006", "lead-006", "researched", 260000, 70000, 6000, 6000, 40000, 132000, 140000, 48, 62, False, False),
    ("deal-007", "lead-007", "offer_sent", 155000, 30000, 4000, 4000, 25000, 75000, 84000, 24, 67, False, False),
    ("deal-008", "lead-008", "under_contract", 310000, 55000, 7000, 7000, 50000, 168000, 180000, 58, 66, True, False),
]


def slug_agent(name: str) -> str:
    return name.lower().replace("&", "and").replace(" ", "-")


def build_agents() -> list[dict[str, object]]:
    agents: list[dict[str, object]] = []
    for division_id, names in AGENT_TEAMS.items():
        for name in names:
            agents.append(
                {
                    "id": slug_agent(name),
                    "name": name,
                    "division_id": division_id,
                    "allowed_actions": sorted(ANALYSIS_ONLY_ACTIONS),
                    "denied_actions": sorted(BLOCKED_ACTIONS),
                    "current_focus": f"{name} is reviewing active queues for {division_id.replace('-', ' ')}.",
                    "recommendation": "Recommend, draft, score, escalate, or flag risk only.",
                    "risk_flags": [],
                    "status": "active",
                }
            )
    return agents


def build_lead_records() -> list[dict[str, object]]:
    leads: list[dict[str, object]] = []
    for row in LEAD_ROWS:
        (
            lead_id,
            seller_name,
            address,
            city,
            state,
            zip_code,
            property_type,
            source_category,
            stage,
            asking_price,
            estimated_equity,
            motivation,
            distress,
            equity,
            urgency,
            contactability,
            seller_temperature,
            data_confidence,
            market_demand,
            compliance_risk,
        ) = row
        opportunity_score = calculate_lead_opportunity(
            {
                "motivation": motivation,
                "distress_signals": distress,
                "equity": equity,
                "urgency": urgency,
                "contactability": contactability,
                "seller_temperature": seller_temperature,
                "data_confidence": data_confidence,
                "market_demand": market_demand,
            }
        )
        leads.append(
            {
                "id": lead_id,
                "seller_name": seller_name,
                "address": address,
                "city": city,
                "state": state,
                "zip_code": zip_code,
                "property_type": property_type,
                "source_category": source_category,
                "stage": stage,
                "asking_price": asking_price,
                "estimated_equity": estimated_equity,
                "motivation_score": motivation,
                "distress_score": distress,
                "equity_score": equity,
                "urgency_score": urgency,
                "contactability_score": contactability,
                "seller_temperature": seller_temperature,
                "data_confidence": data_confidence,
                "market_demand": market_demand,
                "opportunity_score": opportunity_score,
                "compliance_risk": compliance_risk,
                "notes": [
                    f"Source: {source_category}",
                    "No live outreach; owner approval required before real-world action.",
                ],
                "next_best_action": "Research, score, draft, or escalate based on stage.",
            }
        )
    return leads


def build_buyer_records() -> list[dict[str, object]]:
    return [
        {
            "id": buyer_id,
            "name": name,
            "company": company,
            "email": email,
            "phone": phone,
            "target_zip_codes": zip_codes,
            "max_purchase_price": max_price,
            "property_type": property_type,
            "proof_of_funds_status": proof_status,
            "closing_speed_days": closing_days,
            "reliability_score": reliability,
            "past_performance": past_performance,
            "preferred_deal_type": preferred_deal_type,
            "active": True,
        }
        for (
            buyer_id,
            name,
            company,
            email,
            phone,
            zip_codes,
            max_price,
            property_type,
            proof_status,
            closing_days,
            reliability,
            past_performance,
            preferred_deal_type,
        ) in BUYER_ROWS
    ]


def build_deal_records(leads_by_id: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    deals: list[dict[str, object]] = []
    for row in DEAL_ROWS:
        (
            deal_id,
            lead_id,
            status,
            arv,
            repairs,
            buyer_closing_costs,
            buyer_holding_costs,
            buyer_desired_profit,
            seller_contract_price,
            buyer_purchase_price,
            compliance_risk,
            confidence_score,
            under_contract,
            hot,
        ) = row
        lead = leads_by_id[lead_id]
        result = calculate_profit_control(
            ProfitControlInput(
                arv=arv,
                estimated_repairs=repairs,
                buyer_desired_profit=buyer_desired_profit,
                buyer_closing_costs=buyer_closing_costs,
                buyer_holding_costs=buyer_holding_costs,
                seller_contract_price=seller_contract_price,
                buyer_purchase_price=buyer_purchase_price,
            )
        )
        speed = deal_speed_score(
            lead["motivation_score"],
            lead["equity_score"],
            lead["market_demand"],
            lead["contactability_score"],
            compliance_risk,
        )
        deals.append(
            {
                "id": deal_id,
                "lead_id": lead_id,
                "status": status,
                "arv": arv,
                "repairs": repairs,
                "buyer_costs": result["buyer_costs"],
                "buyer_desired_profit": buyer_desired_profit,
                "target_assignment_fee": result["target_assignment_fee"],
                "max_buyer_purchase_price": result["max_buyer_purchase_price"],
                "max_seller_offer": result["max_seller_offer"],
                "seller_contract_price": result["seller_contract_price"],
                "buyer_purchase_price": result["buyer_purchase_price"],
                "projected_assignment_fee": result["projected_assignment_fee"],
                "offer_reasonableness_score": result["offer_reasonableness_score"],
                "spread_confidence_score": result["spread_confidence_score"],
                "risk_score": compliance_risk,
                "confidence_score": confidence_score,
                "deal_speed_score": speed,
                "risk_flags": result["risk_flags"],
                "underwriting_notes": "ARV and repair estimates require documented comps and repair basis.",
                "seller_fairness_notes": result["seller_fairness_notes"],
                "buyer_margin_notes": result["buyer_margin_notes"],
                "conservative_offer": result["offer_options"]["conservative"],
                "standard_offer": result["offer_options"]["standard"],
                "aggressive_offer": result["offer_options"]["aggressive"],
                "owner_approval_required": True,
                "compliance_review_required": True,
                "is_hot_opportunity": bool(hot),
                "is_under_contract": bool(under_contract),
            }
        )
    return deals


def build_compliance_records() -> list[dict[str, object]]:
    return [
        {
            "id": "compliance-001",
            "deal_id": "deal-005",
            "title": "Inherited property authority review",
            "status": "needs_review",
            "required_confirmations": REQUIRED_CONFIRMATIONS,
            "risk_warnings": ["seller_authority_unverified", "state_specific_review_required"],
            "blocked_actions": ["prepare_assignment_packet", "execute_contract"],
            "attorney_title_review_required": True,
            "notes": "Confirm heirs, authority, and title route before assignment prep.",
        },
        {
            "id": "compliance-002",
            "deal_id": "deal-006",
            "title": "Buyer margin protection exception",
            "status": "needs_review",
            "required_confirmations": REQUIRED_CONFIRMATIONS,
            "risk_warnings": ["seller_offer_exceeds_margin_safe_max", "buyer_margin_below_desired_profit"],
            "blocked_actions": ["prepare_offer_packet", "buyer_blast_execute"],
            "attorney_title_review_required": True,
            "notes": "Seller contract price exceeds the computed safe max seller offer.",
        },
        {
            "id": "compliance-003",
            "deal_id": "deal-008",
            "title": "Assignment and role disclosure review",
            "status": "needs_review",
            "required_confirmations": REQUIRED_CONFIRMATIONS,
            "risk_warnings": ["probate_authority_unverified", "assignment_fee_disclosure_review"],
            "blocked_actions": ["prepare_assignment_packet", "execute_contract"],
            "attorney_title_review_required": True,
            "notes": "Under contract example stays blocked until disclosure and title review are documented.",
        },
    ]


def build_match_records(
    deals_by_id: dict[str, dict[str, object]], buyers_by_id: dict[str, dict[str, object]]
) -> list[dict[str, object]]:
    pairs = [("match-001", "deal-001", "buyer-001"), ("match-002", "deal-002", "buyer-002"), ("match-003", "deal-005", "buyer-004")]
    matches = []
    for match_id, deal_id, buyer_id in pairs:
        deal = deals_by_id[deal_id]
        buyer = buyers_by_id[buyer_id]
        enriched_deal = {
            **deal,
            "zip_code": LEAD_LOOKUP[deal["lead_id"]]["zip_code"],
            "property_type": LEAD_LOOKUP[deal["lead_id"]]["property_type"],
        }
        result = score_buyer_match(enriched_deal, buyer)
        matches.append(
            {
                "id": match_id,
                "deal_id": deal_id,
                "buyer_id": buyer_id,
                "score": result["score"],
                "match_reasons": result["match_reasons"],
                "risk_flags": result["risk_flags"],
                "draft_only": True,
                "status": "draft_match",
            }
        )
    return matches


def build_publication_records(
    deals_by_id: dict[str, dict[str, object]]
) -> list[dict[str, object]]:
    property_details = {
        "deal-001": (3, 2.0, 1420, 263000, 287000, 39000, 51000, True, True, "low", "strong"),
        "deal-002": (3, 1.5, 1285, 201000, 219000, 28000, 36000, True, True, "low", "strong"),
        "deal-003": (4, 2.0, 1840, 326000, 354000, 58000, 72000, True, True, "medium", "strong"),
        "deal-004": (3, 2.0, 1315, 176000, 194000, 24000, 33000, False, True, "medium", "strong"),
        "deal-005": (4, 2.5, 2260, 405000, 445000, 80000, 102000, True, False, "high", "strong"),
        "deal-006": (3, 1.0, 1180, 248000, 272000, 64000, 78000, True, True, "high", "weak"),
        "deal-007": (2, 1.0, 980, 148000, 162000, 26000, 34000, True, False, "medium", "weak"),
        "deal-008": (4, 2.0, 1710, 296000, 324000, 48000, 62000, True, False, "high", "strong"),
    }
    records = []
    for deal_id, deal in deals_by_id.items():
        (
            beds,
            baths,
            sqft,
            arv_low,
            arv_high,
            repair_low,
            repair_high,
            seller_contract_controlled,
            compliance_reviewed,
            risk_status,
            buyer_margin_status,
        ) = property_details[deal_id]
        asking_price = deal["buyer_purchase_price"]
        estimated_margin = deal["arv"] - deal["repairs"] - deal["buyer_costs"] - asking_price
        operator_marked_visible = deal_id in {"deal-001", "deal-002", "deal-003", "deal-004", "deal-005", "deal-006", "deal-008"}
        records.append(
            {
                "id": f"publication-{deal_id[-3:]}",
                "deal_id": deal_id,
                "operator_marked_visible": operator_marked_visible,
                "compliance_reviewed": compliance_reviewed,
                "seller_contract_controlled": seller_contract_controlled,
                "risk_status": risk_status,
                "availability_status": "available" if operator_marked_visible else "draft",
                "asking_price": asking_price,
                "beds": beds,
                "baths": baths,
                "sqft": sqft,
                "arv_low": arv_low,
                "arv_high": arv_high,
                "repair_low": repair_low,
                "repair_high": repair_high,
                "estimated_buyer_margin": estimated_margin,
                "buyer_margin_status": buyer_margin_status,
                "photos_placeholder": [
                    "Exterior photo placeholder",
                    "Kitchen photo placeholder",
                    "Mechanical photo placeholder",
                ],
                "access_instructions_placeholder": "Access instructions available after owner review of buyer intent and proof of funds.",
                "blocked_reasons": [],
                "published_at": None,
            }
        )
    return records


def build_interest_records() -> list[dict[str, object]]:
    return [
        {
            "id": "interest-001",
            "buyer_id": "buyer-001",
            "deal_id": "deal-001",
            "interest_status": "owner_review_needed",
            "intended_offer_amount": 166000,
            "proof_of_funds_status": "verified",
            "notes": "Buyer intent recorded as draft only; no contract or payment action.",
            "draft_only": True,
            "contract_execution_allowed": False,
        },
        {
            "id": "interest-002",
            "buyer_id": "buyer-002",
            "deal_id": "deal-002",
            "interest_status": "proof_of_funds_verified",
            "intended_offer_amount": 127000,
            "proof_of_funds_status": "verified",
            "notes": "Owner review needed before any external follow-up.",
            "draft_only": True,
            "contract_execution_allowed": False,
        },
        {
            "id": "interest-003",
            "buyer_id": "buyer-003",
            "deal_id": "deal-003",
            "interest_status": "proof_of_funds_needed",
            "intended_offer_amount": 193000,
            "proof_of_funds_status": "needs_refresh",
            "notes": "POF refresh required; buyer interest is non-binding.",
            "draft_only": True,
            "contract_execution_allowed": False,
        },
        {
            "id": "interest-004",
            "buyer_id": "buyer-003",
            "deal_id": "deal-001",
            "interest_status": "proof_of_funds_needed",
            "intended_offer_amount": 166000,
            "proof_of_funds_status": "needs_refresh",
            "notes": "V4 readiness example: buyer intent exists but POF refresh blocks assignment readiness.",
            "draft_only": True,
            "contract_execution_allowed": False,
        },
        {
            "id": "interest-005",
            "buyer_id": "buyer-004",
            "deal_id": "deal-005",
            "interest_status": "owner_review_needed",
            "intended_offer_amount": 235000,
            "proof_of_funds_status": "verified",
            "notes": "V4 readiness example: buyer intent exists while compliance review remains blocked.",
            "draft_only": True,
            "contract_execution_allowed": False,
        },
    ]


def build_seller_interaction_records() -> list[dict[str, object]]:
    return [
        {
            "id": "seller-interaction-001",
            "lead_id": "lead-001",
            "call_notes": "Seller wants a clean as-is option and asked how repairs affect price.",
            "motivation_answers": {
                "why_sell": "Vacant property is becoming hard to maintain",
                "timeline": "Would like clarity this week",
                "decision_maker": "Seller is primary decision maker",
            },
            "asking_price": 146000,
            "timeline": "7-14 days",
            "property_condition": "Deferred exterior maintenance, kitchen dated, HVAC age unknown.",
            "pain_points": ["vacancy", "maintenance", "uncertain repairs"],
            "objections": ["wants to understand offer math"],
            "next_follow_up_date": datetime(2026, 5, 3, tzinfo=UTC),
            "seller_temperature_score": 91,
            "objection_status": "pricing_needs_explanation",
            "follow_up_urgency": "hot",
            "next_best_seller_action": "Prepare draft offer explanation after owner review.",
            "draft_only": True,
            "live_outreach_allowed": False,
        },
        {
            "id": "seller-interaction-002",
            "lead_id": "lead-002",
            "call_notes": "Seller is open to assignment process after role is explained clearly.",
            "motivation_answers": {
                "why_sell": "Tax pressure and property fatigue",
                "timeline": "Fast but wants clear next steps",
                "decision_maker": "Seller plus spouse",
            },
            "asking_price": 118000,
            "timeline": "under 10 days",
            "property_condition": "Moderate repairs, roof age needs confirmation.",
            "pain_points": ["tax pressure", "time", "repair uncertainty"],
            "objections": ["needs role disclosure in plain language"],
            "next_follow_up_date": datetime(2026, 5, 4, tzinfo=UTC),
            "seller_temperature_score": 94,
            "objection_status": "role_disclosure_needed",
            "follow_up_urgency": "hot",
            "next_best_seller_action": "Compliance-safe assignment role explanation draft.",
            "draft_only": True,
            "live_outreach_allowed": False,
        },
        {
            "id": "seller-interaction-003",
            "lead_id": "lead-003",
            "call_notes": "Seller has a higher price expectation but will review repair-backed logic.",
            "motivation_answers": {
                "why_sell": "Absentee ownership burden",
                "timeline": "30 days",
                "decision_maker": "Seller only",
            },
            "asking_price": 188000,
            "timeline": "30 days",
            "property_condition": "Cosmetic updates plus possible plumbing work.",
            "pain_points": ["distance", "tenant turnover", "pricing uncertainty"],
            "objections": ["price expectation"],
            "next_follow_up_date": datetime(2026, 5, 2, tzinfo=UTC),
            "seller_temperature_score": 79,
            "objection_status": "price_gap",
            "follow_up_urgency": "high",
            "next_best_seller_action": "Draft objection response with no pressure.",
            "draft_only": True,
            "live_outreach_allowed": False,
        },
        {
            "id": "seller-interaction-004",
            "lead_id": "lead-005",
            "call_notes": "Inherited property seller needs authority and title path clarified before offer.",
            "motivation_answers": {
                "why_sell": "Family wants to settle property decision",
                "timeline": "2-4 weeks",
                "decision_maker": "Multiple heirs possible",
            },
            "asking_price": 231000,
            "timeline": "2-4 weeks",
            "property_condition": "Large repair scope, occupancy status needs confirmation.",
            "pain_points": ["inheritance complexity", "repair scope", "family coordination"],
            "objections": ["authority questions"],
            "next_follow_up_date": datetime(2026, 5, 6, tzinfo=UTC),
            "seller_temperature_score": 82,
            "objection_status": "authority_review",
            "follow_up_urgency": "high",
            "next_best_seller_action": "Escalate to compliance before offer packet.",
            "draft_only": True,
            "live_outreach_allowed": False,
        },
        {
            "id": "seller-interaction-005",
            "lead_id": "lead-007",
            "call_notes": "Seller is stressed by timeline and needs a calm follow-up.",
            "motivation_answers": {
                "why_sell": "Payment pressure",
                "timeline": "urgent",
                "decision_maker": "Seller only",
            },
            "asking_price": 99000,
            "timeline": "urgent but unverified",
            "property_condition": "Small house, repairs likely moderate.",
            "pain_points": ["payment pressure", "uncertainty", "time"],
            "objections": ["needs confidence buyer can close"],
            "next_follow_up_date": datetime(2026, 5, 1, tzinfo=UTC),
            "seller_temperature_score": 88,
            "objection_status": "closing_confidence",
            "follow_up_urgency": "hot",
            "next_best_seller_action": "Draft calm follow-up; avoid urgency or guarantees.",
            "draft_only": True,
            "live_outreach_allowed": False,
        },
        {
            "id": "seller-interaction-006",
            "lead_id": "lead-008",
            "call_notes": "Probate path and disclosure review must be clarified before assignment prep.",
            "motivation_answers": {
                "why_sell": "Estate administration",
                "timeline": "depends on title",
                "decision_maker": "Representative authority needs confirmation",
            },
            "asking_price": 171000,
            "timeline": "title-dependent",
            "property_condition": "Repairs likely heavy but ARV supports continued review.",
            "pain_points": ["probate", "title", "repair scope"],
            "objections": ["authority and paperwork"],
            "next_follow_up_date": datetime(2026, 5, 5, tzinfo=UTC),
            "seller_temperature_score": 76,
            "objection_status": "compliance_review",
            "follow_up_urgency": "normal",
            "next_best_seller_action": "Hold until compliance review is complete.",
            "draft_only": True,
            "live_outreach_allowed": False,
        },
    ]


def build_offer_packet_records() -> list[dict[str, object]]:
    return [
        {
            "id": "packet-001",
            "deal_id": "deal-001",
            "packet_status": "draft_ready",
            "owner_approval_recorded": True,
            "compliance_guard_passed": True,
            "buyer_margin_protected": True,
            "target_assignment_fee_checked": True,
            "underwriting_complete": True,
            "packet_prep_allowed": True,
            "blocked_reasons": [],
            "approval_status": "owner_approved_draft_ready",
            "draft_summary": "Draft offer packet may be prepared for owner review only.",
            "draft_only": True,
            "real_world_action_taken": False,
        },
        {
            "id": "packet-002",
            "deal_id": "deal-003",
            "packet_status": "blocked",
            "owner_approval_recorded": False,
            "compliance_guard_passed": True,
            "buyer_margin_protected": True,
            "target_assignment_fee_checked": True,
            "underwriting_complete": True,
            "packet_prep_allowed": False,
            "blocked_reasons": ["owner_approval_not_recorded"],
            "approval_status": "owner_review_required",
            "draft_summary": "Owner approval needed before offer packet prep.",
            "draft_only": True,
            "real_world_action_taken": False,
        },
        {
            "id": "packet-003",
            "deal_id": "deal-005",
            "packet_status": "blocked",
            "owner_approval_recorded": True,
            "compliance_guard_passed": False,
            "buyer_margin_protected": True,
            "target_assignment_fee_checked": True,
            "underwriting_complete": True,
            "packet_prep_allowed": False,
            "blocked_reasons": ["compliance_guard_not_passed"],
            "approval_status": "blocked",
            "draft_summary": "Inherited-property authority review blocks offer packet prep.",
            "draft_only": True,
            "real_world_action_taken": False,
        },
        {
            "id": "packet-004",
            "deal_id": "deal-006",
            "packet_status": "blocked",
            "owner_approval_recorded": True,
            "compliance_guard_passed": True,
            "buyer_margin_protected": False,
            "target_assignment_fee_checked": False,
            "underwriting_complete": True,
            "packet_prep_allowed": False,
            "blocked_reasons": ["buyer_margin_not_protected", "target_assignment_fee_not_checked"],
            "approval_status": "blocked",
            "draft_summary": "Buyer margin and target assignment fee fail the gate.",
            "draft_only": True,
            "real_world_action_taken": False,
        },
        {
            "id": "packet-005",
            "deal_id": "deal-007",
            "packet_status": "blocked",
            "owner_approval_recorded": True,
            "compliance_guard_passed": True,
            "buyer_margin_protected": True,
            "target_assignment_fee_checked": False,
            "underwriting_complete": True,
            "packet_prep_allowed": False,
            "blocked_reasons": ["target_assignment_fee_not_checked"],
            "approval_status": "blocked",
            "draft_summary": "Projected assignment fee is below target.",
            "draft_only": True,
            "real_world_action_taken": False,
        },
    ]


CONTRACT_DOCUMENT_CHECKLIST = [
    "seller accepted terms captured",
    "property details verified",
    "assignment language review required",
    "seller role disclosure reminder",
    "attorney/title review reminder",
]


def build_contract_control_records() -> list[dict[str, object]]:
    return [
        {
            "id": "contract-001",
            "lead_id": "lead-001",
            "deal_id": "deal-001",
            "offer_packet_id": "packet-001",
            "seller_accepted_terms": {
                "price": 151000,
                "closing_timeline": "14-21 days",
                "seller_acknowledges_draft_only": True,
            },
            "contract_status": "prep_review",
            "assignment_allowed_flag": True,
            "inspection_access_notes": "Access instructions are placeholders until owner confirms next step.",
            "earnest_money_notes": "EMD amount to be reviewed by owner and title/attorney before any action.",
            "closing_timeline": "14-21 days",
            "title_company_preference": "Owner-selected investor-friendly title company placeholder",
            "required_documents_checklist": CONTRACT_DOCUMENT_CHECKLIST,
            "owner_approval_status": "approved",
            "compliance_review_status": "approved",
            "contract_prep_allowed": True,
            "blocked_reasons": [],
            "draft_only": True,
            "executable_contract_generated": False,
            "live_sending_allowed": False,
            "title_submission_allowed": False,
            "automatic_status_change_allowed": False,
        },
        {
            "id": "contract-002",
            "lead_id": "lead-003",
            "deal_id": "deal-003",
            "offer_packet_id": "packet-002",
            "seller_accepted_terms": {
                "price": 180000,
                "closing_timeline": "30 days",
                "seller_acknowledges_draft_only": True,
            },
            "contract_status": "prep_review",
            "assignment_allowed_flag": True,
            "inspection_access_notes": "Seller will review access options after owner approval.",
            "earnest_money_notes": "Draft-only EMD note; no funds are collected in V4.",
            "closing_timeline": "30 days",
            "title_company_preference": "Title preference pending owner confirmation",
            "required_documents_checklist": CONTRACT_DOCUMENT_CHECKLIST,
            "owner_approval_status": "pending",
            "compliance_review_status": "approved",
            "contract_prep_allowed": False,
            "blocked_reasons": ["offer_packet_not_approved", "owner_approval_not_recorded"],
            "draft_only": True,
            "executable_contract_generated": False,
            "live_sending_allowed": False,
            "title_submission_allowed": False,
            "automatic_status_change_allowed": False,
        },
        {
            "id": "contract-003",
            "lead_id": "lead-005",
            "deal_id": "deal-005",
            "offer_packet_id": "packet-003",
            "seller_accepted_terms": {
                "price": 220000,
                "closing_timeline": "21-30 days",
                "seller_acknowledges_draft_only": True,
            },
            "contract_status": "prep_review",
            "assignment_allowed_flag": False,
            "inspection_access_notes": "Access blocked until authority and compliance review clear.",
            "earnest_money_notes": "No EMD action until title/attorney review.",
            "closing_timeline": "21-30 days",
            "title_company_preference": "Missing title company preference",
            "required_documents_checklist": CONTRACT_DOCUMENT_CHECKLIST
            + ["missing seller authority documentation"],
            "owner_approval_status": "approved",
            "compliance_review_status": "pending",
            "contract_prep_allowed": False,
            "blocked_reasons": ["compliance_guard_not_passed"],
            "draft_only": True,
            "executable_contract_generated": False,
            "live_sending_allowed": False,
            "title_submission_allowed": False,
            "automatic_status_change_allowed": False,
        },
        {
            "id": "contract-004",
            "lead_id": "lead-006",
            "deal_id": "deal-006",
            "offer_packet_id": "packet-004",
            "seller_accepted_terms": {},
            "contract_status": "blocked",
            "assignment_allowed_flag": False,
            "inspection_access_notes": "No accepted terms; contract prep blocked.",
            "earnest_money_notes": "No EMD action.",
            "closing_timeline": "",
            "title_company_preference": "",
            "required_documents_checklist": CONTRACT_DOCUMENT_CHECKLIST
            + ["missing seller accepted terms", "missing title company preference"],
            "owner_approval_status": "approved",
            "compliance_review_status": "approved",
            "contract_prep_allowed": False,
            "blocked_reasons": [
                "seller_accepted_terms_missing",
                "buyer_margin_not_protected",
                "offer_packet_not_approved",
            ],
            "draft_only": True,
            "executable_contract_generated": False,
            "live_sending_allowed": False,
            "title_submission_allowed": False,
            "automatic_status_change_allowed": False,
        },
        {
            "id": "contract-005",
            "lead_id": "lead-007",
            "deal_id": "deal-007",
            "offer_packet_id": "packet-005",
            "seller_accepted_terms": {
                "price": 75000,
                "closing_timeline": "10-14 days",
                "seller_acknowledges_draft_only": True,
            },
            "contract_status": "prep_review",
            "assignment_allowed_flag": True,
            "inspection_access_notes": "Access notes held for owner review; no live scheduling.",
            "earnest_money_notes": "No EMD action; target assignment fee remains below threshold.",
            "closing_timeline": "10-14 days",
            "title_company_preference": "Title preference pending compliance review",
            "required_documents_checklist": CONTRACT_DOCUMENT_CHECKLIST,
            "owner_approval_status": "approved",
            "compliance_review_status": "approved",
            "contract_prep_allowed": False,
            "blocked_reasons": ["offer_packet_not_approved"],
            "draft_only": True,
            "executable_contract_generated": False,
            "live_sending_allowed": False,
            "title_submission_allowed": False,
            "automatic_status_change_allowed": False,
        },
    ]


def build_title_handoff_records() -> list[dict[str, object]]:
    return [
        {
            "id": "title-001",
            "contract_control_id": "contract-001",
            "deal_id": "deal-001",
            "property_details": {
                "city": "Dallas",
                "state": "TX",
                "zip": "75216",
                "property_type": "single_family",
            },
            "seller_info_placeholder": "Seller info placeholder; verify before any title-company contact.",
            "buyer_entity_info_placeholder": "Buyer/entity info placeholder; owner must confirm before use.",
            "agreed_price": 151000,
            "closing_timeline": "14-21 days",
            "access_notes": "Access notes remain placeholders until owner-approved next step.",
            "assignment_status": "assignment_allowed_reviewed",
            "required_document_checklist": CONTRACT_DOCUMENT_CHECKLIST,
            "attorney_title_review_reminder": "Attorney/title review required before any real-world contract or handoff action.",
            "packet_status": "draft_ready",
            "draft_only": True,
            "title_submission_allowed": False,
            "submitted_to_title": False,
            "legal_advice_provided": False,
        },
        {
            "id": "title-002",
            "contract_control_id": "contract-002",
            "deal_id": "deal-003",
            "property_details": {
                "city": "Dallas",
                "state": "TX",
                "zip": "75224",
                "property_type": "single_family",
            },
            "seller_info_placeholder": "Seller info placeholder; owner approval is still pending.",
            "buyer_entity_info_placeholder": "Buyer/entity info placeholder; no title submission.",
            "agreed_price": 180000,
            "closing_timeline": "30 days",
            "access_notes": "Access instructions require owner review.",
            "assignment_status": "owner_review_required",
            "required_document_checklist": CONTRACT_DOCUMENT_CHECKLIST,
            "attorney_title_review_reminder": "Attorney/title review reminder only; no legal advice.",
            "packet_status": "blocked_owner_review",
            "draft_only": True,
            "title_submission_allowed": False,
            "submitted_to_title": False,
            "legal_advice_provided": False,
        },
        {
            "id": "title-003",
            "contract_control_id": "contract-003",
            "deal_id": "deal-005",
            "property_details": {
                "city": "Dallas",
                "state": "TX",
                "zip": "75216",
                "property_type": "duplex",
            },
            "seller_info_placeholder": "Seller authority placeholder; heirs/title path must be reviewed.",
            "buyer_entity_info_placeholder": "Buyer/entity info placeholder; blocked until compliance clears.",
            "agreed_price": 220000,
            "closing_timeline": "21-30 days",
            "access_notes": "Access blocked until compliance review.",
            "assignment_status": "compliance_blocked",
            "required_document_checklist": CONTRACT_DOCUMENT_CHECKLIST
            + ["missing seller authority documentation"],
            "attorney_title_review_reminder": "Attorney/title review required before any title route is selected.",
            "packet_status": "blocked_compliance",
            "draft_only": True,
            "title_submission_allowed": False,
            "submitted_to_title": False,
            "legal_advice_provided": False,
        },
    ]


def build_assignment_readiness_records() -> list[dict[str, object]]:
    return [
        {
            "id": "assignment-ready-001",
            "contract_control_id": "contract-001",
            "deal_id": "deal-001",
            "buyer_id": "buyer-001",
            "buyer_match_id": "match-001",
            "buyer_interest_id": "interest-001",
            "readiness_status": "assignment_ready",
            "assignment_ready": True,
            "blocked_reasons": [],
            "assignment_allowed_confirmed": True,
            "buyer_pof_status": "verified",
            "compliance_review_passed": True,
            "owner_approval_recorded": True,
            "draft_only": True,
            "contract_execution_allowed": False,
            "title_submission_allowed": False,
        },
        {
            "id": "assignment-ready-002",
            "contract_control_id": "contract-001",
            "deal_id": "deal-001",
            "buyer_id": "buyer-003",
            "buyer_match_id": "match-001",
            "buyer_interest_id": "interest-004",
            "readiness_status": "blocked",
            "assignment_ready": False,
            "blocked_reasons": ["buyer_pof_not_verified"],
            "assignment_allowed_confirmed": True,
            "buyer_pof_status": "needs_refresh",
            "compliance_review_passed": True,
            "owner_approval_recorded": True,
            "draft_only": True,
            "contract_execution_allowed": False,
            "title_submission_allowed": False,
        },
        {
            "id": "assignment-ready-003",
            "contract_control_id": "contract-003",
            "deal_id": "deal-005",
            "buyer_id": "buyer-004",
            "buyer_match_id": "match-003",
            "buyer_interest_id": "interest-005",
            "readiness_status": "blocked",
            "assignment_ready": False,
            "blocked_reasons": [
                "assignment_allowed_not_confirmed",
                "compliance_review_not_passed",
                "contract_control_not_ready",
            ],
            "assignment_allowed_confirmed": False,
            "buyer_pof_status": "verified",
            "compliance_review_passed": False,
            "owner_approval_recorded": True,
            "draft_only": True,
            "contract_execution_allowed": False,
            "title_submission_allowed": False,
        },
        {
            "id": "assignment-ready-004",
            "contract_control_id": "contract-002",
            "deal_id": "deal-003",
            "buyer_id": "buyer-001",
            "buyer_match_id": None,
            "buyer_interest_id": "interest-003",
            "readiness_status": "blocked",
            "assignment_ready": False,
            "blocked_reasons": [
                "buyer_match_missing",
                "contract_control_not_ready",
                "owner_approval_not_recorded",
            ],
            "assignment_allowed_confirmed": True,
            "buyer_pof_status": "verified",
            "compliance_review_passed": True,
            "owner_approval_recorded": False,
            "draft_only": True,
            "contract_execution_allowed": False,
            "title_submission_allowed": False,
        },
    ]


SELLER_PORTAL_DOCUMENT_CHECKLIST = [
    "property details summary reviewed",
    "offer amount summary reviewed",
    "access preference placeholder",
    "title company review reminder",
    "seller questions intake available",
]


def build_seller_offer_publication_records() -> list[dict[str, object]]:
    return [
        {
            "id": "seller-offer-001",
            "lead_id": "lead-001",
            "deal_id": "deal-001",
            "offer_packet_id": "packet-001",
            "contract_control_id": "contract-001",
            "portal_visibility_enabled": True,
            "offer_status": "owner_approved_offer_ready",
            "offer_amount": 151000,
            "closing_timeline_estimate": "14-21 days after owner-approved next steps",
            "inspection_access_next_step": "Share preferred access windows for operator review.",
            "title_company_review_status": "Title/attorney review reminder active; no submission from portal.",
            "document_checklist": SELLER_PORTAL_DOCUMENT_CHECKLIST,
            "operator_contact_placeholder": "Owner/operator contact placeholder for questions.",
            "offer_language": "The offer summary is ready for review. There is no pressure to decide in the portal, and questions are routed for operator review.",
            "offer_language_safety_passed": True,
            "offer_language_safety_result": {},
            "compliance_check_passed": True,
            "owner_approval_recorded": True,
            "visibility_status": "visible",
            "blocked_reasons": [],
            "draft_only": True,
            "contract_execution_allowed": False,
            "live_negotiation_automation_allowed": False,
            "legal_advice_provided": False,
            "buyer_data_exposed": False,
            "internal_profit_logic_exposed": False,
        },
        {
            "id": "seller-offer-002",
            "lead_id": "lead-003",
            "deal_id": "deal-003",
            "offer_packet_id": "packet-002",
            "contract_control_id": "contract-002",
            "portal_visibility_enabled": True,
            "offer_status": "owner_review_required",
            "offer_amount": 180000,
            "closing_timeline_estimate": "30 days after owner approval",
            "inspection_access_next_step": "Access options pending owner approval.",
            "title_company_review_status": "Title review pending owner approval.",
            "document_checklist": SELLER_PORTAL_DOCUMENT_CHECKLIST,
            "operator_contact_placeholder": "Owner/operator contact placeholder.",
            "offer_language": "Owner review is still required before this offer can be shown.",
            "offer_language_safety_passed": True,
            "offer_language_safety_result": {},
            "compliance_check_passed": True,
            "owner_approval_recorded": False,
            "visibility_status": "blocked",
            "blocked_reasons": ["owner_approval_not_recorded"],
            "draft_only": True,
            "contract_execution_allowed": False,
            "live_negotiation_automation_allowed": False,
            "legal_advice_provided": False,
            "buyer_data_exposed": False,
            "internal_profit_logic_exposed": False,
        },
        {
            "id": "seller-offer-003",
            "lead_id": "lead-005",
            "deal_id": "deal-005",
            "offer_packet_id": "packet-003",
            "contract_control_id": "contract-003",
            "portal_visibility_enabled": True,
            "offer_status": "review_blocked",
            "offer_amount": 220000,
            "closing_timeline_estimate": "21-30 days after review clears",
            "inspection_access_next_step": "Access is held until review clears.",
            "title_company_review_status": "Review required before seller-facing visibility.",
            "document_checklist": SELLER_PORTAL_DOCUMENT_CHECKLIST
            + ["authority documentation placeholder"],
            "operator_contact_placeholder": "Owner/operator contact placeholder.",
            "offer_language": "This offer summary remains blocked until review is complete.",
            "offer_language_safety_passed": True,
            "offer_language_safety_result": {},
            "compliance_check_passed": False,
            "owner_approval_recorded": True,
            "visibility_status": "blocked",
            "blocked_reasons": ["compliance_check_not_passed"],
            "draft_only": True,
            "contract_execution_allowed": False,
            "live_negotiation_automation_allowed": False,
            "legal_advice_provided": False,
            "buyer_data_exposed": False,
            "internal_profit_logic_exposed": False,
        },
        {
            "id": "seller-offer-004",
            "lead_id": "lead-007",
            "deal_id": "deal-007",
            "offer_packet_id": "packet-005",
            "contract_control_id": "contract-005",
            "portal_visibility_enabled": False,
            "offer_status": "draft_only",
            "offer_amount": 75000,
            "closing_timeline_estimate": "10-14 days after gate review",
            "inspection_access_next_step": "Access notes held internally.",
            "title_company_review_status": "Review pending.",
            "document_checklist": SELLER_PORTAL_DOCUMENT_CHECKLIST,
            "operator_contact_placeholder": "Owner/operator contact placeholder.",
            "offer_language": "Draft-only offer summary is not visible yet.",
            "offer_language_safety_passed": True,
            "offer_language_safety_result": {},
            "compliance_check_passed": True,
            "owner_approval_recorded": True,
            "visibility_status": "draft",
            "blocked_reasons": ["portal_visibility_not_enabled"],
            "draft_only": True,
            "contract_execution_allowed": False,
            "live_negotiation_automation_allowed": False,
            "legal_advice_provided": False,
            "buyer_data_exposed": False,
            "internal_profit_logic_exposed": False,
        },
        {
            "id": "seller-offer-005",
            "lead_id": "lead-006",
            "deal_id": "deal-006",
            "offer_packet_id": "packet-004",
            "contract_control_id": "contract-004",
            "portal_visibility_enabled": True,
            "offer_status": "blocked_safety",
            "offer_amount": 132000,
            "closing_timeline_estimate": "Held until safety review clears",
            "inspection_access_next_step": "No portal action while blocked.",
            "title_company_review_status": "Review blocked.",
            "document_checklist": SELLER_PORTAL_DOCUMENT_CHECKLIST,
            "operator_contact_placeholder": "Owner/operator contact placeholder.",
            "offer_language": "You must sign now. This is your last chance and no attorney needed.",
            "offer_language_safety_passed": False,
            "offer_language_safety_result": {},
            "compliance_check_passed": True,
            "owner_approval_recorded": True,
            "visibility_status": "blocked",
            "blocked_reasons": ["offer_language_safety_not_passed"],
            "draft_only": True,
            "contract_execution_allowed": False,
            "live_negotiation_automation_allowed": False,
            "legal_advice_provided": False,
            "buyer_data_exposed": False,
            "internal_profit_logic_exposed": False,
        },
    ]


def build_seller_portal_response_records() -> list[dict[str, object]]:
    return [
        {
            "id": "seller-response-001",
            "seller_offer_publication_id": "seller-offer-001",
            "response_type": "seller_portal_note",
            "seller_portal_note": "Seller asked for a plain-language explanation of next steps.",
            "offer_question": "",
            "appointment_access_preference": "",
            "document_upload_placeholder": "",
            "response_status": "received_for_operator_review",
            "operator_review_status": "pending_review",
            "draft_only": True,
            "negotiation_execution_allowed": False,
            "contract_execution_allowed": False,
            "automatic_acceptance_allowed": False,
        },
        {
            "id": "seller-response-002",
            "seller_offer_publication_id": "seller-offer-001",
            "response_type": "offer_question",
            "seller_portal_note": "",
            "offer_question": "Can the closing timeline be closer to three weeks if access is easy?",
            "appointment_access_preference": "",
            "document_upload_placeholder": "",
            "response_status": "received_for_operator_review",
            "operator_review_status": "pending_review",
            "draft_only": True,
            "negotiation_execution_allowed": False,
            "contract_execution_allowed": False,
            "automatic_acceptance_allowed": False,
        },
        {
            "id": "seller-response-003",
            "seller_offer_publication_id": "seller-offer-001",
            "response_type": "appointment_access_preference",
            "seller_portal_note": "",
            "offer_question": "",
            "appointment_access_preference": "Weekday afternoons are easiest for access review.",
            "document_upload_placeholder": "",
            "response_status": "received_for_operator_review",
            "operator_review_status": "reviewed",
            "draft_only": True,
            "negotiation_execution_allowed": False,
            "contract_execution_allowed": False,
            "automatic_acceptance_allowed": False,
        },
        {
            "id": "seller-response-004",
            "seller_offer_publication_id": "seller-offer-001",
            "response_type": "document_upload_placeholder",
            "seller_portal_note": "",
            "offer_question": "",
            "appointment_access_preference": "",
            "document_upload_placeholder": "Seller plans to provide payoff statement placeholder after operator review.",
            "response_status": "placeholder_only",
            "operator_review_status": "pending_review",
            "draft_only": True,
            "negotiation_execution_allowed": False,
            "contract_execution_allowed": False,
            "automatic_acceptance_allowed": False,
        },
    ]


def build_unified_deal_room_records() -> list[dict[str, object]]:
    return [
        {
            "id": "deal-room-001",
            "deal_id": "deal-001",
            "contract_control_id": "contract-001",
            "seller_offer_publication_id": "seller-offer-001",
            "buyer_deal_publication_id": "publication-001",
            "title_handoff_packet_id": "title-001",
            "assignment_readiness_record_id": "assignment-ready-001",
            "seller_portal_status": "visible",
            "buyer_portal_status": "visible",
            "title_handoff_status": "draft_ready",
            "assignment_readiness_status": "assignment_ready",
            "communication_status": "ready",
            "compliance_status": "complete",
            "closing_timeline": "14-21 days",
            "blockers": [],
            "next_required_actions": [],
            "owner_approval_status": "approved",
            "coordination_status": "closing_ready",
            "projected_assignment_fee_at_risk": 0,
            "draft_only": True,
            "legal_execution_allowed": False,
            "executable_contract_generated": False,
            "title_submission_allowed": False,
            "payment_handling_allowed": False,
            "automatic_negotiation_allowed": False,
        },
        {
            "id": "deal-room-002",
            "deal_id": "deal-003",
            "contract_control_id": "contract-002",
            "seller_offer_publication_id": "seller-offer-002",
            "buyer_deal_publication_id": "publication-003",
            "title_handoff_packet_id": "title-002",
            "assignment_readiness_record_id": "assignment-ready-004",
            "seller_portal_status": "blocked",
            "buyer_portal_status": "visible",
            "title_handoff_status": "blocked_owner_review",
            "assignment_readiness_status": "blocked",
            "communication_status": "missing",
            "compliance_status": "complete",
            "closing_timeline": "30 days",
            "blockers": ["missing_owner_approval", "assignment_not_confirmed"],
            "next_required_actions": ["update closing timeline", "review assignment readiness"],
            "owner_approval_status": "pending",
            "coordination_status": "blocked",
            "projected_assignment_fee_at_risk": 13000,
            "draft_only": True,
            "legal_execution_allowed": False,
            "executable_contract_generated": False,
            "title_submission_allowed": False,
            "payment_handling_allowed": False,
            "automatic_negotiation_allowed": False,
        },
        {
            "id": "deal-room-003",
            "deal_id": "deal-005",
            "contract_control_id": "contract-003",
            "seller_offer_publication_id": "seller-offer-003",
            "buyer_deal_publication_id": "publication-005",
            "title_handoff_packet_id": "title-003",
            "assignment_readiness_record_id": "assignment-ready-003",
            "seller_portal_status": "blocked",
            "buyer_portal_status": "blocked",
            "title_handoff_status": "blocked_compliance",
            "assignment_readiness_status": "blocked",
            "communication_status": "missing",
            "compliance_status": "pending",
            "closing_timeline": "21-30 days",
            "blockers": ["missing_compliance_review", "assignment_not_confirmed"],
            "next_required_actions": ["resolve compliance blocker", "review assignment readiness"],
            "owner_approval_status": "approved",
            "coordination_status": "blocked",
            "projected_assignment_fee_at_risk": 15000,
            "draft_only": True,
            "legal_execution_allowed": False,
            "executable_contract_generated": False,
            "title_submission_allowed": False,
            "payment_handling_allowed": False,
            "automatic_negotiation_allowed": False,
        },
        {
            "id": "deal-room-004",
            "deal_id": "deal-006",
            "contract_control_id": "contract-004",
            "seller_offer_publication_id": "seller-offer-005",
            "buyer_deal_publication_id": "publication-006",
            "title_handoff_packet_id": None,
            "assignment_readiness_record_id": None,
            "seller_portal_status": "blocked",
            "buyer_portal_status": "blocked",
            "title_handoff_status": "missing",
            "assignment_readiness_status": "blocked",
            "communication_status": "missing",
            "compliance_status": "complete",
            "closing_timeline": "",
            "blockers": ["weak_buyer_margin", "high_risk_language"],
            "next_required_actions": ["review assignment readiness", "resolve compliance blocker"],
            "owner_approval_status": "approved",
            "coordination_status": "blocked",
            "projected_assignment_fee_at_risk": 8000,
            "draft_only": True,
            "legal_execution_allowed": False,
            "executable_contract_generated": False,
            "title_submission_allowed": False,
            "payment_handling_allowed": False,
            "automatic_negotiation_allowed": False,
        },
    ]


def build_closing_coordination_checklist_records() -> list[dict[str, object]]:
    return [
        {
            "id": "closing-checklist-001",
            "deal_room_id": "deal-room-001",
            "seller_accepted_offer": True,
            "contract_prep_ready": True,
            "buyer_matched": True,
            "buyer_pof_verified": True,
            "assignment_allowed_confirmed": True,
            "title_handoff_prepared": True,
            "inspection_access_coordinated": True,
            "seller_documents_requested": True,
            "buyer_intent_recorded": True,
            "compliance_review_complete": True,
            "owner_approval_complete": True,
            "readiness_status": "checklist_complete",
            "blocked_reasons": [],
            "draft_only": True,
            "legal_execution_allowed": False,
            "title_submission_allowed": False,
            "payment_handling_allowed": False,
            "automatic_negotiation_allowed": False,
        },
        {
            "id": "closing-checklist-002",
            "deal_room_id": "deal-room-002",
            "seller_accepted_offer": True,
            "contract_prep_ready": False,
            "buyer_matched": False,
            "buyer_pof_verified": True,
            "assignment_allowed_confirmed": True,
            "title_handoff_prepared": True,
            "inspection_access_coordinated": True,
            "seller_documents_requested": True,
            "buyer_intent_recorded": True,
            "compliance_review_complete": True,
            "owner_approval_complete": False,
            "readiness_status": "blocked",
            "blocked_reasons": ["contract_prep_ready", "buyer_matched", "owner_approval_complete"],
            "draft_only": True,
            "legal_execution_allowed": False,
            "title_submission_allowed": False,
            "payment_handling_allowed": False,
            "automatic_negotiation_allowed": False,
        },
        {
            "id": "closing-checklist-003",
            "deal_room_id": "deal-room-003",
            "seller_accepted_offer": True,
            "contract_prep_ready": False,
            "buyer_matched": True,
            "buyer_pof_verified": True,
            "assignment_allowed_confirmed": False,
            "title_handoff_prepared": False,
            "inspection_access_coordinated": False,
            "seller_documents_requested": False,
            "buyer_intent_recorded": True,
            "compliance_review_complete": False,
            "owner_approval_complete": True,
            "readiness_status": "blocked",
            "blocked_reasons": [
                "contract_prep_ready",
                "assignment_allowed_confirmed",
                "title_handoff_prepared",
                "inspection_access_coordinated",
                "seller_documents_requested",
                "compliance_review_complete",
            ],
            "draft_only": True,
            "legal_execution_allowed": False,
            "title_submission_allowed": False,
            "payment_handling_allowed": False,
            "automatic_negotiation_allowed": False,
        },
        {
            "id": "closing-checklist-004",
            "deal_room_id": "deal-room-004",
            "seller_accepted_offer": False,
            "contract_prep_ready": False,
            "buyer_matched": False,
            "buyer_pof_verified": False,
            "assignment_allowed_confirmed": False,
            "title_handoff_prepared": False,
            "inspection_access_coordinated": False,
            "seller_documents_requested": False,
            "buyer_intent_recorded": False,
            "compliance_review_complete": True,
            "owner_approval_complete": True,
            "readiness_status": "blocked",
            "blocked_reasons": [
                "seller_accepted_offer",
                "contract_prep_ready",
                "buyer_matched",
                "buyer_pof_verified",
                "assignment_allowed_confirmed",
                "title_handoff_prepared",
                "inspection_access_coordinated",
                "seller_documents_requested",
                "buyer_intent_recorded",
            ],
            "draft_only": True,
            "legal_execution_allowed": False,
            "title_submission_allowed": False,
            "payment_handling_allowed": False,
            "automatic_negotiation_allowed": False,
        },
    ]


def build_deal_room_blocker_records() -> list[dict[str, object]]:
    return [
        {
            "id": "deal-blocker-001",
            "deal_room_id": "deal-room-002",
            "deal_id": "deal-003",
            "blocker_type": "missing_owner_approval",
            "severity": "critical",
            "status": "open",
            "source": "closing_coordination_gate",
            "detail": "Owner approval is required for real-world coordination steps.",
            "recommendation": "update closing timeline",
            "blocks_closing": True,
            "owner_action_required": True,
            "resolved": False,
            "draft_only": True,
        },
        {
            "id": "deal-blocker-002",
            "deal_room_id": "deal-room-003",
            "deal_id": "deal-005",
            "blocker_type": "missing_compliance_review",
            "severity": "critical",
            "status": "open",
            "source": "closing_coordination_gate",
            "detail": "Compliance review must be complete before closing coordination can clear.",
            "recommendation": "resolve compliance blocker",
            "blocks_closing": True,
            "owner_action_required": True,
            "resolved": False,
            "draft_only": True,
        },
        {
            "id": "deal-blocker-003",
            "deal_room_id": "deal-room-004",
            "deal_id": "deal-006",
            "blocker_type": "weak_buyer_margin",
            "severity": "critical",
            "status": "open",
            "source": "closing_coordination_gate",
            "detail": "Buyer margin is below the protected threshold.",
            "recommendation": "review assignment readiness",
            "blocks_closing": True,
            "owner_action_required": True,
            "resolved": False,
            "draft_only": True,
        },
    ]


def build_deal_evidence_packet_records() -> list[dict[str, object]]:
    return [
        {
            "id": "evidence-001",
            "deal_room_id": "deal-room-001",
            "deal_id": "deal-001",
            "lead_source": "vacant",
            "seller_interaction_proof": {},
            "underwriting_snapshot": {},
            "buyer_interest_proof": {},
            "pof_proof_status": "verified",
            "contract_control_status": "prep_review",
            "title_handoff_status": "draft_ready",
            "communication_receipts": [],
            "blocker_history": [],
            "compliance_review_status": "approved",
            "source_records_present": True,
            "unsupported_profit_claims": [],
            "evidence_status": "approved",
            "owner_review_status": "owner_approved",
            "approved": True,
            "sanitized_summary": {},
            "internal_notes_sanitized": True,
            "draft_only": True,
            "client_facing_proof_allowed": False,
            "legal_closing_guarantee_allowed": False,
        },
        {
            "id": "evidence-002",
            "deal_room_id": "deal-room-002",
            "deal_id": "deal-003",
            "lead_source": "absentee owner",
            "seller_interaction_proof": {},
            "underwriting_snapshot": {},
            "buyer_interest_proof": {},
            "pof_proof_status": "needs_refresh",
            "contract_control_status": "prep_review",
            "title_handoff_status": "blocked_owner_review",
            "communication_receipts": [],
            "blocker_history": [],
            "compliance_review_status": "approved",
            "source_records_present": True,
            "unsupported_profit_claims": [],
            "evidence_status": "owner_review_needed",
            "owner_review_status": "pending_review",
            "approved": False,
            "sanitized_summary": {},
            "internal_notes_sanitized": True,
            "draft_only": True,
            "client_facing_proof_allowed": False,
            "legal_closing_guarantee_allowed": False,
        },
        {
            "id": "evidence-003",
            "deal_room_id": "deal-room-003",
            "deal_id": "deal-005",
            "lead_source": "probate",
            "seller_interaction_proof": {},
            "underwriting_snapshot": {},
            "buyer_interest_proof": {},
            "pof_proof_status": "verified",
            "contract_control_status": "prep_review",
            "title_handoff_status": "blocked_compliance",
            "communication_receipts": [],
            "blocker_history": [],
            "compliance_review_status": "pending",
            "source_records_present": True,
            "unsupported_profit_claims": [],
            "evidence_status": "blocked_missing_evidence",
            "owner_review_status": "pending_review",
            "approved": False,
            "sanitized_summary": {},
            "internal_notes_sanitized": True,
            "draft_only": True,
            "client_facing_proof_allowed": False,
            "legal_closing_guarantee_allowed": False,
        },
        {
            "id": "evidence-004",
            "deal_room_id": "deal-room-004",
            "deal_id": "deal-006",
            "lead_source": "tax delinquent",
            "seller_interaction_proof": {},
            "underwriting_snapshot": {},
            "buyer_interest_proof": {},
            "pof_proof_status": "missing",
            "contract_control_status": "blocked",
            "title_handoff_status": "missing",
            "communication_receipts": [],
            "blocker_history": [],
            "compliance_review_status": "approved",
            "source_records_present": False,
            "unsupported_profit_claims": [],
            "evidence_status": "blocked_missing_evidence",
            "owner_review_status": "owner_approved",
            "approved": False,
            "sanitized_summary": {},
            "internal_notes_sanitized": True,
            "draft_only": True,
            "client_facing_proof_allowed": False,
            "legal_closing_guarantee_allowed": False,
        },
    ]


def build_assignment_fee_attribution_records() -> list[dict[str, object]]:
    return [
        {
            "id": "fee-001",
            "deal_room_id": "deal-room-001",
            "deal_id": "deal-001",
            "evidence_packet_id": "evidence-001",
            "projected_assignment_fee": 15000,
            "target_assignment_fee": 10000,
            "seller_contract_price": 151000,
            "buyer_purchase_price": 166000,
            "buyer_margin": 58000,
            "attribution_basis": [],
            "confidence_score": 92,
            "verification_status": "verified",
            "owner_review_status": "owner_approved",
            "source_records_present": True,
            "unsupported_profit_claims": [],
            "verified_10k_opportunity": True,
            "draft_only": True,
            "client_facing_proof_allowed": False,
            "legal_closing_guarantee_allowed": False,
        },
        {
            "id": "fee-002",
            "deal_room_id": "deal-room-002",
            "deal_id": "deal-003",
            "evidence_packet_id": "evidence-002",
            "projected_assignment_fee": 13000,
            "target_assignment_fee": 10000,
            "seller_contract_price": 180000,
            "buyer_purchase_price": 193000,
            "buyer_margin": 74500,
            "attribution_basis": [],
            "confidence_score": 72,
            "verification_status": "owner_review_needed",
            "owner_review_status": "pending_review",
            "source_records_present": True,
            "unsupported_profit_claims": [],
            "verified_10k_opportunity": False,
            "draft_only": True,
            "client_facing_proof_allowed": False,
            "legal_closing_guarantee_allowed": False,
        },
        {
            "id": "fee-003",
            "deal_room_id": "deal-room-003",
            "deal_id": "deal-005",
            "evidence_packet_id": "evidence-003",
            "projected_assignment_fee": 15000,
            "target_assignment_fee": 10000,
            "seller_contract_price": 220000,
            "buyer_purchase_price": 235000,
            "buyer_margin": 90000,
            "attribution_basis": [],
            "confidence_score": 45,
            "verification_status": "blocked",
            "owner_review_status": "pending_review",
            "source_records_present": True,
            "unsupported_profit_claims": [],
            "verified_10k_opportunity": False,
            "draft_only": True,
            "client_facing_proof_allowed": False,
            "legal_closing_guarantee_allowed": False,
        },
        {
            "id": "fee-004",
            "deal_room_id": "deal-room-004",
            "deal_id": "deal-006",
            "evidence_packet_id": "evidence-004",
            "projected_assignment_fee": 8000,
            "target_assignment_fee": 10000,
            "seller_contract_price": 132000,
            "buyer_purchase_price": 140000,
            "buyer_margin": 44000,
            "attribution_basis": [],
            "confidence_score": 45,
            "verification_status": "missing_evidence",
            "owner_review_status": "owner_approved",
            "source_records_present": False,
            "unsupported_profit_claims": [],
            "verified_10k_opportunity": False,
            "draft_only": True,
            "client_facing_proof_allowed": False,
            "legal_closing_guarantee_allowed": False,
        },
    ]


def _draft_obj(row: dict[str, object]):
    return type("DraftSeedObj", (), row)()


def _draft_recipient(row: dict[str, object]) -> str:
    if row["channel"] == "sms":
        return str(row["recipient_phone_placeholder"])
    return str(row["recipient_email_placeholder"] or "owner")


def _dry_run_for(
    receipt_id: str,
    draft: dict[str, object],
    *,
    outdated: bool = False,
) -> dict[str, object]:
    draft_obj = _draft_obj(draft)
    safety = validate_communication_safety(draft_obj)
    recipient = _draft_recipient(draft)
    subject_hash = (
        "outdated-dry-run-hash"
        if outdated
        else communication_hash(str(draft["subject"]), str(draft["draft_body"]))
    )
    return {
        "id": receipt_id,
        "draft_id": draft["id"],
        "recipient": recipient,
        "subject_body_hash": subject_hash,
        "source_record_type": draft["source_record_type"],
        "source_record_id": draft["source_record_id"],
        "risk_status": "clear" if safety["allowed"] and not outdated else "blocked" if not safety["allowed"] else "stale",
        "safety_result": safety,
        "provider_mode": "mock/dry_run",
        "idempotency_key": idempotency_key_for(draft_obj, recipient, subject_hash),
    }


def build_communication_draft_records() -> list[dict[str, object]]:
    return [
        {
            "id": "comm-draft-001",
            "draft_type": "seller_follow_up",
            "channel": "sms",
            "recipient_type": "seller",
            "recipient_email_placeholder": "",
            "recipient_phone_placeholder": "seller-phone-placeholder-lead-001",
            "source_record_type": "seller_interaction",
            "source_record_id": "seller-interaction-001",
            "seller_interaction_id": "seller-interaction-001",
            "buyer_interest_id": None,
            "title_handoff_packet_id": None,
            "subject": "",
            "draft_body": "Hi Angela, this is a draft follow-up for owner review. We can talk through the as-is offer basis when it is convenient. Reply STOP to opt out.",
            "status": "dry_run_ready",
            "safety_checked": True,
            "safety_passed": True,
            "safety_result": {"allowed": True, "risk_flags": [], "reason": "Communication draft passed safety checks."},
            "owner_approval_recorded": False,
            "communication_live_flag_enabled": False,
            "provider_readiness": False,
            "last_dry_run_receipt_id": "dryrun-001",
            "approved_dry_run_receipt_id": None,
            "draft_hash": "",
            "risk_status": "clear",
            "blocked_reasons": [],
            "live_send_count": 0,
            "draft_only": True,
            "bulk_send_allowed": False,
            "campaign_allowed": False,
            "auto_followup_allowed": False,
            "buyer_blast_allowed": False,
            "title_submission_allowed": False,
        },
        {
            "id": "comm-draft-002",
            "draft_type": "buyer_interest_response",
            "channel": "email",
            "recipient_type": "buyer",
            "recipient_email_placeholder": "jules@example.test",
            "recipient_phone_placeholder": "",
            "source_record_type": "buyer_interest",
            "source_record_id": "interest-001",
            "seller_interaction_id": None,
            "buyer_interest_id": "interest-001",
            "title_handoff_packet_id": None,
            "subject": "Draft response on Dallas deal interest",
            "draft_body": "Thanks for the draft interest. The owner will review proof of funds and deal-room details before any next step. This is not a contract or commitment.",
            "status": "owner_approved_waiting_live_flags",
            "safety_checked": True,
            "safety_passed": True,
            "safety_result": {"allowed": True, "risk_flags": [], "reason": "Communication draft passed safety checks."},
            "owner_approval_recorded": True,
            "communication_live_flag_enabled": False,
            "provider_readiness": True,
            "last_dry_run_receipt_id": "dryrun-002",
            "approved_dry_run_receipt_id": "dryrun-002",
            "draft_hash": "",
            "risk_status": "clear",
            "blocked_reasons": [],
            "live_send_count": 0,
            "draft_only": True,
            "bulk_send_allowed": False,
            "campaign_allowed": False,
            "auto_followup_allowed": False,
            "buyer_blast_allowed": False,
            "title_submission_allowed": False,
        },
        {
            "id": "comm-draft-003",
            "draft_type": "title_handoff_email",
            "channel": "email",
            "recipient_type": "title_company",
            "recipient_email_placeholder": "title-company-placeholder@example.test",
            "recipient_phone_placeholder": "",
            "source_record_type": "title_handoff_packet",
            "source_record_id": "title-002",
            "seller_interaction_id": None,
            "buyer_interest_id": None,
            "title_handoff_packet_id": "title-002",
            "subject": "Draft title handoff packet for owner review",
            "draft_body": "Draft only: attached packet placeholders need owner and attorney/title review before any title-company submission or external message.",
            "status": "safety_needed",
            "safety_checked": False,
            "safety_passed": False,
            "safety_result": {},
            "owner_approval_recorded": False,
            "communication_live_flag_enabled": False,
            "provider_readiness": False,
            "last_dry_run_receipt_id": None,
            "approved_dry_run_receipt_id": None,
            "draft_hash": "",
            "risk_status": "unchecked",
            "blocked_reasons": [],
            "live_send_count": 0,
            "draft_only": True,
            "bulk_send_allowed": False,
            "campaign_allowed": False,
            "auto_followup_allowed": False,
            "buyer_blast_allowed": False,
            "title_submission_allowed": False,
        },
        {
            "id": "comm-draft-004",
            "draft_type": "internal_owner_note",
            "channel": "internal",
            "recipient_type": "owner",
            "recipient_email_placeholder": "owner",
            "recipient_phone_placeholder": "",
            "source_record_type": "contract_control",
            "source_record_id": "contract-001",
            "seller_interaction_id": None,
            "buyer_interest_id": None,
            "title_handoff_packet_id": None,
            "subject": "Owner note: communication gate review",
            "draft_body": "Review dry-run receipts, safety results, recipient source tie, and live flags before authorizing any one-off communication.",
            "status": "draft",
            "safety_checked": True,
            "safety_passed": True,
            "safety_result": {"allowed": True, "risk_flags": [], "reason": "Communication draft passed safety checks."},
            "owner_approval_recorded": False,
            "communication_live_flag_enabled": False,
            "provider_readiness": True,
            "last_dry_run_receipt_id": None,
            "approved_dry_run_receipt_id": None,
            "draft_hash": "",
            "risk_status": "clear",
            "blocked_reasons": [],
            "live_send_count": 0,
            "draft_only": True,
            "bulk_send_allowed": False,
            "campaign_allowed": False,
            "auto_followup_allowed": False,
            "buyer_blast_allowed": False,
            "title_submission_allowed": False,
        },
        {
            "id": "comm-draft-005",
            "draft_type": "seller_follow_up",
            "channel": "sms",
            "recipient_type": "seller",
            "recipient_email_placeholder": "",
            "recipient_phone_placeholder": "seller-phone-placeholder-lead-007",
            "source_record_type": "seller_interaction",
            "source_record_id": "seller-interaction-005",
            "seller_interaction_id": "seller-interaction-005",
            "buyer_interest_id": None,
            "title_handoff_packet_id": None,
            "subject": "",
            "draft_body": "You must sign now. This is your last chance and we already have a buyer.",
            "status": "blocked_safety",
            "safety_checked": True,
            "safety_passed": False,
            "safety_result": {},
            "owner_approval_recorded": False,
            "communication_live_flag_enabled": False,
            "provider_readiness": False,
            "last_dry_run_receipt_id": "dryrun-003",
            "approved_dry_run_receipt_id": None,
            "draft_hash": "",
            "risk_status": "blocked",
            "blocked_reasons": ["pressure_language", "fake_buyer_claim", "missing_sms_opt_out"],
            "live_send_count": 0,
            "draft_only": True,
            "bulk_send_allowed": False,
            "campaign_allowed": False,
            "auto_followup_allowed": False,
            "buyer_blast_allowed": False,
            "title_submission_allowed": False,
        },
        {
            "id": "comm-draft-006",
            "draft_type": "buyer_interest_response",
            "channel": "email",
            "recipient_type": "buyer",
            "recipient_email_placeholder": "priya@example.test",
            "recipient_phone_placeholder": "",
            "source_record_type": "buyer_interest",
            "source_record_id": "interest-002",
            "seller_interaction_id": None,
            "buyer_interest_id": "interest-002",
            "title_handoff_packet_id": None,
            "subject": "Updated buyer response after dry-run",
            "draft_body": "The owner updated this draft after the dry-run, so it must be dry-run again before any approval can be used.",
            "status": "changed_after_dry_run",
            "safety_checked": True,
            "safety_passed": True,
            "safety_result": {"allowed": True, "risk_flags": [], "reason": "Communication draft passed safety checks."},
            "owner_approval_recorded": True,
            "communication_live_flag_enabled": True,
            "provider_readiness": True,
            "last_dry_run_receipt_id": "dryrun-004",
            "approved_dry_run_receipt_id": "dryrun-004",
            "draft_hash": "",
            "risk_status": "clear",
            "blocked_reasons": [],
            "live_send_count": 0,
            "draft_only": True,
            "bulk_send_allowed": False,
            "campaign_allowed": False,
            "auto_followup_allowed": False,
            "buyer_blast_allowed": False,
            "title_submission_allowed": False,
        },
    ]


def build_communication_dry_run_records(
    drafts: list[dict[str, object]],
) -> list[dict[str, object]]:
    by_id = {draft["id"]: draft for draft in drafts}
    return [
        _dry_run_for("dryrun-001", by_id["comm-draft-001"]),
        _dry_run_for("dryrun-002", by_id["comm-draft-002"]),
        _dry_run_for("dryrun-003", by_id["comm-draft-005"]),
        _dry_run_for("dryrun-004", by_id["comm-draft-006"], outdated=True),
    ]


def build_communication_approval_records(
    receipts: list[dict[str, object]],
) -> list[dict[str, object]]:
    by_id = {receipt["id"]: receipt for receipt in receipts}
    return [
        {
            "id": "comm-approval-001",
            "draft_id": "comm-draft-002",
            "dry_run_receipt_id": "dryrun-002",
            "owner_approval_recorded": True,
            "approval_status": "approved",
            "approval_notes": "Owner approved one-off mock-send eligibility; global live flag remains disabled.",
            "approved_by": "Owner",
            "draft_hash_at_approval": by_id["dryrun-002"]["subject_body_hash"],
        },
        {
            "id": "comm-approval-002",
            "draft_id": "comm-draft-006",
            "dry_run_receipt_id": "dryrun-004",
            "owner_approval_recorded": True,
            "approval_status": "stale_after_draft_change",
            "approval_notes": "Approval is stale because the draft changed after dry-run.",
            "approved_by": "Owner",
            "draft_hash_at_approval": by_id["dryrun-004"]["subject_body_hash"],
        },
    ]


def build_communication_attempt_records(
    receipts: list[dict[str, object]],
) -> list[dict[str, object]]:
    by_id = {receipt["id"]: receipt for receipt in receipts}
    return [
        {
            "id": "comm-attempt-001",
            "draft_id": "comm-draft-002",
            "dry_run_receipt_id": "dryrun-002",
            "recipient": "jules@example.test",
            "channel": "email",
            "provider_mode": "mock/dry_run",
            "attempt_status": "blocked",
            "blocked_reasons": [
                "global_live_flag_disabled",
                "communication_live_flag_disabled",
            ],
            "safety_result": by_id["dryrun-002"]["safety_result"],
            "idempotency_key": by_id["dryrun-002"]["idempotency_key"],
            "provider_called": False,
            "mock_sent": False,
            "live_send_requested": True,
            "bulk_send_detected": False,
        },
        {
            "id": "comm-attempt-002",
            "draft_id": "comm-draft-005",
            "dry_run_receipt_id": "dryrun-003",
            "recipient": "seller-phone-placeholder-lead-007",
            "channel": "sms",
            "provider_mode": "mock/dry_run",
            "attempt_status": "blocked",
            "blocked_reasons": ["safety_not_passed"],
            "safety_result": by_id["dryrun-003"]["safety_result"],
            "idempotency_key": by_id["dryrun-003"]["idempotency_key"],
            "provider_called": False,
            "mock_sent": False,
            "live_send_requested": True,
            "bulk_send_detected": False,
        },
    ]


LEAD_LOOKUP = {lead["id"]: lead for lead in build_lead_records()}


def seed_payload() -> dict[str, list[dict[str, object]]]:
    leads = build_lead_records()
    leads_by_id = {lead["id"]: lead for lead in leads}
    buyers = build_buyer_records()
    buyers_by_id = {buyer["id"]: buyer for buyer in buyers}
    deals = build_deal_records(leads_by_id)
    deals_by_id = {deal["id"]: deal for deal in deals}
    communication_drafts = build_communication_draft_records()
    communication_dry_runs = build_communication_dry_run_records(communication_drafts)
    return {
        "divisions": DIVISION_DEFINITIONS,
        "agents": build_agents(),
        "leads": leads,
        "buyers": buyers,
        "deals": deals,
        "buyer_matches": build_match_records(deals_by_id, buyers_by_id),
        "buyer_deal_publications": build_publication_records(deals_by_id),
        "buyer_interests": build_interest_records(),
        "seller_interactions": build_seller_interaction_records(),
        "offer_packets": build_offer_packet_records(),
        "contract_controls": build_contract_control_records(),
        "seller_offer_publications": build_seller_offer_publication_records(),
        "seller_portal_responses": build_seller_portal_response_records(),
        "unified_deal_rooms": build_unified_deal_room_records(),
        "closing_coordination_checklists": build_closing_coordination_checklist_records(),
        "deal_room_blockers": build_deal_room_blocker_records(),
        "deal_evidence_packets": build_deal_evidence_packet_records(),
        "assignment_fee_attributions": build_assignment_fee_attribution_records(),
        "title_handoff_packets": build_title_handoff_records(),
        "assignment_readiness_records": build_assignment_readiness_records(),
        "communication_drafts": communication_drafts,
        "communication_dry_run_receipts": communication_dry_runs,
        "communication_approvals": build_communication_approval_records(
            communication_dry_runs
        ),
        "communication_send_attempts": build_communication_attempt_records(
            communication_dry_runs
        ),
        "compliance_records": build_compliance_records(),
    }


def seed_database(session: Session) -> dict[str, int]:
    for model in [
        AssignmentFeeAttribution,
        DealEvidencePacket,
        DealRoomBlocker,
        ClosingCoordinationChecklist,
        UnifiedDealRoom,
        SellerPortalResponse,
        SellerOfferPublication,
        CommunicationSendAttempt,
        CommunicationApproval,
        CommunicationDryRunReceipt,
        CommunicationDraft,
        AssignmentReadinessRecord,
        TitleHandoffPacket,
        ContractControl,
        OfferPacket,
        SellerInteraction,
        BuyerInterest,
        BuyerDealPublication,
        BuyerMatch,
        ComplianceRecord,
        Deal,
        Buyer,
        Lead,
        Agent,
        Division,
    ]:
        session.query(model).delete(synchronize_session=False)

    payload = seed_payload()
    session.add_all(Division(**row) for row in payload["divisions"])
    session.add_all(Agent(**row) for row in payload["agents"])
    session.add_all(Lead(**row) for row in payload["leads"])
    session.add_all(Buyer(**row) for row in payload["buyers"])
    session.add_all(Deal(**row) for row in payload["deals"])
    session.add_all(BuyerMatch(**row) for row in payload["buyer_matches"])
    session.add_all(BuyerDealPublication(**row) for row in payload["buyer_deal_publications"])
    session.add_all(BuyerInterest(**row) for row in payload["buyer_interests"])
    session.add_all(SellerInteraction(**row) for row in payload["seller_interactions"])
    session.add_all(OfferPacket(**row) for row in payload["offer_packets"])
    session.add_all(ContractControl(**row) for row in payload["contract_controls"])
    session.add_all(
        SellerOfferPublication(**row)
        for row in payload["seller_offer_publications"]
    )
    session.add_all(
        SellerPortalResponse(**row) for row in payload["seller_portal_responses"]
    )
    session.add_all(TitleHandoffPacket(**row) for row in payload["title_handoff_packets"])
    session.add_all(
        AssignmentReadinessRecord(**row)
        for row in payload["assignment_readiness_records"]
    )
    session.add_all(UnifiedDealRoom(**row) for row in payload["unified_deal_rooms"])
    session.add_all(
        ClosingCoordinationChecklist(**row)
        for row in payload["closing_coordination_checklists"]
    )
    session.add_all(DealRoomBlocker(**row) for row in payload["deal_room_blockers"])
    session.add_all(
        DealEvidencePacket(**row) for row in payload["deal_evidence_packets"]
    )
    session.add_all(
        AssignmentFeeAttribution(**row)
        for row in payload["assignment_fee_attributions"]
    )
    session.add_all(CommunicationDraft(**row) for row in payload["communication_drafts"])
    session.add_all(
        CommunicationDryRunReceipt(**row)
        for row in payload["communication_dry_run_receipts"]
    )
    session.add_all(
        CommunicationApproval(**row) for row in payload["communication_approvals"]
    )
    session.add_all(
        CommunicationSendAttempt(**row)
        for row in payload["communication_send_attempts"]
    )
    session.add_all(ComplianceRecord(**row) for row in payload["compliance_records"])
    session.flush()
    for publication in session.query(BuyerDealPublication).all():
        update_publication_gate(publication, publication.deal)
    for packet in session.query(OfferPacket).all():
        update_offer_packet_gate(packet, packet.deal)
    for contract in session.query(ContractControl).all():
        update_contract_prep_gate(contract)
    for readiness in session.query(AssignmentReadinessRecord).all():
        update_assignment_readiness(readiness)
    for seller_offer in session.query(SellerOfferPublication).all():
        seller_offer.offer_language_safety_result = validate_seller_portal_language(
            seller_offer.offer_language
        )
        update_seller_visibility_gate(seller_offer)
    for draft in session.query(CommunicationDraft).all():
        draft.draft_hash = communication_hash(draft.subject, draft.draft_body)
        if draft.safety_checked:
            draft.safety_result = validate_communication_safety(draft)
            draft.safety_passed = bool(draft.safety_result["allowed"])
            draft.risk_status = "clear" if draft.safety_passed else "blocked"
    for room in session.query(UnifiedDealRoom).all():
        sync_deal_room(session, room)
    for evidence_packet in session.query(DealEvidencePacket).all():
        sync_evidence_packet(session, evidence_packet)
    for attribution in session.query(AssignmentFeeAttribution).all():
        sync_assignment_fee_attribution(session, attribution)
    session.commit()
    return {key: len(value) for key, value in payload.items()}
