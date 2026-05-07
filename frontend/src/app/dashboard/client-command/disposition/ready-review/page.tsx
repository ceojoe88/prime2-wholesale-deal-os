import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientDispositionReadinessGates, getClientLead } from "@/lib/demo-data";

export default function ClientCommandDispositionReadyReviewPage() {
  const ready = clientDispositionReadinessGates.filter((gate) => gate.readinessStatus === "ready_for_client_review");
  return (
    <div className="page">
      <PageHeader
        eyebrow="Disposition Ready Review"
        title="Disposition-ready leads"
        description="Decision support only — no campaign, contract, or buyer outreach has been sent."
      />

      <div className="metric-grid">
        <MetricCard label="Ready leads" value={String(ready.length)} detail="Manual review queue" />
        <MetricCard label="Buyer evidence" value={String(ready.reduce((sum, gate) => sum + gate.buyerDemandEvidenceCount, 0))} detail="Client-safe evidence notes" />
        <MetricCard label="Strong matches" value={String(ready.reduce((sum, gate) => sum + gate.strongBuyerMatchCount, 0))} detail="Buy box fit" />
        <MetricCard label="Outreach sent" value="0" detail="Manual-use only" />
      </div>

      <Section title="Disposition Readiness Gate">
        <div className="record-list">
          {ready.map((gate) => {
            const lead = getClientLead(gate.leadId);
            return (
              <RecordCard key={gate.id} title={lead?.displayName ?? gate.leadId} meta={gate.recommendedNextStep} right={<Link href={`/dashboard/client-command/leads/${gate.leadId}`}>View Details</Link>}>
                <div className="tag-row">
                  <Pill tone="green">{gate.readinessStatus}</Pill>
                  <Pill tone="green">{gate.readinessScore}</Pill>
                  <Pill tone="gold">No Buyer Contacted</Pill>
                  <Pill tone="gold">No Campaign Started</Pill>
                  {gate.requiresHumanReview ? <Pill tone="gold">Human Review Needed</Pill> : null}
                </div>
              </RecordCard>
            );
          })}
        </div>
      </Section>
    </div>
  );
}
