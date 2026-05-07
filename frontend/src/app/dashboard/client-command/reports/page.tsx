import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientWeeklyBottlenecks,
  clientWeeklyCommandReports,
  clientWeeklyRecommendedActions
} from "@/lib/demo-data";

export default function ClientCommandReportsPage() {
  const latest = clientWeeklyCommandReports[0];
  const topBottleneck = clientWeeklyBottlenecks[0];
  const topAction = clientWeeklyRecommendedActions[0];
  return (
    <div className="page">
      <PageHeader eyebrow="CP7 Reports" title="Weekly Client Command Reports" description="Client-safe weekly report - no revenue, ROI, or deal outcome is guaranteed." />
      <div className="metric-grid">
        <MetricCard label="Latest report" value={latest?.reportStatus ?? "none"} detail={latest?.reportWeekEnd ?? "Not generated"} />
        <MetricCard label="Top bottleneck" value={topBottleneck?.bottleneckType ?? "clear"} detail={topBottleneck?.recommendedFix ?? "No bottlenecks"} />
        <MetricCard label="Next action" value={topAction?.priority ?? "none"} detail={topAction?.actionSummary ?? "No action"} />
        <MetricCard label="Weekly reports" value={String(clientWeeklyCommandReports.length)} detail="Client-safe summaries only" />
      </div>
      <Section title="Command Links">
        <div className="grid-three">
          <RecordCard title="Weekly Reports" meta="Workspace report list" right={<Link href="/dashboard/client-command/reports/weekly">Open</Link>} />
          <RecordCard title="Bottlenecks" meta="Current bottleneck analysis" right={<Link href="/dashboard/client-command/reports/bottlenecks">Open</Link>} />
          <RecordCard title="Recommended Actions" meta="Next-week action plan" right={<Link href="/dashboard/client-command/reports/recommended-actions">Open</Link>} />
          <RecordCard title="Latest Report Detail" meta={latest?.reportTitle ?? "No report"} right={latest ? <Link href={`/dashboard/client-command/reports/${latest.id}`}>Open</Link> : <Pill tone="gold">pending</Pill>} />
        </div>
      </Section>
    </div>
  );
}
