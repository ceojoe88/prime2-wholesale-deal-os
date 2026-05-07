import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientCommunicationApprovalGates,
  clientComplianceReadinessPlaceholders,
  clientSafeContactStatuses
} from "@/lib/demo-data";

export default function ClientCommandCompliancePage() {
  const blocked = clientSafeContactStatuses.filter((status) => status.status === "blocked");
  const needsReview = clientSafeContactStatuses.filter((status) => ["needs_review", "missing_consent"].includes(status.status));
  const safeManualUse = clientSafeContactStatuses.filter((status) => status.status === "safe_for_manual_use");

  return (
    <div className="page">
      <PageHeader
        eyebrow="CP6 Compliance"
        title="Compliance Manager"
        description="Consent, opt-out, safe manual-use status, placeholders, and communication approval gates. No provider checks or live communication occur here."
      />

      <div className="metric-grid">
        <MetricCard label="Blocked contacts" value={String(blocked.length)} detail="Opt-out or blocked manual-use status" />
        <MetricCard label="Needs review" value={String(needsReview.length)} detail="Consent or channel review required" />
        <MetricCard label="Safe manual use" value={String(safeManualUse.length)} detail="Readiness check only" />
        <MetricCard label="Manual-use gates" value={String(clientCommunicationApprovalGates.length)} detail={`${clientComplianceReadinessPlaceholders.length} placeholders tracked`} />
      </div>

      <Section title="Compliance Manager Card">
        <div className="grid-two">
          <RecordCard title="Safe Contact Status" meta="Readiness check only - no provider check or live communication occurred." right={<Pill tone="gold">No Live Send</Pill>} />
          <RecordCard title="Communication Approval Gate" meta="Manual-use approval only - no message has been sent." right={<Pill tone="gold">Manual Use Only</Pill>} />
        </div>
      </Section>

      <Section title="Command Links">
        <div className="grid-three">
          <RecordCard title="Consent" meta="Manual consent records" right={<Link href="/dashboard/client-command/compliance/consent">Open</Link>} />
          <RecordCard title="Opt-Outs" meta="Manual opt-out records" right={<Link href="/dashboard/client-command/compliance/opt-outs">Open</Link>} />
          <RecordCard title="Blocked" meta="Blocked contact statuses" right={<Link href="/dashboard/client-command/compliance/blocked">Open</Link>} />
          <RecordCard title="Needs Review" meta="Consent or channel review queue" right={<Link href="/dashboard/client-command/compliance/needs-review">Open</Link>} />
          <RecordCard title="Safe Manual Use" meta="Cleared for manual-use drafts only" right={<Link href="/dashboard/client-command/compliance/safe-manual-use">Open</Link>} />
          <RecordCard title="Gates" meta="Communication approval gates" right={<Link href="/dashboard/client-command/compliance/gates">Open</Link>} />
        </div>
      </Section>
    </div>
  );
}
