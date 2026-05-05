import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  documentAssignmentWarnings,
  documentExternalReviewTasks,
  documentIntelligenceFiles,
  documentMissingSignatures,
  documentPofIssues,
  documentsNeedingReview
} from "@/lib/demo-data";

export default function DocumentsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V24 Deal Document Intelligence"
        title="Document intelligence command"
        description="Prime 2 classifies deal files, extracts safe metadata, flags missing fields and risky language, and routes review tasks without exposing internal text or changing deal state."
      />

      <div className="metric-grid">
        <MetricCard label="Documents" value={String(documentIntelligenceFiles.length)} detail="Internal review records" />
        <MetricCard label="Need review" value={String(documentsNeedingReview.length)} detail="Owner queue" />
        <MetricCard label="Missing signatures" value={String(documentMissingSignatures.length)} detail="Control check" />
        <MetricCard label="POF issues" value={String(documentPofIssues.length)} detail="Buyer verification" />
      </div>

      <Section title="Recent Documents">
        <div className="record-list">
          {documentIntelligenceFiles.map((document) => (
            <RecordCard
              key={document.id}
              title={document.originalFilename}
              meta={`${document.documentType} / ${document.extractedSummary}`}
              right={<Link href={`/dashboard/documents/${document.id}`}><Pill tone={document.riskStatus === "high" ? "red" : "gold"}>{document.riskStatus}</Pill></Link>}
            />
          ))}
        </div>
      </Section>

      <Section title="Review Work Areas">
        <div className="grid-three">
          <RecordCard title="Upload Intake" meta="Manual metadata and pasted text intake placeholder" right={<Link href="/dashboard/documents/upload">Open</Link>} />
          <RecordCard title="Issues" meta={`${documentAssignmentWarnings.length} assignment warnings`} right={<Link href="/dashboard/documents/issues">Open</Link>} />
          <RecordCard title="Review Queue" meta={`${documentExternalReviewTasks.length} external reminders`} right={<Link href="/dashboard/documents/review-queue">Open</Link>} />
          <RecordCard title="Evidence Links" meta="Document evidence remains sanitized" right={<Link href="/dashboard/documents/evidence">Open</Link>} />
          <RecordCard title="Portal Publishing" meta="Unavailable from document intake" right={<Pill tone="red">off</Pill>} />
          <RecordCard title="Title Delivery" meta="External handoff remains owner-controlled" right={<Pill tone="red">off</Pill>} />
        </div>
      </Section>
    </div>
  );
}

