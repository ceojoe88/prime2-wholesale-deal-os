from fastapi.testclient import TestClient

from app.domain.seller_acquisition import offer_packet_gate, seller_draft_engine, validate_seller_language
from app.main import app
from app.seed_data import seed_payload


def test_seller_safety_guard_blocks_unsafe_language():
    samples = [
        "You must sign now or this is your last chance.",
        "We already have a buyer and the cash buyer is guaranteed.",
        "This is legal advice and no attorney needed.",
        "Hide the assignment fee and do not mention assignment.",
        "Send SMS and call seller now.",
    ]
    for sample in samples:
        result = validate_seller_language(sample)
        assert result["allowed"] is False
        assert result["risk_flags"]


def test_seller_drafts_are_draft_only_and_no_live_outreach():
    payload = seed_payload()
    lead = type("LeadObj", (), payload["leads"][0])()
    interaction = type("InteractionObj", (), payload["seller_interactions"][0])()
    drafts = seller_draft_engine(lead, interaction)
    assert drafts["draft_only"] is True
    assert drafts["live_outreach_allowed"] is False
    assert drafts["language_guard"]["allowed"] is True
    assert "follow_up_sequence_draft" in drafts


def test_offer_packet_gate_requires_underwriting_compliance_and_owner_approval():
    with TestClient(app) as client:
        allowed = client.post("/api/offer-packets/packet-001/prepare")
        missing_owner = client.post("/api/offer-packets/packet-002/prepare")
        missing_compliance = client.post("/api/offer-packets/packet-003/prepare")
        weak_margin = client.post("/api/offer-packets/packet-004/prepare")
        below_target = client.post("/api/offer-packets/packet-005/prepare")
    assert allowed.status_code == 200
    assert allowed.json()["draft_only"] is True
    assert allowed.json()["real_world_action_taken"] is False
    assert missing_owner.status_code == 400
    assert "owner_approval_not_recorded" in missing_owner.json()["detail"]["blocked_reasons"]
    assert missing_compliance.status_code == 400
    assert "compliance_guard_not_passed" in missing_compliance.json()["detail"]["blocked_reasons"]
    assert weak_margin.status_code == 400
    assert "buyer_margin_not_protected" in weak_margin.json()["detail"]["blocked_reasons"]
    assert below_target.status_code == 400
    assert "target_assignment_fee_not_checked" in below_target.json()["detail"]["blocked_reasons"]


def test_follow_up_control_sequences_are_draft_only():
    with TestClient(app) as client:
        response = client.get("/api/follow-up-control")
    assert response.status_code == 200
    body = response.json()
    assert body["draft_only"] is True
    assert body["live_outreach_allowed"] is False
    assert body["follow_up_sequences"]
    assert all(item["draft_only"] is True for item in body["follow_up_sequences"])
    assert all(item["live_outreach_allowed"] is False for item in body["follow_up_sequences"])


def test_no_legal_advice_language_via_api_validator():
    with TestClient(app) as client:
        response = client.post(
            "/api/seller-acquisition/safety/validate",
            json={"content": "This is legal advice and you are legally required to sign."},
        )
    assert response.status_code == 200
    assert response.json()["allowed"] is False
    assert "legal_advice" in response.json()["risk_flags"]
