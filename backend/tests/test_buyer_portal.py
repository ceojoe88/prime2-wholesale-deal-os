from fastapi.testclient import TestClient

from app.domain.buyer_portal import (
    FORBIDDEN_BUYER_KEYS,
    portal_publish_gate,
    sanitize_buyer_deal,
)
from app.main import app
from app.seed_data import seed_payload


INVITE_HEADERS = {"X-Buyer-Invite": "demo-buyer-invite"}


def test_buyer_portal_is_invite_gated():
    with TestClient(app) as client:
        response = client.get("/api/buyer-portal/deals")
    assert response.status_code == 403


def test_buyer_portal_only_shows_sanitized_data():
    with TestClient(app) as client:
        response = client.get("/api/buyer-portal/deals", headers=INVITE_HEADERS)
    assert response.status_code == 200
    deals = response.json()
    assert deals
    for deal in deals:
        assert FORBIDDEN_BUYER_KEYS.isdisjoint(deal.keys())
        assert "seller_name" not in str(deal).lower()
        assert "projected_assignment_fee" not in str(deal).lower()
        assert "source_category" not in str(deal).lower()
        assert deal["offer_interest_action"]["contract_execution_allowed"] is False
        assert deal["offer_interest_action"]["payment_collection_allowed"] is False


def test_hidden_or_blocked_deals_cannot_be_viewed():
    with TestClient(app) as client:
        hidden = client.get("/api/buyer-portal/deals/deal-007", headers=INVITE_HEADERS)
        blocked = client.get("/api/buyer-portal/deals/deal-008", headers=INVITE_HEADERS)
    assert hidden.status_code == 404
    assert blocked.status_code == 404


def test_high_risk_and_weak_margin_deals_cannot_be_published():
    payload = seed_payload()
    deals = {deal["id"]: deal for deal in payload["deals"]}
    publications = {item["deal_id"]: item for item in payload["buyer_deal_publications"]}

    class Obj:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    high_risk = Obj(**deals["deal-008"])
    weak_margin = Obj(**deals["deal-006"])
    high_risk_pub = Obj(**publications["deal-008"])
    weak_margin_pub = Obj(**publications["deal-006"])
    assert "risk_status_high" in portal_publish_gate(high_risk, high_risk_pub)["blocked_reasons"]
    assert "buyer_margin_weak" in portal_publish_gate(weak_margin, weak_margin_pub)["blocked_reasons"]


def test_buyer_interest_does_not_execute_contract_or_collect_payment():
    with TestClient(app) as client:
        response = client.post(
            "/api/buyer-portal/deals/deal-001/interest",
            headers=INVITE_HEADERS,
            json={
                "buyer_id": "buyer-001",
                "intended_offer_amount": 166000,
                "notes": "Draft intent for owner review only.",
            },
        )
    assert response.status_code == 200
    body = response.json()
    assert body["draft_only"] is True
    assert body["contract_execution_allowed"] is False
    assert body["contract_executed"] is False
    assert body["payment_collected"] is False
    assert body["real_world_action_taken"] is False


def test_buyer_interest_blocks_legal_advice_language():
    with TestClient(app) as client:
        response = client.post(
            "/api/buyer-portal/deals/deal-001/interest",
            headers=INVITE_HEADERS,
            json={
                "buyer_id": "buyer-001",
                "intended_offer_amount": 166000,
                "notes": "This is legal advice and no attorney is needed.",
            },
        )
    assert response.status_code == 400


def test_sanitizer_rejects_forbidden_fields():
    payload = {"deal_id": "deal-001", "seller_name": "Should Not Leak"}
    try:
        from app.domain.buyer_portal import assert_no_buyer_leaks

        assert_no_buyer_leaks(payload)
    except ValueError as exc:
        assert "forbidden fields" in str(exc)
    else:
        raise AssertionError("forbidden buyer field was not rejected")
