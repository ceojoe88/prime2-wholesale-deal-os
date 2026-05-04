import { notFound } from "next/navigation";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  contractControls,
  formatCurrency,
  getContractControl,
  getDeal,
  getLead,
  getOfferPacket
} from "@/lib/demo-data";

export function generateStaticParams() {
  return contractControls.map((contract) => ({ contractId: contract.id }));
}

export default function ContractControlDetailPage({ params }: { params: { contractId: string } }) {
  const contract = getContractControl(params.contractId);
  if (!contract) notFound();
  const deal = getDeal(contract.dealId);
  const lead = getLead(contract.leadId);
  const packet = getOfferPacket(contract.offerPacketId);
  const acceptedPrice = Number(contract.sellerAcceptedTerms.price ?? deal?.sellerContractPrice ?? 0);

  return (
    <div className="page">
      <PageHeader
        eyebrow={contract.contractStatus}
        title={`${contract.id} / ${lead?.sellerName ?? contract.leadId}`}
        description="Contract prep is a draft-only control record with no executable contract generation, live sending, title submission, or automatic status change."
      />
      <div className="metric-grid">
        <div className="metric-card"><span>Accepted price</span><strong>{formatCurrency(acceptedPrice)}</strong><small>Terms recorded</small></div>
        <div className="metric-card"><span>Buyer margin</span><strong>{formatCurrency(deal?.buyerMargin ?? 0)}</strong><small>Must protect buyer</small></div>
        <div className="metric-card"><span>Spread</span><strong>{formatCurrency(deal?.projectedAssignmentFee ?? 0)}</strong><small>Calculated</small></div>
        <div className="metric-card"><span>Prep gate</span><strong>{contract.contractPrepAllowed ? "ready" : "blocked"}</strong><small>{contract.blockedReasons.length ? contract.blockedReasons.join(", ") : "clear"}</small></div>
      </div>
      <div className="grid-two">
        <Section title="Gate Checklist">
          <div className="record-list">
            <RecordCard title="Offer packet approved" meta={packet?.approvalStatus} right={<Pill tone={packet?.packetPrepAllowed ? "green" : "red"}>{packet?.packetPrepAllowed ? "passed" : "blocked"}</Pill>} />
            <RecordCard title="Seller accepted terms" meta={Object.keys(contract.sellerAcceptedTerms).length ? "recorded" : "missing"} right={<Pill tone={Object.keys(contract.sellerAcceptedTerms).length ? "green" : "red"}>{Object.keys(contract.sellerAcceptedTerms).length ? "passed" : "blocked"}</Pill>} />
            <RecordCard title="Compliance review" meta={contract.complianceReviewStatus} right={<Pill tone={contract.complianceReviewStatus === "approved" ? "green" : "red"}>{contract.complianceReviewStatus}</Pill>} />
            <RecordCard title="Owner approval" meta={contract.ownerApprovalStatus} right={<Pill tone={contract.ownerApprovalStatus === "approved" ? "green" : "red"}>{contract.ownerApprovalStatus}</Pill>} />
          </div>
        </Section>
        <Section title="Control Notes">
          <div className="record-list">
            <RecordCard title="Inspection/access" meta={contract.inspectionAccessNotes} />
            <RecordCard title="Earnest money" meta={contract.earnestMoneyNotes} />
            <RecordCard title="Title preference" meta={contract.titleCompanyPreference || "missing"} />
            <RecordCard title="Safety boundary" meta="Draft-only prep. Owner controls all real-world action." right={<Pill tone="red">no execution</Pill>} />
          </div>
        </Section>
      </div>
      <Section title="Required Documents">
        <div className="tag-row">
          {contract.requiredDocumentsChecklist.map((item) => <span className="tag" key={item}>{item}</span>)}
        </div>
      </Section>
    </div>
  );
}
