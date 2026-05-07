import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientBuyerDemandEvidence,
  clientBuyerProfiles,
  clientDealBuyerMatches,
  clientDispositionReadinessGates,
  clientBuyerOutreachDrafts
} from "@/lib/demo-data";

export default function ClientCommandDispositionPage() {
  const ready = clientDispositionReadinessGates.filter((gate) => gate.readinessStatus === "ready_for_client_review");
  const blocked = clientDispositionReadinessGates.filter((gate) => gate.readinessStatus !== "ready_for_client_review");
  const strongMatches = clientDealBuyerMatches.filter((match) => match.matchStatus === "strong_match");
  return (
    <div className="page">
      <PageHeader
        eyebrow="CP5 Buyer Matching"
        title="Disposition Manager command"
        description="Client-safe buyer matching, buyer demand evidence, manual-only buyer drafts, and disposition readiness. Decision support only."
      />

      <div className="metric-grid">
        <MetricCard label="Buyer profiles" value={String(clientBuyerProfiles.length)} detail="Workspace-scoped demo buyers" />
        <MetricCard label="Strong matches" value={String(strongMatches.length)} detail="Buy box fit" />
        <MetricCard label="Ready review" value={String(ready.length)} detail="Manual review only" />
        <MetricCard label="Blocked" value={String(blocked.length)} detail="Needs evidence or CP4 clearance" />
      </div>

      <Section title="Disposition Division Cards">
        <div className="grid-three">
          <RecordCard title="Disposition Manager" meta="Checks buyer confidence, buy box fit, demand evidence, and readiness." right={<Pill tone="green">CP5</Pill>} />
          <RecordCard title="Buyer Demand Evidence" meta={`${clientBuyerDemandEvidence.length} client-safe evidence notes`} right={<Pill tone="gold">manual</Pill>} />
          <RecordCard title="Buyer Drafts" meta={`${clientBuyerOutreachDrafts.length} manual-use drafts`} right={<Pill tone="red">no live send</Pill>} />
        </div>
      </Section>

      <Section title="Disposition Queues">
        <div className="grid-three">
          <RecordCard title="Buyers" meta="Buyer profiles and confidence scores" right={<Link href="/dashboard/client-command/disposition/buyers">View Details</Link>} />
          <RecordCard title="Matches" meta={`${clientDealBuyerMatches.length} deterministic match records`} right={<Link href="/dashboard/client-command/disposition/matches">View Details</Link>} />
          <RecordCard title="Ready Review" meta={`${ready.length} leads ready for manual review`} right={<Link href="/dashboard/client-command/disposition/ready-review">View Details</Link>} />
          <RecordCard title="Blocked" meta={`${blocked.length} leads blocked from disposition`} right={<Link href="/dashboard/client-command/disposition/blocked">View Details</Link>} />
          <RecordCard title="Needs Review" meta="Human-review disposition queue" right={<Link href="/dashboard/client-command/disposition/needs-review">View Details</Link>} />
          <RecordCard title="Lead 5 CP5 Demo" meta="Memphis buyer matching-ready scenario" right={<Link href="/dashboard/client-command/leads/client-lead-memphis-005">View Details</Link>} />
        </div>
      </Section>
    </div>
  );
}
