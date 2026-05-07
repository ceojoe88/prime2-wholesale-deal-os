import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import {
  clientAppointmentReadinessReviews,
  clientDispositionReadinessGates,
  clientLeadCards,
  clientOfferReadinessGates,
  formatCurrency
} from "@/lib/demo-data";

export default function ClientCommandLeadsPage() {
  const missingCount = clientLeadCards.reduce((total, card) => total + card.missingData.length, 0);
  return (
    <div className="page">
      <PageHeader
        eyebrow="CP2 Lead Intelligence"
        title="Client lead profiles"
        description="Client-safe lead intelligence scores with confidence, human-review flags, missing data, and recommended next action."
      />

      <div className="metric-grid">
        <MetricCard label="Leads" value={String(clientLeadCards.length)} detail="Across client workspaces" />
        <MetricCard label="Missing data" value={String(missingCount)} detail="Readiness blockers and gaps" />
        <MetricCard label="Human review" value={String(clientLeadCards.filter((card) => card.score.requiresHumanReview).length)} detail="Manager-gated" />
        <MetricCard label="Disposition ready" value={String(clientDispositionReadinessGates.filter((gate) => gate.readinessStatus === "ready_for_client_review").length)} detail="CP5 buyer matching" />
      </div>

      <Section title="Lead Intelligence Queue">
        <table className="data-table">
          <thead>
            <tr>
              <th>Lead</th>
              <th>Market</th>
              <th>Equity</th>
              <th>Priority</th>
              <th>Confidence</th>
              <th>Acquisition</th>
              <th>Offer Gate</th>
              <th>Disposition</th>
              <th>Next Action</th>
            </tr>
          </thead>
          <tbody>
            {clientLeadCards.map((card) => (
              <tr key={card.lead.id}>
                <td>
                  <Link href={`/dashboard/client-command/leads/${card.lead.id}`}>{card.lead.displayName}</Link>
                  <div className="record-meta">{card.lead.leadType}</div>
                </td>
                <td>{card.lead.propertyCity || "missing"} {card.lead.propertyZip}</td>
                <td>{formatCurrency(card.lead.estimatedEquity)}</td>
                <td><Pill tone={card.score.finalPriorityScore >= 70 ? "green" : "gold"}>{card.score.finalPriorityScore}</Pill></td>
                <td>{card.score.confidenceLevel}</td>
                <td>
                  <Pill tone={clientAppointmentReadinessReviews.find((item) => item.leadId === card.lead.id)?.appointmentReady ? "green" : "gold"}>
                    {clientAppointmentReadinessReviews.find((item) => item.leadId === card.lead.id)?.appointmentReady ? "ready" : "review"}
                  </Pill>
                </td>
                <td>
                  <Pill tone={clientOfferReadinessGates.find((item) => item.leadId === card.lead.id)?.readinessStatus === "ready_for_client_review" ? "green" : "red"}>
                    {clientOfferReadinessGates.find((item) => item.leadId === card.lead.id)?.readinessStatus ?? "not_ready"}
                  </Pill>
                </td>
                <td>
                  <Pill tone={clientDispositionReadinessGates.find((item) => item.leadId === card.lead.id)?.readinessStatus === "ready_for_client_review" ? "green" : "gold"}>
                    {clientDispositionReadinessGates.find((item) => item.leadId === card.lead.id)?.readinessStatus ?? "not_ready"}
                  </Pill>
                </td>
                <td>{card.nextAction?.actionLabel ?? card.score.recommendedNextAction}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
