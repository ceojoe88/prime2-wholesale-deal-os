import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  dealsNeedingPriceAdjustment,
  formatCurrency,
  getDeal,
  getLead,
  highReadinessNegotiations,
  negotiationRecords,
  stalledNegotiations
} from "@/lib/demo-data";

export default function NegotiationsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V10 Negotiation Tracking"
        title="Seller acceptance readiness"
        description="Track seller responses, objections, counters, emotional signals, stage, and next move recommendations without live negotiation automation."
      />
      <div className="metric-grid">
        <MetricCard label="Negotiations" value={String(negotiationRecords.length)} detail="Tracked seller conversion records" />
        <MetricCard label="High readiness" value={String(highReadinessNegotiations.length)} detail="High or contract-ready score" />
        <MetricCard label="Stalled" value={String(stalledNegotiations.length)} detail="Needs hold, explanation, or disengage" />
        <MetricCard label="Price adjustment" value={String(dealsNeedingPriceAdjustment.length)} detail="Counter and price objection present" />
      </div>

      <Section title="Negotiation Queue">
        <table className="data-table">
          <thead>
            <tr>
              <th>Record</th>
              <th>Deal</th>
              <th>Stage</th>
              <th>Counter</th>
              <th>Readiness</th>
              <th>Next Move</th>
            </tr>
          </thead>
          <tbody>
            {negotiationRecords.map((record) => {
              const deal = getDeal(record.dealId);
              const lead = deal ? getLead(deal.leadId) : undefined;
              return (
                <tr key={record.id}>
                  <td><Link href={`/dashboard/negotiations/${record.id}`}>{record.id}</Link></td>
                  <td>{record.dealId}<div className="record-meta">{lead?.city}, {lead?.state}</div></td>
                  <td>{record.negotiationStage}</td>
                  <td className="money">{record.counterOffer ? formatCurrency(record.counterOffer) : "none"}</td>
                  <td><Pill tone={record.readinessLevel === "contract-ready" ? "green" : record.readinessLevel === "high readiness" ? "green" : record.readinessLevel === "medium readiness" ? "gold" : "red"}>{record.readinessScore}</Pill></td>
                  <td>{record.nextMoveRecommendation}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>

      <div className="grid-two">
        <Section title="Stalled Negotiations">
          <div className="record-list">
            {stalledNegotiations.map((record) => (
              <RecordCard key={record.id} title={record.id} meta={record.sellerObjections.join(", ")} right={<Pill tone="red">stalled</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Safety Boundary">
          <div className="record-list">
            <RecordCard title="Live negotiation automation" meta="Blocked; these are internal recommendations only." right={<Pill tone="red">off</Pill>} />
            <RecordCard title="Pressure tactics" meta="Sign-now, false urgency, and role deception are blocked." right={<Pill tone="green">guarded</Pill>} />
          </div>
        </Section>
      </div>
    </div>
  );
}
