import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { complianceRecords, formatCurrency, hotDeals, projectedAssignmentTotal } from "@/lib/demo-data";

export default function OverseerPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Executive Overseer"
        title="Wholesale Prime"
        description="Reviews opportunities, routes division work, prioritizes hot deals, flags compliance risk, and blocks unsafe actions."
      />
      <div className="metric-grid">
        <MetricCard label="Hot opportunities" value={String(hotDeals.length)} detail="10K+ spread target" />
        <MetricCard label="Assignment total" value={formatCurrency(projectedAssignmentTotal)} detail="Projected demo pipeline" />
        <MetricCard label="Compliance risk" value={String(complianceRecords.length)} detail="Escalated before packets" />
        <MetricCard label="Authority" value="0" detail="No live execution power" />
      </div>
      <div className="grid-two">
        <Section title="Prime Recommendations">
          <div className="record-list">
            {[
              "Review deal-002 and deal-008 under-contract gates before any buyer packet.",
              "Advance deal-001 first; it has strong spread and buyer demand.",
              "Hold deal-006 until seller price or buyer margin is repaired.",
              "Refresh comp support on deal-005 before inherited-property offer explanation."
            ].map((item) => (
              <RecordCard key={item} title={item} right={<Pill tone="gold">recommend</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Blocked Action Classes">
          <div className="pill-row">
            {["SMS", "email", "calls", "buyer blasts", "contract execution", "legal advice"].map((label) => (
              <Pill key={label} tone="red">{label}</Pill>
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
