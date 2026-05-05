import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  buyerAccelerationPofGaps,
  buyerResponseRoutes,
  buyerResponsesNeedingOwnerAction,
  getBuyer
} from "@/lib/demo-data";

export default function BuyerResponseRouterPage() {
  const accessRequests = buyerResponseRoutes.filter((route) => route.accessRequested);
  const offerIntentRoutes = buyerResponseRoutes.filter((route) => route.offerIntentRecorded);

  return (
    <div className="page">
      <PageHeader
        eyebrow="V14 Buyer Response Router"
        title="Buyer response routing"
        description="Classify buyer responses into owner-review queues: interested, needs POF, wants access, asks for details, offer intent, not interested, or follow-up later."
      />

      <div className="metric-grid">
        <MetricCard label="Responses" value={String(buyerResponseRoutes.length)} detail="All review-only" />
        <MetricCard label="Owner action" value={String(buyerResponsesNeedingOwnerAction.length)} detail="Queued for operator review" />
        <MetricCard label="POF gaps" value={String(buyerAccelerationPofGaps.length)} detail="Route before access" />
        <MetricCard label="Access requests" value={String(accessRequests.length)} detail="No automatic scheduling" />
      </div>

      <div className="grid-two">
        <Section title="Routing Buckets">
          <div className="record-list">
            <RecordCard title="Interested buyers" meta={`${offerIntentRoutes.length} with intent or interest to review`} right={<Pill tone="green">queue</Pill>} />
            <RecordCard title="POF needed" meta={`${buyerAccelerationPofGaps.length} buyers need proof-of-funds action`} right={<Pill tone="gold">verify</Pill>} />
            <RecordCard title="Access coordination" meta={`${accessRequests.length} requests require owner-controlled access review`} right={<Pill tone="gold">review</Pill>} />
            <RecordCard title="Execution" meta="No contract execution, no automatic negotiation, no live response." right={<Pill tone="red">off</Pill>} />
          </div>
        </Section>

        <Section title="Owner Action Queue">
          <div className="record-list">
            {buyerResponsesNeedingOwnerAction.map((route) => (
              <RecordCard
                key={route.id}
                title={`${getBuyer(route.buyerId)?.company ?? route.buyerId} / ${route.responseType}`}
                meta={route.recommendedNextStep}
                right={<Pill tone={route.pofGap ? "gold" : "green"}>{route.routedStatus}</Pill>}
              />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Response Records">
        <table className="data-table">
          <thead>
            <tr>
              <th>Route</th>
              <th>Buyer</th>
              <th>Deal</th>
              <th>Response</th>
              <th>POF</th>
              <th>Execution</th>
            </tr>
          </thead>
          <tbody>
            {buyerResponseRoutes.map((route) => (
              <tr key={route.id}>
                <td>{route.id}</td>
                <td>{getBuyer(route.buyerId)?.company ?? route.buyerId}</td>
                <td>{route.dealId}</td>
                <td>{route.responseType}</td>
                <td><Pill tone={route.pofGap ? "gold" : "green"}>{route.pofGap ? "needed" : "clear"}</Pill></td>
                <td><Pill tone="red">{route.contractExecutionAllowed ? "on" : "off"}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
