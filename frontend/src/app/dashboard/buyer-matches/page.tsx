import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { buyerInterests, buyerMatches, buyerPortalBlockedDeals, buyerVisibleDeals, formatCurrency, getBuyer, getDeal, getLead } from "@/lib/demo-data";

export default function BuyerMatchesPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Buyer Matches"
        title="Draft-only disposition matches"
        description="Matches rank buyer area fit, price capacity, property type, spread, reliability, closing speed, and proof-of-funds readiness."
      />
      <div className="metric-grid">
        <div className="metric-card"><span>Visible rooms</span><strong>{buyerVisibleDeals.length}</strong><small>Passed publishing gate</small></div>
        <div className="metric-card"><span>Intent records</span><strong>{buyerInterests.length}</strong><small>No execution power</small></div>
        <div className="metric-card"><span>POF needed</span><strong>{buyerInterests.filter((interest) => interest.proofOfFundsStatus !== "verified").length}</strong><small>Review before follow-up</small></div>
        <div className="metric-card"><span>Blocked deals</span><strong>{buyerPortalBlockedDeals.length}</strong><small>Not buyer visible</small></div>
      </div>
      <Section title="Match Queue">
        <div className="record-list">
          {buyerMatches.map((match) => {
            const deal = getDeal(match.dealId);
            const buyer = getBuyer(match.buyerId);
            const lead = deal ? getLead(deal.leadId) : undefined;
            return (
              <RecordCard
                key={match.id}
                title={`${buyer?.company ?? match.buyerId} / ${match.dealId}`}
                meta={`${lead?.zipCode ?? ""} / ${deal ? formatCurrency(deal.buyerPurchasePrice) : ""}`}
                right={<Pill tone="green">{match.score}</Pill>}
              >
                <div className="pill-row">
                  {match.matchReasons.map((reason) => <Pill key={reason}>{reason}</Pill>)}
                  <Pill tone="red">draft only</Pill>
                </div>
              </RecordCard>
            );
          })}
        </div>
      </Section>
    </div>
  );
}
