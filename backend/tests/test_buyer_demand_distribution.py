from fastapi.testclient import TestClient

from app.domain.buyer_demand import validate_distribution_language
from app.main import app


def test_buyer_priority_ranking_uses_fit_and_pof():
    with TestClient(app) as client:
        response = client.get("/api/buyer-priority")

    assert response.status_code == 200
    body = response.json()
    deal_001 = [
        priority
        for priority in body["buyer_priority_rankings"]
        if priority["deal_id"] == "deal-001"
    ]
    assert deal_001[0]["buyer_id"] == "buyer-001"
    assert deal_001[0]["rank"] == 1
    assert deal_001[0]["priority_score"] >= 90
    assert deal_001[0]["buyer"]["proof_of_funds_status"] == "verified"
    assert deal_001[0]["buyer_blast_allowed"] is False


def test_deal_sheet_is_sanitized_for_distribution_prep():
    with TestClient(app) as client:
        response = client.get("/api/deal-distribution/distribution-001")

    assert response.status_code == 200
    body = response.json()
    sheet = body["sanitized_deal_sheet"]
    assert set(sheet.keys()) == {
        "property_summary",
        "asking_price",
        "arv_range",
        "repair_estimate_range",
        "buyer_margin_estimate",
        "access_instructions_placeholder",
        "availability_status",
        "proof_inspection_notes_placeholder",
    }
    serialized = str(sheet).lower()
    for forbidden in [
        "seller_name",
        "seller_contact",
        "seller_contract_price",
        "assignment_fee",
        "lead_source",
        "motivation_score",
        "internal_spread",
        "agent_recommendations",
        "compliance_internals",
    ]:
        assert forbidden not in serialized
    assert body["live_send_allowed"] is False
    assert body["bulk_blast_allowed"] is False


def test_live_blast_and_bulk_send_are_blocked():
    with TestClient(app) as client:
        response = client.post(
            "/api/deal-distribution/safety/validate",
            json={"content": "Buyer blast this deal with a bulk send to all buyers."},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["allowed"] is False
    assert "live_buyer_blast" in body["risk_flags"]
    assert "bulk_send" in body["risk_flags"]


def test_unsupported_scarcity_and_fake_competition_are_blocked():
    result = validate_distribution_language(
        "Last chance: we already have offers and multiple buyers are lined up."
    )

    assert result["allowed"] is False
    assert "misleading_scarcity" in result["risk_flags"]
    assert "fake_buyer_competition" in result["risk_flags"]


def test_distribution_records_never_execute_contract_or_send():
    with TestClient(app) as client:
        response = client.get("/api/deal-distribution")

    assert response.status_code == 200
    body = response.json()
    assert body["live_send_allowed"] is False
    assert body["bulk_blast_allowed"] is False
    assert body["buyer_blast_allowed"] is False
    for prep in body["distribution_preps"]:
        assert prep["draft_only"] is True
        assert prep["live_send_allowed"] is False
        assert prep["bulk_blast_allowed"] is False
        assert prep["contract_execution_allowed"] is False
