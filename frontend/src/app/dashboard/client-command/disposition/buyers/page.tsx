import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientBuyerBuyBoxes, clientBuyerConfidenceScores, clientBuyerProfiles, formatCurrency } from "@/lib/demo-data";

export default function ClientCommandDispositionBuyersPage() {
  const reviewBuyers = clientBuyerConfidenceScores.filter((score) => score.requiresHumanReview).length;
  return (
    <div className="page">
      <PageHeader
        eyebrow="CP5 Buyers"
        title="Buyer profiles"
        description="Workspace-scoped buyer profiles, buy boxes, and confidence scores. No buyer has been contacted."
      />

      <div className="metric-grid">
        <MetricCard label="Buyers" value={String(clientBuyerProfiles.length)} detail="Client-safe profiles" />
        <MetricCard label="Buy boxes" value={String(clientBuyerBuyBoxes.length)} detail="Manual/demo criteria" />
        <MetricCard label="Need review" value={String(reviewBuyers)} detail="Funding or buy box gaps" />
        <MetricCard label="Provider actions" value="0" detail="No buyer provider calls" />
      </div>

      <Section title="Buyer Confidence">
        <div className="record-list">
          {clientBuyerProfiles.map((buyer) => {
            const score = clientBuyerConfidenceScores.find((item) => item.buyerId === buyer.id);
            return (
              <RecordCard
                key={buyer.id}
                title={buyer.buyerName}
                meta={buyer.clientSafeSummary}
                right={<Link href={`/dashboard/client-command/disposition/buyers/${buyer.id}`}>View Details</Link>}
              >
                <div className="tag-row">
                  <Pill tone={score?.confidenceScore && score.confidenceScore >= 70 ? "green" : "gold"}>{score?.overallGrade ?? "Review"}</Pill>
                  <Pill tone={buyer.proofOfFundsStatus === "verified" ? "green" : "gold"}>{buyer.proofOfFundsStatus}</Pill>
                  <Pill tone="green">{buyer.maxPrice ? formatCurrency(buyer.maxPrice) : "price range missing"}</Pill>
                </div>
              </RecordCard>
            );
          })}
        </div>
      </Section>
    </div>
  );
}
