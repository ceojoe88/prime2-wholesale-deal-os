import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientLeadNextBestActions, clientLeadProfiles } from "@/lib/demo-data";

function leadName(leadId: string) {
  return clientLeadProfiles.find((lead) => lead.id === leadId)?.displayName ?? leadId;
}

export default function ClientNextActionsPage() {
  const reviewCount = clientLeadNextBestActions.filter((action) => action.requiresHumanReview).length;
  return (
    <div className="page">
      <PageHeader
        eyebrow="Client Next Actions"
        title="Recommended next action queue"
        description="Client-safe recommendations only. Actions can research, review, and prepare internal notes; provider, billing, and e-sign lanes remain unavailable."
      />

      <div className="metric-grid">
        <MetricCard label="Actions" value={String(clientLeadNextBestActions.length)} detail="Client-safe recommendations" />
        <MetricCard label="Human review" value={String(reviewCount)} detail="Manager-gated items" />
        <MetricCard label="Provider actions" value="0" detail="No outbound execution" />
        <MetricCard label="Billing actions" value="0" detail="No payment lane" />
      </div>

      <Section title="Next Action Queue">
        <div className="record-list">
          {clientLeadNextBestActions.map((action) => (
            <RecordCard
              key={action.id}
              title={action.actionLabel}
              meta={`${leadName(action.leadId)} | ${action.reason}`}
              right={<Link href={`/dashboard/client-command/leads/${action.leadId}`}>{action.confidenceLevel}</Link>}
            />
          ))}
        </div>
      </Section>

      <Section title="Execution Locks">
        <div className="grid-three">
          {clientLeadNextBestActions.map((action) => (
            <RecordCard
              key={`${action.id}-lock`}
              title={leadName(action.leadId)}
              meta="Outbound/provider execution remains unavailable in CP1/CP2."
              right={<Pill tone={action.outboundActionAllowed || action.providerActionAllowed ? "red" : "green"}>locked</Pill>}
            />
          ))}
        </div>
      </Section>
    </div>
  );
}
