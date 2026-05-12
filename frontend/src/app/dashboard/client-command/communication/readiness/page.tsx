import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientCommunicationLiveReadinessChecks } from "@/lib/demo-data";

export default function ClientCommandCommunicationReadinessPage() {
  const safe = clientCommunicationLiveReadinessChecks.filter((item) => item.readinessStatus === "ready");
  const blocked = clientCommunicationLiveReadinessChecks.filter((item) => item.readinessStatus === "blocked");

  return (
    <div className="page">
      <PageHeader eyebrow="CP10 Readiness" title="Communication Readiness Checks" description="Blocked by default unless compliance, plan, approval, and live flags pass." />
      <div className="metric-grid">
        <MetricCard label="Checks" value={String(clientCommunicationLiveReadinessChecks.length)} detail="Single-message reviews only" />
        <MetricCard label="Blocked" value={String(blocked.length)} detail="No provider call" />
        <MetricCard label="Ready" value={String(safe.length)} detail="Still requires live flags" />
        <MetricCard label="Dry run state" value="required" detail="Dry run does not send a message." />
      </div>
      <Section title="Readiness Records">
        <div className="record-list">
          {clientCommunicationLiveReadinessChecks.map((item) => (
            <RecordCard
              key={item.id}
              title={item.sourceDraftId || item.sourceDraftType.replaceAll("_", " ")}
              meta={`Status: ${item.readinessStatus}. ${item.blockReasons.join(", ") || "No blockers."}`}
              right={<Pill tone={item.readinessStatus === "blocked" ? "red" : "green"}>{item.channel}</Pill>}
            />
          ))}
        </div>
      </Section>
    </div>
  );
}
