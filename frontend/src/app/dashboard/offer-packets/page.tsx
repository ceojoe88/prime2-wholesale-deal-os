import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { formatCurrency, getDeal, getLead, offerPackets, offerReadyPackets } from "@/lib/demo-data";

export default function OfferPacketsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Offer Packet Prep Gate"
        title="Owner-approved offer packet control"
        description="Offer packet prep is allowed only when underwriting, compliance, buyer margin, target fee, and owner approval all pass."
      />
      <div className="metric-grid">
        <MetricCard label="Packets" value={String(offerPackets.length)} detail="Draft records" />
        <MetricCard label="Ready" value={String(offerReadyPackets.length)} detail="Owner-approved drafts" />
        <MetricCard label="Blocked" value={String(offerPackets.length - offerReadyPackets.length)} detail="Reasons tracked" />
        <MetricCard label="Live execution" value="0" detail="No real-world action" />
      </div>
      <Section title="Offer Packet Queue">
        <table className="data-table">
          <thead>
            <tr>
              <th>Packet</th>
              <th>Seller</th>
              <th>Max Seller</th>
              <th>Spread</th>
              <th>Approval</th>
              <th>Blocks</th>
            </tr>
          </thead>
          <tbody>
            {offerPackets.map((packet) => {
              const deal = getDeal(packet.dealId);
              const lead = deal ? getLead(deal.leadId) : undefined;
              return (
                <tr key={packet.id}>
                  <td><Link href={`/dashboard/offer-packets/${packet.id}`}>{packet.id}</Link><div className="record-meta">{packet.packetStatus}</div></td>
                  <td>{lead?.sellerName}<div className="record-meta">{lead?.stage}</div></td>
                  <td className="money">{formatCurrency(deal?.maxSellerOffer ?? 0)}</td>
                  <td className="money">{formatCurrency(deal?.projectedAssignmentFee ?? 0)}</td>
                  <td><Pill tone={packet.packetPrepAllowed ? "green" : "red"}>{packet.approvalStatus}</Pill></td>
                  <td>{packet.blockedReasons.length ? packet.blockedReasons.join(", ") : "clear"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
