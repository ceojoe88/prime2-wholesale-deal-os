import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Prime2IdentityPanel } from "@/components/Prime2IdentityPanel";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { divisions } from "@/lib/demo-data";

export default function CommandHierarchyPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Governance"
        title="Owner, overseer, divisions"
        description="The owner controls every real-world action. Prime 2 recommends, routes, escalates, and blocks unsafe execution."
      />
      <div className="hierarchy">
        <div className="hierarchy-node compact">
          <span className="eyebrow">Owner</span>
          <h3>Human Operator</h3>
          <Pill tone="green">Final approval</Pill>
        </div>
        <div className="hierarchy-node compact">
          <span className="eyebrow">Overseer</span>
          <h3>Prime 2</h3>
          <Pill tone="gold">Recommend only</Pill>
        </div>
        <div className="hierarchy-node compact">
          <span className="eyebrow">Divisions</span>
          <h3>{divisions.length} governed teams</h3>
          <Pill tone="red">Execution blocked</Pill>
        </div>
      </div>
      <Prime2IdentityPanel />
      <Section title="Division Managers">
        <div className="grid-three">
          {divisions.map((division) => (
            <RecordCard key={division.id} title={division.managerName} meta={division.name}>
              <div className="pill-row">
                <Pill>{division.workload} queued</Pill>
                {division.riskFlags.map((flag) => (
                  <Pill key={flag} tone="gold">{flag}</Pill>
                ))}
              </div>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}
