# Architecture

## System Posture

The app is a private, single-owner command center. It intentionally has no public signup, no team accounts, no public portals, no client portal, and no live outreach execution. The owner is the only final approver for real-world action.

Prime 2 is the executive overseer. It can recommend, route, summarize, escalate, and block unsafe action. It cannot send messages, contact buyers or sellers, execute contracts, provide legal advice, or make guaranteed profit claims.

Prime 2 is the brother system to Vylarion Prime, purpose-built for the private Prime 2 Wholesale Deal OS. Prime 2 is the private wholesale real estate overseer built to identify, control, and accelerate assignment-fee opportunities while preserving owner approval, compliance boundaries, and deal evidence.

Prime 2 is responsible for seller acquisition oversight, buyer disposition oversight, 10K+ opportunity ranking, buyer margin protection, seller offer reasonableness, manager and expert-agent coordination, owner approval escalation, daily operating reports, compliance boundaries, and gated high-risk live actions.

V2 adds a controlled buyer portal. The private operator system remains the source of truth, and the buyer portal is only an invite-gated, sanitized deal-room projection. There is still no public signup, no seller portal, no live buyer blasts, no payments, no legal advice, and no contract execution.

V3 adds seller acquisition and follow-up control. It turns leads into controlled seller opportunities with interaction records and draft preparation only. It still does not send SMS, email, calls, or offers, and it cannot execute contracts.

V4 adds contract control and title handoff preparation. It turns approved offer packets into internal control records, title handoff placeholders, and assignment-readiness checks without executable contract generation, live sending, title-company submission, legal advice, or automatic contract status changes.

V5 adds a controlled communication gate. It can prepare communication drafts and mock dry-runs, but any live-send path is disabled by default and must pass safety, dry-run, unchanged-draft, owner approval, provider readiness, recipient source tie, one-recipient, and idempotency gates. Bulk campaigns, buyer blasts, auto follow-up sequences, and title-company submission remain blocked.

V6 adds a controlled seller offer review room. The private operator system remains the source of truth, and seller-facing visibility is invite-gated, explicitly enabled per offer, sanitized, and blocked unless offer packet, compliance, owner approval, contract-control status, and language-safety gates pass. Seller responses are intake-only for operator review; there is no acceptance execution, negotiation automation, contract execution, file transmission, legal advice, buyer data exposure, or internal profit/spread exposure.

V7 adds a unified internal deal room and closing coordination gate. It connects seller offer room, buyer deal room, contract control, title handoff, communication drafts, compliance, and assignment readiness into one governed coordination layer. It is recommendation-only and cannot execute legal documents, submit title packages, handle payments, or automate buyer/seller negotiation.

V8 adds proof-backed deal evidence and assignment-fee attribution. It ties projected and verified assignment fees to source records instead of guesses, sanitizes internal notes from evidence summaries, and blocks fake profit claims, unsupported ROI claims, invented buyer/seller numbers, client-facing proof without approval, and legal or closing guarantees.

V9 adds buyer demand intelligence and deal distribution prep. It ranks which buyers are most likely to close fast using demand, price, POF, reliability, closing speed, deal type, and buyer margin signals, then prepares sanitized one-recipient distribution drafts without live blasts, bulk sends, fake scarcity, fake competition, or seller/private data exposure.

V10 adds controlled offer-to-contract conversion. It structures offer positioning, negotiation tracking, seller acceptance readiness scoring, and contract-ready state gating so the operator can move faster only when underwriting, profit control, buyer demand, compliance, risk, seller readiness, and owner approval all clear. Contract-ready is an internal coordination status only; it does not create or execute a contract.

V11 adds title company/attorney review coordination. It prepares draft-only review records and review packets for V10 contract-ready deals, tracks missing documents and owner approval, and blocks legal advice, contract execution, document submission, title-company email sending, attorney-client relationship claims, and closing guarantees.

V12 adds near-autonomous internal execution. Prime 2 and its divisions can continuously analyze, prepare, prioritize, route, schedule, escalate, and brief the operator. The default autonomy model is Level 2 for autonomous internal prep, Level 3 for autonomous draft creation and scheduling, Level 4 for controlled live-action review with owner approval only, and Level 5 disabled/unavailable. Real-world actions remain blocked unless a prior controlled gate explicitly allows owner-reviewed next steps.

V13 adds a controlled auto-execution gate for very narrow approved repeatable actions. It does not loosen V5 or V12; it requires approved rules, approved templates, safety, dry-run receipts, owner approval where needed, live flags, provider readiness, one recipient, idempotency, and audit records before a low-risk single-message path can even mock-send.

V14 adds buyer distribution acceleration. It ranks fast-close buyers, prepares draft-only buyer sequences, routes buyer responses, and keeps any controlled buyer message behind sanitized deal sheets, owner approval, V5/V13 gates, one-recipient limits, and no-bulk rules.

V15 adds deterministic deal-flow optimization. It studies source-backed outcomes, detects explainable patterns, recommends market/source/script focus changes, scores agent performance, and logs scoring-weight changes without unsupported ROI or fake revenue claims.

V16 adds revenue forecasting and market scaling. Forecasts are labeled estimates and must reference source records, probability inputs, buyer demand, market heat, verified/pending assignment fees, and owner-reviewed lead spend planning.

V17 adds semi-autonomous operator mode. Prime 2 can run the internal scan-score-route-prepare-check-escalate-brief-log-optimize loop and queue approvals, but cannot bypass owner gates or perform high-risk real-world actions.

V18 adds production readiness, audit export, evidence attachment metadata, backup/export metadata, provider sandbox checks, environment checks, and deployment hardening checks. It keeps public exposure blocked unless auth, env, secrets, provider, audit, backup, and hardening gates pass.

V19 adds real lead import and field testing. It creates preview-first CSV import batches, row-level validation and dedupe, lead QA scoring, manual seller call outcome tracking, do-not-contact eligibility blocks, Prime 2 prediction-versus-reality feedback, explainable scoring adjustment suggestions, and a field briefing. Imported leads cannot trigger live outreach, bulk messages, automatic portal publishing, contract execution, title submission, or payment handling.

V20 adds the AI Gateway controlled intelligence layer. It supports only approved Prime 2 request types: seller script drafts, buyer message drafts, objection responses, deal summaries, daily briefings, negotiation assistance, and field-testing summaries. Every request is template-gated, token/cost-estimated, safety-scanned, audit-logged, and blocked from legal advice, contract generation, deceptive urgency/scarcity, guaranteed profit claims, role misrepresentation, invented ARV/repairs, or financial calculation overrides. `OPENAI_API_KEY` is read from environment only and provider mode defaults to mock/dry-run.

V21 adds the background worker runtime. It introduces queued internal jobs, scheduler cadence, retries/backoff, idempotency keys, job ledgers, heartbeat health, stuck-job detection, and Prime 2 feeds into autonomy, daily briefing, escalation, and next-best-action surfaces. Worker jobs prepare, schedule, route, draft, and escalate only. The worker cannot send SMS/email, call sellers, contact buyers, publish portals, execute contracts, submit to title, change seller/buyer terms, handle payments, or bypass approval gates.

## Backend Modules

