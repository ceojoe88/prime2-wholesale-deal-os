import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { cloudBackupReadiness } from "@/lib/demo-data";

export default function CloudReadinessBackupsPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="Cloud Backups" title="Backup and restore readiness" description="Backup metadata, export manifests, and restore checklists are safe metadata only; no raw secrets or private contact values are included." />
      <div className="metric-grid">
        <MetricCard label="Backup status" value={cloudBackupReadiness.status} detail="Restore test still required" />
        <MetricCard label="Restore steps" value={String(cloudBackupReadiness.restoreChecklist.length)} detail="Private recovery checklist" />
        <MetricCard label="Raw secrets" value="0" detail="Metadata only" />
        <MetricCard label="Target" value="placeholder" detail="Private path or bucket" />
      </div>
      <Section title="Restore Checklist">
        <div className="record-list">
          {cloudBackupReadiness.restoreChecklist.map((step) => (
            <RecordCard key={step} title={step} meta="Operator verification required" right={<Pill tone="gold">check</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
