import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientContactOptOutRecords } from "@/lib/demo-data";

export default function ClientCommandComplianceOptOutPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP6 Opt-Outs" title="Opt-Out Records" description="Manual opt-out tracking only. No channel is contacted from this workspace." />
      <Section title="Opt-Out Status">
        <div className="record-list">
          {clientContactOptOutRecords.map((record) => (
            <RecordCard key={record.id} title={record.contactType} meta={record.optOutSummary} right={<Pill tone={record.optOutStatus === "active" ? "red" : "gold"}>{record.optOutStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
