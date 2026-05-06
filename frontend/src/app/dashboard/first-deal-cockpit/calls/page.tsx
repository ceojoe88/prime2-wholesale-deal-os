import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  fieldCallOutcomes,
  firstDealCallChecklist,
  firstDealCallPriorityLeads,
  firstDealTopImportedLeads
} from "@/lib/demo-data";

export default function FirstDealCallsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V31 Seller Call Workflow"
        title="Guided seller call board"
        description="Use the checklist while the owner performs calls outside the system, then log outcomes, DNC requests, follow-up timing, and seller notes."
      />
      <div className="metric-grid">
        <MetricCard label="Call queue" value={String(firstDealTopImportedLeads.length)} detail="Imported QA rows" />
        <MetricCard label="Priority" value={String(firstDealCallPriorityLeads.length)} detail="Prime 2 call-first rows" />
        <MetricCard label="Logged calls" value={String(fieldCallOutcomes.length)} detail="Owner-entered outcomes" />
        <MetricCard label="System calling" value="off" detail="Capture and guidance only" />
      </div>
      <div className="grid-two">
        <Section title="Guided Checklist">
          <div className="record-list">
            {firstDealCallChecklist.map((item) => (
              <RecordCard key={item} title={item} meta="Required capture item" right={<Pill tone="green">check</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Top Call Queue">
          <div className="record-list">
            {firstDealTopImportedLeads.map((lead) => (
              <RecordCard key={lead.id} title={lead.ownerName} meta={`${lead.property} / ${lead.recommendedNextAction}`} right={<Pill tone={lead.blockedReasons.length ? "gold" : "green"}>{lead.qaScore}</Pill>} />
            ))}
            <RecordCard title="Mobile queue" meta="Same owner field view" right={<Link href="/mobile/calls">Open</Link>} />
          </div>
        </Section>
      </div>
    </div>
  );
}

