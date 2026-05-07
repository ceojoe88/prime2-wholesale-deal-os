import { notFound } from "next/navigation";
import { MetricCard } from "@/components/MetricCard";
import { PageHeader } from "@/components/PageHeader";
import { Pill } from "@/components/Pill";
import { RecordCard } from "@/components/RecordCard";
import { Section } from "@/components/Section";
import {
  clientLeadDivisionEvents,
  clientLeadMissingDataItems,
  clientLeadNextBestActions,
  clientLeadProfiles,
  clientLeadScores,
  clientAcquisitionDivisionEvents,
  clientDealEvidenceItems,
  clientFollowUpDrafts,
  clientObjectionResponseDrafts,
  clientOfferScenarios,
  clientSellerQuestions,
  clientUnderwritingDivisionEvents,
  formatCurrency,
  getClientAcquisitionBrief,
  getClientAppointmentReadiness,
  getClientEvidencePacket,
  getClientLead,
  getClientLeadScore,
  getClientOfferReadiness,
  getClientQuestionPlan,
  getClientUnderwritingReview
} from "@/lib/demo-data";

export function generateStaticParams() {
  return clientLeadProfiles.map((lead) => ({ leadId: lead.id }));
}

export default function ClientLeadDetailPage({ params }: { params: { leadId: string } }) {
  const lead = getClientLead(params.leadId);
  const score = getClientLeadScore(params.leadId);
  if (!lead || !score) {
    notFound();
  }
  const missing = clientLeadMissingDataItems.filter((item) => item.leadId === lead.id);
  const actions = clientLeadNextBestActions.filter((item) => item.leadId === lead.id);
  const events = clientLeadDivisionEvents.filter((item) => item.leadId === lead.id);
  const brief = getClientAcquisitionBrief(lead.id);
  const questionPlan = getClientQuestionPlan(lead.id);
  const appointmentReadiness = getClientAppointmentReadiness(lead.id);
  const acquisitionEvents = clientAcquisitionDivisionEvents.filter((item) => item.leadId === lead.id);
  const questions = questionPlan ? clientSellerQuestions.filter((item) => item.questionPlanId === questionPlan.id) : [];
  const objectionDrafts = clientObjectionResponseDrafts.filter((item) => item.leadId === lead.id);
  const followUpDrafts = clientFollowUpDrafts.filter((item) => item.leadId === lead.id);
  const evidencePacket = getClientEvidencePacket(lead.id);
  const evidenceItems = evidencePacket ? clientDealEvidenceItems.filter((item) => item.packetId === evidencePacket.id) : [];
  const underwritingReview = getClientUnderwritingReview(lead.id);
  const offerReadiness = getClientOfferReadiness(lead.id);
  const scenarios = underwritingReview ? clientOfferScenarios.filter((item) => item.underwritingReviewId === underwritingReview.id) : [];
  const underwritingEvents = clientUnderwritingDivisionEvents.filter((item) => item.leadId === lead.id);

  return (
    <div className="page">
      <PageHeader
        eyebrow="Client Lead Detail"
        title={lead.displayName}
        description="Sanitized client lead intelligence with scoring reasons, missing data, next action, confidence, and human-review status."
      />

      <div className="metric-grid">
        <MetricCard label="Priority" value={String(score.finalPriorityScore)} detail={score.recommendedNextAction} />
        <MetricCard label="Probability" value={String(score.dealProbabilityScore)} detail="Deterministic CP2 score" />
        <MetricCard label="Confidence" value={score.confidenceLevel} detail={score.requiresHumanReview ? "Human review required" : "Client-safe queue"} />
        <MetricCard label="Estimated equity" value={formatCurrency(lead.estimatedEquity)} detail={`${lead.estimatedEquityPercent}% signal`} />
      </div>

      <Section title="Lead Intelligence Score">
        <div className="grid-three">
          <RecordCard title="Motivation" meta={score.reasonSummary} right={<Pill tone="gold">{score.motivationScore}</Pill>} />
          <RecordCard title="Urgency" meta="Timeline-based urgency signal" right={<Pill tone="gold">{score.urgencyScore}</Pill>} />
          <RecordCard title="Equity" meta={`${lead.estimatedEquityPercent}% estimated equity`} right={<Pill tone="green">{score.equitySignalScore}</Pill>} />
          <RecordCard title="Distress" meta={lead.distressSignals.join(", ") || "none"} right={<Pill tone="gold">{score.distressSignalScore}</Pill>} />
          <RecordCard title="Contactability" meta={lead.contactChannelsPresent.join(", ") || "missing"} right={<Pill tone="gold">{score.contactabilityScore}</Pill>} />
          <RecordCard title="Missing Data" meta={`${missing.length} checklist items`} right={<Pill tone={missing.length ? "red" : "green"}>{score.missingDataScore}</Pill>} />
        </div>
      </Section>

      <Section title="Missing Data Checklist">
        <div className="record-list">
          {missing.length === 0 ? (
            <RecordCard title="No blocking missing data" meta="This lead has the required CP2 readiness fields." right={<Pill tone="green">clear</Pill>} />
          ) : (
            missing.map((item) => (
              <RecordCard key={item.id} title={item.fieldName} meta={item.reason} right={<Pill tone={item.severity === "high" ? "red" : "gold"}>{item.resolutionStatus}</Pill>} />
            ))
          )}
        </div>
      </Section>

      <div className="grid-two">
        <Section title="Recommended Next Action">
          <div className="record-list">
            {actions.map((action) => (
              <RecordCard key={action.id} title={action.actionLabel} meta={action.reason} right={<Pill tone={action.requiresHumanReview ? "gold" : "green"}>{action.confidenceLevel}</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Division Events">
          <div className="record-list">
            {events.map((event) => (
              <RecordCard key={event.id} title={event.managerStatus} meta={event.eventSummary} right={<Pill tone="green">{event.eventType}</Pill>} />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Acquisition Manager">
        <div className="grid-two">
          <RecordCard
            title="Call Prep Brief"
            meta={brief?.recommendedCallObjective ?? "Generate Brief to prepare seller discovery."}
            right={<Pill tone={brief?.requiresHumanReview ? "gold" : "green"}>{brief?.confidenceLevel ?? "missing"}</Pill>}
          >
            <p>{brief?.clientSafeSummary ?? "Client-safe acquisition prep is available on demand."}</p>
            <div className="tag-row">
              <Pill tone="green">Client-Safe</Pill>
              {brief?.requiresHumanReview ? <Pill tone="gold">Human Review Needed</Pill> : null}
            </div>
          </RecordCard>
          <RecordCard
            title="Appointment Readiness"
            meta={appointmentReadiness?.recommendedNextStep ?? "Review Appointment Readiness before seller appointment planning."}
            right={<Pill tone={appointmentReadiness?.appointmentReady ? "green" : "red"}>{appointmentReadiness?.readinessScore ?? 0}</Pill>}
          >
            <p>{appointmentReadiness?.reasonSummary ?? "Missing appointment review."}</p>
            <div className="tag-row">
              {(appointmentReadiness?.missingRequirements ?? []).map((item) => (
                <Pill key={item} tone="gold">{item}</Pill>
              ))}
            </div>
          </RecordCard>
        </div>
      </Section>

      <div className="grid-two">
        <Section title="Seller Question Plan">
          <div className="record-list">
            <RecordCard title={questionPlan?.planStatus ?? "Generate Question Plan"} meta={questionPlan?.clientSafeSummary ?? "No plan yet."} right={<Pill tone="gold">{questionPlan?.totalQuestions ?? 0}</Pill>} />
            {questions.map((question) => (
              <RecordCard key={question.id} title={question.questionCategory} meta={question.questionText} right={<Pill tone={question.priority === "high" ? "gold" : "green"}>{question.priority}</Pill>}>
                <p>{question.reason}</p>
              </RecordCard>
            ))}
          </div>
        </Section>
        <Section title="Follow-Up Draft Queue">
          <div className="record-list">
            {followUpDrafts.map((draft) => (
              <RecordCard key={draft.id} title={draft.purpose} meta={draft.draftBody} right={<Pill tone="gold">Manual Use Only</Pill>}>
                <p>Manual use only — no message has been sent.</p>
              </RecordCard>
            ))}
            {objectionDrafts.map((draft) => (
              <RecordCard key={draft.id} title={draft.objectionType} meta={draft.suggestedResponse} right={<Pill tone={draft.riskLevel === "high" ? "red" : "gold"}>{draft.riskLevel}</Pill>} />
            ))}
          </div>
        </Section>
      </div>

      <Section title="Underwriting Manager">
        <div className="grid-two">
          <RecordCard
            title="Deal Evidence Packet"
            meta={evidencePacket?.clientSafeSummary ?? "Create Evidence Packet before underwriting review."}
            right={<Pill tone={evidencePacket?.evidenceStatus === "ready_for_underwriting" ? "green" : "red"}>{evidencePacket?.evidenceStatus ?? "not_ready"}</Pill>}
          >
            <p>{evidencePacket?.propertyConditionSummary ?? "Evidence missing."}</p>
            <div className="tag-row">
              <Pill tone="green">Client-Safe</Pill>
              {evidencePacket?.requiresHumanReview ? <Pill tone="gold">Human Review Needed</Pill> : null}
            </div>
          </RecordCard>
          <RecordCard
            title="Offer Readiness Gate"
            meta={offerReadiness?.recommendedNextStep ?? "Check Offer Readiness after evidence and underwriting review."}
            right={<Pill tone={offerReadiness?.canPresentOffer ? "green" : "red"}>{offerReadiness?.readinessStatus ?? "not_ready"}</Pill>}
          >
            <p>Decision support only — no contract or offer has been sent.</p>
            <div className="tag-row">
              {(offerReadiness?.blockReasons ?? []).map((item) => (
                <Pill key={item} tone="red">{item}</Pill>
              ))}
            </div>
          </RecordCard>
        </div>
      </Section>

      <div className="grid-two">
        <Section title="Missing Evidence Checklist">
          <div className="record-list">
            {(evidencePacket?.requiredEvidenceSummary ?? []).length === 0 ? (
              <RecordCard title="No missing evidence" meta="Packet has the required demo/manual evidence for review." right={<Pill tone="green">clear</Pill>} />
            ) : (
              evidencePacket?.requiredEvidenceSummary.map((item) => (
                <RecordCard key={item} title={item} meta="Required before offer readiness can improve." right={<Pill tone="red">missing</Pill>} />
              ))
            )}
            {evidenceItems.map((item) => (
              <RecordCard key={item.id} title={item.itemType} meta={item.itemSummary} right={<Pill tone="green">{item.confidenceLevel}</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="ARV / Repair / MAO">
          <div className="record-list">
            <RecordCard title="ARV" meta="Manual/demo input only" right={<Pill tone={underwritingReview?.arvEstimate ? "green" : "red"}>{underwritingReview?.arvEstimate ? formatCurrency(underwritingReview.arvEstimate) : "missing"}</Pill>} />
            <RecordCard title="Repairs" meta="Manual/demo input only" right={<Pill tone={underwritingReview?.repairEstimate ? "green" : "red"}>{underwritingReview?.repairEstimate ? formatCurrency(underwritingReview.repairEstimate) : "missing"}</Pill>} />
            <RecordCard title="MAO" meta={underwritingReview?.assumptionsSummary ?? "Run Underwriting Review"} right={<Pill tone={underwritingReview?.maxAllowableOffer ? "green" : "red"}>{underwritingReview?.maxAllowableOffer ? formatCurrency(underwritingReview.maxAllowableOffer) : "blocked"}</Pill>} />
          </div>
        </Section>
      </div>

      <Section title="Offer Scenario Cards">
        <div className="grid-three">
          {scenarios.map((scenario) => (
            <RecordCard key={scenario.id} title={scenario.scenarioName} meta={scenario.clientSafeExplanation} right={<Pill tone={scenario.riskLevel === "high" ? "red" : scenario.riskLevel === "medium" ? "gold" : "green"}>{formatCurrency(scenario.offerAmount)}</Pill>}>
              <p>{scenario.assumptions}</p>
            </RecordCard>
          ))}
          {scenarios.length === 0 ? (
            <RecordCard title="Scenario review blocked" meta="ARV and repair estimate are required before offer scenarios are calculated." right={<Pill tone="red">needs data</Pill>} />
          ) : null}
        </div>
      </Section>

      <div className="grid-two">
        <Section title="Acquisition Division Events">
          <div className="record-list">
            {acquisitionEvents.map((event) => (
              <RecordCard key={event.id} title={event.managerName} meta={event.eventSummary} right={<Pill tone="green">{event.eventType}</Pill>} />
            ))}
          </div>
        </Section>
        <Section title="Underwriting Division Events">
          <div className="record-list">
            {underwritingEvents.map((event) => (
              <RecordCard key={event.id} title={event.managerName} meta={event.eventSummary} right={<Pill tone="green">{event.eventType}</Pill>} />
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
}
