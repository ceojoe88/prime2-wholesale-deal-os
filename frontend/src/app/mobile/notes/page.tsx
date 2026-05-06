import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { mobileOfflineDrafts, mobileOperatorNotes } from "@/lib/demo-data";

export default function MobileNotesPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="Mobile Notes" title="Offline-safe draft capture" description="Field notes, transcript paste, buyer response notes, and document metadata are captured as drafts until reviewed inside the private operator system." />
      <div className="metric-grid">
        <MetricCard label="Notes" value={String(mobileOperatorNotes.length)} detail="Owner review records" />
        <MetricCard label="Offline drafts" value={String(mobileOfflineDrafts.length)} detail="Idempotent sync queue" />
        <MetricCard label="Provider called" value="0" detail="Draft capture only" />
        <MetricCard label="Action taken" value="0" detail="Review before movement" />
      </div>
      <div className="grid-two">
        <Section title="Recent Notes">
          <div className="record-list">
            {mobileOperatorNotes.map((note) => (
              <RecordCard key={note.id} title={note.noteType} meta={note.body} right={<Pill>{note.syncStatus}</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Offline Drafts">
          <div className="record-list">
            {mobileOfflineDrafts.map((draft) => (
              <RecordCard key={draft.id} title={draft.draftType} meta={draft.idempotencyKey} right={<Pill tone="gold">{draft.syncStatus}</Pill>} />
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
