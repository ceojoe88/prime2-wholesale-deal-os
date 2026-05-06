import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { comparableSaleRecords, formatCurrency } from "@/lib/demo-data";

export default function CompsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Comparable Sales"
        title="Comp evidence records"
        description="Comp confidence uses source, distance, recency, property fit, and adjustment notes so ARV confidence stays evidence-based."
      />
      <Section title="Comparable Sales">
        <table className="data-table">
          <thead>
            <tr>
              <th>Comp</th>
              <th>Market</th>
              <th>Type</th>
              <th>Sale Price</th>
              <th>Date</th>
              <th>Distance</th>
              <th>Confidence</th>
            </tr>
          </thead>
          <tbody>
            {comparableSaleRecords.map((comp) => (
              <tr key={comp.compId}>
                <td><Link href={`/dashboard/comps/${comp.compId}`}>{comp.addressSummary}</Link><div className="record-meta">{comp.adjustmentNotes}</div></td>
                <td>{comp.marketId}</td>
                <td>{comp.propertyType}</td>
                <td>{formatCurrency(comp.salePrice)}</td>
                <td>{comp.saleDate}</td>
                <td>{comp.distanceMiles} mi</td>
                <td><Pill tone={comp.confidenceScore >= 70 ? "green" : "gold"}>{comp.confidenceScore}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}

