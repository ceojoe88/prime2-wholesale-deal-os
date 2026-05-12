import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientBillingReadinessRecords } from "@/lib/demo-data";

export default function ClientCommandPlansBillingReadinessPage() {
  const record = clientBillingReadinessRecords[0];

  return (
    <div className="page">
      <PageHeader eyebrow="CP9 Billing Readiness" title="Billing Readiness" description="Billing readiness only - no Stripe/customer/invoice/subscription action occurred." />
      <div className="metric-grid">
        <MetricCard label="Status" value={record?.readinessStatus ?? "not_ready"} detail="Readiness placeholder only" />
        <MetricCard label="Customer info" value={record?.customerInfoCollected ? "collected" : "missing"} detail="No provider call" />
        <MetricCard label="Billing contact" value={record?.billingContactCollected ? "collected" : "missing"} detail="No payment collected" />
        <MetricCard label="Terms placeholder" value={record?.termsAcknowledgmentPlaceholder ? "ready" : "needs setup"} detail="No invoice created" />
      </div>
      <Section title="Billing Readiness Card">
        <RecordCard title="Future Billing Gate" meta="Billing readiness only - no Stripe/customer/invoice/subscription action occurred." right={<Pill tone="gold">{record?.readinessStatus ?? "setup_needed"}</Pill>}>
          <p>{record?.notesSummary ?? "Review placeholders before any future billing gate is considered."}</p>
        </RecordCard>
      </Section>
    </div>
  );
}
