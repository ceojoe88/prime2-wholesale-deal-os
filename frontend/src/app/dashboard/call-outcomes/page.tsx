import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  doNotContactOutcomes,
  fieldCallOutcomes,
  motivatedFieldOutcomes
} from "@/lib/demo-data";

export default function CallOutcomesPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V19 Field Calls"
        title="Call outcome tracking"
        description="The operator records seller call results manually. Prime 2 adjusts internal scores, queues draft-only follow-up work, and blocks do-not-contact leads."
      />

      <div className="metric-grid">
        <MetricCard label="Outcomes" value={String(fieldCallOutcomes.length)} detail="Manual operator records" />
        <MetricCard label="Motivated" value={String(motivatedFieldOutcomes.length)} detail="Escalated to seller acquisition" />
        <MetricCard label="Do not contact" value={String(doNotContactOutcomes.length)} detail="Future live outreach blocked" />
        <MetricCard label="System calls" value="0" detail="No live calling exists" />
      </div>

      <Section title="Outcome Log">
        <div className="record-list">
          {fieldCallOutcomes.map((outcome) => (
            <RecordCard
              key={outcome.id}
              title={outcome.contactResult}
              meta={`${outcome.leadId} | ${outcome.prime2NextRecommendation}`}
              right={<Link href={`/dashboard/call-outcomes/${outcome.id}`}>Open</Link>}
            />
          ))}
        </div>
      </Section>

      <Section title="Safety Boundary">
        <div className="grid-three">
          <RecordCard title="System call capability" meta="No live calling inside the app" right={<Pill tone="green">none</Pill>} />
          <RecordCard title="Do-not-contact" meta="Blocks future live outreach eligibility" right={<Pill tone="green">enforced</Pill>} />
          <RecordCard title="Escalation" meta="Creates internal review tasks only" right={<Pill tone="gold">draft-only</Pill>} />
        </div>
      </Section>
    </div>
  );
}
