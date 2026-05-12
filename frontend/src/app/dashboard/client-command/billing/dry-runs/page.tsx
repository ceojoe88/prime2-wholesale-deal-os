import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientCheckoutDryRunReceipts } from "@/lib/demo-data";

export default function ClientCommandBillingDryRunsPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP11 Dry Runs" title="Checkout Dry Runs" description="Dry run does not charge a card." />
      <Section title="Dry Run Receipts">
        <div className="record-list">
          {clientCheckoutDryRunReceipts.map((receipt) => (
            <RecordCard key={receipt.id} title={receipt.planCode} meta={`${receipt.dryRunSummary} Idempotency: ${receipt.idempotencyKey}.`} right={<Pill tone="gold">{receipt.status}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
