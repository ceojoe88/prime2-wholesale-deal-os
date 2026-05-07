import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientSafeContactStatuses } from "@/lib/demo-data";

export default function ClientCommandComplianceNeedsReviewPage() {
  const needsReview = clientSafeContactStatuses.filter((status) => ["needs_review", "missing_consent"].includes(status.status));
  return (
    <div className="page">
      <PageHeader eyebrow="CP6 Needs Review" title="Compliance Review Queue" description="Manual review queue for consent, channel, and placeholder readiness." />
      <Section title="Needs Review">
        <div className="record-list">
          {needsReview.map((status) => (
            <RecordCard key={status.id} title={status.contactType} meta={status.reasonSummary} right={<Pill tone="gold">{status.status}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
