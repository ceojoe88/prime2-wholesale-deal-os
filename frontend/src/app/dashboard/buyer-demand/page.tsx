import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  bestBuyersForHotDeals,
  buyerDemandProfiles,
  buyerReadyDealsFromDemand,
  distributionDraftsPendingApproval,
  fastCloseBuyerList,
  getBuyer,
  highestDemandZipCodes
} from "@/lib/demo-data";

export default function BuyerDemandPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V9 Buyer Demand Intelligence"
        title="Buyer demand command"
        description="Rank buyer demand, fast-close capacity, POF strength, price-band fit, and hot-deal buyer readiness without sending blasts or exposing internal spread logic."
      />
      <div className="metric-grid">
        <MetricCard label="Demand profiles" value={String(buyerDemandProfiles.length)} detail="Active cash buyer intelligence" />
        <MetricCard label="Fast-close buyers" value={String(fastCloseBuyerList.length)} detail="Verified POF and 10 days or faster" />
        <MetricCard label="Buyer-ready deals" value={String(buyerReadyDealsFromDemand.length)} detail="Strong demand and visible deal room" />
        <MetricCard label="Draft approvals" value={String(distributionDraftsPendingApproval.length)} detail="No live send, owner review needed" />
      </div>

      <div className="grid-two">
        <Section title="Highest-Demand Zip Codes">
          <div className="record-list">
            {highestDemandZipCodes.slice(0, 8).map((zip) => (
              <RecordCard
                key={zip.zipCode}
                title={zip.zipCode}
                meta={`${zip.buyerCount} active buyers weighted by zip demand`}
                right={<Pill tone={zip.demandScore >= 90 ? "green" : "gold"}>{zip.demandScore}</Pill>}
              />
            ))}
          </div>
        </Section>
        <Section title="Best Buyers For Hot Deals">
          <div className="record-list">
            {bestBuyersForHotDeals.map(({ deal, priority, buyer }) => (
              <RecordCard
                key={`${deal.id}-${priority.buyerId}`}
                title={`${deal.id} / ${buyer?.company ?? priority.buyerId}`}
                meta={`Rank ${priority.rank} with ${priority.riskFlags.length || 0} risk flags`}
                right={<Pill tone={priority.priorityScore >= 90 ? "green" : "gold"}>{priority.priorityScore}</Pill>}
              />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Buyer Demand Profiles">
        <table className="data-table">
          <thead>
            <tr>
              <th>Buyer</th>
              <th>Demand</th>
              <th>Zip / Type</th>
              <th>Price Fit</th>
              <th>POF</th>
              <th>Last Engaged</th>
            </tr>
          </thead>
          <tbody>
            {buyerDemandProfiles.map((profile) => {
              const buyer = getBuyer(profile.buyerId);
              return (
                <tr key={profile.id}>
                  <td>
                    <Link href={`/dashboard/buyer-demand/${profile.buyerId}`}>{buyer?.company ?? profile.buyerId}</Link>
                    <div className="record-meta">{buyer?.name}</div>
                  </td>
                  <td><Pill tone={profile.buyerActivityScore >= 90 ? "green" : "gold"}>{profile.buyerActivityScore}</Pill></td>
                  <td>{profile.targetZipCodes.join(", ")}<div className="record-meta">{profile.propertyType}</div></td>
                  <td>{profile.priceBandFitScore}</td>
                  <td><Pill tone={profile.proofOfFundsStrength === 100 ? "green" : "gold"}>{profile.proofOfFundsStrength}</Pill></td>
                  <td>{profile.lastEngagedDate}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
