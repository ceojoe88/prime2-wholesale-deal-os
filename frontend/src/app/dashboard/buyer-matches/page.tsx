import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { buyerMatches, formatCurrency, getBuyer, getDeal, getLead } from "@/lib/demo-data";

export default function BuyerMatchesPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Buyer Matches"
        title="Draft-only disposition matches"
        description="Matches rank buyer area fit, price capacity, property type, spread, reliability, closing speed, and proof-of-funds readiness."
      />
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
