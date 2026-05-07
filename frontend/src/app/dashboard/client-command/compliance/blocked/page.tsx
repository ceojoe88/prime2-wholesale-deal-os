import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientSafeContactStatuses } from "@/lib/demo-data";

export default function ClientCommandComplianceBlockedPage() {
  const blocked = clientSafeContactStatuses.filter((status) => status.status === "blocked");
  return (
    <div className="page">
      <PageHeader eyebrow="CP6 Blocked" title="Blocked Contact Statuses" description="Blocked means manual-use prep is paused. No provider check or live communication occurred." />
      <Section title="Blocked Contacts">
        <div className="record-list">
          {blocked.map((status) => (
            <RecordCard key={status.id} title={status.contactType} meta={status.reasonSummary} right={<Pill tone="red">{status.status}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
