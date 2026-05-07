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
- V20 AI Gateway request allowlist, unsafe response blocking, template enforcement, token/cost tracking, audit logs, and no number overrides
- V21 worker job creation, scheduler execution, retries, idempotency, failed-job logging, heartbeat health, and no live action paths
- V22 provider registry default mock mode, env-only credential checks, masked responses, blocked live readiness, attempt audit records, idempotency, webhook review-only behavior, and unsigned live-like webhook rejection
- V23 call intelligence transcript/manual-note analysis, DNC outreach blocking, compliance escalation, objection extraction, draft-only responses, explainable score deltas, AI Gateway allowlist, deterministic fallback, and worker no-live-action behavior
- V28 mobile operator overview, quick call outcome capture, DNC outreach blocking, offline draft idempotency, quick approval gate blocking, and note safety review
- V29 production cloud readiness fail-closed behavior, masked secret posture, provider flags default off, backup metadata safety, and monitoring health summary
- V30 controlled live provider activation owner approval, dry-run, provider/cloud readiness, unchanged source hash, idempotency, SMS consent/DNC/opt-out, AI safety/cost cap, worker/campaign bypass blocks, and audit logging
- V31 real deal execution batch creation, status transitions, call checklist generation, offer decision calculations, buyer validation gate, contract-ready checklist, assignment-fee evidence validation, field-test report learning signals, execution coach recommendations, and no live/legal/title/payment action paths
- CP1 validation lane `client_command_workspace_cp1`: workspace/member/role tenant isolation, scoped client permissions, sanitized workspace responses, and no client access to internal Prime governance or raw provider payloads
- CP2 validation lane `lead_intelligence_division_cp2`: deterministic lead scoring, missing-data readiness reduction, hot-board ranking, next-action recommendations, and no outbound provider actions
- CP3 validation lane `client_command_acquisition_cp3`: deterministic acquisition briefs, missing-data-driven question plans, manual-use follow-up drafts, appointment readiness blocks, client-safe sanitizer, and no outbound provider actions
- CP4 validation lane `client_command_underwriting_cp4`: evidence packet isolation, missing evidence tracking, ARV/repair blocks, transparent MAO/scenario math, offer readiness gates, no offer/contract execution, and sanitized evidence items

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
- V20/V21 dashboard routes render and expose no live execution controls
- V22 provider readiness dashboard routes render and expose no unsafe live-provider controls
- V23 call intelligence dashboard routes render and expose no live call or send controls
- V28 mobile routes render and expose no unsafe field controls
- V29 cloud readiness routes render and expose no deployment or secret controls
- V30 live activation routes render and expose no bulk or bypass controls
- V31 first deal cockpit routes render and expose no unsafe call/send/contract/title/payment controls
- CP1-CP4 client command routes render and expose no dangerous send/call/provider/billing/contract controls
- CP3/CP4 client command routes render and expose no forbidden send/call/provider/billing/contract/payment controls

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
- `/dashboard/ai`
- `/dashboard/ai/audit`
- `/dashboard/ai/costs`
- `/dashboard/ai/templates`
- `/dashboard/worker`
- `/dashboard/worker/jobs`
- `/dashboard/worker/health`
- `/dashboard/provider-readiness`
- `/dashboard/provider-readiness/attempts`
- `/dashboard/provider-readiness/webhooks`
- `/dashboard/provider-readiness/credentials`
- `/dashboard/call-intelligence`
- `/dashboard/call-intelligence/new`
- `/dashboard/call-intelligence/objections`
- `/dashboard/call-intelligence/follow-ups`
- `/dashboard/call-intelligence/quality`
- `/dashboard/market-enrichment`
- `/dashboard/comps`
- `/dashboard/rent-estimates`
- `/dashboard/buyer-activity`
- `/dashboard/lead-source-roi`
- `/dashboard/market-ranking`
- `/dashboard/prime-memory`
- `/dashboard/learning-signals`
- `/dashboard/scoring-weight-recommendations`
- `/dashboard/playbook-recommendations`
- `/dashboard/production-readiness`
- `/dashboard/backups`
- `/mobile`
- `/mobile/today`
- `/mobile/calls`
- `/mobile/leads/lead-001`
- `/mobile/deals/deal-001`
- `/mobile/approvals`
- `/mobile/briefing`
- `/mobile/notes`
- `/mobile/buyers`
- `/mobile/documents`
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
- `/dashboard/client-command`
- `/dashboard/client-command/workspaces`
- `/dashboard/client-command/leads`
- `/dashboard/client-command/hot-leads`
- `/dashboard/client-command/next-actions`
- `/dashboard/client-command/acquisition`
- `/dashboard/client-command/acquisition/briefs`
- `/dashboard/client-command/acquisition/needs-review`
- `/dashboard/client-command/underwriting`
- `/dashboard/client-command/underwriting/ready-review`
- `/dashboard/client-command/underwriting/blocked`
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
- `/api/v1/ai`
- `/api/v1/ai/audit`
- `/api/v1/ai/costs`
- `/api/v1/ai/templates`
- `/api/v1/worker`
- `/api/v1/worker/health`
- `/api/v1/worker/jobs`
- `/api/v1/worker/logs`
- `/api/v1/provider-readiness`
- `/api/v1/provider-readiness/attempts`
- `/api/v1/provider-readiness/webhooks`
- `/api/v1/provider-readiness/credentials`
- `/api/v1/call-intelligence`
- `/api/v1/call-intelligence/objections`
- `/api/v1/call-intelligence/follow-ups`
- `/api/v1/call-intelligence/quality`
- `/api/v1/documents`
- `/api/v1/documents/issues`
- `/api/v1/documents/review-queue`
- `/api/v1/documents/evidence`
- `/api/v1/campaigns`
- `/api/v1/campaigns/segments`
- `/api/v1/campaigns/sequences`
- `/api/v1/campaigns/approvals`
- `/api/v1/campaigns/performance`
- `/api/v1/market-enrichment`
- `/api/v1/market-enrichment/comps`
- `/api/v1/market-enrichment/rent-estimates`
- `/api/v1/market-enrichment/buyer-activity`
- `/api/v1/market-enrichment/lead-source-roi`
- `/api/v1/market-enrichment/ranking`
- `/api/v1/prime-memory`
- `/api/v1/prime-memory/patterns`
- `/api/v1/prime-memory/learning-signals`
- `/api/v1/prime-memory/scoring-weight-recommendations`
- `/api/v1/prime-memory/playbook-recommendations`
- `/api/v1/mobile`
- `/api/v1/mobile/today`
- `/api/v1/mobile/calls`
- `/api/v1/mobile/leads/lead-001`
- `/api/v1/mobile/deals/deal-001`
- `/api/v1/mobile/approvals`
- `/api/v1/mobile/briefing`
- `/api/v1/mobile/buyers`
- `/api/v1/mobile/documents`
- `/api/v1/cloud-readiness/overview`
- `/api/v1/cloud-readiness/env`
- `/api/v1/cloud-readiness/security`
- `/api/v1/cloud-readiness/backups`
- `/api/v1/cloud-readiness/monitoring`
- `/api/v1/live-activation`
- `/api/v1/live-activation/readiness`
- `/api/v1/live-activation/approvals`
- `/api/v1/live-activation/attempts`
- `/api/v1/live-activation/blocked`
- `/api/v1/real-deal-execution`
- `/api/v1/real-deal-execution/calls`
- `/api/v1/real-deal-execution/offers`
- `/api/v1/real-deal-execution/buyer-validation`
- `/api/v1/real-deal-execution/contract-ready`
- `/api/v1/real-deal-execution/evidence`
- `/api/v1/real-deal-execution/report`
- `/api/v1/client-command/workspaces`
- `/api/v1/client-command/workspaces/client-workspace-001`
- `/api/v1/client-command/workspaces/client-workspace-001/leads`
- `/api/v1/client-command/leads`
- `/api/v1/client-command/leads/client-lead-001`
- `/api/v1/client-command/leads/client-lead-001/score`
- `/api/v1/client-command/leads/hot-board`
- `/api/v1/client-command/leads/next-actions`
- `/api/v1/client-command/acquisition/briefs`
- `/api/v1/client-command/acquisition/needs-review`
- `/api/v1/client-command/underwriting/ready-review`
- `/api/v1/client-command/underwriting/blocked`
- `/api/v1/client-command/underwriting/needs-human-review`
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

