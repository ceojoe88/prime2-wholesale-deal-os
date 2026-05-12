# Prime 2 Wholesale Deal OS - System Overview

## Project Identity

Name: Prime 2 Wholesale Deal OS

Overseer: Prime 2

Relationship: Prime 2 is the brother system to Vylarion Prime.

Purpose: Prime 2 Wholesale Deal OS is a private virtual wholesale real estate operating system for a single owner/operator. It helps identify, underwrite, control, coordinate, and assign wholesale real estate opportunities while preserving owner approval, compliance boundaries, buyer margin, seller offer reasonableness, and source-backed deal evidence.

This is not a SaaS product, public marketplace, buyer blast tool, seller portal marketplace, legal platform, payment system, or contract execution product.

## What The System Does

Prime 2 Wholesale Deal OS supports the full internal acquisition-to-assignment workflow:

- Lead scoring and motivation ranking
- Market and distressed-property intelligence
- Deal underwriting, ARV inputs, repair estimates, MAO, and buyer max price
- Middle-man profit control for target 10K+ assignment-fee opportunities
- Seller acquisition tracking and draft-only follow-up preparation
- Buyer disposition, buyer matching, demand scoring, and distribution prep
- Invite-gated buyer and seller portals with sanitized external views
- Unified internal deal rooms and closing coordination
- Contract-control preparation without executable contract generation
- Title/attorney review coordination without title submission
- Evidence packets and assignment-fee attribution tied to source records
- Buyer demand intelligence and controlled distribution acceleration
- Offer-to-contract conversion readiness without automatic acceptance
- Deterministic optimization and learning from outcomes
- Forecasting, market scaling, and lead spend planning as estimates only
- Near-autonomous and semi-autonomous internal operator workflows
- Production readiness checks, safe audit exports, attachment metadata, and backup/export metadata
- Real CSV lead import, lead QA, field-call outcome tracking, and prediction feedback
- Controlled AI drafting, summarization, negotiation support, and briefing through a safety/cost/audit gateway
- Background worker runtime for scheduled internal prep jobs, retries, idempotency, ledgers, and heartbeat monitoring
- Provider sandbox and credential readiness checks for future integrations without storing secrets or making uncontrolled provider calls
- Seller call intelligence from manual notes or pasted transcripts, including DNC detection, objections, quality scoring, and draft-only follow-up recommendations
- Deal document intelligence for classification, metadata extraction, issue flags, review routing, and sanitized evidence links
- Controlled campaign planning, segmentation, sequence prep, activation gates, stop conditions, and performance tracking
- Mobile operator mode for field-call queues, quick notes, DNC capture, approvals, buyer checks, document metadata, offline-safe drafts, and field briefings
- Production cloud readiness for private deployment profiles, masked environment validation, backup/restore metadata, monitoring readiness, and fail-closed hosting checks
- Controlled live provider activation records for one-action OpenAI, email, SMS, CRM, and storage lanes gated by safety, dry-runs, owner approval, provider readiness, cloud readiness, idempotency, and audit logs
- First Deal Cockpit execution guidance for real lead batches, QA, seller calls, offer decisions, buyer validation, contract-ready prep, assignment-fee evidence, and field-test reports
- Client Command OS workspace, lead intelligence, acquisition prep, underwriting decision-support, buyer matching, and disposition readiness layers that hide internal Prime governance and provider internals

## Command Hierarchy

Owner:

- Human operator and final approver
- Controls every real-world action
- Approves high-risk action, portal visibility, live communication, spend recommendations, and readiness transitions

Prime 2:

- Executive overseer
- Oversees seller acquisition and buyer disposition
- Ranks 10K+ opportunities
- Protects buyer margin and seller offer reasonableness
- Blocks unsafe, deceptive, unsupported, or non-compliant action
- Coordinates managers and expert agents
- Escalates owner approvals and risk exceptions
- Generates daily operating reports
- Maintains compliance boundaries and evidence discipline

