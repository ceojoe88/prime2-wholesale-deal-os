# Virtual Wholesale Real Estate Deal OS

Private, operator-only acquisition-to-assignment command center for wholesale real estate deal analysis. This is not a SaaS, public-facing portal, public CRM, live outreach system, legal product, or contract execution tool.

## Overseer Identity

Prime 2 is the executive overseer for the private Virtual Wholesale Real Estate Deal OS and the brother system to Vylarion Prime. Prime 2 is the private wholesale real estate overseer built to identify, control, and accelerate assignment-fee opportunities while preserving owner approval, compliance boundaries, and deal evidence.

Prime 2 oversees seller acquisition, buyer disposition, 10K+ opportunity ranking, buyer margin protection, seller offer reasonableness, manager/agent routing, owner approval escalation, daily operating reports, and unsafe-action blocking. The safety boundary is unchanged: Prime 2 recommends, drafts, scores, routes, escalates, and briefs, but high-risk live actions stay gated behind owner approval and the existing compliance/provider controls.

## What Is Included

- FastAPI backend with SQLAlchemy models, SQLite local database, Alembic migration, and Postgres-ready `DATABASE_URL` support.
- Domain engines for lead scoring, underwriting, MAO, middle-man profit control, buyer matching, compliance checklists, CSV lead import preview, and v1 action blocking.
- Next.js TypeScript dashboard with all requested `/dashboard/*` routes.
- Seed data for 9 divisions, 9 managers, 51 agents, 30 leads, 10 buyers, 8 deals, 5 hot 10K+ opportunities, 2 under-contract examples, 3 compliance-risk examples, and 3 buyer matches.
- Tests for private mode, blocked live actions, legal-language guardrails, agent execution limits, owner approval gates, formulas, buyer matching, seed coverage, API routes, and dashboard route coverage.
- V2 invite-gated buyer deal room with sanitized deal projections, internal publishing gates, and draft-only buyer interest records.
- V3 seller acquisition command center with seller interaction records, draft-only follow-up engine, and offer packet prep gate.
- V4 contract control and title handoff prep with contract-control records, title packet placeholders, assignment readiness gates, and no legal execution or title submission.
- V5 controlled live communication gate with draft records, safety checks, dry-run receipts, owner approvals, mock provider adapters, idempotency, and blocked-attempt audit records.
- V6 invite-gated seller offer review room with sanitized offer status, seller visibility gates, response intake records, and no buyer/profit/internal strategy exposure.
- V7 unified deal room and closing coordination gate connecting seller offer room, buyer deal room, contract control, title handoff, communications, and assignment readiness with blocker tracking and recommendation-only next actions.
- V8 deal evidence and assignment-fee attribution layer tying projected and verified fees to source records, evidence packets, owner review, and unsupported-claim guards.
- V9 buyer demand intelligence and deal distribution prep with buyer demand profiles, per-deal priority rankings, sanitized private deal sheets, one-recipient draft records, POF gap tracking, and no live blasts.
- V10 controlled offer-to-contract conversion gate with offer positioning, negotiation tracking, seller acceptance readiness scoring, contract-ready state gates, and no contract execution.
- V11 title company/attorney review coordination gate with draft-only review records, review packet prep, missing-item queues, and no title submission, title email, legal advice, or contract execution.
- V12 near-autonomous execution engine with automation rules, scheduler runtime, run/attempt ledgers, autonomous agent task queues, event triggers, daily command briefings, escalation queues, and a Prime 2 autonomy panel.
- V13 controlled auto-execution gate with approved rules, approved template library, conditional dry-run/approval/live-flag workflow, single-attempt idempotency, and audit records.

## Safety Boundaries

The system only analyzes, scores, drafts, recommends, escalates, flags risk, and prepares checklists. In v1 it blocks live SMS, live email, calls, buyer contact, buyer blast execution, paid API calls, contract execution, public signup, portals, legal advice language, deceptive language, and guaranteed profit claims.