- `app/models.py`: SQLAlchemy persistence models for divisions, agents, leads, deals, buyers, portals, communications, contract control, title/review coordination, deal rooms, evidence, assignment fees, automation, optimization, forecasting, operator mode, production readiness, audit exports, attachments, backups, lead imports, lead QA, call outcomes, field feedback, and scoring adjustment suggestions.
- `app/domain/scoring.py`: lead opportunity scoring and deal speed score.
- `app/domain/profit_control.py`: MAO, max buyer purchase price, max seller offer, offer options, assignment spread, reasonableness scoring, and buyer margin flags.
- `app/domain/buyer_matching.py`: draft-only buyer match scoring by area, price, property type, reliability, closing speed, and proof of funds.
- `app/domain/buyer_portal.py`: buyer visibility publishing gate, sanitized deal-room projection, forbidden-field leak guard, and V2 portal policy.
- `app/domain/buyer_demand.py`: V9 buyer demand scoring, per-deal priority ranking, sanitized private deal sheet generation, distribution prep guard, and buyer demand dashboard aggregation.
- `app/domain/offer_conversion.py`: V10 offer positioning summaries, negotiation readiness scoring, conversion gates, deal acceleration recommendations, contract-ready state sync, and conversion safety validation.
- `app/domain/title_review.py`: V11 title/attorney review coordination gates, draft review packet summaries, missing-item queues, safety validation, and no-submission boundaries.
- `app/domain/autonomy.py`: V12 automation rule engine, scheduler runtime, run/attempt ledgers, idempotency guard, autonomous task queue, event trigger summaries, daily command briefing generation, escalation queue, and autonomy safety guard.
- `app/domain/auto_execution.py`: V13 controlled auto-execution rules, approved template safety checks, conditional execution gate, dry-run receipts, idempotent single-attempt workflow, and audit trail aggregation.
- `app/domain/field_testing.py`: V19 CSV import preview/commit workflow, normalization, critical field validation, dedupe checks, lead QA scoring, call outcome updates, do-not-contact guard, prediction feedback comparison, scoring adjustment suggestions, field dashboard, and daily field briefing.
- `app/domains/ai_gateway/*`: V20 controlled AI Gateway with request type allowlist, versioned templates, safety scanner, token/cost ledger, request audit trail, and deterministic mock/template responses.
- `app/domains/worker_runtime/*`: V21 background worker runtime with queueing, scheduler, runner, retry manager, idempotency, ledgers, heartbeat health, and hard blocks against live action.
- `app/domain/seller_acquisition.py`: seller safety language guard, draft-only follow-up engine, seller pipeline command center, and offer packet prep gate.
- `app/domain/contract_control.py`: V4 contract prep gate, title handoff safety summary, assignment readiness gate, and contract/title language guard.
- `app/domain/communications.py`: V5 communication safety checks, dry-run receipts, owner approval gate, idempotency gate, blocked attempt audit, and mock email/SMS adapters.
- `app/domain/seller_portal.py`: V6 seller visibility gate, sanitized offer-room projection, response intake guard, forbidden-field leak guard, and seller portal policy.
- `app/domain/closing_coordination.py`: V7 unified deal room status sync, closing checklist readiness, blocker generation, next-best-action recommendations, and coordination dashboard aggregation.
- `app/domain/deal_evidence.py`: V8 evidence packet sync, assignment-fee attribution, source-record verification, 10K+ verification, sanitized evidence summaries, and unsupported-claim guards.
- `app/domain/rules.py`: private-mode rules and v1 action validation.
- `app/domain/compliance.py`: purchase, assignment, title, seller disclosure, buyer disclosure, and state-review checklists.
- `app/domain/imports.py`: CSV-ready lead import preview with accepted source categories.
- `app/domain/command_center.py`: daily ranking and attention queue aggregation.
- `app/seed_data.py`: realistic demo hierarchy, leads, buyers, deals, matches, and compliance examples.
- `app/api/routes.py`: read APIs and validation endpoints.

## Core Formulas

```text
max_buyer_purchase_price = ARV - repairs - buyer_costs - buyer_desired_profit
max_seller_offer = max_buyer_purchase_price - target_assignment_fee
projected_assignment_fee = buyer_purchase_price - seller_contract_price
```

The profit-control engine flags assignment spreads below target, buyer margins below desired profit, seller offers above the safe max, overly aggressive seller offers, and invalid ARV or repair inputs.

## Data Model

