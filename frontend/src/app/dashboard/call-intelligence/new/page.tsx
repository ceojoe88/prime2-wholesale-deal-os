import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";

export default function NewCallIntelligencePage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Analysis Intake"
        title="New call intelligence session"
        description="Manual notes and pasted transcript text can be reviewed into structured signals. Audio capture and live calling are outside this layer."
      />

      <Section title="Supported Inputs">
        <div className="grid-three">
          <RecordCard title="Manual notes" meta="Operator-entered call notes" right={<Pill tone="green">allowed</Pill>} />
          <RecordCard title="Pasted transcript" meta="Text transcript intake" right={<Pill tone="green">allowed</Pill>} />
          <RecordCard title="Linked call outcome" meta="Connects to V19 outcome records" right={<Pill tone="green">allowed</Pill>} />
          <RecordCard title="Audio processing" meta="Not added in V23" right={<Pill tone="red">off</Pill>} />
          <RecordCard title="Live call path" meta="No call execution inside the system" right={<Pill tone="red">off</Pill>} />
          <RecordCard title="Live response" meta="V5/V13 gates required elsewhere" right={<Pill tone="red">off</Pill>} />
        </div>
      </Section>
    </div>
  );
}

