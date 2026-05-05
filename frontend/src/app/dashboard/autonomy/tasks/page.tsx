import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  autonomousAgentTasks,
  autonomyDraftTasks,
  autonomyOpenTasks,
  autonomyOwnerApprovalTasks
} from "@/lib/demo-data";

export default function AutonomyTasksPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="V12 Autonomous Agent Task Queue"
        title="Internal prep task routing"
        description="Prime 2 can queue analysis, draft, reminder, blocker, and readiness tasks for division agents without live execution."
      />

      <div className="metric-grid">
        <MetricCard label="Tasks" value={String(autonomousAgentTasks.length)} detail="Agent prep queue" />
        <MetricCard label="Open" value={String(autonomyOpenTasks.length)} detail="Awaiting operator review" />
        <MetricCard label="Draft tasks" value={String(autonomyDraftTasks.length)} detail="Draft-only output" />
        <MetricCard label="Owner approvals" value={String(autonomyOwnerApprovalTasks.length)} detail="Owner-gated next step" />
      </div>

      <Section title="Task Queue">
        <table className="data-table">
          <thead>
            <tr>
              <th>Task</th>
              <th>Agent</th>
              <th>Division</th>
              <th>Source</th>
              <th>Priority</th>
              <th>Status</th>
              <th>Owner</th>
            </tr>
          </thead>
          <tbody>
            {autonomousAgentTasks.map((task) => (
              <tr key={task.id}>
                <td>{task.taskType}<div className="record-meta">{task.id}</div></td>
                <td>{task.agentName}</td>
                <td>{task.division}</td>
                <td>{task.sourceRecordType}:{task.sourceRecordId}</td>
                <td><Pill tone={task.priority === "critical" ? "red" : task.priority === "high" ? "gold" : "green"}>{task.priority}</Pill></td>
                <td>{task.status}</td>
                <td><Pill tone={task.ownerApprovalRequired ? "gold" : "green"}>{task.ownerApprovalRequired ? "required" : "not required"}</Pill></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>

      <Section title="Recommendations">
        <div className="record-list">
          {autonomyOpenTasks.slice(0, 6).map((task) => (
            <RecordCard key={task.id} title={task.recommendation} meta={`${task.agentName} / ${task.division}`} right={<Pill tone={task.liveActionAllowed ? "green" : "red"}>{task.liveActionAllowed ? "live" : "draft"}</Pill>} />
          ))}
        </div>
      </Section>
    </div>
  );
}
