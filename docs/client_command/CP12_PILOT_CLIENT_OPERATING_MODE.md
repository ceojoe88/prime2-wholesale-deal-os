# CP12 Pilot Client Operating Mode

CP12 adds pilot client operating mode for Prime2 Client Command OS.

Purpose:
- support a small, invite-only pilot rollout
- keep real client work manual-first and closely reviewed
- cap scope while communication, billing, and support gates mature
- preserve source-linked auditability for every enabled action

Core records:
- pilot programs
- workspace enrollments
- pilot operating modes
- health snapshots
- launch checklists
- risk reviews
- client-safe updates

Memphis demo state:
- Memphis is enrolled in `beta_pilot` with `manual_only` posture
- the launch checklist is blocked by compliance, communication, and billing gates
- the seeded risk review is blocked and requires escalation
- client-safe pilot updates remain visible while hiding admin-only notes

Implemented backend routes:
- `GET/POST /api/v1/client-command/pilot/programs`
- `GET/POST /api/v1/client-command/workspaces/{workspace_id}/pilot/enrollment`
- `GET/POST /api/v1/client-command/workspaces/{workspace_id}/pilot/operating-mode`
- `GET/POST /api/v1/client-command/workspaces/{workspace_id}/pilot/health-snapshot`
- `GET/POST /api/v1/client-command/workspaces/{workspace_id}/pilot/launch-checklist`
- `GET/POST /api/v1/client-command/workspaces/{workspace_id}/pilot/risk-review`
- `GET/POST /api/v1/client-command/workspaces/{workspace_id}/pilot/client-safe-updates`

Pilot mode defaults:
- off by default
- owner-approved per workspace
- manual-first
- non-autonomous
- non-bulk

What pilot mode does not allow:
- no public signup
- no bulk campaigns
- no autonomous execution
- no bypass of source gates
- no bypass of communication, billing, or owner-approval gates
- no exposure of Prime governance internals to pilot clients

Pilot rule:
CP12 can narrow and monitor live usage, but it cannot weaken existing source, consent, approval, provider, billing, or audit requirements.
