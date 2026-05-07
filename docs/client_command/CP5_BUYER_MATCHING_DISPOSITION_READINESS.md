# CP5 Buyer Matching + Disposition Readiness

CP5 extends the client-facing Prime2 Client Command OS with a non-live Disposition Manager. It helps a client review buyer profiles, buy boxes, buyer confidence, deal-to-buyer fit, buyer demand evidence, and disposition readiness without contacting buyers or marketing a deal automatically.

## Scope

CP5 adds:

- Client buyer profiles and workspace-scoped buy boxes
- Deterministic buyer confidence scores
- Deal-to-buyer match records
- Buyer demand evidence notes
- Disposition readiness gates
- Manual-only buyer outreach drafts
- Disposition division events
- Client dashboard routes for disposition, buyers, matches, ready review, blocked, and needs review

CP5 consumes CP2 lead intelligence and CP4 evidence/underwriting/offer readiness. It does not replace those source-of-truth layers.

## Safety Boundary

CP5 is controlled and non-live:

- No buyer has been contacted.
- No campaign has started.
- No SMS, email, voice, CRM sync, buyer scraping, skip tracing, DNC provider check, MLS/property provider call, billing charge, e-signature, or contract generation occurs.
- Buyer outreach drafts are manual-use only.
- Disposition readiness is decision support only.
- No buyer purchase, profit, assignment fee, close, or market-demand result is guaranteed.
- Prime governance internals, raw provider payloads, secrets, internal notes, and unsafe execution fields remain hidden from client responses.

## Deterministic Logic

Buyer confidence improves when a buyer has clear target zip codes, price range, property type preferences, known rehab tolerance, active status, and stated or verified funding. It drops when the buy box is unclear, funding is unknown, price range is missing, proof of funds is missing, or the buyer needs review.

Deal-to-buyer matching uses client-entered buyer criteria plus CP4 decision-support values:

- Market and zip fit
- Property type fit
- Price range fit
- Rehab tolerance fit
- Buyer confidence and funding posture

Disposition readiness can reach `ready_for_client_review` only when CP4 offer readiness is safe, at least one possible or strong buyer match exists, buyer demand evidence or a buy box match exists, and no critical disposition blocker remains.

## Memphis Demo Scenario

The Memphis Virtual Wholesale Operator demo now includes four demo/local buyers:

- Memphis rental landlord: stated funding, medium rehab tolerance, rental buy box
- Memphis fix-and-flip buyer: verified POF, fast close speed, heavy rehab tolerance
- Out-of-market hedge buyer: narrow buy box and partial fit
- Needs-review buyer: unclear buy box and unknown funding

The five Memphis leads demonstrate the CP5 states:

- Lead 1: acquisition ready, not yet disposition-ready
- Lead 2: missing ARV/repair evidence, disposition blocked
- Lead 3: underwriting ready with buyer demand gap
- Lead 4: blocked by thin offer margin
- Lead 5: ready for CP5 buyer matching with strong buyer matches

## Routes

Backend:

- `/api/v1/client-command/workspaces/{workspace_id}/buyers`
- `/api/v1/client-command/buyers/{buyer_id}`
- `/api/v1/client-command/buyers/{buyer_id}/confidence-score`
- `/api/v1/client-command/buyers/{buyer_id}/buy-boxes`
- `/api/v1/client-command/leads/{lead_id}/buyer-matches`
- `/api/v1/client-command/disposition/matches`
- `/api/v1/client-command/disposition/strong-matches`
- `/api/v1/client-command/disposition/needs-review`
- `/api/v1/client-command/leads/{lead_id}/buyer-demand-evidence`
- `/api/v1/client-command/leads/{lead_id}/disposition-readiness`
- `/api/v1/client-command/disposition/ready-review`
- `/api/v1/client-command/disposition/blocked`
- `/api/v1/client-command/leads/{lead_id}/buyer-outreach-drafts`

Frontend:

- `/dashboard/client-command/disposition`
- `/dashboard/client-command/disposition/buyers`
- `/dashboard/client-command/disposition/buyers/[buyerId]`
- `/dashboard/client-command/disposition/matches`
- `/dashboard/client-command/disposition/ready-review`
- `/dashboard/client-command/disposition/blocked`
- `/dashboard/client-command/disposition/needs-review`
