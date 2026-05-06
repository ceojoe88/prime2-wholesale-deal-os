# Prime 2 Wholesale Deal OS

Private, operator-only virtual wholesale real estate command system with an executive overseer named **Prime 2**. Prime 2 is the brother system to Vylarion Prime and is purpose-built to help a single owner identify, underwrite, control, coordinate, and assign wholesale real estate opportunities while preserving owner approval, compliance boundaries, buyer margin, seller offer reasonableness, and evidence-backed profit attribution.

This repository is not a SaaS product, public CRM, buyer/seller marketplace, legal platform, contract execution system, payment product, skip-tracing service, or live outreach campaign tool.

## Why This Project Exists

Wholesale deal flow can become messy fast: lead sources, seller motivation, ARV inputs, repairs, MAO, assignment spread, buyer demand, proof of funds, title readiness, compliance flags, follow-up timing, and owner approvals all compete for attention. Prime 2 Wholesale Deal OS gives the owner a governed internal operating layer for those decisions.

The useful outcome is speed with guardrails:

- Find and rank motivated seller leads.
- Underwrite deals with explicit ARV, repairs, buyer costs, MAO, max seller offer, and target assignment fee math.
- Protect buyer margin and seller offer reasonableness.
- Identify 10K+ assignment-fee opportunities from source records.
- Prepare seller and buyer communications as drafts.
- Coordinate controlled buyer/seller portal views without leaking internal strategy.
- Keep legal, title, payment, live outreach, and high-risk actions gated.

## Prime 2 Identity

Prime 2 is the executive overseer for the private Prime 2 Wholesale Deal OS and the brother system to Vylarion Prime.

Prime 2 oversees seller acquisition, buyer disposition, 10K+ opportunity ranking, buyer margin protection, seller offer reasonableness, manager/agent routing, owner approval escalation, daily operating reports, and unsafe-action blocking. Prime 2 recommends, drafts, scores, routes, escalates, and briefs. It does not bypass owner approval or execute high-risk real-world actions.

## Current System Status

Implemented phases:

- V1 private operator-only Prime 2 Wholesale Deal OS
- V2 controlled buyer portal and deal room
- V3 seller acquisition and follow-up gate
- V4 contract control and title handoff gate
- V5 controlled live communication gate
- V6 seller portal and offer review room
- V7 unified deal room and closing coordination
- V8 deal evidence and assignment fee attribution
- V9 buyer demand intelligence and distribution prep
- V10 offer-to-contract conversion gate
- V11 title company and attorney review coordination
- V12 near-autonomous execution engine
- V13 controlled auto-execution gate
- V14 buyer distribution acceleration engine
- V15 deal flow optimization and learning engine
- V16 revenue forecast and market scaling engine
- V17 semi-autonomous operator mode
- V18 production readiness and audit export layer
- V19 real lead import and field testing loop
- V20 AI Gateway controlled intelligence layer
- V21 background worker runtime
- V22 provider sandbox and credential readiness gate
- V23 call intelligence layer
- V24 deal document intelligence
- V25 controlled campaign brain
- V26 market data enrichment
- Prime 2 overseer rebrand

## Core Capabilities

Backend:

- FastAPI API with SQLAlchemy models
- Alembic migrations
- SQLite for local use and Postgres-ready `DATABASE_URL`
- Seed/demo data for divisions, managers, agents, leads, buyers, deals, portals, evidence, forecasts, automation, audit exports, production readiness, real lead imports, QA, call outcomes, and field feedback
- Deterministic domain modules for scoring, underwriting, profit control, portals, communication gates, automation, optimization, forecasting, readiness checks, CSV import QA, field-call outcome tracking, prediction feedback, controlled AI drafting/summarization, and background worker jobs
- Tests for safety gates, formulas, route coverage, portal sanitizers, automation blocks, evidence attribution, production readiness, seed integrity, real CSV import, lead QA, call outcomes, field-testing guardrails, AI Gateway safety/cost/audit controls, and worker runtime idempotency/retry/heartbeat behavior

Frontend:

- Next.js and TypeScript dashboard
- Premium dark internal command UI
- `/dashboard/*` command surfaces for the operator
- Invite/gated buyer portal routes under `/buyer-portal`
- Invite/gated seller portal routes under `/seller-portal`
- Detail pages guard missing IDs with `notFound()`
- Portal pages avoid seller/internal/profit logic leakage

## V19 Field Testing Workflow

V19 moves the project from demo-ready toward real operator testing:

- Import CSV lead lists through a preview-first batch system.
- Validate critical fields, normalize phone/email, dedupe by property address and owner phone, and show blocked rows with reasons.
- Commit approved rows only once; blocked rows, duplicate rows, and invalid critical rows cannot become leads.
- Run lead QA for data quality, contactability, distress confidence, equity confidence, and recommended next action.
- Record real seller call outcomes manually, including do-not-contact, wrong number, motivated, offer requested, and appointment set.
- Compare Prime 2 predictions against real field outcomes and queue deterministic, explainable scoring adjustment suggestions.
- Generate a Prime 2 field briefing with call-priority leads, research gaps, first-deal candidates, prediction misses, and owner next actions.

