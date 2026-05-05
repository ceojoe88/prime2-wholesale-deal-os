from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.domains.ai_gateway.ai_router import handle_ai_request
from app.domains.document_intelligence.classifier import classify_document
from app.domains.document_intelligence.extractor import extract_document_fields
from app.domains.document_intelligence.safety import issue_for_safety_flag, scan_document_text
from app.domains.document_intelligence.sanitizer import sanitize_document, sanitize_record
from app.models import (
    Deal,
    DealEvidencePacket,
    DocumentClassificationResult,
    DocumentEvidenceLink,
    DocumentExtractedFields,
    DocumentIntelligenceFile,
    DocumentIssueFlag,
    DocumentReviewTask,
)


def _next_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:10]}"


def _issue(
    *,
    issue_type: str,
    severity: str,
    source_field: str,
    explanation: str,
    recommended_next_action: str,
    compliance: bool = False,
    external: bool = False,
) -> dict[str, object]:
    return {
        "issue_type": issue_type,
        "severity": severity,
        "source_field": source_field,
        "explanation": explanation,
        "recommended_next_action": recommended_next_action,
        "owner_review_required": True,
        "compliance_review_required": compliance,
        "external_review_reminder": external,
    }


def _issues_from_extraction(
    *,
    document_type: str,
    extracted: dict[str, object],
    deal: Deal | None,
    safety: dict[str, object],
) -> list[dict[str, object]]:
    issues = [
        _issue(
            issue_type=f"missing_{field}",
            severity="high" if field in {"purchase_price", "signature", "property_address"} else "medium",
            source_field=str(field),
            explanation=f"Required document field is missing: {field}.",
            recommended_next_action="Request missing data or route document for owner review before relying on it.",
            compliance=field in {"signature", "assignment_language"},
            external=field in {"signature", "assignment_language"},
        )
        for field in extracted["missing_fields"]
    ]
    if deal and extracted.get("purchase_price") and document_type in {"purchase_agreement", "assignment_agreement"}:
        expected = deal.seller_contract_price if document_type == "purchase_agreement" else deal.buyer_purchase_price
        actual = int(extracted["purchase_price"])
        if abs(actual - expected) > 500:
            issues.append(
                _issue(
                    issue_type="mismatched_purchase_price",
                    severity="high",
                    source_field="purchase_price",
                    explanation=f"Document price {actual} does not match the deal record value {expected}.",
                    recommended_next_action="Reconcile source numbers before any review packet or evidence use.",
                    compliance=True,
                    external=True,
                )
            )
    if deal and extracted.get("pof_amount"):
        pof_amount = int(extracted["pof_amount"])
        if pof_amount < deal.buyer_purchase_price:
            issues.append(
                _issue(
                    issue_type="pof_amount_below_buyer_offer",
                    severity="high",
                    source_field="pof_amount",
                    explanation="Proof-of-funds amount is below the buyer purchase price on the deal record.",
                    recommended_next_action="Queue buyer POF follow-up; no buyer-facing claim should be made.",
                    compliance=True,
                )
            )
    if document_type in {"purchase_agreement", "assignment_agreement", "title_doc"} and not extracted.get("title_company_name"):
        issues.append(
            _issue(
                issue_type="title_company_missing",
                severity="medium",
                source_field="title_company_name",
                explanation="Title company name was not captured from the document.",
                recommended_next_action="Add title/attorney review reminder and confirm externally.",
                external=True,
            )
        )
    for flag in safety["risk_flags"]:
        issues.append(issue_for_safety_flag(str(flag)))
    return issues


def _create_review_tasks(session: Session, document_id: str, issues: list[dict[str, object]]) -> None:
    task_types = {"owner_review"}
    if any(issue.get("compliance_review_required") for issue in issues):
        task_types.add("compliance_review")
    if any(issue.get("external_review_reminder") for issue in issues):
        task_types.add("title_attorney_external_review_reminder")
    if any("pof" in str(issue.get("issue_type")) for issue in issues):
        task_types.add("buyer_pof_follow_up")
    if any("missing" in str(issue.get("issue_type")) for issue in issues):
        task_types.add("missing_data_request")
    for task_type in sorted(task_types):
        session.add(
            DocumentReviewTask(
                id=_next_id("doc-review"),
                document_id=document_id,
                task_type=task_type,
                assigned_to="Owner" if task_type == "owner_review" else "Prime 2",
                status="open",
                priority="high" if task_type in {"compliance_review", "title_attorney_external_review_reminder"} else "normal",
                reason=f"{task_type} required by document intelligence.",
                recommended_next_action="Review document evidence and resolve issue before operational use.",
                owner_review_required=True,
                live_send_allowed=False,
                legal_review_external_only=task_type == "title_attorney_external_review_reminder",
            )
        )


