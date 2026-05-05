import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { backupExportRecords, safeBackupExports } from "@/lib/demo-data";

export default function BackupsPage() {
  const excludedCount = backupExportRecords.reduce((sum, backup) => sum + backup.excludedFields.length, 0);

  return (
    <div className="page">
      <PageHeader
        eyebrow="V18 Backup / Export Tools"
        title="Safe backup metadata"
        description="Backup records expose metadata, table scope, excluded private fields, and restore-test status. Raw seller, buyer, provider, and internal strategy data stay out of unsafe exports."
      />

      <div className="metric-grid">
        <MetricCard label="Backups" value={String(backupExportRecords.length)} detail="Prepared metadata records" />
        <MetricCard label="Safe metadata" value={String(safeBackupExports.length)} detail="No raw private data" />
        <MetricCard label="Excluded fields" value={String(excludedCount)} detail="Private and secret fields omitted" />
        <MetricCard label="Restore tests" value="pending" detail="Operator verification needed" />
      </div>

      <Section title="Backup Records">
        <table className="data-table">
          <thead>
            <tr>
              <th>Backup</th>
              <th>Scope</th>
              <th>Tables</th>
              <th>Private Data</th>
              <th>Approval</th>
            </tr>
          </thead>
          <tbody>
            {backupExportRecords.map((backup) => (
              <tr key={backup.id}>
                <td>{backup.id}<div className="record-meta">{backup.backupType}</div></td>
                <td>{backup.backupScope}</td>
                <td>{backup.includedTables.length}</td>
                <td><Pill tone={backup.containsRawPrivateData ? "red" : "green"}>{backup.containsRawPrivateData ? "blocked" : "none"}</Pill></td>
                <td>{backup.ownerApprovalStatus}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>

      <Section title="Excluded Fields">
        <div className="grid-three">
          {Array.from(new Set(backupExportRecords.flatMap((backup) => backup.excludedFields))).map((field) => (
            <RecordCard key={field} title={field} meta="Omitted from backup/export metadata" right={<Pill tone="green">excluded</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
