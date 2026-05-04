import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { buyerVisibleDeals, formatCurrency } from "@/lib/demo-data";

export default function BuyerPortalPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Invite-Gated"
        title="Controlled buyer deal room"
        description="Only operator-published, compliance-cleared deals appear here. Interest is a draft intent for owner review, not a contract or payment action."
      />
      <div className="metric-grid">
        <MetricCard label="Visible deals" value={String(buyerVisibleDeals.length)} detail="Sanitized and gated" />
        <MetricCard label="Public signup" value="Off" detail="Invite access only" />
        <MetricCard label="Contract execution" value="Off" detail="Intent records only" />
        <MetricCard label="Payment collection" value="Off" detail="No checkout flow" />
      </div>
      <Section title="Available Deal Rooms">
        <div className="grid-three">
          {buyerVisibleDeals.map((deal) => (
            <RecordCard
              key={deal.dealId}
              title={`${deal.city}, ${deal.state} ${deal.zipCode}`}
              meta={`${deal.propertyType} / ${deal.beds} bd / ${deal.baths} ba / ${deal.sqft} sqft`}
              right={<Pill tone="green">{deal.availabilityStatus}</Pill>}
            >
              <span className="record-meta">Asking {deal.askingPrice ? formatCurrency(deal.askingPrice) : "review"} / buyer margin {deal.estimatedBuyerMargin ? formatCurrency(deal.estimatedBuyerMargin) : "review"}</span>
              <Link className="pill green" href={`/buyer-portal/deals/${deal.dealId}`}>open deal room</Link>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}
