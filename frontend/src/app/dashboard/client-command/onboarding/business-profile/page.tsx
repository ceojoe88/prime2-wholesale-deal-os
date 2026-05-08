import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { getClientBusinessProfile } from "@/lib/demo-data";

export default function ClientCommandOnboardingBusinessProfilePage() {
  const profile = getClientBusinessProfile();
  return (
    <div className="page">
      <PageHeader eyebrow="CP8 Business Profile" title="Client Business Profile" description="Business identity, goals, market focus, and bottlenecks for the client workspace." />
      <Section title="Business Profile Card">
        <div className="grid-two">
          <RecordCard title={profile?.businessName ?? "Client business"} meta={profile?.clientSafeSummary ?? "Create Business Profile"} right={<Pill tone="green">{profile?.businessType ?? "unknown"}</Pill>} />
          <RecordCard title="Operator" meta={profile?.operatorName ?? "Unassigned"} right={<Pill tone="gold">{profile?.experienceLevel ?? "unknown"}</Pill>} />
          <RecordCard title="Primary market" meta={profile?.primaryMarket ?? "No market"} right={<Pill tone="gold">{profile?.preferredStrategy ?? "unknown"}</Pill>} />
          <RecordCard title="Biggest bottleneck" meta={profile?.currentToolsSummary ?? "No tools summary"} right={<Pill tone="gold">{profile?.biggestBottleneck ?? "unknown"}</Pill>} />
        </div>
      </Section>
    </div>
  );
}
