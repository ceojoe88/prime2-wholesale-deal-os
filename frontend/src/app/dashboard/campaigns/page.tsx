import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  campaignActiveControlled,
  campaignApprovalsNeeded,
  campaignAttemptsBlocked,
  campaignDncExclusions,
  campaignRuleRecords
} from "@/lib/demo-data";

export default function CampaignsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V25 Controlled Campaign Brain"
        title="Campaign planning and governance"
        description="Prime 2 segments audiences, prepares safe sequences, tracks approvals, and audits controlled one-message events without uncontrolled outreach."
      />

      <div className="metric-grid">
        <MetricCard label="Campaigns" value={String(campaignRuleRecords.length)} detail="Draft by default" />
        <MetricCard label="Controlled active" value={String(campaignActiveControlled.length)} detail="Approval-gated" />
        <MetricCard label="Approvals" value={String(campaignApprovalsNeeded.length)} detail="Owner queue" />
        <MetricCard label="DNC exclusions" value={String(campaignDncExclusions.length)} detail="Audience guard" />
      </div>

      <Section title="Campaign Records">
        <div className="record-list">
          {campaignRuleRecords.map((campaign) => (
            <RecordCard
              key={campaign.id}
              title={campaign.name}
              meta={`${campaign.campaignType} / ${campaign.audienceType} / cap ${campaign.maxRecipientsPerDay} per day`}
              right={<Link href={`/dashboard/campaigns/${campaign.campaignId}`}><Pill tone={campaign.status === "active_controlled" ? "green" : campaign.status === "blocked" ? "red" : "gold"}>{campaign.status}</Pill></Link>}
            />
          ))}
        </div>
      </Section>

      <Section title="Work Areas">
        <div className="grid-three">
          <RecordCard title="New Draft" meta="Create planning record and preview only" right={<Link href="/dashboard/campaigns/new">Open</Link>} />
          <RecordCard title="Segments" meta="Preview audience and exclusions" right={<Link href="/dashboard/campaigns/segments">Open</Link>} />
          <RecordCard title="Sequences" meta="Draft-only steps and timing" right={<Link href="/dashboard/campaigns/sequences">Open</Link>} />
          <RecordCard title="Approvals" meta="Owner approvals before activation" right={<Link href="/dashboard/campaigns/approvals">Open</Link>} />
          <RecordCard title="Performance" meta={`${campaignAttemptsBlocked.length} blocked attempts audited`} right={<Link href="/dashboard/campaigns/performance">Open</Link>} />
          <RecordCard title="Live path" meta="Requires V5, V13, V22, flags, idempotency, and audit" right={<Pill tone="red">gated</Pill>} />
        </div>
      </Section>
    </div>
  );
}

