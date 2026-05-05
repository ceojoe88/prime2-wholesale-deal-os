import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  approvedAutoExecutionRules,
  approvedTemplateLibrary,
  autoExecutionAttempts,
  autoExecutionBlockedAttempts,
  autoExecutionDryRunBlocks,
  autoExecutionSafetyCards,
  autoExecutionAuditTrail
} from "@/lib/demo-data";

export default function AutoExecutionPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V13 Controlled Auto-Execution"
        title="Controlled auto-execution gate"
        description="Narrow repeatable actions require an approved rule, approved template, safety check, dry-run, approval, live flags, idempotency, and audit trail."
      />

      <div className="metric-grid">
        <MetricCard label="Approved rules" value={String(approvedAutoExecutionRules.length)} detail="Rule and owner approval required" />
        <MetricCard label="Approved templates" value={String(approvedTemplateLibrary.length)} detail="Safety-checked library" />
        <MetricCard label="Attempts" value={String(autoExecutionAttempts.length)} detail="Prepared, mock-sent, or blocked" />
        <MetricCard label="Audit records" value={String(autoExecutionAuditTrail.length)} detail="Every attempt recorded" />
      </div>

      <Section title="Safety Boundaries">
        <div className="grid-three">
          {autoExecutionSafetyCards.map((card) => (
            <RecordCard key={card.label} title={card.label} meta={card.detail} right={<Pill tone={card.value === "off" ? "red" : "green"}>{card.value}</Pill>} />
          ))}
        </div>
      </Section>

      <div className="grid-two">
        <Section title="Conditional Workflow">
          <div className="record-list">
            <RecordCard title="Trigger to template" meta="Source event must match an approved rule and approved template." right={<Pill tone="green">match</Pill>} />
            <RecordCard title="V5/V13 gate stack" meta="Live send requires safety, dry-run receipt, owner approval, live flags, provider readiness, and idempotency." right={<Pill tone="gold">gated</Pill>} />
            <RecordCard title="Single attempt" meta="One rule, one template, one recipient, one source record, one audit trail." right={<Pill tone="red">no bulk</Pill>} />
          </div>
        </Section>
        <Section title="Current Blocks">
          <div className="record-list">
            <RecordCard title="Blocked attempts" meta={`${autoExecutionBlockedAttempts.length} unsafe or non-compliant attempts`} right={<Pill tone="red">blocked</Pill>} />
            <RecordCard title="Dry-run blocks" meta={`${autoExecutionDryRunBlocks.length} dry-run failed safety`} right={<Pill tone="red">review</Pill>} />
            <RecordCard title="Provider mode" meta="Mock/dry-run only in this local OS." right={<Pill>mock</Pill>} />
          </div>
        </Section>
      </div>

      <Section title="Auto-Execution Routes">
        <div className="grid-three">
          <RecordCard title="Rules" meta="Approved action rules" right={<Link href="/dashboard/auto-execution/rules">Open</Link>} />
          <RecordCard title="Templates" meta="Approved template library" right={<Link href="/dashboard/auto-execution/templates">Open</Link>} />
          <RecordCard title="Dry-runs" meta="Safety receipts" right={<Link href="/dashboard/auto-execution/dry-runs">Open</Link>} />
          <RecordCard title="Attempts" meta="Execution attempts" right={<Link href="/dashboard/auto-execution/attempts">Open</Link>} />
          <RecordCard title="Audit" meta="Immutable audit trail" right={<Link href="/dashboard/auto-execution/audit">Open</Link>} />
        </div>
      </Section>
    </div>
  );
}