Divisions:

- Market Intelligence Division
- Lead Intelligence Division
- Seller Acquisition Division
- Deal Underwriting Division
- Middle-Man Profit Control Division
- Buyer Disposition Division
- Contract & Compliance Division
- Follow-Up Division
- Operations Command Division

Managers and expert agent teams:

- Managers own division queues, workload, risk flags, recommendations, and next best actions.
- Expert agents analyze, score, draft, recommend, escalate, and prepare checklists.
- Agents cannot contact sellers, contact buyers, execute contracts, submit title packets, collect payment, provide legal advice, or bypass owner approval.

## Safety Model

The core safety line is recommendation versus execution.

Allowed by design:

- Analyze
- Score
- Draft
- Recommend
- Escalate
- Flag risk
- Prepare checklists
- Prepare internal packets
- Record evidence and audit metadata

Blocked by design:

- Public signup
- Uncontrolled live SMS, email, or calls
- Bulk buyer blasts and campaigns
- Cold SMS automation
- Executable contract generation
- Automatic contract execution
- Title-company submission
- Payment handling
- Legal advice
- Guaranteed profit or guaranteed closing claims
- Fake ARV, fake repairs, or unsupported profit claims
- Deceptive urgency, fake scarcity, or fake buyer claims
- Hidden assignment-fee deception
- Autonomous portal publishing
- Autonomous seller or buyer term changes
- Level 5 full autonomy

Controlled provider/action stack:

1. Safety check passes.
2. Draft-only record exists.
3. Dry-run receipt is created.
4. Draft is unchanged after dry run.
5. Owner approval is recorded.
6. Global live flag is enabled.
7. Communication or auto-execution live flag is enabled.
8. Provider sandbox/readiness is true.
9. Recipient is tied to the source record.
10. One-recipient and no-bulk constraints pass.
11. Idempotency prevents duplicate sends.
12. Attempt and audit records are created.

Default provider mode remains mock/dry-run. No real provider secrets are required or committed.

## Phase Map V1-V31

V1 Private Operator Deal OS:
Established the single-owner dashboard, divisions, managers, expert agents, lead scoring, underwriting, profit control, buyer matching, compliance checklists, seed data, and private-mode safety rules.

V2 Buyer Portal and Deal Room:
Added invite-gated buyer deal rooms with sanitized buyer-facing deal data, publishing gates, buyer interest records, and no seller/internal/profit logic exposure.

V3 Seller Acquisition and Follow-Up Gate:
Added seller pipeline command center, interaction records, draft-only scripts and follow-up sequences, offer packet prep gate, and seller safety language checks.

V4 Contract Control and Title Handoff Gate:
Added contract-control records, contract prep gates, title handoff packet prep, assignment readiness gates, and blocks against executable contracts or title submission.

V5 Controlled Live Communication Gate:
Added communication drafts, safety checks, dry-run receipts, owner approvals, mock provider adapters, one-recipient send gates, and blocked attempt audit records.

V6 Seller Portal and Offer Review Room:
Added invite-gated seller portal routes, sanitized offer room, seller visibility gate, seller response records, and no buyer/profit/internal exposure.

V7 Unified Deal Room and Closing Coordination:
Connected seller room, buyer room, contract control, title handoff, communications, assignment readiness, blockers, checklists, and next best actions into one internal coordination layer.

V8 Deal Evidence and Assignment Fee Attribution:
Added evidence packets, source-backed assignment fee attribution, 10K+ verification logic, unsupported claim guards, and internal-note sanitization.

V9 Buyer Demand Intelligence and Distribution Prep:
Added buyer demand profiles, per-deal buyer priority ranking, sanitized private deal sheets, distribution drafts, and buyer-side safety guards.

V10 Offer-to-Contract Conversion Gate:
Added offer positioning, negotiation tracking, acceptance readiness scoring, contract-ready internal status, and safety gates against pressure, fake claims, or contract execution.

