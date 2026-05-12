import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientBillingCustomerProfiles } from "@/lib/demo-data";

export default function ClientCommandBillingCustomersPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP11 Customers" title="Billing Customer Profiles" description="No raw card data is stored." />
      <Section title="Customer Profiles">
        <div className="record-list">
          {clientBillingCustomerProfiles.map((customer) => (
            <RecordCard
              key={customer.id}
              title={customer.customerName}
              meta={`${customer.clientSafeSummary} Billing email: ${customer.billingEmail}.`}
              right={<Pill tone="gold">{customer.billingContactCollected ? "contact ready" : "needs review"}</Pill>}
            />
          ))}
        </div>
      </Section>
    </div>
  );
}
