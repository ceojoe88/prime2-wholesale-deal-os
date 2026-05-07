import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientDealBuyerMatches, getClientBuyer, getClientLead } from "@/lib/demo-data";

export default function ClientCommandDispositionMatchesPage() {
  const strong = clientDealBuyerMatches.filter((match) => match.matchStatus === "strong_match");
  const review = clientDealBuyerMatches.filter((match) => match.requiresHumanReview);
  return (
    <div className="page">
      <PageHeader
        eyebrow="CP5 Buyer Matching"
        title="Deal-to-buyer matches"
        description="Deterministic buyer fit records based on client-entered profiles, buy boxes, CP4 readiness, and demo demand evidence."
      />

      <div className="metric-grid">
        <MetricCard label="Matches" value={String(clientDealBuyerMatches.length)} detail="No automatic buyer outreach" />
        <MetricCard label="Strong" value={String(strong.length)} detail="Market, price, property, and buy box fit" />
        <MetricCard label="Human review" value={String(review.length)} detail="Funding or fit gaps" />
        <MetricCard label="Provider actions" value="0" detail="No scraping or sync" />
      </div>

      <Section title="Buyer Match Summary">
        <div className="record-list">
          {clientDealBuyerMatches.map((match) => {
            const lead = getClientLead(match.leadId);
            const buyer = getClientBuyer(match.buyerId);
            return (
              <RecordCard key={match.id} title={`${lead?.displayName ?? match.leadId} - ${buyer?.buyerName ?? match.buyerId}`} meta={match.clientSafeSummary} right={<Link href={`/dashboard/client-command/leads/${match.leadId}`}>View Details</Link>}>
                <div className="tag-row">
                  <Pill tone={match.matchStatus === "strong_match" ? "green" : match.matchStatus === "possible_match" ? "gold" : "red"}>{match.matchStatus}</Pill>
                  <Pill tone="gold">{match.matchScore}</Pill>
                  <Pill tone="green">{match.priceFitStatus}</Pill>
                  {match.requiresHumanReview ? <Pill tone="gold">Human Review Needed</Pill> : null}
                  {match.mismatchReasons.map((reason) => (
                    <Pill key={reason} tone="red">{reason}</Pill>
                  ))}
                </div>
              </RecordCard>
            );
          })}
        </div>
      </Section>
    </div>
  );
}