V11 Title Company and Attorney Review Coordination:
Added review coordination records and review packet prep for contract-ready deals without document submission, legal advice, or title-company email sending.

V12 Near-Autonomous Execution Engine:
Added automation rules, scheduler runtime, run and attempt ledgers, autonomous agent tasks, triggers, daily briefings, and escalation queues. Level 5 is disabled.

V13 Controlled Auto-Execution Gate:
Added approved rules, approved templates, conditional dry-run/approval/live-flag workflow, idempotent single attempts, and auto-execution audit records.

V14 Buyer Distribution Acceleration:
Added buyer acceleration records, smart buyer sequence prep, controlled distribution gate, buyer response router, and buyer velocity scoring.

V15 Deal Flow Optimization and Learning:
Added deterministic outcome learning, pattern detection, optimization recommendations, agent performance scoring, and source-backed scoring weight changes.

V16 Revenue Forecast and Market Scaling:
Added forecast records, deal probability scoring, market scaling scores, lead spend planner, and estimate-labeled pipeline value views.

V17 Semi-Autonomous Operator Mode:
Added operator mode settings, semi-autonomous command loop, owner approval console, exception management, daily operating report, and system trust scoring.

V18 Production Readiness Layer:
Although outside the requested V1-V17 phase map, the current project also includes V18 production readiness, audit export packets, evidence attachment metadata, backup/export metadata, provider sandbox readiness checks, environment readiness checks, and deployment hardening docs.

V19 Real Lead Import and Field Testing Loop:
Added preview-first CSV lead import, import batch and row records, critical field validation, phone/email normalization, property-plus-phone dedupe, lead QA scoring, call outcome tracking, do-not-contact eligibility blocking, Prime 2 prediction-versus-reality feedback, deterministic scoring adjustment suggestions, and field-testing daily briefing. Imports remain private/operator-only and cannot trigger live outreach, bulk messages, portal publishing, contract execution, title submission, or payment handling.

V20 AI Gateway:
Added a controlled intelligence layer for approved request types only: seller script drafts, buyer message drafts, objection responses, deal summaries, daily briefings, negotiation assistance, and field-testing summaries. The gateway enforces versioned templates, system-data-only numbers, response safety scanning, token/cost tracking, monthly caps, environment-only API key loading, request audit logs, and blocks legal advice, contract generation, guaranteed profit claims, deceptive urgency/scarcity, and financial calculation overrides.

V21 Background Worker Runtime:
Added a production-grade internal worker layer with queued jobs, scheduler cadence, retries/backoff, job ledgers, idempotency keys, heartbeat health, stuck-job detection, and Prime 2 routing. Supported jobs are internal prep only: lead scoring refresh, follow-up scheduling, daily briefing generation, buyer ranking refresh, QA checks, automation rule evaluation, field-testing summary, and forecast refresh. The worker cannot trigger live outreach, buyer blasts, contract execution, title submission, portal publishing, payment handling, or term changes.

V22 Provider Sandbox Readiness Gate:
Added provider registry records for OpenAI, email, SMS, CRM, skip-trace, storage, and webhook categories; mock/sandbox/live mode separation; env-only credential reference checks; masked provider responses; provider attempt audits; and webhook review records. No secret values are stored, no real provider calls are made by default, live readiness remains owner-gated, and webhook events cannot mutate deals automatically.

V23 Call Intelligence Layer:
Added text-only call intelligence sessions for manual notes and pasted transcripts, seller signal extraction, objection records, motivation/contactability/readiness deltas, call quality scoring, follow-up recommendations, DNC detection tied to outreach eligibility blocks, and compliance escalation for title/contract questions. It can draft and recommend only; it does not place calls, record audio, send responses, change offer terms, or bypass V5/V13 communication gates.

