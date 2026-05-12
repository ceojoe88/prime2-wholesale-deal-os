import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientPlanAssignments,
  clientPlanLimits,
  clientSeatUsageRecords,
  clientUsageCounters
} from "@/lib/demo-data";

const workspaceId = "client-workspace-003";

export default function ClientCommandPlanUsagePage() {
  const assignment = clientPlanAssignments.find((item) => item.workspaceId === workspaceId);
  const limits = clientPlanLimits.find((item) => item.planCode === assignment?.planCode);
  const usage = clientUsageCounters.find((item) => item.workspaceId === workspaceId);
  const seats = clientSeatUsageRecords.filter((item) => item.workspaceId === workspaceId);

  return (
    <div className="page">
      <PageHeader
        eyebrow="CP9 Usage"
        title="Plan Usage Counters"
        description="Workspace usage counters and seat posture against the assigned client-command plan. This page does not create a live entitlement change."
      />

      <div className="metric-grid">
        <MetricCard label="Users" value={`${usage?.usersCount ?? 0}/${limits?.maxUsers ?? 0}`} detail="Seat-bound usage" />
        <MetricCard label="Leads" value={`${usage?.leadsCount ?? 0}/${limits?.maxLeads ?? 0}`} detail="Lead registry usage" />
        <MetricCard label="Buyers" value={`${usage?.buyersCount ?? 0}/${limits?.maxBuyers ?? 0}`} detail="Buyer registry usage" />
        <MetricCard label="Drafts" value={`${usage?.manualDraftsCount ?? 0}/${limits?.maxManualDrafts ?? 0}`} detail="Manual-only draft usage" />
      </div>

      <Section title="Usage Detail">
        <div className="grid-two">
          <RecordCard title="Weekly Reports" meta="Report usage against the assigned plan" right={<Pill tone="green">{`${usage?.weeklyReportsCount ?? 0}/${limits?.maxWeeklyReports ?? 0}`}</Pill>} />
          <RecordCard title="Readiness Gates" meta="Manual-use gate count visible in the workspace" right={<Pill tone="gold">{String(usage?.complianceGatesCount ?? 0)}</Pill>} />
        </div>
      </Section>

      <Section title="Seat Registry">
        <div className="record-list">
          {seats.map((seat) => (
            <RecordCard key={seat.id} title={seat.seatLabel} meta={seat.roleName} right={<Pill tone={seat.countsAgainstLimit ? "green" : "gold"}>{seat.seatStatus}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
