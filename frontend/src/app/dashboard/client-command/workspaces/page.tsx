import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { clientCommandPermissions, clientCommandSafetyCards, clientWorkspaces } from "@/lib/demo-data";

export default function ClientCommandWorkspacesPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="CP1 Workspace Foundation"
        title="Client workspaces"
        description="Tenant-safe client command rooms with scoped permissions, sanitized workspace data, and disabled live-provider, billing, and e-sign lanes."
      />

      <div className="metric-grid">
        <MetricCard label="Workspaces" value={String(clientWorkspaces.length)} detail="Client-safe tenants" />
        <MetricCard label="Permissions" value={String(clientCommandPermissions.length)} detail="Scoped client command grants" />
        <MetricCard label="Live lanes" value="0" detail="Provider lanes unavailable" />
        <MetricCard label="Admin exposure" value="0" detail="Internal governance hidden" />
      </div>

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
