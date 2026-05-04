# Virtual Wholesale Real Estate Deal OS

Private, operator-only acquisition-to-assignment command center for wholesale real estate deal analysis. This is not a SaaS, public-facing portal, public CRM, live outreach system, legal product, or contract execution tool.

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

## Safety Boundaries

The system only analyzes, scores, drafts, recommends, escalates, flags risk, and prepares checklists. In v1 it blocks live SMS, live email, calls, buyer contact, buyer blast execution, paid API calls, contract execution, public signup, portals, legal advice language, deceptive language, and guaranteed profit claims.

All real-world action requires owner approval. Assignment packet preparation also requires compliance review.

V2 adds a controlled buyer portal, but the private operator system remains the source of truth. The portal is invite-gated, has no public signup, shows sanitized deal-room data only, records buyer interest as non-binding draft intent, and still blocks blasts, payments, legal advice, and contract execution.

V3 adds seller acquisition control without live outreach. Seller scripts, SMS, email, objection responses, offer explanations, and follow-up sequences are draft-only. Offer packet prep is blocked until underwriting, buyer margin, target assignment fee, compliance guard, and owner approval are all recorded.

V4 moves offer-ready opportunities into contract-control preparation only. Contract prep is blocked unless the offer packet is approved, seller accepted terms are recorded, ARV and repairs exist, buyer margin is protected, assignment spread is calculated, compliance passed, and owner approval is recorded. Title handoff packets are placeholders/checklists only; title-company submission, executable contract generation, live sending, legal advice, false assignment claims, hidden disclosure language, misrepresentation, and automatic contract status changes are blocked.

V5 allows only narrow communication preparation and gated one-off attempts. Live communication is disabled by default by a global flag and per-draft live flag. A draft must pass safety checks, produce a dry-run receipt, remain unchanged after dry-run, have owner approval, have provider readiness, tie its recipient to the source record, and satisfy idempotency before any mock-send can occur. Bulk sends, campaigns, auto follow-up sequences, buyer blasts, title-company submission, legal advice, pressure, fake urgency, fake buyer claims, guaranteed close claims, unsupported claims, and hidden/deceptive assignment language are blocked.

V6 adds an invite-gated seller offer review room. The operator system remains the source of truth, and seller visibility is blocked unless the offer packet is approved, compliance and owner approvals are recorded, contract-control status is valid, offer language passes safety checks, and portal visibility is explicitly enabled. Seller pages show only approved offer status, amount, property summary, timeline estimate, access next step, title review status, and document checklist. Buyer data, assignment fee logic, buyer price, spread strategy, MAO logic, motivation/temperature scores, internal notes, Wholesale Prime recommendations, compliance internals, and queues are hidden. Seller responses are draft/intake records for operator review only; no acceptance, negotiation automation, contract execution, or file transmission occurs.

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

## Validation

```powershell
cd backend
..\.venv\Scripts\python.exe -m pytest

cd ..\frontend
npm test
npm run build
```

## Documentation

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the domain architecture, guardrails, and route map.
