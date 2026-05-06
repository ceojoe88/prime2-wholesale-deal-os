import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { getLiveProviderActivation, liveProviderActivations } from "@/lib/demo-data";

export function generateStaticParams() {
  return liveProviderActivations.map((activation) => ({ activationId: activation.id }));
}

export default function LiveActivationDetailPage({ params }: { params: { activationId: string } }) {
  const activation = getLiveProviderActivation(params.activationId);
  if (!activation) notFound();
  return (
    <div className="page">
      <PageHeader eyebrow={activation.providerType} title={activation.providerName} description={`${activation.laneType} / ${activation.allowedActionType}`} />
      <div className="metric-grid">
        <MetricCard label="Status" value={activation.activationStatus} detail="Gate result" />
        <MetricCard label="Mode" value={activation.activationMode} detail="Sandbox/live separation" />
        <MetricCard label="Owner approval" value={activation.ownerApprovalStatus} detail="Required for every lane" />
        <MetricCard label="Provider called" value="0" detail="Blocked until all gates pass" />
      </div>
      <div className="grid-two">
        <Section title="Activation Gate">
          <table className="data-table">
            <tbody>
              <tr><th>Dry-run receipt</th><td>{activation.dryRunReceiptId}</td></tr>
              <tr><th>Dry-run hash</th><td>{activation.dryRunHash}</td></tr>
              <tr><th>Current source hash</th><td>{activation.currentSourceHash}</td></tr>
              <tr><th>Live flag</th><td>{activation.liveFlagStatus}</td></tr>
              <tr><th>Idempotency</th><td>{activation.idempotencyKey}</td></tr>
            </tbody>
          </table>
        </Section>
        <Section title="Blocked Reasons">
          <div className="record-list">
            {activation.blockedReasons.map((reason) => (
              <RecordCard key={reason} title={reason} meta="Must clear before provider action" right={<Pill tone="red">blocked</Pill>} />
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
