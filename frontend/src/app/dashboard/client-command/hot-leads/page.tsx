import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientHotLeadCards, formatCurrency } from "@/lib/demo-data";

export default function ClientHotLeadsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Hot Lead Board"
        title="Client-safe hot leads"
        description="Highest-priority client leads ranked by motivation, urgency, equity, distress, contactability, missing data, and confidence."
      />

      <div className="metric-grid">
        <MetricCard label="Hot leads" value={String(clientHotLeadCards.length)} detail="Priority score 70+" />
        <MetricCard label="Human review" value={String(clientHotLeadCards.filter((card) => card.score.requiresHumanReview).length)} detail="Client manager queue" />
        <MetricCard label="Provider actions" value="0" detail="Foundation phase only" />
        <MetricCard label="Raw payloads" value="0" detail="Sanitized views only" />
      </div>

      <Section title="Hot Lead Board">
        <div className="record-list">
          {clientHotLeadCards.map((card) => (
            <RecordCard
              key={card.lead.id}
              title={card.lead.displayName}
              meta={`${card.lead.propertyAddressSummary} | equity ${formatCurrency(card.lead.estimatedEquity)} | ${card.score.reasonSummary}`}
              right={<Link href={`/dashboard/client-command/leads/${card.lead.id}`}>Review</Link>}
            />
          ))}
          {clientHotLeadCards.length === 0 ? (
            <RecordCard title="No hot leads yet" meta="Complete missing data or import stronger client-safe lead evidence." right={<Pill tone="gold">waiting</Pill>} />
          ) : null}
        </div>
      </Section>
    </div>
  );
}
