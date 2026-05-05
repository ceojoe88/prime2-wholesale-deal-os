import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  buyerAccelerationBlockedRecords,
  buyerAccelerationPofGaps,
  buyerAccelerationReadyDeals,
  buyerAccelerationRecords,
  buyerAccelerationSafetyCards,
  controlledDistributionAttempts,
  formatCurrency,
  getBuyer,
  getDeal,
  getLead,
  topBuyerForTenKDeals
} from "@/lib/demo-data";

export default function BuyerAccelerationPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V14 Buyer Distribution Acceleration"
        title="Buyer acceleration command"
        description="Rank fast-close buyers, prepare controlled one-recipient distribution, route buyer responses, and keep every live path behind sanitizer, owner approval, and V5/V13 gates."
      />

      <div className="metric-grid">
        <MetricCard label="Acceleration records" value={String(buyerAccelerationRecords.length)} detail="Deal-level buyer speed snapshots" />
        <MetricCard label="Controlled-ready" value={String(buyerAccelerationReadyDeals.length)} detail="One-recipient gated distribution only" />
        <MetricCard label="POF gaps" value={String(buyerAccelerationPofGaps.length)} detail="Routed before access or offer follow-up" />
        <MetricCard label="Blocked records" value={String(buyerAccelerationBlockedRecords.length)} detail="Margin, sanitizer, compliance, or approval gaps" />
      </div>

      <Section title="Safety Boundaries">
        <div className="grid-three">
          {buyerAccelerationSafetyCards.map((card) => (
            <RecordCard
              key={card.label}
              title={card.label}
              meta={card.detail}
              right={<Pill tone={card.value === "off" ? "red" : "green"}>{card.value}</Pill>}
            />
          ))}
        </div>
      </Section>

      <div className="grid-two">
        <Section title="Top Buyer For 10K+ Deals">
          <div className="record-list">
            {topBuyerForTenKDeals.map(({ record, deal, buyer }) => (
              <RecordCard
                key={record.id}
                title={`${deal.id} / ${buyer?.company ?? record.topBuyerList[0]}`}
                meta={`Projected spread ${formatCurrency(deal.projectedAssignmentFee)} with buyer margin strength ${record.buyerMarginStrength}`}
                right={<Pill tone="green">ready</Pill>}
              />
            ))}
          </div>
        </Section>

        <Section title="Attempts And Blocked Reasons">
          <div className="record-list">
            {controlledDistributionAttempts.map((attempt) => (
              <RecordCard
                key={attempt.dealId}
                title={attempt.dealId}
                meta={attempt.blockedReasons.length ? attempt.blockedReasons.join(", ") : "V5/V13 gates clear for one approved draft"}
                right={<Pill tone={attempt.status === "blocked" ? "red" : "green"}>{attempt.status === "blocked" ? "blocked" : "ready"}</Pill>}
              />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Buyer Acceleration Records">
        <table className="data-table">
          <thead>
            <tr>
              <th>Deal</th>
              <th>Top Buyer</th>
              <th>POF</th>
              <th>Margin</th>
              <th>Owner Approval</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {buyerAccelerationRecords.map((record) => {
              const deal = getDeal(record.dealId);
              const lead = deal ? getLead(deal.leadId) : undefined;
              const buyer = getBuyer(record.topBuyerList[0]);
              return (
                <tr key={record.id}>
                  <td>
                    <Link href={`/dashboard/buyer-acceleration/${record.dealId}`}>{record.dealId}</Link>
                    <div className="record-meta">{lead?.city}, {lead?.state}</div>
                  </td>
                  <td>{buyer?.company ?? record.topBuyerList[0]}</td>
                  <td><Pill tone={record.pofStatus === "verified" ? "green" : "gold"}>{record.pofStatus}</Pill></td>
                  <td>{record.buyerMarginStrength}</td>
                  <td>{record.ownerApprovalStatus}</td>
                  <td><Pill tone={record.controlledSendAllowed ? "green" : "red"}>{record.distributionReadiness}</Pill></td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