def _maybe_ai_assist(
    session: Session,
    *,
    document_id: str,
    text: str,
    extracted: dict[str, object],
    use_ai_assist: bool,
) -> str | None:
    if not use_ai_assist:
        return None
    try:
        result = handle_ai_request(
            session,
            request_type="document_intelligence_extraction",
            prompt="Extract document fields using provided text evidence only. Do not provide legal conclusions.",
            source_record_type="document_intelligence_file",
            source_record_id=document_id,
            source_data={
                "document_excerpt": text[:600],
                "extracted_fields": extracted,
                "next_best_action": "owner document review",
            },
        )
    except Exception:
        return None
    return str(result["id"]) if result.get("allowed") else None


def analyze_document(session: Session, **payload: object) -> dict[str, object]:
    text = str(payload.get("pasted_text") or "")
    manual_metadata = dict(payload.get("manual_metadata") or {})
    filename = str(payload.get("original_filename") or "document.txt")
    classification = classify_document(
        filename=filename,
        text=text,
        manual_document_type=payload.get("manual_document_type"),
    )
    document_type = str(classification["document_type"])
    extracted = extract_document_fields(
        document_type=document_type,
        text=text,
        manual_metadata=manual_metadata,
    )
    safety = scan_document_text(text)
    deal_id = payload.get("source_deal_id")
    deal = session.get(Deal, str(deal_id)) if deal_id else None
    issues = _issues_from_extraction(
        document_type=document_type,
        extracted=extracted,
        deal=deal,
        safety=safety,
    )
    high_issue = any(issue["severity"] == "high" for issue in issues)
    document_id = _next_id("doc-intel")
    ai_request_id = _maybe_ai_assist(
        session,
        document_id=document_id,
        text=text,
        extracted=extracted,
        use_ai_assist=bool(payload.get("use_ai_assist")),
    )
    document = DocumentIntelligenceFile(
        id=document_id,
        source_deal_id=str(deal_id) if deal_id else None,
        source_lead_id=payload.get("source_lead_id"),
        source_buyer_id=payload.get("source_buyer_id"),
        uploaded_by=str(payload.get("uploaded_by") or "Owner"),
        original_filename=filename,
        file_type=str(payload.get("file_type") or "text"),
        storage_reference=str(payload.get("storage_reference") or ""),
        document_type=document_type,
        status="needs_review" if issues else "approved_for_internal_use",
        classification_confidence=float(classification["confidence_score"]),
        extracted_summary=str(extracted["summary"]),
        extracted_price=extracted.get("purchase_price"),
        extracted_buyer_name=str(extracted["buyer_name"]),
        extracted_seller_name=str(extracted["seller_name"]),
        extracted_property_address=str(extracted["property_address"]),
        extracted_effective_date=str(extracted["effective_date"]),
        extracted_closing_date=str(extracted["closing_date"]),
        extracted_signature_status=str(extracted["signature_status"]),
        extracted_assignment_language_present=bool(extracted["assignment_language_present"]),
        extracted_pof_amount=extracted.get("pof_amount"),
        risk_status="high" if high_issue else ("needs_review" if issues else "clear"),
        owner_review_status="pending_review" if issues else "reviewed_internal_use",
        full_text_internal=text,
        raw_text_stored=bool(text),
        portal_publish_allowed=False,
        legal_advice_provided=False,
        executable_contract_generated=False,
    )
    session.add(document)
    session.flush()
    session.add(
        DocumentClassificationResult(
            id=_next_id("doc-class"),
            document_id=document_id,
            document_type=document_type,
            confidence_score=float(classification["confidence_score"]),
            classification_reasons=classification["classification_reasons"],
            owner_review_required=True,
        )
    )
    session.add(
        DocumentExtractedFields(
            id=_next_id("doc-fields"),
            document_id=document_id,
            parties={"seller": extracted["seller_name"], "buyer": extracted["buyer_name"]},
            prices={"purchase_price": extracted.get("purchase_price")},
            dates={
                "effective_date": extracted["effective_date"],
                "closing_date": extracted["closing_date"],
            },
            signature_status=str(extracted["signature_status"]),
            assignment_language_present=bool(extracted["assignment_language_present"]),
            pof_amount=extracted.get("pof_amount"),
            title_company_name=str(extracted["title_company_name"]),
            missing_fields=extracted["missing_fields"],
            source_basis=extracted["source_basis"],
            deterministic_fallback_used=True,
            ai_request_id=ai_request_id,
        )
    )
    for issue in issues:
        session.add(DocumentIssueFlag(id=_next_id("doc-issue"), document_id=document_id, **issue))
    _create_review_tasks(session, document_id, issues)
    if deal:
        packet = (
            session.query(DealEvidencePacket)
            .filter(DealEvidencePacket.deal_id == deal.id)
            .first()
        )
        session.add(
            DocumentEvidenceLink(
                id=_next_id("doc-evidence"),
                document_id=document_id,
                deal_evidence_packet_id=packet.id if packet else None,
                source_record_type="deal",
                source_record_id=deal.id,
                linkage_status="linked" if packet else "packet_missing",
                sanitized_for_export=True,
                portal_publish_allowed=False,
            )
        )
    session.commit()
    return document_detail(session, document_id)


