import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { campaignApprovalsNeeded, campaignRuleRecords } from "@/lib/demo-data";

export default function CampaignApprovalsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Campaign Approvals"
        title="Owner approval queue"
        description="Activation requires owner approval, approved templates, audience approval, DNC and compliance guards, caps, stop conditions, provider readiness, and idempotency."
      />
      <Section title="Approval Queue">
        <div className="record-list">
          {campaignApprovalsNeeded.map((campaign) => (
            <RecordCard key={campaign.id} title={campaign.name} meta={campaign.blockedReasons.join(", ") || "Owner review needed"} right={<Pill tone="gold">{campaign.ownerApprovalStatus}</Pill>} />
          ))}
          {campaignRuleRecords.length === campaignApprovalsNeeded.length ? null : (
            <RecordCard title="Approved controlled records" meta={`${campaignRuleRecords.length - campaignApprovalsNeeded.length} campaign record already approved`} right={<Pill tone="green">tracked</Pill>} />
          )}
        </div>
      </Section>
    </div>
  );
}

