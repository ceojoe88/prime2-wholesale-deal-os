import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { getLeadImportBatch, leadImportBatches, leadImportRows } from "@/lib/demo-data";

export function generateStaticParams() {
  return leadImportBatches.map((batch) => ({ batchId: batch.id }));
}

export default async function LeadImportBatchDetailPage({
  params
}: {
  params: Promise<{ batchId: string }>;
}) {
  const { batchId } = await params;
  const batch = getLeadImportBatch(batchId);
  if (!batch) notFound();
  const rows = leadImportRows.filter((row) => row.batchId === batch.id);

  return (
    <div className="page">
      <PageHeader
        eyebrow={batch.status}
        title={batch.batchName}
        description="Batch detail shows row-level approval, duplicate, confidence, and blocked reasons. Commit remains explicit and approved-row-only."
      />

      <div className="metric-grid">
        <MetricCard label="Rows" value={String(batch.rowCount)} detail={batch.sourceFilename} />
        <MetricCard label="Approved" value={String(batch.approvedRowCount)} detail="Commit candidates only" />
        <MetricCard label="Blocked" value={String(batch.blockedRowCount)} detail="Cannot commit" />
        <MetricCard label="Live outreach" value="off" detail="Import cannot contact sellers" />
      </div>

      <Section title="Rows">
        <table className="data-table">
          <thead>
            <tr>
              <th>Owner</th>
              <th>Property</th>
              <th>Source</th>
              <th>Confidence</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.id}>
                <td>{row.ownerName}<div className="record-meta">{row.ownerPhone || "phone missing"}</div></td>
                <td>{row.propertyAddress || "address missing"}<div className="record-meta">{row.propertyCity}, {row.propertyState} {row.propertyZip}</div></td>
                <td>{row.leadSource}<div className="record-meta">{row.leadType}</div></td>
                <td>{row.dataConfidence}</td>
                <td><Pill tone={row.blockedReasons.length ? "red" : "green"}>{row.rowStatus}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>

      <Section title="Blocked Reasons">
        <div className="grid-three">
          {rows.filter((row) => row.blockedReasons.length > 0).map((row) => (
            <RecordCard key={row.id} title={row.id} meta={row.blockedReasons.join(", ")} right={<Pill tone="red">blocked</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