```mermaid
erDiagram
  DIVISION ||--o{ AGENT : manages
  LEAD ||--o{ DEAL : produces
  DEAL ||--o{ BUYER_MATCH : matches
  BUYER ||--o{ BUYER_MATCH : receives
  DEAL ||--o{ COMPLIANCE_RECORD : requires
  DEAL ||--o| BUYER_DEAL_PUBLICATION : projects
  DEAL ||--o{ BUYER_INTEREST : receives
  BUYER ||--o{ BUYER_INTEREST : records
  LEAD ||--o{ SELLER_INTERACTION : captures
  DEAL ||--o{ OFFER_PACKET : gates
  LEAD ||--o{ CONTRACT_CONTROL : controls
  DEAL ||--o{ CONTRACT_CONTROL : prepares
  OFFER_PACKET ||--o{ CONTRACT_CONTROL : authorizes
  CONTRACT_CONTROL ||--o{ TITLE_HANDOFF_PACKET : drafts
  CONTRACT_CONTROL ||--o{ ASSIGNMENT_READINESS_RECORD : checks
  DEAL ||--o{ ASSIGNMENT_READINESS_RECORD : readies
  BUYER ||--o{ ASSIGNMENT_READINESS_RECORD : verifies
  SELLER_INTERACTION ||--o{ COMMUNICATION_DRAFT : sources
  BUYER_INTEREST ||--o{ COMMUNICATION_DRAFT : sources
  TITLE_HANDOFF_PACKET ||--o{ COMMUNICATION_DRAFT : sources
  COMMUNICATION_DRAFT ||--o{ COMMUNICATION_DRY_RUN_RECEIPT : produces
  COMMUNICATION_DRY_RUN_RECEIPT ||--o{ COMMUNICATION_APPROVAL : gates
  COMMUNICATION_DRAFT ||--o{ COMMUNICATION_SEND_ATTEMPT : audits
  LEAD ||--o{ SELLER_OFFER_PUBLICATION : projects
  DEAL ||--o{ SELLER_OFFER_PUBLICATION : publishes
  OFFER_PACKET ||--o{ SELLER_OFFER_PUBLICATION : gates
  CONTRACT_CONTROL ||--o{ SELLER_OFFER_PUBLICATION : validates
  SELLER_OFFER_PUBLICATION ||--o{ SELLER_PORTAL_RESPONSE : intakes
  DEAL ||--o{ UNIFIED_DEAL_ROOM : coordinates
  CONTRACT_CONTROL ||--o{ UNIFIED_DEAL_ROOM : controls
  UNIFIED_DEAL_ROOM ||--o| CLOSING_COORDINATION_CHECKLIST : checks
  UNIFIED_DEAL_ROOM ||--o{ DEAL_ROOM_BLOCKER : blocks
  UNIFIED_DEAL_ROOM ||--o{ DEAL_EVIDENCE_PACKET : proves
  DEAL ||--o{ DEAL_EVIDENCE_PACKET : evidences
  DEAL_EVIDENCE_PACKET ||--o{ ASSIGNMENT_FEE_ATTRIBUTION : attributes
  DEAL ||--o{ ASSIGNMENT_FEE_ATTRIBUTION : calculates
  BUYER ||--o| BUYER_DEMAND_PROFILE : profiles
  DEAL ||--o{ BUYER_DEAL_PRIORITY : ranks
  BUYER ||--o{ BUYER_DEAL_PRIORITY : scores
  BUYER_DEMAND_PROFILE ||--o{ BUYER_DEAL_PRIORITY : informs
  DEAL ||--o{ DEAL_DISTRIBUTION_PREP : prepares
  BUYER ||--o{ DEAL_DISTRIBUTION_PREP : targets
  BUYER_DEAL_PRIORITY ||--o{ DEAL_DISTRIBUTION_PREP : sources
  DEAL ||--o{ OFFER_POSITIONING_RECORD : positions
  OFFER_PACKET ||--o{ OFFER_POSITIONING_RECORD : supports
  DEAL ||--o{ NEGOTIATION_RECORD : tracks
  OFFER_POSITIONING_RECORD ||--o{ NEGOTIATION_RECORD : frames
  DEAL ||--o{ CONTRACT_READY_STATE : gates
  OFFER_POSITIONING_RECORD ||--o{ CONTRACT_READY_STATE : supports
  NEGOTIATION_RECORD ||--o{ CONTRACT_READY_STATE : readies
  DEAL ||--o{ TITLE_REVIEW_COORDINATION : coordinates
  CONTRACT_READY_STATE ||--o{ TITLE_REVIEW_COORDINATION : gates
  TITLE_REVIEW_COORDINATION ||--o{ REVIEW_PACKET_PREP : prepares
  DEAL ||--o{ REVIEW_PACKET_PREP : drafts
  AUTOMATION_RULE ||--o{ SCHEDULER_RUN : schedules
  SCHEDULER_RUN ||--o{ AUTOMATION_ATTEMPT : audits
  AUTOMATION_RULE ||--o{ AUTONOMOUS_AGENT_TASK : routes
  SCHEDULER_RUN ||--o{ AUTONOMOUS_AGENT_TASK : creates
  AUTOMATION_RULE ||--o{ AUTOMATION_EVENT_TRIGGER : listens
  SCHEDULER_RUN ||--o{ DAILY_COMMAND_BRIEFING : generates
  SCHEDULER_RUN ||--o{ AUTONOMY_ESCALATION : escalates
  DEAL ||--o{ AUTONOMY_ESCALATION : raises
  LEAD ||--o{ AUTONOMY_ESCALATION : raises
  APPROVED_TEMPLATE ||--o{ AUTO_EXECUTION_RULE : authorizes
  AUTO_EXECUTION_RULE ||--o{ AUTO_EXECUTION_DRY_RUN : produces
  APPROVED_TEMPLATE ||--o{ AUTO_EXECUTION_DRY_RUN : hashes
  AUTO_EXECUTION_RULE ||--o{ AUTO_EXECUTION_ATTEMPT : gates
  AUTO_EXECUTION_DRY_RUN ||--o{ AUTO_EXECUTION_ATTEMPT : supports
  AUTO_EXECUTION_ATTEMPT ||--o{ AUTO_EXECUTION_AUDIT_RECORD : audits
  LEAD_IMPORT_BATCH ||--o{ LEAD_IMPORT_ROW : previews
  LEAD_IMPORT_BATCH ||--o{ LEAD_QUALITY_REVIEW : scores
  LEAD_IMPORT_ROW ||--o{ LEAD_QUALITY_REVIEW : checks
  LEAD ||--o{ LEAD_QUALITY_REVIEW : links
  LEAD ||--o{ FIELD_CALL_OUTCOME : records
  FIELD_CALL_OUTCOME ||--o{ PREDICTION_FEEDBACK_RECORD : compares
  PREDICTION_FEEDBACK_RECORD ||--o{ SCORING_ADJUSTMENT_SUGGESTION : suggests
  AI_TEMPLATE ||--o{ AI_REQUEST_LOG : gates
  AI_REQUEST_LOG ||--o{ AI_AUDIT_RECORD : audits
  AI_REQUEST_LOG ||--o{ AI_COST_LEDGER : costs
  WORKER_JOB ||--o{ WORKER_JOB_LOG : ledgers
  WORKER_HEARTBEAT ||--o{ WORKER_JOB : monitors
```

## V20 AI Gateway

Backend routes:

- `/api/v1/ai`
- `/api/v1/ai/request`
- `/api/v1/ai/audit`
- `/api/v1/ai/costs`
- `/api/v1/ai/templates`

Frontend routes:

- `/dashboard/ai`
- `/dashboard/ai/audit`
- `/dashboard/ai/costs`
- `/dashboard/ai/templates`

The gateway is not an open AI chat surface. It is a controlled internal service that renders approved templates with system data, estimates tokens and cost, scans prompts and responses, records audit and cost ledgers, and rejects unsupported or unsafe request types. It does not make real provider calls in the default configuration and it never allows AI to override system financial calculations.

## V21 Worker Runtime

Backend routes:

- `/api/v1/worker`
- `/api/v1/worker/health`
- `/api/v1/worker/jobs`
- `/api/v1/worker/logs`

Frontend routes:

- `/dashboard/worker`
- `/dashboard/worker/jobs`
- `/dashboard/worker/health`

Supported worker jobs are lead scoring refresh, follow-up scheduling, daily briefing generation, buyer ranking refresh, QA checks, automation rule evaluation, field-testing summary, and forecast refresh. Jobs use idempotency keys to prevent duplicate execution, retry/backoff to avoid runaway loops, and ledgers for completed or failed attempts. Heartbeat health reports stuck jobs and recovery needs without granting live execution authority.

## V2 Buyer Portal

Buyer-facing routes:

- `/buyer-portal`
- `/buyer-portal/deals`
- `/buyer-portal/deals/[dealId]`
- `/buyer-portal/profile`
- `/buyer-portal/watchlist`

The buyer portal shows only property city/state/zip, property type, beds/baths/sqft, ARV range, repair estimate range, asking price, estimated buyer margin, photo placeholders, access instructions placeholder, proof-of-funds status, deal availability status, and a draft-only offer-interest control.

The buyer portal never exposes seller identity, seller contact details, lead source, motivation score, seller temperature, seller contract price except as intentionally published asking price, assignment fee logic, projected assignment spread, max seller offer, internal notes, compliance internals, Prime 2 recommendations, agent queues, or manager queues.

## Publishing Gate

A deal can be buyer-visible only when all of these are true:

- Operator explicitly marked it buyer-visible
- ARV exists
- Repair estimate exists
- Asking price exists
- Compliance review is marked complete
- Seller contract is marked controlled
- Risk status is not high
- Buyer margin is not weak

The internal dashboard shows buyer-visible deals, buyer interest queue, proof-of-funds needs, owner-review offer intents, and deals blocked from buyer portal with reasons.

## V3 Seller Acquisition

Internal routes:

