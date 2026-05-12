# CP11 Stripe Billing Live Payment Gate

CP11 adds the Stripe billing live payment gate for Prime2 Client Command OS.

Recommended billing shape:
- Stripe Billing APIs manage the subscription lifecycle
- Stripe Prices define plan amounts and intervals
- Stripe Checkout Sessions in subscription mode handle initial live billing
- Stripe Customer Portal handles payment-method and subscription self-service

What CP11 stores:
- Stripe customer IDs
- Stripe subscription IDs
- Stripe price IDs
- masked billing metadata that is safe for support review

What CP11 never stores:
- raw card number
- CVC
- full expiration data
- magnetic-stripe or equivalent raw card data

What it does not do:
- no deal earnest money, purchase funds, or closing payments
- no billing-triggered bulk campaigns
- no autonomous execution
- no provider-payload exposure to clients
- no Prime governance internals exposed to client-facing billing surfaces

Default posture:
- billing is off by default
- plan assignment can exist without live payment collection
- a billing-ready state does not unlock communication or pilot actions by itself

Memphis demo state:
- billing provider `client-billing-provider-memphis` remains in `mock`
- customer profile `client-billing-customer-memphis` stores no raw card data
- readiness check `client-billing-check-memphis` is blocked by billing readiness, plan gate, and live flags
- checkout dry run exists, but the billing attempt and ledger entry stay blocked before any payment action

Implemented backend routes:
- `GET/POST /api/v1/client-command/billing/providers`
- `GET/POST /api/v1/client-command/billing/customer-profiles`
- `POST /api/v1/client-command/billing/readiness-check`
- `GET /api/v1/client-command/billing/readiness-checks`
- `POST /api/v1/client-command/billing/checkout-dry-run`
- `GET /api/v1/client-command/billing/checkout-dry-runs`
- `POST /api/v1/client-command/billing/approval`
- `GET /api/v1/client-command/billing/approvals`
- `POST /api/v1/client-command/billing/attempt`
- `GET /api/v1/client-command/billing/attempts`
- `GET /api/v1/client-command/billing/external-references`
- `GET /api/v1/client-command/billing/ledger`
- `GET /api/v1/client-command/billing/overview`

Billing rule:
CP11 may support future subscription billing only through Stripe-hosted or tokenized flows. Raw card data never enters Prime2 application storage, logs, seed data, or client-safe surfaces.
