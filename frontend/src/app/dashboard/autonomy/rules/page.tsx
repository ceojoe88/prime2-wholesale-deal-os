import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  automationRules,
  autonomyEnabledRules,
  autonomyLevel4Rules,
  autonomyLevel5Disabled
} from "@/lib/demo-data";

export default function AutonomyRulesPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V12 Automation Rule Engine"
        title="Governed autonomy rules"
        description="Each workflow has explicit allowed prep actions, blocked real-world actions, schedule rules, and owner approval requirements."
      />

      <div className="metric-grid">
        <MetricCard label="Rules" value={String(automationRules.length)} detail="Seeded V12 workflows" />
        <MetricCard label="Enabled" value={String(autonomyEnabledRules.length)} detail="Internal prep enabled" />
        <MetricCard label="Level 4 rules" value={String(autonomyLevel4Rules.length)} detail="Owner approval required" />
        <MetricCard label="Level 5 available" value={autonomyLevel5Disabled ? "0" : "review"} detail="Disabled by design" />
      </div>

      <Section title="Rule Matrix">
        <table className="data-table">
          <thead>
            <tr>
              <th>Rule</th>
              <th>Workflow</th>
              <th>Level</th>
              <th>Trigger</th>
              <th>Schedule</th>
              <th>Owner</th>
              <th>Live</th>
            </tr>
          </thead>
          <tbody>
            {automationRules.map((rule) => (
              <tr key={rule.id}>
                <td>{rule.name}<div className="record-meta">{rule.safetyStatus}</div></td>
                <td>{rule.workflowType}</td>
                <td><Pill tone={rule.autonomyLevel === 4 ? "gold" : "green"}>L{rule.autonomyLevel}</Pill></td>
                <td>{rule.triggerEvent}</td>
                <td>{rule.scheduleLabel}</td>
                <td><Pill tone={rule.ownerApprovalRequired ? "gold" : "green"}>{rule.ownerApprovalRequired ? "required" : "not required"}</Pill></td>
                <td><Pill tone="red">{rule.liveActionAllowed ? "on" : "off"}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>

      <div className="grid-two">
        <Section title="Allowed Prep Actions">
          <div className="record-list">
            {automationRules.slice(0, 5).map((rule) => (
              <RecordCard key={rule.id} title={rule.name} meta={rule.allowedActions.join(", ")} right={<Pill tone="green">prep</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Universal Blocks">
          <div className="record-list">
            <RecordCard title="Live communication" meta="SMS, email, calls, buyer contact, bulk sends, and buyer blasts remain blocked for autonomy." right={<Pill tone="red">off</Pill>} />
            <RecordCard title="Legal execution" meta="Contracts, title submission, payment collection, binding commitments, and legal advice remain blocked." right={<Pill tone="red">off</Pill>} />
            <RecordCard title="Portal publishing" meta="Buyer and seller visibility cannot be turned on by autonomy." right={<Pill tone="red">off</Pill>} />
          </div>
        </Section>
      </div>
    </div>
  );
}