- `/dashboard/seller-acquisition`
- `/dashboard/seller-acquisition/[leadId]`
- `/dashboard/follow-up-control`
- `/dashboard/offer-packets`
- `/dashboard/offer-packets/[packetId]`

Seller interaction records capture call notes, motivation answers, asking price, timeline, property condition, pain points, objections, next follow-up date, seller temperature score, objection status, follow-up urgency, and next best seller action.

The follow-up engine prepares only drafts:

- Call script draft
- SMS draft
- Email draft
- Objection response draft
- Offer explanation draft
- Follow-up sequence draft

## Offer Packet Prep Gate

Offer packet prep is allowed only when all of these are true:

- ARV exists
- Repair estimate exists
- Max seller offer is calculated
- Buyer margin is protected
- Target assignment fee is checked
- Compliance guard passed
- Owner approval is recorded

The gate returns blocked reasons for missing underwriting, weak buyer margin, target assignment fee failure, missing compliance, or missing owner approval. Even when allowed, the packet remains draft-only and no real-world action is taken.

## Seller Safety Boundary

Blocked seller acquisition language and actions include pressure language, fake buyer claims, fake urgency, guaranteed closing claims, legal advice, misleading assignment language, live SMS, live email, and live calls.

## V4 Contract Control

Internal routes:

- `/dashboard/contract-control`
- `/dashboard/contract-control/[contractId]`
- `/dashboard/title-handoff`
- `/dashboard/title-handoff/[packetId]`
- `/dashboard/assignment-readiness`

Contract control records connect the lead, deal, and approved offer packet to seller accepted terms, contract status, assignment allowed flag, inspection/access notes, earnest money notes, closing timeline, title company preference, required document checklist, owner approval status, and compliance review status.

Contract prep is allowed only when all of these are true:

- Offer packet is approved
- Seller accepted terms are recorded
- ARV and repair estimate exist
- Buyer margin is protected
- Assignment spread is calculated
- Compliance guard passed
- Owner approval is recorded

Title handoff packets are preparation artifacts only. They contain property details, seller info placeholder, buyer/entity info placeholder, agreed price, closing timeline, access notes, assignment status, required document checklist, and attorney/title review reminder. V4 has no title-company submission path.

Assignment readiness is true only when contract control exists, assignment allowed is confirmed, buyer match exists, buyer proof-of-funds is verified, buyer interest is recorded, compliance review passed, and owner approval is recorded.

The V4 safety guard blocks executable contract generation, legal advice language, live email/SMS/calls, title-company submission, false assignment claims, hidden disclosure language, buyer/seller misrepresentation, and automatic contract status changes.

## V5 Communication Gate

Internal routes:

- `/dashboard/communications`
- `/dashboard/communications/[draftId]`
- `/dashboard/communications/dry-runs`
- `/dashboard/communications/attempts`
- `/dashboard/communications/approvals`

Communication draft records cover seller follow-up drafts, buyer interest response drafts, title handoff email drafts, and internal owner notes. Each draft stores recipient type, recipient email/phone placeholder, source record type/id, subject, draft body, status, safety result, owner approval status, communication live flag, provider readiness, dry-run references, and blocked reasons.

Before a dry-run or send attempt, the safety check blocks pressure language, legal advice, fake urgency, fake buyer claims, guaranteed close claims, misleading assignment language, hidden fee or deception language, missing SMS opt-out language, unsupported claims, bulk language, and campaign language.

Dry-run receipts record:

- Recipient
- Subject/body hash
- Source record
- Risk status
- Safety result
- Timestamp
- Provider mode `mock/dry_run`
- Idempotency key

The live-send gate requires all of these before a mock-send can occur:

- Draft unchanged after dry-run
- Safety passed
- Dry-run receipt exists
- Owner approval recorded
- Global live flag enabled
- Draft communication live flag enabled
- Provider readiness true
- Recipient tied to the source record
- One-send idempotency not already used
- Exactly one recipient

The provider layer contains mock email and SMS adapters only. No provider secrets are required. Blocked attempts create audit records with `provider_called = false`. Even a successful gated attempt is `mock_sent` unless a future owner-controlled provider integration is explicitly added.

V5 live-send limits:

- One recipient only
- One approved draft only
- One source record only
- No bulk send
- No campaigns
- No auto-follow-up sequence
- No buyer blast execution
- No title-company submission

## V6 Seller Portal

Seller-facing routes:

- `/seller-portal`
- `/seller-portal/offer`
- `/seller-portal/property`
- `/seller-portal/timeline`
- `/seller-portal/documents`
- `/seller-portal/messages`

The seller portal shows only approved external-facing offer information:

- Property address summary
- Offer status
- Offer amount
- Closing timeline estimate
- Inspection/access next step
- Title company review status
- Document checklist
- Owner/operator contact placeholder
- Seller question/note intake action

The seller portal never exposes buyer lists, buyer data, buyer purchase price, assignment fee, internal spread strategy, MAO logic, motivation score, seller temperature, lead source, internal notes, Prime 2 recommendations, compliance-risk internals, agent queues, or manager queues.

Seller visibility is allowed only when all of these are true:

- Portal visibility is explicitly enabled
- Offer packet is approved
- Compliance check passed
- Owner approval is recorded
- Contract-control status is valid
- Offer language safety passed
- Contract execution is disabled
- Live negotiation automation is disabled
- Buyer data and internal profit logic exposure are disabled

Seller response records cover seller portal notes, offer questions, appointment/access preferences, and document upload placeholders. They are always review-only: `draft_only = true`, `negotiation_execution_allowed = false`, `contract_execution_allowed = false`, and `automatic_acceptance_allowed = false`.

The internal dashboard shows seller-visible offers, seller portal questions, seller document checklist queue, seller response queue, and blocked seller visibility reasons.

## V7 Unified Deal Room

Internal routes:

- `/dashboard/deal-room`
- `/dashboard/deal-room/[dealRoomId]`
- `/dashboard/closing-coordination`
- `/dashboard/closing-coordination/blockers`
- `/dashboard/closing-coordination/readiness`

Unified deal room records connect each deal to contract control, seller portal status, buyer portal status, title handoff status, assignment readiness status, communication status, compliance status, closing timeline, blockers, next required actions, owner approval status, and projected assignment fees at risk.

The closing coordination checklist tracks:

- Seller accepted offer
- Contract prep ready
- Buyer matched
- Buyer POF verified
- Assignment allowed confirmed
- Title handoff prepared
- Inspection/access coordinated
- Seller documents requested
- Buyer intent recorded
- Compliance review complete
- Owner approval complete

The blocker engine creates internal blocker records for missing buyer POF, missing seller documents, missing compliance review, missing owner approval, weak buyer margin, high-risk language, assignment not confirmed, title handoff incomplete, and communication drafts pending.

The next-best-action engine only recommends internal actions such as reviewing seller response, verifying buyer POF, preparing title handoff, approving a communication dry-run, updating the closing timeline, resolving a compliance blocker, or reviewing assignment readiness.

The V7 safety boundary blocks legal execution, executable contract generation, title-company submission, payment handling, hidden fee/deceptive language, automatic negotiation, and automatic real-world status changes.

## V8 Evidence And Attribution

Internal routes:

- `/dashboard/deal-evidence`
- `/dashboard/deal-evidence/[packetId]`
- `/dashboard/assignment-fees`
- `/dashboard/assignment-fees/[feeId]`

