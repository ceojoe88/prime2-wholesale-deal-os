from __future__ import annotations

from fastapi.testclient import TestClient

from app.domains.client_command.safety import (
    CLIENT_COMMAND_BLOCKED_ACTIONS,
    validate_client_safe_text,
)
from app.main import app


def test_cp5_buyer_profile_creation_enforces_workspace_isolation():
    with TestClient(app) as client:
        created = client.post(
            "/api/v1/client-command/workspaces/client-workspace-003/buyers",
            json={
                "buyer_name": "CP5 isolation buyer",
                "primary_market": "Memphis",
                "target_zip_codes": ["38118"],
                "preferred_property_types": ["single_family"],
                "max_price": 100000,
                "funding_status": "stated",
                "proof_of_funds_status": "requested",
                "active_status": "active",
            },
        )
        buyer_id = created.json()["buyer"]["id"]
        allowed = client.get(
            f"/api/v1/client-command/buyers/{buyer_id}",
            params={"workspace_id": "client-workspace-003"},
        )
        denied = client.get(
            f"/api/v1/client-command/buyers/{buyer_id}",
            params={"workspace_id": "client-workspace-001"},
        )

    assert created.status_code == 200
    assert allowed.status_code == 200
    assert allowed.json()["buyer"]["workspace_id"] == "client-workspace-003"
    assert denied.status_code == 404


def test_cp5_buyer_buy_box_is_workspace_scoped():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/client-command/buyers/client-buyer-memphis-flipper/buy-boxes",
            params={"workspace_id": "client-workspace-003"},
        )
        denied = client.get(
            "/api/v1/client-command/buyers/client-buyer-memphis-flipper/buy-boxes",
            params={"workspace_id": "client-workspace-001"},
        )

    assert response.status_code == 200
    assert response.json()["buy_boxes"]
    assert response.json()["buy_boxes"][0]["workspace_id"] == "client-workspace-003"
    assert denied.status_code == 404


def test_cp5_buyer_confidence_is_deterministic_and_lowers_for_unclear_buy_box():
    with TestClient(app) as client:
        strong_first = client.get(
            "/api/v1/client-command/buyers/client-buyer-memphis-flipper/confidence-score",
            params={"workspace_id": "client-workspace-003"},
        )
        strong_second = client.get(
            "/api/v1/client-command/buyers/client-buyer-memphis-flipper/confidence-score",
            params={"workspace_id": "client-workspace-003"},
        )
        weak = client.get(
            "/api/v1/client-command/buyers/client-buyer-memphis-review/confidence-score",
            params={"workspace_id": "client-workspace-003"},
        )

    assert strong_first.status_code == 200
    assert strong_second.status_code == 200
    assert strong_first.json()["confidence"]["confidence_score"] == strong_second.json()["confidence"]["confidence_score"]
    assert strong_first.json()["confidence"]["confidence_score"] > weak.json()["confidence"]["confidence_score"]
    assert weak.json()["confidence"]["requires_human_review"] is True


def test_cp5_deal_to_buyer_matching_is_deterministic_and_has_strong_fit():
    with TestClient(app) as client:
        first = client.get(
            "/api/v1/client-command/leads/client-lead-memphis-005/buyer-matches",
            params={"workspace_id": "client-workspace-003"},
        )
        second = client.get(
            "/api/v1/client-command/leads/client-lead-memphis-005/buyer-matches",
            params={"workspace_id": "client-workspace-003"},
        )

    assert first.status_code == 200
    assert second.status_code == 200
    first_matches = first.json()["buyer_matches"]
    second_matches = second.json()["buyer_matches"]
    assert [(item["buyer_id"], item["match_score"]) for item in first_matches] == [
        (item["buyer_id"], item["match_score"]) for item in second_matches
    ]
    strong = [item for item in first_matches if item["match_status"] == "strong_match"]
    assert {item["buyer_id"] for item in strong} >= {
        "client-buyer-memphis-landlord",
        "client-buyer-memphis-flipper",
    }


def test_cp5_weak_buyer_match_shows_mismatch_reasons():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/client-command/leads/client-lead-memphis-005/buyer-matches",
            params={"workspace_id": "client-workspace-003"},
        )

    weak = next(item for item in response.json()["buyer_matches"] if item["buyer_id"] == "client-buyer-memphis-review")
    assert weak["match_status"] in {"weak_match", "blocked", "needs_review"}
    assert "buyer_buy_box_missing" in weak["mismatch_reasons"]
    assert weak["requires_human_review"] is True


