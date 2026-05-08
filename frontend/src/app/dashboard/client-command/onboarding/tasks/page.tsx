import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientOnboardingTasks } from "@/lib/demo-data";

export default function ClientCommandOnboardingTasksPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP8 Tasks" title="Onboarding Tasks" description="Deterministic activation tasks for getting the workspace operational in manual mode." />
      <Section title="Onboarding Tasks Card">
        <div className="record-list">
          {clientOnboardingTasks.map((task) => (
            <RecordCard key={task.id} title={task.taskTitle} meta={task.taskDescription} right={<Pill tone={task.priority === "urgent" ? "red" : task.priority === "high" ? "gold" : "green"}>{task.taskStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
