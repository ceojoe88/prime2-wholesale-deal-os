import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientOfferReadinessGates, getClientLead } from "@/lib/demo-data";

export default function ClientCommandUnderwritingBlockedPage() {
  const blocked = clientOfferReadinessGates.filter((gate) => gate.readinessStatus !== "ready_for_client_review");
  const missingEvidence = blocked.filter((gate) => gate.blockReasons.includes("evidence_missing")).length;
  return (
    <div className="page">
      <PageHeader
        eyebrow="Underwriting Blocked"
        title="Blocked offer readiness"
        description="Evidence and underwriting gaps prevent client review. Decision support only — no contract or offer has been sent."
      />

      <div className="metric-grid">
        <MetricCard label="Blocked" value={String(blocked.length)} detail="Needs evidence or review" />
        <MetricCard label="Missing evidence" value={String(missingEvidence)} detail="Packet gaps" />
        <MetricCard label="Unsupported values" value={String(blocked.filter((gate) => gate.blockReasons.length > 0).length)} detail="No invented numbers" />
        <MetricCard label="Provider actions" value="0" detail="Manual/demo data only" />
      </div>

      <Section title="Blocked Queue">
        <div className="record-list">
          {blocked.map((gate) => {
            const lead = getClientLead(gate.leadId);
            return (
              <RecordCard
                key={gate.id}
                title={lead?.displayName ?? gate.leadId}
                meta={gate.recommendedNextStep}
                right={<Link href={`/dashboard/client-command/leads/${gate.leadId}`}>View Details</Link>}
              >
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
