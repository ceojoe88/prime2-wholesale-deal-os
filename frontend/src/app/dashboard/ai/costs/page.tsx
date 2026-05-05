import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { aiCostLedgers } from "@/lib/demo-data";

export default function AiCostsPage() {
  const total = aiCostLedgers.reduce((sum, ledger) => sum + ledger.costEstimate, 0);
  const tokens = aiCostLedgers.reduce((sum, ledger) => sum + ledger.tokenEstimate, 0);

  return (
    <div className="page">
      <PageHeader
        eyebrow="V20 AI Cost Controls"
        title="Token and cost ledger"
        description="Prime 2 estimates tokens and monthly cost before AI output is approved. The default template mode records zero provider spend."
      />

      <div className="metric-grid">
        <MetricCard label="Estimated spend" value={`$${total.toFixed(2)}`} detail="Current seeded period" />
        <MetricCard label="Tokens" value={String(tokens)} detail="Per-request estimate" />
        <MetricCard label="Monthly cap" value="$25" detail="Config driven" />
        <MetricCard label="Provider calls" value="0" detail="No live AI call path" />
      </div>

      <Section title="Cost Entries">
        <table className="data-table">
          <thead>
            <tr>
              <th>Ledger</th>
              <th>Request</th>
              <th>Period</th>
              <th>Tokens</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {aiCostLedgers.map((ledger) => (
              <tr key={ledger.id}>
                <td>{ledger.id}</td>
                <td>{ledger.requestId}</td>
                <td>{ledger.period}</td>
                <td>{ledger.tokenEstimate}</td>
                <td><Pill tone={ledger.capStatus === "within_cap" ? "green" : "red"}>{ledger.capStatus}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}

