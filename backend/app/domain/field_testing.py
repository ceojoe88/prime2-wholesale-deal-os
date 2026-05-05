from __future__ import annotations

import csv
import re
from datetime import UTC, datetime
from io import StringIO
from typing import Any

from sqlalchemy.orm import Session

from app.domain.imports import LEAD_SOURCE_CATEGORIES
from app.domain.scoring import calculate_lead_opportunity, clamp_score
from app.models import (
    AutonomousAgentTask,
    FieldCallOutcome,
    Lead,
    LeadImportBatch,
    LeadImportRow,
    LeadQualityReview,
    OperatorExceptionRecord,
    PredictionFeedbackRecord,
    ScoringAdjustmentSuggestion,
)
from app.serializers import model_to_dict


V19_CSV_FIELDS = [
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
    "notes",
]

CRITICAL_IMPORT_FIELDS = {
    "owner_name",
    "property_address",
    "property_city",
    "property_state",
    "property_zip",
    "lead_source",
}

DISTRESS_FLAG_FIELDS = [
    "tax_delinquent_flag",
    "vacant_flag",
    "absentee_owner_flag",
    "probate_flag",
    "inherited_flag",
    "code_violation_flag",
    "pre_foreclosure_flag",
    "tired_landlord_flag",
]

CALL_RESULTS = {
    "no_answer",
    "wrong_number",
    "disconnected",
    "left_voicemail",
    "spoke_to_owner",
    "spoke_to_relative",
    "not_interested",
    "call_back_later",
    "motivated",
    "offer_requested",
    "appointment_set",
    "do_not_contact",
}

UNSAFE_FIELD_TESTING_TERMS = {
    "guaranteed profit": "guaranteed_profit_language",
    "guarantee profit": "guaranteed_profit_language",
    "legal advice": "legal_advice_language",
    "must sign": "pressure_language",
    "last chance": "pressure_language",
    "send all": "bulk_outreach_language",
    "blast": "bulk_outreach_language",
    "auto call": "live_call_automation_language",
    "execute contract": "contract_execution_language",
    "submit to title": "title_submission_language",
    "publish automatically": "automatic_portal_publish_language",
}


