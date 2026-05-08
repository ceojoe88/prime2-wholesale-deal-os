import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientActivationBlockers,
  clientCommandPermissions,
  clientCommandSafetyCards,
  clientGoLiveReadinessGates,
  clientWorkspaceReadinessScores,
  clientWorkspaces
} from "@/lib/demo-data";

export default function ClientCommandWorkspacesPage() {
  const readiness = clientWorkspaceReadinessScores[0];
  const gate = clientGoLiveReadinessGates[0];
  const blocker = clientActivationBlockers[0];
  return (
    <div className="page">
      <PageHeader
        eyebrow="CP1 Workspace Foundation"
        title="Client workspaces"
        description="Tenant-safe client command rooms with scoped permissions, sanitized workspace data, and disabled live-provider, billing, and document signing lanes."
      />

      <div className="metric-grid">
        <MetricCard label="Workspaces" value={String(clientWorkspaces.length)} detail="Client-safe tenants" />
        <MetricCard label="Permissions" value={String(clientCommandPermissions.length)} detail="Scoped client command grants" />
        <MetricCard label="Live lanes" value="0" detail="Provider lanes unavailable" />
        <MetricCard label="Admin exposure" value="0" detail="Internal governance hidden" />
      </div>

      <Section title="Activation Readiness Snapshot">
        <div className="metric-grid">
          <MetricCard label="Workspace readiness" value={String(readiness?.readinessScore ?? 0)} detail={readiness?.readinessStatus ?? "not_started"} />
          <MetricCard label="Manual gate" value={gate?.gateStatus ?? "not_ready"} detail={gate?.approvedScope ?? "manual review only"} />
          <MetricCard label="Top blocker" value={blocker?.severity ?? "clear"} detail={blocker?.blockerSummary ?? "No blockers"} />
          <MetricCard label="Billing lanes" value="0" detail="No billing/admin controls in client view" />
        </div>
      </Section>

      <Section title="Workspace Registry">
        <div className="record-list">
          {clientWorkspaces.map((workspace) => (
            <RecordCard
              key={workspace.id}
              title={workspace.workspaceName}
              meta={`${workspace.clientName} | ${workspace.marketFocus.join(", ")}`}
              right={<Pill tone={workspace.workspaceStatus === "active" ? "green" : "gold"}>{workspace.workspaceStatus}</Pill>}
            />
          ))}
        </div>
      </Section>

      <Section title="Safety Locks">
        <div className="grid-three">
          {clientCommandSafetyCards.map((card) => (
            <RecordCard key={card.label} title={card.label} meta={card.detail} right={<Pill tone="red">{card.value}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
