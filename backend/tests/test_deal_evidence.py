from fastapi.testclient import TestClient

from app.domain.deal_evidence import validate_profit_claims
from app.main import app


def test_assignment_fee_attribution_requires_source_records():
    with TestClient(app) as client:
        response = client.get("/api/assignment-fees/fee-004")

    assert response.status_code == 200
    body = response.json()
    assert body["verification_status"] == "missing_evidence"
    assert body["source_records_present"] is False
    assert "source_records_missing" in body["fee_gate"]["blocked_reasons"]
    assert body["client_facing_proof_allowed"] is False


def test_unsupported_profit_claims_are_blocked():
    result = validate_profit_claims(
        "This deal has guaranteed profit and guaranteed ROI with an invented buyer price."
    )

    assert result["allowed"] is False
    assert "fake_profit_claim" in result["risk_flags"]
    assert "unsupported_roi_claim" in result["risk_flags"]
    assert "invented_buyer_seller_numbers" in result["risk_flags"]


def test_10k_flag_uses_actual_source_numbers():
    with TestClient(app) as client:
        verified = client.get("/api/assignment-fees/fee-001")
        owner_review = client.get("/api/assignment-fees/fee-002")

    assert verified.status_code == 200
    body = verified.json()
    assert body["projected_assignment_fee"] == (
        body["buyer_purchase_price"] - body["seller_contract_price"]
    )
    assert body["projected_assignment_fee"] >= body["target_assignment_fee"]
    assert body["verified_10k_opportunity"] is True

    assert owner_review.status_code == 200
    pending = owner_review.json()
    assert pending["projected_assignment_fee"] >= pending["target_assignment_fee"]
    assert pending["verified_10k_opportunity"] is False
    assert pending["verification_status"] == "owner_review_needed"


def test_evidence_packet_sanitizes_internal_notes():
    with TestClient(app) as client:
        response = client.get("/api/deal-evidence/evidence-001")

    assert response.status_code == 200
    body = response.json()
    serialized = str(body["sanitized_summary"]).lower()
    for forbidden in [
        "call_notes",
        "motivation_answers",
        "pain_points",
        "objections",
        "seller_temperature_score",
        "wholesale_prime_recommendations",
    ]:
        assert forbidden not in serialized
    assert body["internal_notes_sanitized"] is True
    assert body["client_facing_proof_allowed"] is False


def test_no_legal_or_closing_guarantees_in_evidence_language():
    with TestClient(app) as client:
        response = client.post(
            "/api/deal-evidence/safety/validate",
            json={"content": "We guarantee closing and this is a risk-free return."},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["allowed"] is False
    assert "legal_closing_guarantee" in body["risk_flags"]
    assert "unsupported_roi_claim" in body["risk_flags"]
