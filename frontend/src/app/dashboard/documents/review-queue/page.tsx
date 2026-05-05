import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { documentReviewTasks } from "@/lib/demo-data";

export default function DocumentReviewQueuePage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Document Review Queue"
        title="Owner and external-review reminders"
        description="Review tasks coordinate missing data, compliance checks, buyer POF follow-up, and title/attorney reminders without sending files or changing contract state."
      />
      <Section title="Tasks">
        <div className="record-list">
          {documentReviewTasks.map((task) => (
            <RecordCard key={task.id} title={task.taskType} meta={task.reason} right={<Pill tone={task.priority === "high" ? "red" : "gold"}>{task.priority}</Pill>}>
              <p>{task.recommendedNextAction}</p>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}

