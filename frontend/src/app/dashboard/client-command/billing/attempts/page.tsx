import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientBillingAttempts } from "@/lib/demo-data";

export default function ClientCommandBillingAttemptsPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP11 Attempts" title="Controlled Billing Attempts" description="Billing gate only - no payment occurs unless all billing gates pass." />
      <Section title="Attempt Log">
        <div className="record-list">
          {clientBillingAttempts.map((attempt) => (
            <RecordCard
              key={attempt.id}
              title={attempt.attemptType}
              meta={`${attempt.requestSummary} Blockers: ${attempt.blockReasons.join(", ") || "none"}.`}
              right={<Pill tone={attempt.attemptStatus === "blocked" ? "red" : "green"}>{attempt.attemptStatus}</Pill>}
            />
          ))}
        </div>
      </Section>
    </div>
  );
}
