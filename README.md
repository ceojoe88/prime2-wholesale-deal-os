# Wholesale Prime Deal OS

Private, operator-only virtual wholesale real estate command system with an executive overseer named **Prime 2**. Prime 2 is the brother system to Vylarion Prime and is purpose-built to help a single owner identify, underwrite, control, coordinate, and assign wholesale real estate opportunities while preserving owner approval, compliance boundaries, buyer margin, seller offer reasonableness, and evidence-backed profit attribution.

This repository is not a SaaS product, public CRM, buyer/seller marketplace, legal platform, contract execution system, payment product, skip-tracing service, or live outreach campaign tool.

## Why This Project Exists

Wholesale deal flow can become messy fast: lead sources, seller motivation, ARV inputs, repairs, MAO, assignment spread, buyer demand, proof of funds, title readiness, compliance flags, follow-up timing, and owner approvals all compete for attention. Wholesale Prime Deal OS gives the owner a governed internal operating layer for those decisions.

The useful outcome is speed with guardrails:

- Find and rank motivated seller leads.
- Underwrite deals with explicit ARV, repairs, buyer costs, MAO, max seller offer, and target assignment fee math.
- Protect buyer margin and seller offer reasonableness.
- Identify 10K+ assignment-fee opportunities from source records.
- Prepare seller and buyer communications as drafts.
- Coordinate controlled buyer/seller portal views without leaking internal strategy.
- Keep legal, title, payment, live outreach, and high-risk actions gated.

## Prime 2 Identity

Prime 2 is the executive overseer for the private Virtual Wholesale Real Estate Deal OS and the brother system to Vylarion Prime.

Prime 2 oversees seller acquisition, buyer disposition, 10K+ opportunity ranking, buyer margin protection, seller offer reasonableness, manager/agent routing, owner approval escalation, daily operating reports, and unsafe-action blocking. Prime 2 recommends, drafts, scores, routes, escalates, and briefs. It does not bypass owner approval or execute high-risk real-world actions.

## Current System Status

Implemented phases:

- V1 private operator-only Wholesale Prime Deal OS
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
- Prime 2 overseer rebrand

## Core Capabilities

Backend:

- FastAPI API with SQLAlchemy models
- Alembic migrations
- SQLite for local use and Postgres-ready `DATABASE_URL`
- Seed/demo data for divisions, managers, agents, leads, buyers, deals, portals, evidence, forecasts, automation, audit exports, and production readiness
- Deterministic domain modules for scoring, underwriting, profit control, portals, communication gates, automation, optimization, forecasting, and readiness checks
- Tests for safety gates, formulas, route coverage, portal sanitizers, automation blocks, evidence attribution, production readiness, and seed integrity

Frontend:

- Next.js and TypeScript dashboard
- Premium dark internal command UI
- `/dashboard/*` command surfaces for the operator
- Invite/gated buyer portal routes under `/buyer-portal`
- Invite/gated seller portal routes under `/seller-portal`
- Detail pages guard missing IDs with `notFound()`
- Portal pages avoid seller/internal/profit logic leakage

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
  Select-String -Pattern "Wholesale Prime" -CaseSensitive:$false

Get-ChildItem -Recurse -File -Include *.py,*.ts,*.tsx backend,frontend\src |
  Select-String -Pattern "execute contract|submit to title|buyer blast|bulk send|guaranteed profit|legal advice" -CaseSensitive:$false
```

The only intended product/identity use of `Wholesale Prime` is the product title `Wholesale Prime Deal OS`; validation docs and tests may also contain the literal search term.

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