Evidence packets connect a unified deal room to:

- Lead source
- Seller interaction proof
- Underwriting snapshot
- Buyer interest proof
- POF proof status
- Contract control status
- Title handoff status
- Communication receipts
- Blocker history
- Compliance review status

The evidence review gate allows evidence approval only when contract control exists, buyer interest exists, seller acceptance is recorded, compliance passed, source records are present, and no unsupported profit claims are present. Owner review is tracked separately, so a packet may be source-ready but still sit in owner review.

Assignment-fee attribution records track projected assignment fee, target assignment fee, seller contract price, buyer purchase price, buyer margin, attribution basis, confidence score, verification status, owner review status, and 10K+ verification status.

The 10K+ verified flag is true only when:

- The assignment fee equals buyer purchase price minus seller contract price
- The calculated fee meets or exceeds the target assignment fee
- The evidence packet is approved
- Required source records are present

V8 blocks fake profit claims, unsupported ROI claims, invented buyer/seller numbers, client-facing proof without approval, legal guarantees, and closing guarantees. Evidence summaries are sanitized to avoid call notes, motivation answers, pain points, objections, seller temperature, Prime 2 recommendations, and other internal notes.

## V9 Buyer Demand And Distribution Prep

Internal routes:

- `/dashboard/buyer-demand`
- `/dashboard/buyer-demand/[buyerId]`
- `/dashboard/buyer-priority`
- `/dashboard/deal-distribution`
- `/dashboard/deal-distribution/[distributionId]`

Buyer demand profiles track buyer activity score, zip-code demand score, property-type demand score, price-band fit, closing-speed score, proof-of-funds strength, reliability score, last-engaged date, and preferred spread/margin notes.

Buyer priority records rank buyers per deal by target area match, max price fit, POF status, past reliability, closing speed, deal type fit, and buyer margin strength. These rankings create internal recommendations only. They do not contact buyers, negotiate, execute contracts, or publish deal data.

Distribution prep records are draft-only and one-recipient scoped. They store buyer deal email drafts, SMS drafts, a sanitized private deal sheet, buyer call notes, and buyer response trackers. No live send, bulk send, campaign, auto-follow-up, buyer blast, title submission, payment handling, or contract execution is available in V9.

The buyer deal sheet sanitizer exposes only property summary, asking price, ARV range, repair estimate range, buyer margin estimate, access instructions placeholder, availability status, and proof/inspection placeholder notes.

The sanitizer hides seller name/contact, seller contract price unless intentionally represented as asking price, assignment fee logic, lead source, motivation score, internal spread logic, agent recommendations, compliance internals, Prime 2 recommendations, and manager queues.

The V9 safety guard blocks live buyer blasts, bulk sends, misleading scarcity, fake offers, fake buyer competition, seller/private data exposure, assignment fee exposure without approval, legal guarantees, and closing guarantees.

## V10 Offer To Contract Conversion

Internal routes:

- `/dashboard/offer-conversion`
- `/dashboard/offer-conversion/[dealId]`
- `/dashboard/negotiations`
- `/dashboard/negotiations/[recordId]`
- `/dashboard/contract-ready`

Offer positioning records capture strategy type (`cash-fast`, `as-is`, `investor-grade`, or `flexible-close`), seller pain alignment, justification summary, anchor price, walk-away price, ideal contract price, concession range, negotiation notes, confidence score, owner approval status, and safety status.

Negotiation records track seller last response, objections, counteroffer, emotional signals, negotiation stage, next move recommendation, and the acceptance readiness inputs:

- Motivation score
- Price alignment
- Timeline alignment
- Trust level
- Objection resolution
- Contact consistency

The acceptance readiness engine returns low readiness, medium readiness, high readiness, or contract-ready. The contract-ready level requires a high readiness score plus a stabilized stage such as soft-accepted or verbally accepted.

The offer conversion gate allows a contract-ready internal state only when all of these are true:

- Underwriting complete
- Profit control validated
- Buyer demand confirmed
- Compliance passed
- No risk flags
- Seller readiness high
- Owner approval recorded

The contract-ready state means the deal is ready for external contract drafting by attorney/title resources, the seller is likely to sign, numbers are locked, and negotiation is stabilized. It does not create a contract, execute a contract, auto-accept an offer, submit anything to title, or negotiate with the seller.

The deal acceleration engine only recommends internal next moves such as sending an updated offer explanation draft, handling a specific objection, adjusting price within the safe range, moving toward verbal agreement, holding position, or disengaging.

The V10 safety guard blocks legal advice, executable contract generation, automatic acceptance, pressure tactics, fake urgency, fake buyer claims, guaranteed close language, misleading assignment language, deception about role or assignment, and live negotiation automation.

## V11 Title Attorney Review Coordination

Internal routes:

- `/dashboard/title-review`
- `/dashboard/title-review/[reviewId]`
- `/dashboard/review-packets`

Review coordination records track:

- Deal
- V10 contract-ready status
- Selected title company placeholder
- Attorney/title review status
- Required documents
- Missing items
- Review notes
- Owner approval status

Review packet prep is draft-only and organizes:

- Property summary
- Seller terms
- Buyer/assignment readiness summary
- Closing timeline
- Access notes
- Compliance checklist
- Document checklist

The V11 review packet gate allows prep only when all of these are true:

- V10 contract-ready state is cleared
- Compliance passed
- Owner approval recorded
- Numbers locked
- Seller acceptance readiness is high or contract-ready

Even when the gate passes, the review packet is only an internal preparation artifact. It cannot submit documents, email a title company, create or execute a contract, provide legal advice, claim an attorney-client relationship, or guarantee closing.

## V12 Near-Autonomous Execution

Internal routes:

- `/dashboard/autonomy`
- `/dashboard/autonomy/rules`
- `/dashboard/autonomy/runs`
- `/dashboard/autonomy/tasks`
- `/dashboard/autonomy/daily-briefing`
- `/dashboard/autonomy/escalations`

Automation rules define workflow type, autonomy level, trigger event, allowed prep actions, blocked real-world actions, schedule label, owner approval requirement, and safety status.

The scheduler runtime supports these workflows:

- New Lead Intake
- Hot Deal Acceleration
- Buyer Demand Refresh
- Contract Readiness
- Daily Command Briefing

Each scheduler run records idempotency, workflow status, created tasks, attempts, escalation creation, briefing creation, owner approval requirements, autonomy level, and whether any real-world action was taken. V12 always records `real_world_action_taken = false`.

Attempt ledgers record prepared internal actions and blocked real-world attempts. Blocked attempts store action type, source record, blocked reasons, provider-call status, owner approval status, and safety result. Provider calls remain false for blocked attempts.

Autonomous agent tasks route work to divisions and agents for lead scoring, priority queues, seller follow-up drafts, buyer distribution drafts, offer packet drafts, evidence packets, blocker records, contract readiness checks, and daily briefings. Tasks are recommendations or draft preparation only.

Event triggers capture source events such as lead import, hot deal score, buyer demand refresh, gate pass, and daily schedule. Triggers can create runs but cannot publish portals, submit title packets, execute contracts, send messages, contact buyers/sellers, change terms, collect payments, or make commitments.

