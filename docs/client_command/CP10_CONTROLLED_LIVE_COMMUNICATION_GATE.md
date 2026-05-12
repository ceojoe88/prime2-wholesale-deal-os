# CP10 Controlled Live Communication Gate

CP10 adds the controlled live communication gate for Prime2 Client Command OS.

What it does:
- gates live communication to source-linked records only
- requires draft review before any live attempt
- requires dry-run verification, unchanged content, owner approval, provider readiness, idempotency, and audit
- records blocked attempts when any requirement fails
- keeps providers in mock or blocked posture until every gate clears

What it does not do:
- no bulk campaigns
- no buyer blasts or seller blasts
- no autonomous execution
- no source-less messaging
- no exposure of Prime governance internals to client-facing surfaces

Default posture:
- live communication is blocked by default
- draft and review remain the normal path
- blocked review is safer than fallback send behavior

Memphis demo state:
- provider profile `client-comm-provider-memphis-email` runs in `mock`
- lead 1 is blocked by live flags even with dry run and approval present
- lead 2 is blocked by missing consent, failed message-risk review, missing approval artifacts, and disabled live flags
- buyer outreach for Memphis lead 5 stays blocked by missing approval and live flags
- all send attempts remain blocked and audited with `no_live_send=true`

Implemented backend routes:
- `GET/POST /api/v1/client-command/communication/providers`
- `POST /api/v1/client-command/communication/readiness-check`
- `GET /api/v1/client-command/communication/readiness-checks`
- `POST /api/v1/client-command/communication/dry-run`
- `GET /api/v1/client-command/communication/dry-runs`
- `POST /api/v1/client-command/communication/send-approval`
- `GET /api/v1/client-command/communication/send-approvals`
- `POST /api/v1/client-command/communication/send-attempt`
- `GET /api/v1/client-command/communication/send-attempts`
- `GET /api/v1/client-command/communication/external-references`
- `GET /api/v1/client-command/communication/overview`

Visible boundary text:
- one recipient only
- source linkage required
- owner approval required
- no bulk campaigns
- no autonomous sends
