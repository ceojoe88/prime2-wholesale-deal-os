import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientDealBuyerMatches, clientDispositionReadinessGates, getClientBuyer, getClientLead } from "@/lib/demo-data";

export default function ClientCommandDispositionNeedsReviewPage() {
  const gates = clientDispositionReadinessGates.filter((gate) => gate.requiresHumanReview);
  const matches = clientDealBuyerMatches.filter((match) => match.requiresHumanReview);
  return (
    <div className="page">
      <PageHeader
        eyebrow="Disposition Needs Review"
        title="Human-review disposition queue"
        description="Buyer confidence, demand evidence, and CP4 readiness gaps for manual client review."
      />

      <div className="metric-grid">
        <MetricCard label="Lead gates" value={String(gates.length)} detail="Disposition review needed" />
        <MetricCard label="Buyer matches" value={String(matches.length)} detail="Fit or funding review" />
        <MetricCard label="Safe boundary" value="manual" detail="No campaign or buyer outreach sent" />
        <MetricCard label="Provider actions" value="0" detail="No external data pull" />
      </div>

      <Section title="Lead Review Queue">
        <div className="record-list">
          {gates.map((gate) => {
            const lead = getClientLead(gate.leadId);
            return (
              <RecordCard key={gate.id} title={lead?.displayName ?? gate.leadId} meta={gate.recommendedNextStep} right={<Link href={`/dashboard/client-command/leads/${gate.leadId}`}>View Details</Link>}>
                <div className="tag-row">
                  <Pill tone={gate.readinessStatus === "ready_for_client_review" ? "green" : "gold"}>{gate.readinessStatus}</Pill>
                  <Pill tone="gold">Human Review Needed</Pill>
                </div>
              </RecordCard>
            );
          })}
        </div>
      </Section>

      <Section title="Buyer Match Review">
        <div className="record-list">
          {matches.map((match) => {
            const buyer = getClientBuyer(match.buyerId);
            const lead = getClientLead(match.leadId);
            return (
              <RecordCard key={match.id} title={buyer?.buyerName ?? match.buyerId} meta={match.recommendedNextStep} right={<Link href={`/dashboard/client-command/leads/${match.leadId}`}>View Details</Link>}>
                <div className="tag-row">
                  <Pill tone="gold">{lead?.displayName ?? match.leadId}</Pill>
                  <Pill tone="gold">{match.matchStatus}</Pill>
                  {match.mismatchReasons.map((reason) => (
                    <Pill key={reason} tone="red">{reason}</Pill>
                  ))}
                </div>
              </RecordCard>
            );
          })}
        </div>
      </Section>
    </div>
  );
}