Daily command briefings are generated by Prime 2 and contain hot deals, priority actions, manager queues, escalations, owner review items, and safety summary. They are internal recommendations only.

Escalations flag urgent owner-review items such as hot 10K+ opportunities, compliance blockers, POF gaps, missing approvals, title blockers, and communication risk. Escalation records never perform the action they recommend.

The autonomy safety guard blocks:

- Autonomous SMS, email, calls, buyer contact, buyer blasts, bulk sends, and campaigns
- Autonomous contract execution, executable contract generation, or binding commitments
- Autonomous title-company submission or review packet submission
- Autonomous buyer/seller portal publishing
- Autonomous payment collection
- Autonomous seller/buyer term changes
- Legal advice
- Level 5 autonomy

Level 4 is owner-approval-required and still cannot bypass the specific communication, portal, title, contract, payment, or compliance gates.

## V13 Controlled Auto-Execution

Internal routes:

- `/dashboard/auto-execution`
- `/dashboard/auto-execution/rules`
- `/dashboard/auto-execution/templates`
- `/dashboard/auto-execution/dry-runs`
- `/dashboard/auto-execution/attempts`
- `/dashboard/auto-execution/audit`

Auto-execution rule records store rule name, action type, source type, allowed recipient type, trigger, required conditions, approved template, autonomy level, live flag requirements, risk score, owner approval status, status, and blocked reasons.

Approved templates cover seller follow-up templates, buyer response templates, internal reminder templates, title/review coordination templates, opt-out-safe SMS templates, and email templates. Template safety blocks pressure language, fake urgency, fake buyer claims, legal advice, contract execution language, hidden assignment fee deception, unsupported claims, and missing SMS opt-out language.

The conditional execution workflow is:

```text
trigger -> template match -> safety check -> dry run -> approval check -> live flag check -> provider readiness -> single execution attempt -> audit record
```

Allowed V13 actions:

- Internal reminders
- Operator task creation
- Approved seller follow-up drafts
- Approved buyer response drafts
- Approved low-risk single-message sends only when V5 gates pass

Blocked V13 actions:

- Bulk campaigns
- Buyer blasts
- Cold SMS automation
- Legal or contract messages
- Seller pressure language
- Fake urgency
- Fake buyer claims
- Any action without an approved rule and approved template

Auto-execution attempts are one-recipient and one-source-record scoped. Idempotency prevents duplicate sends, and every attempt creates an audit record with outcome, blocked reasons, safety snapshot, provider-call status, and source record.

## V14 Buyer Distribution Acceleration

Internal routes:

- `/dashboard/buyer-acceleration`
- `/dashboard/buyer-acceleration/[dealId]`
- `/dashboard/buyer-sequences`
- `/dashboard/buyer-response-router`
- `/dashboard/buyer-velocity`

Buyer acceleration records connect a deal to a buyer ranking snapshot, top buyer list, POF status, reliability, buyer margin strength, distribution readiness, owner approval status, controlled-send status, and blocked reasons.

Smart buyer sequences remain draft-only by default. They can prepare first buyer notice drafts, detail follow-ups, POF requests, viewing/access coordination notes, offer-intent follow-ups, and deadline reminders that avoid deceptive scarcity.

The controlled buyer distribution gate allows a live buyer message only when the deal is buyer-visible, the deal sheet is sanitized, the buyer match is approved, POF status is acceptable or the message is only a POF request, compliance passed, V5/V13 gates passed, no bulk blast is attempted, and owner approval is recorded.

Buyer response routing classifies buyer replies as interested, needs POF, wants access, asks repair details, submits offer intent, not interested, or follow-up later. Routing records recommend owner review and do not execute negotiation or contracts.

## V15 Deal Flow Optimization And Learning

Internal routes:

- `/dashboard/optimization`
- `/dashboard/optimization/patterns`
- `/dashboard/optimization/recommendations`
- `/dashboard/optimization/agent-performance`
- `/dashboard/optimization/lost-deals`
- `/dashboard/optimization/source-quality`

Outcome learning records store lead source, market, seller type, buyer type, offer strategy, follow-up type, conversion result, projected and verified assignment fee, time to contract-ready, blockers, lost reason, source evidence IDs, and confidence score.

Pattern detection identifies best lead types, zip codes, buyer profiles, offer strategies, weak seller scripts, stale follow-up patterns, POF bottlenecks, deals dying before contract-ready, and deals with strong 10K+ probability.

Optimization recommendations are deterministic and explainable. They can suggest market focus, offer range adjustments, lead type priorities, follow-up timing, buyer segments, deal types to avoid, and script/template improvements. Unsupported revenue claims, unsupported ROI, fake profit claims, and unlogged scoring changes are blocked.

## V16 Revenue Forecast And Market Scaling

Internal routes:

- `/dashboard/revenue-forecast`
- `/dashboard/revenue-forecast/[forecastId]`
- `/dashboard/market-scaling`
- `/dashboard/lead-spend-planner`
- `/dashboard/pipeline-value`

Forecast records track period, projected assignment fees, verified assignment fees, probability-adjusted revenue, conservative/base/aggressive scenarios, deals at risk, expected close window, confidence level, source basis, and estimate labels.

Deal probability uses seller readiness, buyer demand, underwriting confidence, compliance status, title/review readiness, blocker severity, buyer POF strength, and communication momentum. These probabilities are estimate-only and source-backed.

Market scaling and lead spend recommendations use lead volume, hot lead percentage, buyer demand, average spread, conversion rate, title/compliance friction, competition risk, evidence basis, and break-even assignment targets. The planner cannot recommend unsupported spend or guaranteed ROI.

## V17 Semi-Autonomous Operator Mode

Internal routes:

- `/dashboard/operator-mode`
- `/dashboard/operator-mode/approvals`
- `/dashboard/operator-mode/exceptions`
- `/dashboard/operator-mode/daily-report`
- `/dashboard/operator-mode/system-trust`
- `/dashboard/operator-mode/settings`

Operator mode settings support manual, assisted, near-autonomous, and semi-autonomous modes. The default remains assisted or near-autonomous; semi-autonomous mode requires owner enablement. Level 5 remains disabled.

The semi-autonomous command loop runs scan, score, route, prepare, check gates, escalate, brief, wait for approvals, log outcomes, and optimize. It prepares internal work and queues real-world actions for owner approval, but it cannot execute contracts, submit title packets, send bulk campaigns, change seller or buyer terms, publish portal data without approval, handle payments, give legal advice, or guarantee closing/profit.

The approval console aggregates seller follow-up live sends, buyer response live sends, offer packet prep, contract-ready status, title review packets, buyer distribution, portal visibility, forecast/spend recommendations, and automation rule activation. Execution stays blocked until each underlying gate passes.

## V18 Production Readiness

The production readiness layer is still private/operator-only. It adds `ApprovalUxReview`, `AuditExportPacket`, `EvidenceAttachmentRecord`, `BackupExportRecord`, `ProviderSandboxReadinessCheck`, `EnvironmentReadinessCheck`, and `DeploymentHardeningCheck` records plus deterministic gates in `app.domain.production_readiness`.

