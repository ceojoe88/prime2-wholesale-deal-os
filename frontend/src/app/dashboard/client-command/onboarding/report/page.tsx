import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientOnboardingManagerEvents, getClientOnboardingReport } from "@/lib/demo-data";

export default function ClientCommandOnboardingReportPage() {
  const report = getClientOnboardingReport();
  return (
    <div className="page">
      <PageHeader eyebrow="CP8 Report" title="Onboarding Report" description="Client-safe onboarding report - no revenue, ROI, or deal outcome is guaranteed." />
      <Section title="Onboarding Report Card">
        <div className="grid-two">
          <RecordCard title={report?.reportTitle ?? "Onboarding report"} meta={report?.executiveSummary ?? "Generate Onboarding Report"} right={<Pill tone="green">{report?.reportStatus ?? "draft"}</Pill>} />
          <RecordCard title="Readiness summary" meta={report?.readinessSummary ?? "No readiness summary"} right={<Pill tone="gold">{report?.noLiveActionsEnabled ? "no live actions" : "review"}</Pill>} />
          <RecordCard title="Blocker summary" meta={report?.blockerSummary ?? "No blockers"} right={<Pill tone="gold">{report?.noRevenueGuarantee ? "no revenue guarantee" : "review"}</Pill>} />
          <RecordCard title="Next steps" meta={report?.nextStepsSummary ?? "No next steps"} right={<Pill tone="gold">{report?.noRoiClaim ? "no ROI claim" : "review"}</Pill>} />
        </div>
      </Section>
      <Section title="Onboarding Manager Events">
        <div className="record-list">
          {clientOnboardingManagerEvents.map((event) => (
            <RecordCard key={event.id} title={event.managerName} meta={event.eventSummary} right={<Pill tone="green">{event.eventType}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
