import assert from "node:assert/strict";
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));

const requiredRouteFiles = [
  "src/app/dashboard/page.tsx",
  "src/app/dashboard/command-center/page.tsx",
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
  "src/app/dashboard/buyers/page.tsx",
  "src/app/dashboard/buyers/[buyerId]/page.tsx",
  "src/app/dashboard/buyer-matches/page.tsx",
  "src/app/dashboard/compliance/page.tsx",
  "src/app/dashboard/daily-briefing/page.tsx",
  "src/app/buyer-portal/page.tsx",
  "src/app/buyer-portal/deals/page.tsx",
  "src/app/buyer-portal/deals/[dealId]/page.tsx",
  "src/app/buyer-portal/profile/page.tsx",
  "src/app/buyer-portal/watchlist/page.tsx"
];

function walk(dir) {
  return readdirSync(dir).flatMap((entry) => {
    const file = join(dir, entry);
    return statSync(file).isDirectory() ? walk(file) : [file];
  });
}

test("dashboard route files exist and render a page component", () => {
  for (const routeFile of requiredRouteFiles) {
    const absolute = join(root, routeFile);
    assert.equal(existsSync(absolute), true, routeFile);
    const source = readFileSync(absolute, "utf8");
    assert.match(source, /export default function/);
    assert.match(source, /return \(/);
  }
});

test("operator-only frontend has no public signup or seller/client portals", () => {
  const files = walk(join(root, "src", "app")).filter((file) => file.endsWith(".tsx"));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n").toLowerCase();
  assert.equal(joined.includes("/signup"), false);
  assert.equal(joined.includes("seller portal"), false);
  assert.equal(joined.includes("client portal"), false);
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
    "wholesale prime",
    "compliance risk"
  ]) {
    assert.equal(joined.includes(forbidden), false, forbidden);
  }
  assert.equal(joined.includes("contract executionallowed: true"), false);
});
