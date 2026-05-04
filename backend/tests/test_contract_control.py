from fastapi.testclient import TestClient

from app.domain.contract_control import validate_contract_language
from app.main import app


def test_contract_safety_guard_blocks_v4_execution_language():
    samples = [
        "Generate executable contract and make it ready to sign.",
        "This is legal advice and no attorney needed.",
        "Send SMS, send email, and call seller.",
        "Submit to title company and open escrow now.",
        "Assignment is guaranteed and buyer will definitely close.",
        "Hide the assignment and keep the fee hidden.",
        "Pretend to be the end buyer and say we own it already.",
        "Automatically mark under contract after this step.",
    ]
    for sample in samples:
        result = validate_contract_language(sample)
        assert result["allowed"] is False
        assert result["risk_flags"]


def test_contract_prep_is_draft_only_and_blocks_unapproved_offer_packet():
    with TestClient(app) as client:
        allowed = client.post("/api/contract-control/contract-001/prepare")
        blocked = client.post("/api/contract-control/contract-002/prepare")

    assert allowed.status_code == 200
    body = allowed.json()
    assert body["draft_only"] is True
    assert body["executable_contract_generated"] is False
    assert body["contract_execution_allowed"] is False
    assert body["title_submission_allowed"] is False
    assert body["automatic_status_change_allowed"] is False
    assert blocked.status_code == 400
    assert "offer_packet_not_approved" in blocked.json()["detail"]["blocked_reasons"]
    assert "owner_approval_not_recorded" in blocked.json()["detail"]["blocked_reasons"]


def test_title_handoff_submission_is_blocked():
    with TestClient(app) as client:
        packet = client.get("/api/title-handoff/title-001")
        submitted = client.post("/api/title-handoff/title-001/submit")

    assert packet.status_code == 200
    assert packet.json()["draft_only"] is True
    assert packet.json()["title_submission_allowed"] is False
    assert packet.json()["submitted_to_title"] is False
    assert submitted.status_code == 400
    assert submitted.json()["detail"]["title_submission_allowed"] is False
    assert submitted.json()["detail"]["submitted_to_title"] is False


def test_assignment_readiness_requires_pof_compliance_and_owner_approval():
    with TestClient(app) as client:
        response = client.get("/api/assignment-readiness")

    assert response.status_code == 200
    records = {record["id"]: record for record in response.json()}
    assert records["assignment-ready-001"]["assignment_ready"] is True
    assert records["assignment-ready-001"]["contract_execution_allowed"] is False
    assert records["assignment-ready-001"]["title_submission_allowed"] is False
    assert "buyer_pof_not_verified" in records["assignment-ready-002"]["blocked_reasons"]
    assert "compliance_review_not_passed" in records["assignment-ready-003"]["blocked_reasons"]
    assert "owner_approval_not_recorded" in records["assignment-ready-004"]["blocked_reasons"]


def test_contract_safety_api_blocks_legal_advice_and_title_submission():
    with TestClient(app) as client:
        legal = client.post(
            "/api/contract-control/safety/validate",
            json={"content": "This is legal advice and you are legally required to sign."},
        )
        title = client.post(
            "/api/contract-control/safety/validate",
            json={"content": "Submit to title company now."},
        )

    assert legal.status_code == 200
    assert legal.json()["allowed"] is False
    assert "legal_advice" in legal.json()["risk_flags"]
    assert title.status_code == 200
    assert title.json()["allowed"] is False
    assert "title_company_submission" in title.json()["risk_flags"]
