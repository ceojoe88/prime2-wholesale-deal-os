import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { formatCurrency, leadSourceRoiRecords } from "@/lib/demo-data";

export default function LeadSourceRoiPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Lead Source ROI"
        title="Source quality estimates"
        description="Lead source records connect imports, QA, calls, seller motivation, offers, and assignment-fee evidence while clearly labeling cost gaps as estimates."
      />
      <div className="metric-grid">
        <MetricCard label="Sources" value={String(leadSourceRoiRecords.length)} detail="Evidence-backed source records" />
        <MetricCard label="Leads imported" value={String(leadSourceRoiRecords.reduce((total, row) => total + row.leadsImported, 0))} detail="Field-test volume" />
        <MetricCard label="Motivated sellers" value={String(leadSourceRoiRecords.reduce((total, row) => total + row.motivatedSellers, 0))} detail="Call outcome basis" />
        <MetricCard label="Projected fees" value={formatCurrency(leadSourceRoiRecords.reduce((total, row) => total + row.projectedAssignmentFees, 0))} detail="Estimate only" />
      </div>
      <Section title="Source Records">
        <div className="record-list">
          {leadSourceRoiRecords.map((record) => (
            <RecordCard key={record.id} title={`${record.sourceName} / ${record.marketId}`} meta={`${record.notes} Evidence: ${record.evidenceBasis.join(", ")}`} right={<Pill tone={record.roiConfidence >= 60 ? "green" : "gold"}>{record.roiConfidence}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}

