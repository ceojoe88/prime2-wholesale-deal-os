import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientBillingApprovals,
  clientBillingAttempts,
  clientBillingCustomerProfiles,
  clientBillingLedgerEntries,
  clientBillingLiveFlags,
  clientBillingProviderProfiles,
  clientBillingReadinessChecks,
  clientBillingReadinessRecords,
  clientCheckoutDryRunReceipts,
  clientSubscriptionPlaceholders,
  formatCurrency
} from "@/lib/demo-data";

const cp11Guardrails = [
  {
    title: "Billing gate",
    meta: "Every billing attempt stays blocked until the full path is clear.",
    detail: "Billing gate only - no payment occurs unless all billing gates pass.",
    tone: "gold" as const
  },
  {
    title: "Dry run",
    meta: "Checkout previews remain non-monetary.",
    detail: "Dry run does not charge a card.",
    tone: "green" as const
  },
  {
    title: "Approval",
    meta: "Human signoff stays separate from collection.",
    detail: "Approval does not charge a card.",
    tone: "green" as const
  },
  {
    title: "Card handling",
    meta: "Workspace billing records stay client-safe.",
    detail: "No raw card data is stored.",
    tone: "red" as const
  },
  {
    title: "Provider posture",
    meta: "Live execution remains disabled across the workspace.",
    detail: "Stripe/live provider execution is disabled by default.",
    tone: "red" as const
  }
];

