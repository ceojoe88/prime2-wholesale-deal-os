import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  formatCurrency,
  mobileApprovalQueue,
  mobileCallQueue,
  mobileFieldBriefingCards,
  mobileMoneyActions,
  mobileRiskActions
} from "@/lib/demo-data";

const mobileRoutes = [
  ["/mobile/today", "Today"],
  ["/mobile/calls", "Calls"],
  ["/mobile/approvals", "Approvals"],
  ["/mobile/briefing", "Briefing"],
  ["/mobile/notes", "Notes"],
  ["/mobile/buyers", "Buyers"],
  ["/mobile/documents", "Documents"]
];

export default function MobilePage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V28 Mobile Operator Mode"
        title="Mobile field command"
        description="Prime 2 gives the owner a phone-ready view for field notes, call outcomes, approvals, buyers, and documents while real-world actions stay gated."
      />

      <div className="pill-row">
        {mobileRoutes.map(([href, label]) => (
          <Link key={href} href={href}>
            <Pill>{label}</Pill>
          </Link>
        ))}
      </div>

      <div className="metric-grid">
        {mobileFieldBriefingCards.map((card) => (
          <MetricCard key={card.label} label={card.label} value={card.value} detail={card.detail} />
        ))}
      </div>

      <div className="grid-two">
        <Section title="Top Money Actions">
          <div className="record-list">
            {mobileMoneyActions.map((deal) => (
              <RecordCard key={deal.id} title={deal.id} meta={deal.status} right={<Link href={`/mobile/deals/${deal.id}`}><Pill tone="green">{formatCurrency(deal.projectedAssignmentFee)}</Pill></Link>} />
            ))}
          </div>
        </Section>
        <Section title="Top Risk Actions">
          <div className="record-list">
            {mobileRiskActions.map((deal) => (
              <RecordCard key={deal.id} title={deal.id} meta={`Risk ${deal.riskScore}`} right={<Pill tone="red">review</Pill>} />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Field Queues">
        <div className="grid-three">
          <RecordCard title="Call queue" meta={`${mobileCallQueue.length} leads ready for owner review`} right={<Link href="/mobile/calls">Open</Link>} />
          <RecordCard title="Approval queue" meta={`${mobileApprovalQueue.length} items need owner attention`} right={<Link href="/mobile/approvals">Open</Link>} />
          <RecordCard title="Safety boundary" meta="Mobile captures drafts and notes; provider gates remain upstream" right={<Pill tone="gold">gated</Pill>} />
        </div>
      </Section>
    </div>
  );
}
