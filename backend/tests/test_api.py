from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_core_api_routes_respond():
    routes = [
        "/health",
        "/api/system/rules",
        "/api/command-center",
        "/api/hierarchy",
        "/api/divisions",
        "/api/managers",
        "/api/agents",
        "/api/leads",
        "/api/deals",
        "/api/underwriting",
        "/api/profit-control",
        "/api/seller-followups",
        "/api/buyers",
        "/api/buyer-matches",
        "/api/buyer-portal/rules",
        "/api/buyer-portal/internal-dashboard",
        "/api/compliance",
        "/api/daily-briefing",
    ]
    with TestClient(app) as scoped_client:
        for route in routes:
            response = scoped_client.get(route)
            assert response.status_code == 200, route


def test_no_public_signup_or_portal_routes_are_registered():
    paths = {route.path for route in app.routes}
    assert not any("signup" in path for path in paths)
    assert not any("seller-portal" in path for path in paths)
    assert not any("client-portal" in path for path in paths)


def test_action_validation_endpoint_blocks_live_sms():
    with TestClient(app) as scoped_client:
        response = scoped_client.post(
            "/api/actions/validate",
            json={"actor": "Seller Script Agent", "action": "send_sms"},
        )
    assert response.status_code == 200
    assert response.json()["allowed"] is False
