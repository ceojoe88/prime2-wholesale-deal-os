import assert from "node:assert/strict";
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));

const requiredRouteFiles = [
  "src/app/dashboard/page.tsx",
  "src/app/dashboard/command-center/page.tsx",
  "src/app/dashboard/client-command/page.tsx",
  "src/app/dashboard/client-command/workspaces/page.tsx",
  "src/app/dashboard/client-command/leads/page.tsx",
  "src/app/dashboard/client-command/leads/[leadId]/page.tsx",
  "src/app/dashboard/client-command/hot-leads/page.tsx",
  "src/app/dashboard/client-command/next-actions/page.tsx",
  "src/app/dashboard/client-command/acquisition/page.tsx",
  "src/app/dashboard/client-command/acquisition/briefs/page.tsx",
  "src/app/dashboard/client-command/acquisition/needs-review/page.tsx",
  "src/app/dashboard/client-command/underwriting/page.tsx",
  "src/app/dashboard/client-command/underwriting/ready-review/page.tsx",
  "src/app/dashboard/client-command/underwriting/blocked/page.tsx",
  "src/app/dashboard/client-command/disposition/page.tsx",
  "src/app/dashboard/client-command/disposition/buyers/page.tsx",
  "src/app/dashboard/client-command/disposition/buyers/[buyerId]/page.tsx",
  "src/app/dashboard/client-command/disposition/matches/page.tsx",
  "src/app/dashboard/client-command/disposition/ready-review/page.tsx",
  "src/app/dashboard/client-command/disposition/blocked/page.tsx",
  "src/app/dashboard/client-command/disposition/needs-review/page.tsx",
  "src/app/dashboard/client-command/compliance/page.tsx",
  "src/app/dashboard/client-command/compliance/consent/page.tsx",
  "src/app/dashboard/client-command/compliance/opt-outs/page.tsx",
  "src/app/dashboard/client-command/compliance/blocked/page.tsx",
  "src/app/dashboard/client-command/compliance/needs-review/page.tsx",
  "src/app/dashboard/client-command/compliance/safe-manual-use/page.tsx",
  "src/app/dashboard/client-command/compliance/gates/page.tsx",
  "src/app/dashboard/client-command/reports/page.tsx",
  "src/app/dashboard/client-command/reports/[reportId]/page.tsx",
  "src/app/dashboard/client-command/reports/weekly/page.tsx",
  "src/app/dashboard/client-command/reports/bottlenecks/page.tsx",
  "src/app/dashboard/client-command/reports/recommended-actions/page.tsx",
  "src/app/dashboard/client-command/onboarding/page.tsx",
  "src/app/dashboard/client-command/onboarding/business-profile/page.tsx",
  "src/app/dashboard/client-command/onboarding/strategy/page.tsx",
  "src/app/dashboard/client-command/onboarding/markets/page.tsx",
  "src/app/dashboard/client-command/onboarding/pipeline/page.tsx",
  "src/app/dashboard/client-command/onboarding/lead-sources/page.tsx",
  "src/app/dashboard/client-command/onboarding/buyer-list/page.tsx",
  "src/app/dashboard/client-command/onboarding/team/page.tsx",
  "src/app/dashboard/client-command/onboarding/compliance/page.tsx",
  "src/app/dashboard/client-command/onboarding/first-leads/page.tsx",
  "src/app/dashboard/client-command/onboarding/readiness/page.tsx",
  "src/app/dashboard/client-command/onboarding/blockers/page.tsx",
  "src/app/dashboard/client-command/onboarding/tasks/page.tsx",
  "src/app/dashboard/client-command/onboarding/report/page.tsx",
  "src/app/dashboard/client-command/onboarding/activation-board/page.tsx",
  "src/app/dashboard/client-command/plans/page.tsx",
  "src/app/dashboard/client-command/plans/catalog/page.tsx",
  "src/app/dashboard/client-command/plans/features/page.tsx",
  "src/app/dashboard/client-command/plans/usage/page.tsx",
  "src/app/dashboard/client-command/plans/upgrade-recommendations/page.tsx",
  "src/app/dashboard/client-command/plans/billing-readiness/page.tsx",
  "src/app/dashboard/client-command/plans/subscription-placeholder/page.tsx",
  "src/app/dashboard/client-command/communication/page.tsx",
  "src/app/dashboard/client-command/communication/providers/page.tsx",
  "src/app/dashboard/client-command/communication/readiness/page.tsx",
  "src/app/dashboard/client-command/communication/dry-runs/page.tsx",
  "src/app/dashboard/client-command/communication/approvals/page.tsx",
  "src/app/dashboard/client-command/communication/attempts/page.tsx",
  "src/app/dashboard/client-command/communication/external-references/page.tsx",
  "src/app/dashboard/client-command/billing/page.tsx",
  "src/app/dashboard/client-command/billing/providers/page.tsx",
  "src/app/dashboard/client-command/billing/customers/page.tsx",
  "src/app/dashboard/client-command/billing/readiness/page.tsx",
  "src/app/dashboard/client-command/billing/dry-runs/page.tsx",
  "src/app/dashboard/client-command/billing/approvals/page.tsx",
  "src/app/dashboard/client-command/billing/attempts/page.tsx",
  "src/app/dashboard/client-command/billing/ledger/page.tsx",
  "src/app/dashboard/client-command/billing/external-references/page.tsx",
  "src/app/dashboard/client-command/pilot/page.tsx",
  "src/app/dashboard/client-command/pilot/admin-console/page.tsx",
  "src/app/dashboard/client-command/pilot/support-console/page.tsx",
  "src/app/dashboard/client-command/pilot/programs/page.tsx",
  "src/app/dashboard/client-command/pilot/enrollments/page.tsx",
  "src/app/dashboard/client-command/pilot/health/page.tsx",
  "src/app/dashboard/client-command/pilot/support/page.tsx",
  "src/app/dashboard/client-command/pilot/support-tickets/page.tsx",
  "src/app/dashboard/client-command/pilot/escalations/page.tsx",
  "src/app/dashboard/client-command/pilot/launch-checklist/page.tsx",
  "src/app/dashboard/client-command/pilot/risk-review/page.tsx",
  "src/app/dashboard/client-command/pilot/client-updates/page.tsx",
  "src/app/dashboard/client-command/pilot/updates/page.tsx",
  "src/app/dashboard/client-command/pilot/blocked/page.tsx",
  "src/app/dashboard/client-command/pilot/needs-review/page.tsx",
  "src/app/dashboard/first-deal-cockpit/page.tsx",
  "src/app/dashboard/first-deal-cockpit/calls/page.tsx",
  "src/app/dashboard/first-deal-cockpit/offers/page.tsx",
  "src/app/dashboard/first-deal-cockpit/buyer-validation/page.tsx",
  "src/app/dashboard/first-deal-cockpit/contract-ready/page.tsx",
  "src/app/dashboard/first-deal-cockpit/evidence/page.tsx",
  "src/app/dashboard/first-deal-cockpit/report/page.tsx",
  "src/app/dashboard/autonomy/page.tsx",
  "src/app/dashboard/autonomy/rules/page.tsx",
  "src/app/dashboard/autonomy/runs/page.tsx",
  "src/app/dashboard/autonomy/tasks/page.tsx",
  "src/app/dashboard/autonomy/daily-briefing/page.tsx",
  "src/app/dashboard/autonomy/escalations/page.tsx",
  "src/app/dashboard/auto-execution/page.tsx",
  "src/app/dashboard/auto-execution/rules/page.tsx",
  "src/app/dashboard/auto-execution/templates/page.tsx",
  "src/app/dashboard/auto-execution/dry-runs/page.tsx",
  "src/app/dashboard/auto-execution/attempts/page.tsx",
  "src/app/dashboard/auto-execution/audit/page.tsx",
  "src/app/dashboard/ai/page.tsx",
  "src/app/dashboard/ai/audit/page.tsx",
  "src/app/dashboard/ai/costs/page.tsx",
  "src/app/dashboard/ai/templates/page.tsx",
  "src/app/dashboard/worker/page.tsx",
  "src/app/dashboard/worker/jobs/page.tsx",
  "src/app/dashboard/worker/health/page.tsx",
  "src/app/dashboard/command-hierarchy/page.tsx",
  "src/app/dashboard/overseer/page.tsx",
  "src/app/dashboard/divisions/page.tsx",
  "src/app/dashboard/divisions/[divisionId]/page.tsx",
  "src/app/dashboard/managers/page.tsx",
  "src/app/dashboard/manager-queue/page.tsx",
  "src/app/dashboard/agents/page.tsx",
  "src/app/dashboard/agents/[agentId]/page.tsx",
  "src/app/dashboard/leads/page.tsx",
  "src/app/dashboard/leads/[leadId]/page.tsx",
  "src/app/dashboard/lead-imports/page.tsx",
  "src/app/dashboard/lead-imports/[batchId]/page.tsx",
  "src/app/dashboard/lead-imports/preview/page.tsx",
  "src/app/dashboard/lead-qa/page.tsx",
  "src/app/dashboard/lead-qa/[leadId]/page.tsx",
  "src/app/dashboard/call-outcomes/page.tsx",
  "src/app/dashboard/call-outcomes/[outcomeId]/page.tsx",
  "src/app/dashboard/call-intelligence/page.tsx",
  "src/app/dashboard/call-intelligence/[sessionId]/page.tsx",
  "src/app/dashboard/call-intelligence/new/page.tsx",
  "src/app/dashboard/call-intelligence/objections/page.tsx",
  "src/app/dashboard/call-intelligence/follow-ups/page.tsx",
  "src/app/dashboard/call-intelligence/quality/page.tsx",
  "src/app/dashboard/field-testing/page.tsx",
  "src/app/dashboard/feedback-loop/page.tsx",
  "src/app/dashboard/feedback-loop/[feedbackId]/page.tsx",
  "src/app/dashboard/scoring-adjustments/page.tsx",
  "src/app/dashboard/field-briefing/page.tsx",
  "src/app/dashboard/deals/page.tsx",
  "src/app/dashboard/deals/[dealId]/page.tsx",
  "src/app/dashboard/underwriting/page.tsx",
  "src/app/dashboard/profit-control/page.tsx",
  "src/app/dashboard/seller-acquisition/page.tsx",
  "src/app/dashboard/seller-acquisition/[leadId]/page.tsx",
  "src/app/dashboard/seller-followups/page.tsx",
  "src/app/dashboard/follow-up-control/page.tsx",
  "src/app/dashboard/offer-packets/page.tsx",
  "src/app/dashboard/offer-packets/[packetId]/page.tsx",
  "src/app/dashboard/contract-control/page.tsx",
  "src/app/dashboard/contract-control/[contractId]/page.tsx",
  "src/app/dashboard/title-handoff/page.tsx",
  "src/app/dashboard/title-handoff/[packetId]/page.tsx",
  "src/app/dashboard/assignment-readiness/page.tsx",
  "src/app/dashboard/communications/page.tsx",
  "src/app/dashboard/communications/[draftId]/page.tsx",
  "src/app/dashboard/communications/dry-runs/page.tsx",
  "src/app/dashboard/communications/attempts/page.tsx",
  "src/app/dashboard/communications/approvals/page.tsx",
  "src/app/dashboard/deal-room/page.tsx",
  "src/app/dashboard/deal-room/[dealRoomId]/page.tsx",
  "src/app/dashboard/closing-coordination/page.tsx",
  "src/app/dashboard/closing-coordination/blockers/page.tsx",
  "src/app/dashboard/closing-coordination/readiness/page.tsx",
  "src/app/dashboard/deal-evidence/page.tsx",
  "src/app/dashboard/deal-evidence/[packetId]/page.tsx",
  "src/app/dashboard/documents/page.tsx",
  "src/app/dashboard/documents/[documentId]/page.tsx",
  "src/app/dashboard/documents/upload/page.tsx",
  "src/app/dashboard/documents/issues/page.tsx",
  "src/app/dashboard/documents/review-queue/page.tsx",
  "src/app/dashboard/documents/evidence/page.tsx",
  "src/app/dashboard/assignment-fees/page.tsx",
  "src/app/dashboard/assignment-fees/[feeId]/page.tsx",
  "src/app/dashboard/buyer-demand/page.tsx",
  "src/app/dashboard/buyer-demand/[buyerId]/page.tsx",
  "src/app/dashboard/deal-distribution/page.tsx",
  "src/app/dashboard/deal-distribution/[distributionId]/page.tsx",
  "src/app/dashboard/buyer-priority/page.tsx",
  "src/app/dashboard/buyer-acceleration/page.tsx",
  "src/app/dashboard/buyer-acceleration/[dealId]/page.tsx",
  "src/app/dashboard/buyer-sequences/page.tsx",
  "src/app/dashboard/buyer-response-router/page.tsx",
  "src/app/dashboard/buyer-velocity/page.tsx",
  "src/app/dashboard/optimization/page.tsx",
  "src/app/dashboard/optimization/patterns/page.tsx",
  "src/app/dashboard/optimization/recommendations/page.tsx",
  "src/app/dashboard/optimization/agent-performance/page.tsx",
  "src/app/dashboard/optimization/lost-deals/page.tsx",
  "src/app/dashboard/optimization/source-quality/page.tsx",
  "src/app/dashboard/revenue-forecast/page.tsx",
  "src/app/dashboard/revenue-forecast/[forecastId]/page.tsx",
  "src/app/dashboard/market-scaling/page.tsx",
  "src/app/dashboard/lead-spend-planner/page.tsx",
  "src/app/dashboard/pipeline-value/page.tsx",
  "src/app/dashboard/operator-mode/page.tsx",
  "src/app/dashboard/operator-mode/approvals/page.tsx",
  "src/app/dashboard/operator-mode/exceptions/page.tsx",
  "src/app/dashboard/operator-mode/daily-report/page.tsx",
  "src/app/dashboard/operator-mode/system-trust/page.tsx",
  "src/app/dashboard/operator-mode/settings/page.tsx",
  "src/app/dashboard/production-readiness/page.tsx",
  "src/app/dashboard/cloud-readiness/page.tsx",
  "src/app/dashboard/cloud-readiness/env/page.tsx",
  "src/app/dashboard/cloud-readiness/security/page.tsx",
  "src/app/dashboard/cloud-readiness/backups/page.tsx",
  "src/app/dashboard/cloud-readiness/monitoring/page.tsx",
  "src/app/dashboard/cloud-readiness/deployment-checklist/page.tsx",
  "src/app/dashboard/live-activation/page.tsx",
  "src/app/dashboard/live-activation/[activationId]/page.tsx",
  "src/app/dashboard/live-activation/readiness/page.tsx",
  "src/app/dashboard/live-activation/approvals/page.tsx",
  "src/app/dashboard/live-activation/attempts/page.tsx",
  "src/app/dashboard/live-activation/blocked/page.tsx",
  "src/app/dashboard/audit-exports/page.tsx",
  "src/app/dashboard/audit-exports/[exportId]/page.tsx",
  "src/app/dashboard/evidence-attachments/page.tsx",
  "src/app/dashboard/provider-readiness/page.tsx",
  "src/app/dashboard/provider-readiness/[providerId]/page.tsx",
  "src/app/dashboard/provider-readiness/attempts/page.tsx",
  "src/app/dashboard/provider-readiness/webhooks/page.tsx",
  "src/app/dashboard/provider-readiness/credentials/page.tsx",
  "src/app/dashboard/campaigns/page.tsx",
  "src/app/dashboard/campaigns/[campaignId]/page.tsx",
  "src/app/dashboard/campaigns/new/page.tsx",
  "src/app/dashboard/campaigns/segments/page.tsx",
  "src/app/dashboard/campaigns/sequences/page.tsx",
  "src/app/dashboard/campaigns/approvals/page.tsx",
  "src/app/dashboard/campaigns/performance/page.tsx",
  "src/app/dashboard/market-enrichment/page.tsx",
  "src/app/dashboard/market-enrichment/[marketId]/page.tsx",
  "src/app/dashboard/comps/page.tsx",
  "src/app/dashboard/comps/[compId]/page.tsx",
  "src/app/dashboard/rent-estimates/page.tsx",
  "src/app/dashboard/buyer-activity/page.tsx",
  "src/app/dashboard/lead-source-roi/page.tsx",
  "src/app/dashboard/market-ranking/page.tsx",
  "src/app/dashboard/prime-memory/page.tsx",
  "src/app/dashboard/prime-memory/[memoryId]/page.tsx",
  "src/app/dashboard/prime-memory/patterns/page.tsx",
  "src/app/dashboard/learning-signals/page.tsx",
  "src/app/dashboard/scoring-weight-recommendations/page.tsx",
  "src/app/dashboard/playbook-recommendations/page.tsx",
  "src/app/dashboard/backups/page.tsx",
  "src/app/dashboard/offer-conversion/page.tsx",
  "src/app/dashboard/offer-conversion/[dealId]/page.tsx",
  "src/app/dashboard/negotiations/page.tsx",
  "src/app/dashboard/negotiations/[recordId]/page.tsx",
  "src/app/dashboard/contract-ready/page.tsx",
  "src/app/dashboard/title-review/page.tsx",
  "src/app/dashboard/title-review/[reviewId]/page.tsx",
  "src/app/dashboard/review-packets/page.tsx",
  "src/app/dashboard/buyers/page.tsx",
  "src/app/dashboard/buyers/[buyerId]/page.tsx",
  "src/app/dashboard/buyer-matches/page.tsx",
  "src/app/dashboard/compliance/page.tsx",
  "src/app/dashboard/daily-briefing/page.tsx",
  "src/app/buyer-portal/page.tsx",
  "src/app/buyer-portal/deals/page.tsx",
  "src/app/buyer-portal/deals/[dealId]/page.tsx",
  "src/app/buyer-portal/profile/page.tsx",
  "src/app/buyer-portal/watchlist/page.tsx",
  "src/app/seller-portal/page.tsx",
  "src/app/seller-portal/offer/page.tsx",
  "src/app/seller-portal/property/page.tsx",
  "src/app/seller-portal/timeline/page.tsx",
  "src/app/seller-portal/documents/page.tsx",
  "src/app/seller-portal/messages/page.tsx",
  "src/app/mobile/page.tsx",
  "src/app/mobile/today/page.tsx",
  "src/app/mobile/calls/page.tsx",
  "src/app/mobile/leads/[leadId]/page.tsx",
  "src/app/mobile/deals/[dealId]/page.tsx",
  "src/app/mobile/approvals/page.tsx",
  "src/app/mobile/briefing/page.tsx",
  "src/app/mobile/notes/page.tsx",
  "src/app/mobile/buyers/page.tsx",
  "src/app/mobile/documents/page.tsx"
];

