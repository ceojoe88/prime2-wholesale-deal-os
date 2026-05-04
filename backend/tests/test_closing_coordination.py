from fastapi.testclient import TestClient

from app.domain.closing_coordination import NEXT_ACTION_BY_BLOCKER
from app.main import app


BUYER_HEADERS = {"X-Buyer-Invite": "demo-buyer-invite"}
SELLER_HEADERS = {"X-Seller-Invite": "demo-seller-invite"}


def test_unified_deal_room_does_not_leak_to_portals():
    with TestClient(app) as client:
        buyer = client.get("/api/buyer-portal/deals", headers=BUYER_HEADERS)
        seller = client.get("/api/seller-portal/offer", headers=SELLER_HEADERS)

    assert buyer.status_code == 200
    assert seller.status_code == 200
    serialized = f"{buyer.json()} {seller.json()}".lower()
    for forbidden in [
        "deal_room",
        "closing_coordination",
        "blocker_records",
        "next_best_actions",
        "projected_assignment_fee",
        "internal_spread",
        "assignment fee",
    ]:
        assert forbidden not in serialized


def test_deal_room_is_coordination_only_no_execution_title_or_payment():
    with TestClient(app) as client:
        response = client.get("/api/deal-room/deal-room-001")

    assert response.status_code == 200
    body = response.json()
    assert body["recommendation_only"] is True
    assert body["legal_execution_allowed"] is False
    assert body["executable_contract_generated"] is False
    assert body["title_submission_allowed"] is False
    assert body["payment_handling_allowed"] is False
    assert body["automatic_negotiation_allowed"] is False
    assert body["readiness_gate"]["legal_execution_allowed"] is False
    assert body["readiness_gate"]["title_submission_allowed"] is False
    assert body["readiness_gate"]["payment_handling_allowed"] is False


def test_blockers_are_generated_from_missing_conditions():
    with TestClient(app) as client:
        response = client.get("/api/closing-coordination/blockers")

    assert response.status_code == 200
    blockers = response.json()
    blocker_types = {blocker["blocker_type"] for blocker in blockers}
    assert "missing_owner_approval" in blocker_types
    assert "missing_compliance_review" in blocker_types
    assert "missing_buyer_pof" in blocker_types
    assert "missing_seller_document" in blocker_types
    assert "weak_buyer_margin" in blocker_types
    assert "high_risk_language" in blocker_types
    assert "assignment_not_confirmed" in blocker_types
    assert "title_handoff_incomplete" in blocker_types
    assert "communication_draft_pending" in blocker_types
    assert all(blocker["draft_only"] is True for blocker in blockers)


def test_readiness_requires_buyer_seller_compliance_owner_and_title_conditions():
    with TestClient(app) as client:
        response = client.get("/api/closing-coordination/readiness")

    assert response.status_code == 200
    records = {record["deal_room_id"]: record for record in response.json()}
    assert records["deal-room-001"]["gate"]["closing_ready"] is True
    assert records["deal-room-001"]["coordination_status"] == "closing_ready"
    assert records["deal-room-002"]["gate"]["closing_ready"] is False
    assert "owner_approval_complete" in records["deal-room-002"]["gate"]["blocked_reasons"]
    assert records["deal-room-003"]["gate"]["closing_ready"] is False
    assert "compliance_review_complete" in records["deal-room-003"]["gate"]["blocked_reasons"]
    assert records["deal-room-004"]["gate"]["closing_ready"] is False
    assert "buyer_pof_verified" in records["deal-room-004"]["gate"]["blocked_reasons"]
    assert "title_handoff_prepared" in records["deal-room-004"]["gate"]["blocked_reasons"]


def test_next_best_actions_are_recommendations_only():
    with TestClient(app) as client:
        response = client.get("/api/closing-coordination")

    assert response.status_code == 200
    actions = response.json()["next_best_actions"]
    allowed_actions = set(NEXT_ACTION_BY_BLOCKER.values())
    assert actions
    for action in actions:
        assert action["action"] in allowed_actions
        assert action["recommendation_only"] is True
        assert action["legal_execution_allowed"] is False
        assert action["title_submission_allowed"] is False
        assert action["payment_handling_allowed"] is False
        assert action["automatic_negotiation_allowed"] is False


def test_projected_assignment_fees_at_risk_visible_in_internal_dashboard_only():
    with TestClient(app) as client:
        internal = client.get("/api/deal-room")
        seller = client.get("/api/seller-portal/offer", headers=SELLER_HEADERS)

    assert internal.status_code == 200
    assert internal.json()["projected_assignment_fees_at_risk"] > 0
    assert "projected_assignment_fees_at_risk" not in str(seller.json())