def document_detail(session: Session, document_id: str) -> dict[str, object]:
    document = session.get(DocumentIntelligenceFile, document_id)
    if document is None:
        raise ValueError("document_not_found")
    return {
        "document": sanitize_document(document),
        "classification": [
            sanitize_record(record)
            for record in session.query(DocumentClassificationResult).filter_by(document_id=document_id).all()
        ],
        "extracted_fields": [
            sanitize_record(record)
            for record in session.query(DocumentExtractedFields).filter_by(document_id=document_id).all()
        ],
        "issues": [
            sanitize_record(record)
            for record in session.query(DocumentIssueFlag).filter_by(document_id=document_id).all()
        ],
        "review_tasks": [
            sanitize_record(record)
            for record in session.query(DocumentReviewTask).filter_by(document_id=document_id).all()
        ],
        "evidence_links": [
            sanitize_record(record)
            for record in session.query(DocumentEvidenceLink).filter_by(document_id=document_id).all()
        ],
        "raw_text_exposed": False,
        "legal_advice_provided": False,
        "contract_execution_allowed": False,
        "automatic_portal_publish_allowed": False,
    }


def document_dashboard(session: Session) -> dict[str, object]:
    documents = (
        session.query(DocumentIntelligenceFile)
        .order_by(DocumentIntelligenceFile.created_at.desc())
        .all()
    )
    issues = session.query(DocumentIssueFlag).all()
    tasks = session.query(DocumentReviewTask).all()
    evidence_links = session.query(DocumentEvidenceLink).all()
    return {
        "documents": [sanitize_document(record) for record in documents],
        "recent_documents": [sanitize_document(record) for record in documents[:10]],
        "documents_needing_review": [
            sanitize_document(record) for record in documents if record.owner_review_status == "pending_review"
        ],
        "missing_signatures": [
            sanitize_document(record) for record in documents if record.extracted_signature_status != "signed"
        ],
        "price_mismatches": [
            sanitize_record(issue) for issue in issues if issue.issue_type == "mismatched_purchase_price"
        ],
        "pof_issues": [
            sanitize_record(issue) for issue in issues if "pof" in issue.issue_type
        ],
        "assignment_language_warnings": [
            sanitize_record(issue) for issue in issues if "assignment" in issue.issue_type
        ],
        "external_review_reminders": [
            sanitize_record(task) for task in tasks if task.legal_review_external_only
        ],
        "linked_deal_evidence": [sanitize_record(record) for record in evidence_links],
        "issues": [sanitize_record(issue) for issue in issues],
        "review_tasks": [sanitize_record(task) for task in tasks],
        "document_intelligence_only": True,
        "legal_review_performed": False,
        "executable_contract_generation_allowed": False,
        "title_submission_allowed": False,
    }

