import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { buyerMatches, buyerVisibleDeals, formatCurrency } from "@/lib/demo-data";

export default function BuyerPortalWatchlistPage() {
  const visibleIds = new Set(buyerVisibleDeals.map((deal) => deal.dealId));
  const matches = buyerMatches.filter((match) => visibleIds.has(match.dealId));
  return (
    <div className="page">
      <PageHeader
        eyebrow="Watchlist"
        title="Matched deal rooms"
        description="Watchlist entries are draft-only and filtered through the same buyer visibility gate."
      />
      <Section title="Visible Matches">
        <div className="record-list">
          {matches.map((match) => {
            const deal = buyerVisibleDeals.find((item) => item.dealId === match.dealId);
            return (
              <RecordCard
                key={match.id}
                title={deal ? `${deal.city}, ${deal.state} ${deal.zipCode}` : match.dealId}
                meta={deal ? `Asking ${formatCurrency(deal.askingPrice ?? 0)} / margin ${formatCurrency(deal.estimatedBuyerMargin ?? 0)}` : "Unavailable"}
                right={<Pill tone="green">{match.score}</Pill>}
              >
                <Link className="pill green" href={`/buyer-portal/deals/${match.dealId}`}>open deal room</Link>
              </RecordCard>
            );
          })}
        </div>
      </Section>
    </div>
  );
}
