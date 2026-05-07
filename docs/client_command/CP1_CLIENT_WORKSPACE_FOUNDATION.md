# CP1 Client Workspace Foundation

CP1 introduces the first customer-facing Prime2 Client Command OS layer. It is a client-safe workspace foundation for real estate investor users without exposing internal Prime 2 governance, provider payloads, audit internals, secrets, or admin-only controls.

## Scope

CP1 adds:

- `ClientWorkspace`
- `ClientWorkspaceRole`
- `ClientWorkspaceMember`
- Tenant-safe permission grants:
  - `client_command.view`
  - `client_command.manage`
  - `client_command.leads_view`
  - `client_command.leads_manage`
  - `client_command.reports_view`
  - `client_command.admin`

## Safety Boundary

The client workspace layer is foundation-only. It cannot:

- Send SMS
- Send email
- Place voice calls
- Call skip-trace providers
- Call DNC-check providers
- Charge Stripe or any payment method
- Send contracts or e-signature packets
- Provide legal guidance
- Make fake ROI or profit claims
- Show internal Prime governance
- Show raw provider payloads

## Tenant Model

Every client lead, score, missing-data item, next action, and division event is attached to a `workspace_id`. API routes that include workspace context enforce workspace-safe access and return sanitized records only.

## API Surface

- `/api/v1/client-command/workspaces`
- `/api/v1/client-command/workspaces/{workspace_id}`
- `/api/v1/client-command/workspaces/{workspace_id}/leads`

## Frontend Surface

- `/dashboard/client-command`
- `/dashboard/client-command/workspaces`

CP1 is intentionally not a public SaaS launch, billing system, provider integration, or client self-service automation layer.
