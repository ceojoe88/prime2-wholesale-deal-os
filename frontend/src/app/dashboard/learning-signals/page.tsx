import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { Section } from "@/components/Section";
import { learningSignals } from "@/lib/demo-data";

export default function LearningSignalsPage() {
  return (
    <div className="page">
      <PageHeader
        eyebrow="Learning Signals"
        title="Prediction versus outcome"
        description="Signals compare predicted values with actual field, buyer, document, and campaign outcomes using deterministic variance explanations."
      />
      <Section title="Signals">
        <table className="data-table">
          <thead>
            <tr>
              <th>Signal</th>
              <th>Predicted</th>
              <th>Actual</th>
              <th>Variance</th>
              <th>Confidence</th>
              <th>Review</th>
            </tr>
          </thead>
          <tbody>
            {learningSignals.map((signal) => (
              <tr key={signal.signalId}>
                <td>{signal.signalType}<div className="record-meta">{signal.explanation}</div></td>
                <td>{signal.predictedValue}</td>
                <td>{signal.actualValue}</td>
                <td>{signal.variance}</td>
                <td><Pill tone={signal.confidence >= 80 ? "green" : "gold"}>{signal.confidence}</Pill></td>
                <td>{signal.ownerReviewStatus}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
    </div>
  );
}

