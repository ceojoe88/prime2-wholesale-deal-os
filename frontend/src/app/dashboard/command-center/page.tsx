import { DealTable } from "@/components/DealTable";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { complianceRecords, deals, formatCurrency, hotDeals, leads } from "@/lib/demo-data";
import { buyerInterests, buyerPortalBlockedDeals, buyerVisibleDeals } from "@/lib/demo-data";

export default function CommandCenterPage() {
  const staleFollowUps = leads.filter((lead) => lead.stage === "follow_up");
  const needsUnderwriting = leads.filter((lead) => ["researched", "offer_needed"].includes(lead.stage));
  return (
    <div className="page">
      <PageHeader
        eyebrow="Operations Command"
        title="Ranked attention queue"
        description="Wholesale Prime routes hot deals, underwriting gaps, buyer-ready opportunities, stale follow-ups, and compliance blockers."
      />
      <div className="metric-grid">
        <MetricCard label="Top hot deals" value={String(hotDeals.length)} detail="Projected 10K+ assignment fees" />
        <MetricCard label="Underwriting queue" value={String(needsUnderwriting.length)} detail="Research or offer-needed leads" />
        <MetricCard label="Stale follow-ups" value={String(staleFollowUps.length)} detail="Draft-only touchpoint planning" />
        <MetricCard label="Risk blocks" value={String(complianceRecords.length)} detail="Owner plus compliance review" />
      </div>
      <div className="grid-two">
        <Section title="Hot Opportunities">
          <DealTable limit={8} />
        </Section>
        <Section title="Next Best Actions">
          <div className="record-list">
            {[
              ["critical", "Review under-contract spreads", `${formatCurrency(deals[1].projectedAssignmentFee)} projected on deal-002`],
              ["critical", "Review buyer portal intent queue", `${buyerInterests.length} buyer intents need owner handling`],
              ["high", "Route inherited-property review", "Deal-005 needs authority and title review"],
              ["high", "Fix buyer margin exception", "Deal-006 is blocked by spread and margin risk"],
              ["high", "Clear buyer portal publishing blocks", `${buyerPortalBlockedDeals.length} deals are blocked from buyer visibility`],
              ["normal", "Monitor visible deal rooms", `${buyerVisibleDeals.length} sanitized deals are currently visible`],
              ["normal", "Prepare draft follow-up notes", `${staleFollowUps.length} seller records need timing recommendations`]
            ].map(([priority, title, meta]) => (
              <RecordCard key={title} title={title} meta={meta} right={<Pill tone={priority === "critical" ? "red" : "gold"}>{priority}</Pill>} />
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
