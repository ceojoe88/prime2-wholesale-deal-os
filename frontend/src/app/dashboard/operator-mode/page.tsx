import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Prime2IdentityPanel } from "@/components/Prime2IdentityPanel";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  activeOperatorMode,
  currentSystemTrustScore,
  fieldTestingAccuracy,
  firstDealCandidates,
  latestOperatorDailyReport,
  lowConfidenceQaReviews,
  operatorExceptionsOpen,
  operatorHardBoundaryCards,
  predictionMisses,
  pendingOwnerApprovals,
  semiAutonomousCommandLoopRuns
} from "@/lib/demo-data";

export default function OperatorModePage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V17 Semi-Autonomous Operator Mode"
        title="Operator mode command loop"
        description="Prime 2 scans, scores, routes, prepares, checks gates, escalates, briefs, waits for approvals, logs outcomes, and optimizes while real-world high-risk actions remain owner-approved."
      />

      <div className="metric-grid">
        <MetricCard label="Current mode" value={activeOperatorMode.currentMode} detail={`Default ${activeOperatorMode.defaultMode}`} />
        <MetricCard label="Pending approvals" value={String(pendingOwnerApprovals.length)} detail="Unified owner approval console" />
        <MetricCard label="Open exceptions" value={String(operatorExceptionsOpen.length)} detail="Only high-value or risk exceptions escalate" />
        <MetricCard label="Trust score" value={String(currentSystemTrustScore.overallTrustScore)} detail={currentSystemTrustScore.trustStatus} />
      </div>

      <Section title="Field Testing Queue">
        <div className="grid-three">
          <RecordCard title="Real lead QA" meta={`${lowConfidenceQaReviews.length} low-confidence or blocked records need review`} right={<Pill tone="gold">review</Pill>} />
          <RecordCard title="First-deal candidates" meta={`${firstDealCandidates.length} imported records are ready for owner-reviewed field work`} right={<Pill tone="green">queue</Pill>} />
          <RecordCard title="Prediction accuracy" meta={`${predictionMisses.length} misses need scoring review`} right={<Pill tone={predictionMisses.length ? "gold" : "green"}>{fieldTestingAccuracy}%</Pill>} />
        </div>
      </Section>

      <Prime2IdentityPanel />

      <Section title="Hard Boundaries">
        <div className="grid-three">
          {operatorHardBoundaryCards.map((card) => (
            <RecordCard key={card.label} title={card.label} meta={card.detail} right={<Pill tone={card.value === "off" || card.value === "disabled" ? "red" : "gold"}>{card.value}</Pill>} />
          ))}
        </div>
      </Section>

      <div className="grid-two">
        <Section title="Command Loop">
          <div className="record-list">
            {semiAutonomousCommandLoopRuns.map((loop) => (
              <RecordCard key={loop.id} title={loop.cycleStatus} meta={`Approvals waiting: ${loop.approvalsWaiting.join(", ")}`} right={<Pill tone="gold">waiting</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Daily Focus">
          <div className="record-list">
            {latestOperatorDailyReport.recommendedFocusToday.map((item) => (
              <RecordCard key={item} title={item} right={<Pill>focus</Pill>} />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Operator Mode Routes">
        <div className="grid-three">
          <RecordCard title="Approvals" meta="Unified owner approval console" right={<Link href="/dashboard/operator-mode/approvals">Open</Link>} />
          <RecordCard title="Exceptions" meta="Risk and money exceptions" right={<Link href="/dashboard/operator-mode/exceptions">Open</Link>} />
          <RecordCard title="Daily Report" meta="Autonomous operating report" right={<Link href="/dashboard/operator-mode/daily-report">Open</Link>} />
          <RecordCard title="System Trust" meta="Trust and health scoring" right={<Link href="/dashboard/operator-mode/system-trust">Open</Link>} />
          <RecordCard title="Settings" meta="Mode and boundary settings" right={<Link href="/dashboard/operator-mode/settings">Open</Link>} />
        </div>
      </Section>
    </div>
  );
}
