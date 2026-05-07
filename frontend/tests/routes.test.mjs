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
    "charge",
    "invoice",
    "activate",
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
    "charge",
    "invoice",
    "activate",
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
