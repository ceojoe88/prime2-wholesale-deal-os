import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";

const csvFields = [
  "owner_name",
  "owner_phone",
  "owner_email",
  "property_address",
  "property_city",
  "property_state",
  "property_zip",
  "mailing_address",
  "lead_source",
  "lead_type",
  "property_type",
  "beds",
  "baths",
  "sqft",
  "year_built",
  "estimated_value",
  "estimated_equity",
  "mortgage_balance",
  "tax_delinquent_flag",
  "vacant_flag",
  "absentee_owner_flag",
  "probate_flag",
  "inherited_flag",
  "code_violation_flag",
  "pre_foreclosure_flag",
  "tired_landlord_flag",
  "notes"
];

export default function LeadImportPreviewPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="CSV Preview"
        title="Import preview template"
        description="Prime 2 validates real lead CSV data before any row can be committed. Property address is critical, and bad rows stay visible with reasons."
      />

      <Section title="Supported Fields">
        <div className="grid-three">
          {csvFields.map((field) => (
            <RecordCard key={field} title={field} right={<Pill>{field.includes("property_") || field === "owner_name" || field === "lead_source" ? "critical" : "field"}</Pill>} />
          ))}
        </div>
      </Section>

      <Section title="Preview Rules">
        <div className="grid-three">
          <RecordCard title="Required preview" meta="Rows are normalized, deduped, and QA-scored before commit" right={<Pill tone="green">on</Pill>} />
          <RecordCard title="Approved rows only" meta="Blocked, duplicate, and invalid critical rows cannot commit" right={<Pill tone="green">gated</Pill>} />
          <RecordCard title="No contact" meta="Imported leads never trigger live outreach" right={<Pill tone="green">blocked</Pill>} />
        </div>
      </Section>
    </div>
  );
}
