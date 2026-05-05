import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  buyerAccelerationRecords,
  formatCurrency,
  getBuyer,
  getBuyerAccelerationRecordByDeal,
  getBuyerResponseRoutesForDeal,
  getBuyerSequencesForDeal,
  getDeal,
  getLead
} from "@/lib/demo-data";

export function generateStaticParams() {
  return buyerAccelerationRecords.map((record) => ({ dealId: record.dealId }));
}

export default async function BuyerAccelerationDetailPage({
  params
}: {
  params: Promise<{ dealId: string }>;
}) {
  const { dealId } = await params;
  const record = getBuyerAccelerationRecordByDeal(dealId);
  if (!record) notFound();
  const deal = getDeal(record.dealId);
  const lead = deal ? getLead(deal.leadId) : undefined;
  const sequences = getBuyerSequencesForDeal(record.dealId);
  const routes = getBuyerResponseRoutesForDeal(record.dealId);

  return (
    <div className="page">
      <PageHeader
        eyebrow={record.distributionReadiness}
        title={`${record.dealId} buyer acceleration`}
        description="Controlled distribution stays one buyer, one approved draft, one source record, and one audit path. Buyer-facing content is sanitized before any owner-approved send."
      />

      <div className="metric-grid">
        <MetricCard label="Projected spread" value={formatCurrency(deal?.projectedAssignmentFee ?? 0)} detail="Internal operator view only" />
        <MetricCard label="Buyer margin strength" value={String(record.buyerMarginStrength)} detail="Weak margin blocks distribution" />
        <MetricCard label="POF status" value={record.pofStatus} detail="POF request allowed when that is the message purpose" />
        <MetricCard label="Controlled send" value={record.controlledSendAllowed ? "ready" : "blocked"} detail="Requires V5/V13 gates" />
      </div>

      <div className="grid-two">
        <Section title="Gate Conditions">
          <div className="record-list">
            <RecordCard title="Buyer-visible deal" meta={record.buyerVisible ? "Marked visible and sanitized" : "Buyer visibility blocked"} right={<Pill tone={record.buyerVisible ? "green" : "red"}>{record.buyerVisible ? "yes" : "no"}</Pill>} />
            <RecordCard title="Sanitized deal sheet" meta={record.sanitizedDealSheetReady ? "External-safe sheet ready" : "Sanitizer missing"} right={<Pill tone={record.sanitizedDealSheetReady ? "green" : "red"}>{record.sanitizedDealSheetReady ? "ready" : "blocked"}</Pill>} />
            <RecordCard title="Buyer match" meta={record.buyerMatchApproved ? "Approved match" : "Match needs owner review"} right={<Pill tone={record.buyerMatchApproved ? "green" : "red"}>{record.buyerMatchApproved ? "approved" : "pending"}</Pill>} />
            <RecordCard title="Compliance" meta={record.compliancePassed ? "Compliance clear" : "Compliance blocker"} right={<Pill tone={record.compliancePassed ? "green" : "red"}>{record.compliancePassed ? "passed" : "blocked"}</Pill>} />
            <RecordCard title="V5/V13 gates" meta={`V5 ${record.v5GatePassed ? "passed" : "missing"} / V13 ${record.v13GatePassed ? "passed" : "missing"}`} right={<Pill tone={record.v5GatePassed && record.v13GatePassed ? "green" : "red"}>gated</Pill>} />
          </div>
        </Section>

        <Section title="Top Buyer List">
          <div className="record-list">
            {record.buyerRankingSnapshot.map((ranking) => {
              const buyer = getBuyer(ranking.buyerId);
              return (
                <RecordCard
                  key={ranking.buyerId}
                  title={`${ranking.rank}. ${buyer?.company ?? ranking.buyerId}`}
                  meta={`${buyer?.proofOfFundsStatus ?? "unknown"} POF / ${buyer?.closingSpeedDays ?? "n/a"} day close profile`}
                  right={<Pill tone={ranking.priorityScore >= 90 ? "green" : "gold"}>{ranking.priorityScore}</Pill>}
                />
              );
            })}
          </div>
        </Section>
      </div>

      <Section title="Draft Buyer Sequence">
        <div className="record-list">
          {sequences.map((sequence) => (
            <RecordCard
              key={sequence.id}
              title={`${sequence.id} / ${getBuyer(sequence.buyerId)?.company ?? sequence.buyerId}`}
              meta={sequence.blockedReasons.length ? sequence.blockedReasons.join(", ") : sequence.firstBuyerNotice}
              right={<Pill tone={sequence.safetyStatus === "blocked" ? "red" : "green"}>{sequence.safetyStatus}</Pill>}
            />
          ))}
        </div>
      </Section>

      <Section title="Buyer Response Routing">
        <table className="data-table">
          <thead>
            <tr>
              <th>Buyer</th>
              <th>Response</th>
              <th>Route</th>
              <th>POF Gap</th>
              <th>Next Step</th>
            </tr>
          </thead>
          <tbody>
            {routes.map((route) => (
              <tr key={route.id}>
                <td>{getBuyer(route.buyerId)?.company ?? route.buyerId}</td>
                <td>{route.responseType}</td>
                <td>{route.routedStatus}</td>
                <td><Pill tone={route.pofGap ? "gold" : "green"}>{route.pofGap ? "yes" : "no"}</Pill></td>
                <td>{route.recommendedNextStep}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>

      <Section title="Property Context">
        <RecordCard
          title={`${lead?.city ?? "Unknown"}, ${lead?.state ?? ""}`}
          meta={`${lead?.propertyType ?? "property"} / buyer-facing details remain sanitized`}
          right={<Pill>{record.ownerApprovalStatus}</Pill>}
        />
      </Section>
    </div>
  );
}
