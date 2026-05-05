from __future__ import annotations

from fastapi.testclient import TestClient

from app.domains.ai_gateway.ai_safety import validate_ai_request_type
from app.domains.document_intelligence.classifier import classify_document
from app.domains.document_intelligence.extractor import extract_document_fields
from app.main import app


def test_document_classification_and_extraction_from_pasted_text():
    text = (
        "Purchase Agreement\nSeller: Angela Morris\nBuyer: Prime 2 Acquisitions LLC\n"
        "Property Address: 1420 Cedar Crest Ave, Dallas, TX 75216\n"
        "Purchase Price: $140,000\nEffective Date: 05/08/2026\nClosing Date: 05/30/2026\n"
        "Assignment allowed. Seller signature signed."
    )
    classification = classify_document(filename="purchase-agreement.txt", text=text)
    extracted = extract_document_fields(document_type="purchase_agreement", text=text)
    assert classification["document_type"] == "purchase_agreement"
    assert extracted["purchase_price"] == 140000
    assert extracted["assignment_language_present"] is True
    assert extracted["signature_status"] == "signed"


def test_document_analysis_flags_missing_fields_and_sanitizes_raw_text():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/documents/analyze",
            json={
                "source_deal_id": "deal-002",
                "original_filename": "assignment-draft.txt",
                "manual_document_type": "assignment_agreement",
                "pasted_text": "Assignment Agreement\nSeller: Nina Patel\nPrice: $175,000\nEffective Date: 05/10/2026\nUnsigned.",
                "use_ai_assist": False,
            },
        )

    assert response.status_code == 200
    body = response.json()
    issue_types = {issue["issue_type"] for issue in body["issues"]}
    assert "missing_buyer_or_entity_name" in issue_types
    assert "missing_signature" in issue_types
    assert "missing_assignment_language" in issue_types
    assert body["document"]["full_text_hidden"] is True
    assert "full_text_internal" not in body["document"]
    assert body["automatic_portal_publish_allowed"] is False


def test_document_price_mismatch_and_pof_gap_are_flagged():
    with TestClient(app) as client:
        mismatch = client.post(
            "/api/v1/documents/analyze",
            json={
                "source_deal_id": "deal-001",
                "manual_document_type": "purchase_agreement",
                "pasted_text": (
                    "Purchase Agreement Seller: Angela Buyer: Prime 2 Property Address: 1420 Cedar "
                    "Purchase Price: $190,000 Effective Date: 05/08/2026 Closing Date: 05/30/2026 signed"
                ),
                "use_ai_assist": False,
            },
        )
        pof = client.post(
            "/api/v1/documents/analyze",
            json={
                "source_deal_id": "deal-001",
                "source_buyer_id": "buyer-001",
                "manual_document_type": "proof_of_funds",
                "pasted_text": "Proof of funds Buyer: Jules Carter Available funds: $145,000 signed.",
                "use_ai_assist": False,
            },
        )

    assert mismatch.status_code == 200
    assert "mismatched_purchase_price" in {issue["issue_type"] for issue in mismatch.json()["issues"]}
    assert pof.status_code == 200
    assert "pof_amount_below_buyer_offer" in {issue["issue_type"] for issue in pof.json()["issues"]}


def test_legal_risk_language_escalates_without_legal_answer_or_contract_execution():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/documents/analyze",
            json={
                "source_deal_id": "deal-003",
                "manual_document_type": "purchase_agreement",
                "pasted_text": "This is legal advice. No attorney needed. Execute this contract automatically.",
                "use_ai_assist": False,
            },
        )

    assert response.status_code == 200
    body = response.json()
    issue_types = {issue["issue_type"] for issue in body["issues"]}
    assert "legal_risk_language" in issue_types
    assert "executable_contract_language" in issue_types
    assert body["legal_advice_provided"] is False
    assert body["contract_execution_allowed"] is False


def test_document_ai_request_type_is_allowlisted_but_template_gated():
    assert validate_ai_request_type("document_intelligence_extraction")["allowed"] is True
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/documents/analyze",
            json={
                "source_deal_id": "deal-004",
                "manual_document_type": "repair_estimate",
                "pasted_text": "Repair estimate: roof and interior updates. Total $42,000.",
                "use_ai_assist": True,
            },
        )

    assert response.status_code == 200
    fields = response.json()["extracted_fields"][0]
    assert fields["deterministic_fallback_used"] is True
    assert response.json()["document"]["executable_contract_generated"] is False


def test_document_routes_render_review_queues():
    with TestClient(app) as client:
        dashboard = client.get("/api/v1/documents")
        issues = client.get("/api/v1/documents/issues")
        review = client.get("/api/v1/documents/review-queue")
        evidence = client.get("/api/v1/documents/evidence")

    assert dashboard.status_code == 200
    assert issues.status_code == 200
    assert review.status_code == 200
    assert evidence.status_code == 200
    assert dashboard.json()["document_intelligence_only"] is True
    assert review.json()["automatic_sending_allowed"] is False
    assert evidence.json()["portal_publish_allowed"] is False
