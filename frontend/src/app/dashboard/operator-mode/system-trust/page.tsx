import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { currentSystemTrustScore } from "@/lib/demo-data";

export default function OperatorSystemTrustPage() {
  const trust = currentSystemTrustScore;

  return (
    <div className="page">
      <PageHeader
        eyebrow="System Health"
        title="System trust scoring"
        description="Track automation success, blocked unsafe actions, approval age, stale tasks, scoring confidence, forecast confidence, buyer response velocity, and seller conversion velocity."
      />

      <div className="metric-grid">
        <MetricCard label="Trust score" value={String(trust.overallTrustScore)} detail={trust.trustStatus} />
        <MetricCard label="Automation success" value={`${trust.automationSuccessRate}%`} detail="Internal prep success rate" />
        <MetricCard label="Blocked unsafe" value={String(trust.blockedUnsafeActions)} detail="Guardrails doing their job" />
        <MetricCard label="Approval age" value={`${trust.approvalQueueAgeHours}h`} detail="Owner queue freshness" />
      </div>

      <Section title="Trust Inputs">
        <div className="grid-three">
          <RecordCard title="Scoring confidence" meta="Opportunity and optimization confidence" right={<Pill>{trust.scoringConfidence}</Pill>} />
          <RecordCard title="Forecast confidence" meta="Revenue forecast confidence" right={<Pill>{trust.forecastConfidence}</Pill>} />
          <RecordCard title="Buyer velocity" meta="Buyer response speed and reliability" right={<Pill>{trust.buyerResponseVelocity}</Pill>} />
          <RecordCard title="Seller velocity" meta="Seller conversion momentum" right={<Pill>{trust.sellerConversionVelocity}</Pill>} />
          <RecordCard title="Stale tasks" meta="Open tasks past ideal window" right={<Pill tone={trust.staleTasks ? "gold" : "green"}>{trust.staleTasks}</Pill>} />
          <RecordCard title="Source basis" meta={trust.sourceRecordIds.join(", ")} right={<Pill>evidence</Pill>} />
        </div>
      </Section>
    </div>
  );
}
