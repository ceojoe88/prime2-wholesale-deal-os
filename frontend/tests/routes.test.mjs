import assert from "node:assert/strict";
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));

const requiredRouteFiles = [
  "src/app/dashboard/page.tsx",
  "src/app/dashboard/command-center/page.tsx",
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
  "src/app/dashboard/audit-exports/page.tsx",
  "src/app/dashboard/audit-exports/[exportId]/page.tsx",
  "src/app/dashboard/evidence-attachments/page.tsx",
  "src/app/dashboard/provider-readiness/page.tsx",
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
  "src/app/seller-portal/messages/page.tsx"
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

test("Prime 2 identity is used internally and old overseer name is limited to product title", () => {
  const sourceFiles = walk(join(root, "src")).filter((file) =>
    [".ts", ".tsx"].some((extension) => file.endsWith(extension))
  );
  const oldNameFiles = sourceFiles
    .filter((file) => readFileSync(file, "utf8").includes("Wholesale Prime"))
    .map(relativeFromRoot);
  assert.deepEqual(oldNameFiles, ["src/app/layout.tsx"]);

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
