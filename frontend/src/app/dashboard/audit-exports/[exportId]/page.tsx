import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { auditExportPackets, getAuditExportPacket } from "@/lib/demo-data";

export function generateStaticParams() {
  return auditExportPackets.map((packet) => ({ exportId: packet.id }));
}

export default async function AuditExportDetailPage({
  params
}: {
  params: Promise<{ exportId: string }>;
}) {
  const { exportId } = await params;
  const packet = getAuditExportPacket(exportId);
  if (!packet) notFound();

  const removedFields = [...packet.omittedSensitiveFields, ...packet.internalFieldsRemoved];

  return (
    <div className="page">
      <PageHeader
        eyebrow={packet.exportStatus}
        title={packet.id}
        description="This packet shows sanitized audit payload details only. Private contact data, source strategy, and internal spread logic stay out of unsafe exports."
      />

      <div className="metric-grid">
        <MetricCard label="Source" value={packet.sourceRecordType} detail={packet.sourceRecordId} />
        <MetricCard label="Removed fields" value={String(removedFields.length)} detail="Sensitive and internal fields" />
        <MetricCard label="Raw private data" value={packet.containsRawPrivateData ? "present" : "none"} detail="Unsafe exports are blocked" />
        <MetricCard label="Approval" value={packet.ownerApprovalStatus} detail={packet.exportScope} />
      </div>

      <div className="grid-two">
        <Section title="Sanitized Payload">
          <div className="record-list">
            {Object.entries(packet.sanitizedPayload).map(([key, value]) => (
              <RecordCard key={key} title={key} meta={Array.isArray(value) ? value.join(", ") : String(value)} right={<Pill>safe</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Removed Fields">
          <div className="record-list">
            {removedFields.map((field) => (
              <RecordCard key={field} title={field} meta="Removed from export payload" right={<Pill tone="green">redacted</Pill>} />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Included Source Records">
        <div className="grid-three">
          {packet.includedRecordIds.map((recordId) => (
            <RecordCard key={recordId} title={recordId} meta="Audit source reference" right={<Pill>source</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
