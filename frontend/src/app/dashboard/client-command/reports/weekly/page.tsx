import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientWeeklyCommandReports } from "@/lib/demo-data";

export default function ClientCommandReportsWeeklyPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="CP7 Weekly" title="Weekly Reports" description="Client-safe weekly report - no revenue, ROI, or deal outcome is guaranteed." />
      <Section title="Weekly Executive Summary">
        <div className="record-list">
          {clientWeeklyCommandReports.map((report) => (
            <RecordCard key={report.id} title={report.reportTitle} meta={report.executiveSummary} right={<Link href={`/dashboard/client-command/reports/${report.id}`}>View Details</Link>}>
              <div className="tag-row">
                <Pill tone="green">{report.reportStatus}</Pill>
                <Pill tone="gold">No ROI Claim</Pill>
                <Pill tone="gold">No Live Actions Taken</Pill>
              </div>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}
