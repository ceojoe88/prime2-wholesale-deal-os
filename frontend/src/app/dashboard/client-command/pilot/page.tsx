import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientPilotClientSafeUpdates,
  clientPilotEscalations,
  clientPilotEvents,
  clientPilotHealthSnapshots,
  clientPilotLaunchChecklists,
  clientPilotOperatingModes,
  clientPilotOutcomeCheckpoints,
  clientPilotPrograms,
  clientPilotRiskReviews,
  clientPilotSupportActions,
  clientPilotSupportTickets,
  clientPilotWorkspaceEnrollments
} from "@/lib/demo-data";

const cp12Guardrails = [
  {
    title: "Source gates",
    meta: "Pilot enrollment never clears upstream blockers on its own.",
    detail: "Pilot mode does not bypass source gates.",
    tone: "red" as const
  },
  {
    title: "Support routing",
    meta: "Support teams can help route work without unlocking live actions.",
    detail: "Admin support can review and route issues, but cannot force live actions.",
    tone: "gold" as const
  },
  {
    title: "Client-safe update policy",
    meta: "Visible updates stay sanitized for customer review.",
    detail: "Client-safe updates hide internal governance, provider payloads, and admin notes.",
    tone: "green" as const
  },
  {
    title: "Controlled live posture",
    meta: "Pilot health stays downstream from plan, communication, and billing gates.",
    detail: "Controlled live posture requires CP9, CP10, and CP11 gates.",
    tone: "gold" as const
  }
];

