import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientDealEvidencePackets,
  clientOfferReadinessGates,
  clientUnderwritingReviews
} from "@/lib/demo-data";

export default function ClientCommandUnderwritingPage() {
  const ready = clientOfferReadinessGates.filter((gate) => gate.readinessStatus === "ready_for_client_review");
  const blocked = clientOfferReadinessGates.filter((gate) => gate.readinessStatus !== "ready_for_client_review");
  return (
    <div className="page">
      <PageHeader
        eyebrow="CP4 Underwriting + Evidence"
        title="Underwriting Manager command"
        description="Client-safe evidence packets, transparent MAO math, offer scenarios, and readiness gates. Decision support only."
      />

      <div className="metric-grid">
        <MetricCard label="Evidence packets" value={String(clientDealEvidencePackets.length)} detail="Manual/demo evidence only" />
        <MetricCard label="Reviews" value={String(clientUnderwritingReviews.length)} detail="Transparent deterministic math" />
        <MetricCard label="Ready review" value={String(ready.length)} detail="Client review queue" />
        <MetricCard label="Blocked" value={String(blocked.length)} detail="Missing evidence or inputs" />
      </div>

      <Section title="Underwriting Division Cards">
        <div className="grid-three">
          <RecordCard title="Underwriting Manager" meta="Checks ARV, repair estimate, holding cost, target assignment fee, MAO, and scenarios." right={<Pill tone="green">active</Pill>} />
          <RecordCard title="Evidence Packet" meta="Requires seller, repair, comp, occupancy, and title-review notes." right={<Pill tone="gold">gated</Pill>} />
          <RecordCard title="Offer Readiness Gate" meta="Decision support only — no contract or offer has been sent." right={<Pill tone="red">locked</Pill>} />
        </div>
      </Section>

      <Section title="Underwriting Queues">
        <div className="grid-three">
          <RecordCard title="Ready Review" meta={`${ready.length} leads ready for client decision support`} right={<Link href="/dashboard/client-command/underwriting/ready-review">View Details</Link>} />
          <RecordCard title="Blocked" meta={`${blocked.length} leads blocked by evidence or review gaps`} right={<Link href="/dashboard/client-command/underwriting/blocked">View Details</Link>} />
          <RecordCard title="Lead Detail" meta="Evidence, scenarios, and readiness live on each lead page" right={<Link href="/dashboard/client-command/leads">View Details</Link>} />
        </div>
      </Section>
    </div>
  );
}
