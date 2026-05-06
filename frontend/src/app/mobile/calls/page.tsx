import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { doNotContactOutcomes, mobileCallQueue, motivatedFieldOutcomes } from "@/lib/demo-data";

export default function MobileCallsPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="Mobile Calls" title="Call outcome capture" description="Use this field view to record outcomes, DNC marks, follow-up dates, objections, and call notes. Prime 2 routes the result internally." />
      <div className="metric-grid">
        <MetricCard label="Call queue" value={String(mobileCallQueue.length)} detail="Owner field planning" />
        <MetricCard label="Motivated found" value={String(motivatedFieldOutcomes.length)} detail="Escalated internally" />
        <MetricCard label="DNC records" value={String(doNotContactOutcomes.length)} detail="Eligibility blocked" />
        <MetricCard label="System dialing" value="off" detail="No phone action here" />
      </div>
      <Section title="Call Queue">
        <div className="record-list">
          {mobileCallQueue.map((lead) => (
            <RecordCard key={lead.id} title={lead.sellerName} meta={`${lead.city}, ${lead.state} / ${lead.nextBestAction}`} right={<Link href={`/mobile/leads/${lead.id}`}><Pill tone="green">{lead.opportunityScore}</Pill></Link>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
