import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  contractReadyDeals,
  fastestPathToContract,
  formatCurrency,
  getDeal,
  getLead,
  highReadinessNegotiations,
  offerConversionDealsAtRisk,
  offerPositioningRecords,
  projected10kContractsReady
} from "@/lib/demo-data";

export default function OfferConversionPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V10 Offer-to-Contract Conversion"
        title="Controlled offer conversion gate"
        description="Structure offer positioning, negotiation tracking, and acceptance readiness so high-confidence opportunities can be marked ready for external attorney/title drafting without creating contracts."
      />
      <div className="metric-grid">
        <MetricCard label="Positioning records" value={String(offerPositioningRecords.length)} detail="Strategy, anchors, walk-away, and concession range" />
        <MetricCard label="High readiness" value={String(highReadinessNegotiations.length)} detail="Seller readiness scored high or contract-ready" />
        <MetricCard label="Contract-ready" value={String(contractReadyDeals.length)} detail="External drafting readiness only" />
        <MetricCard label="10K+ ready" value={String(projected10kContractsReady.length)} detail="Projected contracts with protected spread" />
      </div>

      <div className="grid-two">
        <Section title="Offer Positioning Queue">
          <table className="data-table">
            <thead>
              <tr>
                <th>Deal</th>
                <th>Strategy</th>
                <th>Anchor / Ideal / Walk-Away</th>
                <th>Confidence</th>
                <th>Owner</th>
              </tr>
            </thead>
            <tbody>
              {offerPositioningRecords.map((record) => {
                const deal = getDeal(record.dealId);
                const lead = deal ? getLead(deal.leadId) : undefined;
                return (
                  <tr key={record.id}>
                    <td><Link href={`/dashboard/offer-conversion/${record.dealId}`}>{record.dealId}</Link><div className="record-meta">{lead?.city}, {lead?.state}</div></td>
                    <td>{record.offerStrategyType}</td>
                    <td className="money">{formatCurrency(record.anchorPrice)} / {formatCurrency(record.idealContractPrice)} / {formatCurrency(record.walkAwayPrice)}</td>
                    <td><Pill tone={record.confidenceScore >= 80 ? "green" : "gold"}>{record.confidenceScore}</Pill></td>
                    <td><Pill tone={record.ownerApprovalRecorded ? "green" : "gold"}>{record.ownerApprovalRecorded ? "approved" : "review"}</Pill></td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </Section>
        <Section title="Fastest Path To Contract">
          <div className="record-list">
            {fastestPathToContract.map((item) => (
              <RecordCard
                key={item.stateId}
                title={item.dealId}
                meta={item.actions.join(", ")}
                right={<Pill tone={item.blockedReasons.length ? "gold" : "green"}>{item.blockedReasons.length ? "gated" : "ready"}</Pill>}
              />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Safety Guard">
        <div className="grid-three">
          <RecordCard title="Executable contracts" meta="Not generated in V10." right={<Pill tone="red">off</Pill>} />
          <RecordCard title="Automatic acceptance" meta="Blocked; owner remains final approver." right={<Pill tone="red">off</Pill>} />
          <RecordCard title="Unsafe negotiation language" meta="False urgency, fake buyer claims, pressure, and legal statements are blocked." right={<Pill tone="green">guarded</Pill>} />
        </div>
      </Section>

      <Section title="Deals At Risk">
        <div className="record-list">
          {offerConversionDealsAtRisk.map((state) => (
            <RecordCard
              key={state.id}
              title={`${state.dealId} / ${state.id}`}
              meta={state.blockedReasons.join(", ")}
              right={<Pill tone="red">{state.blockedReasons.length}</Pill>}
            />
          ))}
        </div>
      </Section>
    </div>
  );
}
