import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientActivationBlockers,
  clientOnboardingTasks,
  getClientFirstWeeklyCycleReadiness,
  getClientGoLiveGate,
  getClientOnboardingReport,
  getClientWorkspaceReadinessScore
} from "@/lib/demo-data";

export default function ClientCommandOnboardingPage() {
  const readiness = getClientWorkspaceReadinessScore();
  const gate = getClientGoLiveGate();
  const firstWeekly = getClientFirstWeeklyCycleReadiness();
  const report = getClientOnboardingReport();
  const blocker = clientActivationBlockers[0];
  const task = clientOnboardingTasks[0];

  return (
    <div className="page">
      <PageHeader eyebrow="CP8 Onboarding" title="Onboarding Manager" description="Client onboarding and workspace activation readiness for controlled/manual Prime2 operation only." />
      <div className="metric-grid">
        <MetricCard label="Readiness score" value={String(readiness?.readinessScore ?? 0)} detail={readiness?.readinessStatus ?? "not_started"} />
        <MetricCard label="Manual gate" value={gate?.gateStatus ?? "not_ready"} detail={gate?.approvedScope ?? "none"} />
        <MetricCard label="Top blocker" value={blocker?.severity ?? "clear"} detail={blocker?.blockerSummary ?? "No blockers"} />
        <MetricCard label="First weekly cycle" value={firstWeekly?.readyForFirstWeeklyCycle ? "ready" : "review"} detail={firstWeekly?.recommendedNextStep ?? "Review readiness"} />
      </div>
      <Section title="Onboarding Manager Card">
        <div className="grid-two">
          <RecordCard title="Go-Live Readiness Gate" meta={gate?.clientSafeSummary ?? "Manual operation readiness only - no live communication, provider execution, billing, contracts, or campaigns are enabled."} right={<Pill tone="gold">{gate?.approvedScope ?? "manual only"}</Pill>} />
          <RecordCard title="Onboarding Report" meta={report?.clientSafeSummary ?? "Client-safe onboarding report - no revenue, ROI, or deal outcome is guaranteed."} right={<Pill tone="green">{report?.reportStatus ?? "draft"}</Pill>} />
        </div>
      </Section>
      <Section title="Command Links">
        <div className="grid-three">
          <RecordCard title="Business Profile" meta="Who the client is and what they run" right={<Link href="/dashboard/client-command/onboarding/business-profile">Open</Link>} />
          <RecordCard title="Strategy" meta="Acquisition and disposition posture" right={<Link href="/dashboard/client-command/onboarding/strategy">Open</Link>} />
          <RecordCard title="Markets" meta="Primary market setup and coverage" right={<Link href="/dashboard/client-command/onboarding/markets">Open</Link>} />
          <RecordCard title="Pipeline" meta="Default stage setup and manager owners" right={<Link href="/dashboard/client-command/onboarding/pipeline">Open</Link>} />
          <RecordCard title="Lead Sources" meta="Setup record only - no provider sync or campaign launch occurred." right={<Link href="/dashboard/client-command/onboarding/lead-sources">Open</Link>} />
          <RecordCard title="Buyer List" meta="Buyer setup only - no buyer has been contacted." right={<Link href="/dashboard/client-command/onboarding/buyer-list">Open</Link>} />
          <RecordCard title="Team" meta="Role coverage and missing owners" right={<Link href="/dashboard/client-command/onboarding/team">Open</Link>} />
          <RecordCard title="Compliance" meta="Readiness checklist only - no DNC provider check or 10DLC live registration occurred." right={<Link href="/dashboard/client-command/onboarding/compliance">Open</Link>} />
          <RecordCard title="First Leads" meta="First 10 leads checklist" right={<Link href="/dashboard/client-command/onboarding/first-leads">Open</Link>} />
          <RecordCard title="Readiness" meta="Weighted workspace readiness score" right={<Link href="/dashboard/client-command/onboarding/readiness">Open</Link>} />
          <RecordCard title="Blockers" meta={blocker?.recommendedFix ?? "No blockers"} right={<Link href="/dashboard/client-command/onboarding/blockers">Open</Link>} />
          <RecordCard title="Tasks" meta={task?.taskTitle ?? "Review activation tasks"} right={<Link href="/dashboard/client-command/onboarding/tasks">Open</Link>} />
          <RecordCard title="Activation Board" meta="Manual-operation activation board" right={<Link href="/dashboard/client-command/onboarding/activation-board">Open</Link>} />
          <RecordCard title="Onboarding Report" meta={report?.reportTitle ?? "Generate onboarding report"} right={<Link href="/dashboard/client-command/onboarding/report">Open</Link>} />
        </div>
      </Section>
    </div>
  );
}