export default function ClientCommandBillingPage() {
  const readinessRecord = clientBillingReadinessRecords[0];
  const subscription = clientSubscriptionPlaceholders[0];
  const blockedChecks = clientBillingReadinessChecks.filter((check) => check.readinessStatus !== "ready");

  return (
    <div className="page">
      <PageHeader
        eyebrow="CP11 Billing"
        title="Controlled billing gate"
        description="Client-safe billing readiness, checkout previews, approval records, and blocked provider lanes."
      />

      <div className="metric-grid">
        <MetricCard label="Readiness records" value={String(clientBillingReadinessRecords.length)} detail={readinessRecord?.readinessStatus ?? "pending"} />
        <MetricCard label="Blocked checks" value={String(blockedChecks.length)} detail="Plan and live flags still block execution" />
        <MetricCard label="Dry runs" value={String(clientCheckoutDryRunReceipts.length)} detail="Preview-only checkout shells" />
        <MetricCard label="Ledger entries" value={String(clientBillingLedgerEntries.length)} detail="Client-safe attempt history" />
      </div>

      <Section title="Billing Guardrails">
        <div className="record-list">
          {cp11Guardrails.map((item) => (
            <RecordCard key={item.title} title={item.title} meta={item.meta} right={<Pill tone={item.tone}>guarded</Pill>}>
              <p>{item.detail}</p>
            </RecordCard>
          ))}
        </div>
      </Section>

      <Section title="Workspace Billing Gate">
        <div className="grid-two">
          <RecordCard title="Plan placeholder" meta={subscription?.clientSafeSummary ?? "No plan placeholder is recorded."} right={<Pill tone="gold">{subscription?.placeholderStatus ?? "draft"}</Pill>}>
            <div className="tag-row">
              <Pill tone="green">{formatCurrency(subscription?.monthlyPricePlaceholder ?? 0)} monthly</Pill>
              <Pill tone="green">{formatCurrency(subscription?.setupFeePlaceholder ?? 0)} setup</Pill>
            </div>
          </RecordCard>
          {clientBillingProviderProfiles.map((profile) => (
            <RecordCard key={profile.id} title={profile.providerName} meta={profile.clientSafeSummary} right={<Pill tone={profile.enabled ? "green" : "gold"}>{profile.providerMode}</Pill>}>
              <div className="tag-row">
                <Pill tone="green">{profile.supportsPaymentLinks ? "payment links" : "payment links off"}</Pill>
                <Pill tone="green">{profile.supportsSubscriptions ? "subscriptions" : "subscriptions off"}</Pill>
              </div>
            </RecordCard>
          ))}
          {clientBillingCustomerProfiles.map((profile) => (
            <RecordCard key={profile.id} title={profile.customerName} meta={profile.clientSafeSummary} right={<Pill tone={profile.rawCardDataPresent ? "red" : "green"}>{profile.rawCardDataPresent ? "review" : "clear"}</Pill>}>
              <div className="tag-row">
                <Pill tone="green">{profile.billingContactName}</Pill>
                <Pill tone="green">{profile.billingEmail}</Pill>
              </div>
            </RecordCard>
          ))}
          {clientBillingLiveFlags.map((flag) => (
            <RecordCard key={flag.id} title="Live billing flags" meta="Global, workspace, provider, payment-link, and subscription flags must all be true." right={<Pill tone="red">locked</Pill>}>
              <div className="tag-row">
                <Pill tone={flag.globalBillingLiveEnabled ? "green" : "red"}>{flag.globalBillingLiveEnabled ? "global on" : "global off"}</Pill>
                <Pill tone={flag.workspaceBillingLiveEnabled ? "green" : "red"}>{flag.workspaceBillingLiveEnabled ? "workspace on" : "workspace off"}</Pill>
                <Pill tone={flag.providerBillingLiveEnabled ? "green" : "red"}>{flag.providerBillingLiveEnabled ? "provider on" : "provider off"}</Pill>
                <Pill tone={flag.paymentLinkLiveEnabled ? "green" : "red"}>{flag.paymentLinkLiveEnabled ? "link on" : "link off"}</Pill>
                <Pill tone={flag.subscriptionLiveEnabled ? "green" : "red"}>{flag.subscriptionLiveEnabled ? "subscription on" : "subscription off"}</Pill>
              </div>
            </RecordCard>
          ))}
        </div>
      </Section>

      <Section title="Readiness and Attempt Ledger">
        <div className="grid-two">
          {clientBillingReadinessChecks.map((check) => (
            <RecordCard key={check.id} title="Billing readiness check" meta={check.blockReasons.join(", ") || "Ready for review."} right={<Pill tone={check.readinessStatus === "ready" ? "green" : "gold"}>{check.readinessStatus}</Pill>}>
              <p>{readinessRecord?.notesSummary ?? "Billing readiness placeholder exists for future paid-pilot review only."}</p>
            </RecordCard>
          ))}
          {clientCheckoutDryRunReceipts.map((receipt) => (
            <RecordCard key={receipt.id} title={receipt.attemptType.replaceAll("_", " ")} meta={receipt.dryRunSummary} right={<Pill tone="green">{receipt.status}</Pill>}>
              <p>{formatCurrency(receipt.amountPlaceholder)} placeholder amount</p>
            </RecordCard>
          ))}
          {clientBillingApprovals.map((approval) => (
            <RecordCard key={approval.id} title={approval.approvedBy} meta={approval.reasonSummary} right={<Pill tone="green">{approval.approvalStatus}</Pill>}>
              <p>Approval record: {approval.readinessCheckId}</p>
            </RecordCard>
          ))}
          {clientBillingAttempts.map((attempt) => (
            <RecordCard key={attempt.id} title={attempt.attemptType.replaceAll("_", " ")} meta={attempt.requestSummary} right={<Pill tone={attempt.attemptStatus === "blocked" ? "red" : "green"}>{attempt.attemptStatus}</Pill>}>
              <div className="tag-row">
                <Pill tone="green">{attempt.providerMode}</Pill>
                <Pill tone="green">{attempt.idempotencyKey}</Pill>
                {attempt.blockReasons.map((reason) => (
                  <Pill key={reason} tone="red">
                    {reason}
                  </Pill>
                ))}
              </div>
            </RecordCard>
          ))}
          {clientBillingLedgerEntries.map((entry) => (
            <RecordCard key={entry.id} title={entry.entryType.replaceAll("_", " ")} meta={entry.summary} right={<Pill tone={entry.status === "blocked" ? "gold" : "green"}>{entry.status}</Pill>}>
              <p>
                {formatCurrency(entry.amountPlaceholder)} {entry.currency}
              </p>
            </RecordCard>
          ))}
        </div>
      </Section>

      <Section title="Command Links">
        <div className="grid-three">
          <RecordCard title="Plans" meta="CP9 plan assignment and upgrade gates" right={<Link href="/dashboard/client-command/plans">Open</Link>} />
          <RecordCard title="Communication" meta="CP10 single-message live gate" right={<Link href="/dashboard/client-command/communication">Open</Link>} />
          <RecordCard title="Pilot" meta="CP12 pilot routing and updates" right={<Link href="/dashboard/client-command/pilot">Open</Link>} />
          <RecordCard title="Workspaces" meta="Workspace readiness context" right={<Link href="/dashboard/client-command/workspaces">Open</Link>} />
          <RecordCard title="Onboarding" meta="CP8 readiness and blockers" right={<Link href="/dashboard/client-command/onboarding">Open</Link>} />
          <RecordCard title="Reports" meta="Client-visible weekly updates" right={<Link href="/dashboard/client-command/reports">Open</Link>} />
        </div>
      </Section>
    </div>
  );
}
