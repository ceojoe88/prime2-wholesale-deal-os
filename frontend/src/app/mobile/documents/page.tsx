import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { documentMissingSignatures, documentPofIssues, documentsNeedingReview, mobileDocumentQueue } from "@/lib/demo-data";

export default function MobileDocumentsPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="Mobile Documents" title="Document metadata capture" description="Capture document/photo placeholders and review document intelligence flags while uploads and portal exposure stay gated." />
      <div className="metric-grid">
        <MetricCard label="Mobile docs" value={String(mobileDocumentQueue.length)} detail="Recent internal records" />
        <MetricCard label="Need review" value={String(documentsNeedingReview.length)} detail="Owner queue" />
        <MetricCard label="Missing signatures" value={String(documentMissingSignatures.length)} detail="Review flag" />
        <MetricCard label="POF issues" value={String(documentPofIssues.length)} detail="Buyer verification" />
      </div>
      <Section title="Recent Document Records">
        <div className="record-list">
          {mobileDocumentQueue.map((document) => (
            <RecordCard key={document.id} title={document.originalFilename} meta={document.extractedSummary} right={<Link href={`/dashboard/documents/${document.id}`}><Pill tone={document.riskStatus === "high" ? "red" : "gold"}>{document.riskStatus}</Pill></Link>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
