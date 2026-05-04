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
  "src/app/dashboard/seller-followups/page.tsx",
  "src/app/dashboard/buyers/page.tsx",
  "src/app/dashboard/buyers/[buyerId]/page.tsx",
  "src/app/dashboard/buyer-matches/page.tsx",
  "src/app/dashboard/compliance/page.tsx",
  "src/app/dashboard/daily-briefing/page.tsx"
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

test("operator-only frontend has no public signup or portals", () => {
  const files = walk(join(root, "src", "app")).filter((file) => file.endsWith(".tsx"));
  const joined = files.map((file) => readFileSync(file, "utf8")).join("\n").toLowerCase();
  assert.equal(joined.includes("/signup"), false);
  assert.equal(joined.includes("buyer portal"), false);
  assert.equal(joined.includes("seller portal"), false);
  assert.equal(joined.includes("client portal"), false);
});
