import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";

export default function NewCampaignPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Campaign Draft Intake"
        title="Create controlled campaign plan"
        description="New campaign records start as drafts and require audience preview, approved templates, stop conditions, owner approval, caps, readiness, idempotency, and audit before controlled activation."
      />
      <div className="metric-grid">
        <MetricCard label="Default status" value="draft" detail="No uncontrolled send path" />
        <MetricCard label="Audience preview" value="required" detail="DNC and compliance exclusions" />
        <MetricCard label="Daily cap" value="required" detail="One-recipient events" />
        <MetricCard label="Stop rules" value="required" detail="Reply, DNC, compliance, provider, owner pause" />
      </div>
      <Section title="Required Planning Fields">
        <div className="grid-three">
          <RecordCard title="Audience type" meta="Seller or buyer segment" right={<Pill>required</Pill>} />
          <RecordCard title="Templates" meta="Approved V13/V20 templates only" right={<Pill>required</Pill>} />
          <RecordCard title="Owner approval" meta="Required before controlled activation" right={<Pill tone="gold">pending</Pill>} />
        </div>
      </Section>
    </div>
  );
}

