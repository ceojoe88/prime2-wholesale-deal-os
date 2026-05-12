# CP9 Subscription Plan Gating Readiness

CP9 adds subscription-plan gating readiness for Prime2 Client Command OS.

Purpose:
- define the workspace plan posture before any live billing exists
- record client-safe entitlement readiness
- prepare billing contacts and approval state
- keep communication, billing, and pilot rollout subordinate to explicit gates
- recalculate workspace usage and seat counts against plan limits

CP9 is non-live by default:
- no Stripe checkout session is created
- no charge, invoice, refund, or payout occurs
- no live communication lane is unlocked
- no bulk campaigns are unlocked
- no autonomous execution is unlocked

Core records:
- subscription plan catalog
- plan feature matrix
- plan limits
- workspace plan assignment
- feature-gate evaluations
- usage counters and seat usage
- entitlement summary
- billing-readiness records
- subscription placeholders
- billing contact readiness
- upgrade or downgrade review notes
- plan gating events

Memphis demo state:
- `client-workspace-003` is assigned to `pro`
- `billing` and `admin_support` remain `blocked_by_plan` until `command`
- upgrade guidance points Memphis from `pro` to `command`
- usage recalculates to 5 leads, 4 buyers, 1 user, 1 weekly report, and 6 manual drafts

Implemented backend routes:
- `GET/POST /api/v1/client-command/plans/catalog`
- `GET /api/v1/client-command/plans/features`
- `GET /api/v1/client-command/plans/limits`
- `GET /api/v1/client-command/plans/overview`
- `GET/POST /api/v1/client-command/workspaces/{workspace_id}/plan-assignment`
- `GET /api/v1/client-command/workspaces/{workspace_id}/feature-gates`
- `POST /api/v1/client-command/workspaces/{workspace_id}/feature-gates/evaluate`
- `GET /api/v1/client-command/workspaces/{workspace_id}/usage`
- `POST /api/v1/client-command/workspaces/{workspace_id}/usage/recalculate`
- `GET /api/v1/client-command/workspaces/{workspace_id}/upgrade-recommendations`
- `GET/POST /api/v1/client-command/workspaces/{workspace_id}/billing-readiness`
- `GET/POST /api/v1/client-command/workspaces/{workspace_id}/subscription-placeholder`

Client-safe rule:
CP9 can label plan posture and readiness only. It does not enable billing, does not enable campaigns, does not bypass communication or source gates, and does not expose Prime governance internals.
