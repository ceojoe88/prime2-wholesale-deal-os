import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { agentPerformanceByScore } from "@/lib/demo-data";

export default function OptimizationAgentPerformancePage() {
  const top = agentPerformanceByScore[0];
  const average = Math.round(
    agentPerformanceByScore.reduce((total, score) => total + score.overallScore, 0) /
      agentPerformanceByScore.length
  );

  return (
    <div className="page">
      <PageHeader
        eyebrow="Agent Performance"
        title="Division scoring"
        description="Track Lead Intelligence quality, Seller Acquisition conversion, Underwriting accuracy, Buyer Disposition effectiveness, Compliance block rate, Follow-Up performance, and Prime 2 recommendation accuracy."
      />

      <div className="metric-grid">
        <MetricCard label="Scored groups" value={String(agentPerformanceByScore.length)} detail="Division-level explainable scoring" />
        <MetricCard label="Top performer" value={String(top?.overallScore ?? 0)} detail={top?.divisionName ?? "n/a"} />
        <MetricCard label="Average score" value={String(average)} detail="Weighted deterministic performance score" />
        <MetricCard label="Black-box ML" value="off" detail="No opaque model scoring" />
      </div>

      <Section title="Performance Scores">
        <table className="data-table">
          <thead>
            <tr>
              <th>Division</th>
              <th>Group</th>
              <th>Overall</th>
              <th>Quality</th>
              <th>Accuracy</th>
              <th>Compliance Block Rate</th>
            </tr>
          </thead>
          <tbody>
            {agentPerformanceByScore.map((score) => (
              <tr key={score.id}>
                <td>{score.divisionName}<div className="record-meta">{score.explanation}</div></td>
                <td>{score.agentGroup}</td>
                <td><Pill tone={score.overallScore >= 85 ? "green" : "gold"}>{score.overallScore}</Pill></td>
                <td>{score.qualityScore}</td>
                <td>{score.accuracyScore}</td>
                <td>{score.complianceBlockRate}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}
