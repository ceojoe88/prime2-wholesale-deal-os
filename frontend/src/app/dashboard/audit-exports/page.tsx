import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { auditExportPackets, auditExportsReady } from "@/lib/demo-data";

export default function AuditExportsPage() {
  const removedFieldCount = auditExportPackets.reduce(
    (sum, packet) => sum + packet.omittedSensitiveFields.length + packet.internalFieldsRemoved.length,
    0
  );

  return (
    <div className="page">
      <PageHeader
        eyebrow="V18 Audit Export Packets"
        title="Sanitized audit exports"
        description="Audit packets are owner-review artifacts that remove private, secret, and internal strategy fields before any export status can move forward."
      />

      <div className="metric-grid">
        <MetricCard label="Packets" value={String(auditExportPackets.length)} detail="Internal owner audit packets" />
        <MetricCard label="Ready for review" value={String(auditExportsReady.length)} detail="Sanitized payloads only" />
        <MetricCard label="Removed fields" value={String(removedFieldCount)} detail="Sensitive or internal fields stripped" />
        <MetricCard label="Raw private data" value="0" detail="Unsafe export payloads blocked" />
      </div>

      <Section title="Export Packets">
        <table className="data-table">
          <thead>
            <tr>
              <th>Export</th>
              <th>Source</th>
              <th>Status</th>
              <th>Removed</th>
              <th>Approval</th>
            </tr>
          </thead>
          <tbody>
            {auditExportPackets.map((packet) => (
              <tr key={packet.id}>
                <td><Link href={`/dashboard/audit-exports/${packet.id}`}>{packet.exportType}</Link><div className="record-meta">{packet.id}</div></td>
                <td>{packet.sourceRecordType} / {packet.sourceRecordId}</td>
                <td><Pill tone={packet.exportStatus.includes("ready") ? "green" : "gold"}>{packet.exportStatus}</Pill></td>
                <td>{packet.omittedSensitiveFields.length + packet.internalFieldsRemoved.length}</td>
                <td>{packet.ownerApprovalStatus}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>

      <Section title="Export Guardrails">
        <div className="grid-three">
          <RecordCard title="Raw private data" meta="Seller, buyer, contact, and secret fields are removed" right={<Pill tone="green">blocked</Pill>} />
          <RecordCard title="Internal strategy" meta="Lead source, spread logic, and private notes are stripped" right={<Pill tone="green">hidden</Pill>} />
          <RecordCard title="External share" meta="Requires owner approval and a safe packet status" right={<Pill tone="gold">gated</Pill>} />
        </div>
      </Section>
    </div>
  );
}