CSV imports never auto-contact sellers, create campaigns, publish portals, execute contracts, submit title packets, or change terms.

## V20 AI Gateway And V21 Worker Runtime

V20 adds a controlled AI Gateway for Prime 2. It allows only approved request types such as seller script drafts, buyer message drafts, objection responses, deal summaries, daily briefings, negotiation assistance, and field-testing summaries. Outputs are template-gated, scanned for unsafe language, cost-estimated, audit-logged, and blocked from inventing numbers or overriding system calculations. `OPENAI_API_KEY` is read from the environment only, and the default provider mode remains mock/dry-run.

V21 adds a background worker runtime for continuous internal operation. It supports queued jobs for lead scoring refresh, follow-up scheduling, daily briefing generation, buyer ranking refresh, QA checks, automation rule evaluation, field-testing summaries, and forecast refresh. Jobs have idempotency keys, retry/backoff, status ledgers, and heartbeat health. The worker can prepare, schedule, route, draft, and escalate only; it cannot send live outreach, execute contracts, publish portals, submit to title, change terms, handle payments, or bypass approval gates.

## V22 Provider Sandbox Readiness

V22 adds a provider registry and credential readiness gate for future OpenAI, email, SMS, CRM, skip-trace, storage, and webhook integrations. Providers default to mock mode, credential values are never stored, only masked environment reference names are surfaced, sandbox/live modes are separated, and every attempt records readiness, idempotency, metadata hashes, blocked reasons, and audit-only status.

Webhook handling is a skeleton for mock or sandbox events only. Events create review queue records and never mutate deals automatically. Unsigned live-like webhook payloads are rejected and recorded safely.

## V23 Call Intelligence

V23 converts manual seller call notes and pasted text transcripts into structured intelligence: motivation reason, urgency, asking price, condition clues, objections, decision-maker status, trust, price flexibility, follow-up preference, DNC detection, risk flags, quality score, and next best action. It is text-only; no audio processing, live calling, or automatic response execution is added.

Do-not-contact detection creates a V19 call outcome and blocks future outreach eligibility. Legal/title/contract questions create compliance escalations and attorney/title review reminders. Objections produce safe draft-only responses that remain owner-reviewed and cannot send without the existing V5/V13 gates.

## V24 Deal Document Intelligence

V24 adds internal document intelligence for deal files. Prime 2 can classify purchase agreements, assignment agreements, proof-of-funds letters, title docs, seller/buyer docs, inspection notes, repair estimates, comp reports, and other files from manual metadata or pasted text. It extracts safe metadata such as parties, property address, prices, dates, signatures, assignment-language presence, POF amount, and title company name.

The layer flags missing fields, price mismatches, weak POF, unclear assignment language, risky language, unsupported ARV/repair claims, and external review needs. It is review routing only: no legal conclusions, no contract rewriting, no file delivery, no title submission, and no automatic portal publishing.

## V25 Controlled Campaign Brain

V25 adds campaign planning and governance for sellers, buyers, stale leads, appointment reminders, POF requests, and internal operator pushes. Campaigns default to draft, segment audiences with DNC/compliance/quality exclusions, prepare safe sequences, require owner approval and daily caps, and pause on replies, DNC, compliance risk, provider readiness failure, owner pause, or max attempts.

This is not a mass outreach engine. Controlled activation is one-recipient/one-message-event based, audited, idempotent, capped, and any live path remains subordinate to V5 communication safety, V13 auto-execution rules/templates, V22 provider readiness, dry-runs, live flags, and owner approval.

## V26 Market Data Enrichment

V26 adds market profiles, comparable sale records, rent estimates, buyer activity snapshots, and lead source ROI records. Prime 2 can rank markets, improve ARV confidence from recent nearby comps, strengthen buyer-demand confidence from POF and velocity evidence, and label source ROI as estimate-only when cost or outcome evidence is incomplete.

V26 uses manual/imported data only. It does not call paid external APIs, invent comps, invent ARV, guarantee ROI, or turn market ranking into automated spend or outreach.

## Safety Boundaries

Allowed:

- Analyze, score, draft, recommend, escalate, flag risk, prepare checklists, prepare packets, and record evidence.

Blocked:

- Public signup
- Public client portal
- Uncontrolled SMS, email, or calls
- Bulk sends, buyer blasts, and campaigns
- Cold SMS automation
- Executable legal contract generation
- Automatic contract execution
- Title-company submission
- Payment handling
- Legal advice
- Guaranteed closing or guaranteed profit claims
- Fake ARV, repairs, buyer claims, scarcity, urgency, or ROI
- Hidden assignment-fee deception
- Autonomous portal publishing
- Autonomous seller or buyer term changes
- Level 5 full autonomy
- AI legal/contract/profit-promise output
- Worker live outreach, title, contract, portal publishing, payment, or bulk-send execution
- Provider secret storage or uncontrolled provider calls
- Live call recording, live calling, or automatic seller response from call intelligence