## V31 First Deal Execution Checklist

Before using the cockpit with a real batch:

- Confirm imported leads were previewed, QA checked, and committed intentionally.
- Confirm the top call queue is guidance-only and does not expose live call, SMS, or email controls.
- Confirm DNC call outcomes block future outreach eligibility.
- Confirm offer decisions use source-backed ARV, repair, buyer-cost, buyer-profit, seller-ask, and target assignment-fee inputs.
- Confirm buyer validation blocks weak margin, weak demand, missing POF, low reliability, and price-below-spread cases.
- Confirm contract-ready remains an internal readiness status for external attorney/title process only.
- Confirm assignment-fee evidence blocks unsupported 10K+ claims and invented seller/buyer numbers.
- Confirm batch reports create advisory learning signals only and do not auto-apply scoring changes.
- Confirm owner approval remains required before any real-world action.

## Production Readiness Gates

Before any hosted deployment:

- Auth checklist must pass.
- Environment variables must be explicit.
- Secrets must be outside the repository.
- Provider sandbox checks must pass before any provider action.
- V22 provider readiness must keep credential values outside the database and expose masked env reference names only.
- Webhook receiver records must create review tasks only and never mutate deals automatically.
- Call intelligence must remain text-only and analysis-only; no audio recording, live calling, automatic seller response, or term changes.
- Document intelligence must remain classification/extraction/review routing only; full text must stay out of external surfaces and no document should trigger contract execution, title delivery, or portal publishing.
- Campaign brain must remain draft/preview/governance-first; DNC and compliance exclusions, owner approval, caps, stop conditions, one-message event modeling, V5/V13/V22 gates, idempotency, and audit must remain required before any controlled live path.
- Market enrichment must remain manual/import-data only; comp, rent, buyer activity, market heat, and lead source ROI outputs must be evidence-backed estimates with no paid API calls, invented ARV, or guaranteed ROI language.
- Prime 2 memory must remain deterministic and source-cited; memory may inform recommendations but cannot invent facts, expose internal strategy to portals, auto-apply scoring changes, override compliance, or create unsupported claims.
- Mobile operator mode must remain field capture and review only; quick approvals cannot bypass dry-run, safety, provider readiness, idempotency, audit, and owner gates.
- Cloud readiness must fail closed for unsafe production posture; it can report masked readiness but cannot deploy the app or activate providers.
- Live provider activation must remain one-action, source-linked, hash-verified, idempotent, audited, owner-approved, provider-ready, and production-ready before any provider lane can proceed.
- Audit exports must be sanitized.
- Backup/export records must be metadata-safe unless a future encrypted storage design is added.
- Legal/title review remains external.
- Contract execution remains external.
- Payment handling remains unavailable.
- Owner approval gates remain enabled.