def test_cp5_disposition_readiness_blocks_when_cp4_offer_readiness_is_blocked():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/client-command/leads/client-lead-memphis-004/disposition-readiness",
            params={"workspace_id": "client-workspace-003"},
        )

    gate = response.json()["disposition_readiness"]
    assert response.status_code == 200
    assert gate["readiness_status"] == "offer_readiness_blocked"
    assert "thin_offer_margin" in gate["block_reasons"]
    assert gate["can_prepare_buyer_outreach"] is False


def test_cp5_disposition_readiness_blocks_when_buyer_demand_evidence_is_missing():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/client-command/leads/client-lead-memphis-003/disposition-readiness",
            params={"workspace_id": "client-workspace-003"},
        )

    gate = response.json()["disposition_readiness"]
    assert response.status_code == 200
    assert gate["readiness_status"] == "buyer_demand_missing"
    assert "buyer_demand_evidence_missing" in gate["block_reasons"]
    assert gate["no_buyer_contacted"] is True


def test_cp5_disposition_readiness_reaches_ready_for_memphis_lead_5():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/client-command/leads/client-lead-memphis-005/disposition-readiness",
            params={"workspace_id": "client-workspace-003"},
        )

    gate = response.json()["disposition_readiness"]
    assert response.status_code == 200
    assert gate["readiness_status"] == "ready_for_client_review"
    assert gate["can_prepare_buyer_outreach"] is True
    assert gate["no_buyer_contacted"] is True
    assert gate["no_campaign_started"] is True
    assert gate["no_contract_generated"] is True


def test_cp5_buyer_outreach_drafts_are_manual_use_only_and_do_not_contact_buyers():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/client-command/leads/client-lead-memphis-005/buyer-outreach-drafts",
            params={"workspace_id": "client-workspace-003"},
        )

    assert response.status_code == 200
    assert response.json()["buyer_contacted"] is False
    assert response.json()["campaign_started"] is False
    drafts = response.json()["buyer_outreach_drafts"]
    assert drafts
    for draft in drafts:
        assert draft["manual_use_only"] is True
        assert draft["no_live_send"] is True
        assert draft["no_blast"] is True


def test_cp5_sanitizer_hides_internal_notes_and_provider_payloads():
    with TestClient(app) as client:
        evidence = client.get(
            "/api/v1/client-command/leads/client-lead-memphis-005/buyer-demand-evidence",
            params={"workspace_id": "client-workspace-003"},
        )
        lead_detail = client.get(
            "/api/v1/client-command/leads/client-lead-memphis-005",
            params={"workspace_id": "client-workspace-003"},
        )

    serialized = f"{evidence.json()} {lead_detail.json()}".lower()
    assert "internal_notes" not in serialized
    assert "raw_provider_payload" not in serialized
    assert "provider_config" not in serialized
    assert "internal_prime_governance" not in serialized


def test_cp5_safety_guard_blocks_provider_outbound_and_campaign_actions():
    unsafe = validate_client_safe_text(
        "Send Email, Blast Buyers, Pull Buyer List, Scrape Buyers, Contact Buyer, Market Deal, "
        "Launch Campaign, generate contract, and guarantee profit."
    )
    assert unsafe["allowed"] is False
    assert {
        "email_send",
        "buyer_blast",
        "buyer_scraping",
        "campaign_launch",
        "contract_generation",
        "fake_roi_claim",
    } <= set(unsafe["risk_flags"])
    for blocked in [
        "buyer_blast",
        "campaign_launch",
        "buyer_scraping",
        "sms_send",
        "email_send",
        "voice_call",
        "skip_trace_provider_call",
        "dnc_check_provider_call",
        "provider_sync",
        "autonomous_fulfillment",
    ]:
        assert blocked in CLIENT_COMMAND_BLOCKED_ACTIONS


def test_memphis_demo_validates_all_five_cp5_disposition_states():
    expected = {
        "client-lead-memphis-001": "buyer_match_needed",
        "client-lead-memphis-002": "offer_readiness_blocked",
        "client-lead-memphis-003": "buyer_demand_missing",
        "client-lead-memphis-004": "offer_readiness_blocked",
        "client-lead-memphis-005": "ready_for_client_review",
    }
    with TestClient(app) as client:
        responses = {
            lead_id: client.get(
                f"/api/v1/client-command/leads/{lead_id}/disposition-readiness",
                params={"workspace_id": "client-workspace-003"},
            )
            for lead_id in expected
        }

    for lead_id, status in expected.items():
        assert responses[lead_id].status_code == 200
        body = responses[lead_id].json()["disposition_readiness"]
        assert body["readiness_status"] == status
        assert body["no_buyer_contacted"] is True
        assert body["no_campaign_started"] is True
