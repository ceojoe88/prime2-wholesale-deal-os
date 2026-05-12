import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientCommunicationDryRunReceipts,
  clientCommunicationLiveFlags,
  clientCommunicationLiveReadinessChecks,
  clientCommunicationProviderProfiles,
  clientCommunicationSendApprovals,
  clientCommunicationSendAttempts,
  clientFeatureGateEvaluations
} from "@/lib/demo-data";

const cp10Guardrails = [
  {
    title: "Single-message gate",
    meta: "Outbound communication stays scoped to one record at a time.",
    detail: "Controlled single-message gate - no bulk campaigns.",
    tone: "gold" as const
  },
  {
    title: "Default block posture",
    meta: "Every live lane remains off until the full path is clear.",
    detail: "Blocked by default unless compliance, plan, approval, and live flags pass.",
    tone: "red" as const
  },
  {
    title: "Dry run",
    meta: "Message content can be reviewed without outbound delivery.",
    detail: "Dry run does not send a message.",
    tone: "green" as const
  },
  {
    title: "Approval",
    meta: "Human signoff stays separate from delivery.",
    detail: "Approval does not send a message.",
    tone: "green" as const
  },
  {
    title: "Audited live lane",
    meta: "Any future live path must stay traceable and repeat-safe.",
    detail: "Live send is single-message, idempotent, and audited.",
    tone: "gold" as const
  }
];

