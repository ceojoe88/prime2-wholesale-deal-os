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
        "/api/seller-acquisition",
        "/api/follow-up-control",
        "/api/offer-packets",
        "/api/contract-control",
        "/api/title-handoff",
        "/api/assignment-readiness",
        "/api/deal-room",
        "/api/closing-coordination",
        "/api/closing-coordination/blockers",
        "/api/closing-coordination/readiness",
        "/api/deal-evidence",
        "/api/assignment-fees",
        "/api/buyer-demand",
        "/api/buyer-priority",
        "/api/deal-distribution",
        "/api/offer-conversion",
        "/api/negotiations",
        "/api/contract-ready",
        "/api/title-review",
        "/api/review-packets",
        "/api/autonomy",
        "/api/autonomy/rules",
        "/api/autonomy/runs",
        "/api/autonomy/tasks",
        "/api/autonomy/daily-briefing",
        "/api/autonomy/escalations",
        "/api/auto-execution",
        "/api/auto-execution/rules",
        "/api/auto-execution/templates",
        "/api/auto-execution/dry-runs",
        "/api/auto-execution/attempts",
        "/api/auto-execution/audit",
        "/api/buyer-acceleration",
        "/api/buyer-sequences",
        "/api/buyer-response-router",
        "/api/buyer-velocity",
        "/api/optimization",
        "/api/optimization/patterns",
        "/api/optimization/recommendations",
        "/api/optimization/agent-performance",
        "/api/optimization/lost-deals",
        "/api/optimization/source-quality",
        "/api/communications",
        "/api/communications/dry-runs",
        "/api/communications/attempts",
        "/api/communications/approvals",
        "/api/buyers",
        "/api/buyer-matches",
        "/api/buyer-portal/rules",
        "/api/buyer-portal/internal-dashboard",
        "/api/seller-portal/rules",
        "/api/seller-portal/internal-dashboard",
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
    assert not any("client-portal" in path for path in paths)


def test_action_validation_endpoint_blocks_live_sms():
    with TestClient(app) as scoped_client:
        response = scoped_client.post(
            "/api/actions/validate",
            json={"actor": "Seller Script Agent", "action": "send_sms"},
        )
    assert response.status_code == 200
    assert response.json()["allowed"] is False
