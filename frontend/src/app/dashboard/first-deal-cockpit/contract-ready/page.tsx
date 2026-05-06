import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { firstDealContractReadyChecklist, formatCurrency } from "@/lib/demo-data";

export default function FirstDealContractReadyPage() {
  const ready = firstDealContractReadyChecklist.filter((row) => row.state.contractReady);
  return (
    <div className="page">
      <PageHeader
        eyebrow="V31 Contract-Ready Checklist"
        title="External drafting readiness"
        description="This board marks readiness for an external contract/title/attorney process only after seller, underwriting, buyer, compliance, assignment, and owner gates are clear."
      />
      <div className="metric-grid">
        <MetricCard label="Ready candidates" value={String(ready.length)} detail="External process readiness" />
        <MetricCard label="Blocked candidates" value={String(firstDealContractReadyChecklist.length - ready.length)} detail="Required gates missing" />
        <MetricCard label="Document creation" value="off" detail="Prep marker only" />
        <MetricCard label="Owner approval" value="required" detail="No bypass" />
      </div>
      <Section title="Candidate Checklist">
        <div className="record-list">
          {firstDealContractReadyChecklist.map((row) => (
            <RecordCard
              key={row.state.id}
              title={`${row.state.dealId} / ${row.state.readinessStatus}`}
              meta={`Projected spread ${formatCurrency(row.state.projectedAssignmentFee)}. Missing: ${row.blockedReasons.join(", ") || "none"}`}
              right={<Pill tone={row.state.contractReady ? "green" : "red"}>{row.state.contractReady ? "ready" : "blocked"}</Pill>}
            />
          ))}
        </div>
      </Section>
    </div>
  );
}