V24 Deal Document Intelligence:
Added internal document intelligence files, classification results, extracted document fields, issue flags, review tasks, and document evidence links. Prime 2 can classify and extract metadata from manual entries or pasted text, flag missing signatures, price mismatches, POF gaps, unclear assignment language, risky phrases, and external review reminders. It does not provide legal conclusions, rewrite documents, generate executable contracts, submit files to title, or publish documents to portals automatically.

V25 Controlled Campaign Brain:
Added campaign rule records, audience previews, sequence steps, activation attempts, stop events, and performance records. Campaigns default to draft, exclude DNC/high-risk records, require approved templates, owner approval, caps, stop conditions, audience approval, V5/V13/V22 gates for any live path, one-recipient events, idempotency, and audit. It cannot run uncontrolled outreach, mass sends, deceptive scarcity, fake claims, or approval bypass.

V26 Market Data Enrichment:
Added market profiles, comparable sale records, rent estimates, buyer activity snapshots, and lead source ROI records. Prime 2 can improve ARV confidence from comp count, recency, distance, and market confidence; improve buyer-demand confidence from POF strength, fast-close depth, response velocity, and recent interest; and rank markets with evidence-backed heat scoring. V26 is manual/import-data only and cannot invent comps, invent ARV, guarantee ROI, call paid external APIs, or auto-scale spend/outreach.

V27 Prime 2 Memory + Learning Layer:
Added source-cited memory items, learning signals, scoring weight recommendations, and playbook recommendations. Prime 2 can remember winning scripts, weak lead sources, strong buyer profiles, high-spread markets, document issue patterns, campaign patterns, pricing adjustments, and compliance risk patterns. Scoring changes require owner approval, AI context uses approved memory as context only, and memory cannot invent facts, override compliance, expose internal strategy to portals, or create unsupported claims.

V28 Mobile Operator Mode:
Added `/mobile` field command routes plus a mobile operator API aggregation layer for top money actions, risk actions, call queue, lead/deal detail, approvals, field briefing, buyer snapshots, document metadata, mobile note capture, quick DNC mark, offline draft sync, and quick approval gate checks. Mobile mode captures and routes only; it cannot send outreach, execute contracts, publish portals, change terms, submit title packets, or bypass safety/dry-run/provider/idempotency gates.

V29 Production Cloud Readiness:
Added cloud deployment profiles, environment validation, security checks, backup/restore readiness metadata, monitoring snapshots, and `/api/v1/cloud-readiness` endpoints. The production profile fails closed when auth, env, CORS, database, frontend API, backup, provider flags, or secret posture are unsafe. V29 does not deploy the system or activate providers; it reports readiness only.

V30 Controlled Live Provider Activation:
Added provider activation records, attempts, blocked attempts, and audit events for OpenAI generation, single email, single SMS, CRM sync eligibility, and sanitized storage upload lanes. Every lane requires source linkage, dry-run hash verification, owner approval, live flag status, provider readiness, production cloud readiness, idempotency, one-action constraints, and sanitized audit responses. Bulk sends, buyer blasts, worker bypass, campaign bulk execution, legal/title/contract/payment actions, and source-changed-after-dry-run attempts remain blocked.

V31 Real Deal Execution Pack:
Added the First Deal Cockpit for the first real wholesale execution loop: imported real leads, QA, prioritized calls, manual call outcomes, underwriting, offer decisioning, buyer validation, contract-ready readiness, title/attorney review prep, assignment-fee evidence, field-test reporting, and Prime 2 execution coaching. V31 is guidance and tracking only; the owner still performs and approves real-world action, and the cockpit cannot send outreach, execute contracts, submit title packets, handle payments, publish portals, or provide legal guidance.

CP1 Client Workspace Foundation:
Added tenant-safe client workspaces, members, roles, permissions, and sanitized client workspace APIs. Client access cannot expose internal Prime governance, raw provider payloads, secrets, billing, e-signature, or admin-only controls.

