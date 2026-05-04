import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  dailyCommandBriefings,
  formatCurrency,
  getDeal,
  latestAutonomyDailyBriefing
} from "@/lib/demo-data";

export default function AutonomyDailyBriefingPage() {
  const briefing = latestAutonomyDailyBriefing;
  const hotFeeTotal = briefing?.hotDeals.reduce((total, deal) => total + deal.projectedAssignmentFee, 0) ?? 0;

  return (
    <div className="page">
      <PageHeader
        eyebrow="V12 Daily Command Briefing"
        title="Wholesale Prime briefing"
        description="Autonomous daily briefings summarize hot deals, owner queues, blockers, and safe next actions as recommendations only."
      />

      <div className="metric-grid">
        <MetricCard label="Briefings" value={String(dailyCommandBriefings.length)} detail="Internal briefing records" />
        <MetricCard label="Hot deals" value={String(briefing?.hotDeals.length ?? 0)} detail="Ranked for owner review" />
        <MetricCard label="Hot fee exposure" value={formatCurrency(hotFeeTotal)} detail="Projected, not guaranteed" />
        <MetricCard label="Execution" value="0" detail="No live actions" />
      </div>

      {briefing && (
        <>
          <Section title={`${briefing.generatedBy} Briefing`}>
            <div className="command-band">
              <strong>{briefing.briefingDate}</strong>
              <div className="pill-row">
                <Pill tone="green">draft-only</Pill>
                <Pill tone="red">live outreach off</Pill>
                <Pill tone="red">title submission off</Pill>
                <Pill tone="red">contract execution off</Pill>
              </div>
              <span className="muted">Recommendations are internal only and remain subject to owner approval.</span>
            </div>
          </Section>

          <div className="grid-two">
            <Section title="Hot Deals">
              <div className="record-list">
                {briefing.hotDeals.map((hotDeal) => {
                  const deal = getDeal(hotDeal.dealId);
                  return (
                    <RecordCard key={hotDeal.dealId} title={hotDeal.dealId} meta={`Speed ${hotDeal.dealSpeedScore} / fee ${formatCurrency(hotDeal.projectedAssignmentFee)}`} right={<Pill tone={deal?.hot ? "red" : "gold"}>review</Pill>} />
                  );
                })}
              </div>
            </Section>
            <Section title="Owner Priority Actions">
              <div className="record-list">
                {briefing.priorityActions.map((action) => (
                  <RecordCard key={action} title={action} meta="Recommendation only" right={<Pill tone="gold">owner</Pill>} />
                ))}
              </div>
            </Section>
          </div>

          <div className="grid-two">
            <Section title="Manager Queue">
              <div className="record-list">
                {briefing.managerQueue.map((item) => (
                  <RecordCard key={item.division} title={item.manager} meta={`${item.division}: ${item.nextBestAction}`} right={<Pill>queue</Pill>} />
                ))}
              </div>
            </Section>
            <Section title="Safety Summary">
              <div className="record-list">
                {Object.entries(briefing.safetySummary).map(([label, enabled]) => (
                  <RecordCard key={label} title={label} meta={enabled ? "Enabled" : "Blocked"} right={<Pill tone={enabled ? "green" : "red"}>{enabled ? "on" : "off"}</Pill>} />
                ))}
              </div>
            </Section>
          </div>
        </>
      )}
    </div>
  );
}
