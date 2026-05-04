import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { communicationDryRunReceipts } from "@/lib/demo-data";

export default function CommunicationDryRunsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Dry-Run Receipts"
        title="Mock provider receipts before approval"
        description="Every live-send candidate needs a dry-run receipt with recipient, source record, safety result, provider mode, timestamp, and idempotency key."
      />
      <div className="metric-grid">
        <MetricCard label="Receipts" value={String(communicationDryRunReceipts.length)} detail="Mock/dry-run only" />
        <MetricCard label="Clear" value={String(communicationDryRunReceipts.filter((receipt) => receipt.safetyResult.allowed).length)} detail="Safety passed" />
        <MetricCard label="Blocked" value={String(communicationDryRunReceipts.filter((receipt) => !receipt.safetyResult.allowed).length)} detail="Safety failed" />
        <MetricCard label="Provider calls" value="0" detail="Dry-run does not send" />
      </div>
      <Section title="Receipt Log">
        <table className="data-table">
          <thead><tr><th>Receipt</th><th>Draft</th><th>Recipient</th><th>Risk</th><th>Provider</th><th>Idempotency</th></tr></thead>
          <tbody>
            {communicationDryRunReceipts.map((receipt) => (
              <tr key={receipt.id}>
                <td>{receipt.id}<div className="record-meta">{receipt.timestamp}</div></td>
                <td>{receipt.draftId}<div className="record-meta">{receipt.sourceRecordType} / {receipt.sourceRecordId}</div></td>
                <td>{receipt.recipient}</td>
                <td><Pill tone={receipt.safetyResult.allowed ? "green" : "red"}>{receipt.riskStatus}</Pill></td>
                <td>{receipt.providerMode}</td>
                <td>{receipt.idempotencyKey}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
