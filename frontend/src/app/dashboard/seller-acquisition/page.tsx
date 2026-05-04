import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  formatCurrency,
  getLead,
  hotSellerLeads,
  negotiationStageLeads,
  offerNeededLeads,
  sellerInteractions,
  staleSellerFollowUps,
  underContractCandidates
} from "@/lib/demo-data";

export default function SellerAcquisitionPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Seller Acquisition"
        title="Seller pipeline command center"
        description="Turns leads into controlled opportunities through discovery notes, draft-only scripts, follow-up timing, objection tracking, and gated offer packet readiness."
      />
      <div className="metric-grid">
        <MetricCard label="Hot sellers" value={String(hotSellerLeads.length)} detail="High temperature or opportunity" />
        <MetricCard label="Stale follow-ups" value={String(staleSellerFollowUps.length)} detail="Needs owner-reviewed next step" />
        <MetricCard label="Offer needed" value={String(offerNeededLeads.length)} detail="Underwriting and gate required" />
        <MetricCard label="Negotiations" value={String(negotiationStageLeads.length)} detail="Objections tracked" />
      </div>
      <div className="grid-two">
        <Section title="Seller Queue">
          <div className="record-list">
            {sellerInteractions.map((interaction) => {
              const lead = getLead(interaction.leadId);
              return (
                <RecordCard
                  key={interaction.id}
                  title={lead?.sellerName ?? interaction.leadId}
                  meta={`${lead?.stage ?? "lead"} / asking ${formatCurrency(interaction.askingPrice ?? lead?.askingPrice ?? 0)}`}
                  right={<Pill tone={interaction.followUpUrgency === "hot" ? "red" : "gold"}>{interaction.sellerTemperatureScore}</Pill>}
                >
                  <span className="record-meta">{interaction.nextBestSellerAction}</span>
                  <div className="pill-row">
                    <Pill>{interaction.objectionStatus}</Pill>
                    <Pill tone="green">draft only</Pill>
                    <Link className="pill green" href={`/dashboard/seller-acquisition/${interaction.leadId}`}>open</Link>
                  </div>
                </RecordCard>
              );
            })}
          </div>
        </Section>
        <Section title="Under-Contract Candidates">
          <div className="record-list">
            {underContractCandidates.map((lead) => (
              <RecordCard key={lead.id} title={lead.sellerName} meta={`${lead.stage} / ${lead.sourceCategory}`} right={<Pill tone="gold">{lead.opportunityScore}</Pill>} />
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
