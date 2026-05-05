import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  buyerSequencePreps,
  buyerSequencesBlocked,
  getBuyer,
  getDeal,
  getLead
} from "@/lib/demo-data";

export default function BuyerSequencesPage() {
  const safeSequences = buyerSequencePreps.filter((sequence) => sequence.safetyStatus !== "blocked");

  return (
    <div className="page">
      <PageHeader
        eyebrow="V14 Smart Buyer Sequence Prep"
        title="Draft-only buyer sequences"
        description="Prepare first notice, detail follow-up, POF request, access coordination, offer-intent follow-up, and non-deceptive deadline reminders without live send or bulk distribution."
      />

      <div className="metric-grid">
        <MetricCard label="Sequence drafts" value={String(buyerSequencePreps.length)} detail="No auto-follow-up execution" />
        <MetricCard label="Safe drafts" value={String(safeSequences.length)} detail="Still owner-reviewed before any send" />
        <MetricCard label="Blocked drafts" value={String(buyerSequencesBlocked.length)} detail="Unsafe language or exposure removed" />
        <MetricCard label="Bulk send" value="off" detail="One buyer at a time only" />
      </div>

      <Section title="Sequence Records">
        <table className="data-table">
          <thead>
            <tr>
              <th>Sequence</th>
              <th>Deal</th>
              <th>Buyer</th>
              <th>Safety</th>
              <th>Blocks</th>
            </tr>
          </thead>
          <tbody>
            {buyerSequencePreps.map((sequence) => {
              const deal = getDeal(sequence.dealId);
              const lead = deal ? getLead(deal.leadId) : undefined;
              const buyer = getBuyer(sequence.buyerId);
              return (
                <tr key={sequence.id}>
                  <td>{sequence.id}<div className="record-meta">draft-only</div></td>
                  <td>{lead?.city}, {lead?.state}<div className="record-meta">{sequence.dealId}</div></td>
                  <td>{buyer?.company ?? sequence.buyerId}</td>
                  <td><Pill tone={sequence.safetyStatus === "blocked" ? "red" : "green"}>{sequence.safetyStatus}</Pill></td>
                  <td>{sequence.blockedReasons.length ? sequence.blockedReasons.join(", ") : "clear"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </Section>

      <div className="grid-two">
        <Section title="Draft Components">
          <div className="record-list">
            {safeSequences.slice(0, 2).map((sequence) => (
              <RecordCard
                key={sequence.id}
                title={`${sequence.id} / ${getBuyer(sequence.buyerId)?.company ?? sequence.buyerId}`}
                meta={sequence.firstBuyerNotice}
                right={<Pill>draft</Pill>}
              >
                <div className="stack">
                  <span>{sequence.pofRequest}</span>
                  <span>{sequence.viewingAccessCoordination}</span>
                  <span>{sequence.offerIntentFollowUp}</span>
                </div>
              </RecordCard>
            ))}
          </div>
        </Section>
        <Section title="Hard Stops">
          <div className="record-list">
            <RecordCard title="Live send" meta="Disabled until V5/V13 gates and owner approval are present." right={<Pill tone="red">off</Pill>} />
            <RecordCard title="Bulk buyer blasts" meta="No campaigns, no all-buyer sends, no uncontrolled acceleration." right={<Pill tone="red">blocked</Pill>} />
            <RecordCard title="Scarcity and competition" meta="No unsupported urgency or fake buyer competition." right={<Pill tone="green">guarded</Pill>} />
          </div>
        </Section>
      </div>
    </div>
  );
}
