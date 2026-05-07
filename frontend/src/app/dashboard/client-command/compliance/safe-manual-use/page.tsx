import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientSafeContactStatuses } from "@/lib/demo-data";

export default function ClientCommandComplianceSafeManualUsePage() {
  const safeManualUse = clientSafeContactStatuses.filter((status) => status.status === "safe_for_manual_use");
  return (
    <div className="page">
      <PageHeader eyebrow="CP6 Safe Manual Use" title="Safe Manual-Use Status" description="Readiness check only - no provider check or live communication occurred." />
      <Section title="Safe Manual Use">
        <div className="record-list">
          {safeManualUse.map((status) => (
            <RecordCard key={status.id} title={status.contactType} meta={status.reasonSummary} right={<Pill tone="green">{status.channel}</Pill>}>
              <p>Readiness check only - no provider check or live communication occurred.</p>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}
