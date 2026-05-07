from __future__ import annotations

from fastapi.testclient import TestClient

from app.domains.client_command.safety import (
    CLIENT_COMMAND_BLOCKED_ACTIONS,
    validate_client_safe_text,
)
from app.main import app


def test_cp3_acquisition_brief_generation_is_deterministic():
    with TestClient(app) as client:
        first = client.get(
            "/api/v1/client-command/leads/client-lead-001/acquisition-brief",
            params={"workspace_id": "client-workspace-001"},
        )
        second = client.get(
            "/api/v1/client-command/leads/client-lead-001/acquisition-brief",
            params={"workspace_id": "client-workspace-001"},
        )

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["brief"]["recommended_call_objective"] == second.json()["brief"]["recommended_call_objective"]
    assert first.json()["brief"]["manager_name"] == "Acquisition Manager"
    assert first.json()["brief"]["client_safe"] is True


def test_cp3_question_plan_reflects_missing_data():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/client-command/leads/client-lead-003/question-plan",
            params={"workspace_id": "client-workspace-001"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["question_plan"]["plan_status"] == "needs_review"
    tied_fields = {question["tied_missing_data_key"] for question in body["questions"]}
    assert "property_address_summary" in tied_fields
    assert "contact_channels_present" in tied_fields


def test_cp3_follow_up_drafts_are_manual_use_only_and_no_live_send():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/client-command/leads/client-lead-001/follow-up-drafts",
            params={"workspace_id": "client-workspace-001"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["outbound_provider_actions_allowed"] is False
    assert body["follow_up_drafts"]
    for draft in body["follow_up_drafts"]:
        assert draft["manual_use_only"] is True
        assert draft["no_live_send"] is True


def test_cp3_appointment_readiness_blocks_missing_contact_motivation_and_condition_data():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/client-command/leads/client-lead-003/appointment-readiness",
            params={"workspace_id": "client-workspace-001"},
        )

    review = response.json()["appointment_readiness"]
    assert response.status_code == 200
    assert review["appointment_ready"] is False
    assert review["requires_human_review"] is True
    assert {"seller_motivation", "phone_or_email", "asking_price_or_expectation"} <= set(
        review["missing_requirements"]
    )


def test_cp4_evidence_packet_enforces_workspace_isolation():
    with TestClient(app) as client:
        allowed = client.get(
            "/api/v1/client-command/leads/client-lead-001/deal-evidence-packet",
            params={"workspace_id": "client-workspace-001"},
        )
        denied = client.get(
            "/api/v1/client-command/leads/client-lead-001/deal-evidence-packet",
            params={"workspace_id": "client-workspace-002"},
        )

    assert allowed.status_code == 200
    assert allowed.json()["evidence_packet"]["workspace_id"] == "client-workspace-001"
    assert denied.status_code == 404


def test_cp4_evidence_packet_tracks_missing_evidence():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/client-command/leads/client-lead-002/deal-evidence-packet",
            params={"workspace_id": "client-workspace-001"},
        )

    packet = response.json()["evidence_packet"]
    assert response.status_code == 200
    assert packet["evidence_status"] == "missing_evidence"
    assert packet["missing_evidence_count"] > 0
    assert "repair_note" in packet["required_evidence_summary"]


def test_cp4_underwriting_blocks_missing_arv_or_repair_estimate():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/client-command/leads/client-lead-002/underwriting-review",
            params={"workspace_id": "client-workspace-001"},
        )

    review = response.json()["underwriting_review"]
    assert response.status_code == 200
    assert review["arv_estimate"] is None
    assert review["repair_estimate"] is None
    assert review["max_allowable_offer"] is None
    assert review["requires_human_review"] is True


def test_cp4_mao_and_offer_scenario_calculations_are_deterministic():
    with TestClient(app) as client:
        first = client.get(
            "/api/v1/client-command/leads/client-lead-001/underwriting-review",
            params={"workspace_id": "client-workspace-001"},
        )
        second = client.get(
            "/api/v1/client-command/leads/client-lead-001/underwriting-review",
            params={"workspace_id": "client-workspace-001"},
        )

    review = first.json()["underwriting_review"]
    assert first.status_code == 200
    assert second.status_code == 200
    assert review["max_allowable_offer"] == 106600
    assert review["conservative_offer"] == 95940
    assert review["standard_offer"] == 106600
    assert review["aggressive_offer"] == 111930
    assert first.json()["offer_scenarios"][0]["underwriting_review_id"] == review["id"]


def test_cp4_offer_readiness_blocks_low_confidence_or_missing_evidence():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/client-command/leads/client-lead-002/offer-readiness",
            params={"workspace_id": "client-workspace-001"},
        )

    gate = response.json()["offer_readiness"]
    assert response.status_code == 200
    assert gate["readiness_status"] in {"evidence_missing", "underwriting_review_needed", "blocked"}
    assert gate["can_present_offer"] is False
    assert "arv_estimate_missing" in gate["block_reasons"]


def test_cp4_offer_readiness_never_generates_contract_or_sends_offer():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/client-command/leads/client-lead-001/offer-readiness",
            params={"workspace_id": "client-workspace-001"},
        )

    gate = response.json()["offer_readiness"]
    assert response.status_code == 200
    assert gate["no_contract_generated"] is True
    assert gate["no_offer_sent"] is True


def test_cp4_sanitizer_hides_internal_notes_and_provider_payloads():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/client-command/leads/client-lead-001/deal-evidence-packet",
            params={"workspace_id": "client-workspace-001"},
        )

    serialized = str(response.json()).lower()
    assert "internal_notes" not in serialized
    assert "raw_provider_payload" not in serialized
    assert "provider_config" not in serialized


def test_cp3_cp4_safety_guard_blocks_outbound_provider_and_unsafe_actions():
    unsafe = validate_client_safe_text(
        "Send SMS, pull live comps, generate contract, invoice, sync to provider, and guarantee profit."
    )
    assert unsafe["allowed"] is False
    assert {"sms_send", "live_comp_property_data_pull", "contract_generation", "invoice_action", "provider_sync", "fake_roi_claim"} <= set(
        unsafe["risk_flags"]
    )
    for blocked in [
        "sms_send",
        "email_send",
        "voice_call",
        "skip_trace_provider_call",
        "dnc_check_provider_call",
        "live_comp_property_data_pull",
        "stripe_charge",
        "contract_generation",
        "contract_esignature_send",
        "provider_sync",
        "autonomous_fulfillment",
    ]:
        assert blocked in CLIENT_COMMAND_BLOCKED_ACTIONS
