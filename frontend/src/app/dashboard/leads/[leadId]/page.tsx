import { notFound } from "next/navigation";
import { deals, formatCurrency, getLead, leads } from "@/lib/demo-data";

export function generateStaticParams() {
  return leads.map((lead) => ({ leadId: lead.id }));
}

export default async function LeadDetailPage({ params }: { params: Promise<{ leadId: string }> }) {
  const { leadId } = await params;
  const lead = getLead(leadId);
  if (!lead) notFound();
  const leadDeals = deals.filter((deal) => deal.leadId === lead.id);
  return (
    <div className="page">
      <header className="page-header">
        <span className="eyebrow">{lead.sourceCategory}</span>
        <h2>{lead.sellerName}</h2>
        <p>{`${lead.address}, ${lead.city}, ${lead.state} ${lead.zipCode}`}</p>
      </header>
      <div className="metric-grid">
        <div className="metric-card"><span>Opportunity</span><strong>{lead.opportunityScore}</strong><small>Weighted motivation score</small></div>
        <div className="metric-card"><span>Equity</span><strong>{formatCurrency(lead.estimatedEquity)}</strong><small>Estimated</small></div>
        <div className="metric-card"><span>Market demand</span><strong>{lead.marketDemand}</strong><small>Zip-level signal</small></div>
        <div className="metric-card"><span>Compliance risk</span><strong>{lead.complianceRisk}</strong><small>Escalate when elevated</small></div>
      </div>
      <div className="grid-two">
        <section className="surface">
          <div className="section-title">
            <h3>Seller Acquisition Drafts</h3>
          </div>
          <div className="pill-row">
            {["first call script", "SMS draft", "email draft", "objection response", "follow-up plan", "offer explanation"].map((item) => (
              <span key={item} className="pill green">{item}</span>
            ))}
          </div>
        </section>
        <section className="surface">
          <div className="section-title">
            <h3>Related Deals</h3>
          </div>
          <div className="record-list">
            {leadDeals.length ? leadDeals.map((deal) => (
              <article key={deal.id} className="record-card">
                <div className="record-head">
                  <div className="compact">
                    <h3>{deal.id}</h3>
                    <span className="record-meta">{deal.status}</span>
                  </div>
                  <span className={`pill ${deal.hot ? "green" : "gold"}`}>{formatCurrency(deal.projectedAssignmentFee)}</span>
                </div>
              </article>
            )) : (
              <article className="record-card">
                <div className="record-head">
                  <div className="compact">
                    <h3>No active deal yet</h3>
                    <span className="record-meta">{lead.nextBestAction}</span>
                  </div>
                </div>
              </article>
            )}
          </div>
        </section>
      </div>
    </div>
  );
}
