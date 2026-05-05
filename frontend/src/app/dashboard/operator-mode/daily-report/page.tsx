import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { formatCurrency, latestOperatorDailyReport } from "@/lib/demo-data";

export default function OperatorDailyReportPage() {
  const report = latestOperatorDailyReport;

  return (
    <div className="page">
      <PageHeader
        eyebrow={report.reportDate}
        title="Autonomous daily operating report"
        description="Shows what the system did, prepared, blocked, what needs owner approval, top money actions, top risk actions, fee movement, and today's focus."
      />

      <div className="metric-grid">
        <MetricCard label="Prepared" value={String(report.whatPrepared.length)} detail="Draft or approval-ready items" />
        <MetricCard label="Blocked" value={String(report.whatBlocked.length)} detail="Unsafe or high-risk paths stopped" />
        <MetricCard label="Approvals" value={String(report.needsOwnerApproval.length)} detail="Owner review needed" />
        <MetricCard label="Fee movement" value={formatCurrency(report.projectedAssignmentFeeMovement)} detail="Projected movement estimate" />
      </div>

      <div className="grid-two">
        <Section title="Top Money Actions">
          <div className="record-list">
            {report.topMoneyActions.map((item) => <RecordCard key={item} title={item} right={<Pill tone="green">money</Pill>} />)}
          </div>
        </Section>
        <Section title="Top Risk Actions">
          <div className="record-list">
            {report.topRiskActions.map((item) => <RecordCard key={item} title={item} right={<Pill tone="red">risk</Pill>} />)}
          </div>
        </Section>
      </div>

      <Section title="Blocked By System">
        <div className="record-list">
          {report.whatBlocked.map((item) => <RecordCard key={item} title={item} right={<Pill tone="red">blocked</Pill>} />)}
        </div>
      </Section>
    </div>
  );
}
