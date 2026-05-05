import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  formatCurrency,
  leadSpendPlans,
  leadSpendRecommendations,
  unsupportedLeadSpendPlans
} from "@/lib/demo-data";

export default function LeadSpendPlannerPage() {
  const totalSpend = leadSpendRecommendations.reduce((total, plan) => total + plan.maxMonthlySpend, 0);

  return (
    <div className="page">
      <PageHeader
        eyebrow="V16 Lead Spend Planner"
        title="Evidence-based lead spend planner"
        description="Recommend zip codes, lead types, max monthly spend, expected deal count, expected assignment fee range, and break-even assignment targets without unsupported spend or guaranteed ROI."
      />

      <div className="metric-grid">
        <MetricCard label="Spend plans" value={String(leadSpendPlans.length)} detail="Draft estimates only" />
        <MetricCard label="Recommended spend" value={formatCurrency(totalSpend)} detail="Owner review required" />
        <MetricCard label="Unsupported plans" value={String(unsupportedLeadSpendPlans.length)} detail="Blocked by evidence guard" />
        <MetricCard label="Guaranteed ROI" value="off" detail="No unsupported ROI language" />
      </div>

      <Section title="Spend Recommendations">
        <div className="record-list">
          {leadSpendPlans.map((plan) => (
            <RecordCard
              key={plan.id}
              title={`${plan.targetZipCodes.join(", ")} / ${plan.leadTypes.join(", ")}`}
              meta={`Expected ${plan.expectedDealCount} deals; fee range ${formatCurrency(plan.expectedAssignmentFeeLow)} - ${formatCurrency(plan.expectedAssignmentFeeHigh)}`}
              right={<Pill tone={plan.maxMonthlySpend > 0 ? "gold" : "red"}>{formatCurrency(plan.maxMonthlySpend)}</Pill>}
            >
              <div className="stack">
                <span>Break-even target: {formatCurrency(plan.breakEvenAssignmentTarget)}</span>
                <span className="record-meta">Evidence: {plan.evidenceBasis.join(", ")}</span>
              </div>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}
