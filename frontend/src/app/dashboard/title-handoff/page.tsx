import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { formatCurrency, getContractControl, getLead, titleHandoffPackets } from "@/lib/demo-data";

export default function TitleHandoffPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Title Handoff Prep"
        title="Draft-only title packet queue"
        description="Title handoff packets collect placeholders and review reminders without submitting anything to a title company."
      />
      <div className="metric-grid">
        <MetricCard label="Packets" value={String(titleHandoffPackets.length)} detail="Draft records" />
        <MetricCard label="Submitted" value="0" detail="Submission blocked" />
        <MetricCard label="Ready drafts" value={String(titleHandoffPackets.filter((packet) => packet.packetStatus === "draft_ready").length)} detail="Owner review still required" />
        <MetricCard label="Review reminders" value={String(titleHandoffPackets.length)} detail="Attorney/title checks" />
      </div>
      <Section title="Title Handoff Packets">
        <table className="data-table">
          <thead>
            <tr>
              <th>Packet</th>
              <th>Seller Opportunity</th>
              <th>Agreed Price</th>
              <th>Assignment</th>
              <th>Status</th>
              <th>Submission</th>
            </tr>
          </thead>
          <tbody>
            {titleHandoffPackets.map((packet) => {
              const contract = getContractControl(packet.contractControlId);
              const lead = contract ? getLead(contract.leadId) : undefined;
              return (
                <tr key={packet.id}>
                  <td><Link href={`/dashboard/title-handoff/${packet.id}`}>{packet.id}</Link><div className="record-meta">{packet.contractControlId}</div></td>
                  <td>{lead?.sellerName}<div className="record-meta">{packet.propertyDetails.city}, {packet.propertyDetails.state}</div></td>
                  <td className="money">{formatCurrency(packet.agreedPrice)}</td>
                  <td>{packet.assignmentStatus}</td>
                  <td><Pill tone={packet.packetStatus === "draft_ready" ? "green" : "red"}>{packet.packetStatus}</Pill></td>
                  <td><Pill tone="red">blocked</Pill></td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