CP2 Lead Intelligence Division:
Added deterministic lead scoring, missing-data items, hot lead boards, next-best-action records, and client-safe Lead Intelligence Manager status. CP2 remains the source of truth for lead priority, missing data, and next action.

CP3 Acquisition AI Team:
Added Acquisition Manager briefs, seller question plans, objection response drafts, manual follow-up drafts, appointment readiness reviews, and acquisition division events. CP3 is non-live; drafts are manual-use only and no message is sent.

CP4 Underwriting + Deal Evidence:
Added deal evidence packets, evidence items, underwriting reviews, offer scenarios, offer readiness gates, and Underwriting Manager events. CP4 is decision support only; no provider data pulls, offers, contracts, title submissions, payments, legal advice, or profit guarantees are created.

CP5 Buyer Matching + Disposition Readiness:
Added buyer profiles, buy boxes, buyer confidence scoring, deterministic deal-to-buyer matching, buyer demand evidence, disposition readiness gates, manual-only buyer outreach drafts, and Disposition Manager events. CP5 is non-live; no buyer is contacted, no campaign starts, no provider calls occur, and no buyer purchase/profit/assignment result is guaranteed.

Client Command now extends through CP12 with guarded backend surfaces for subscription plan gating, controlled communication gating, billing gating, and pilot/support coordination. These phases preserve non-live defaults, no bulk campaigns, no autonomous execution, no raw card data storage, no source-gate bypass, and no client exposure to Prime governance internals.

## Local Run Commands

Backend setup:

```powershell
cd backend
python -m venv ..\.venv
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\.venv\Scripts\alembic.exe upgrade head
..\.venv\Scripts\python.exe seed.py
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Frontend setup:

```powershell
cd frontend
npm install
npm run dev
```

Local URLs:

- Frontend dashboard: http://localhost:3000/dashboard
- Mobile operator mode: http://localhost:3000/mobile
- Cloud readiness: http://localhost:3000/dashboard/cloud-readiness
- Live activation: http://localhost:3000/dashboard/live-activation
- First Deal Cockpit: http://localhost:3000/dashboard/first-deal-cockpit
- Backend health: http://localhost:8000/health
- Backend API root examples: http://localhost:8000/api/command-center and http://localhost:8000/api/system/rules
- Buyer portal demo: http://localhost:3000/buyer-portal
- Seller portal demo: http://localhost:3000/seller-portal

## Validation Checklist

Run before trusting a change:

```powershell
cd backend
..\.venv\Scripts\alembic.exe upgrade head
..\.venv\Scripts\python.exe seed.py
..\.venv\Scripts\python.exe -m pytest

cd ..\frontend
npm test
npm run build
npm audit --omit=dev
```

Recommended route smoke checks:

- `/dashboard`
- `/dashboard/command-center`
- `/dashboard/overseer`
- `/dashboard/autonomy`
- `/dashboard/auto-execution`
- `/dashboard/lead-imports`
- `/dashboard/lead-qa`
- `/dashboard/call-outcomes`
- `/dashboard/field-testing`
- `/dashboard/feedback-loop`
- `/dashboard/scoring-adjustments`
- `/dashboard/field-briefing`
- `/dashboard/ai`
- `/dashboard/ai/audit`
- `/dashboard/ai/costs`
- `/dashboard/ai/templates`
- `/dashboard/worker`
- `/dashboard/worker/jobs`
- `/dashboard/worker/health`
- `/dashboard/buyer-acceleration`
- `/dashboard/optimization`
- `/dashboard/revenue-forecast`
- `/dashboard/operator-mode`
- `/dashboard/production-readiness`
- `/dashboard/backups`
- `/mobile`
- `/mobile/today`
- `/mobile/calls`
- `/mobile/approvals`
- `/dashboard/cloud-readiness`
- `/dashboard/cloud-readiness/env`
- `/dashboard/cloud-readiness/security`
- `/dashboard/cloud-readiness/backups`
- `/dashboard/cloud-readiness/monitoring`
- `/dashboard/cloud-readiness/deployment-checklist`
- `/dashboard/live-activation`
- `/dashboard/live-activation/readiness`
- `/dashboard/live-activation/approvals`
- `/dashboard/live-activation/attempts`
- `/dashboard/live-activation/blocked`
- `/dashboard/first-deal-cockpit`
- `/dashboard/first-deal-cockpit/calls`
- `/dashboard/first-deal-cockpit/offers`
- `/dashboard/first-deal-cockpit/buyer-validation`
- `/dashboard/first-deal-cockpit/contract-ready`
- `/dashboard/first-deal-cockpit/evidence`
- `/dashboard/first-deal-cockpit/report`
- `/buyer-portal`
- `/seller-portal`

Recommended source sweeps:

```powershell
Get-ChildItem -Recurse -File -Include *.py,*.ts,*.tsx,*.mjs,*.md backend,frontend\src,frontend\tests,docs,README.md |
  Select-String -Pattern ("Wholesale" + " Prime") -CaseSensitive:$false

