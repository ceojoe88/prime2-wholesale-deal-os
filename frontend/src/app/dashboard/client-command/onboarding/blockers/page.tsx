import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientActivationBlockers } from "@/lib/demo-data";

export default function ClientCommandOnboardingBlockersPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP8 Blockers" title="Activation Blockers" description="What still blocks controlled/manual Prime2 operation and the first weekly command cycle." />
      <Section title="Activation Blockers Card">
        <div className="record-list">
          {clientActivationBlockers.map((blocker) => (
            <RecordCard key={blocker.id} title={blocker.blockerType} meta={blocker.blockerSummary} right={<Pill tone={blocker.severity === "critical" ? "red" : blocker.severity === "high" ? "gold" : "green"}>{blocker.severity}</Pill>}>
              <p>{blocker.recommendedFix}</p>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}
