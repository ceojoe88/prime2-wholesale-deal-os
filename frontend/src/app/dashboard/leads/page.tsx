import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { formatCurrency, leads } from "@/lib/demo-data";

export default function LeadsPage() {
  const hot = leads.filter((lead) => lead.opportunityScore >= 80);
  const followups = leads.filter((lead) => lead.stage === "follow_up");
  return (
    <div className="page">
      <PageHeader
        eyebrow="Lead Intelligence"
        title="Motivated seller lead board"
        description="CSV-ready demo leads are scored for motivation, distress, equity, urgency, contactability, seller temperature, data confidence, and market demand."
      />
      <div className="metric-grid">
        <MetricCard label="Total leads" value={String(leads.length)} detail="Seeded source categories" />
        <MetricCard label="80+ opportunity" value={String(hot.length)} detail="High-priority research" />
        <MetricCard label="Follow-ups" value={String(followups.length)} detail="Draft-only timing" />
        <MetricCard label="Avg equity" value={formatCurrency(Math.round(leads.reduce((sum, lead) => sum + lead.estimatedEquity, 0) / leads.length))} detail="Estimated demo equity" />
      </div>
      <Section title="Lead Pipeline">
        <table className="data-table">
          <thead>
            <tr>
              <th>Seller</th>
              <th>Source</th>
              <th>Stage</th>
              <th>Equity</th>
              <th>Opportunity</th>
              <th>Risk</th>
            </tr>
          </thead>
          <tbody>
            {leads.map((lead) => (
              <tr key={lead.id}>
                <td><Link href={`/dashboard/leads/${lead.id}`}>{lead.sellerName}</Link><div className="record-meta">{lead.address}</div></td>
                <td>{lead.sourceCategory}<div className="record-meta">{lead.zipCode}</div></td>
                <td><Pill>{lead.stage}</Pill></td>
                <td className="money">{formatCurrency(lead.estimatedEquity)}</td>
                <td>{lead.opportunityScore}</td>
                <td><Pill tone={lead.complianceRisk > 35 ? "red" : "gold"}>{lead.complianceRisk}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
