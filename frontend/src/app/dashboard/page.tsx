import { DealTable } from "@/components/DealTable";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  buyerMatches,
  buyerInterests,
  buyerPortalBlockedDeals,
  buyerVisibleDeals,
  complianceRecords,
  deals,
  divisions,
  formatCurrency,
  hotDeals,
  hotSellerLeads,
  leads,
  offerReadyPackets,
  offerPackets,
  projectedAssignmentTotal,
  sellerInteractions,
  staleSellerFollowUps,
  underContractDeals
} from "@/lib/demo-data";

export default function DashboardPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Wholesale Prime"
        title="Daily acquisition command"
        description="Hot opportunities, spread protection, buyer demand, and compliance risk are ranked for owner approval."
      />

      <div className="metric-grid">
        <MetricCard label="Active leads" value={String(leads.length)} detail="30 motivated seller records seeded" />
        <MetricCard label="Hot 10K+ targets" value={String(hotDeals.length)} detail="Owner review before offer prep" />
        <MetricCard label="Projected fees" value={formatCurrency(projectedAssignmentTotal)} detail="Across active demo deals" />
        <MetricCard label="Compliance alerts" value={String(complianceRecords.length)} detail="Blocked until reviewed" />
      </div>

      <div className="command-band">
        <strong>Wholesale Prime briefing</strong>
        <div className="pill-row">
          <Pill tone="green">{underContractDeals.length} under contract</Pill>
          <Pill tone="gold">{buyerMatches.length} draft buyer matches</Pill>
          <Pill tone="red">No live outreach in v1</Pill>
        </div>
        <span className="muted">
          Prioritize 10K+ spreads with verified buyer margin, then route compliance-risk examples before assignment packet prep.
        </span>
      </div>

      <div className="grid-two">
        <Section title="Top Deal Queue">
          <DealTable limit={5} />
        </Section>
        <Section title="Manager Load">
          <div className="record-list">
            {divisions.slice(0, 5).map((division) => (
              <RecordCard
                key={division.id}
                title={division.managerName}
                meta={division.name}
                right={<Pill tone={division.riskFlags.length ? "gold" : "green"}>{division.workload} active</Pill>}
              >
                <span className="record-meta">{division.nextBestAction}</span>
              </RecordCard>
            ))}
          </div>
        </Section>
      </div>

      <Section title="V2 Buyer Portal Gate">
        <div className="grid-three">
          <RecordCard title="Buyer-visible deals" meta={`${buyerVisibleDeals.length} sanitized deal rooms`} right={<Pill tone="green">visible</Pill>} />
          <RecordCard title="Buyer interest queue" meta={`${buyerInterests.length} draft intent records`} right={<Pill tone="gold">owner review</Pill>} />
          <RecordCard title="Blocked from portal" meta={`${buyerPortalBlockedDeals.length} deals have gate reasons`} right={<Pill tone="red">blocked</Pill>} />
        </div>
      </Section>

      <Section title="V3 Seller Acquisition Gate">
        <div className="grid-three">
          <RecordCard title="Seller temperature" meta={`${hotSellerLeads.length} hot sellers`} right={<Pill tone="red">hot</Pill>} />
          <RecordCard title="Follow-up urgency" meta={`${staleSellerFollowUps.length} stale or urgent follow-ups`} right={<Pill tone="gold">review</Pill>} />
          <RecordCard title="Offer readiness" meta={`${offerReadyPackets.length}/${offerPackets.length} packets ready`} right={<Pill tone="green">gated</Pill>} />
        </div>
        <div className="record-list">
          {sellerInteractions.slice(0, 3).map((interaction) => (
            <RecordCard key={interaction.id} title={interaction.nextBestSellerAction} meta={`${interaction.objectionStatus} / ${interaction.followUpUrgency}`} right={<Pill>{interaction.sellerTemperatureScore}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
