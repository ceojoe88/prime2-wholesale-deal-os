from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def test_mobile_overview_and_routes_render():
    with TestClient(app) as client:
        overview = client.get("/api/v1/mobile")
        today = client.get("/api/v1/mobile/today")
        calls = client.get("/api/v1/mobile/calls")
        approvals = client.get("/api/v1/mobile/approvals")
        briefing = client.get("/api/v1/mobile/briefing")
        buyers = client.get("/api/v1/mobile/buyers")
        documents = client.get("/api/v1/mobile/documents")

    assert overview.status_code == 200
    assert today.status_code == 200
    assert calls.status_code == 200
    assert approvals.status_code == 200
    assert briefing.status_code == 200
    assert buyers.status_code == 200
    assert documents.status_code == 200
    body = overview.json()
    assert body["mobile_safety"]["live_outreach_from_mobile_allowed"] is False
    assert body["mobile_safety"]["contract_execution_allowed"] is False


def test_quick_call_outcome_records_field_result_without_live_call():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/mobile/calls/outcomes",
            json={
                "lead_id": "lead-002",
                "contact_result": "motivated",
                "motivation_notes": "Seller asked for a repair-backed explanation.",
                "seller_temperature": 82,
                "operator_notes": "Mobile field note only.",
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["call_outcome"]["contact_result"] == "motivated"
    assert body["call_outcome"]["live_call_recorded"] is False
    assert body["call_outcome"]["live_outreach_allowed"] is False
    assert body["call_outcome"]["escalation_created"] is True


def test_quick_dnc_mark_blocks_outreach_eligibility():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/mobile/dnc",
            json={"lead_id": "lead-004", "notes": "Seller requested no further contact."},
        )
        detail = client.get("/api/v1/mobile/leads/lead-004")

    assert response.status_code == 200
    body = response.json()
    assert body["call_outcome"]["do_not_contact"] is True
    assert body["call_outcome"]["outreach_eligibility_status"] == "blocked_do_not_contact"
    assert detail.json()["outreach_eligibility"]["eligible"] is False
    assert "do_not_contact_recorded" in detail.json()["outreach_eligibility"]["blocked_reasons"]


def test_offline_draft_sync_is_idempotent_and_does_not_execute_action():
    payload = {
        "draft_type": "quick_seller_note",
        "source_record_type": "lead",
        "source_record_id": "lead-005",
        "payload": {"note": "Owner captured a field draft."},
        "idempotency_key": "test-mobile-offline-draft-001",
    }
    with TestClient(app) as client:
        first = client.post("/api/v1/mobile/offline-drafts", json=payload)
        second = client.post("/api/v1/mobile/offline-drafts", json=payload)

    assert first.status_code == 200
    assert first.json()["action_executed"] is False
    assert first.json()["provider_called"] is False
    assert second.json()["idempotent_replay"] is True
    assert second.json()["action_executed"] is False


def test_quick_approval_cannot_bypass_required_gates():
    with TestClient(app) as client:
        blocked = client.post(
            "/api/v1/mobile/approvals/quick-check",
            json={
                "approval_type": "seller_follow_up_review",
                "source_record_type": "lead",
                "source_record_id": "lead-001",
                "safety_status": "passed",
                "dry_run_receipt_id": "",
                "provider_readiness_status": "ready",
                "idempotency_key": "test-mobile-approval-blocked",
                "owner_approval_recorded": True,
            },
        )
        ready_review = client.post(
            "/api/v1/mobile/approvals/quick-check",
            json={
                "approval_type": "seller_follow_up_review",
                "source_record_type": "lead",
                "source_record_id": "lead-001",
                "safety_status": "passed",
                "dry_run_receipt_id": "dry-run-test",
                "provider_readiness_status": "ready",
                "idempotency_key": "test-mobile-approval-ready",
                "owner_approval_recorded": True,
            },
        )

    assert blocked.status_code == 200
    assert "dry_run_receipt_required" in blocked.json()["blocked_reasons"]
    assert blocked.json()["live_action_allowed"] is False
    assert ready_review.status_code == 200
    assert ready_review.json()["approval_status"] == "ready_for_owner_review"
    assert ready_review.json()["approved"] is False
    assert ready_review.json()["live_action_allowed"] is False


def test_mobile_note_safety_flags_unsafe_text_as_capture_only():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/mobile/notes",
            json={
                "note_type": "seller_note",
                "source_record_type": "lead",
                "source_record_id": "lead-001",
                "body": "Owner note says last chance, which must be reviewed.",
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["action_executed"] is False
    assert body["safety_status"] == "needs_owner_review"
    assert "pressure_language" in body["blocked_reasons"]
