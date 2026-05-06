import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { playbookRecommendations } from "@/lib/demo-data";

export default function PlaybookRecommendationsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Playbook Recommendations"
        title="Evidence-backed draft playbooks"
        description="Playbooks turn approved memory into safer draft recommendations for sellers, buyers, documents, and campaigns without creating commitments."
      />
      <Section title="Playbooks">
        <div className="record-list">
          {playbookRecommendations.map((playbook) => (
            <RecordCard key={playbook.playbookId} title={playbook.playbookType} meta={`${playbook.targetContext} / ${playbook.recommendation}`} right={<Pill tone={playbook.status === "approved" ? "green" : "gold"}>{playbook.status}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
