import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import { documentIssueFlags } from "@/lib/demo-data";

export default function DocumentIssuesPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Document Issue Flags"
        title="Missing fields and risk queue"
        description="Prime 2 flags missing signatures, price mismatches, POF gaps, assignment-language warnings, and unsupported claims for internal review."
      />
      <Section title="Open Issues">
        <div className="record-list">
          {documentIssueFlags.map((issue) => (
            <RecordCard key={issue.id} title={issue.issueType} meta={issue.recommendedNextAction} right={<Pill tone={issue.severity === "high" ? "red" : "gold"}>{issue.severity}</Pill>}>
              <p>{issue.explanation}</p>
            </RecordCard>
          ))}
        </div>
      </Section>
    </div>
  );
}

