import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { getClientFirstLeadImportChecklist } from "@/lib/demo-data";

export default function ClientCommandOnboardingFirstLeadsPage() {
  const checklist = getClientFirstLeadImportChecklist();
  return (
    <div className="page">
      <PageHeader eyebrow="CP8 First Leads" title="First 10 Leads Checklist" description="First-batch readiness and data coverage for the first controlled command cycle." />
      <Section title="First 10 Leads Checklist Card">
        <div className="grid-two">
          <RecordCard title="Lead batch status" meta={checklist?.recommendedNextStep ?? "Review First Leads Checklist"} right={<Pill tone="gold">{checklist?.importStatus ?? "not_started"}</Pill>} />
          <RecordCard title="Coverage" meta={`${checklist?.currentLeadCount ?? 0}/${checklist?.first10LeadsTarget ?? 10} leads | ${checklist?.hotLeadsCount ?? 0} hot leads`} right={<Pill tone="green">{checklist?.leadsScoredCount ?? 0} scored</Pill>} />
        </div>
      </Section>
    </div>
  );
}
