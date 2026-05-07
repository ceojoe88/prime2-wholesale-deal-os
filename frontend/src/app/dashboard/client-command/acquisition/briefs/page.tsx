import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientAcquisitionBriefs, getClientLead } from "@/lib/demo-data";

export default function ClientCommandAcquisitionBriefsPage() {
  const reviewCount = clientAcquisitionBriefs.filter((brief) => brief.requiresHumanReview).length;
  return (
    <div className="page">
      <PageHeader
        eyebrow="Acquisition Briefs"
        title="Call prep briefs"
        description="Seller conversation guidance generated from CP2 lead intelligence and missing-data signals. Manual use only."
      />

      <div className="metric-grid">
        <MetricCard label="Briefs" value={String(clientAcquisitionBriefs.length)} detail="Client-safe summaries" />
        <MetricCard label="Review flags" value={String(reviewCount)} detail="Human review needed" />
        <MetricCard label="Provider actions" value="0" detail="No external calls" />
        <MetricCard label="Draft status" value="manual" detail="Guidance only" />
      </div>

      <Section title="Brief Queue">
        <div className="record-list">
          {clientAcquisitionBriefs.map((brief) => {
            const lead = getClientLead(brief.leadId);
            return (
              <RecordCard
                key={brief.id}
                title={lead?.displayName ?? brief.leadId}
                meta={brief.recommendedCallObjective}
                right={<Link href={`/dashboard/client-command/leads/${brief.leadId}`}>View Details</Link>}
              >
                <p>{brief.clientSafeSummary}</p>
                <div className="tag-row">
                  <Pill tone="green">Client-Safe</Pill>
                  <Pill tone={brief.confidenceLevel === "high" ? "green" : "gold"}>{brief.confidenceLevel}</Pill>
                  {brief.requiresHumanReview ? <Pill tone="gold">Human Review Needed</Pill> : null}
                </div>
              </RecordCard>
            );
          })}
        </div>
      </Section>
    </div>
  );
}
