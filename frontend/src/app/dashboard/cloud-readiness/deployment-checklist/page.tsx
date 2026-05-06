import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";

const checklist = [
  "Configure private owner authentication",
  "Set production DATABASE_URL outside git",
  "Restrict CORS to private frontend origins",
  "Set frontend API base URL",
  "Confirm provider flags remain off",
  "Configure backup target placeholder or private bucket",
  "Verify worker heartbeat and failed-job alerting",
  "Run full validation before hosting",
  "Keep title, contract, and payment workflows external"
];

export default function CloudReadinessDeploymentChecklistPage() {
  return (
    <div className="page">
      <PageHeader eyebrow="Deployment Checklist" title="Private deployment hardening guide" description="Cloud readiness is documentation and validation only; no deployment automation or provider activation occurs from this page." />
      <Section title="Checklist">
        <div className="record-list">
          {checklist.map((item) => (
            <RecordCard key={item} title={item} meta="Owner or deployment operator must verify" right={<Pill tone="gold">required</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
