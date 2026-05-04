import { notFound } from "next/navigation";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  communicationApprovals,
  communicationDrafts,
  communicationDryRunReceipts,
  communicationSendAttempts,
  getCommunicationDraft
} from "@/lib/demo-data";

export function generateStaticParams() {
  return communicationDrafts.map((draft) => ({ draftId: draft.id }));
}

export default function CommunicationDraftDetailPage({ params }: { params: { draftId: string } }) {
  const draft = getCommunicationDraft(params.draftId);
  if (!draft) notFound();
  const dryRuns = communicationDryRunReceipts.filter((receipt) => receipt.draftId === draft.id);
  const approvals = communicationApprovals.filter((approval) => approval.draftId === draft.id);
  const attempts = communicationSendAttempts.filter((attempt) => attempt.draftId === draft.id);
  return (
    <div className="page">
      <PageHeader
        eyebrow={draft.status}
        title={`${draft.id} / ${draft.draftType}`}
        description="Live communication remains blocked unless the unchanged draft, safety result, dry-run receipt, owner approval, live flags, provider readiness, recipient tie, and idempotency gate all clear."
      />
      <div className="metric-grid">
        <div className="metric-card"><span>Safety</span><strong>{draft.safetyPassed ? "passed" : draft.safetyChecked ? "blocked" : "needed"}</strong><small>{draft.riskStatus}</small></div>
        <div className="metric-card"><span>Dry-runs</span><strong>{String(dryRuns.length)}</strong><small>{draft.lastDryRunReceiptId ?? "none"}</small></div>
        <div className="metric-card"><span>Approvals</span><strong>{String(approvals.length)}</strong><small>{draft.ownerApprovalRecorded ? "owner recorded" : "pending"}</small></div>
        <div className="metric-card"><span>Live flags</span><strong>{draft.communicationLiveFlagEnabled ? "draft on" : "draft off"}</strong><small>global off by default</small></div>
      </div>
      <div className="grid-two">
        <Section title="Draft Body">
          <div className="record-list">
            <RecordCard title={draft.subject || "SMS draft"} meta={draft.draftBody} right={<Pill tone="gold">draft</Pill>} />
            <RecordCard title="Recipient tie" meta={`${draft.recipientType} / ${draft.sourceRecordType} ${draft.sourceRecordId}`} />
            <RecordCard title="Provider readiness" meta={draft.providerReadiness ? "ready for mock adapter" : "not ready"} right={<Pill tone={draft.providerReadiness ? "green" : "red"}>{draft.providerReadiness ? "ready" : "blocked"}</Pill>} />
          </div>
        </Section>
        <Section title="Live Send Limits">
          <div className="record-list">
            <RecordCard title="One recipient" meta="Bulk send and campaigns are blocked." right={<Pill tone="red">no bulk</Pill>} />
            <RecordCard title="Buyer blasts" meta="Buyer blast execution remains blocked." right={<Pill tone="red">blocked</Pill>} />
            <RecordCard title="Title submission" meta="Title-company submission is blocked." right={<Pill tone="red">blocked</Pill>} />
            <RecordCard title="Auto follow-up" meta="No auto sequences or uncontrolled outreach." right={<Pill tone="red">blocked</Pill>} />
          </div>
        </Section>
      </div>
      <Section title="Attempts">
        <div className="record-list">
          {attempts.length ? attempts.map((attempt) => (
            <RecordCard key={attempt.id} title={attempt.id} meta={attempt.blockedReasons.length ? attempt.blockedReasons.join(", ") : attempt.attemptStatus} right={<Pill tone={attempt.attemptStatus === "blocked" ? "red" : "green"}>{attempt.attemptStatus}</Pill>} />
          )) : <RecordCard title="No attempts" meta="No live or mock-send attempt recorded." />}
        </div>
      </Section>
    </div>
  );
}
