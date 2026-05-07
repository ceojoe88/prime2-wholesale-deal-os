import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientWeeklyRecommendedActions } from "@/lib/demo-data";

export default function ClientCommandReportsRecommendedActionsPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP7 Actions" title="Recommended Actions" description="Client-safe weekly report - no revenue, ROI, or deal outcome is guaranteed." />
      <Section title="Recommended Next Actions">
        <div className="record-list">
          {clientWeeklyRecommendedActions.map((action) => (
            <RecordCard key={action.id} title={action.actionType} meta={action.actionSummary} right={<Pill tone={action.priority === "urgent" ? "red" : action.priority === "high" ? "gold" : "green"}>{action.dueWindow}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
