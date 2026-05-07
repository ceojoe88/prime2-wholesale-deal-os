import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientDispositionReadinessGates, getClientLead } from "@/lib/demo-data";

export default function ClientCommandDispositionBlockedPage() {
  const blocked = clientDispositionReadinessGates.filter((gate) => gate.readinessStatus !== "ready_for_client_review");
  const offerBlocked = blocked.filter((gate) => gate.readinessStatus === "offer_readiness_blocked").length;
  return (
    <div className="page">
      <PageHeader
        eyebrow="Disposition Blocked"
        title="Blocked disposition readiness"
        description="Buyer demand, offer readiness, or evidence gaps prevent client review. No buyer outreach has been sent."
      />

      <div className="metric-grid">
        <MetricCard label="Blocked" value={String(blocked.length)} detail="Needs CP4 or buyer evidence" />
        <MetricCard label="Offer blocked" value={String(offerBlocked)} detail="CP4 gate not ready" />
        <MetricCard label="Buyer evidence gaps" value={String(blocked.filter((gate) => gate.blockReasons.includes("buyer_demand_evidence_missing")).length)} detail="Manual evidence needed" />
        <MetricCard label="Provider actions" value="0" detail="No buyer provider calls" />
      </div>

      <Section title="Blocked Queue">
        <div className="record-list">
          {blocked.map((gate) => {
            const lead = getClientLead(gate.leadId);
            return (
              <RecordCard key={gate.id} title={lead?.displayName ?? gate.leadId} meta={gate.recommendedNextStep} right={<Link href={`/dashboard/client-command/leads/${gate.leadId}`}>View Details</Link>}>
                <div className="tag-row">
                  <Pill tone="red">{gate.readinessStatus}</Pill>
                  {gate.blockReasons.map((reason) => (
                    <Pill key={reason} tone="red">{reason}</Pill>
                  ))}
                  {gate.riskFlags.map((flag) => (
                    <Pill key={flag} tone="gold">{flag}</Pill>
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
