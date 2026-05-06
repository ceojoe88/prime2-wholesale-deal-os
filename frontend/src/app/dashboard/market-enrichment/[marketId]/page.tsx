import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  buyerActivitySnapshots,
  comparableSaleRecords,
  formatCurrency,
  leadSourceRoiRecords,
  marketProfiles,
  rentEstimateRecords
} from "@/lib/demo-data";

export function generateStaticParams() {
  return marketProfiles.map((market) => ({ marketId: market.marketId }));
}

export default function MarketDetailPage({ params }: { params: { marketId: string } }) {
  const market = marketProfiles.find((item) => item.marketId === params.marketId);
  if (!market) {
    notFound();
  }
  const comps = comparableSaleRecords.filter((comp) => comp.marketId === market.marketId);
  const rents = rentEstimateRecords.filter((rent) => rent.marketId === market.marketId);
  const activity = buyerActivitySnapshots.find((snapshot) => snapshot.marketId === market.marketId);
  const roi = leadSourceRoiRecords.filter((record) => record.marketId === market.marketId);

  return (
    <div className="page">
      <PageHeader
        eyebrow="Market Detail"
        title={`${market.city} ${market.zipCode}`}
        description="Market detail ties heat, ARV confidence, buyer demand, rent support, and lead source quality to source records."
      />

      <div className="metric-grid">
        <MetricCard label="Heat" value={String(market.marketHeatScore)} detail="Demand plus source quality minus friction" />
        <MetricCard label="Confidence" value={String(market.confidenceScore)} detail={`${comps.length} comp records`} />
        <MetricCard label="Median value" value={formatCurrency(market.medianEstimatedValue)} detail={`${market.averageDaysOnMarket} DOM`} />
        <MetricCard label="Buyer confidence" value={String(activity?.demandConfidence ?? 0)} detail={`${activity?.activeBuyerCount ?? 0} active buyers`} />
      </div>

      <div className="grid-two">
        <Section title="Comps">
          <div className="record-list">
            {comps.map((comp) => (
              <RecordCard key={comp.compId} title={comp.addressSummary} meta={`${formatCurrency(comp.salePrice)} / ${comp.distanceMiles} mi / ${comp.saleDate}`} right={<Pill tone={comp.confidenceScore >= 70 ? "green" : "gold"}>{comp.confidenceScore}</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Lead Source Evidence">
          <div className="record-list">
            {roi.map((record) => (
              <RecordCard key={record.id} title={record.sourceName} meta={`${record.evidenceBasis.join(", ")} / ${record.notes}`} right={<Pill tone={record.roiConfidence >= 60 ? "green" : "gold"}>{record.roiConfidence}</Pill>} />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Rent Support">
        <div className="grid-three">
          {rents.map((rent) => (
            <RecordCard key={rent.rentId} title={`${rent.propertyType} ${rent.beds}/${rent.baths}`} meta={`${formatCurrency(rent.rentRangeLow)} to ${formatCurrency(rent.rentRangeHigh)}`} right={<Pill>{rent.confidenceScore}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}

