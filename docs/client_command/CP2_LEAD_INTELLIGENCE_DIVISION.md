# CP2 Lead Intelligence Division

CP2 adds a client-safe Lead Intelligence Division for investor workspaces. It scores leads deterministically and exposes only sanitized, client-appropriate intelligence.

## Scoring Outputs

Each `ClientLeadIntelligenceScore` tracks:

- `motivation_score`
- `urgency_score`
- `equity_signal_score`
- `distress_signal_score`
- `contactability_score`
- `deal_probability_score`
- `missing_data_score`
- `final_priority_score`
- `recommended_next_action`
- `reason_summary`
- `confidence_level`
- `requires_human_review`

## Missing Data

`ClientLeadMissingDataItem` records readiness gaps such as missing property address, missing valuation data, missing equity signal, missing contactability data, and missing motivation signal. Missing data lowers readiness and can force human review.

## Next Best Action

`ClientLeadNextBestAction` records are recommendations only. They can tell the client to review, research, complete data, or prepare a call plan, but they cannot trigger any outbound provider action.

## Division Events

`ClientLeadDivisionEvent` records provide client-safe manager status and division summaries. They do not expose internal Prime governance, raw risk logic, raw provider payloads, or sensitive audit internals.

## Safety Boundary

CP2 cannot:

- Send or schedule outreach
- Trigger provider calls
- Run skip tracing
- Check DNC providers
- Charge payments
- Send contracts or e-signature packets
- Provide legal guidance
- Make unsupported ROI or profit claims
- Invent property value, equity, or distress data
- Expose internal Prime 2 governance

## API Surface

- `/api/v1/client-command/workspaces/{workspace_id}/leads`
- `/api/v1/client-command/leads/{lead_id}`
- `/api/v1/client-command/leads/{lead_id}/score`
- `/api/v1/client-command/leads/hot-board`
- `/api/v1/client-command/leads/next-actions`

## Frontend Surface

- `/dashboard/client-command/leads`
- `/dashboard/client-command/leads/[leadId]`
- `/dashboard/client-command/hot-leads`
- `/dashboard/client-command/next-actions`

CP2 is a controlled intelligence foundation, not autonomous fulfillment.
