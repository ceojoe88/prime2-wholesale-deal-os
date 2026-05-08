import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { getClientTeamSetupChecklist } from "@/lib/demo-data";

export default function ClientCommandOnboardingTeamPage() {
  const checklist = getClientTeamSetupChecklist();
  return (
    <div className="page">
      <PageHeader eyebrow="CP8 Team" title="Team Setup Checklist" description="Workspace role coverage and ownership checklist for controlled/manual Prime2 operation." />
      <Section title="Team Setup Checklist Card">
        <div className="grid-two">
          <RecordCard title="Setup status" meta={checklist?.recommendedNextStep ?? "Review Team Checklist"} right={<Pill tone="gold">{checklist?.setupStatus ?? "not_started"}</Pill>} />
          <RecordCard title="Missing roles" meta={(checklist?.missingRoles ?? []).join(", ") || "No missing roles"} right={<Pill tone="green">{String(checklist?.teamMemberCount ?? 0)} member</Pill>} />
        </div>
      </Section>
    </div>
  );
}
