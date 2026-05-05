import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { fieldCallOutcomes, getCallOutcome } from "@/lib/demo-data";

export function generateStaticParams() {
  return fieldCallOutcomes.map((outcome) => ({ outcomeId: outcome.id }));
}

export default async function CallOutcomeDetailPage({
  params
}: {
  params: Promise<{ outcomeId: string }>;
}) {
  const { outcomeId } = await params;
  const outcome = getCallOutcome(outcomeId);
  if (!outcome) notFound();

  return (
    <div className="page">
      <PageHeader
        eyebrow={outcome.contactResult}
        title={outcome.id}
        description="Call outcome records compare field reality against Prime 2 scoring. They do not place calls or trigger follow-up."
      />

      <div className="metric-grid">
        <MetricCard label="Lead" value={outcome.leadId} detail={outcome.callDatetime} />
        <MetricCard label="Seller temp" value={String(outcome.sellerTemperature)} detail="Manual outcome score" />
        <MetricCard label="DNC" value={outcome.doNotContact ? "yes" : "no"} detail={outcome.outreachEligibilityStatus} />
        <MetricCard label="Live call" value="off" detail="Recorded only" />
      </div>

      <div className="grid-two">
        <Section title="Conversation Notes">
          <div className="record-list">
            <RecordCard title="Motivation" meta={outcome.motivationNotes || "No motivation notes"} />
            <RecordCard title="Timeline" meta={outcome.timeline || "No timeline captured"} />
            <RecordCard title="Condition" meta={outcome.propertyConditionNotes || "No condition notes"} />
          </div>
        </Section>
        <Section title="Prime 2 Recommendation">
          <RecordCard title="Next step" meta={outcome.prime2NextRecommendation} right={<Pill tone="gold">owner review</Pill>} />
        </Section>
      </div>
    </div>
  );
}
