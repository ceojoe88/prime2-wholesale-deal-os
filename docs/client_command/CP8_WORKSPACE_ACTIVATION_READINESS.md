# CP8 Workspace Activation Readiness

CP8 adds workspace activation readiness for Prime2 Client Command OS.

"Go-live" in CP8 means:
- the workspace is ready for controlled/manual Prime2 operation
- the client can begin the first weekly command cycle with manual review

"Go-live" in CP8 does **not** mean:
- live SMS
- live email
- voice calling
- provider execution
- billing or subscription activation
- contract generation or e-signature
- campaign launch

Readiness outputs:
- workspace readiness score
- readiness status
- activation blockers
- go-live readiness gate
- first weekly-cycle readiness
- onboarding report

Mandatory guardrails:
- `no_live_communication=true`
- `no_provider_execution=true`
- `no_billing_action=true`
- `no_contract_action=true`
- `no_campaign_action=true`

Reporting boundary:
- onboarding reports are client-safe
- no revenue, ROI, buyer purchase, assignment fee, or deal outcome is guaranteed
- Prime governance internals remain private
