import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  documentIntelligenceFiles,
  getDocumentEvidenceLinks,
  getDocumentIntelligenceFile,
  getDocumentIssues,
  getDocumentReviewTasks
} from "@/lib/demo-data";

export function generateStaticParams() {
  return documentIntelligenceFiles.map((document) => ({ documentId: document.id }));
}

export default async function DocumentDetailPage({
  params
}: {
  params: Promise<{ documentId: string }>;
}) {
  const { documentId } = await params;
  const document = getDocumentIntelligenceFile(documentId);
  if (!document) notFound();
  const issues = getDocumentIssues(document.id);
  const tasks = getDocumentReviewTasks(document.id);
  const evidenceLinks = getDocumentEvidenceLinks(document.id);

  return (
    <div className="page">
      <PageHeader
        eyebrow={document.ownerReviewStatus}
        title={document.originalFilename}
        description={document.extractedSummary}
      />

      <div className="metric-grid">
        <MetricCard label="Confidence" value={`${document.classificationConfidence}%`} detail={document.documentType} />
        <MetricCard label="Price" value={document.extractedPrice ? `$${document.extractedPrice.toLocaleString()}` : "missing"} detail="Extracted from source record" />
        <MetricCard label="Signature" value={document.extractedSignatureStatus} detail="Review-only status" />
        <MetricCard label="Full text" value={document.fullTextHidden ? "hidden" : "visible"} detail="Internal surface is sanitized" />
      </div>

      <div className="grid-two">
        <Section title="Extracted Fields">
          <table className="data-table">
            <tbody>
              <tr><td>Seller</td><td>{document.extractedSellerName || "missing"}</td></tr>
              <tr><td>Buyer/entity</td><td>{document.extractedBuyerName || "missing"}</td></tr>
              <tr><td>Property</td><td>{document.extractedPropertyAddress || "missing"}</td></tr>
              <tr><td>Closing date</td><td>{document.extractedClosingDate || "missing"}</td></tr>
              <tr><td>POF amount</td><td>{document.extractedPofAmount ? `$${document.extractedPofAmount.toLocaleString()}` : "not captured"}</td></tr>
            </tbody>
          </table>
        </Section>

        <Section title="Issue Flags">
          <div className="record-list">
            {issues.map((issue) => (
              <RecordCard key={issue.id} title={issue.issueType} meta={issue.explanation} right={<Pill tone={issue.severity === "high" ? "red" : "gold"}>{issue.severity}</Pill>} />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Review Tasks">
        <div className="record-list">
          {tasks.map((task) => (
            <RecordCard key={task.id} title={task.taskType} meta={task.recommendedNextAction} right={<Pill tone={task.priority === "high" ? "red" : "gold"}>{task.status}</Pill>} />
          ))}
        </div>
      </Section>

      <Section title="Evidence Links">
        <div className="record-list">
          {evidenceLinks.map((link) => (
            <RecordCard key={link.id} title={link.sourceRecordId} meta={`${link.sourceRecordType} / ${link.linkageStatus}`} right={<Pill tone="green">sanitized</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}

