import { DealTable } from "@/components/DealTable";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  buyerMatches,
  complianceRecords,
  deals,
  divisions,
  formatCurrency,
  hotDeals,
  leads,
  projectedAssignmentTotal,
  underContractDeals
} from "@/lib/demo-data";

export default function DashboardPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Wholesale Prime"
        title="Daily acquisition command"
        description="Hot opportunities, spread protection, buyer demand, and compliance risk are ranked for owner approval."
      />

      <div className="metric-grid">
        <MetricCard label="Active leads" value={String(leads.length)} detail="30 motivated seller records seeded" />
        <MetricCard label="Hot 10K+ targets" value={String(hotDeals.length)} detail="Owner review before offer prep" />
        <MetricCard label="Projected fees" value={formatCurrency(projectedAssignmentTotal)} detail="Across active demo deals" />
        <MetricCard label="Compliance alerts" value={String(complianceRecords.length)} detail="Blocked until reviewed" />
      </div>

      <div className="command-band">
        <strong>Wholesale Prime briefing</strong>
        <div className="pill-row">
          <Pill tone="green">{underContractDeals.length} under contract</Pill>
          <Pill tone="gold">{buyerMatches.length} draft buyer matches</Pill>
          <Pill tone="red">No live outreach in v1</Pill>
        </div>
        <span className="muted">
          Prioritize 10K+ spreads with verified buyer margin, then route compliance-risk examples before assignment packet prep.
        </span>
      </div>

      <div className="grid-two">
        <Section title="Top Deal Queue">
          <DealTable limit={5} />
        </Section>
        <Section title="Manager Load">
          <div className="record-list">
            {divisions.slice(0, 5).map((division) => (
              <RecordCard
                key={division.id}
                title={division.managerName}
                meta={division.name}
                right={<Pill tone={division.riskFlags.length ? "gold" : "green"}>{division.workload} active</Pill>}
              >
                <span className="record-meta">{division.nextBestAction}</span>
              </RecordCard>
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
