import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { complianceRecords } from "@/lib/demo-data";

const confirmations = [
  "contract reviewed by attorney/title company",
  "seller understands role",
  "buyer understands assignment",
  "assignment fee disclosure reviewed",
  "no legal advice provided",
  "no misrepresentation"
];

export default function CompliancePage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Contract & Compliance"
        title="Checklist and risk guard"
        description="The system prepares checklists and warnings only. Contracts, assignments, legal review, and real-world action stay outside automation."
      />
      <div className="grid-two">
        <Section title="Required Confirmations">
          <div className="record-list">
            {confirmations.map((item) => <RecordCard key={item} title={item} right={<Pill tone="gold">required</Pill>} />)}
          </div>
        </Section>
        <Section title="Compliance Risk Examples">
          <div className="record-list">
            {complianceRecords.map((record) => (
              <RecordCard key={record.id} title={record.title} meta={record.dealId} right={<Pill tone="red">blocked</Pill>}>
                <div className="pill-row">
                  {record.riskWarnings.map((warning) => <Pill key={warning} tone="red">{warning}</Pill>)}
                </div>
              </RecordCard>
            ))}
          </div>
        </Section>
      </div>
      <Section title="Blocked Execution">
        <div className="pill-row">
          {["execute contracts", "give legal advice", "misrepresent role", "hide assignment fee", "send buyer blast", "live seller outreach"].map((item) => (
            <Pill key={item} tone="red">{item}</Pill>
          ))}
        </div>
      </Section>
    </div>
  );
}
