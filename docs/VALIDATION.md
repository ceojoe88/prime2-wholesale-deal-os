# Validation Checklist

Use this checklist before trusting a change, cutting a release, or moving the project toward a hosted environment.

## Backend

From the repository root:

```powershell
cd backend
..\.venv\Scripts\alembic.exe upgrade head
..\.venv\Scripts\python.exe seed.py
..\.venv\Scripts\python.exe -m pytest
```

For an isolated SQLite validation database:

```powershell
cd backend
$env:DATABASE_URL = "sqlite:///./wholesale_os_validation.db"
..\.venv\Scripts\alembic.exe upgrade head
..\.venv\Scripts\python.exe seed.py
..\.venv\Scripts\python.exe -m pytest
```

Expected coverage includes:

- API route registration
- Domain module imports
- Alembic migration compatibility
- Seed/model alignment
- Lead scoring and MAO formulas
- Middle-man profit formulas
- Buyer margin protection
- Portal sanitizers
- Seller safety language
- Communication gates
- Auto-execution gates
- Autonomy and operator-mode hard boundaries
- Evidence and forecast source requirements
- Production readiness and audit export sanitizers
- V19 CSV import preview, approved-row commit, dedupe, lead QA, call outcomes, do-not-contact blocking, field feedback, and scoring adjustment guardrails

## Frontend

```powershell
cd frontend
npm test
npm run build
npm audit --omit=dev
```

Expected coverage includes:

- Dashboard and portal route files exist
- Dynamic detail routes guard missing IDs with `notFound()`
- Navigation targets implemented pages
- Buyer and seller portal routes avoid internal/profit/seller/buyer data leaks
- Prime 2 identity appears on internal operator routes
- Old overseer naming remains limited to the product title
- V19 dashboard routes render and do not expose unsafe live-action buttons

## Source Sweeps

Old overseer or product naming:

```powershell
Get-ChildItem -Recurse -File -Include *.py,*.ts,*.tsx,*.mjs,*.md backend,frontend\src,frontend\tests,docs,README.md |
  Select-String -Pattern ("Wholesale" + " Prime") -CaseSensitive:$false
```

Expected result: no legacy overseer/product wording in runtime source. Tests and docs should avoid storing the old phrase as a literal.

Potential unsafe language and action references:

```powershell
Get-ChildItem -Recurse -File -Include *.py,*.ts,*.tsx backend,frontend\src |
  Select-String -Pattern "Send All|Blast|Auto Call|Execute Contract|Submit to Title|Guarantee Profit|Legal Advice|Publish Automatically|execute contract|submit to title|buyer blast|bulk send|guaranteed profit|guaranteed close|legal advice|must sign|last chance|buyers lined up|payment" -CaseSensitive:$false
```

Expected result: matches should be guardrail constants, blocked examples, false/disabled flags, test cases, or safety copy. They should not expose executable buttons, uncontrolled live action paths, or provider secrets.

## Route Smoke

When the frontend is running:

```powershell
cd frontend
npm run dev
```

Smoke check:

- `/dashboard`
- `/dashboard/command-center`
- `/dashboard/overseer`
- `/dashboard/command-hierarchy`
- `/dashboard/autonomy`
- `/dashboard/auto-execution`
- `/dashboard/buyer-acceleration`
- `/dashboard/optimization`
- `/dashboard/revenue-forecast`
- `/dashboard/operator-mode`
- `/dashboard/field-testing`
- `/dashboard/lead-imports`
- `/dashboard/lead-qa`
- `/dashboard/call-outcomes`
- `/dashboard/feedback-loop`
- `/dashboard/scoring-adjustments`
- `/dashboard/field-briefing`
- `/dashboard/production-readiness`
- `/dashboard/backups`
- `/buyer-portal`
- `/seller-portal`

When the backend is running:

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Smoke check:

- `/health`
- `/api/system/rules`
- `/api/command-center`
- `/api/hierarchy`
- `/api/autonomy`
- `/api/operator-mode`
- `/api/lead-imports`
- `/api/lead-qa`
- `/api/call-outcomes`
- `/api/field-testing`
- `/api/field-briefing`
- `/api/feedback-loop`
- `/api/scoring-adjustments`
- `/api/production-readiness`

## V19 Field Testing Checklist

Before using real lead data:

- Confirm CSV rows preview successfully before commit.
- Confirm bad rows remain visible with `blocked_reasons`.
- Confirm rows with no property address cannot commit.
- Confirm duplicate property plus owner phone rows are blocked.
- Confirm committed rows do not trigger SMS, email, calls, portal publishing, or automation sends.
- Confirm do-not-contact call outcomes block future live outreach eligibility.
- Confirm prediction feedback produces deterministic, explainable scoring suggestions.
- Confirm owner review remains required before applying scoring adjustments or taking field action.

## Production Readiness Gates

Before any hosted deployment:

- Auth checklist must pass.
- Environment variables must be explicit.
- Secrets must be outside the repository.
- Provider sandbox checks must pass before any provider action.
- Audit exports must be sanitized.
- Backup/export records must be metadata-safe unless a future encrypted storage design is added.
- Legal/title review remains external.
- Contract execution remains external.
- Payment handling remains unavailable.
- Owner approval gates remain enabled.
