import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientActivationBlockers,
  clientOnboardingTasks,
  clientOnboardingTimelineEvents,
  getClientFirstWeeklyCycleReadiness,
  getClientGoLiveGate
} from "@/lib/demo-data";

export default function ClientCommandOnboardingActivationBoardPage() {
  const gate = getClientGoLiveGate();
  const firstWeekly = getClientFirstWeeklyCycleReadiness();
  return (
    <div className="page">
      <PageHeader eyebrow="CP8 Activation Board" title="Workspace Activation Board" description="Manual operation readiness only - no live communication, provider execution, billing, contracts, or campaigns are enabled." />
      <Section title="Go-Live Readiness Gate Card">
        <div className="grid-two">
          <RecordCard title="Readiness gate" meta={gate?.clientSafeSummary ?? "Check Manual Readiness"} right={<Pill tone={gate?.gateStatus === "ready_for_manual_operation" ? "green" : "gold"}>{gate?.gateStatus ?? "review"}</Pill>} />
          <RecordCard title="First weekly cycle" meta={firstWeekly?.recommendedNextStep ?? "Review first weekly cycle"} right={<Pill tone={firstWeekly?.readyForFirstWeeklyCycle ? "green" : "gold"}>{firstWeekly?.readyForFirstWeeklyCycle ? "ready" : "review"}</Pill>} />
        </div>
      </Section>
      <Section title="Activation Blockers">
        <div className="record-list">
          {clientActivationBlockers.map((blocker) => (
            <RecordCard key={blocker.id} title={blocker.blockerType} meta={blocker.blockerSummary} right={<Pill tone="gold">{blocker.affectedArea}</Pill>} />
          ))}
        </div>
      </Section>
      <Section title="Onboarding Tasks">
        <div className="record-list">
          {clientOnboardingTasks.map((task) => (
            <RecordCard key={task.id} title={task.taskTitle} meta={task.taskDescription} right={<Pill tone="green">{task.ownerRole}</Pill>} />
          ))}
        </div>
      </Section>
      <Section title="Onboarding Timeline">
        <div className="record-list">
          {clientOnboardingTimelineEvents.map((event) => (
            <RecordCard key={event.id} title={event.milestoneName} meta={event.eventSummary} right={<Pill tone="green">{event.progressPercent}%</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
