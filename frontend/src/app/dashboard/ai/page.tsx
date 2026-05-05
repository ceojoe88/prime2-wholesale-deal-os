import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  aiRequestLogs,
  approvedAiTemplates,
  blockedAiRequests,
  aiCostLedgers
} from "@/lib/demo-data";

export default function AiGatewayPage() {
  const tokens = aiRequestLogs.reduce((sum, request) => sum + request.tokenEstimate, 0);

  return (
    <div className="page">
      <PageHeader
        eyebrow="V20 AI Gateway"
        title="Controlled intelligence layer"
        description="Prime 2 can draft, summarize, assist negotiation, and brief through approved templates while safety scans, cost limits, and audit logs remain mandatory."
      />

      <div className="metric-grid">
        <MetricCard label="AI requests" value={String(aiRequestLogs.length)} detail={`${blockedAiRequests.length} blocked by guardrails`} />
        <MetricCard label="Templates" value={String(approvedAiTemplates.length)} detail="Versioned and system-data-only" />
        <MetricCard label="Token estimate" value={String(tokens)} detail="Tracked before provider use" />
        <MetricCard label="Provider mode" value="mock" detail="No real calls by default" />
      </div>

      <Section title="Allowed Intelligence">
        <div className="grid-three">
          {["seller_script_draft", "buyer_message_draft", "objection_response", "deal_summary", "daily_briefing", "negotiation_assist", "field_testing_summary"].map((type) => (
            <RecordCard key={type} title={type} meta="Template-gated request type" right={<Pill tone="green">allowed</Pill>} />
          ))}
        </div>
      </Section>

      <Section title="Hard Blocks">
        <div className="grid-three">
          {["legal advice", "contract generation", "profit promises", "deceptive urgency", "invented numbers", "calculation overrides"].map((item) => (
            <RecordCard key={item} title={item} meta="Rejected before response is released" right={<Pill tone="red">blocked</Pill>} />
          ))}
        </div>
      </Section>

      <Section title="AI Gateway Routes">
        <div className="grid-three">
          <RecordCard title="Audit" meta="Safety outcomes and response hashes" right={<Link href="/dashboard/ai/audit">Open</Link>} />
          <RecordCard title="Costs" meta={`${aiCostLedgers.length} cost ledger entries`} right={<Link href="/dashboard/ai/costs">Open</Link>} />
          <RecordCard title="Templates" meta="Approved prompt structures" right={<Link href="/dashboard/ai/templates">Open</Link>} />
        </div>
      </Section>
    </div>
  );
}

