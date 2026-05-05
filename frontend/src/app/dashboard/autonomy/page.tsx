import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Prime2IdentityPanel } from "@/components/Prime2IdentityPanel";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  automationRules,
  autonomyCriticalEscalations,
  autonomyDraftTasks,
  autonomyEnabledRules,
  autonomyEscalationQueue,
  autonomyLevel4Rules,
  autonomyOpenTasks,
  autonomySafetyBoundaryCards,
  blockedAutomationAttempts,
  dailyCommandBriefings,
  latestAutonomyDailyBriefing,
  schedulerRuns
} from "@/lib/demo-data";

export default function AutonomyPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V12 Prime 2 Autonomy"
        title="Near-autonomous execution panel"
        description="Prime 2 can prepare, score, schedule, route, escalate, and brief internally while real-world actions stay owner-gated."
      />

      <div className="metric-grid">
        <MetricCard label="Rules enabled" value={String(autonomyEnabledRules.length)} detail={`${automationRules.length} guarded rules`} />
        <MetricCard label="Open tasks" value={String(autonomyOpenTasks.length)} detail="Internal prep queue" />
        <MetricCard label="Escalations" value={String(autonomyEscalationQueue.length)} detail={`${autonomyCriticalEscalations.length} critical`} />
        <MetricCard label="Level 5" value="disabled" detail="Unavailable in V12" />
      </div>

      <Prime2IdentityPanel />

      <Section title="Prime 2 Autonomy Panel">
        <div className="grid-three">
          <RecordCard title="Default Level 2" meta="Autonomous internal prep: scoring, queues, blockers, evidence, readiness checks." right={<Pill tone="green">on</Pill>} />
          <RecordCard title="Default Level 3" meta="Draft creation and reminder scheduling with audit ledgers." right={<Pill tone="green">on</Pill>} />
          <RecordCard title="Controlled Level 4" meta={`${autonomyLevel4Rules.length} rule requires owner approval before any gated review.`} right={<Pill tone="gold">owner</Pill>} />
        </div>
      </Section>

      <Section title="Safety Boundaries">
        <div className="grid-three">
          {autonomySafetyBoundaryCards.map((card) => (
            <RecordCard key={card.label} title={card.label} meta={card.detail} right={<Pill tone="red">{card.value}</Pill>} />
          ))}
        </div>
      </Section>

      <div className="grid-two">
        <Section title="Active Workflow Runs">
          <div className="record-list">
            {schedulerRuns.map((run) => (
              <RecordCard key={run.id} title={run.workflowType} meta={`${run.createdTasks} tasks / ${run.createdAttempts} attempts`} right={<Pill tone={run.escalationCreated ? "red" : "green"}>{run.runStatus}</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Draft And Escalation Queue">
          <div className="record-list">
            <RecordCard title="Draft tasks" meta={`${autonomyDraftTasks.length} drafts, queues, or briefings prepared for owner review`} right={<Pill tone="gold">draft</Pill>} />
            <RecordCard title="Blocked attempts" meta={`${blockedAutomationAttempts.length} attempts audited without provider calls or execution`} right={<Pill tone="red">blocked</Pill>} />
            <RecordCard title="Daily briefing" meta={`${dailyCommandBriefings.length} Prime 2 briefing generated for ${latestAutonomyDailyBriefing?.briefingDate ?? "today"}`} right={<Pill>brief</Pill>} />
          </div>
        </Section>
      </div>

      <Section title="Autonomy Routes">
        <div className="grid-three">
          <RecordCard title="Rules" meta="Automation rules and autonomy levels" right={<Link href="/dashboard/autonomy/rules">Open</Link>} />
          <RecordCard title="Runs" meta="Run and attempt ledgers" right={<Link href="/dashboard/autonomy/runs">Open</Link>} />
          <RecordCard title="Tasks" meta="Agent task queues" right={<Link href="/dashboard/autonomy/tasks">Open</Link>} />
          <RecordCard title="Briefing" meta="Daily command briefing" right={<Link href="/dashboard/autonomy/daily-briefing">Open</Link>} />
          <RecordCard title="Escalations" meta="Urgent owner review queue" right={<Link href="/dashboard/autonomy/escalations">Open</Link>} />
        </div>
      </Section>
    </div>
  );
}