Audit packets are sanitized before review by stripping seller/buyer contact fields, secrets, lead-source details, internal spread strategy, assignment-fee logic, negotiation notes, and compliance internals. Backup/export records expose safe metadata only. Attachment records require source linkage to a source record and a deal or evidence packet, and raw local file paths are blocked. Provider readiness defaults to mock/blocked until sandbox readiness, external secret configuration, safety checks, dry-runs, owner approval, idempotency, and audit trails are present. Production readiness remains blocked when auth, environment variables, secrets, public-exposure hardening, or provider sandbox checks are missing.

## V19 Real Lead Import And Field Testing

V19 is the first real operator field-testing loop. The CSV import engine accepts the supported lead fields from the V19 spec, normalizes phone and email where possible, validates critical fields, dedupes by property address plus owner phone, marks low-confidence rows, creates `LeadImportBatch` and `LeadImportRow` records, and supports preview before commit. Commit only processes approved rows once. Rows missing a property address, rows with invalid critical data, duplicate rows, and operator-blocked rows stay visible with reasons and cannot become leads.

Lead QA creates `LeadQualityReview` records with data quality, contactability, distress signal confidence, equity confidence, import confidence, blocked reasons, and recommended next action. Supported next actions are `research_more`, `underwrite_now`, `call_priority`, `skip_for_now`, and `duplicate_review`.

Field call outcomes are manual operator records only. `FieldCallOutcome` can reduce contactability for wrong/disconnected numbers, block outreach eligibility for do-not-contact records, and escalate motivated/offer-requested/appointment outcomes into internal review tasks. It never places calls, sends messages, or schedules uncontrolled outreach.

The feedback loop stores `PredictionFeedbackRecord` and `ScoringAdjustmentSuggestion` records. Prime 2 compares predicted motivation, contactability, 10K+ opportunity, buyer demand, and contract readiness against actual field outcomes using deterministic scoring explanations. Suggested scoring changes require owner review and are not automatically applied.

V19 routes:

- `/dashboard/lead-imports`
- `/dashboard/lead-imports/[batchId]`
- `/dashboard/lead-imports/preview`
- `/dashboard/lead-qa`
- `/dashboard/lead-qa/[leadId]`
- `/dashboard/call-outcomes`
- `/dashboard/call-outcomes/[outcomeId]`
- `/dashboard/field-testing`
- `/dashboard/feedback-loop`
- `/dashboard/feedback-loop/[feedbackId]`
- `/dashboard/scoring-adjustments`
- `/dashboard/field-briefing`

V19 safety boundary:

- No live outreach from imported rows.
- No bulk SMS, email, calls, or buyer blasts.
- No automatic portal publishing.
- No fake ARV, fake repairs, guaranteed profit, pressure language, legal advice, executable contracts, title submission, or payment handling.
- Do-not-contact outcomes block future live outreach eligibility.
- Owner remains final approver for real-world field actions.

## Frontend Routes

All requested dashboard routes are implemented under `frontend/src/app/dashboard`, including dynamic detail pages:

- `/dashboard`
- `/dashboard/command-center`
- `/dashboard/command-hierarchy`
- `/dashboard/overseer`
- `/dashboard/divisions`
- `/dashboard/divisions/[divisionId]`
- `/dashboard/managers`
- `/dashboard/manager-queue`
- `/dashboard/agents`
- `/dashboard/agents/[agentId]`
- `/dashboard/leads`
- `/dashboard/leads/[leadId]`
- `/dashboard/lead-imports`
- `/dashboard/lead-imports/[batchId]`
- `/dashboard/lead-imports/preview`
- `/dashboard/lead-qa`
- `/dashboard/lead-qa/[leadId]`
- `/dashboard/call-outcomes`
- `/dashboard/call-outcomes/[outcomeId]`
- `/dashboard/field-testing`
- `/dashboard/deals`
- `/dashboard/deals/[dealId]`
- `/dashboard/underwriting`
- `/dashboard/profit-control`
- `/dashboard/seller-acquisition`
- `/dashboard/seller-acquisition/[leadId]`
- `/dashboard/seller-followups`
- `/dashboard/follow-up-control`
- `/dashboard/offer-packets`
- `/dashboard/offer-packets/[packetId]`
- `/dashboard/contract-control`
- `/dashboard/contract-control/[contractId]`
- `/dashboard/title-handoff`
- `/dashboard/title-handoff/[packetId]`
- `/dashboard/assignment-readiness`
- `/dashboard/communications`
- `/dashboard/communications/[draftId]`
- `/dashboard/communications/dry-runs`
- `/dashboard/communications/attempts`
- `/dashboard/communications/approvals`
- `/dashboard/deal-room`
- `/dashboard/deal-room/[dealRoomId]`
- `/dashboard/closing-coordination`
- `/dashboard/closing-coordination/blockers`
- `/dashboard/closing-coordination/readiness`
- `/dashboard/deal-evidence`
- `/dashboard/deal-evidence/[packetId]`
- `/dashboard/assignment-fees`
- `/dashboard/assignment-fees/[feeId]`
- `/dashboard/buyer-demand`
- `/dashboard/buyer-demand/[buyerId]`
- `/dashboard/buyer-priority`
- `/dashboard/deal-distribution`
- `/dashboard/deal-distribution/[distributionId]`
- `/dashboard/buyer-acceleration`
- `/dashboard/buyer-acceleration/[dealId]`
- `/dashboard/buyer-sequences`
- `/dashboard/buyer-response-router`
- `/dashboard/buyer-velocity`
- `/dashboard/offer-conversion`
- `/dashboard/offer-conversion/[dealId]`
- `/dashboard/negotiations`
- `/dashboard/negotiations/[recordId]`
- `/dashboard/contract-ready`
- `/dashboard/title-review`
- `/dashboard/title-review/[reviewId]`
- `/dashboard/review-packets`
- `/dashboard/autonomy`
- `/dashboard/autonomy/rules`
- `/dashboard/autonomy/runs`
- `/dashboard/autonomy/tasks`
- `/dashboard/autonomy/daily-briefing`
- `/dashboard/autonomy/escalations`
- `/dashboard/auto-execution`
- `/dashboard/auto-execution/rules`
- `/dashboard/auto-execution/templates`
- `/dashboard/auto-execution/dry-runs`
- `/dashboard/auto-execution/attempts`
- `/dashboard/auto-execution/audit`
- `/dashboard/optimization`
- `/dashboard/optimization/patterns`
- `/dashboard/optimization/recommendations`
- `/dashboard/optimization/agent-performance`
- `/dashboard/optimization/lost-deals`
- `/dashboard/optimization/source-quality`
- `/dashboard/feedback-loop`
- `/dashboard/feedback-loop/[feedbackId]`
- `/dashboard/scoring-adjustments`
- `/dashboard/field-briefing`
- `/dashboard/revenue-forecast`
- `/dashboard/revenue-forecast/[forecastId]`
- `/dashboard/market-scaling`
- `/dashboard/lead-spend-planner`
- `/dashboard/pipeline-value`
- `/dashboard/operator-mode`
- `/dashboard/operator-mode/approvals`
- `/dashboard/operator-mode/exceptions`
- `/dashboard/operator-mode/daily-report`
- `/dashboard/operator-mode/system-trust`
- `/dashboard/operator-mode/settings`
- `/dashboard/production-readiness`
- `/dashboard/audit-exports`
- `/dashboard/audit-exports/[exportId]`
- `/dashboard/evidence-attachments`
- `/dashboard/provider-readiness`
- `/dashboard/backups`
- `/dashboard/buyers`
- `/dashboard/buyers/[buyerId]`
- `/dashboard/buyer-matches`
- `/dashboard/compliance`
- `/dashboard/daily-briefing`

