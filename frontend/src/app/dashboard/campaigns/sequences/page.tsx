import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { campaignSequenceSteps } from "@/lib/demo-data";

export default function CampaignSequencesPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Sequence Prep"
        title="Draft-only campaign sequences"
        description="Sequence steps define safe purpose, template, timing offset, approval state, dry-run state, and stop condition. They do not send messages."
      />
      <Section title="Prepared Steps">
        <div className="record-list">
          {campaignSequenceSteps.map((step) => (
            <RecordCard key={step.id} title={step.messagePurpose} meta={`${step.recipientType} / ${step.timingOffsetHours}h / ${step.stopCondition}`} right={<Pill tone={step.safetyStatus === "passed" ? "green" : "red"}>{step.dryRunStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}

