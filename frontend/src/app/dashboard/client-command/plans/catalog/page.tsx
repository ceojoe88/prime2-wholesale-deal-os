import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientPlanCatalogEntries } from "@/lib/demo-data";

export default function ClientCommandPlansCatalogPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP9 Catalog" title="Plan Catalog" description="Plan gate only - no payment has been collected." />
      <Section title="Catalog">
        <div className="record-list">
          {clientPlanCatalogEntries.map((plan) => (
            <RecordCard
              key={plan.id}
              title={plan.planName}
              meta={`${plan.clientSafeSummary} Monthly placeholder: ${plan.monthlyPricePlaceholder}. Setup placeholder: ${plan.setupFeePlaceholder}.`}
              right={<Pill tone={plan.isActive ? "green" : "gold"}>{plan.planCode}</Pill>}
            />
          ))}
        </div>
      </Section>
    </div>
  );
}
