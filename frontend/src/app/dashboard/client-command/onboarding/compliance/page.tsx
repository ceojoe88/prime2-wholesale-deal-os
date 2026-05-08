import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { getClientComplianceSetupChecklist } from "@/lib/demo-data";

export default function ClientCommandOnboardingCompliancePage() {
  const checklist = getClientComplianceSetupChecklist();
  return (
    <div className="page">
      <PageHeader eyebrow="CP8 Compliance Setup" title="Compliance Setup Checklist" description="Readiness checklist only - no DNC provider check or 10DLC live registration occurred." />
      <Section title="Compliance Setup Checklist Card">
        <div className="grid-two">
          <RecordCard title="Compliance posture" meta={checklist?.recommendedNextStep ?? "Review Compliance Checklist"} right={<Pill tone="gold">{checklist?.setupStatus ?? "not_started"}</Pill>} />
          <RecordCard title="Block reasons" meta={(checklist?.blockReasons ?? []).join(", ") || "No block reasons"} right={<Pill tone="green">{checklist?.noProviderCheck ? "no provider check" : "review"}</Pill>} />
        </div>
      </Section>
    </div>
  );
}
