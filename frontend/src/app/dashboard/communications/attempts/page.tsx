import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { blockedCommunicationAttempts, communicationSendAttempts, sentOrMockSentCommunicationAttempts } from "@/lib/demo-data";

export default function CommunicationAttemptsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Send Attempt Audit"
        title="Blocked and mock-sent attempt log"
        description="Blocked attempts are recorded without provider calls. Successful attempts can only use mock adapters in this build."
      />
      <div className="metric-grid">
        <MetricCard label="Attempts" value={String(communicationSendAttempts.length)} detail="Audited" />
        <MetricCard label="Blocked" value={String(blockedCommunicationAttempts.length)} detail="No provider call" />
        <MetricCard label="Mock-sent" value={String(sentOrMockSentCommunicationAttempts.length)} detail="Placeholder adapter" />
        <MetricCard label="Bulk detected" value={String(communicationSendAttempts.filter((attempt) => attempt.bulkSendDetected).length)} detail="Blocked" />
      </div>
      <Section title="Attempt Log">
        <table className="data-table">
          <thead><tr><th>Attempt</th><th>Draft</th><th>Recipient</th><th>Status</th><th>Provider Called</th><th>Blocks</th></tr></thead>
          <tbody>
            {communicationSendAttempts.map((attempt) => (
              <tr key={attempt.id}>
                <td>{attempt.id}<div className="record-meta">{attempt.channel}</div></td>
                <td>{attempt.draftId}<div className="record-meta">{attempt.dryRunReceiptId ?? "no dry-run"}</div></td>
                <td>{attempt.recipient}</td>
                <td><Pill tone={attempt.attemptStatus === "blocked" ? "red" : "green"}>{attempt.attemptStatus}</Pill></td>
                <td>{attempt.providerCalled ? "yes" : "no"}</td>
                <td>{attempt.blockedReasons.length ? attempt.blockedReasons.join(", ") : "clear"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
