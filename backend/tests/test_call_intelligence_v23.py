from __future__ import annotations

from uuid import uuid4

from fastapi.testclient import TestClient

from app.domains.ai_gateway.ai_safety import validate_ai_request_type
from app.domains.call_intelligence.extractor import extract_call_intelligence
from app.domains.worker_runtime.worker import worker_safety_guard
from app.main import app


def test_manual_call_note_analysis_extracts_structured_signals():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/call-intelligence/analyze",
            json={
                "lead_id": "lead-002",
                "input_type": "manual_call_notes",
                "transcript_text": (
                    "Owner said the roof and HVAC need repairs, wants to sell soon, "
                    "is asking $165,000, and asked us to call me back next week."
                ),
                "use_ai_assist": False,
            },
        )

    assert response.status_code == 200
    body = response.json()
    session = body["session"]
    assert session["asking_price"] == 165000
    assert "roof" in session["repair_clues"]
    assert session["urgency_timeline"] in {"soon", "next week"}
    assert body["draft_only"] is True
    assert body["live_response_generated"] is False


def test_dnc_detection_blocks_outreach_eligibility():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/call-intelligence/analyze",
            json={
                "lead_id": "lead-009",
                "input_type": "pasted_transcript",
                "transcript_text": "Please do not contact me again or call this number.",
                "use_ai_assist": False,
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["session"]["do_not_contact_detected"] is True
    assert body["outreach_eligibility"]["eligible"] is False
    assert "do_not_contact_recorded" in body["outreach_eligibility"]["blocked_reasons"]


def test_legal_question_escalates_to_compliance_review():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/call-intelligence/analyze",
            json={
                "lead_id": "lead-004",
                "transcript_text": "Seller asked what the contract legally means and whether an attorney is needed.",
                "use_ai_assist": False,
            },
        )

    assert response.status_code == 200
    session = response.json()["session"]
    assert session["compliance_escalation_created"] is True
    assert "attorney" in session["legal_compliance_red_flags"]
    assert "compliance" in session["next_best_action"]


def test_objections_create_safe_draft_only_responses():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/call-intelligence/analyze",
            json={
                "lead_id": "lead-005",
                "transcript_text": "The seller said the price is too low and wants family input before discussing assignment.",
                "use_ai_assist": False,
            },
        )

    assert response.status_code == 200
    objections = response.json()["objections"]
    objection_types = {objection["objection_type"] for objection in objections}
    assert "price_too_low" in objection_types
    assert "wants_family_input" in objection_types
    assert any(objection["draft_only"] and not objection["live_response_allowed"] for objection in objections)


def test_score_deltas_are_deterministic_and_explainable():
    extracted = extract_call_intelligence(
        "Seller is motivated, wants a quick cash as-is option, and has roof repairs."
    )
    assert extracted["motivation_score_delta"] > 0
    assert extracted["confidence_score"] >= 45
    assert extracted["quality_items"]["captured_property_condition"] is True
    assert extracted["transcript_basis"]["condition"]


def test_ai_gateway_allows_call_intelligence_extraction_safely():
    assert validate_ai_request_type("call_intelligence_extraction")["allowed"] is True
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/call-intelligence/analyze",
            json={
                "lead_id": "lead-010",
                "transcript_text": "Seller wants to sell soon, asked about repairs, and requested owner review.",
                "use_ai_assist": True,
            },
        )

    assert response.status_code == 200
    session = response.json()["session"]
    assert session["deterministic_fallback_used"] is True
    assert session["live_response_generated"] is False


def test_worker_call_analysis_job_does_not_trigger_live_outreach():
    assert worker_safety_guard("call_analysis")["allowed"] is True
    with TestClient(app) as client:
        created = client.post(
            "/api/v1/worker/jobs",
            json={
                "job_type": "call_analysis",
                "source_record": "call-intel-001",
                "idempotency_key": f"call-analysis-{uuid4().hex}",
            },
        )
        run = client.post(f"/api/v1/worker/jobs/{created.json()['job_id']}/run")

    assert created.status_code == 200
    assert run.status_code == 200
    assert run.json()["provider_called"] is False
    assert run.json()["real_world_action_taken"] is False
    assert run.json()["live_action_allowed"] is False

