from fastapi.testclient import TestClient

from app.domain.seller_portal import (
    FORBIDDEN_SELLER_PORTAL_KEYS,
    seller_response_is_review_only,
    seller_visibility_gate,
    validate_seller_portal_language,
)
from app.main import app
from app.seed_data import seed_payload


INVITE_HEADERS = {"X-Seller-Invite": "demo-seller-invite"}


def test_seller_portal_is_invite_gated_and_no_public_signup():
    with TestClient(app) as client:
        gated = client.get("/api/seller-portal/offer")
        rules = client.get("/api/seller-portal/rules")
    assert gated.status_code == 403
    assert rules.status_code == 200
    assert rules.json()["invite_gated_only"] is True
    assert rules.json()["public_signup"] is False


def test_seller_portal_only_shows_sanitized_offer_data():
    with TestClient(app) as client:
        response = client.get("/api/seller-portal/offer", headers=INVITE_HEADERS)
    assert response.status_code == 200
    offer = response.json()
    assert FORBIDDEN_SELLER_PORTAL_KEYS.isdisjoint(offer.keys())
    serialized = str(offer).lower()
    for forbidden in [
        "buyer_purchase_price",
        "assignment fee",
        "internal spread",
        "max seller offer",
        "motivation score",
        "seller temperature",
        "prime 2",
        "compliance risk",
    ]:
        assert forbidden not in serialized
    assert offer["seller_questions_notes_action"]["type"] == "draft_intake_only"
    assert offer["seller_questions_notes_action"]["automatic_negotiation_allowed"] is False
    assert offer["seller_questions_notes_action"]["offer_acceptance_execution_allowed"] is False


def test_hidden_or_blocked_seller_offers_cannot_be_viewed():
    with TestClient(app) as client:
        hidden = client.get("/api/seller-portal/offers/seller-offer-004", headers=INVITE_HEADERS)
        owner_blocked = client.get("/api/seller-portal/offers/seller-offer-002", headers=INVITE_HEADERS)
        safety_blocked = client.get("/api/seller-portal/offers/seller-offer-005", headers=INVITE_HEADERS)
    assert hidden.status_code == 404
    assert owner_blocked.status_code == 404
    assert safety_blocked.status_code == 404


def test_visibility_blocks_without_owner_compliance_and_safety():
    payload = seed_payload()
    offers = {offer["id"]: offer for offer in payload["seller_offer_publications"]}

    class Obj:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    packet_ok = Obj(packet_prep_allowed=True, approval_status="owner_approved_draft_ready", compliance_guard_passed=True, owner_approval_recorded=True)
    packet_blocked = Obj(packet_prep_allowed=False, approval_status="owner_review_required", compliance_guard_passed=True, owner_approval_recorded=False)
    contract_ok = Obj(contract_status="prep_review", contract_prep_allowed=True, compliance_review_status="approved", owner_approval_status="approved")
    contract_no_owner = Obj(contract_status="prep_review", contract_prep_allowed=False, compliance_review_status="approved", owner_approval_status="pending")
    contract_no_compliance = Obj(contract_status="prep_review", contract_prep_allowed=False, compliance_review_status="pending", owner_approval_status="approved")

    owner_missing = Obj(**offers["seller-offer-002"])
    owner_missing.offer_packet = packet_blocked
    owner_missing.contract_control = contract_no_owner
    compliance_missing = Obj(**offers["seller-offer-003"])
    compliance_missing.offer_packet = packet_ok
    compliance_missing.contract_control = contract_no_compliance
    unsafe = Obj(**offers["seller-offer-005"])
    unsafe.offer_packet = packet_ok
    unsafe.contract_control = contract_ok

    assert "owner_approval_not_recorded" in seller_visibility_gate(owner_missing)["blocked_reasons"]
    assert "compliance_check_not_passed" in seller_visibility_gate(compliance_missing)["blocked_reasons"]
    assert "offer_language_safety_not_passed" in seller_visibility_gate(unsafe)["blocked_reasons"]


def test_seller_response_is_review_only_and_does_not_execute_acceptance():
    with TestClient(app) as client:
        response = client.post(
            "/api/seller-portal/responses",
            headers=INVITE_HEADERS,
            json={
                "offer_id": "seller-offer-001",
                "response_type": "offer_question",
                "offer_question": "Can we review access next week?",
            },
        )
        acceptance = client.post(
            "/api/seller-portal/offers/seller-offer-001/accept",
            headers=INVITE_HEADERS,
        )
    assert response.status_code == 200
    body = response.json()
    assert body["draft_only"] is True
    assert body["review_only"] is True
    assert body["negotiation_execution_allowed"] is False
    assert body["contract_execution_allowed"] is False
    assert body["automatic_acceptance_allowed"] is False
    assert acceptance.status_code == 400
    assert acceptance.json()["detail"]["contract_execution_allowed"] is False


def test_seller_portal_language_blocks_legal_advice_and_pressure():
    samples = [
        "You must sign now.",
        "This is legal advice and no attorney needed.",
        "Offer expires in minutes.",
        "We already have a buyer and guaranteed closing.",
        "Click to accept contract.",
        "Automatically accept the counteroffer.",
    ]
    for sample in samples:
        result = validate_seller_portal_language(sample)
        assert result["allowed"] is False
        assert result["risk_flags"]


def test_seeded_responses_are_review_only():
    payload = seed_payload()
    for row in payload["seller_portal_responses"]:
        response = type("Response", (), row)()
        assert seller_response_is_review_only(response) is True
