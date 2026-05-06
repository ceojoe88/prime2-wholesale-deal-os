import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { liveActivationApprovalsNeeded, liveProviderActivations } from "@/lib/demo-data";

export default function LiveActivationApprovalsPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="Live Approvals" title="Owner approval posture" description="Every provider lane remains owner-approved, one-action, source-linked, and idempotent before it can move beyond blocked review." />
      <div className="metric-grid">
        <MetricCard label="Approval needed" value={String(liveActivationApprovalsNeeded.length)} detail="Owner queue" />
        <MetricCard label="Approved records" value={String(liveProviderActivations.length - liveActivationApprovalsNeeded.length)} detail="Still needs other gates" />
        <MetricCard label="Bypass" value="off" detail="Worker and campaign bypass blocked" />
        <MetricCard label="Provider called" value="0" detail="No call from approval page" />
      </div>
      <Section title="Approval Records">
        <div className="record-list">
          {liveProviderActivations.map((activation) => (
            <RecordCard key={activation.id} title={activation.providerName} meta={activation.ownerApprovalStatus} right={<Pill tone={activation.ownerApprovalStatus === "approved" ? "green" : "gold"}>{activation.activationStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
