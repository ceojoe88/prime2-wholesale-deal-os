import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientWeeklyBottlenecks,
  clientWeeklyCommandReports,
  clientWeeklyDivisionSummaries,
  clientWeeklyLeadStatusRollups,
  clientWeeklyRecommendedActions,
  clientWeeklyReportMetricSnapshots,
  getClientWeeklyReport
} from "@/lib/demo-data";

export function generateStaticParams() {
  return clientWeeklyCommandReports.map((report) => ({ reportId: report.id }));
}

export default function ClientCommandReportDetailPage({ params }: { params: { reportId: string } }) {
  const report = getClientWeeklyReport(params.reportId);
  if (!report) {
    notFound();
  }
  const metrics = clientWeeklyReportMetricSnapshots.find((item) => item.reportId === report.id);
  const rollups = clientWeeklyLeadStatusRollups.filter((item) => item.reportId === report.id);
  const bottlenecks = clientWeeklyBottlenecks.filter((item) => item.reportId === report.id);
  const actions = clientWeeklyRecommendedActions.filter((item) => item.reportId === report.id);
  const divisions = clientWeeklyDivisionSummaries.filter((item) => item.reportId === report.id);

  return (
    <div className="page">
      <PageHeader eyebrow="CP7 Report Detail" title={report.reportTitle} description="Client-safe weekly report - no revenue, ROI, or deal outcome is guaranteed." />
      <div className="metric-grid">
        <MetricCard label="Status" value={report.reportStatus} detail={`${report.reportWeekStart} to ${report.reportWeekEnd}`} />
        <MetricCard label="Total leads" value={String(metrics?.totalLeads ?? 0)} detail={`${metrics?.hotLeadsCount ?? 0} hot`} />
        <MetricCard label="Compliance" value={String(metrics?.complianceNeedsReviewCount ?? 0)} detail={`${metrics?.complianceBlockedCount ?? 0} blocked`} />
        <MetricCard label="Disposition ready" value={String(metrics?.dispositionReadyCount ?? 0)} detail={`${metrics?.buyerMatchCount ?? 0} buyer matches`} />
      </div>
      <Section title="Weekly Executive Summary">
        <div className="grid-two">
          <RecordCard title="Executive Summary" meta={report.executiveSummary} right={<Pill tone="gold">No ROI Claim</Pill>} />
          <RecordCard title="Next Week Focus" meta={report.nextWeekFocus} right={<Pill tone="gold">No Live Actions Taken</Pill>} />
        </div>
      </Section>
      <div className="grid-two">
        <Section title="Lead Status Rollup">
          <div className="record-list">
            {rollups.map((rollup) => (
              <RecordCard key={rollup.id} title={rollup.leadNameOrAddress} meta={rollup.statusSummary} right={<Pill tone={rollup.priorityLevel === "urgent" ? "red" : rollup.priorityLevel === "high" ? "gold" : "green"}>{rollup.currentStage}</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Division Health Summary">
          <div className="record-list">
            {divisions.map((division) => (
              <RecordCard key={division.id} title={division.divisionName} meta={division.summary} right={<Pill tone={division.healthStatus === "strong" ? "green" : division.healthStatus === "blocked" ? "red" : "gold"}>{division.healthStatus}</Pill>} />
            ))}
          </div>
        </Section>
      </div>
      <div className="grid-two">
        <Section title="Bottleneck Analysis">
          <div className="record-list">
            {bottlenecks.map((item) => (
              <RecordCard key={item.id} title={item.bottleneckType} meta={item.bottleneckSummary} right={<Pill tone={item.severity === "high" ? "red" : "gold"}>{item.affectedLeadCount}</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Recommended Next Actions">
          <div className="record-list">
            {actions.map((action) => (
              <RecordCard key={action.id} title={action.actionType} meta={action.actionSummary} right={<Pill tone={action.priority === "urgent" ? "red" : action.priority === "high" ? "gold" : "green"}>{action.dueWindow}</Pill>} />
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