Buyer-facing V2 routes are implemented under `frontend/src/app/buyer-portal`:

- `/buyer-portal`
- `/buyer-portal/deals`
- `/buyer-portal/deals/[dealId]`
- `/buyer-portal/profile`
- `/buyer-portal/watchlist`

Seller-facing V6 routes are implemented under `frontend/src/app/seller-portal`:

- `/seller-portal`
- `/seller-portal/offer`
- `/seller-portal/property`
- `/seller-portal/timeline`
- `/seller-portal/documents`
- `/seller-portal/messages`

## Guardrails

Blocked in v1:

- Live SMS, email, calls, buyer contact, buyer blast execution
- Paid API calls and skip tracing
- Contract execution
- Legal advice language
- Guaranteed profit claims
- Misrepresentation or hidden assignment fee language
- Public signup and public portals

V2 exception: the controlled buyer portal is allowed only as an invite-gated sanitized deal room. Client portals remain blocked.

V3 exception: seller acquisition drafting is allowed only inside the private command center. Live seller outreach remains blocked.

V4 exception: contract/title preparation is allowed only as draft records, checklists, placeholders, and readiness scoring. Executable contracts, title-company submission, and automatic status changes remain blocked.

V5 exception: communication attempts are allowed only through the controlled gate and default to blocked because the global live flag is off. Dry-runs and blocked attempts are auditable, provider adapters are mock-only, and bulk/campaign/title/buyer-blast paths remain blocked.

V6 exception: the controlled seller portal is allowed only as an invite-gated sanitized offer review room. It can receive draft/intake responses for operator review, but it cannot execute acceptance, negotiate, transmit documents, expose buyer/profit/internal strategy, or provide legal advice.

V7 exception: unified deal rooms are allowed only as internal coordination records. They can show blocker queues, next recommended actions, projected fees at risk, and readiness status inside the operator dashboard, but they cannot execute legal documents, submit title packets, process payments, auto-negotiate, or expose internal data to buyer/seller portals.

V8 exception: evidence and attribution records are allowed only as internal proof and verification records. They can show source-backed fee math, evidence gaps, missing owner review, and verified 10K+ opportunities inside the operator dashboard, but they cannot publish client-facing proof, invent profit support, guarantee ROI, guarantee closing, or expose unsanitized internal notes.

V9 exception: buyer demand and distribution prep records are allowed only as internal ranking and draft-preparation records. They can rank likely buyers, prepare one-recipient drafts, and generate sanitized deal sheets, but they cannot send blasts, send bulk messages, claim fake scarcity or buyer competition, expose seller/private data, expose internal spread logic, guarantee closing, or execute contracts.

V10 exception: offer-to-contract conversion records are allowed only as internal offer positioning, negotiation tracking, readiness scoring, and contract-ready coordination records. They can recommend next moves and mark a deal ready for external attorney/title drafting when gates pass, but they cannot create executable contracts, auto-accept terms, provide legal advice, pressure sellers, fake urgency or buyer demand, guarantee closing, or automate live negotiation.

V11 exception: title/attorney review records and review packets are allowed only as internal draft coordination artifacts. They can track title placeholders, required documents, missing items, compliance checklists, and owner approval, but they cannot submit documents, send title-company email, execute contracts, give legal advice, claim an attorney-client relationship, or guarantee closing.

V12 exception: near-autonomous execution is allowed only for internal scoring, routing, scheduling, draft creation, blocker/evidence creation, readiness marking when existing gates pass, daily briefings, and escalation records. It cannot autonomously send messages, contact buyers or sellers, publish portal data, execute contracts, submit title packets, collect payments, change deal terms, provide legal advice, make commitments, or use Level 5 autonomy. Level 4 remains owner-approval-required and subordinate to every underlying gate.

V13 exception: controlled auto-execution can complete internal reminders and task creation, prepare approved drafts, and mock-send a low-risk single message only when an approved rule, approved template, V5 safety, V5 dry-run receipt, V5 approval, live flags, provider readiness, single-recipient limit, idempotency, and audit creation all pass. It cannot send bulk campaigns, buyer blasts, cold SMS automation, legal/contract messages, pressure language, fake urgency, fake buyer claims, or any unapproved rule/template action.

V14 exception: buyer distribution acceleration is allowed only as internal buyer ranking, sequence drafting, response routing, and velocity scoring. It can identify fastest buyers, POF gaps, controlled-distribution readiness, and draft follow-up sequences, but it cannot send buyer blasts, run bulk sends, expose seller/private data, expose internal spread or assignment-fee strategy, claim fake scarcity or competition, guarantee closing, or bypass the V5/V13 owner-approved one-recipient gate stack.

V15 exception: deal-flow optimization is allowed only as deterministic, explainable, source-backed learning. It can detect patterns, recommend focus markets, tune follow-up priority, score agent performance, and log scoring-weight changes, but it cannot make guaranteed revenue claims, unsupported ROI claims, fake profit claims, or black-box scoring changes without source evidence.

V16 exception: revenue forecasting and market scaling are allowed only as estimate-labeled, source-backed planning tools. They can calculate probability-adjusted pipeline value, conservative/base/aggressive forecast scenarios, market scaling scores, and lead-spend recommendations, but they cannot guarantee revenue or profit, invent close probabilities, recommend unsupported spend, or present ROI without evidence and owner review.

V17 exception: semi-autonomous operator mode can run the internal scan-score-route-prepare-check-escalate-brief-log-optimize loop and queue owner approvals, but it cannot bypass approvals, execute contracts, submit title packets, send bulk campaigns, change seller/buyer terms, publish portals without approval, handle payments, provide legal advice, guarantee closing/profit, or enable Level 5 autonomy.

V18 exception: production readiness records can prepare approval UX summaries, sanitized audit export packets, evidence attachment metadata, backup/export metadata, provider sandbox checks, environment checks, and deployment hardening checklists. They cannot make real provider calls unless sandbox-ready and explicitly gated, expose the system publicly without an auth checklist, commit secrets, include raw private seller/buyer data in unsafe exports, provide legal advice, or convert audit/backup records into live transmissions.

V19 exception: real lead import and field testing can preview CSV rows, commit approved rows once, score lead QA, record manual call outcomes, block do-not-contact eligibility, and suggest explainable scoring adjustments from field feedback. It cannot auto-contact imported leads, create bulk outreach, publish imported rows to portals, invent valuation/profit inputs, guarantee deals, execute contracts, submit to title, collect payments, or apply scoring changes without owner review.

Allowed:

- Analysis
- Scoring
- Drafting
- Recommendations
- Escalations
- Risk flags
- Checklist preparation

## Migration Strategy

The initial Alembic revision creates the SQLAlchemy metadata-defined schema. The backend defaults to SQLite for local operator use and switches to Postgres when `DATABASE_URL` points to a Postgres database.
