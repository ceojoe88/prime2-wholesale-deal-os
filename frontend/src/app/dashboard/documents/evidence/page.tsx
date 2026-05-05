import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { documentEvidenceLinks } from "@/lib/demo-data";

export default function DocumentEvidencePage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Document Evidence Links"
        title="Sanitized document evidence"
        description="Document records can support evidence packets through sanitized metadata only, with portal exposure and client-facing proof disabled by default."
      />
      <Section title="Linked Evidence">
        <div className="record-list">
          {documentEvidenceLinks.map((link) => (
            <RecordCard key={link.id} title={link.sourceRecordId} meta={`${link.sourceRecordType} / packet ${link.dealEvidencePacketId ?? "missing"}`} right={<Pill tone={link.sanitizedForExport ? "green" : "red"}>{link.linkageStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
