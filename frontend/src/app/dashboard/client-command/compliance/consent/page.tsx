import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientContactConsentRecords } from "@/lib/demo-data";

export default function ClientCommandComplianceConsentPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP6 Consent" title="Consent Records" description="Manual consent records only. No provider calls, DNC checks, or live communication occur here." />
      <Section title="Consent Status">
        <div className="record-list">
          {clientContactConsentRecords.map((record) => (
            <RecordCard key={record.id} title={record.contactName ?? record.id} meta={record.consentSummary} right={<Pill tone={record.consentStatus === "confirmed" ? "green" : "gold"}>{record.consentStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
