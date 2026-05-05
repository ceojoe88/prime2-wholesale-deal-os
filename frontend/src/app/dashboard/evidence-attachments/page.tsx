import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { evidenceAttachmentRecords, sensitiveAttachments } from "@/lib/demo-data";

export default function EvidenceAttachmentsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V18 Evidence Attachments"
        title="Evidence attachment records"
        description="Attachment records track safe metadata and source linkage. File bytes and raw private document paths are not committed or exposed by this readiness layer."
      />

      <div className="metric-grid">
        <MetricCard label="Attachments" value={String(evidenceAttachmentRecords.length)} detail="Metadata records only" />
        <MetricCard label="Sensitive" value={String(sensitiveAttachments.length)} detail="Kept internal, not export-ready" />
        <MetricCard label="Source-linked" value={String(evidenceAttachmentRecords.filter((item) => item.sourceLinkageVerified).length)} detail="Deal or evidence packet linkage" />
        <MetricCard label="Raw file paths" value="0" detail="Committed file paths blocked" />
      </div>

      <Section title="Attachment Queue">
        <table className="data-table">
          <thead>
            <tr>
              <th>Attachment</th>
              <th>Source</th>
              <th>Storage</th>
              <th>Sensitive</th>
              <th>Export</th>
            </tr>
          </thead>
          <tbody>
            {evidenceAttachmentRecords.map((attachment) => (
              <tr key={attachment.id}>
                <td>{attachment.filenamePlaceholder}<div className="record-meta">{attachment.attachmentType}</div></td>
                <td>{attachment.sourceRecordType} / {attachment.sourceRecordId}</td>
                <td>{attachment.storageMode}</td>
                <td><Pill tone={attachment.containsSensitiveData ? "gold" : "green"}>{attachment.containsSensitiveData ? "internal" : "safe metadata"}</Pill></td>
                <td><Pill tone={attachment.safeToExport ? "green" : "red"}>{attachment.safeToExport ? "ready" : "blocked"}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>

      <Section title="Linkage Guardrails">
        <div className="grid-three">
          {evidenceAttachmentRecords.map((attachment) => (
            <RecordCard key={attachment.id} title={attachment.id} meta={attachment.operatorNotes} right={<Pill tone={attachment.sourceLinkageVerified ? "green" : "red"}>{attachment.sourceLinkageVerified ? "linked" : "blocked"}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
