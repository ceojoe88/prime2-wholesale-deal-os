import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientBillingLedgerEntries } from "@/lib/demo-data";

export default function ClientCommandBillingLedgerPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP11 Ledger" title="Billing Ledger" description="No raw card data is stored." />
      <Section title="Ledger Entries">
        <div className="record-list">
          {clientBillingLedgerEntries.map((entry) => (
            <RecordCard key={entry.id} title={entry.entryType} meta={entry.summary} right={<Pill tone={entry.status === "blocked" ? "red" : "green"}>{entry.status}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