All real-world action requires owner approval. Assignment packet preparation also requires compliance review.

V2 adds a controlled buyer portal, but the private operator system remains the source of truth. The portal is invite-gated, has no public signup, shows sanitized deal-room data only, records buyer interest as non-binding draft intent, and still blocks blasts, payments, legal advice, and contract execution.

V3 adds seller acquisition control without live outreach. Seller scripts, SMS, email, objection responses, offer explanations, and follow-up sequences are draft-only. Offer packet prep is blocked until underwriting, buyer margin, target assignment fee, compliance guard, and owner approval are all recorded.

V4 moves offer-ready opportunities into contract-control preparation only. Contract prep is blocked unless the offer packet is approved, seller accepted terms are recorded, ARV and repairs exist, buyer margin is protected, assignment spread is calculated, compliance passed, and owner approval is recorded. Title handoff packets are placeholders/checklists only; title-company submission, executable contract generation, live sending, legal advice, false assignment claims, hidden disclosure language, misrepresentation, and automatic contract status changes are blocked.

V5 allows only narrow communication preparation and gated one-off attempts. Live communication is disabled by default by a global flag and per-draft live flag. A draft must pass safety checks, produce a dry-run receipt, remain unchanged after dry-run, have owner approval, have provider readiness, tie its recipient to the source record, and satisfy idempotency before any mock-send can occur. Bulk sends, campaigns, auto follow-up sequences, buyer blasts, title-company submission, legal advice, pressure, fake urgency, fake buyer claims, guaranteed close claims, unsupported claims, and hidden/deceptive assignment language are blocked.

V6 adds an invite-gated seller offer review room. The operator system remains the source of truth, and seller visibility is blocked unless the offer packet is approved, compliance and owner approvals are recorded, contract-control status is valid, offer language passes safety checks, and portal visibility is explicitly enabled. Seller pages show only approved offer status, amount, property summary, timeline estimate, access next step, title review status, and document checklist. Buyer data, assignment fee logic, buyer price, spread strategy, MAO logic, motivation/temperature scores, internal notes, Prime 2 recommendations, compliance internals, and queues are hidden. Seller responses are draft/intake records for operator review only; no acceptance, negotiation automation, contract execution, or file transmission occurs.

V7 adds an internal unified deal room for closing coordination. It connects seller offer room status, buyer deal room status, contract control, title handoff, communications, assignment readiness, compliance, blocker records, projected fees at risk, closing timeline, and owner approval status. This layer is coordination-only: it cannot generate executable contracts, submit to title, handle payments, auto-negotiate, or change real-world status without the owner.

V8 adds proof-backed deal evidence and assignment-fee attribution. Evidence packets collect lead source, seller interaction proof, underwriting snapshot, buyer interest proof, POF status, contract/title status, communication receipts, blocker history, and compliance status. Assignment-fee records calculate the spread from buyer purchase price minus seller contract price and only flag 10K+ opportunities when the source-number formula and evidence gate support it. Fake profit claims, unsupported ROI claims, invented buyer/seller numbers, client-facing proof without approval, legal guarantees, and closing guarantees are blocked.

V9 adds internal buyer demand intelligence and deal distribution prep. Buyers are ranked by area, price fit, POF, reliability, close speed, deal type, and buyer margin strength. Distribution records prepare buyer email drafts, SMS drafts, private deal sheets, call notes, and response trackers only. The deal sheet sanitizer exposes property summary, asking price, ARV range, repair range, buyer margin estimate, access placeholder, availability, and proof/inspection placeholders while hiding seller data, lead source, motivation, assignment fee logic, internal spread strategy, agent recommendations, and compliance internals. Live buyer blasts, bulk sends, misleading scarcity, fake offers, fake competition, seller/private data exposure, legal guarantees, and closing guarantees are blocked.