Controlled provider actions require all relevant gates:

- Safety check
- Draft record
- Dry-run receipt
- Unchanged draft hash
- Owner approval
- Global live flag
- Communication or auto-execution live flag
- Provider readiness
- Recipient-source linkage
- One-recipient/no-bulk limit
- Idempotency
- Attempt and audit record

Default provider mode is mock/dry-run. No real provider secrets are required.

## Repository Map

- [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md): complete system identity, phase map, safety model, local run commands, and production readiness notes.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): domain architecture, route map, data model, and guardrails.
- [docs/VALIDATION.md](docs/VALIDATION.md): validation commands and audit checklist.
- [backend](backend): FastAPI app, models, domain modules, migrations, seed script, and backend tests.
- [frontend](frontend): Next.js app routes, dashboard components, demo data, navigation, and frontend route tests.

## Local Setup

Backend:

```powershell
cd backend
python -m venv ..\.venv
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\.venv\Scripts\alembic.exe upgrade head
..\.venv\Scripts\python.exe seed.py
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

Open:

- Dashboard: [http://localhost:3000/dashboard](http://localhost:3000/dashboard)
- Command center: [http://localhost:3000/dashboard/command-center](http://localhost:3000/dashboard/command-center)
- Prime 2 overseer: [http://localhost:3000/dashboard/overseer](http://localhost:3000/dashboard/overseer)
- Autonomy: [http://localhost:3000/dashboard/autonomy](http://localhost:3000/dashboard/autonomy)
- Operator mode: [http://localhost:3000/dashboard/operator-mode](http://localhost:3000/dashboard/operator-mode)
- Field testing: [http://localhost:3000/dashboard/field-testing](http://localhost:3000/dashboard/field-testing)
- Lead imports: [http://localhost:3000/dashboard/lead-imports](http://localhost:3000/dashboard/lead-imports)
- Field briefing: [http://localhost:3000/dashboard/field-briefing](http://localhost:3000/dashboard/field-briefing)
- AI Gateway: [http://localhost:3000/dashboard/ai](http://localhost:3000/dashboard/ai)
- Worker runtime: [http://localhost:3000/dashboard/worker](http://localhost:3000/dashboard/worker)
- Provider readiness: [http://localhost:3000/dashboard/provider-readiness](http://localhost:3000/dashboard/provider-readiness)
- Call intelligence: [http://localhost:3000/dashboard/call-intelligence](http://localhost:3000/dashboard/call-intelligence)
- Production readiness: [http://localhost:3000/dashboard/production-readiness](http://localhost:3000/dashboard/production-readiness)
- Buyer portal demo: [http://localhost:3000/buyer-portal](http://localhost:3000/buyer-portal)
- Seller portal demo: [http://localhost:3000/seller-portal](http://localhost:3000/seller-portal)
- Backend health: [http://localhost:8000/health](http://localhost:8000/health)

## Validation

Backend:

```powershell
cd backend
..\.venv\Scripts\alembic.exe upgrade head
..\.venv\Scripts\python.exe seed.py
..\.venv\Scripts\python.exe -m pytest
```

Frontend:

```powershell
cd frontend
npm test
npm run build
npm audit --omit=dev
```

Useful source sweeps:

```powershell
Get-ChildItem -Recurse -File -Include *.py,*.ts,*.tsx,*.mjs,*.md backend,frontend\src,frontend\tests,docs,README.md |
  Select-String -Pattern ("Wholesale" + " Prime") -CaseSensitive:$false

Get-ChildItem -Recurse -File -Include *.py,*.ts,*.tsx backend,frontend\src |
  Select-String -Pattern "Send All|Blast|Auto Call|Execute Contract|Submit to Title|Guarantee Profit|Legal Advice|Publish Automatically|execute contract|submit to title|buyer blast|bulk send|guaranteed profit|legal advice" -CaseSensitive:$false
```

No legacy overseer/product wording should remain in runtime source. The product/system identity is `Prime 2 Wholesale Deal OS`, and the overseer identity is `Prime 2`.

## Production Readiness

The app is local-first. Hosted production use requires:

- Private operator authentication
- Environment-specific configuration
- Secrets stored outside the repository
- Postgres or another managed database via `DATABASE_URL`
- Alembic migrations run before app startup
- Backup/export plan
- Sanitized audit export review
- Provider sandbox readiness before any provider action
- Owner approval gates left enabled
- Legal/title review handled externally by qualified professionals

Production readiness pages exist in the app, but missing auth/env/secrets/provider checks intentionally block public production exposure.

## Real-World Boundary

This system supports wholesale real estate operations, but the operator is responsible for following applicable local and state law. Contracts, disclosures, title review, legal questions, and closing coordination must be handled with qualified professionals. Forecasts, assignment fees, ARV, repair estimates, buyer margin, and probability scores are estimates or source-backed internal calculations, not guaranteed profits or guaranteed closings.
