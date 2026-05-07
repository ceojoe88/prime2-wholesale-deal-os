# CP3 Acquisition AI Team

CP3 extends the Prime2 Client Command OS with a client-safe Acquisition Manager. It prepares seller conversation guidance from CP2 lead intelligence, missing-data records, and sanitized lead profile fields.

## What CP3 Adds

- Acquisition briefs
- Seller question plans
- Seller discovery questions
- Objection response drafts
- Follow-up draft queue
- Appointment readiness review
- Acquisition division events

## Safety Boundary

CP3 is non-live. It does not send SMS, send email, place calls, run skip tracing, check DNC providers, sync providers, collect payment, generate contracts, or provide legal advice.

All follow-up drafts are manual-use only. The UI must show:

```text
Manual use only — no message has been sent.
```

## Deterministic Logic

The Acquisition Manager consumes CP2 signals and never replaces CP2 scoring. Appointment readiness drops when seller motivation, phone/email, timeline, property condition, asking price, or CP2 missing-data confidence is incomplete.

High-risk or incomplete records require human review.

## Client-Safe Output

Client responses may include summaries, confidence levels, human-review flags, missing data, question plans, manual-use drafts, and recommended next action. They must not expose internal Prime governance, raw provider payloads, hidden scoring logic, admin controls, or unsafe execution fields.
