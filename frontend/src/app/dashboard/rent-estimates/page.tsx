import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { formatCurrency, rentEstimateRecords } from "@/lib/demo-data";

export default function RentEstimatesPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Rent Demand"
        title="Rent estimate support"
        description="Rent records support buyer-demand context and hold/rental exit assumptions without inventing numbers."
      />
      <Section title="Rent Estimates">
        <table className="data-table">
          <thead>
            <tr>
              <th>Market</th>
              <th>Type</th>
              <th>Estimate</th>
              <th>Range</th>
              <th>Source</th>
              <th>Confidence</th>
            </tr>
          </thead>
          <tbody>
            {rentEstimateRecords.map((rent) => (
              <tr key={rent.rentId}>
                <td>{rent.marketId}</td>
                <td>{rent.propertyType} {rent.beds}/{rent.baths}</td>
                <td>{formatCurrency(rent.estimatedRent)}</td>
                <td>{formatCurrency(rent.rentRangeLow)} to {formatCurrency(rent.rentRangeHigh)}</td>
                <td>{rent.source}</td>
                <td><Pill tone={rent.confidenceScore >= 70 ? "green" : "gold"}>{rent.confidenceScore}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}

