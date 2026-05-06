import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { firstDealEvidenceRecords, firstDealExecutionBatch, formatCurrency } from "@/lib/demo-data";

export default function FirstDealEvidencePage() {
  const supported = firstDealEvidenceRecords.filter((record) => record.evidenceSupported);
  return (
    <div className="page">
      <PageHeader
        eyebrow="V31 Assignment-Fee Evidence"
        title="Evidence-backed spread tracker"
        description="Prime 2 ties projected spread, seller price, buyer price, buyer margin, confidence, and proof gaps to source records before any owner-facing claim."
      />
      <div className="metric-grid">
        <MetricCard label="Supported" value={String(supported.length)} detail="Source records present" />
        <MetricCard label="Needs proof" value={String(firstDealEvidenceRecords.length - supported.length)} detail="Missing or weak evidence" />
        <MetricCard label="Target spread" value={formatCurrency(firstDealExecutionBatch.targetAssignmentFee)} detail="Evidence required" />
        <MetricCard label="Client proof" value="off" detail="Internal tracker only" />
      </div>
      <Section title="Evidence Rows">
        <table className="data-table">
          <thead>
            <tr>
              <th>Deal</th>
              <th>Projected Spread</th>
              <th>Buyer Margin</th>
              <th>Confidence</th>
              <th>Source Count</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {firstDealEvidenceRecords.map((record) => (
              <tr key={record.deal.id}>
                <td>{record.deal.id}</td>
                <td>{formatCurrency(record.projectedAssignmentFee)}</td>
                <td>{formatCurrency(record.buyerMargin)}</td>
                <td>{record.confidenceScore}</td>
                <td>{record.evidenceSourceRecords.length}</td>
                <td><Pill tone={record.evidenceSupported ? "green" : "red"}>{record.evidenceSupported ? "supported" : "needs proof"}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}

