import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientWeeklyBottlenecks } from "@/lib/demo-data";

export default function ClientCommandReportsBottlenecksPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP7 Bottlenecks" title="Bottleneck Analysis" description="Client-safe weekly report - no revenue, ROI, or deal outcome is guaranteed." />
      <Section title="Bottleneck Analysis">
        <div className="record-list">
          {clientWeeklyBottlenecks.map((item) => (
            <RecordCard key={item.id} title={item.bottleneckType} meta={item.bottleneckSummary} right={<Pill tone={item.severity === "high" ? "red" : "gold"}>{item.affectedLeadCount}</Pill>}>
              <p>{item.recommendedFix}</p>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}
