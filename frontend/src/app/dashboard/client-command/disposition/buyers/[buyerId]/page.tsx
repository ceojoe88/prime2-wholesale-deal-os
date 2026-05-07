import Link from "next/link";
import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientBuyerBuyBoxes,
  clientBuyerProfiles,
  clientCommunicationApprovalGates,
  clientContactConsentRecords,
  clientContactOptOutRecords,
  clientDealBuyerMatches,
  getClientComplianceStatusesForBuyer,
  formatCurrency,
  getClientBuyer,
  getClientBuyerConfidence,
  getClientLead
} from "@/lib/demo-data";

export function generateStaticParams() {
  return clientBuyerProfiles.map((buyer) => ({ buyerId: buyer.id }));
}

export default function ClientCommandDispositionBuyerDetailPage({ params }: { params: { buyerId: string } }) {
  const buyer = getClientBuyer(params.buyerId);
  if (!buyer) {
    notFound();
  }
  const confidence = getClientBuyerConfidence(buyer.id);
  const buyBoxes = clientBuyerBuyBoxes.filter((box) => box.buyerId === buyer.id);
  const matches = clientDealBuyerMatches.filter((match) => match.buyerId === buyer.id);
  const safeStatuses = getClientComplianceStatusesForBuyer(buyer.id);
  const consentRecords = clientContactConsentRecords.filter((record) => record.buyerId === buyer.id);
  const optOutRecords = clientContactOptOutRecords.filter((record) => record.buyerId === buyer.id);
  const gates = clientCommunicationApprovalGates.filter((gate) => gate.buyerId === buyer.id);

  return (
    <div className="page">
      <PageHeader
        eyebrow="CP5 Buyer Detail"
        title={buyer.buyerName}
        description="Workspace-scoped buyer confidence, buy box fit, and deterministic match context. No buyer has been contacted."
      />

      <div className="metric-grid">
        <MetricCard label="Confidence" value={String(confidence?.confidenceScore ?? 0)} detail={confidence?.overallGrade ?? "Review"} />
        <MetricCard label="Funding" value={buyer.fundingStatus} detail={buyer.proofOfFundsStatus} />
        <MetricCard label="Buy boxes" value={String(buyBoxes.length)} detail="Client-entered criteria" />
        <MetricCard label="Matches" value={String(matches.length)} detail="Decision support only" />
      </div>

      <Section title="Buyer Confidence">
        <div className="grid-two">
          <RecordCard title="Buyer Profile" meta={buyer.clientSafeSummary} right={<Pill tone={buyer.activeStatus === "active" ? "green" : "gold"}>{buyer.activeStatus}</Pill>}>
            <div className="tag-row">
              <Pill tone="green">{buyer.buyerType}</Pill>
              <Pill tone="gold">{buyer.rehabTolerance} rehab</Pill>
              <Pill tone="gold">{buyer.closeSpeed} close</Pill>
              {buyer.maxPrice ? <Pill tone="green">{formatCurrency(buyer.maxPrice)}</Pill> : <Pill tone="red">price missing</Pill>}
            </div>
          </RecordCard>
          <RecordCard title="Confidence Score" meta={confidence?.reasonSummary ?? "Score Buyer to create a deterministic confidence snapshot."} right={<Pill tone={confidence?.requiresHumanReview ? "gold" : "green"}>{confidence?.overallGrade ?? "Review"}</Pill>}>
            <div className="tag-row">
              <Pill tone="gold">Funding {confidence?.fundingConfidenceScore ?? 0}</Pill>
              <Pill tone="gold">Buy Box {confidence?.buyBoxClarityScore ?? 0}</Pill>
              {confidence?.requiresHumanReview ? <Pill tone="gold">Human Review Needed</Pill> : null}
            </div>
          </RecordCard>
        </div>
      </Section>

      <Section title="Buy Box Fit">
        <div className="record-list">
          {buyBoxes.length === 0 ? (
            <RecordCard title="Buy box missing" meta="Add Buy Box before this buyer can become a strong deterministic match." right={<Pill tone="red">needs review</Pill>} />
          ) : (
            buyBoxes.map((box) => (
              <RecordCard key={box.id} title={`${box.market} buy box`} meta={box.notesSummary} right={<Pill tone="green">{box.dealTypePreference}</Pill>}>
                <div className="tag-row">
                  <Pill tone="green">{box.zipCodes.join(", ")}</Pill>
                  <Pill tone="gold">{box.rehabLevel} rehab</Pill>
                  <Pill tone="gold">{box.maxPurchasePrice ? formatCurrency(box.maxPurchasePrice) : "max missing"}</Pill>
                </div>
              </RecordCard>
            ))
          )}
        </div>
      </Section>

      <Section title="Deal Matches">
        <div className="record-list">
          {matches.length === 0 ? (
            <RecordCard title="No deal matches yet" meta="Match Buyers on a lead to evaluate fit." right={<Pill tone="gold">pending</Pill>} />
          ) : (
            matches.map((match) => {
              const lead = getClientLead(match.leadId);
              return (
                <RecordCard key={match.id} title={lead?.displayName ?? match.leadId} meta={match.clientSafeSummary} right={<Link href={`/dashboard/client-command/leads/${match.leadId}`}>View Details</Link>}>
                  <div className="tag-row">
                    <Pill tone={match.matchStatus === "strong_match" ? "green" : "gold"}>{match.matchStatus}</Pill>
                    <Pill tone="gold">{match.matchScore}</Pill>
                    {match.mismatchReasons.map((reason) => (
                      <Pill key={reason} tone="red">{reason}</Pill>
                    ))}
                  </div>
                </RecordCard>
              );
            })
          )}
        </div>
      </Section>

      <Section title="Compliance Manager">
        <div className="grid-two">
          <RecordCard title="Safe Contact Status" meta={safeStatuses[0]?.reasonSummary ?? "No buyer contact readiness recorded."} right={<Pill tone={safeStatuses[0]?.status === "safe_for_manual_use" ? "green" : safeStatuses[0]?.status === "blocked" ? "red" : "gold"}>{safeStatuses[0]?.status ?? "pending"}</Pill>}>
            <p>Readiness check only - no provider check or live communication occurred.</p>
            <div className="tag-row">
              <Pill tone="gold">Manual Use Only</Pill>
              <Pill tone="green">No Live Send</Pill>
              <Pill tone="green">No Provider Check</Pill>
            </div>
          </RecordCard>
          <RecordCard title="Communication Gate" meta={gates[0]?.clientSafeSummary ?? "No manual-use gate yet."} right={<Pill tone={gates[0]?.gateStatus === "manual_use_allowed" ? "green" : "gold"}>{gates[0]?.gateStatus ?? "pending"}</Pill>}>
            <p>Manual-use approval only - no message has been sent.</p>
          </RecordCard>
        </div>
      </Section>

      <div className="grid-two">
        <Section title="Consent Records">
          <div className="record-list">
            {consentRecords.length === 0 ? (
              <RecordCard title="No consent records" meta="Consent is still missing or untracked for this buyer." right={<Pill tone="gold">review</Pill>} />
            ) : (
              consentRecords.map((record) => (
                <RecordCard key={record.id} title={record.consentChannel} meta={record.consentSummary} right={<Pill tone={record.consentStatus === "confirmed" ? "green" : "gold"}>{record.consentStatus}</Pill>} />
              ))
            )}
          </div>
        </Section>
        <Section title="Opt-Out Records">
          <div className="record-list">
            {optOutRecords.length === 0 ? (
              <RecordCard title="No opt-out records" meta="No opt-out is stored for this buyer." right={<Pill tone="green">clear</Pill>} />
            ) : (
              optOutRecords.map((record) => (
                <RecordCard key={record.id} title={record.channel} meta={record.optOutSummary} right={<Pill tone={record.optOutStatus === "active" ? "red" : "gold"}>{record.optOutStatus}</Pill>} />
              ))
            )}
          </div>
        </Section>
      </div>
    </div>
  );
}
