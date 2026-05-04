from fastapi.testclient import TestClient

from app.domain.title_review import validate_title_review_language
from app.main import app


def test_title_review_gate_allows_only_v10_ready_deals():
    with TestClient(app) as client:
        response = client.get("/api/title-review")

    assert response.status_code == 200
    body = response.json()
    ready_ids = {
        record["id"]
        for record in body["title_review_records"]
        if record["packet_prep_allowed"]
    }
    assert ready_ids == {"title-review-001"}
    blocked = {
        record["id"]: record
        for record in body["title_review_records"]
        if not record["packet_prep_allowed"]
    }
    assert "v10_contract_ready_not_cleared" in blocked["title-review-002"]["blocked_reasons"]
    assert "owner_approval_not_recorded" in blocked["title-review-002"]["blocked_reasons"]
    assert "compliance_not_passed" in blocked["title-review-003"]["blocked_reasons"]
    assert body["contract_execution_allowed"] is False
    assert body["document_submission_allowed"] is False
    assert body["title_company_email_send_allowed"] is False


def test_review_packet_prep_is_draft_only_and_never_submits():
    with TestClient(app) as client:
        response = client.get("/api/review-packets")

    assert response.status_code == 200
    body = response.json()
    ready_packets = {packet["id"] for packet in body["packet_prep_ready"]}
    assert ready_packets == {"review-packet-001"}
    for packet in body["review_packet_preps"]:
        assert packet["draft_only"] is True
        assert packet["submitted_to_title"] is False
        assert packet["contract_execution_allowed"] is False
        assert packet["document_submission_allowed"] is False
        assert packet["title_company_email_send_allowed"] is False


def test_title_review_safety_blocks_legal_submission_and_guarantee_language():
    result = validate_title_review_language(
        "No attorney needed. Send documents to title and guaranteed closing."
    )

    assert result["allowed"] is False
    assert "legal_advice" in result["risk_flags"]
    assert "document_submission" in result["risk_flags"]
    assert "closing_guarantee" in result["risk_flags"]


def test_title_review_safety_endpoint_blocks_title_email_send():
    with TestClient(app) as client:
        response = client.post(
            "/api/title-review/safety/validate",
            json={"content": "Email title company now and say we are your attorney."},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["allowed"] is False
    assert "title_company_email_send" in body["risk_flags"]
    assert "attorney_client_relationship_claim" in body["risk_flags"]
