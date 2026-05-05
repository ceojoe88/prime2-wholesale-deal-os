import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Prime2IdentityPanel } from "@/components/Prime2IdentityPanel";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { complianceRecords, formatCurrency, hotDeals, leads, projectedAssignmentTotal, underContractDeals } from "@/lib/demo-data";

export default function DailyBriefingPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Daily Briefing"
        title="Prime 2 daily strategy"
        description="Prioritize hot spreads, protect buyer margins, and clear compliance gates before any owner-approved real-world step."
      />
      <div className="metric-grid">
        <MetricCard label="Leads" value={String(leads.length)} detail="Motivated seller board" />
        <MetricCard label="Hot deals" value={String(hotDeals.length)} detail="10K+ opportunities" />
        <MetricCard label="Under contract" value={String(underContractDeals.length)} detail="Assignment review needed" />
        <MetricCard label="Projected fees" value={formatCurrency(projectedAssignmentTotal)} detail="Demo pipeline" />
      </div>
      <Prime2IdentityPanel />
      <div className="grid-two">
        <Section title="Prime 2 Readout">
          <div className="record-list">
            <RecordCard title="Move first on clean hot deals" meta="Deal-001 and deal-002 have strong spreads and buyer demand." right={<Pill tone="green">today</Pill>} />
            <RecordCard title="Repair the margin exception" meta="Deal-006 should not advance until the spread and buyer margin are corrected." right={<Pill tone="red">block</Pill>} />
            <RecordCard title="Clear inherited and probate review" meta="Deal-005 and deal-008 need attorney/title review reminders." right={<Pill tone="gold">review</Pill>} />
          </div>
        </Section>
        <Section title="Compliance Alerts">
          <div className="record-list">
            {complianceRecords.map((record) => <RecordCard key={record.id} title={record.title} meta={record.dealId} right={<Pill tone="red">alert</Pill>} />)}
          </div>
        </Section>
      </div>
    </div>
  );
}
