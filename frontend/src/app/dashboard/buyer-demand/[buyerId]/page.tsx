import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  buyerDealPriorities,
  buyers,
  formatCurrency,
  getBuyer,
  getBuyerDemandProfile,
  getDeal,
  getDealDistributionPrepsForBuyer,
  getLead
} from "@/lib/demo-data";

export function generateStaticParams() {
  return buyers.map((buyer) => ({ buyerId: buyer.id }));
}

export default async function BuyerDemandDetailPage({ params }: { params: Promise<{ buyerId: string }> }) {
  const { buyerId } = await params;
  const buyer = getBuyer(buyerId);
  const profile = getBuyerDemandProfile(buyerId);
  if (!buyer || !profile) notFound();
  const priorities = buyerDealPriorities
    .filter((priority) => priority.buyerId === buyerId)
    .sort((first, second) => first.rank - second.rank);
  const distributions = getDealDistributionPrepsForBuyer(buyerId);

  return (
    <div className="page">
      <PageHeader
        eyebrow="Buyer Demand Detail"
        title={`${buyer.company} demand profile`}
        description="Internal buyer intelligence for ranking only. Communication remains draft-only and one recipient at a time."
      />
      <div className="metric-grid">
        <MetricCard label="Activity" value={String(profile.buyerActivityScore)} detail="Engagement and response quality" />
        <MetricCard label="Zip demand" value={String(profile.zipCodeDemandScore)} detail={profile.targetZipCodes.join(", ")} />
        <MetricCard label="POF strength" value={String(profile.proofOfFundsStrength)} detail={buyer.proofOfFundsStatus} />
        <MetricCard label="Close speed" value={`${buyer.closingSpeedDays} days`} detail={`Reliability ${buyer.reliabilityScore}`} />
      </div>

      <div className="grid-two">
        <Section title="Preferred Fit">
          <div className="record-list">
            <RecordCard title="Price band" meta={profile.priceBand} right={<Pill>{profile.priceBandFitScore}</Pill>} />
            <RecordCard title="Property type" meta={profile.propertyType} right={<Pill>{profile.propertyTypeDemandScore}</Pill>} />
            <RecordCard title="Margin notes" meta={profile.preferredSpreadMarginNotes} right={<Pill tone="green">internal</Pill>} />
            <RecordCard title="Live outreach" meta="Disabled in V9 distribution prep." right={<Pill tone="red">off</Pill>} />
          </div>
        </Section>
        <Section title="Distribution Drafts">
          <div className="record-list">
            {distributions.map((prep) => (
              <RecordCard
                key={prep.id}
                title={prep.id}
                meta={`${prep.dealId}: ${prep.approvalStatus}`}
                right={<Pill tone={prep.blockedReasons.length ? "red" : "gold"}>{prep.draftStatus}</Pill>}
              />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Ranked Deal Fit">
        <table className="data-table">
          <thead>
            <tr>
              <th>Deal</th>
              <th>Property</th>
              <th>Asking</th>
              <th>Priority</th>
              <th>Risk Flags</th>
            </tr>
          </thead>
          <tbody>
            {priorities.map((priority) => {
              const deal = getDeal(priority.dealId);
              const lead = deal ? getLead(deal.leadId) : undefined;
              return (
                <tr key={priority.id}>
                  <td>{priority.dealId}<div className="record-meta">rank {priority.rank}</div></td>
                  <td>{lead?.city}, {lead?.state}<div className="record-meta">{lead?.zipCode}</div></td>
                  <td className="money">{formatCurrency(deal?.buyerPurchasePrice ?? 0)}</td>
                  <td><Pill tone={priority.priorityScore >= 85 ? "green" : "gold"}>{priority.priorityScore}</Pill></td>
                  <td>{priority.riskFlags.length ? priority.riskFlags.join(", ") : "clear"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
