import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientFeatureGateEvaluations,
  clientPlanAssignments,
  clientPlanCatalogEntries,
  clientPlanFeatures,
  clientPlanLimits,
  clientPlanUpgradeRecommendations,
  clientSeatUsageRecords,
  clientSubscriptionPlaceholders,
  clientUsageCounters,
  formatCurrency
} from "@/lib/demo-data";

const cp9Guardrails = [
  {
    title: "Plan gate",
    meta: "Current workspace plan stays in placeholder mode.",
    detail: "Plan gate only - no payment has been collected.",
    tone: "gold" as const
  },
  {
    title: "Billing readiness boundary",
    meta: "Provider setup is still informational.",
    detail: "Billing readiness only - no Stripe/customer/invoice/subscription action occurred.",
    tone: "red" as const
  },
  {
    title: "Feature access policy",
    meta: "Workspace expansion stays behind explicit gates.",
    detail: "Feature access is controlled by plan, readiness, and safety gates.",
    tone: "green" as const
  }
];

export default function ClientCommandPlansPage() {
  const assignment = clientPlanAssignments[0];
  const subscription = clientSubscriptionPlaceholders[0];
  const usage = clientUsageCounters[0];
  const upgrade = clientPlanUpgradeRecommendations[0];
  const currentLimit = clientPlanLimits.find((limit) => limit.planCode === assignment?.planCode);
  const seatCount = clientSeatUsageRecords.filter((seat) => seat.workspaceId === assignment?.workspaceId && seat.countsAgainstLimit).length;
  const blockedGates = clientFeatureGateEvaluations.filter((gate) => gate.gateStatus !== "allowed");

  return (
    <div className="page">
      <PageHeader
        eyebrow="CP9 Plans"
        title="Plan catalog and readiness gates"
        description="Client-safe plan visibility for workspace assignment, limits, and controlled feature access."
      />

      <div className="metric-grid">
        <MetricCard label="Catalog plans" value={String(clientPlanCatalogEntries.length)} detail="Client-safe plan shells" />
        <MetricCard label="Assigned plan" value={assignment?.planName ?? "Unassigned"} detail={assignment?.assignmentStatus ?? "pending"} />
        <MetricCard label="Blocked gates" value={String(blockedGates.length)} detail="Upgrade or readiness follow-up needed" />
        <MetricCard
          label="Manual drafts"
          value={currentLimit ? `${usage?.manualDraftsCount ?? 0}/${currentLimit.maxManualDrafts}` : String(usage?.manualDraftsCount ?? 0)}
          detail="Current plan allowance"
        />
      </div>

      <Section title="Plan Guardrails">
        <div className="grid-three">
          {cp9Guardrails.map((item) => (
            <RecordCard key={item.title} title={item.title} meta={item.meta} right={<Pill tone={item.tone}>locked</Pill>}>
              <p>{item.detail}</p>
            </RecordCard>
          ))}
        </div>
      </Section>

      <Section title="Workspace Plan">
        <div className="grid-two">
          <RecordCard title={`${assignment?.planName ?? "Unknown"} workspace plan`} meta={assignment?.clientSafeSummary ?? "No workspace plan has been assigned yet."} right={<Pill tone="green">{assignment?.assignmentStatus ?? "pending"}</Pill>}>
            <div className="tag-row">
              <Pill tone="gold">{subscription?.placeholderStatus ?? "draft"}</Pill>
              <Pill tone="green">{currentLimit ? `${seatCount}/${currentLimit.maxUsers} seats` : "seat cap pending"}</Pill>
              <Pill tone="green">{currentLimit ? `${usage?.buyersCount ?? 0}/${currentLimit.maxBuyers} buyers` : "buyer cap pending"}</Pill>
            </div>
          </RecordCard>
          <RecordCard
            title="Subscription placeholder"
            meta={subscription?.billingContactEmail ?? "No billing contact recorded."}
            right={<Pill tone="gold">{subscription?.planCode ?? "draft"}</Pill>}
          >
            <p>{subscription?.clientSafeSummary ?? "Plan gate only - no payment has been collected."}</p>
            <div className="tag-row">
              <Pill tone="green">{formatCurrency(subscription?.monthlyPricePlaceholder ?? 0)} monthly</Pill>
              <Pill tone="green">{formatCurrency(subscription?.setupFeePlaceholder ?? 0)} setup</Pill>
            </div>
          </RecordCard>
          <RecordCard title="Upgrade recommendation" meta={upgrade?.reasonSummary ?? "No upgrade recommendation is active."} right={<Pill tone="gold">{upgrade?.recommendedPlanCode ?? "none"}</Pill>}>
            <p>{upgrade?.clientSafeSummary ?? "Feature access is controlled by plan, readiness, and safety gates."}</p>
          </RecordCard>
          <RecordCard title="Current plan limits" meta="Usage stays visible without unlocking live billing." right={<Pill tone="green">{assignment?.planCode ?? "unknown"}</Pill>}>
            <div className="tag-row">
              <Pill tone="green">{currentLimit ? `${usage?.usersCount ?? 0}/${currentLimit.maxUsers} users` : "users pending"}</Pill>
              <Pill tone="green">{currentLimit ? `${usage?.leadsCount ?? 0}/${currentLimit.maxLeads} leads` : "leads pending"}</Pill>
              <Pill tone="green">{currentLimit ? `${usage?.weeklyReportsCount ?? 0}/${currentLimit.maxWeeklyReports} reports` : "reports pending"}</Pill>
            </div>
          </RecordCard>
        </div>
      </Section>

      <Section title="Feature Gates">
        <div className="record-list">
          {clientFeatureGateEvaluations.map((gate) => (
            <RecordCard
              key={gate.id}
              title={gate.featureKey.replaceAll("_", " ")}
              meta={gate.reasonSummary}
              right={<Pill tone={gate.gateStatus === "allowed" ? "green" : "gold"}>{gate.gateStatus}</Pill>}
            >
              <div className="tag-row">
                <Pill tone="green">{gate.requiredUpgradePlan ?? "current plan"}</Pill>
                <Pill tone="red">{gate.noLiveAction ? "no live action" : "review"}</Pill>
              </div>
            </RecordCard>
          ))}
        </div>
      </Section>

      <Section title="Plan Catalog">
        <div className="record-list">
          {clientPlanCatalogEntries.map((plan) => {
            const featureSummary = clientPlanFeatures.filter(
              (feature) => feature.planCode === plan.planCode && ["live_communication", "billing", "admin_support", "pilot_mode"].includes(feature.featureKey)
            );
            return (
              <RecordCard
                key={plan.id}
                title={plan.planName}
                meta={plan.clientSafeSummary}
                right={<Pill tone={plan.isPublic ? "green" : "gold"}>{plan.isPublic ? "public" : "private"}</Pill>}
              >
                <div className="tag-row">
                  <Pill tone="green">{formatCurrency(plan.monthlyPricePlaceholder)} monthly</Pill>
                  <Pill tone="green">{formatCurrency(plan.setupFeePlaceholder)} setup</Pill>
                  {featureSummary.map((feature) => (
                    <Pill key={feature.id} tone={feature.allowed ? "green" : "gold"}>
                      {feature.featureKey.replaceAll("_", " ")}
                    </Pill>
                  ))}
                </div>
              </RecordCard>
            );
          })}
        </div>
      </Section>

      <Section title="Command Links">
        <div className="grid-three">
          <RecordCard title="Catalog" meta="Public and private plan placeholders" right={<Link href="/dashboard/client-command/plans/catalog">Open</Link>} />
          <RecordCard title="Features" meta="Assigned feature gates and blocked access" right={<Link href="/dashboard/client-command/plans/features">Open</Link>} />
          <RecordCard title="Usage" meta="Current plan usage and seat posture" right={<Link href="/dashboard/client-command/plans/usage">Open</Link>} />
          <RecordCard title="Billing Readiness" meta="Billing readiness only - no Stripe/customer/invoice/subscription action occurred." right={<Link href="/dashboard/client-command/plans/billing-readiness">Open</Link>} />
          <RecordCard title="Subscription Placeholder" meta="Plan gate only - no payment has been collected." right={<Link href="/dashboard/client-command/plans/subscription-placeholder">Open</Link>} />
          <RecordCard title="Upgrade Recommendations" meta="Feature access is controlled by plan, readiness, and safety gates." right={<Link href="/dashboard/client-command/plans/upgrade-recommendations">Open</Link>} />
          <RecordCard title="Communication Gate" meta="CP10 controlled live communication" right={<Link href="/dashboard/client-command/communication">Open</Link>} />
          <RecordCard title="Billing Gate" meta="CP11 billing live-readiness controls" right={<Link href="/dashboard/client-command/billing">Open</Link>} />
          <RecordCard title="Pilot Mode" meta="CP12 pilot support and client-safe updates" right={<Link href="/dashboard/client-command/pilot">Open</Link>} />
          <RecordCard title="Workspaces" meta="Workspace setup and readiness" right={<Link href="/dashboard/client-command/workspaces">Open</Link>} />
          <RecordCard title="Onboarding" meta="CP8 setup and activation context" right={<Link href="/dashboard/client-command/onboarding">Open</Link>} />
          <RecordCard title="Compliance" meta="CP6 consent and approval gates" right={<Link href="/dashboard/client-command/compliance">Open</Link>} />
        </div>
      </Section>
    </div>
  );
}
