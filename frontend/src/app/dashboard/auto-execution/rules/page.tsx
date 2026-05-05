import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  approvedAutoExecutionRules,
  autoExecutionRules,
  blockedAutoExecutionRules
} from "@/lib/demo-data";

export default function AutoExecutionRulesPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="V13 Rules" title="Auto-execution rule records" description="Only approved low-risk rules can participate in the conditional execution workflow." />
      <div className="metric-grid">
        <MetricCard label="Rules" value={String(autoExecutionRules.length)} detail="Controlled auto-execution records" />
        <MetricCard label="Approved" value={String(approvedAutoExecutionRules.length)} detail="Owner-approved rules" />
        <MetricCard label="Blocked" value={String(blockedAutoExecutionRules.length)} detail="Unsafe or unapproved" />
        <MetricCard label="Level 5" value="disabled" detail="Not available" />
      </div>
      <Section title="Rule Queue">
        <table className="data-table">
          <thead><tr><th>Rule</th><th>Action</th><th>Source</th><th>Recipient</th><th>Level</th><th>Risk</th><th>Status</th><th>Blocks</th></tr></thead>
          <tbody>
            {autoExecutionRules.map((rule) => (
              <tr key={rule.id}>
                <td>{rule.ruleName}<div className="record-meta">{rule.trigger}</div></td>
                <td>{rule.actionType}</td>
                <td>{rule.sourceType}</td>
                <td>{rule.allowedRecipientType}</td>
                <td><Pill tone={rule.autonomyLevel === 4 ? "gold" : "green"}>L{rule.autonomyLevel}</Pill></td>
                <td>{rule.riskScore}</td>
                <td><Pill tone={rule.status === "approved" ? "green" : "red"}>{rule.status}</Pill></td>
                <td>{rule.blockedReasons.length ? rule.blockedReasons.join(", ") : "clear"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
      <Section title="Rule Guardrails">
        <div className="grid-three">
          <RecordCard title="Approved rule required" meta="No action can execute without a matching approved rule." right={<Pill tone="green">required</Pill>} />
          <RecordCard title="Bulk and blasts" meta="Bulk campaigns, buyer blasts, and cold SMS automation remain blocked." right={<Pill tone="red">off</Pill>} />
          <RecordCard title="Legal messages" meta="Legal, contract, pressure, fake urgency, and fake buyer claim messages are blocked." right={<Pill tone="red">off</Pill>} />
        </div>
      </Section>
    </div>
  );
}
