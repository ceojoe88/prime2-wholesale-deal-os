import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { formatCurrency, mobileApprovalQueue, mobileMoneyActions, mobileRiskActions } from "@/lib/demo-data";

export default function MobileTodayPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="Mobile Today" title="Today's field command" description="Prime 2 compresses the day into the highest-value money actions, risk reviews, and owner approval checks." />
      <div className="metric-grid">
        <MetricCard label="Money actions" value={String(mobileMoneyActions.length)} detail="Top fee-at-risk reviews" />
        <MetricCard label="Risk actions" value={String(mobileRiskActions.length)} detail="Resolve before movement" />
        <MetricCard label="Approvals" value={String(mobileApprovalQueue.length)} detail="Owner-only review queue" />
        <MetricCard label="Provider actions" value="off" detail="Existing gates still required" />
      </div>
      <div className="grid-two">
        <Section title="Top 5 Money Actions">
          <div className="record-list">
            {mobileMoneyActions.map((deal) => (
              <RecordCard key={deal.id} title={deal.id} meta={`Buyer margin ${formatCurrency(deal.buyerMargin)}`} right={<Link href={`/mobile/deals/${deal.id}`}><Pill tone="green">{formatCurrency(deal.projectedAssignmentFee)}</Pill></Link>} />
            ))}
          </div>
        </Section>
        <Section title="Top 5 Risk Actions">
          <div className="record-list">
            {mobileRiskActions.map((deal) => (
              <RecordCard key={deal.id} title={deal.id} meta={deal.riskFlags.join(", ") || "Review risk score"} right={<Pill tone="red">{deal.riskScore}</Pill>} />
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
