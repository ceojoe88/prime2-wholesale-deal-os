from __future__ import annotations

from fastapi.testclient import TestClient

from app.domains.real_deal_execution.safety import validate_execution_guidance_text
from app.main import app


def test_first_deal_cockpit_routes_render_and_preserve_boundaries():
    with TestClient(app) as client:
        cockpit = client.get("/api/v1/real-deal-execution")
        calls = client.get("/api/v1/real-deal-execution/calls")
        offers = client.get("/api/v1/real-deal-execution/offers")
        buyers = client.get("/api/v1/real-deal-execution/buyer-validation")
        contract_ready = client.get("/api/v1/real-deal-execution/contract-ready")
        evidence = client.get("/api/v1/real-deal-execution/evidence")
        report = client.get("/api/v1/real-deal-execution/report")

    for response in [cockpit, calls, offers, buyers, contract_ready, evidence, report]:
        assert response.status_code == 200
    boundary = cockpit.json()["safety_boundary"]
    assert boundary["live_outreach_allowed"] is False
    assert boundary["contract_execution_allowed"] is False
    assert boundary["title_submission_allowed"] is False
    assert boundary["owner_final_approver"] is True


def test_execution_batch_creation_and_status_transition():
    with TestClient(app) as client:
        created = client.post(
            "/api/v1/real-deal-execution/batches",
            json={
                "batch_name": "Test 10 lead batch",
                "lead_import_batch_id": "lead-import-001",
                "market_zip_focus": ["75216"],
                "target_assignment_fee": 10000,
                "owner_notes": "Test batch.",
            },
        )
        batch_id = created.json()["id"]
        updated = client.post(
            f"/api/v1/real-deal-execution/batches/{batch_id}/status",
            json={"batch_status": "calling", "owner_notes": "Call queue opened."},
        )
        bad = client.post(
            f"/api/v1/real-deal-execution/batches/{batch_id}/status",
            json={"batch_status": "send_everything"},
        )

    assert created.status_code == 200
    assert created.json()["live_outreach_allowed"] is False
    assert updated.status_code == 200
    assert updated.json()["batch_status"] == "calling"
    assert bad.status_code == 400


def test_call_checklist_generation_and_no_live_calling():
    with TestClient(app) as client:
        response = client.get("/api/v1/real-deal-execution/calls")

    body = response.json()
    checklist_ids = [item["id"] for item in body["guided_call_checklist"]]
    assert "verify_owner_identity" in checklist_ids
    assert "log_dnc_if_requested" in checklist_ids
    assert body["system_calling_enabled"] is False
    assert body["mobile_call_queue_path"] == "/mobile/calls"


def test_offer_decision_board_calculations_and_unsupported_numbers_blocked():
    with TestClient(app) as client:
        response = client.get("/api/v1/real-deal-execution/offers")

    offers = response.json()["offers"]
    assert offers
    for offer in offers:
        assert offer["buyer_max_price"] >= 0
        assert offer["target_assignment_fee"] >= 10000
        if offer["decision_status"] == "needs_data":
            assert offer["blocked_reasons"]
    assert any(offer["recommended_offer_range"]["standard"] >= 0 for offer in offers)


def test_buyer_validation_blocks_weak_or_missing_buyer_margin():
    with TestClient(app) as client:
        response = client.get("/api/v1/real-deal-execution/buyer-validation")

    rows = response.json()["buyer_validations"]
    assert rows
    blocked = [row for row in rows if not row["gate"]["validated"]]
    assert blocked
    assert any(
        set(row["gate"]["blocked_reasons"])
        & {"weak_buyer_margin", "pof_request_unresolved", "no_buyer_demand", "buyer_price_below_needed_spread"}
        for row in blocked
    )


def test_contract_ready_requires_required_gates_and_external_process_only():
    with TestClient(app) as client:
        response = client.get("/api/v1/real-deal-execution/contract-ready")

    rows = response.json()["contract_ready_candidates"]
    assert rows
    for row in rows:
        assert row["contract_document_created"] is False
        assert row["external_drafting_required"] is True
        if not row["gate"]["contract_ready"]:
            assert row["gate"]["blocked_reasons"]


def test_assignment_fee_evidence_validation_blocks_unsupported_10k_claims():
    with TestClient(app) as client:
        response = client.get("/api/v1/real-deal-execution/evidence")

    records = response.json()["evidence_records"]
    assert records
    for record in records:
        assert record["gate"]["client_facing_claim_allowed"] is False
        assert record["gate"]["guarantee_language_allowed"] is False
        if not record["gate"]["evidence_supported"]:
            assert record["missing_proof"]


def test_field_report_creates_advisory_learning_signal_only():
    with TestClient(app) as client:
        response = client.get("/api/v1/real-deal-execution/report")

    body = response.json()
    signal = body["learning_signal"]
    assert signal["source_domain"] == "real_deal_execution"
    assert signal["auto_applied"] is False
    assert signal["owner_review_status"] == "pending_review"
    assert body["safety_boundary"]["guaranteed_profit_claim_allowed"] is False


def test_prime_2_execution_coach_recommendations_are_internal_only():
    with TestClient(app) as client:
        response = client.get("/api/v1/real-deal-execution")

    recommendations = response.json()["prime_2_execution_coach"]
    assert recommendations
    assert all(item["internal_recommendation_only"] is True for item in recommendations)
    assert all(item["safe_text"]["allowed"] is True for item in recommendations)


def test_ai_summary_safety_blocks_unsafe_execution_language():
    unsafe = validate_execution_guidance_text(
        "This is legal advice and a guaranteed profit if you execute contract now."
    )
    safe = validate_execution_guidance_text("Review the seller call notes and prepare an owner-only decision summary.")
    assert unsafe["allowed"] is False
    assert {"legal_guidance", "guaranteed_profit", "contract_execution"} <= set(unsafe["risk_flags"])
    assert safe["allowed"] is True


def test_mobile_call_queue_still_cannot_bypass_gates():
    with TestClient(app) as client:
        mobile_calls = client.get("/api/v1/mobile/calls")
        quick_check = client.post(
            "/api/v1/mobile/approvals/quick-check",
            json={
                "approval_type": "first_deal_call_review",
                "source_record_type": "lead",
                "source_record_id": "lead-001",
                "safety_status": "passed",
                "dry_run_receipt_id": "",
                "provider_readiness_status": "ready",
                "idempotency_key": "test-v31-mobile-gate",
                "owner_approval_recorded": True,
            },
        )

    assert mobile_calls.status_code == 200
    assert mobile_calls.json()["system_calling_enabled"] is False
    assert quick_check.json()["live_action_allowed"] is False
    assert "dry_run_receipt_required" in quick_check.json()["blocked_reasons"]
