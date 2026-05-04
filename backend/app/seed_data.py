from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.buyer_matching import score_buyer_match
from app.domain.compliance import REQUIRED_CONFIRMATIONS
from app.domain.profit_control import ProfitControlInput, calculate_profit_control
from app.domain.rules import ANALYSIS_ONLY_ACTIONS, BLOCKED_ACTIONS
from app.domain.scoring import calculate_lead_opportunity, deal_speed_score
from app.models import Agent, Buyer, BuyerMatch, ComplianceRecord, Deal, Division, Lead


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


LEAD_LOOKUP = {lead["id"]: lead for lead in build_lead_records()}


def seed_payload() -> dict[str, list[dict[str, object]]]:
    leads = build_lead_records()
    leads_by_id = {lead["id"]: lead for lead in leads}
    buyers = build_buyer_records()
    buyers_by_id = {buyer["id"]: buyer for buyer in buyers}
    deals = build_deal_records(leads_by_id)
    deals_by_id = {deal["id"]: deal for deal in deals}
    return {
        "divisions": DIVISION_DEFINITIONS,
        "agents": build_agents(),
        "leads": leads,
        "buyers": buyers,
        "deals": deals,
        "buyer_matches": build_match_records(deals_by_id, buyers_by_id),
        "compliance_records": build_compliance_records(),
    }


def seed_database(session: Session) -> dict[str, int]:
    for model in [BuyerMatch, ComplianceRecord, Deal, Buyer, Lead, Agent, Division]:
        session.query(model).delete(synchronize_session=False)

    payload = seed_payload()
    session.add_all(Division(**row) for row in payload["divisions"])
    session.add_all(Agent(**row) for row in payload["agents"])
    session.add_all(Lead(**row) for row in payload["leads"])
    session.add_all(Buyer(**row) for row in payload["buyers"])
    session.add_all(Deal(**row) for row in payload["deals"])
    session.add_all(BuyerMatch(**row) for row in payload["buyer_matches"])
    session.add_all(ComplianceRecord(**row) for row in payload["compliance_records"])
    session.commit()
    return {key: len(value) for key, value in payload.items()}
