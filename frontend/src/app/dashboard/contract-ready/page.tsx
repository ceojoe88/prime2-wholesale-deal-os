import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  contractReadyDeals,
  contractReadyStates,
  formatCurrency,
  getDeal,
  getLead,
  offerConversionDealsAtRisk,
  projected10kContractsReady
} from "@/lib/demo-data";

export default function ContractReadyPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V10 Contract-Ready State"
        title="External drafting readiness"
        description="Marks opportunities ready for attorney/title drafting only when underwriting, profit control, buyer demand, compliance, risk, seller readiness, and owner approval gates pass."
      />
      <div className="metric-grid">
        <MetricCard label="Contract-ready deals" value={String(contractReadyDeals.length)} detail="No contract is generated" />
        <MetricCard label="10K+ ready" value={String(projected10kContractsReady.length)} detail="Projected fee target protected" />
        <MetricCard label="At risk" value={String(offerConversionDealsAtRisk.length)} detail="Blocked readiness records" />
        <MetricCard label="Execution" value="off" detail="Owner plus attorney/title path only" />
      </div>

      <Section title="Contract-Ready Gate Matrix">
        <table className="data-table">
          <thead>
            <tr>
              <th>Deal</th>
              <th>Status</th>
              <th>Projected Fee</th>
              <th>Buyer Demand</th>
              <th>Seller Ready</th>
              <th>Blocks</th>
            </tr>
          </thead>
          <tbody>
            {contractReadyStates.map((state) => {
              const deal = getDeal(state.dealId);
              const lead = deal ? getLead(deal.leadId) : undefined;
              return (
                <tr key={state.id}>
                  <td><Link href={`/dashboard/offer-conversion/${state.dealId}`}>{state.dealId}</Link><div className="record-meta">{lead?.city}, {lead?.state}</div></td>
                  <td><Pill tone={state.contractReady ? "green" : "red"}>{state.readinessStatus}</Pill></td>
                  <td className="money">{formatCurrency(state.projectedAssignmentFee)}</td>
                  <td>{state.buyerDemandConfirmed ? "confirmed" : "not confirmed"}</td>
                  <td>{state.sellerReadinessHigh ? "high" : "not high"}</td>
                  <td>{state.blockedReasons.length ? state.blockedReasons.join(", ") : "clear"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>

      <div className="grid-two">
        <Section title="Projected 10K+ Contracts Ready">
          <div className="record-list">
            {projected10kContractsReady.map((state) => (
              <RecordCard key={state.id} title={state.dealId} meta="External drafting readiness only" right={<Pill tone="green">{formatCurrency(state.projectedAssignmentFee)}</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Boundary">
          <div className="record-list">
            <RecordCard title="External drafting" meta="Attorney/title drafting reminder; no executable contract output." right={<Pill tone="green">required</Pill>} />
            <RecordCard title="Automatic acceptance" meta="Blocked; seller acceptance is never executed by the system." right={<Pill tone="red">off</Pill>} />
            <RecordCard title="Legal advice" meta="Blocked; use title/attorney review reminders." right={<Pill tone="red">off</Pill>} />
          </div>
        </Section>
      </div>
    </div>
  );
}