def _slug(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return cleaned[:40] or "record"


def normalize_phone(value: str | None) -> str:
    digits = re.sub(r"\D", "", value or "")
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    return digits


def normalize_email(value: str | None) -> str:
    email = (value or "").strip().lower()
    return email if "@" in email and "." in email.split("@")[-1] else ""


def normalize_bool(value: object) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y", "x"}


def _int_or_none(value: object) -> int | None:
    text = str(value or "").strip().replace("$", "").replace(",", "")
    if not text:
        return None
    try:
        return int(float(text))
    except ValueError:
        return None


def _float_or_none(value: object) -> float | None:
    text = str(value or "").strip().replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _valid_zip(value: str) -> bool:
    return bool(re.fullmatch(r"\d{5}(?:-\d{4})?", value.strip()))


def _duplicate_key(address: str, city: str, state: str, zip_code: str, phone: str) -> str:
    parts = [address, city, state, zip_code, phone]
    return "|".join(re.sub(r"\s+", " ", part.lower().strip()) for part in parts)


def _existing_property_keys(session: Session) -> set[str]:
    return {
        _duplicate_key(lead.address, lead.city, lead.state, lead.zip_code, "")
        for lead in session.query(Lead).all()
    }


def sanitize_field_testing_text(content: str) -> dict[str, object]:
    lowered = content.lower()
    flags = sorted(
        {flag for term, flag in UNSAFE_FIELD_TESTING_TERMS.items() if term in lowered}
    )
    return {
        "allowed": not flags,
        "risk_flags": flags,
        "blocked_reasons": flags,
        "live_outreach_allowed": False,
        "bulk_outreach_allowed": False,
        "contract_execution_allowed": False,
        "title_submission_allowed": False,
        "legal_advice_allowed": False,
    }


def normalize_import_row(raw: dict[str, Any]) -> dict[str, Any]:
    normalized = {field: str(raw.get(field, "") or "").strip() for field in V19_CSV_FIELDS}
    normalized["owner_phone"] = normalize_phone(normalized["owner_phone"])
    normalized["owner_email"] = normalize_email(normalized["owner_email"])
    normalized["property_state"] = normalized["property_state"].upper()
    normalized["lead_source"] = normalized["lead_source"].lower()
    normalized["lead_type"] = normalized["lead_type"].lower()
    normalized["property_type"] = normalized["property_type"] or "single_family"
    for field in ["beds", "baths"]:
        normalized[field] = _float_or_none(normalized[field])
    for field in ["sqft", "year_built", "estimated_value", "estimated_equity", "mortgage_balance"]:
        normalized[field] = _int_or_none(normalized[field])
    for field in DISTRESS_FLAG_FIELDS:
        normalized[field] = normalize_bool(raw.get(field))
    return normalized


def qa_from_row(row: LeadImportRow) -> LeadQualityReview:
    checks = {
        "missing_phone": not bool(row.owner_phone),
        "missing_owner_name": not bool(row.owner_name),
        "missing_property_address": not bool(row.property_address),
        "invalid_zip": not _valid_zip(row.property_zip),
        "low_equity": (row.estimated_equity or 0) < 25_000,
        "duplicate_property": "duplicate_property" in row.blocked_reasons
        or "duplicate_property_owner_phone" in row.blocked_reasons,
        "conflicting_distress_flags": row.probate_flag and row.tired_landlord_flag,
        "weak_lead_type": row.lead_type in {"", "unknown", "general"},
        "missing_valuation_data": row.estimated_value is None,
        "missing_contactability_data": not bool(row.owner_phone or row.owner_email),
        "stale_source_notes": "stale" in row.notes.lower(),
    }
    data_quality = 100
    data_quality -= 20 if checks["missing_property_address"] else 0
    data_quality -= 12 if checks["missing_owner_name"] else 0
    data_quality -= 10 if checks["invalid_zip"] else 0
    data_quality -= 10 if checks["missing_valuation_data"] else 0
    data_quality -= 8 if checks["weak_lead_type"] else 0
    data_quality -= 15 if checks["duplicate_property"] else 0
    data_quality -= 6 if checks["stale_source_notes"] else 0

    contactability = 85
    contactability -= 45 if checks["missing_phone"] else 0
    contactability -= 15 if not row.owner_email else 0
    contactability -= 10 if row.row_status == "blocked" else 0

    distress_flags = sum(bool(getattr(row, field)) for field in DISTRESS_FLAG_FIELDS)
    distress_confidence = clamp_score(30 + distress_flags * 10)
    equity_confidence = 80 if (row.estimated_equity or 0) >= 50_000 else 45 if row.estimated_equity else 25
    import_confidence = clamp_score(
        data_quality * 0.40
        + contactability * 0.25
        + distress_confidence * 0.20
        + equity_confidence * 0.15
    )
    if row.row_status == "blocked":
        action = "duplicate_review" if checks["duplicate_property"] else "research_more"
    elif import_confidence >= 78 and contactability >= 55:
        action = "call_priority"
    elif import_confidence >= 68:
        action = "underwrite_now"
    elif checks["duplicate_property"]:
        action = "duplicate_review"
    elif import_confidence < 45:
        action = "skip_for_now"
    else:
        action = "research_more"

    return LeadQualityReview(
        id=f"qa-{row.id}",
        lead_id=row.committed_lead_id,
        import_row_id=row.id,
        batch_id=row.batch_id,
        checks=checks,
        data_quality_score=clamp_score(data_quality),
        contactability_score=clamp_score(contactability),
        distress_signal_confidence=distress_confidence,
        equity_confidence=clamp_score(equity_confidence),
        import_confidence=import_confidence,
        recommended_next_action=action,
        blocked_reasons=row.blocked_reasons,
        reviewed_by="Prime 2",
    )


def sync_batch_counts(batch: LeadImportBatch) -> None:
    rows = list(batch.rows)
    batch.row_count = len(rows)
    batch.approved_row_count = len([row for row in rows if row.row_status == "approved"])
    batch.blocked_row_count = len([row for row in rows if row.row_status == "blocked"])
    batch.duplicate_row_count = len(
        [
            row
            for row in rows
            if "duplicate_property" in row.blocked_reasons
            or "duplicate_property_owner_phone" in row.blocked_reasons
        ]
    )
    batch.committed_row_count = len([row for row in rows if row.row_status == "committed"])
    batch.created_leads_count = len([row for row in rows if row.committed_lead_id])
    if batch.committed_row_count:
        batch.status = "committed"
    elif batch.blocked_row_count and not batch.approved_row_count:
        batch.status = "blocked_preview"
    else:
        batch.status = "preview_ready"


def preview_real_lead_csv(
    session: Session,
    csv_text: str,
    *,
    batch_name: str = "Real lead CSV preview",
    source_filename: str = "uploaded-leads.csv",
) -> LeadImportBatch:
    reader = csv.DictReader(StringIO(csv_text))
    fieldnames = set(reader.fieldnames or [])
    missing_columns = sorted(CRITICAL_IMPORT_FIELDS - fieldnames)
    batch_number = session.query(LeadImportBatch).count() + 1
    batch = LeadImportBatch(
        id=f"lead-import-{batch_number:03d}",
        batch_name=batch_name,
        source_filename=source_filename,
        imported_by="Owner",
        safety_notes=[
            "Preview only; imported leads cannot trigger live outreach.",
            "Approved rows require explicit commit and remain operator-controlled.",
        ],
    )
    session.add(batch)
    session.flush()

    seen_keys: set[str] = set()
    existing_keys = _existing_property_keys(session)
    rows = list(reader)
    if not rows and missing_columns:
        rows = [{}]
    for index, raw in enumerate(rows, start=1):
        normalized = normalize_import_row(raw)
        phone = str(normalized["owner_phone"] or "")
        address = str(normalized["property_address"] or "")
        city = str(normalized["property_city"] or "")
        state = str(normalized["property_state"] or "")
        zip_code = str(normalized["property_zip"] or "")
        key = _duplicate_key(address, city, state, zip_code, phone)
        property_key = _duplicate_key(address, city, state, zip_code, "")
        blocked: list[str] = []
        low_confidence: list[str] = []

        for column in missing_columns:
            blocked.append(f"missing_required_column:{column}")
        for column in CRITICAL_IMPORT_FIELDS:
            if not normalized.get(column):
                reason = f"missing_required_field:{column}"
                if column == "property_address":
                    reason = "missing_property_address"
                blocked.append(reason)
        if zip_code and not _valid_zip(zip_code):
            blocked.append("invalid_zip")
        if not phone:
            low_confidence.append("missing_phone")
        if not normalized.get("owner_email"):
            low_confidence.append("missing_email")
        if not normalized.get("estimated_value"):
            low_confidence.append("missing_valuation_data")
        if (normalized.get("estimated_equity") or 0) < 25_000:
            low_confidence.append("low_equity")
        if key in seen_keys and phone:
            blocked.append("duplicate_property_owner_phone")
        if property_key in existing_keys:
            blocked.append("duplicate_property")
        seen_keys.add(key)

        data_confidence = 88 - len(low_confidence) * 10 - len(blocked) * 18
        row = LeadImportRow(
            id=f"{batch.id}-row-{index:03d}",
            batch_id=batch.id,
            row_number=index,
            raw_payload={field: raw.get(field, "") for field in (reader.fieldnames or V19_CSV_FIELDS)},
            normalized_payload=normalized,
            owner_name=str(normalized["owner_name"] or ""),
            owner_phone=phone,
            owner_email=str(normalized["owner_email"] or ""),
            property_address=address,
            property_city=city,
            property_state=state,
            property_zip=zip_code,
            mailing_address=str(normalized["mailing_address"] or ""),
            lead_source=str(normalized["lead_source"] or ""),
            lead_type=str(normalized["lead_type"] or ""),
            property_type=str(normalized["property_type"] or "single_family"),
            beds=normalized["beds"],
            baths=normalized["baths"],
            sqft=normalized["sqft"],
            year_built=normalized["year_built"],
            estimated_value=normalized["estimated_value"],
            estimated_equity=normalized["estimated_equity"],
            mortgage_balance=normalized["mortgage_balance"],
            tax_delinquent_flag=bool(normalized["tax_delinquent_flag"]),
            vacant_flag=bool(normalized["vacant_flag"]),
            absentee_owner_flag=bool(normalized["absentee_owner_flag"]),
            probate_flag=bool(normalized["probate_flag"]),
            inherited_flag=bool(normalized["inherited_flag"]),
            code_violation_flag=bool(normalized["code_violation_flag"]),
            pre_foreclosure_flag=bool(normalized["pre_foreclosure_flag"]),
            tired_landlord_flag=bool(normalized["tired_landlord_flag"]),
            notes=str(normalized["notes"] or ""),
            row_status="blocked" if blocked else "approved",
            approved_for_commit=not blocked,
            blocked_reasons=sorted(set(blocked)),
            low_confidence_flags=sorted(set(low_confidence)),
            duplicate_key=key,
            data_confidence=clamp_score(data_confidence),
        )
        session.add(row)
        session.flush()
        session.add(qa_from_row(row))
    session.flush()
    sync_batch_counts(batch)
    session.commit()
    return batch


def lead_from_import_row(row: LeadImportRow) -> Lead:
    distress = sum(bool(getattr(row, field)) for field in DISTRESS_FLAG_FIELDS)
    motivation = clamp_score(45 + distress * 7)
    equity = clamp_score(min(100, ((row.estimated_equity or 0) / 100_000) * 100))
    contactability = clamp_score(90 if row.owner_phone else 45 if row.owner_email else 20)
    data_confidence = row.data_confidence
    market_demand = 68 if row.property_zip else 45
    opportunity = calculate_lead_opportunity(
        {
            "motivation": motivation,
            "distress_signals": clamp_score(35 + distress * 10),
            "equity": equity,
            "urgency": 55 if row.pre_foreclosure_flag or row.tax_delinquent_flag else 40,
            "contactability": contactability,
            "seller_temperature": 35,
            "data_confidence": data_confidence,
            "market_demand": market_demand,
        }
    )
    source = row.lead_source if row.lead_source in LEAD_SOURCE_CATEGORIES else "county records"
    lead_id = f"real-lead-{row.batch_id[-3:]}-{row.row_number:03d}"
    return Lead(
        id=lead_id,
        seller_name=row.owner_name or "Owner name pending",
        address=row.property_address,
        city=row.property_city,
        state=row.property_state,
        zip_code=row.property_zip,
        property_type=row.property_type or "single_family",
        source_category=source,
        stage="new_lead",
        estimated_equity=row.estimated_equity or 0,
        motivation_score=motivation,
        distress_score=clamp_score(35 + distress * 10),
        equity_score=equity,
        urgency_score=55 if row.pre_foreclosure_flag or row.tax_delinquent_flag else 40,
        contactability_score=contactability,
        seller_temperature=35,
        data_confidence=data_confidence,
        market_demand=market_demand,
        opportunity_score=opportunity,
        compliance_risk=10 if row.probate_flag else 4,
        notes=[
            f"Imported from V19 batch {row.batch_id}.",
            "No live outreach or portal publishing was triggered by import.",
            row.notes,
        ],
        next_best_action="Prime 2 QA review before any owner-approved field action.",
    )


def commit_approved_import_rows(session: Session, batch: LeadImportBatch) -> dict[str, object]:
    batch.commit_requested = True
    committed: list[LeadImportRow] = []
    skipped: list[dict[str, object]] = []
    for row in batch.rows:
        if row.row_status == "committed":
            skipped.append({"row_id": row.id, "reason": "already_committed"})
            continue
        if row.row_status != "approved" or not row.approved_for_commit:
            skipped.append({"row_id": row.id, "reason": "row_not_approved"})
            continue
        if row.blocked_reasons:
            skipped.append({"row_id": row.id, "reason": "blocked_row"})
            continue
        lead = lead_from_import_row(row)
        if session.get(Lead, lead.id):
            skipped.append({"row_id": row.id, "reason": "lead_id_already_exists"})
            continue
        session.add(lead)
        session.flush()
        row.row_status = "committed"
        row.approved_for_commit = False
        row.committed_lead_id = lead.id
        row.committed_at = datetime.now(UTC)
        committed.append(row)
        review = session.get(LeadQualityReview, f"qa-{row.id}")
        if review:
            review.lead_id = lead.id
            sync_lead_quality_review(review)
    batch.committed_at = datetime.now(UTC)
    sync_batch_counts(batch)
    session.commit()
    return {
        "batch": model_to_dict(batch),
        "committed_rows": [model_to_dict(row) for row in committed],
        "skipped_rows": skipped,
        "live_outreach_allowed": False,
        "bulk_outreach_allowed": False,
        "auto_portal_publish_allowed": False,
    }


def sync_lead_quality_review(review: LeadQualityReview) -> LeadQualityReview:
    blocked = list(review.blocked_reasons)
    if review.data_quality_score < 45 and "low_data_quality" not in blocked:
        blocked.append("low_data_quality")
    if review.contactability_score < 35 and "weak_contactability" not in blocked:
        blocked.append("weak_contactability")
    if review.import_confidence >= 78 and review.contactability_score >= 55 and not blocked:
        review.recommended_next_action = "call_priority"
    elif review.import_confidence >= 68 and not blocked:
        review.recommended_next_action = "underwrite_now"
    elif any("duplicate" in reason for reason in blocked):
        review.recommended_next_action = "duplicate_review"
    elif review.import_confidence < 45:
        review.recommended_next_action = "skip_for_now"
    else:
        review.recommended_next_action = "research_more"
    review.blocked_reasons = sorted(set(blocked))
    return review


def outreach_eligibility_for_lead(session: Session, lead_id: str) -> dict[str, object]:
    outcomes = (
        session.query(FieldCallOutcome)
        .filter(FieldCallOutcome.lead_id == lead_id)
        .order_by(FieldCallOutcome.call_datetime.desc())
        .all()
    )
    blocked = any(outcome.do_not_contact for outcome in outcomes)
    return {
        "lead_id": lead_id,
        "eligible": not blocked,
        "blocked_reasons": ["do_not_contact_recorded"] if blocked else [],
        "live_outreach_allowed": False,
        "owner_approval_required": True,
    }


def apply_call_outcome(session: Session, outcome: FieldCallOutcome) -> FieldCallOutcome:
    lead = outcome.lead
    result = outcome.contact_result
    if result == "do_not_contact":
        outcome.do_not_contact = True
        outcome.outreach_eligibility_status = "blocked_do_not_contact"
        lead.next_best_action = "Do not contact; retain record for compliance and owner review."
        lead.contactability_score = 0
        lead.stage = "dead"
    elif result in {"wrong_number", "disconnected"}:
        outcome.outreach_eligibility_status = "research_contact_info"
        lead.contactability_score = 15 if result == "disconnected" else 25
        lead.next_best_action = "Research contact data before any future owner-approved outreach."
    elif result in {"motivated", "offer_requested", "appointment_set"}:
        outcome.outreach_eligibility_status = "owner_review_required"
        lead.motivation_score = max(lead.motivation_score, 82)
        lead.seller_temperature = max(lead.seller_temperature, outcome.seller_temperature or 76)
        lead.stage = "offer_needed" if result == "offer_requested" else "contacted"
        lead.next_best_action = "Escalate to seller acquisition for draft-only next step review."
        outcome.escalation_created = True
        outcome.internal_task_created = True
        create_field_escalation_and_task(session, outcome)
    elif result == "not_interested":
        outcome.outreach_eligibility_status = "low_priority"
        lead.motivation_score = min(lead.motivation_score, 25)
        lead.next_best_action = "Do not pursue unless seller re-engages or owner reopens."
    else:
        outcome.outreach_eligibility_status = "eligible_owner_review"
    outcome.contactability_adjustment = lead.contactability_score
    outcome.motivation_adjustment = lead.motivation_score
    outcome.live_call_recorded = False
    outcome.live_outreach_allowed = False
    return outcome


def create_field_escalation_and_task(session: Session, outcome: FieldCallOutcome) -> None:
    escalation_id = f"field-escalation-{outcome.id}"
    if not session.get(OperatorExceptionRecord, escalation_id):
        session.add(
            OperatorExceptionRecord(
                id=escalation_id,
                exception_type="field_testing_seller_escalation",
                severity="high",
                source_record_type="call_outcome",
                source_record_id=outcome.id,
                reason="Seller field call outcome indicates motivation, offer request, or appointment readiness.",
                recommended_action="Review seller acquisition queue and prepare draft-only next step.",
                owner_action_required=True,
                status="open",
            )
        )
    task_id = f"field-task-{outcome.id}"
    if not session.get(AutonomousAgentTask, task_id):
        session.add(
            AutonomousAgentTask(
                id=task_id,
                agent_name="Seller Temperature Agent",
                division="Seller Acquisition Division",
                task_type="field_call_follow_up_review",
                source_record_type="call_outcome",
                source_record_id=outcome.id,
                priority="high",
                status="queued",
                recommendation="Prepare owner-reviewed follow-up draft; no live call, SMS, or email.",
                idempotency_key=f"{outcome.id}:field-task",
                owner_approval_required=True,
                draft_only=True,
                live_action_allowed=False,
            )
        )


def prediction_accuracy(source_prediction_type: str, source_prediction_value: str, actual_result: str) -> tuple[float, str, str, str]:
    predicted = source_prediction_value.lower()
    actual = actual_result.lower()
    if source_prediction_type == "predicted_motivation":
        if ("high" in predicted or "motivated" in predicted) and actual in {"motivated", "offer_requested", "appointment_set"}:
            return 92, "prediction_matched", "maintain motivation weighting", "High motivation prediction matched seller outcome."
        if ("high" in predicted or "motivated" in predicted) and actual in {"not_interested", "wrong_number", "disconnected"}:
            return 35, "prediction_overstated_motivation", "reduce motivation weight when contactability or distress evidence is weak", "Prediction missed because seller response did not support high motivation."
    if source_prediction_type == "predicted_contactability":
        if ("high" in predicted or "reachable" in predicted) and actual in {"spoke_to_owner", "motivated", "offer_requested", "appointment_set"}:
            return 90, "prediction_matched", "maintain contactability weighting", "Contactability prediction matched actual conversation."
        if ("high" in predicted or "reachable" in predicted) and actual in {"wrong_number", "disconnected", "no_answer"}:
            return 40, "contactability_overstated", "reduce contactability and phone confidence unless recent verification exists", "Actual call outcome showed weaker contactability than predicted."
    if "10k" in source_prediction_type or "opportunity" in source_prediction_type:
        if "verified" in actual or "underwriting supports" in actual:
            return 86, "profit_prediction_supported", "keep evidence-backed 10K+ opportunity weighting", "Updated evidence supports the original 10K+ opportunity prediction."
        return 48, "profit_prediction_needs_evidence", "require underwriting and buyer demand before 10K+ confidence", "Updated field evidence did not yet support the prediction."
    return 70, "needs_more_samples", "collect more field outcomes before changing weights", "Prediction can be evaluated but needs more comparable outcomes."


def sync_prediction_feedback(feedback: PredictionFeedbackRecord) -> PredictionFeedbackRecord:
    accuracy, variance, adjustment, explanation = prediction_accuracy(
        feedback.source_prediction_type,
        feedback.source_prediction_value,
        feedback.actual_result,
    )
    feedback.accuracy_score = accuracy
    feedback.variance_reason = variance
    feedback.recommended_scoring_adjustment = adjustment
    feedback.adjustment_explanation = explanation
    if feedback.call_outcome_id and feedback.call_outcome_id not in feedback.source_record_ids:
        feedback.source_record_ids = [*feedback.source_record_ids, feedback.call_outcome_id]
    return feedback


def scoring_adjustment_from_feedback(feedback: PredictionFeedbackRecord) -> ScoringAdjustmentSuggestion:
    if "contactability" in feedback.recommended_scoring_adjustment:
        group = "contactability"
        current = 0.10
        delta = -0.02 if feedback.accuracy_score < 60 else 0.0
    elif "motivation" in feedback.recommended_scoring_adjustment:
        group = "motivation"
        current = 0.18
        delta = -0.02 if feedback.accuracy_score < 60 else 0.0
    elif "10K" in feedback.source_prediction_type or "opportunity" in feedback.source_prediction_type:
        group = "opportunity_confidence"
        current = 0.16
        delta = -0.01 if feedback.accuracy_score < 60 else 0.01
    else:
        group = "field_sample_size"
        current = 0.08
        delta = 0.0
    return ScoringAdjustmentSuggestion(
        id=f"adjustment-{feedback.id}",
        feedback_id=feedback.id,
        weight_group=group,
        current_weight=current,
        recommended_weight=round(current + delta, 3),
        adjustment_delta=delta,
        reason=feedback.variance_reason,
        explanation=feedback.adjustment_explanation,
        owner_review_status="pending_review",
        applied=False,
        deterministic=True,
    )


def field_testing_dashboard(session: Session) -> dict[str, object]:
    batches = session.query(LeadImportBatch).all()
    rows = session.query(LeadImportRow).all()
    reviews = session.query(LeadQualityReview).all()
    outcomes = session.query(FieldCallOutcome).all()
    feedback = session.query(PredictionFeedbackRecord).all()
    adjustments = session.query(ScoringAdjustmentSuggestion).all()
    return {
        "lead_import_batches": [model_to_dict(batch) for batch in batches],
        "import_errors": [model_to_dict(row) for row in rows if row.blocked_reasons],
        "qa_low_confidence_leads": [
            model_to_dict(review) for review in reviews if review.import_confidence < 60
        ],
        "call_outcomes_today": [model_to_dict(outcome) for outcome in outcomes],
        "motivated_sellers_found": [
            model_to_dict(outcome)
            for outcome in outcomes
            if outcome.contact_result in {"motivated", "offer_requested", "appointment_set"}
        ],
        "do_not_contact_records": [
            model_to_dict(outcome) for outcome in outcomes if outcome.do_not_contact
        ],
        "prediction_accuracy": round(
            sum(item.accuracy_score for item in feedback) / len(feedback), 2
        )
        if feedback
        else 0,
        "scoring_adjustment_queue": [
            model_to_dict(adjustment)
            for adjustment in adjustments
            if adjustment.owner_review_status == "pending_review"
        ],
        "first_deal_candidate_list": [
            model_to_dict(review)
            for review in reviews
            if review.recommended_next_action in {"call_priority", "underwrite_now"}
        ][:10],
        "live_outreach_allowed": False,
        "bulk_outreach_allowed": False,
        "auto_portal_publish_allowed": False,
    }


def field_testing_briefing(session: Session) -> dict[str, object]:
    dashboard = field_testing_dashboard(session)
    reviews = session.query(LeadQualityReview).all()
    feedback = session.query(PredictionFeedbackRecord).all()
    outcomes = session.query(FieldCallOutcome).all()
    return {
        "generated_by": "Prime 2",
        "imported_leads_today": sum(batch.committed_row_count for batch in session.query(LeadImportBatch).all()),
        "bad_rows_blocked": len(dashboard["import_errors"]),
        "top_10_call_priority_leads": [
            model_to_dict(review)
            for review in sorted(reviews, key=lambda item: item.import_confidence, reverse=True)
            if review.recommended_next_action == "call_priority"
        ][:10],
        "top_5_10k_candidates": [
            {"lead_id": review.lead_id, "import_confidence": review.import_confidence}
            for review in sorted(reviews, key=lambda item: item.import_confidence, reverse=True)
            if review.lead_id and review.import_confidence >= 70
        ][:5],
        "leads_needing_research": [
            model_to_dict(review)
            for review in reviews
            if review.recommended_next_action == "research_more"
        ],
        "leads_with_bad_contact_info": [
            model_to_dict(review)
            for review in reviews
            if review.checks.get("missing_phone") or review.contactability_score < 40
        ],
        "follow_ups_due": [
            model_to_dict(outcome)
            for outcome in outcomes
            if outcome.next_follow_up_date is not None
        ],
        "prediction_misses": [
            model_to_dict(item) for item in feedback if item.accuracy_score < 70
        ],
        "scoring_adjustment_suggestions": dashboard["scoring_adjustment_queue"],
        "next_best_action_for_operator": "Review bad rows, call-priority leads, and prediction misses before any owner-approved field action.",
        "live_outreach_allowed": False,
        "bulk_outreach_allowed": False,
    }
