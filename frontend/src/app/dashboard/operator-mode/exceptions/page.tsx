import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { criticalOperatorExceptions, operatorExceptionsOpen, operatorExceptionRecords } from "@/lib/demo-data";

export default function OperatorExceptionsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Exception Management"
        title="High-value and risk exceptions"
        description="Escalate only high profit potential, high compliance risk, seller ready to sign, buyer ready to offer, title/review blockers, stuck deals, forecast risk, and automation blocks."
      />

      <div className="metric-grid">
        <MetricCard label="Open exceptions" value={String(operatorExceptionsOpen.length)} detail="Owner action required" />
        <MetricCard label="Critical" value={String(criticalOperatorExceptions.length)} detail="Money or compliance priority" />
        <MetricCard label="Auto execution" value="off" detail="Recommendations only" />
        <MetricCard label="Payment handling" value="off" detail="Hard boundary" />
      </div>

      <Section title="Exception Queue">
        <div className="record-list">
          {operatorExceptionRecords.map((exception) => (
            <RecordCard
              key={exception.id}
              title={`${exception.exceptionType} / ${exception.sourceRecordId}`}
              meta={exception.reason}
              right={<Pill tone={exception.severity === "critical" ? "red" : "gold"}>{exception.severity}</Pill>}
            >
              <span className="record-meta">{exception.recommendedAction}</span>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}
