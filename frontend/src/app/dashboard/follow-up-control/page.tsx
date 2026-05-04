import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { getLead, sellerDrafts, sellerInteractions, staleSellerFollowUps } from "@/lib/demo-data";

export default function FollowUpControlPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Follow-Up Control"
        title="Draft-only seller follow-up engine"
        description="Follow-up sequences, scripts, texts, emails, objection responses, and offer explanations remain drafts until the owner decides what real-world action to take."
      />
      <div className="metric-grid">
        <MetricCard label="Sequences" value={String(sellerInteractions.length)} detail="Draft-only plans" />
        <MetricCard label="Stale" value={String(staleSellerFollowUps.length)} detail="Needs owner review" />
        <MetricCard label="Live SMS/email/calls" value="0" detail="Blocked in V3" />
        <MetricCard label="Unsafe scripts" value="0" detail="Guarded before use" />
      </div>
      <Section title="Follow-Up Queue">
        <div className="record-list">
          {sellerInteractions.map((interaction) => {
            const lead = getLead(interaction.leadId);
            const drafts = lead ? sellerDrafts(lead, interaction) : undefined;
            return (
              <RecordCard
                key={interaction.id}
                title={lead?.sellerName ?? interaction.leadId}
                meta={`Next date ${interaction.nextFollowUpDate} / ${interaction.nextBestSellerAction}`}
                right={<Pill tone={interaction.followUpUrgency === "hot" ? "red" : "gold"}>{interaction.followUpUrgency}</Pill>}
              >
                <div className="pill-row">
                  {drafts?.followUpSequenceDraft.map((step) => <Pill key={step}>{step}</Pill>)}
                  <Pill tone="green">draft only</Pill>
                  <Link className="pill green" href={`/dashboard/seller-acquisition/${interaction.leadId}`}>open seller</Link>
                </div>
              </RecordCard>
            );
          })}
        </div>
      </Section>
    </div>
  );
}
