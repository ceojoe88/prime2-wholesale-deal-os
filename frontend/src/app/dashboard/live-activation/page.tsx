import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  blockedLiveProviderActivations,
  liveActivationSafetyCards,
  liveProviderActivations,
  readyLiveProviderActivations
} from "@/lib/demo-data";

export default function LiveActivationPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V30 Controlled Live Provider Activation"
        title="One-action provider activation gate"
        description="Prime 2 tracks owner-approved provider lanes, readiness snapshots, dry-run hashes, live flags, idempotency, blocked attempts, and audit events before any limited provider action."
      />
      <div className="metric-grid">
        {liveActivationSafetyCards.map((card) => (
          <MetricCard key={card.label} label={card.label} value={card.value} detail={card.detail} />
        ))}
      </div>
      <div className="grid-two">
        <Section title="Provider Lanes">
          <div className="record-list">
            {liveProviderActivations.map((activation) => (
              <RecordCard key={activation.id} title={activation.providerName} meta={`${activation.laneType} / ${activation.allowedActionType}`} right={<Link href={`/dashboard/live-activation/${activation.id}`}><Pill tone={activation.activationStatus === "blocked" ? "red" : "green"}>{activation.activationStatus}</Pill></Link>} />
            ))}
          </div>
        </Section>
        <Section title="Gate Routes">
          <div className="record-list">
            <RecordCard title="Readiness" meta={`${readyLiveProviderActivations.length} lanes ready`} right={<Link href="/dashboard/live-activation/readiness">Open</Link>} />
            <RecordCard title="Approvals" meta="Owner approval posture" right={<Link href="/dashboard/live-activation/approvals">Open</Link>} />
            <RecordCard title="Attempts" meta="Idempotent one-action records" right={<Link href="/dashboard/live-activation/attempts">Open</Link>} />
            <RecordCard title="Blocked" meta={`${blockedLiveProviderActivations.length} fail-closed lanes`} right={<Link href="/dashboard/live-activation/blocked">Open</Link>} />
          </div>
        </Section>
      </div>
    </div>
  );
}