function walk(dir) {
  return readdirSync(dir).flatMap((entry) => {
    const file = join(dir, entry);
    return statSync(file).isDirectory() ? walk(file) : [file];
  });
}

function routeToPageFile(href) {
  const segments = href.split("/").filter(Boolean);
  return join(root, "src", "app", ...segments, "page.tsx");
}

function relativeFromRoot(file) {
  return file.slice(root.length + 1).replaceAll("\\", "/");
}

test("dashboard route files exist and render a page component", () => {
  for (const routeFile of requiredRouteFiles) {
    const absolute = join(root, routeFile);
    assert.equal(existsSync(absolute), true, routeFile);
    const source = readFileSync(absolute, "utf8");
    assert.match(source, /export default (async )?function/);
    assert.match(source, /return \(/);
  }
});

test("operator-only frontend has no public signup or client portals", () => {
  const files = walk(join(root, "src", "app")).filter((file) => file.endsWith(".tsx"));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n").toLowerCase();
  assert.equal(joined.includes("/signup"), false);
  assert.equal(joined.includes("client portal"), false);
});

test("dashboard navigation targets implemented page routes", () => {
  const navigation = readFileSync(join(root, "src", "lib", "navigation.ts"), "utf8");
  const hrefs = [...navigation.matchAll(/href: "([^"]+)"/g)].map((match) => match[1]);
  assert.ok(hrefs.length > 40);
  for (const href of hrefs) {
    assert.equal(existsSync(routeToPageFile(href)), true, href);
  }
});

test("dynamic detail route files guard missing ids with notFound", () => {
  const detailFiles = walk(join(root, "src", "app")).filter((file) =>
    file.endsWith("page.tsx") && file.includes("[")
  );
  assert.ok(detailFiles.length > 20);
  for (const file of detailFiles) {
    const source = readFileSync(file, "utf8");
    assert.match(source, /notFound\(/, relativeFromRoot(file));
    assert.match(source, /from "next\/navigation"/, relativeFromRoot(file));
  }
});

test("Prime 2 identity is used internally and old overseer/product name is absent", () => {
  const sourceFiles = walk(join(root, "src")).filter((file) =>
    [".ts", ".tsx"].some((extension) => file.endsWith(extension))
  );
  const oldNameFiles = sourceFiles
    .filter((file) => readFileSync(file, "utf8").includes(["Wholesale", "Prime"].join(" ")))
    .map(relativeFromRoot);
  assert.deepEqual(oldNameFiles, []);

  for (const routeFile of [
    "src/app/dashboard/overseer/page.tsx",
    "src/app/dashboard/operator-mode/page.tsx",
    "src/app/dashboard/autonomy/page.tsx",
    "src/app/dashboard/command-hierarchy/page.tsx",
    "src/app/dashboard/daily-briefing/page.tsx",
    "src/app/dashboard/autonomy/daily-briefing/page.tsx"
  ]) {
    const source = readFileSync(join(root, routeFile), "utf8");
    assert.match(source, /Prime 2/, routeFile);
  }
});

test("buyer portal route files avoid internal seller and profit logic labels", () => {
  const files = walk(join(root, "src", "app", "buyer-portal")).filter((file) => file.endsWith(".tsx"));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n").toLowerCase();
  for (const forbidden of [
    "seller name",
    "seller contact",
    "motivation score",
    "lead source",
    "assignment fee",
    "projected assignment",
    "max seller offer",
    "prime 2",
    "compliance risk"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
  assert.equal(joined.includes("contract executionallowed: true"), false);
});

test("seller portal route files avoid buyer data and internal profit logic labels", () => {
  const files = walk(join(root, "src", "app", "seller-portal")).filter((file) => file.endsWith(".tsx"));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n").toLowerCase();
  for (const forbidden of [
    "buyer list",
    "buyer price",
    "assignment fee",
    "internal spread",
    "mao",
    "motivation score",
    "seller temperature",
    "prime 2",
    "compliance risk",
    "manager queue",
    "agent queue"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
  assert.equal(joined.includes("contractexecutionallowed: true"), false);
  assert.equal(joined.includes("automaticnegotiationallowed: true"), false);
});

test("V19 field-testing pages expose no unsafe live-action buttons", () => {
  const files = [
    "src/app/dashboard/lead-imports/page.tsx",
    "src/app/dashboard/lead-imports/[batchId]/page.tsx",
    "src/app/dashboard/lead-imports/preview/page.tsx",
    "src/app/dashboard/lead-qa/page.tsx",
    "src/app/dashboard/lead-qa/[leadId]/page.tsx",
    "src/app/dashboard/call-outcomes/page.tsx",
    "src/app/dashboard/call-outcomes/[outcomeId]/page.tsx",
    "src/app/dashboard/field-testing/page.tsx",
    "src/app/dashboard/feedback-loop/page.tsx",
    "src/app/dashboard/feedback-loop/[feedbackId]/page.tsx",
    "src/app/dashboard/scoring-adjustments/page.tsx",
    "src/app/dashboard/field-briefing/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send all",
    "auto call",
    "execute contract",
    "submit to title",
    "guarantee profit",
    "legal advice",
    "publish automatically"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("V20 and V21 pages expose no live execution controls", () => {
  const files = [
    "src/app/dashboard/ai/page.tsx",
    "src/app/dashboard/ai/audit/page.tsx",
    "src/app/dashboard/ai/costs/page.tsx",
    "src/app/dashboard/ai/templates/page.tsx",
    "src/app/dashboard/worker/page.tsx",
    "src/app/dashboard/worker/jobs/page.tsx",
    "src/app/dashboard/worker/health/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send all",
    "bulk blast",
    "auto call",
    "execute contract",
    "submit to title",
    "publish automatically",
    "provider calls\" value=\"1"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("V22 provider readiness pages expose no unsafe live-provider controls", () => {
  const files = [
    "src/app/dashboard/provider-readiness/page.tsx",
    "src/app/dashboard/provider-readiness/[providerId]/page.tsx",
    "src/app/dashboard/provider-readiness/attempts/page.tsx",
    "src/app/dashboard/provider-readiness/webhooks/page.tsx",
    "src/app/dashboard/provider-readiness/credentials/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send all",
    "bulk blast",
    "auto call",
    "execute contract",
    "submit to title",
    "publish automatically",
    "raw values are stored"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("V23 call intelligence pages expose no live call or send controls", () => {
  const files = [
    "src/app/dashboard/call-intelligence/page.tsx",
    "src/app/dashboard/call-intelligence/[sessionId]/page.tsx",
    "src/app/dashboard/call-intelligence/new/page.tsx",
    "src/app/dashboard/call-intelligence/objections/page.tsx",
    "src/app/dashboard/call-intelligence/follow-ups/page.tsx",
    "src/app/dashboard/call-intelligence/quality/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send all",
    "bulk blast",
    "auto call",
    "execute contract",
    "submit to title",
    "publish automatically",
    "live calling enabled",
    "live response generated"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("V24 document intelligence pages expose no execution or raw document controls", () => {
  const files = [
    "src/app/dashboard/documents/page.tsx",
    "src/app/dashboard/documents/[documentId]/page.tsx",
    "src/app/dashboard/documents/upload/page.tsx",
    "src/app/dashboard/documents/issues/page.tsx",
    "src/app/dashboard/documents/review-queue/page.tsx",
    "src/app/dashboard/documents/evidence/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send all",
    "bulk blast",
    "auto call",
    "execute contract",
    "submit to title",
    "publish automatically",
    "raw document text",
    "legal advice"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("V25 campaign brain pages expose no bulk or uncontrolled send controls", () => {
  const files = [
    "src/app/dashboard/campaigns/page.tsx",
    "src/app/dashboard/campaigns/[campaignId]/page.tsx",
    "src/app/dashboard/campaigns/new/page.tsx",
    "src/app/dashboard/campaigns/segments/page.tsx",
    "src/app/dashboard/campaigns/sequences/page.tsx",
    "src/app/dashboard/campaigns/approvals/page.tsx",
    "src/app/dashboard/campaigns/performance/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send all",
    "blast",
    "auto call",
    "execute contract",
    "submit to title",
    "publish automatically",
    "guaranteed profit",
    "this will sell today"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("V26 market enrichment pages expose no unsupported market claims", () => {
  const files = [
    "src/app/dashboard/market-enrichment/page.tsx",
    "src/app/dashboard/market-enrichment/[marketId]/page.tsx",
    "src/app/dashboard/comps/page.tsx",
    "src/app/dashboard/comps/[compId]/page.tsx",
    "src/app/dashboard/rent-estimates/page.tsx",
    "src/app/dashboard/buyer-activity/page.tsx",
    "src/app/dashboard/lead-source-roi/page.tsx",
    "src/app/dashboard/market-ranking/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send all",
    "bulk blast",
    "auto call",
    "execute contract",
    "submit to title",
    "publish automatically",
    "guaranteed roi",
    "guaranteed profit",
    "fake comps",
    "paid api"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("V27 Prime 2 memory pages expose no unsafe learning controls", () => {
  const files = [
    "src/app/dashboard/prime-memory/page.tsx",
    "src/app/dashboard/prime-memory/[memoryId]/page.tsx",
    "src/app/dashboard/prime-memory/patterns/page.tsx",
    "src/app/dashboard/learning-signals/page.tsx",
    "src/app/dashboard/scoring-weight-recommendations/page.tsx",
    "src/app/dashboard/playbook-recommendations/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send all",
    "bulk blast",
    "auto call",
    "execute contract",
    "submit to title",
    "publish automatically",
    "auto-apply",
    "override compliance",
    "guaranteed profit",
    "guaranteed roi",
    "expose internal strategy"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("V28 mobile operator pages expose no unsafe field controls", () => {
  const files = [
    "src/app/mobile/page.tsx",
    "src/app/mobile/today/page.tsx",
    "src/app/mobile/calls/page.tsx",
    "src/app/mobile/leads/[leadId]/page.tsx",
    "src/app/mobile/deals/[dealId]/page.tsx",
    "src/app/mobile/approvals/page.tsx",
    "src/app/mobile/briefing/page.tsx",
    "src/app/mobile/notes/page.tsx",
    "src/app/mobile/buyers/page.tsx",
    "src/app/mobile/documents/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send all",
    "blast",
    "auto call",
    "execute contract",
    "submit to title",
    "publish automatically",
    "guarantee profit",
    "legal advice",
    "live send"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("V29 cloud readiness pages expose no deployment or secret controls", () => {
  const files = [
    "src/app/dashboard/cloud-readiness/page.tsx",
    "src/app/dashboard/cloud-readiness/env/page.tsx",
    "src/app/dashboard/cloud-readiness/security/page.tsx",
    "src/app/dashboard/cloud-readiness/backups/page.tsx",
    "src/app/dashboard/cloud-readiness/monitoring/page.tsx",
    "src/app/dashboard/cloud-readiness/deployment-checklist/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send all",
    "blast",
    "auto call",
    "execute contract",
    "submit to title",
    "publish automatically",
    "guarantee profit",
    "deploy now",
    "show secret",
    "secret value:"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("V30 live activation pages expose no bulk or bypass controls", () => {
  const files = [
    "src/app/dashboard/live-activation/page.tsx",
    "src/app/dashboard/live-activation/[activationId]/page.tsx",
    "src/app/dashboard/live-activation/readiness/page.tsx",
    "src/app/dashboard/live-activation/approvals/page.tsx",
    "src/app/dashboard/live-activation/attempts/page.tsx",
    "src/app/dashboard/live-activation/blocked/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send all",
    "blast",
    "auto call",
    "execute contract",
    "submit to title",
    "publish automatically",
    "guarantee profit",
    "bypass enabled",
    "bulk enabled",
    "provider called\" value=\"1"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("V31 first deal cockpit pages expose no unsafe execution controls", () => {
  const files = [
    "src/app/dashboard/first-deal-cockpit/page.tsx",
    "src/app/dashboard/first-deal-cockpit/calls/page.tsx",
    "src/app/dashboard/first-deal-cockpit/offers/page.tsx",
    "src/app/dashboard/first-deal-cockpit/buyer-validation/page.tsx",
    "src/app/dashboard/first-deal-cockpit/contract-ready/page.tsx",
    "src/app/dashboard/first-deal-cockpit/evidence/page.tsx",
    "src/app/dashboard/first-deal-cockpit/report/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send all",
    "blast",
    "auto call",
    "execute contract",
    "submit to title",
    "publish automatically",
    "guarantee profit",
    "legal advice",
    "live send",
    "buyer is guaranteed"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("CP1 and CP2 client command pages expose no dangerous client controls", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/workspaces/page.tsx",
    "src/app/dashboard/client-command/leads/page.tsx",
    "src/app/dashboard/client-command/leads/[leadId]/page.tsx",
    "src/app/dashboard/client-command/hot-leads/page.tsx",
    "src/app/dashboard/client-command/next-actions/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send sms",
    "send email",
    "auto call",
    "voice call",
    "skip trace provider",
    "dnc check provider",
    "stripe charge",
    "charge card",
    "send contract",
    "e-signature send",
    "legal advice",
    "guaranteed roi",
    "guaranteed profit",
    "raw_provider_payload",
    "internal_prime_governance"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("CP3 and CP4 client command pages render managers and preserve manual boundaries", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/acquisition/page.tsx",
    "src/app/dashboard/client-command/acquisition/briefs/page.tsx",
    "src/app/dashboard/client-command/acquisition/needs-review/page.tsx",
    "src/app/dashboard/client-command/underwriting/page.tsx",
    "src/app/dashboard/client-command/underwriting/ready-review/page.tsx",
    "src/app/dashboard/client-command/underwriting/blocked/page.tsx",
    "src/app/dashboard/client-command/leads/[leadId]/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n");
  assert.match(joined, /Acquisition Manager/);
  assert.match(joined, /Underwriting Manager/);
  assert.match(joined, /Memphis Demo Scenario/);
  assert.match(joined, /Manual use only — no message has been sent\./);
  assert.match(joined, /Decision support only — no contract or offer has been sent\./);
});

test("CP3 and CP4 client command pages expose no forbidden client controls", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/workspaces/page.tsx",
    "src/app/dashboard/client-command/leads/page.tsx",
    "src/app/dashboard/client-command/leads/[leadId]/page.tsx",
    "src/app/dashboard/client-command/hot-leads/page.tsx",
    "src/app/dashboard/client-command/next-actions/page.tsx",
    "src/app/dashboard/client-command/acquisition/page.tsx",
    "src/app/dashboard/client-command/acquisition/briefs/page.tsx",
    "src/app/dashboard/client-command/acquisition/needs-review/page.tsx",
    "src/app/dashboard/client-command/underwriting/page.tsx",
    "src/app/dashboard/client-command/underwriting/ready-review/page.tsx",
    "src/app/dashboard/client-command/underwriting/blocked/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send sms",
    "send email",
    "call now",
    "auto dial",
    "start campaign",
    "pull skip trace",
    "check dnc live",
    "pull live comps",
    "generate contract",
    "send offer",
    "e-sign",
    "charge now",
    "collect payment",
    "activate live",
    "sync to provider",
    "dispatch agent",
    "execute",
    "legal advice",
    "guaranteed roi",
    "guaranteed profit",
    "raw_provider_payload",
    "internal_prime_governance"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("CP5 client command pages render Disposition Manager and manual buyer boundaries", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/disposition/page.tsx",
    "src/app/dashboard/client-command/disposition/buyers/page.tsx",
    "src/app/dashboard/client-command/disposition/buyers/[buyerId]/page.tsx",
    "src/app/dashboard/client-command/disposition/matches/page.tsx",
    "src/app/dashboard/client-command/disposition/ready-review/page.tsx",
    "src/app/dashboard/client-command/disposition/blocked/page.tsx",
    "src/app/dashboard/client-command/disposition/needs-review/page.tsx",
    "src/app/dashboard/client-command/leads/[leadId]/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n");
  assert.match(joined, /Disposition Manager/);
  assert.match(joined, /Buyer Match Summary/);
  assert.match(joined, /Buyer Demand Evidence/);
  assert.match(joined, /Memphis Demo Scenario/);
  assert.match(joined, /Manual use only .* no buyer has been contacted\./);
  assert.match(joined, /Decision support only .* no campaign, contract, or buyer outreach has been sent\./);
});

test("CP5 client command pages expose no forbidden buyer execution controls", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/leads/page.tsx",
    "src/app/dashboard/client-command/leads/[leadId]/page.tsx",
    "src/app/dashboard/client-command/disposition/page.tsx",
    "src/app/dashboard/client-command/disposition/buyers/page.tsx",
    "src/app/dashboard/client-command/disposition/buyers/[buyerId]/page.tsx",
    "src/app/dashboard/client-command/disposition/matches/page.tsx",
    "src/app/dashboard/client-command/disposition/ready-review/page.tsx",
    "src/app/dashboard/client-command/disposition/blocked/page.tsx",
    "src/app/dashboard/client-command/disposition/needs-review/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send sms",
    "send email",
    "call now",
    "auto dial",
    "start campaign",
    "blast buyers",
    "pull buyer list",
    "scrape buyers",
    "pull skip trace",
    "check dnc live",
    "pull live comps",
    "generate contract",
    "send offer",
    "e-sign",
    "charge now",
    "collect payment",
    "activate live",
    "sync to provider",
    "dispatch agent",
    "execute",
    "contact buyer",
    "market deal",
    "launch campaign",
    "send deal"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("CP6 client command pages render Compliance Manager and manual-use boundaries", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/compliance/page.tsx",
    "src/app/dashboard/client-command/compliance/consent/page.tsx",
    "src/app/dashboard/client-command/compliance/opt-outs/page.tsx",
    "src/app/dashboard/client-command/compliance/blocked/page.tsx",
    "src/app/dashboard/client-command/compliance/needs-review/page.tsx",
    "src/app/dashboard/client-command/compliance/safe-manual-use/page.tsx",
    "src/app/dashboard/client-command/compliance/gates/page.tsx",
    "src/app/dashboard/client-command/leads/[leadId]/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n");
  assert.match(joined, /Compliance Manager/);
  assert.match(joined, /Manual-use approval only - no message has been sent\./);
  assert.match(joined, /Readiness check only - no provider check or live communication occurred\./);
});

test("CP7 client command pages render weekly report boundaries", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/reports/page.tsx",
    "src/app/dashboard/client-command/reports/weekly/page.tsx",
    "src/app/dashboard/client-command/reports/[reportId]/page.tsx",
    "src/app/dashboard/client-command/reports/bottlenecks/page.tsx",
    "src/app/dashboard/client-command/reports/recommended-actions/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n");
  assert.match(joined, /Client Success Manager|Weekly Client Command Reports/);
  assert.match(joined, /Client-safe weekly report - no revenue, ROI, or deal outcome is guaranteed\./);
});

test("CP6 and CP7 client command pages expose no forbidden compliance or reporting controls", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/leads/[leadId]/page.tsx",
    "src/app/dashboard/client-command/disposition/buyers/[buyerId]/page.tsx",
    "src/app/dashboard/client-command/compliance/page.tsx",
    "src/app/dashboard/client-command/compliance/consent/page.tsx",
    "src/app/dashboard/client-command/compliance/opt-outs/page.tsx",
    "src/app/dashboard/client-command/compliance/blocked/page.tsx",
    "src/app/dashboard/client-command/compliance/needs-review/page.tsx",
    "src/app/dashboard/client-command/compliance/safe-manual-use/page.tsx",
    "src/app/dashboard/client-command/compliance/gates/page.tsx",
    "src/app/dashboard/client-command/reports/page.tsx",
    "src/app/dashboard/client-command/reports/weekly/page.tsx",
    "src/app/dashboard/client-command/reports/[reportId]/page.tsx",
    "src/app/dashboard/client-command/reports/bottlenecks/page.tsx",
    "src/app/dashboard/client-command/reports/recommended-actions/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send sms",
    "send email",
    "call now",
    "auto dial",
    "start campaign",
    "blast buyers",
    "contact buyer",
    "contact seller",
    "pull buyer list",
    "scrape buyers",
    "pull skip trace",
    "check dnc live",
    "register 10dlc live",
    "pull live comps",
    "generate contract",
    "send offer",
    "e-sign",
    "charge now",
    "collect payment",
    "activate live",
    "sync to provider",
    "dispatch agent",
    "execute",
    "launch campaign",
    "send deal",
    "guaranteed roi",
    "guaranteed profit",
    "guaranteed buyer",
    "guaranteed assignment fee"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("CP8 client command pages render onboarding and manual-readiness boundaries", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/workspaces/page.tsx",
    "src/app/dashboard/client-command/leads/[leadId]/page.tsx",
    "src/app/dashboard/client-command/onboarding/page.tsx",
    "src/app/dashboard/client-command/onboarding/business-profile/page.tsx",
    "src/app/dashboard/client-command/onboarding/strategy/page.tsx",
    "src/app/dashboard/client-command/onboarding/markets/page.tsx",
    "src/app/dashboard/client-command/onboarding/pipeline/page.tsx",
    "src/app/dashboard/client-command/onboarding/lead-sources/page.tsx",
    "src/app/dashboard/client-command/onboarding/buyer-list/page.tsx",
    "src/app/dashboard/client-command/onboarding/team/page.tsx",
    "src/app/dashboard/client-command/onboarding/compliance/page.tsx",
    "src/app/dashboard/client-command/onboarding/first-leads/page.tsx",
    "src/app/dashboard/client-command/onboarding/readiness/page.tsx",
    "src/app/dashboard/client-command/onboarding/blockers/page.tsx",
    "src/app/dashboard/client-command/onboarding/tasks/page.tsx",
    "src/app/dashboard/client-command/onboarding/report/page.tsx",
    "src/app/dashboard/client-command/onboarding/activation-board/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n");
  assert.match(joined, /Onboarding Manager/);
  assert.match(joined, /Manual operation readiness only - no live communication, provider execution, billing, contracts, or campaigns are enabled\./);
  assert.match(joined, /Setup record only - no provider sync or campaign launch occurred\./);
  assert.match(joined, /Buyer setup only - no buyer has been contacted\./);
  assert.match(joined, /Readiness checklist only - no DNC provider check or 10DLC live registration occurred\./);
  assert.match(joined, /Client-safe onboarding report - no revenue, ROI, or deal outcome is guaranteed\./);
});

test("CP8 client command pages expose no forbidden onboarding or activation controls", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/workspaces/page.tsx",
    "src/app/dashboard/client-command/leads/[leadId]/page.tsx",
    "src/app/dashboard/client-command/onboarding/page.tsx",
    "src/app/dashboard/client-command/onboarding/business-profile/page.tsx",
    "src/app/dashboard/client-command/onboarding/strategy/page.tsx",
    "src/app/dashboard/client-command/onboarding/markets/page.tsx",
    "src/app/dashboard/client-command/onboarding/pipeline/page.tsx",
    "src/app/dashboard/client-command/onboarding/lead-sources/page.tsx",
    "src/app/dashboard/client-command/onboarding/buyer-list/page.tsx",
    "src/app/dashboard/client-command/onboarding/team/page.tsx",
    "src/app/dashboard/client-command/onboarding/compliance/page.tsx",
    "src/app/dashboard/client-command/onboarding/first-leads/page.tsx",
    "src/app/dashboard/client-command/onboarding/readiness/page.tsx",
    "src/app/dashboard/client-command/onboarding/blockers/page.tsx",
    "src/app/dashboard/client-command/onboarding/tasks/page.tsx",
    "src/app/dashboard/client-command/onboarding/report/page.tsx",
    "src/app/dashboard/client-command/onboarding/activation-board/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send sms",
    "send email",
    "call now",
    "auto dial",
    "start campaign",
    "launch campaign",
    "blast buyers",
    "contact buyer",
    "contact seller",
    "pull buyer list",
    "scrape buyers",
    "pull skip trace",
    "check dnc live",
    "register 10dlc live",
    "pull live comps",
    "generate contract",
    "send offer",
    "e-sign",
    "charge now",
    "collect payment",
    "activate billing",
    "activate live",
    "sync to provider",
    "dispatch agent",
    "execute",
    "send deal",
    "guaranteed roi",
    "guaranteed profit",
    "guaranteed buyer",
    "guaranteed assignment fee"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("client-command CP9-CP12 navigation entries target implemented routes", () => {
  const navigation = readFileSync(join(root, "src", "lib", "navigation.ts"), "utf8");
  for (const expected of [
    'href: "/dashboard/client-command/plans", label: "Client Plans"',
    'href: "/dashboard/client-command/communication", label: "Client Communication"',
    'href: "/dashboard/client-command/billing", label: "Client Billing"',
    'href: "/dashboard/client-command/pilot", label: "Client Pilot"'
  ]) {
    assert.match(navigation, new RegExp(expected.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
  }
});

test("client-command CP9-CP12 implemented surface route files exist", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/plans/page.tsx",
    "src/app/dashboard/client-command/communication/page.tsx",
    "src/app/dashboard/client-command/billing/page.tsx",
    "src/app/dashboard/client-command/pilot/page.tsx"
  ];
  for (const routeFile of files) {
    const absolute = join(root, routeFile);
    assert.equal(existsSync(absolute), true, routeFile);
    assert.match(readFileSync(absolute, "utf8"), /export default (async )?function/, routeFile);
  }
});

test("client-command CP9-CP12 dedicated pages render expected titles and boundaries", () => {
  const files = [
    "src/app/dashboard/client-command/plans/page.tsx",
    "src/app/dashboard/client-command/communication/page.tsx",
    "src/app/dashboard/client-command/billing/page.tsx",
    "src/app/dashboard/client-command/pilot/page.tsx",
    "src/app/dashboard/client-command/plans/catalog/page.tsx",
    "src/app/dashboard/client-command/communication/dry-runs/page.tsx",
    "src/app/dashboard/client-command/billing/approvals/page.tsx",
    "src/app/dashboard/client-command/pilot/blocked/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n");
  for (const requiredText of [
    "Plan catalog and readiness gates",
    "Controlled live communication gate",
    "Controlled billing gate",
    "Pilot mode and support routing",
    "Plan Catalog",
    "Communication Dry Runs",
    "Billing Approvals",
    "Blocked Pilot Workspaces",
    "Client-safe Updates",
    "Billing gate only - no payment occurs unless all billing gates pass.",
    "Pilot mode does not bypass source gates."
  ]) {
    assert.match(joined, new RegExp(requiredText.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
  }
});

test("client-command dashboard renders CP9-CP12 plans communication billing and pilot panels", () => {
  const source = readFileSync(join(root, "src", "app", "dashboard", "client-command", "page.tsx"), "utf8");
  for (const requiredText of [
    "CP9 Plans Panel",
    "CP10 Communication Panel",
    "CP11 Billing Panel",
    "CP12 Pilot Panel",
    "Memphis plan gate",
    "Memphis communication gate",
    "Billing guard",
    "Memphis pilot health",
    "Plan Access Manager",
    "Communication Control Manager",
    "Billing Guard Manager",
    "Pilot Operations Manager",
    "No raw card data is stored.",
    "Pilot mode does not bypass source gates.",
    "Billing gate only - no payment occurs unless all billing gates pass.",
    "Live communication remains manual-only until readiness, dry-run, approval, and live-flag gates all clear.",
    "/dashboard/client-command/plans",
    "/dashboard/client-command/communication",
    "/dashboard/client-command/billing",
    "/dashboard/client-command/pilot"
  ]) {
    assert.match(source, new RegExp(requiredText.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
  }
});

test("client-command CP9-CP12 surface exposes no forbidden plan billing pilot or live-send controls", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/plans/page.tsx",
    "src/app/dashboard/client-command/communication/page.tsx",
    "src/app/dashboard/client-command/communication/dry-runs/page.tsx",
    "src/app/dashboard/client-command/communication/approvals/page.tsx",
    "src/app/dashboard/client-command/communication/attempts/page.tsx",
    "src/app/dashboard/client-command/billing/page.tsx",
    "src/app/dashboard/client-command/billing/dry-runs/page.tsx",
    "src/app/dashboard/client-command/billing/approvals/page.tsx",
    "src/app/dashboard/client-command/pilot/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "create stripe customer",
    "store card",
    "start subscription",
    "force charge",
    "charge card",
    "override gate",
    "delete client data",
    "contractexecutionallowed: true",
    "titlesubmissionallowed: true",
    "automaticacceptanceallowed: true",
    "billingliveallowed: true",
    "provider called\" value=\"1",
    "raw_provider_payload",
    "internal_prime_governance"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("CP9 dashboard route files exist for buyer demand and distribution pages", () => {
  const files = [
    "src/app/dashboard/buyer-demand/page.tsx",
    "src/app/dashboard/buyer-demand/[buyerId]/page.tsx",
    "src/app/dashboard/deal-distribution/page.tsx",
    "src/app/dashboard/deal-distribution/[distributionId]/page.tsx",
    "src/app/dashboard/buyer-priority/page.tsx"
  ];
  for (const routeFile of files) {
    const absolute = join(root, routeFile);
    assert.equal(existsSync(absolute), true, routeFile);
    assert.match(readFileSync(absolute, "utf8"), /export default (async )?function/, routeFile);
  }
});

test("CP9 dashboard pages render draft-only buyer demand and distribution boundaries", () => {
  const files = [
    "src/app/dashboard/buyer-demand/page.tsx",
    "src/app/dashboard/deal-distribution/page.tsx",
    "src/app/dashboard/buyer-priority/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n");
  assert.match(joined, /Buyer demand command/);
  assert.match(joined, /without sending blasts or exposing internal spread logic\./);
  assert.match(joined, /Draft-only buyer distribution/);
  assert.match(joined, /without live sends, bulk blasts, or seller data exposure\./);
  assert.match(joined, /Most likely buyers to close fast/);
  assert.match(joined, /Recommendations remain internal only\./);
});

test("CP9 dashboard pages expose no forbidden buyer-demand execution controls", () => {
  const files = [
    "src/app/dashboard/buyer-demand/page.tsx",
    "src/app/dashboard/deal-distribution/page.tsx",
    "src/app/dashboard/buyer-priority/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send all",
    "auto call",
    "execute contract",
    "submit to title",
    "charge card",
    "create stripe customer",
    "store card",
    "provider called\" value=\"1",
    "raw_provider_payload"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("CP10 dashboard route files exist for conversion and negotiation pages", () => {
  const files = [
    "src/app/dashboard/offer-conversion/page.tsx",
    "src/app/dashboard/offer-conversion/[dealId]/page.tsx",
    "src/app/dashboard/negotiations/page.tsx",
    "src/app/dashboard/negotiations/[recordId]/page.tsx",
    "src/app/dashboard/contract-ready/page.tsx"
  ];
  for (const routeFile of files) {
    const absolute = join(root, routeFile);
    assert.equal(existsSync(absolute), true, routeFile);
    assert.match(readFileSync(absolute, "utf8"), /export default (async )?function/, routeFile);
  }
});

test("CP10 dashboard pages render gated conversion and negotiation boundaries", () => {
  const files = [
    "src/app/dashboard/offer-conversion/page.tsx",
    "src/app/dashboard/offer-conversion/[dealId]/page.tsx",
    "src/app/dashboard/negotiations/page.tsx",
    "src/app/dashboard/negotiations/[recordId]/page.tsx",
    "src/app/dashboard/contract-ready/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n");
  assert.match(joined, /Controlled offer conversion gate/);
  assert.match(joined, /No contract is generated, accepted, or executed here\./);
  assert.match(joined, /No acceptance, send, or contract action happens here\./);
  assert.match(joined, /External drafting readiness/);
  assert.match(joined, /Automatic acceptance/);
});

test("CP10 dashboard pages expose no forbidden negotiation or contract controls", () => {
  const files = [
    "src/app/dashboard/offer-conversion/page.tsx",
    "src/app/dashboard/offer-conversion/[dealId]/page.tsx",
    "src/app/dashboard/negotiations/page.tsx",
    "src/app/dashboard/negotiations/[recordId]/page.tsx",
    "src/app/dashboard/contract-ready/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send all",
    "auto call",
    "send contract",
    "e-signature",
    "charge card",
    "create stripe customer",
    "submit to title",
    "provider called\" value=\"1",
    "automaticacceptanceallowed: true",
    "contractexecutionallowed: true"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("CP11 dashboard route files exist for title review pages", () => {
  const files = [
    "src/app/dashboard/title-review/page.tsx",
    "src/app/dashboard/title-review/[reviewId]/page.tsx",
    "src/app/dashboard/review-packets/page.tsx"
  ];
  for (const routeFile of files) {
    const absolute = join(root, routeFile);
    assert.equal(existsSync(absolute), true, routeFile);
    assert.match(readFileSync(absolute, "utf8"), /export default (async )?function/, routeFile);
  }
});

test("CP11 dashboard pages render review-only packet preparation boundaries", () => {
  const files = [
    "src/app/dashboard/title-review/page.tsx",
    "src/app/dashboard/title-review/[reviewId]/page.tsx",
    "src/app/dashboard/review-packets/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n");
  assert.match(joined, /Review coordination gate/);
  assert.match(joined, /Draft-only title review packets/);
  assert.match(joined, /does not submit documents, send title-company email, create legal relationships, or execute contracts\./);
  assert.match(joined, /without submission or legal execution\./);
  assert.match(joined, /Closing guarantees/);
});

test("CP11 dashboard pages expose no forbidden title-review controls", () => {
  const files = [
    "src/app/dashboard/title-review/page.tsx",
    "src/app/dashboard/title-review/[reviewId]/page.tsx",
    "src/app/dashboard/review-packets/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send all",
    "auto call",
    "submit to title",
    "submit documents now",
    "wire funds",
    "charge card",
    "create stripe customer",
    "provider called\" value=\"1",
    "contractexecutionallowed: true",
    "documentsubmissionallowed: true"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("CP12 implemented controlled-lane route files exist", () => {
  const files = [
    "src/app/dashboard/communications/page.tsx",
    "src/app/dashboard/communications/[draftId]/page.tsx",
    "src/app/dashboard/communications/dry-runs/page.tsx",
    "src/app/dashboard/communications/approvals/page.tsx",
    "src/app/dashboard/communications/attempts/page.tsx"
  ];
  for (const routeFile of files) {
    const absolute = join(root, routeFile);
    assert.equal(existsSync(absolute), true, routeFile);
    assert.match(readFileSync(absolute, "utf8"), /export default (async )?function/, routeFile);
  }
});

test("CP12 implemented controlled-lane pages render dry-run and approval boundaries", () => {
  const files = [
    "src/app/dashboard/communications/page.tsx",
    "src/app/dashboard/communications/[draftId]/page.tsx",
    "src/app/dashboard/communications/dry-runs/page.tsx",
    "src/app/dashboard/communications/approvals/page.tsx",
    "src/app/dashboard/communications/attempts/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n");
  assert.match(joined, /Owner-approved communication control/);
  assert.match(joined, /Live communication remains blocked unless the unchanged draft, safety result, dry-run receipt, owner approval, live flags, provider readiness, recipient tie, and idempotency gate all clear\./);
  assert.match(joined, /Dry-run does not send/);
  assert.match(joined, /Approval records tied to dry-runs/);
  assert.match(joined, /Blocked and mock-sent attempt log/);
});

test("CP12 implemented controlled-lane pages expose no forbidden live-send controls", () => {
  const files = [
    "src/app/dashboard/communications/page.tsx",
    "src/app/dashboard/communications/[draftId]/page.tsx",
    "src/app/dashboard/communications/dry-runs/page.tsx",
    "src/app/dashboard/communications/approvals/page.tsx",
    "src/app/dashboard/communications/attempts/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of [
    "<button",
    "send all",
    "auto dial",
    "charge card",
    "create stripe customer",
    "store card",
    "bypass enabled",
    "provider called\" value=\"1",
    "bulksendallowed: true",
    "titlesubmissionallowed: true"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("CP9 client command plan pages render plan and billing-readiness boundaries", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/plans/page.tsx",
    "src/app/dashboard/client-command/plans/catalog/page.tsx",
    "src/app/dashboard/client-command/plans/features/page.tsx",
    "src/app/dashboard/client-command/plans/usage/page.tsx",
    "src/app/dashboard/client-command/plans/upgrade-recommendations/page.tsx",
    "src/app/dashboard/client-command/plans/billing-readiness/page.tsx",
    "src/app/dashboard/client-command/plans/subscription-placeholder/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n");
  assert.match(joined, /Plan gate only - no payment has been collected\./);
  assert.match(joined, /Billing readiness only - no Stripe\/customer\/invoice\/subscription action occurred\./);
  assert.match(joined, /Feature access is controlled by plan, readiness, and safety gates\./);
});

test("CP9 client command plan pages expose no forbidden billing controls", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/plans/page.tsx",
    "src/app/dashboard/client-command/plans/catalog/page.tsx",
    "src/app/dashboard/client-command/plans/features/page.tsx",
    "src/app/dashboard/client-command/plans/usage/page.tsx",
    "src/app/dashboard/client-command/plans/upgrade-recommendations/page.tsx",
    "src/app/dashboard/client-command/plans/billing-readiness/page.tsx",
    "src/app/dashboard/client-command/plans/subscription-placeholder/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of ["<button", "collect payment", "activate billing", "create stripe customer", "start subscription", "bill client"]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("CP10 client command communication pages render dry-run and approval boundaries", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/communication/page.tsx",
    "src/app/dashboard/client-command/communication/providers/page.tsx",
    "src/app/dashboard/client-command/communication/readiness/page.tsx",
    "src/app/dashboard/client-command/communication/dry-runs/page.tsx",
    "src/app/dashboard/client-command/communication/approvals/page.tsx",
    "src/app/dashboard/client-command/communication/attempts/page.tsx",
    "src/app/dashboard/client-command/communication/external-references/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n");
  assert.match(joined, /Controlled single-message gate - no bulk campaigns\./);
  assert.match(joined, /Blocked by default unless compliance, plan, approval, and live flags pass\./);
  assert.match(joined, /Dry run does not send a message\./);
  assert.match(joined, /Approval does not send a message\./);
  assert.match(joined, /Live send is single-message, idempotent, and audited\./);
});

test("CP10 client command communication pages expose no forbidden communication controls", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/communication/page.tsx",
    "src/app/dashboard/client-command/communication/providers/page.tsx",
    "src/app/dashboard/client-command/communication/readiness/page.tsx",
    "src/app/dashboard/client-command/communication/dry-runs/page.tsx",
    "src/app/dashboard/client-command/communication/approvals/page.tsx",
    "src/app/dashboard/client-command/communication/attempts/page.tsx",
    "src/app/dashboard/client-command/communication/external-references/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of ["<button", "blast buyers", "start campaign", "auto follow-up", "auto reply", "send bulk", "launch drip", "contact all"]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("CP11 client command billing pages render billing gate boundaries", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/billing/page.tsx",
    "src/app/dashboard/client-command/billing/providers/page.tsx",
    "src/app/dashboard/client-command/billing/customers/page.tsx",
    "src/app/dashboard/client-command/billing/readiness/page.tsx",
    "src/app/dashboard/client-command/billing/dry-runs/page.tsx",
    "src/app/dashboard/client-command/billing/approvals/page.tsx",
    "src/app/dashboard/client-command/billing/attempts/page.tsx",
    "src/app/dashboard/client-command/billing/ledger/page.tsx",
    "src/app/dashboard/client-command/billing/external-references/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n");
  assert.match(joined, /Billing gate only - no payment occurs unless all billing gates pass\./);
  assert.match(joined, /Dry run does not charge a card\./);
  assert.match(joined, /Approval does not charge a card\./);
  assert.match(joined, /No raw card data is stored\./);
  assert.match(joined, /Stripe\/live provider execution is disabled by default\./);
});

test("CP11 client command billing pages expose no forbidden billing execution controls", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/billing/page.tsx",
    "src/app/dashboard/client-command/billing/providers/page.tsx",
    "src/app/dashboard/client-command/billing/customers/page.tsx",
    "src/app/dashboard/client-command/billing/readiness/page.tsx",
    "src/app/dashboard/client-command/billing/dry-runs/page.tsx",
    "src/app/dashboard/client-command/billing/approvals/page.tsx",
    "src/app/dashboard/client-command/billing/attempts/page.tsx",
    "src/app/dashboard/client-command/billing/ledger/page.tsx",
    "src/app/dashboard/client-command/billing/external-references/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of ["<button", "charge now", "refund", "auto subscribe", "auto upgrade", "auto downgrade", "delete customer", "store card", "force payment"]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});

test("CP12 client command pilot pages render pilot/admin support boundaries", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/pilot/page.tsx",
    "src/app/dashboard/client-command/pilot/admin-console/page.tsx",
    "src/app/dashboard/client-command/pilot/support-console/page.tsx",
    "src/app/dashboard/client-command/pilot/programs/page.tsx",
    "src/app/dashboard/client-command/pilot/enrollments/page.tsx",
    "src/app/dashboard/client-command/pilot/health/page.tsx",
    "src/app/dashboard/client-command/pilot/support-tickets/page.tsx",
    "src/app/dashboard/client-command/pilot/escalations/page.tsx",
    "src/app/dashboard/client-command/pilot/launch-checklist/page.tsx",
    "src/app/dashboard/client-command/pilot/risk-review/page.tsx",
    "src/app/dashboard/client-command/pilot/client-updates/page.tsx",
    "src/app/dashboard/client-command/pilot/blocked/page.tsx",
    "src/app/dashboard/client-command/pilot/needs-review/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n");
  assert.match(joined, /Pilot mode does not bypass source gates\./);
  assert.match(joined, /Admin support can review and route issues, but cannot force live actions\./);
  assert.match(joined, /Client-safe updates hide internal governance, provider payloads, and admin notes\./);
  assert.match(joined, /Controlled live posture requires CP9, CP10, and CP11 gates\./);
});

test("CP12 client command pilot pages expose no forbidden override controls", () => {
  const files = [
    "src/app/dashboard/client-command/page.tsx",
    "src/app/dashboard/client-command/pilot/page.tsx",
    "src/app/dashboard/client-command/pilot/admin-console/page.tsx",
    "src/app/dashboard/client-command/pilot/support-console/page.tsx",
    "src/app/dashboard/client-command/pilot/programs/page.tsx",
    "src/app/dashboard/client-command/pilot/enrollments/page.tsx",
    "src/app/dashboard/client-command/pilot/health/page.tsx",
    "src/app/dashboard/client-command/pilot/support-tickets/page.tsx",
    "src/app/dashboard/client-command/pilot/escalations/page.tsx",
    "src/app/dashboard/client-command/pilot/launch-checklist/page.tsx",
    "src/app/dashboard/client-command/pilot/risk-review/page.tsx",
    "src/app/dashboard/client-command/pilot/client-updates/page.tsx",
    "src/app/dashboard/client-command/pilot/blocked/page.tsx",
    "src/app/dashboard/client-command/pilot/needs-review/page.tsx"
  ].map((file) => join(root, file));
  const joined = files.map((file) => readFileSync(file, "utf8").toLowerCase()).join("\n");
  for (const forbidden of ["<button", "force send", "force charge", "override gate", "bypass compliance", "activate live", "execute provider", "delete client data", "auto campaign", "auto billing"]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
});
