import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  deals,
  formatCurrency,
  getContractReadyStateByDeal,
  getDeal,
  getLead,
  getNegotiationByDeal,
  getOfferPositioningByDeal
} from "@/lib/demo-data";

export function generateStaticParams() {
  return deals.map((deal) => ({ dealId: deal.id }));
}

export default async function OfferConversionDetailPage({ params }: { params: Promise<{ dealId: string }> }) {
  const { dealId } = await params;
  const deal = getDeal(dealId);
  if (!deal) notFound();
  const lead = getLead(deal.leadId);
  const positioning = getOfferPositioningByDeal(dealId);
  const negotiation = getNegotiationByDeal(dealId);
  const state = getContractReadyStateByDeal(dealId);
  if (!positioning || !negotiation || !state) notFound();

  return (
    <div className="page">
      <PageHeader
        eyebrow={state.readinessStatus}
        title={`${deal.id} / ${lead?.city ?? "Property"}, ${lead?.state ?? ""}`}
        description="Contract-ready means numbers and negotiation are stable enough for external attorney/title drafting. No contract is generated, accepted, or executed here."
      />
      <div className="metric-grid">
        <MetricCard label="Readiness" value={negotiation.readinessLevel} detail={`${negotiation.readinessScore} score`} />
        <MetricCard label="Ideal price" value={formatCurrency(positioning.idealContractPrice)} detail={positioning.offerStrategyType} />
        <MetricCard label="Projected fee" value={formatCurrency(state.projectedAssignmentFee)} detail="Source deal projection" />
        <MetricCard label="Contract-ready" value={state.contractReady ? "yes" : "no"} detail="External drafting only" />
      </div>

      <div className="grid-two">
        <Section title="Offer Positioning">
          <div className="record-list">
            <RecordCard title="Pain alignment" meta={positioning.sellerPainAlignment.join(", ")} right={<Pill>{positioning.confidenceScore}</Pill>} />
            <RecordCard title="Comps" meta={positioning.justificationSummary.comps} />
            <RecordCard title="Repairs" meta={positioning.justificationSummary.repairs} />
            <RecordCard title="Timeline" meta={positioning.justificationSummary.timeline} />
            <RecordCard title="Concession range" meta={`${formatCurrency(positioning.concessionRange.low)} - ${formatCurrency(positioning.concessionRange.high)}`} right={<Pill tone="gold">safe range</Pill>} />
          </div>
        </Section>
        <Section title="Conversion Gate">
          <div className="record-list">
            <RecordCard title="Underwriting" meta={state.underwritingComplete ? "Complete" : "Missing"} right={<Pill tone={state.underwritingComplete ? "green" : "red"}>{state.underwritingComplete ? "pass" : "block"}</Pill>} />
            <RecordCard title="Profit control" meta={state.profitControlValidated ? "Spread and buyer margin validated" : "Needs review"} right={<Pill tone={state.profitControlValidated ? "green" : "red"}>{state.profitControlValidated ? "pass" : "block"}</Pill>} />
            <RecordCard title="Buyer demand" meta={state.buyerDemandConfirmed ? "Confirmed" : "Not confirmed"} right={<Pill tone={state.buyerDemandConfirmed ? "green" : "gold"}>{state.buyerDemandConfirmed ? "pass" : "review"}</Pill>} />
            <RecordCard title="Compliance" meta={state.compliancePassed ? "Passed" : "Blocked"} right={<Pill tone={state.compliancePassed ? "green" : "red"}>{state.compliancePassed ? "pass" : "block"}</Pill>} />
            <RecordCard title="Owner approval" meta={state.ownerApprovalRecorded ? "Recorded" : "Missing"} right={<Pill tone={state.ownerApprovalRecorded ? "green" : "gold"}>{state.ownerApprovalRecorded ? "approved" : "review"}</Pill>} />
          </div>
        </Section>
      </div>

      <Section title="Negotiation Tracking">
        <div className="record-list">
          <RecordCard title="Seller last response" meta={negotiation.sellerLastResponse} right={<Pill>{negotiation.negotiationStage}</Pill>} />
          <RecordCard title="Objections" meta={negotiation.sellerObjections.join(", ")} right={<Pill tone="gold">{formatCurrency(negotiation.counterOffer ?? 0)}</Pill>} />
          <RecordCard title="Signals" meta={negotiation.emotionalSignals.join(", ")} />
          <RecordCard title="Next move" meta={negotiation.nextMoveRecommendation} right={<Pill tone="green">recommend</Pill>} />
        </div>
      </Section>

      <Section title="Contract-Ready Boundary">
        <div className="grid-three">
          <RecordCard title="External drafting" meta={state.readyForExternalDrafting ? "Ready for attorney/title drafting request." : "Blocked until all gates pass."} right={<Pill tone={state.readyForExternalDrafting ? "green" : "red"}>{state.readyForExternalDrafting ? "ready" : "blocked"}</Pill>} />
          <RecordCard title="Executable contract" meta="Not generated by the system." right={<Pill tone="red">off</Pill>} />
          <RecordCard title="Automatic acceptance" meta="Not allowed." right={<Pill tone="red">off</Pill>} />
        </div>
      </Section>
    </div>
  );
}
