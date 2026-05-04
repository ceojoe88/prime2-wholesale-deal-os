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

## Safety Boundaries

The system only analyzes, scores, drafts, recommends, escalates, flags risk, and prepares checklists. In v1 it blocks live SMS, live email, calls, buyer contact, buyer blast execution, paid API calls, contract execution, public signup, portals, legal advice language, deceptive language, and guaranteed profit claims.

All real-world action requires owner approval. Assignment packet preparation also requires compliance review.

V2 adds a controlled buyer portal, but the private operator system remains the source of truth. The portal is invite-gated, has no public signup, shows sanitized deal-room data only, records buyer interest as non-binding draft intent, and still blocks blasts, payments, legal advice, and contract execution.

V3 adds seller acquisition control without live outreach. Seller scripts, SMS, email, objection responses, offer explanations, and follow-up sequences are draft-only. Offer packet prep is blocked until underwriting, buyer margin, target assignment fee, compliance guard, and owner approval are all recorded.

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
- `GET /api/buyer-portal/rules`
- `GET /api/buyer-portal/deals` with `X-Buyer-Invite: demo-buyer-invite`
- `GET /api/buyer-portal/deals/{deal_id}` with `X-Buyer-Invite: demo-buyer-invite`
- `POST /api/buyer-portal/deals/{deal_id}/interest` with `X-Buyer-Invite: demo-buyer-invite`
- `GET /api/buyer-portal/internal-dashboard`
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
