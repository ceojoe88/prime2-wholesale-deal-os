# CP4 Underwriting + Deal Evidence

CP4 adds the client-safe Underwriting Manager for evidence-backed review before any client offer decision. It is decision support only.

## What CP4 Adds

- Deal evidence packets
- Evidence items
- Underwriting reviews
- Conservative, standard, and aggressive offer scenarios
- Offer readiness gates
- Underwriting division events

## Underwriting Formula

When all required manual/demo inputs are present:

```text
max_allowable_offer = arv_estimate * 0.70 - repair_estimate - desired_assignment_fee - holding_cost_estimate
conservative_offer = max_allowable_offer * 0.90
standard_offer = max_allowable_offer
aggressive_offer = max_allowable_offer * 1.05
```

If ARV, repair estimate, holding cost, or target assignment fee is missing, CP4 does not invent values.

## Safety Boundary

CP4 does not pull live comps, call property/tax/title/MLS providers, generate contracts, send offers, submit title work, collect payment, or provide legal advice.

Every readiness section must show:

```text
Decision support only — no contract or offer has been sent.
```

## Evidence Gate

Offer readiness is blocked when evidence is missing, ARV or repairs are missing, calculated margin is thin or negative, DNC flags are present, or legal/title questions require qualified review.

Client-safe responses may show summaries, missing evidence, assumptions, transparent math, scenario ranges, risk flags, block reasons, and human-review status. Internal notes, provider payloads, audit internals, secrets, and hidden policy logic remain private.
