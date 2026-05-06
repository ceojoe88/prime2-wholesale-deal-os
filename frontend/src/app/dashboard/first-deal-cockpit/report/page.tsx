import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { firstDealReport, formatCurrency } from "@/lib/demo-data";

export default function FirstDealReportPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V31 Field-Test Report"
        title="First batch learning report"
        description="Prime 2 summarizes import, QA, calls, motivated sellers, offers, buyer matches, contract-ready candidates, projected spread, misses, and next-batch recommendations."
      />
      <div className="metric-grid">
        <MetricCard label="Leads imported" value={String(firstDealReport.leadsImported)} detail="First batch sample" />
        <MetricCard label="QA passed" value={String(firstDealReport.leadsQaPassed)} detail="Data confidence clear" />
        <MetricCard label="Sellers reached" value={String(firstDealReport.sellersReached)} detail="Logged outcomes" />
        <MetricCard label="Projected spread" value={formatCurrency(firstDealReport.projectedAssignmentFees)} detail="Estimate, evidence-gated" />
      </div>
      <div className="grid-two">
        <Section title="Scoring Lessons">
          <div className="record-list">
            {firstDealReport.scoringLessons.map((lesson) => (
              <RecordCard key={lesson} title={lesson} meta="Advisory only" right={<Pill tone="gold">review</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Next Batch Recommendations">
          <div className="record-list">
            {firstDealReport.nextBatchRecommendations.map((item) => (
              <RecordCard key={item} title={item} meta="Owner review before scoring changes" right={<Pill tone="green">ready</Pill>} />
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
