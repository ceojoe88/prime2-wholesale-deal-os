import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { approvedTemplateLibrary, approvedTemplates } from "@/lib/demo-data";

export default function AutoExecutionTemplatesPage() {
  const blockedTemplates = approvedTemplates.filter((template) => !template.approved || template.riskFlags.length > 0);
  return (
    <div className="page">
      <PageHeader eyebrow="V13 Templates" title="Approved template library" description="Seller, buyer, internal, title/review, SMS, and email templates are safety-checked before any controlled workflow can use them." />
      <div className="metric-grid">
        <MetricCard label="Templates" value={String(approvedTemplates.length)} detail="Template library records" />
        <MetricCard label="Approved" value={String(approvedTemplateLibrary.length)} detail="Can be matched to rules" />
        <MetricCard label="Blocked" value={String(blockedTemplates.length)} detail="Unsafe or unapproved" />
        <MetricCard label="SMS opt-out" value="required" detail="For SMS templates" />
      </div>
      <Section title="Template Library">
        <table className="data-table">
          <thead><tr><th>Template</th><th>Type</th><th>Channel</th><th>Recipient</th><th>Safety</th><th>Opt-out</th><th>Flags</th></tr></thead>
          <tbody>
            {approvedTemplates.map((template) => (
              <tr key={template.id}>
                <td>{template.templateName}<div className="record-meta">{template.subject || "SMS/no subject"}</div></td>
                <td>{template.templateType}</td>
                <td>{template.channel}</td>
                <td>{template.recipientType}</td>
                <td><Pill tone={template.safetyStatus === "approved" ? "green" : "red"}>{template.safetyStatus}</Pill></td>
                <td><Pill tone={!template.requiresOptOut || template.includesOptOut ? "green" : "red"}>{template.requiresOptOut ? (template.includesOptOut ? "included" : "missing") : "n/a"}</Pill></td>
                <td>{template.riskFlags.length ? template.riskFlags.join(", ") : "clear"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
      <Section title="Blocked Language">
        <div className="grid-three">
          <RecordCard title="Pressure" meta="No must-sign-now or last-chance language." right={<Pill tone="red">blocked</Pill>} />
          <RecordCard title="Fake claims" meta="No fake urgency or fake buyer claims." right={<Pill tone="red">blocked</Pill>} />
          <RecordCard title="Legal/contract" meta="No legal advice, contract execution, or guarantee language." right={<Pill tone="red">blocked</Pill>} />
        </div>
      </Section>
    </div>
  );
}
