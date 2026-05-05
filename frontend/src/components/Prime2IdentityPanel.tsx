import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";

const prime2Responsibilities = [
  "seller acquisition",
  "buyer disposition",
  "10K+ ranking",
  "buyer margin",
  "seller reasonableness",
  "approval escalation",
  "compliance boundaries",
  "gated live actions"
];

export function Prime2IdentityPanel() {
  return (
    <Section title="Prime 2">
      <RecordCard
        title="Brother system to Vylarion Prime"
        meta="Prime 2 is the private wholesale real estate overseer built to identify, control, and accelerate assignment-fee opportunities while preserving owner approval, compliance boundaries, and deal evidence."
        right={<Pill tone="gold">overseer</Pill>}
      >
        <div className="pill-row">
          {prime2Responsibilities.map((responsibility) => (
            <Pill key={responsibility}>{responsibility}</Pill>
          ))}
        </div>
      </RecordCard>
    </Section>
  );
}
