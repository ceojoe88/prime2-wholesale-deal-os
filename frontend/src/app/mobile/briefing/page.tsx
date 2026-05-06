import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  doNotContactOutcomes,
  fieldTestingAccuracy,
  mobileFieldBriefingCards,
  predictionMisses,
  topLearningInsights
} from "@/lib/demo-data";

export default function MobileBriefingPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="Mobile Briefing" title="Field briefing" description="Prime 2 highlights the field-testing queue, prediction misses, DNC records, and learning insights for owner focus." />
      <div className="metric-grid">
        {mobileFieldBriefingCards.map((card) => (
          <MetricCard key={card.label} label={card.label} value={card.value} detail={card.detail} />
        ))}
      </div>
      <div className="grid-two">
        <Section title="Prediction And DNC">
          <div className="record-list">
            <RecordCard title="Prediction accuracy" meta={`${fieldTestingAccuracy}% current field loop accuracy`} right={<Pill tone="gold">estimate</Pill>} />
            <RecordCard title="Prediction misses" meta={`${predictionMisses.length} records need review`} right={<Pill tone="red">review</Pill>} />
            <RecordCard title="DNC records" meta={`${doNotContactOutcomes.length} future outreach eligibility blocks`} right={<Pill tone="red">blocked</Pill>} />
          </div>
        </Section>
        <Section title="Learning Insights">
          <div className="record-list">
            {topLearningInsights.map((memory) => (
              <RecordCard key={memory.memoryId} title={memory.memoryType} meta={memory.summary} right={<Pill>{memory.confidenceScore}</Pill>} />
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
