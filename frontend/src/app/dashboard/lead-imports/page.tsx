import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  approvedLeadImportRows,
  blockedLeadImportRows,
  leadImportBatches,
  leadImportRows,
  v19SafetyCards
} from "@/lib/demo-data";

export default function LeadImportsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V19 Real Lead Import"
        title="Lead import control"
        description="CSV import batches are previewed, normalized, deduped, QA-scored, and committed only by approved row. Imported rows never trigger live outreach or portal publishing."
      />

      <div className="metric-grid">
        <MetricCard label="Batches" value={String(leadImportBatches.length)} detail="Preview-first import records" />
        <MetricCard label="Rows" value={String(leadImportRows.length)} detail="Normalized field-test rows" />
        <MetricCard label="Approved rows" value={String(approvedLeadImportRows.length)} detail="Eligible for explicit commit only" />
        <MetricCard label="Blocked rows" value={String(blockedLeadImportRows.length)} detail="Visible with reasons" />
      </div>

      <Section title="Import Batches">
        <div className="record-list">
          {leadImportBatches.map((batch) => (
            <RecordCard
              key={batch.id}
              title={batch.batchName}
              meta={`${batch.sourceFilename} | ${batch.rowCount} rows | ${batch.blockedRowCount} blocked`}
              right={<Link href={`/dashboard/lead-imports/${batch.id}`}>Open</Link>}
            />
          ))}
        </div>
      </Section>

      <Section title="Field-Test Safety">
        <div className="grid-three">
          {v19SafetyCards.map((card) => (
            <RecordCard key={card.label} title={card.label} meta={card.detail} right={<Pill tone={card.value === "off" ? "green" : "gold"}>{card.value}</Pill>} />
          ))}
        </div>
      </Section>

      <Section title="Import Tools">
        <div className="grid-three">
          <RecordCard title="Preview Template" meta="CSV fields and critical row validation" right={<Link href="/dashboard/lead-imports/preview">Open</Link>} />
          <RecordCard title="Lead QA" meta="Data confidence and next action scoring" right={<Link href="/dashboard/lead-qa">Open</Link>} />
          <RecordCard title="Field Briefing" meta="Prime 2 daily field-test queue" right={<Link href="/dashboard/field-briefing">Open</Link>} />
        </div>
      </Section>
    </div>
  );
}