Get-ChildItem -Recurse -File -Include *.py,*.ts,*.tsx backend,frontend\src |
  Select-String -Pattern "execute contract|submit to title|buyer blast|bulk send|guaranteed profit|legal advice" -CaseSensitive:$false
```

No legacy overseer/product wording should remain in runtime source. The product/system identity is `Prime 2 Wholesale Deal OS`, and the overseer identity is `Prime 2`.

## Production Readiness Notes

The system is local-first. It can be prepared for a hosted deployment later, but public exposure is intentionally blocked until authentication, environment, secrets, provider sandbox, backup, audit export, and deployment hardening checks pass.

Production checklist:

- Keep operator authentication private and explicit.
- Keep secrets out of the repository.
- Use `DATABASE_URL` for Postgres when leaving local SQLite.
- Run Alembic migrations before app startup.
- Verify backup/export metadata before relying on exports.
- Keep audit exports sanitized and owner-approved.
- Keep provider integrations in sandbox/mock mode until all gates pass.
- Keep legal/title review external with qualified professionals.
- Keep contracts external and non-executable inside this app.

## Real-World Usage Boundary

Prime 2 Wholesale Deal OS supports wholesale real estate operations, but it does not replace professional judgment, local/state law compliance, attorney review, title company review, or licensed professional guidance where required.

Forecasts, buyer margins, assignment fees, ARV inputs, repair estimates, and probability scores are estimates or source-backed internal calculations. They are not guaranteed profits, guaranteed closings, legal advice, investment advice, or binding commitments.
## Client Command OS

The client-facing Prime2 Client Command OS runtime currently spans CP1 through CP12.

Current controlled loop:
Lead Intelligence -> Acquisition Prep -> Underwriting -> Buyer Matching -> Compliance Contact Gate -> Weekly Client Command Report -> Client Onboarding + Workspace Activation Readiness

CP6 through CP12 remain gated and non-live by default:
- no provider calls
- no DNC checks
- no 10DLC registration
- no live communication
- no guaranteed ROI or revenue claims

CP8 adds:
- business and strategy profiles
- market and pipeline setup
- lead-source and buyer-list setup review
- team and compliance setup checklists
- first-lead readiness tracking
- workspace readiness scoring
- activation blockers
- manual-operation go-live gating
- onboarding tasks and timeline events
- first weekly-cycle readiness
- client-safe onboarding reports

CP9 through CP12 add:
- CP9 subscription plan gating readiness
- CP10 controlled live communication gate
- CP11 Stripe billing live payment gate
- CP12 pilot client operating mode and admin support console

Those phases keep the same hard boundaries:
- default non-live posture until each gate is explicitly cleared
- no bulk campaigns
- no autonomous execution
- no raw card data storage
- no bypass of source-linked gates in pilot or support modes
- Prime governance internals remain private
