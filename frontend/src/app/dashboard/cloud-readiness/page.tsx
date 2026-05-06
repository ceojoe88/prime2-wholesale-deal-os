import Link from "next/link";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  cloudBackupReadiness,
  cloudDeploymentProfiles,
  cloudMonitoringSnapshot,
  cloudProductionReady,
  cloudReadinessBlockedReasons,
  failedCloudEnvironmentChecks
} from "@/lib/demo-data";

export default function CloudReadinessPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V29 Production Cloud Readiness"
        title="Private cloud readiness gate"
        description="Prime 2 checks auth, env, CORS, secret posture, backup metadata, worker health, provider readiness, and deployment profile gaps before private hosting."
      />

      <div className="metric-grid">
        <MetricCard label="Production status" value={cloudProductionReady ? "ready" : "blocked"} detail="Fail-closed private hosting gate" />
        <MetricCard label="Env blockers" value={String(failedCloudEnvironmentChecks.length)} detail="Auth, CORS, DB, API base" />
        <MetricCard label="Backup status" value={cloudBackupReadiness.status} detail="Metadata-safe restore plan" />
        <MetricCard label="Monitoring" value={cloudMonitoringSnapshot.readinessStatus} detail="Health, worker, provider, cost cap" />
      </div>

      <Section title="Blocked Reasons">
        <div className="grid-three">
          {cloudReadinessBlockedReasons.map((reason) => (
            <RecordCard key={reason} title={reason} meta="Must clear before production readiness" right={<Pill tone="red">blocked</Pill>} />
          ))}
        </div>
      </Section>

      <div className="grid-two">
        <Section title="Deployment Profiles">
          <div className="record-list">
            {cloudDeploymentProfiles.map((profile) => (
              <RecordCard key={profile.id} title={profile.profileName} meta={profile.blockedReasons.join(", ") || "Ready for local use"} right={<Pill tone={profile.readinessStatus === "ready" ? "green" : "red"}>{profile.readinessStatus}</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Cloud Work Areas">
          <div className="record-list">
            <RecordCard title="Environment" meta="Masked env posture and critical gaps" right={<Link href="/dashboard/cloud-readiness/env">Open</Link>} />
            <RecordCard title="Security" meta="Auth, CORS, secret posture, provider flags" right={<Link href="/dashboard/cloud-readiness/security">Open</Link>} />
            <RecordCard title="Backups" meta="Safe backup manifest and restore checklist" right={<Link href="/dashboard/cloud-readiness/backups">Open</Link>} />
            <RecordCard title="Monitoring" meta="Health, worker heartbeat, provider status" right={<Link href="/dashboard/cloud-readiness/monitoring">Open</Link>} />
            <RecordCard title="Deployment Checklist" meta="Private hosting hardening sequence" right={<Link href="/dashboard/cloud-readiness/deployment-checklist">Open</Link>} />
          </div>
        </Section>
      </div>
    </div>
  );
}
