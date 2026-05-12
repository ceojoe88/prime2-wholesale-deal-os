import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientPilotRiskReviews } from "@/lib/demo-data";

export default function ClientCommandPilotRiskReviewPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP12 Risk Review" title="Pilot Risk Review" description="Controlled live posture requires CP9, CP10, and CP11 gates." />
      <Section title="Risk Reviews">
        <div className="record-list">
          {clientPilotRiskReviews.map((item) => (
            <RecordCard key={item.id} title={item.riskStatus} meta={item.summary} right={<Pill tone={item.riskStatus === "blocked" ? "red" : "gold"}>{item.escalationRequired ? "escalate" : "watch"}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
