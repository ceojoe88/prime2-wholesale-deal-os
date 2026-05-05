import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  buyerVelocityProfiles,
  fastestBuyerVelocity,
  getBuyer
} from "@/lib/demo-data";

export default function BuyerVelocityPage() {
  const fastClose = fastestBuyerVelocity.filter((profile) => profile.recommendedUse === "fast_close_priority");
  const pofReview = fastestBuyerVelocity.filter((profile) => profile.recommendedUse === "pof_or_fit_review");

  return (
    <div className="page">
      <PageHeader
        eyebrow="V14 Buyer Velocity"
        title="Fast-close buyer intelligence"
        description="Score buyers by response speed, POF strength, close history, price fit, market fit, reliability, and prior intent quality so hot deals route to the fastest likely closers."
      />

      <div className="metric-grid">
        <MetricCard label="Velocity profiles" value={String(buyerVelocityProfiles.length)} detail="Deterministic buyer-side speed scoring" />
        <MetricCard label="Fast-close priority" value={String(fastClose.length)} detail="Best candidates for controlled distribution" />
        <MetricCard label="POF or fit review" value={String(pofReview.length)} detail="Needs verification before access" />
        <MetricCard label="Live contact" value="off" detail="Scores do not trigger outreach" />
      </div>

      <div className="grid-two">
        <Section title="Fastest Buyers">
          <div className="record-list">
            {fastestBuyerVelocity.map((profile) => {
              const buyer = getBuyer(profile.buyerId);
              return (
                <RecordCard
                  key={profile.id}
                  title={buyer?.company ?? profile.buyerId}
                  meta={`${buyer?.proofOfFundsStatus ?? "unknown"} POF / ${buyer?.closingSpeedDays ?? "n/a"} day closing speed`}
                  right={<Pill tone={profile.velocityScore >= 88 ? "green" : profile.velocityScore >= 75 ? "gold" : "red"}>{profile.velocityScore}</Pill>}
                />
              );
            })}
          </div>
        </Section>

        <Section title="Scoring Inputs">
          <div className="record-list">
            <RecordCard title="Response speed" meta="How quickly the buyer responds to controlled messages." right={<Pill>18%</Pill>} />
            <RecordCard title="POF strength" meta="Verified proof-of-funds capacity and recency." right={<Pill>18%</Pill>} />
            <RecordCard title="Close history" meta="Past ability to close without avoidable friction." right={<Pill>18%</Pill>} />
            <RecordCard title="Fit and reliability" meta="Price, market, reliability, and previous intent quality." right={<Pill>46%</Pill>} />
          </div>
        </Section>
      </div>

      <Section title="Velocity Profiles">
        <table className="data-table">
          <thead>
            <tr>
              <th>Buyer</th>
              <th>Velocity</th>
              <th>POF</th>
              <th>Close</th>
              <th>Price / Market</th>
              <th>Recommended Use</th>
            </tr>
          </thead>
          <tbody>
            {fastestBuyerVelocity.map((profile) => {
              const buyer = getBuyer(profile.buyerId);
              return (
                <tr key={profile.id}>
                  <td>{buyer?.company ?? profile.buyerId}<div className="record-meta">{buyer?.name}</div></td>
                  <td><Pill tone={profile.velocityScore >= 88 ? "green" : "gold"}>{profile.velocityScore}</Pill></td>
                  <td>{profile.pofStrength}</td>
                  <td>{profile.closeHistory}</td>
                  <td>{profile.priceFit} / {profile.marketFit}</td>
                  <td>{profile.recommendedUse}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
