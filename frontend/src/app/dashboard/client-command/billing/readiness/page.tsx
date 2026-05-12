import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientBillingReadinessChecks } from "@/lib/demo-data";

export default function ClientCommandBillingReadinessPage() {
  const check = clientBillingReadinessChecks[0];

  return (
    <div className="page">
      <PageHeader eyebrow="CP11 Readiness" title="Billing Readiness Checks" description="Billing gate only - no payment occurs unless all billing gates pass." />
      <div className="metric-grid">
        <MetricCard label="Status" value={check?.readinessStatus ?? "blocked"} detail="No provider call" />
        <MetricCard label="Plan assignment" value={check?.planAssignmentPresent ? "present" : "missing"} detail="Plan gate required" />
        <MetricCard label="Provider mode" value={check?.providerMode ?? "unknown"} detail="Stripe/live provider execution is disabled by default." />
        <MetricCard label="No payment" value={check?.noPaymentCollected ? "true" : "false"} detail="No raw card data is stored." />
      </div>
      <Section title="Readiness Records">
        <div className="record-list">
          {clientBillingReadinessChecks.map((item) => (
            <RecordCard key={item.id} title={item.readinessStatus} meta={`Blockers: ${item.blockReasons.join(", ") || "none"}.`} right={<Pill tone={item.readinessStatus === "blocked" ? "red" : "green"}>{item.providerMode}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