export default function ClientCommandCommunicationPage() {
  const blockedChecks = clientCommunicationLiveReadinessChecks.filter((check) => check.readinessStatus !== "ready");
  const livePlanGate = clientFeatureGateEvaluations.find((gate) => gate.featureKey === "live_communication");

  return (
    <div className="page">
      <PageHeader
        eyebrow="CP10 Communication"
        title="Controlled live communication gate"
        description="Client-safe readiness, dry-run review, approvals, and audited single-recipient communication attempts."
      />

      <div className="metric-grid">
        <MetricCard label="Provider profiles" value={String(clientCommunicationProviderProfiles.length)} detail="Mock communication lanes only" />
        <MetricCard label="Blocked checks" value={String(blockedChecks.length)} detail="Live flags still disabled" />
        <MetricCard label="Dry runs" value={String(clientCommunicationDryRunReceipts.length)} detail="Preview-only delivery checks" />
        <MetricCard label="Approvals" value={String(clientCommunicationSendApprovals.length)} detail="Human signoff records" />
      </div>

      <Section title="Communication Guardrails">
        <div className="record-list">
          {cp10Guardrails.map((item) => (
            <RecordCard key={item.title} title={item.title} meta={item.meta} right={<Pill tone={item.tone}>guarded</Pill>}>
              <p>{item.detail}</p>
            </RecordCard>
          ))}
        </div>
      </Section>

      <Section title="Live Gate Snapshot">
        <div className="grid-two">
          {clientCommunicationProviderProfiles.map((profile) => (
            <RecordCard key={profile.id} title={profile.providerName} meta={profile.clientSafeSummary} right={<Pill tone={profile.enabled ? "green" : "gold"}>{profile.providerMode}</Pill>}>
              <div className="tag-row">
                <Pill tone="green">{profile.channel}</Pill>
                <Pill tone="red">no live send</Pill>
              </div>
            </RecordCard>
          ))}
          {clientCommunicationLiveFlags.map((flag) => (
            <RecordCard key={flag.id} title="Live flags" meta="Global, workspace, provider, and channel flags must all be true." right={<Pill tone="red">locked</Pill>}>
              <div className="tag-row">
                <Pill tone={flag.globalCommunicationLiveEnabled ? "green" : "red"}>{flag.globalCommunicationLiveEnabled ? "global on" : "global off"}</Pill>
                <Pill tone={flag.workspaceCommunicationLiveEnabled ? "green" : "red"}>{flag.workspaceCommunicationLiveEnabled ? "workspace on" : "workspace off"}</Pill>
                <Pill tone={flag.providerLiveEnabled ? "green" : "red"}>{flag.providerLiveEnabled ? "provider on" : "provider off"}</Pill>
                <Pill tone={flag.channelLiveEnabled ? "green" : "red"}>{flag.channelLiveEnabled ? "channel on" : "channel off"}</Pill>
              </div>
            </RecordCard>
          ))}
          <RecordCard title="Plan gate snapshot" meta={livePlanGate?.reasonSummary ?? "No live communication gate has been recorded."} right={<Pill tone={livePlanGate?.gateStatus === "allowed" ? "green" : "gold"}>{livePlanGate?.gateStatus ?? "pending"}</Pill>}>
            <p>{livePlanGate?.requiredUpgradePlan ? `Upgrade target: ${livePlanGate.requiredUpgradePlan}` : "Current plan can proceed only after downstream gates clear."}</p>
          </RecordCard>
        </div>
      </Section>

      <Section title="Readiness Queue">
        <div className="record-list">
          {clientCommunicationLiveReadinessChecks.map((check) => (
            <RecordCard key={check.id} title={check.sourceDraftType.replaceAll("_", " ")} meta={check.blockReasons.join(", ") || "Ready for review."} right={<Pill tone={check.readinessStatus === "ready" ? "green" : "gold"}>{check.readinessStatus}</Pill>}>
              <p>Idempotency key: {check.idempotencyKey}</p>
              <div className="tag-row">
                <Pill tone={check.cp6StatusSnapshot === "safe_for_manual_use" ? "green" : "gold"}>{check.cp6StatusSnapshot}</Pill>
                <Pill tone={check.cp9GateSnapshot === "allowed" ? "green" : "gold"}>{check.cp9GateSnapshot}</Pill>
                <Pill tone={check.dryRunPresent ? "green" : "gold"}>{check.dryRunPresent ? "dry run present" : "dry run needed"}</Pill>
                <Pill tone={check.approvalPresent ? "green" : "gold"}>{check.approvalPresent ? "approval present" : "approval needed"}</Pill>
              </div>
            </RecordCard>
          ))}
        </div>
      </Section>

      <Section title="Dry Run and Attempt Ledger">
        <div className="grid-two">
          {clientCommunicationDryRunReceipts.map((receipt) => (
            <RecordCard key={receipt.id} title={receipt.sourceDraftType.replaceAll("_", " ")} meta={receipt.dryRunSummary} right={<Pill tone="green">{receipt.status}</Pill>}>
              <p>{receipt.contentHash}</p>
            </RecordCard>
          ))}
          {clientCommunicationSendApprovals.map((approval) => (
            <RecordCard key={approval.id} title={approval.approvedBy} meta={approval.reasonSummary} right={<Pill tone="green">{approval.approvalStatus}</Pill>}>
              <p>Approval record: {approval.readinessCheckId}</p>
            </RecordCard>
          ))}
          {clientCommunicationSendAttempts.map((attempt) => (
            <RecordCard key={attempt.id} title={attempt.sourceDraftType.replaceAll("_", " ")} meta={attempt.requestSummary} right={<Pill tone={attempt.attemptStatus === "blocked" ? "red" : "green"}>{attempt.attemptStatus}</Pill>}>
              <p>Live send is single-message, idempotent, and audited.</p>
              <div className="tag-row">
                <Pill tone="green">{attempt.channel}</Pill>
                <Pill tone="green">{attempt.idempotencyKey}</Pill>
                {attempt.blockReasons.map((reason) => (
                  <Pill key={reason} tone="red">
                    {reason}
                  </Pill>
                ))}
              </div>
            </RecordCard>
          ))}
        </div>
      </Section>

      <Section title="Command Links">
        <div className="grid-three">
          <RecordCard title="Providers" meta="Provider profiles stay mock or test by default" right={<Link href="/dashboard/client-command/communication/providers">Open</Link>} />
          <RecordCard title="Readiness" meta="Blocked by default unless compliance, plan, approval, and live flags pass." right={<Link href="/dashboard/client-command/communication/readiness">Open</Link>} />
          <RecordCard title="Dry Runs" meta="Dry run does not send a message." right={<Link href="/dashboard/client-command/communication/dry-runs">Open</Link>} />
          <RecordCard title="Approvals" meta="Approval does not send a message." right={<Link href="/dashboard/client-command/communication/approvals">Open</Link>} />
          <RecordCard title="Attempts" meta="Live send is single-message, idempotent, and audited." right={<Link href="/dashboard/client-command/communication/attempts">Open</Link>} />
          <RecordCard title="External References" meta="Client-safe delivery references only" right={<Link href="/dashboard/client-command/communication/external-references">Open</Link>} />
          <RecordCard title="Plans" meta="CP9 plan assignment and feature gates" right={<Link href="/dashboard/client-command/plans">Open</Link>} />
          <RecordCard title="Billing" meta="CP11 billing live-readiness controls" right={<Link href="/dashboard/client-command/billing">Open</Link>} />
          <RecordCard title="Pilot" meta="CP12 pilot support and updates" right={<Link href="/dashboard/client-command/pilot">Open</Link>} />
          <RecordCard title="Compliance" meta="CP6 consent and safe-contact review" right={<Link href="/dashboard/client-command/compliance">Open</Link>} />
          <RecordCard title="Leads" meta="Lead pages still carry CP2-CP6 context" right={<Link href="/dashboard/client-command/leads">Open</Link>} />
          <RecordCard title="Disposition" meta="Buyer-side draft context" right={<Link href="/dashboard/client-command/disposition">Open</Link>} />
        </div>
      </Section>
    </div>
  );
}
