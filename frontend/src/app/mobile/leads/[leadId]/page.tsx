import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { fieldCallOutcomes, formatCurrency, getLead, leads, mobileOperatorNotes } from "@/lib/demo-data";

export function generateStaticParams() {
  return leads.map((lead) => ({ leadId: lead.id }));
}

export default function MobileLeadDetailPage({ params }: { params: { leadId: string } }) {
  const lead = getLead(params.leadId);
  if (!lead) notFound();
  const outcomes = fieldCallOutcomes.filter((outcome) => outcome.leadId === lead.id);
  const notes = mobileOperatorNotes.filter((note) => note.sourceRecordId === lead.id);
  return (
    <div className="page">
      <PageHeader eyebrow="Mobile Lead" title={lead.sellerName} description={`${lead.address}, ${lead.city}, ${lead.state} ${lead.zipCode}`} />
      <div className="metric-grid">
        <MetricCard label="Opportunity" value={String(lead.opportunityScore)} detail="Prime 2 score" />
        <MetricCard label="Equity" value={formatCurrency(lead.estimatedEquity)} detail="Estimate from source data" />
        <MetricCard label="Motivation" value={String(lead.motivationScore)} detail="Updated by field outcomes" />
        <MetricCard label="Contactability" value={String(lead.contactabilityScore)} detail="DNC can reduce to zero" />
      </div>
      <div className="grid-two">
        <Section title="Quick Capture Slots">
          <div className="record-list">
            {["call outcome", "seller note", "buyer response note", "DNC mark", "follow-up date", "transcript paste"].map((item) => (
              <RecordCard key={item} title={item} meta="Captured for owner review; no provider action" right={<Pill tone="gold">capture</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Recent Outcomes And Notes">
          <div className="record-list">
            {outcomes.map((outcome) => (
              <RecordCard key={outcome.id} title={outcome.contactResult} meta={outcome.prime2NextRecommendation} right={<Pill tone={outcome.doNotContact ? "red" : "green"}>{outcome.outreachEligibilityStatus}</Pill>} />
            ))}
            {notes.map((note) => (
              <RecordCard key={note.id} title={note.noteType} meta={note.body} right={<Pill>{note.syncStatus}</Pill>} />
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