export default function ClientCommandPilotPage() {
  const openTickets = clientPilotSupportTickets.filter((ticket) => ticket.status === "open");
  const openEscalations = clientPilotEscalations.filter((item) => item.escalationStatus === "open");
  const blockedRiskReviews = clientPilotRiskReviews.filter((review) => review.riskStatus === "blocked");

  return (
    <div className="page">
      <PageHeader
        eyebrow="CP12 Pilot"
        title="Pilot mode and support routing"
        description="Client-safe pilot enrollment, health review, support routing, and sanitized status updates."
      />

      <div className="metric-grid">
        <MetricCard label="Pilot programs" value={String(clientPilotPrograms.length)} detail="Controlled workspace cohorts" />
        <MetricCard label="Open tickets" value={String(openTickets.length)} detail="Support routing only" />
        <MetricCard label="Escalations" value={String(openEscalations.length)} detail="Human review required" />
        <MetricCard label="Risk blocks" value={String(blockedRiskReviews.length)} detail="Controlled live posture still blocked" />
      </div>

      <Section title="Pilot Guardrails">
        <div className="record-list">
          {cp12Guardrails.map((item) => (
            <RecordCard key={item.title} title={item.title} meta={item.meta} right={<Pill tone={item.tone}>guarded</Pill>}>
              <p>{item.detail}</p>
            </RecordCard>
          ))}
        </div>
      </Section>

      <Section title="Pilot Health">
        <div className="grid-two">
          {clientPilotPrograms.map((program) => (
            <RecordCard key={program.id} title={program.programName} meta={program.clientSafeSummary} right={<Pill tone={program.programStatus === "active" ? "green" : "gold"}>{program.programStatus}</Pill>} />
          ))}
          {clientPilotWorkspaceEnrollments.map((enrollment) => (
            <RecordCard key={enrollment.id} title={enrollment.pilotMode} meta={enrollment.clientSafeSummary} right={<Pill tone={enrollment.enrollmentStatus === "active" ? "green" : "gold"}>{enrollment.enrollmentStatus}</Pill>}>
              <div className="tag-row">
                <Pill tone="green">{enrollment.supportOwnerName}</Pill>
              </div>
            </RecordCard>
          ))}
          {clientPilotOperatingModes.map((mode) => (
            <RecordCard key={mode.id} title={mode.operatingPosture.replaceAll("_", " ")} meta={mode.reasonSummary} right={<Pill tone={mode.requiresHumanReview ? "gold" : "green"}>{mode.pilotMode}</Pill>}>
              <p>{mode.noGateBypass ? "Pilot mode does not bypass source gates." : "Pilot posture needs review."}</p>
            </RecordCard>
          ))}
          {clientPilotHealthSnapshots.map((snapshot) => (
            <RecordCard key={snapshot.id} title={`Health: ${snapshot.healthStatus}`} meta={snapshot.clientSafeSummary} right={<Pill tone={snapshot.healthStatus === "watch" ? "gold" : "green"}>{snapshot.weeklyReportStatus}</Pill>}>
              <div className="tag-row">
                <Pill tone="green">{snapshot.planStatus}</Pill>
                <Pill tone={snapshot.communicationStatus === "blocked" ? "red" : "green"}>{snapshot.communicationStatus}</Pill>
                <Pill tone={snapshot.billingStatus === "blocked" ? "red" : "green"}>{snapshot.billingStatus}</Pill>
                <Pill tone={snapshot.complianceStatus === "needs_review" ? "gold" : "green"}>{snapshot.complianceStatus}</Pill>
              </div>
            </RecordCard>
          ))}
          {clientPilotLaunchChecklists.map((checklist) => (
            <RecordCard key={checklist.id} title="Pilot launch checklist" meta={checklist.clientSafeSummary} right={<Pill tone={checklist.checklistStatus === "blocked" ? "gold" : "green"}>{checklist.checklistStatus}</Pill>}>
              <div className="tag-row">
                <Pill tone={checklist.onboardingReady ? "green" : "gold"}>{checklist.onboardingReady ? "onboarding ready" : "onboarding pending"}</Pill>
                <Pill tone={checklist.planAssigned ? "green" : "gold"}>{checklist.planAssigned ? "plan assigned" : "plan pending"}</Pill>
                <Pill tone={checklist.complianceAcceptable ? "green" : "gold"}>{checklist.complianceAcceptable ? "compliance ready" : "compliance review"}</Pill>
              </div>
            </RecordCard>
          ))}
          {clientPilotRiskReviews.map((review) => (
            <RecordCard key={review.id} title="Risk review" meta={review.summary} right={<Pill tone={review.riskStatus === "blocked" ? "red" : "green"}>{review.riskStatus}</Pill>}>
              <div className="tag-row">
                {review.criticalBlockers.map((blocker) => (
                  <Pill key={blocker} tone="red">
                    {blocker}
                  </Pill>
                ))}
              </div>
            </RecordCard>
          ))}
        </div>
      </Section>

      <Section title="Support Routing">
        <div className="record-list">
          {clientPilotSupportTickets.map((ticket) => (
            <RecordCard key={ticket.id} title={ticket.title} meta={ticket.summary} right={<Pill tone={ticket.priority === "high" ? "red" : "gold"}>{ticket.priority}</Pill>}>
              <div className="tag-row">
                <Pill tone="green">{ticket.ticketType}</Pill>
                <Pill tone="green">{ticket.assignedTo}</Pill>
                <Pill tone="green">{ticket.status}</Pill>
              </div>
            </RecordCard>
          ))}
          {clientPilotSupportActions.map((action) => (
            <RecordCard key={action.id} title={action.ownerRole.replaceAll("_", " ")} meta={action.actionSummary} right={<Pill tone={action.clientVisible ? "green" : "gold"}>{action.actionStatus}</Pill>}>
              <p>Admin support can review and route issues, but cannot force live actions.</p>
            </RecordCard>
          ))}
          {clientPilotEscalations.map((escalation) => (
            <RecordCard key={escalation.id} title={escalation.sourceDomain} meta={escalation.escalationReason} right={<Pill tone={escalation.requiresHumanReview ? "gold" : "green"}>{escalation.escalationStatus}</Pill>}>
              <div className="tag-row">
                <Pill tone="green">{escalation.escalationType}</Pill>
                <Pill tone="green">{escalation.sourceRecordId}</Pill>
              </div>
            </RecordCard>
          ))}
        </div>
      </Section>

      <Section title="Client-safe Updates">
        <div className="record-list">
          {clientPilotClientSafeUpdates.map((update) => (
            <RecordCard key={update.id} title={update.updateTitle} meta={update.updateSummary} right={<Pill tone={update.status === "client_visible" ? "green" : "gold"}>{update.status}</Pill>}>
              <p>{update.clientSafeSummary}</p>
            </RecordCard>
          ))}
          {clientPilotOutcomeCheckpoints.map((checkpoint) => (
            <RecordCard key={checkpoint.id} title={checkpoint.checkpointName} meta={checkpoint.summary} right={<Pill tone={checkpoint.clientSafe ? "green" : "gold"}>{checkpoint.checkpointStatus}</Pill>} />
          ))}
          {clientPilotEvents.map((event) => (
            <RecordCard key={event.id} title={event.eventType.replaceAll("_", " ")} meta={event.eventSummary} right={<Pill tone={event.clientVisible ? "green" : "gold"}>{event.clientVisible ? "visible" : "internal"}</Pill>} />
          ))}
        </div>
      </Section>

      <Section title="Command Links">
        <div className="grid-three">
          <RecordCard title="Plans" meta="CP9 plan assignment and gating" right={<Link href="/dashboard/client-command/plans">Open</Link>} />
          <RecordCard title="Communication" meta="CP10 controlled live messaging" right={<Link href="/dashboard/client-command/communication">Open</Link>} />
          <RecordCard title="Billing" meta="CP11 billing live-readiness" right={<Link href="/dashboard/client-command/billing">Open</Link>} />
          <RecordCard title="Workspaces" meta="CP1 workspace setup context" right={<Link href="/dashboard/client-command/workspaces">Open</Link>} />
          <RecordCard title="Onboarding" meta="CP8 readiness and blockers" right={<Link href="/dashboard/client-command/onboarding">Open</Link>} />
          <RecordCard title="Reports" meta="Weekly client-safe report outputs" right={<Link href="/dashboard/client-command/reports">Open</Link>} />
        </div>
      </Section>
    </div>
  );
}
