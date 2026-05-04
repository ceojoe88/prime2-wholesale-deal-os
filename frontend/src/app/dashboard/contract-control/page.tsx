import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import {
  contractControls,
  contractPrepBlocked,
  contractPrepReady,
  formatCurrency,
  getDeal,
  getLead
} from "@/lib/demo-data";

export default function ContractControlPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V4 Contract Control"
        title="Contract prep gate"
        description="Offer-ready seller opportunities move into controlled prep only after accepted terms, underwriting, margin, compliance, and owner approvals clear."
      />
      <div className="metric-grid">
        <MetricCard label="Control records" value={String(contractControls.length)} detail="Internal only" />
        <MetricCard label="Prep ready" value={String(contractPrepReady.length)} detail="Draft prep allowed" />
        <MetricCard label="Blocked" value={String(contractPrepBlocked.length)} detail="Reason tracked" />
        <MetricCard label="Executions" value="0" detail="No contract execution" />
      </div>
      <Section title="Contract Control Queue">
        <table className="data-table">
          <thead>
            <tr>
              <th>Control</th>
              <th>Seller</th>
              <th>Accepted Price</th>
              <th>Spread</th>
              <th>Prep</th>
              <th>Blocks</th>
            </tr>
          </thead>
          <tbody>
            {contractControls.map((contract) => {
              const deal = getDeal(contract.dealId);
              const lead = getLead(contract.leadId);
              const price = Number(contract.sellerAcceptedTerms.price ?? deal?.sellerContractPrice ?? 0);
              return (
                <tr key={contract.id}>
                  <td>
                    <Link href={`/dashboard/contract-control/${contract.id}`}>{contract.id}</Link>
                    <div className="record-meta">{contract.contractStatus}</div>
                  </td>
                  <td>{lead?.sellerName}<div className="record-meta">{lead?.stage}</div></td>
                  <td className="money">{formatCurrency(price)}</td>
                  <td className="money">{formatCurrency(deal?.projectedAssignmentFee ?? 0)}</td>
                  <td><Pill tone={contract.contractPrepAllowed ? "green" : "red"}>{contract.contractPrepAllowed ? "ready" : "blocked"}</Pill></td>
                  <td>{contract.blockedReasons.length ? contract.blockedReasons.join(", ") : "clear"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