V10 converts high-confidence seller opportunities into contract-ready internal states only. Offer positioning stores strategy type, seller pain alignment, justification, anchor/walk-away/ideal prices, concession range, and confidence. Negotiation tracking stores seller responses, objections, counteroffers, emotional signals, stage, next move, and acceptance readiness score. Contract-ready means externally draft-ready for attorney/title review, seller likely to sign, numbers locked, and negotiation stabilized; it never creates, executes, or auto-accepts a contract. Legal advice, pressure tactics, fake urgency, fake buyer claims, guaranteed close language, live negotiation automation, and deception about role or assignment are blocked.

V11 prepares title/attorney review coordination for V10 contract-ready deals only. Review records track selected title company placeholders, review status, required documents, missing items, notes, and owner approval. Review packets organize property summary, seller terms, buyer/assignment readiness, timeline, access notes, compliance checklist, and document checklist. Packet prep is blocked unless V10 contract-ready, compliance passed, owner approval recorded, numbers locked, and seller acceptance readiness is high or contract-ready. Legal advice, contract execution, document submission, title-company email sending, attorney-client relationship claims, and closing guarantees are blocked.

V12 adds near-autonomous internal execution. Level 2 allows autonomous internal prep, Level 3 allows autonomous draft creation and scheduling, Level 4 allows only controlled live-action review with owner approval, and Level 5 is disabled. Prime 2 can score leads, refresh deal scores, update queues, create drafts, create evidence packets, create blockers, schedule reminders, escalate urgent deals, mark internal readiness when gates pass, and generate daily briefings. It cannot autonomously send SMS/email, call sellers, contact buyers, execute contracts, submit title packets, collect payments, publish buyer/seller portal data, change terms, give legal advice, or make binding commitments. Scheduler runs and blocked attempts are auditable, and idempotency prevents duplicate task creation.

V13 allows only very narrow controlled automation for approved low-risk repeatable actions. A trigger must match an approved auto-execution rule and approved template, pass safety, create a dry-run receipt, pass owner approval and live-flag checks when applicable, verify provider readiness, enforce one recipient and idempotency, and create an audit record. Allowed actions are internal reminders, operator task creation, approved seller follow-up drafts, approved buyer response drafts, and approved low-risk single-message sends only when V5 gates pass. Bulk campaigns, buyer blasts, cold SMS automation, legal/contract messages, pressure language, fake urgency, fake buyer claims, and actions without an approved rule/template are blocked.

## Backend

