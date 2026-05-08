import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { getClientStrategyProfile } from "@/lib/demo-data";

export default function ClientCommandOnboardingStrategyPage() {
  const profile = getClientStrategyProfile();
  return (
    <div className="page">
      <PageHeader eyebrow="CP8 Strategy" title="Strategy Profile" description="Target markets, channels, property types, and operating mode for controlled/manual Prime2 usage." />
      <Section title="Strategy Profile Card">
        <div className="grid-two">
          <RecordCard title={profile?.strategyType ?? "unknown"} meta={profile?.strategySummary ?? "Create Strategy Profile"} right={<Pill tone="green">{profile?.riskTolerance ?? "unknown"}</Pill>} />
          <RecordCard title="Acquisition channels" meta={(profile?.acquisitionChannels ?? []).join(", ") || "None"} right={<Pill tone="gold">{profile?.operatingMode ?? "unknown"}</Pill>} />
          <RecordCard title="Disposition channels" meta={(profile?.dispositionChannels ?? []).join(", ") || "None"} right={<Pill tone="gold">manual only</Pill>} />
          <RecordCard title="Target property types" meta={(profile?.targetPropertyTypes ?? []).join(", ") || "None"} right={<Pill tone="gold">{profile?.assignmentFeeTarget ? `$${profile.assignmentFeeTarget.toLocaleString()}` : "no target"}</Pill>} />
        </div>
      </Section>
    </div>
  );
}
