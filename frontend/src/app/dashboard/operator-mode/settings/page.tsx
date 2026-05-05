import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { activeOperatorMode, operatorHardBoundaryCards, operatorModeSettings } from "@/lib/demo-data";

export default function OperatorSettingsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Operator Mode Settings"
        title="Mode and boundary settings"
        description="Modes are manual, assisted, near-autonomous, and semi-autonomous. Semi-autonomous is not the default unless the owner enables it."
      />

      <div className="metric-grid">
        <MetricCard label="Active mode" value={activeOperatorMode.currentMode} detail={`Default ${activeOperatorMode.defaultMode}`} />
        <MetricCard label="Max autonomy" value={String(activeOperatorMode.maxAutonomyLevel)} detail="Level 5 unavailable" />
        <MetricCard label="Owner enabled" value={activeOperatorMode.ownerEnabled ? "yes" : "no"} detail="Required for semi-autonomous" />
        <MetricCard label="Live gates" value="required" detail="Safety, dry-run, approval, flags, idempotency" />
      </div>

      <Section title="Mode Records">
        <div className="record-list">
          {operatorModeSettings.map((setting) => (
            <RecordCard key={setting.id} title={setting.currentMode} meta={`Default ${setting.defaultMode}; owner enabled ${setting.ownerEnabled ? "yes" : "no"}`} right={<Pill tone={setting.currentMode === "semi_autonomous" ? "gold" : "green"}>{setting.maxAutonomyLevel}</Pill>} />
          ))}
        </div>
      </Section>

      <Section title="Hard Boundaries">
        <div className="grid-three">
          {operatorHardBoundaryCards.map((card) => (
            <RecordCard key={card.label} title={card.label} meta={card.detail} right={<Pill tone={card.value === "off" || card.value === "disabled" ? "red" : "gold"}>{card.value}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
