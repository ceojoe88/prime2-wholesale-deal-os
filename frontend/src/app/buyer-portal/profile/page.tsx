import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { buyers, formatCurrency } from "@/lib/demo-data";

const buyer = buyers[0];

export default function BuyerPortalProfilePage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Buyer Profile"
        title={buyer.company}
        description="Invite-gated profile details used for fit and proof-of-funds status. No payment or contract execution is available here."
      />
      <div className="metric-grid">
        <div className="metric-card"><span>Max purchase</span><strong>{formatCurrency(buyer.maxPurchasePrice)}</strong><small>Profile capacity</small></div>
        <div className="metric-card"><span>POF status</span><strong>{buyer.proofOfFundsStatus}</strong><small>Operator reviewed</small></div>
        <div className="metric-card"><span>Close speed</span><strong>{buyer.closingSpeedDays}d</strong><small>Profile signal</small></div>
        <div className="metric-card"><span>Access</span><strong>Invite</strong><small>No public signup</small></div>
      </div>
      <Section title="Criteria">
        <div className="pill-row">
          {buyer.targetZipCodes.map((zip) => <Pill key={zip}>{zip}</Pill>)}
          <Pill tone="green">{buyer.propertyType}</Pill>
        </div>
      </Section>
    </div>
  );
}
