import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import {
  blockedCommunicationAttempts,
  communicationDrafts,
  communicationDraftsNeedingSafety,
  communicationDryRunsNeedingApproval,
  communicationRiskQueue,
  sentOrMockSentCommunicationAttempts
} from "@/lib/demo-data";

export default function CommunicationsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V5 Controlled Live Communication Gate"
        title="Owner-approved communication control"
        description="Drafts can only move toward a one-off mock/live attempt after safety, dry-run receipt, owner approval, live flags, provider readiness, source tie, and idempotency gates."
      />
      <div className="metric-grid">
        <MetricCard label="Drafts" value={String(communicationDrafts.length)} detail="Seller, buyer, title, owner" />
        <MetricCard label="Need safety" value={String(communicationDraftsNeedingSafety.length)} detail="Safety check required" />
        <MetricCard label="Need approval" value={String(communicationDryRunsNeedingApproval.length)} detail="Dry-run receipts waiting" />
        <MetricCard label="Blocked attempts" value={String(blockedCommunicationAttempts.length)} detail="No provider calls" />
      </div>
      <div className="metric-grid">
        <MetricCard label="Mock-sent" value={String(sentOrMockSentCommunicationAttempts.length)} detail="Adapter placeholders only" />
        <MetricCard label="Risk queue" value={String(communicationRiskQueue.length)} detail="Unsafe or blocked drafts" />
        <MetricCard label="Global live flag" value="off" detail="Default disabled" />
        <MetricCard label="Bulk campaigns" value="0" detail="Not supported" />
      </div>
      <Section title="Communication Draft Queue">
        <table className="data-table">
          <thead>
            <tr>
              <th>Draft</th>
              <th>Type</th>
              <th>Recipient</th>
              <th>Source</th>
              <th>Safety</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {communicationDrafts.map((draft) => (
              <tr key={draft.id}>
                <td><Link href={`/dashboard/communications/${draft.id}`}>{draft.id}</Link><div className="record-meta">{draft.channel}</div></td>
                <td>{draft.draftType}</td>
                <td>{draft.recipientEmailPlaceholder || draft.recipientPhonePlaceholder || "owner"}</td>
                <td>{draft.sourceRecordType}<div className="record-meta">{draft.sourceRecordId}</div></td>
                <td><Pill tone={draft.safetyPassed ? "green" : draft.safetyChecked ? "red" : "gold"}>{draft.safetyChecked ? (draft.safetyPassed ? "passed" : "blocked") : "needed"}</Pill></td>
                <td><Pill tone={draft.status.includes("blocked") ? "red" : "gold"}>{draft.status}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
