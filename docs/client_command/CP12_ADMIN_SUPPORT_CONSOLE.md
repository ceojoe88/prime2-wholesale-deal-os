# CP12 Admin Support Console

CP12 adds the admin support console for Prime2 Client Command OS.

Purpose:
- let internal support review workspace health
- inspect plan, billing, communication, and pilot posture
- coordinate support notes, escalation, and owner review
- keep support actions bounded by the same operating gates as the product

Support console defaults:
- internal-only
- read-heavy by default
- non-live by default
- non-autonomous by default

Seeded Memphis support state:
- 3 open support tickets are present for onboarding, compliance, and buyer-demand follow-up
- 1 queued support action routes the missing-consent path to compliance review
- 1 open escalation tracks the blocked communication gate on Memphis lead 2
- admin-console aggregation shows active pilot program, enrollment, support workload, and blocked health-snapshot visibility

Implemented backend routes:
- `GET/POST /api/v1/client-command/workspaces/{workspace_id}/pilot/support-tickets`
- `GET/POST /api/v1/client-command/pilot/support-actions`
- `GET/POST /api/v1/client-command/pilot/escalations`
- `GET /api/v1/client-command/pilot/admin-console`
- `GET /api/v1/client-command/pilot/support-console`
- `GET /api/v1/client-command/pilot/blocked`
- `GET /api/v1/client-command/pilot/needs-review`

What the support console does not do:
- no bulk campaigns
- no autonomous execution
- no direct message send bypass
- no billing bypass
- no source-gate bypass
- no raw card data display or storage
- no client exposure to Prime governance internals

Support rule:
The admin support console may review, annotate, pause, escalate, and request approval. It cannot create a live action that the source system and its gates would block.
