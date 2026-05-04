# Virtual Wholesale Real Estate Deal OS

Private, operator-only acquisition-to-assignment command center for wholesale real estate deal analysis. This is not a SaaS, portal, public CRM, live outreach system, legal product, or contract execution tool.

## What Is Included

- FastAPI backend with SQLAlchemy models, SQLite local database, Alembic migration, and Postgres-ready `DATABASE_URL` support.
- Domain engines for lead scoring, underwriting, MAO, middle-man profit control, buyer matching, compliance checklists, CSV lead import preview, and v1 action blocking.
- Next.js TypeScript dashboard with all requested `/dashboard/*` routes.
- Seed data for 9 divisions, 9 managers, 51 agents, 30 leads, 10 buyers, 8 deals, 5 hot 10K+ opportunities, 2 under-contract examples, 3 compliance-risk examples, and 3 buyer matches.
- Tests for private mode, blocked live actions, legal-language guardrails, agent execution limits, owner approval gates, formulas, buyer matching, seed coverage, API routes, and dashboard route coverage.

## Safety Boundaries

The system only analyzes, scores, drafts, recommends, escalates, flags risk, and prepares checklists. In v1 it blocks live SMS, live email, calls, buyer contact, buyer blast execution, paid API calls, contract execution, public signup, portals, legal advice language, deceptive language, and guaranteed profit claims.

All real-world action requires owner approval. Assignment packet preparation also requires compliance review.

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