```powershell
cd backend
python -m venv ..\.venv
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\.venv\Scripts\python.exe seed.py
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Useful endpoints:

- `GET /health`
- `GET /api/command-center`
- `GET /api/hierarchy`
- `GET /api/leads`
- `GET /api/deals`
- `GET /api/profit-control`
- `GET /api/seller-acquisition`
- `GET /api/seller-acquisition/{lead_id}`
- `POST /api/seller-acquisition/safety/validate`
- `GET /api/follow-up-control`
- `GET /api/offer-packets`
- `GET /api/offer-packets/{packet_id}`
- `POST /api/offer-packets/{packet_id}/prepare`
- `GET /api/contract-control`
- `GET /api/contract-control/{contract_id}`
- `POST /api/contract-control/{contract_id}/prepare`
- `POST /api/contract-control/safety/validate`
- `GET /api/title-handoff`
- `GET /api/title-handoff/{packet_id}`
- `POST /api/title-handoff/{packet_id}/submit` returns a blocked response in V4
- `GET /api/assignment-readiness`
- `GET /api/communications`
- `GET /api/communications/{draft_id}`
- `POST /api/communications/{draft_id}/safety-check`
- `POST /api/communications/{draft_id}/dry-run`
- `POST /api/communications/{draft_id}/approvals`
- `POST /api/communications/{draft_id}/send`
- `GET /api/communications/dry-runs`
- `GET /api/communications/attempts`
- `GET /api/communications/approvals`
- `GET /api/buyer-portal/rules`
- `GET /api/buyer-portal/deals` with `X-Buyer-Invite: demo-buyer-invite`
- `GET /api/buyer-portal/deals/{deal_id}` with `X-Buyer-Invite: demo-buyer-invite`
- `POST /api/buyer-portal/deals/{deal_id}/interest` with `X-Buyer-Invite: demo-buyer-invite`
- `GET /api/buyer-portal/internal-dashboard`
- `GET /api/seller-portal/rules`
- `GET /api/seller-portal/offer` with `X-Seller-Invite: demo-seller-invite`
- `GET /api/seller-portal/offers/{offer_id}` with `X-Seller-Invite: demo-seller-invite`
- `POST /api/seller-portal/responses` with `X-Seller-Invite: demo-seller-invite`
- `POST /api/seller-portal/offers/{offer_id}/accept` returns a blocked response in V6
- `GET /api/seller-portal/internal-dashboard`
- `GET /api/deal-room`
- `GET /api/deal-room/{deal_room_id}`
- `GET /api/closing-coordination`
- `GET /api/closing-coordination/blockers`
- `GET /api/closing-coordination/readiness`
- `GET /api/deal-evidence`
- `GET /api/deal-evidence/{packet_id}`
- `POST /api/deal-evidence/safety/validate`
- `GET /api/assignment-fees`
- `GET /api/assignment-fees/{fee_id}`
- `GET /api/buyer-demand`
- `GET /api/buyer-demand/{buyer_id}`
- `GET /api/buyer-priority`
- `GET /api/deal-distribution`
- `GET /api/deal-distribution/{distribution_id}`
- `POST /api/deal-distribution/safety/validate`
- `GET /api/offer-conversion`
- `GET /api/offer-conversion/{deal_id}`
- `POST /api/offer-conversion/safety/validate`
- `GET /api/negotiations`
- `GET /api/negotiations/{record_id}`
- `GET /api/contract-ready`
- `GET /api/title-review`
- `GET /api/title-review/{review_id}`
- `POST /api/title-review/safety/validate`
- `GET /api/review-packets`
- `GET /api/review-packets/{packet_id}`
- `GET /api/autonomy`
- `GET /api/autonomy/rules`
- `GET /api/autonomy/runs`
- `GET /api/autonomy/tasks`
- `GET /api/autonomy/daily-briefing`
- `GET /api/autonomy/escalations`
- `POST /api/autonomy/safety/validate`
- `POST /api/autonomy/run`
- `GET /api/auto-execution`
- `GET /api/auto-execution/rules`
- `GET /api/auto-execution/templates`
- `GET /api/auto-execution/dry-runs`
- `GET /api/auto-execution/attempts`
- `GET /api/auto-execution/audit`
- `POST /api/auto-execution/execute`
- `GET /api/compliance`
- `POST /api/actions/validate`
- `POST /api/data-import/leads/preview`

Alembic:

```powershell
cd backend
..\.venv\Scripts\alembic.exe upgrade head
```

For Postgres, set `DATABASE_URL` before running migrations or the app.

## Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000/dashboard](http://localhost:3000/dashboard).

Buyer portal demo:

- [http://localhost:3000/buyer-portal](http://localhost:3000/buyer-portal)
- [http://localhost:3000/buyer-portal/deals](http://localhost:3000/buyer-portal/deals)
- [http://localhost:3000/buyer-portal/profile](http://localhost:3000/buyer-portal/profile)

Seller acquisition V3 routes:

- [http://localhost:3000/dashboard/seller-acquisition](http://localhost:3000/dashboard/seller-acquisition)
- [http://localhost:3000/dashboard/follow-up-control](http://localhost:3000/dashboard/follow-up-control)
- [http://localhost:3000/dashboard/offer-packets](http://localhost:3000/dashboard/offer-packets)

Contract/title V4 routes:

- [http://localhost:3000/dashboard/contract-control](http://localhost:3000/dashboard/contract-control)
- [http://localhost:3000/dashboard/title-handoff](http://localhost:3000/dashboard/title-handoff)
- [http://localhost:3000/dashboard/assignment-readiness](http://localhost:3000/dashboard/assignment-readiness)

Communication V5 routes:

- [http://localhost:3000/dashboard/communications](http://localhost:3000/dashboard/communications)
- [http://localhost:3000/dashboard/communications/dry-runs](http://localhost:3000/dashboard/communications/dry-runs)
- [http://localhost:3000/dashboard/communications/attempts](http://localhost:3000/dashboard/communications/attempts)
- [http://localhost:3000/dashboard/communications/approvals](http://localhost:3000/dashboard/communications/approvals)

Seller portal V6 routes:

- [http://localhost:3000/seller-portal](http://localhost:3000/seller-portal)
- [http://localhost:3000/seller-portal/offer](http://localhost:3000/seller-portal/offer)
- [http://localhost:3000/seller-portal/property](http://localhost:3000/seller-portal/property)
- [http://localhost:3000/seller-portal/timeline](http://localhost:3000/seller-portal/timeline)
- [http://localhost:3000/seller-portal/documents](http://localhost:3000/seller-portal/documents)
- [http://localhost:3000/seller-portal/messages](http://localhost:3000/seller-portal/messages)

Unified deal room V7 routes:

- [http://localhost:3000/dashboard/deal-room](http://localhost:3000/dashboard/deal-room)
- [http://localhost:3000/dashboard/closing-coordination](http://localhost:3000/dashboard/closing-coordination)
- [http://localhost:3000/dashboard/closing-coordination/blockers](http://localhost:3000/dashboard/closing-coordination/blockers)
- [http://localhost:3000/dashboard/closing-coordination/readiness](http://localhost:3000/dashboard/closing-coordination/readiness)

Evidence/attribution V8 routes:

- [http://localhost:3000/dashboard/deal-evidence](http://localhost:3000/dashboard/deal-evidence)
- [http://localhost:3000/dashboard/assignment-fees](http://localhost:3000/dashboard/assignment-fees)

Buyer demand/distribution V9 routes:

- [http://localhost:3000/dashboard/buyer-demand](http://localhost:3000/dashboard/buyer-demand)
- [http://localhost:3000/dashboard/buyer-priority](http://localhost:3000/dashboard/buyer-priority)
- [http://localhost:3000/dashboard/deal-distribution](http://localhost:3000/dashboard/deal-distribution)

Offer conversion V10 routes:

- [http://localhost:3000/dashboard/offer-conversion](http://localhost:3000/dashboard/offer-conversion)
- [http://localhost:3000/dashboard/negotiations](http://localhost:3000/dashboard/negotiations)
- [http://localhost:3000/dashboard/contract-ready](http://localhost:3000/dashboard/contract-ready)

Title/attorney review V11 routes:

- [http://localhost:3000/dashboard/title-review](http://localhost:3000/dashboard/title-review)
- [http://localhost:3000/dashboard/review-packets](http://localhost:3000/dashboard/review-packets)

Near-autonomous execution V12 routes:

- [http://localhost:3000/dashboard/autonomy](http://localhost:3000/dashboard/autonomy)
- [http://localhost:3000/dashboard/autonomy/rules](http://localhost:3000/dashboard/autonomy/rules)
- [http://localhost:3000/dashboard/autonomy/runs](http://localhost:3000/dashboard/autonomy/runs)
- [http://localhost:3000/dashboard/autonomy/tasks](http://localhost:3000/dashboard/autonomy/tasks)
- [http://localhost:3000/dashboard/autonomy/daily-briefing](http://localhost:3000/dashboard/autonomy/daily-briefing)
- [http://localhost:3000/dashboard/autonomy/escalations](http://localhost:3000/dashboard/autonomy/escalations)

Controlled auto-execution V13 routes:

- [http://localhost:3000/dashboard/auto-execution](http://localhost:3000/dashboard/auto-execution)
- [http://localhost:3000/dashboard/auto-execution/rules](http://localhost:3000/dashboard/auto-execution/rules)
- [http://localhost:3000/dashboard/auto-execution/templates](http://localhost:3000/dashboard/auto-execution/templates)
- [http://localhost:3000/dashboard/auto-execution/dry-runs](http://localhost:3000/dashboard/auto-execution/dry-runs)
- [http://localhost:3000/dashboard/auto-execution/attempts](http://localhost:3000/dashboard/auto-execution/attempts)
- [http://localhost:3000/dashboard/auto-execution/audit](http://localhost:3000/dashboard/auto-execution/audit)

Buyer acceleration V14 routes:

- [http://localhost:3000/dashboard/buyer-acceleration](http://localhost:3000/dashboard/buyer-acceleration)
- [http://localhost:3000/dashboard/buyer-sequences](http://localhost:3000/dashboard/buyer-sequences)
- [http://localhost:3000/dashboard/buyer-response-router](http://localhost:3000/dashboard/buyer-response-router)
- [http://localhost:3000/dashboard/buyer-velocity](http://localhost:3000/dashboard/buyer-velocity)

Optimization learning V15 routes:

- [http://localhost:3000/dashboard/optimization](http://localhost:3000/dashboard/optimization)
- [http://localhost:3000/dashboard/optimization/patterns](http://localhost:3000/dashboard/optimization/patterns)
- [http://localhost:3000/dashboard/optimization/recommendations](http://localhost:3000/dashboard/optimization/recommendations)
- [http://localhost:3000/dashboard/optimization/agent-performance](http://localhost:3000/dashboard/optimization/agent-performance)
- [http://localhost:3000/dashboard/optimization/lost-deals](http://localhost:3000/dashboard/optimization/lost-deals)
- [http://localhost:3000/dashboard/optimization/source-quality](http://localhost:3000/dashboard/optimization/source-quality)

Revenue forecast/scaling V16 routes:

- [http://localhost:3000/dashboard/revenue-forecast](http://localhost:3000/dashboard/revenue-forecast)
- [http://localhost:3000/dashboard/market-scaling](http://localhost:3000/dashboard/market-scaling)
- [http://localhost:3000/dashboard/lead-spend-planner](http://localhost:3000/dashboard/lead-spend-planner)
- [http://localhost:3000/dashboard/pipeline-value](http://localhost:3000/dashboard/pipeline-value)

Semi-autonomous operator mode V17 routes:

- [http://localhost:3000/dashboard/operator-mode](http://localhost:3000/dashboard/operator-mode)
- [http://localhost:3000/dashboard/operator-mode/approvals](http://localhost:3000/dashboard/operator-mode/approvals)
- [http://localhost:3000/dashboard/operator-mode/exceptions](http://localhost:3000/dashboard/operator-mode/exceptions)
- [http://localhost:3000/dashboard/operator-mode/daily-report](http://localhost:3000/dashboard/operator-mode/daily-report)
- [http://localhost:3000/dashboard/operator-mode/system-trust](http://localhost:3000/dashboard/operator-mode/system-trust)
- [http://localhost:3000/dashboard/operator-mode/settings](http://localhost:3000/dashboard/operator-mode/settings)

Production readiness/audit export V18 routes:

- [http://localhost:3000/dashboard/production-readiness](http://localhost:3000/dashboard/production-readiness)
- [http://localhost:3000/dashboard/audit-exports](http://localhost:3000/dashboard/audit-exports)
- [http://localhost:3000/dashboard/evidence-attachments](http://localhost:3000/dashboard/evidence-attachments)
- [http://localhost:3000/dashboard/provider-readiness](http://localhost:3000/dashboard/provider-readiness)
- [http://localhost:3000/dashboard/backups](http://localhost:3000/dashboard/backups)

## Validation

```powershell
cd backend
..\.venv\Scripts\python.exe seed.py
..\.venv\Scripts\python.exe -m pytest

cd ..\frontend
npm test
npm run build
```

## Documentation

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the domain architecture, guardrails, and route map.
