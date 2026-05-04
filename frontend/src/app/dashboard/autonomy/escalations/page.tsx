import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  autonomyCriticalEscalations,
  autonomyEscalationQueue,
  autonomyEscalations,
  formatCurrency,
  getDeal,
  getLead
} from "@/lib/demo-data";

export default function AutonomyEscalationsPage() {
  const projectedFeesAtReview = autonomyEscalationQueue.reduce((total, escalation) => {
    const deal = getDeal(escalation.dealId);
    return total + (deal?.projectedAssignmentFee ?? 0);
  }, 0);

  return (
    <div className="page">
      <PageHeader
        eyebrow="V12 Escalation Queue"
        title="Owner review escalations"
        description="Urgent deals, missing approvals, compliance blockers, and live-action risks are escalated as recommendations only."
      />

      <div className="metric-grid">
        <MetricCard label="Escalations" value={String(autonomyEscalations.length)} detail="Seeded V12 records" />
        <MetricCard label="Open" value={String(autonomyEscalationQueue.length)} detail="Needs owner attention" />
        <MetricCard label="Critical" value={String(autonomyCriticalEscalations.length)} detail="Hot deal acceleration" />
        <MetricCard label="Fees at review" value={formatCurrency(projectedFeesAtReview)} detail="Projected, not guaranteed" />
      </div>

      <Section title="Escalation Queue">
        <table className="data-table">
          <thead>
            <tr>
              <th>Escalation</th>
              <th>Deal</th>
              <th>Lead</th>
              <th>Severity</th>
              <th>Reason</th>
              <th>Owner</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {autonomyEscalations.map((escalation) => {
              const deal = getDeal(escalation.dealId);
              const lead = getLead(escalation.leadId);
              return (
                <tr key={escalation.id}>
                  <td>{escalation.escalationType}<div className="record-meta">{escalation.id}</div></td>
                  <td>{escalation.dealId}<div className="record-meta">{deal ? formatCurrency(deal.projectedAssignmentFee) : "n/a"}</div></td>
                  <td>{lead ? `${lead.city}, ${lead.state}` : "n/a"}</td>
                  <td><Pill tone={escalation.severity === "critical" ? "red" : "gold"}>{escalation.severity}</Pill></td>
                  <td>{escalation.reason}</td>
                  <td><Pill tone={escalation.ownerActionRequired ? "gold" : "green"}>{escalation.ownerActionRequired ? "required" : "clear"}</Pill></td>
                  <td><Pill tone={escalation.realWorldActionBlocked ? "red" : "green"}>{escalation.realWorldActionBlocked ? "blocked" : "allowed"}</Pill></td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>

      <Section title="Recommended Actions">
        <div className="record-list">
          {autonomyEscalationQueue.map((escalation) => (
            <RecordCard key={escalation.id} title={escalation.recommendedAction} meta={escalation.reason} right={<Pill tone="gold">owner</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
