import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientPilotHealthSnapshots, clientPilotRiskReviews } from "@/lib/demo-data";

export default function ClientCommandPilotNeedsReviewPage() {
  const needsReview = [
    ...clientPilotHealthSnapshots.filter((item) => item.healthStatus === "needs_review" || item.healthStatus === "watch"),
    ...clientPilotRiskReviews.filter((item) => item.riskStatus !== "healthy")
  ];

  return (
    <div className="page">
      <PageHeader eyebrow="CP12 Needs Review" title="Pilot Needs Review" description="Admin support can review and route issues, but cannot force live actions." />
      <Section title="Needs Review">
        <div className="record-list">
          {needsReview.map((item) => (
            <RecordCard key={item.id} title={"healthStatus" in item ? item.healthStatus : item.riskStatus} meta={"summary" in item ? item.summary : item.clientSafeSummary} right={<Pill tone="gold">review</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
