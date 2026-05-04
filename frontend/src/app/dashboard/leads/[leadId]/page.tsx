import { notFound } from "next/navigation";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { deals, formatCurrency, getLead, leads } from "@/lib/demo-data";

export function generateStaticParams() {
  return leads.map((lead) => ({ leadId: lead.id }));
}

export default function LeadDetailPage({ params }: { params: { leadId: string } }) {
  const lead = getLead(params.leadId);
  if (!lead) notFound();
  const leadDeals = deals.filter((deal) => deal.leadId === lead.id);
  return (
    <div className="page">
      <PageHeader eyebrow={lead.sourceCategory} title={lead.sellerName} description={`${lead.address}, ${lead.city}, ${lead.state} ${lead.zipCode}`} />
      <div className="metric-grid">
        <div className="metric-card"><span>Opportunity</span><strong>{lead.opportunityScore}</strong><small>Weighted motivation score</small></div>
        <div className="metric-card"><span>Equity</span><strong>{formatCurrency(lead.estimatedEquity)}</strong><small>Estimated</small></div>
        <div className="metric-card"><span>Market demand</span><strong>{lead.marketDemand}</strong><small>Zip-level signal</small></div>
        <div className="metric-card"><span>Compliance risk</span><strong>{lead.complianceRisk}</strong><small>Escalate when elevated</small></div>
      </div>
      <div className="grid-two">
        <Section title="Seller Acquisition Drafts">
          <div className="pill-row">
            {["first call script", "SMS draft", "email draft", "objection response", "follow-up plan", "offer explanation"].map((item) => (
              <Pill key={item} tone="green">{item}</Pill>
            ))}
          </div>
        </Section>
        <Section title="Related Deals">
          <div className="record-list">
            {leadDeals.length ? leadDeals.map((deal) => (
              <RecordCard key={deal.id} title={deal.id} meta={deal.status} right={<Pill tone={deal.hot ? "green" : "gold"}>{formatCurrency(deal.projectedAssignmentFee)}</Pill>} />
            )) : <RecordCard title="No active deal yet" meta={lead.nextBestAction} />}
          </div>
        </Section>
      </div>
    </div>
  );
}
