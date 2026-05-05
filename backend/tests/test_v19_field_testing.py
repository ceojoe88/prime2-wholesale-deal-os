from __future__ import annotations

from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def _csv(rows: list[dict[str, object]]) -> str:
    fields = [
        "owner_name",
        "owner_phone",
        "owner_email",
        "property_address",
        "property_city",
        "property_state",
        "property_zip",
        "mailing_address",
        "lead_source",
        "lead_type",
        "property_type",
        "beds",
        "baths",
        "sqft",
        "year_built",
        "estimated_value",
        "estimated_equity",
        "mortgage_balance",
        "tax_delinquent_flag",
        "vacant_flag",
        "absentee_owner_flag",
        "probate_flag",
        "inherited_flag",
        "code_violation_flag",
        "pre_foreclosure_flag",
        "tired_landlord_flag",
        "notes",
    ]
    lines = [",".join(fields)]
    for row in rows:
        lines.append(",".join(str(row.get(field, "")) for field in fields))
    return "\n".join(lines)


def _sample_rows(suffix: str) -> list[dict[str, object]]:
    return [
        {
            "owner_name": f"Field Seller {suffix}",
            "owner_phone": f"214555{suffix[-4:]}",
            "owner_email": f"seller-{suffix}@example.test",
            "property_address": f"{suffix[-4:]} V19 Test Ave",
            "property_city": "Dallas",
            "property_state": "TX",
            "property_zip": "75216",
            "mailing_address": "PO Box 19",
            "lead_source": "vacant",
            "lead_type": "vacant high equity",
            "property_type": "single_family",
            "beds": 3,
            "baths": 2,
            "sqft": 1400,
            "year_built": 1965,
            "estimated_value": 240000,
            "estimated_equity": 120000,
            "mortgage_balance": 80000,
            "vacant_flag": "true",
            "absentee_owner_flag": "true",
            "notes": "Fresh field-test row",
        },
        {
            "owner_name": f"Bad Seller {suffix}",
            "owner_phone": f"972555{suffix[-4:]}",
            "property_address": "",
            "property_city": "Dallas",
            "property_state": "TX",
            "property_zip": "75216",
            "lead_source": "vacant",
            "lead_type": "vacant",
            "notes": "Missing property address should block commit",
        },
    ]


def test_csv_preview_validates_rows_and_blocks_bad_rows():
    suffix = uuid4().hex
    with TestClient(app) as client:
        response = client.post(
            "/api/lead-imports/preview",
            content=_csv(_sample_rows(suffix)),
            headers={"content-type": "text/csv"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["row_count"] == 2
    assert body["approved_row_count"] == 1
    assert body["blocked_row_count"] == 1
    assert any(
        "missing_property_address" in row["blocked_reasons"] for row in body["rows"]
    )
    assert body["live_outreach_allowed"] is False
    assert body["bulk_outreach_allowed"] is False


def test_approved_rows_commit_only_once():
    suffix = uuid4().hex
    with TestClient(app) as client:
        preview = client.post(
            "/api/lead-imports/preview",
            content=_csv(_sample_rows(suffix)),
            headers={"content-type": "text/csv"},
        ).json()
        first = client.post(f"/api/lead-imports/{preview['id']}/commit")
        second = client.post(f"/api/lead-imports/{preview['id']}/commit")

    assert first.status_code == 200
    assert len(first.json()["committed_rows"]) == 1
    assert first.json()["live_outreach_allowed"] is False
    assert second.status_code == 200
    assert second.json()["committed_rows"] == []
    assert any(row["reason"] == "already_committed" for row in second.json()["skipped_rows"])


def test_import_dedupe_blocks_duplicate_property_owner_phone():
    suffix = uuid4().hex
    rows = _sample_rows(suffix)
    rows[1] = {**rows[0], "owner_name": "Duplicate Seller"}
    with TestClient(app) as client:
        response = client.post(
            "/api/lead-imports/preview",
            content=_csv(rows),
            headers={"content-type": "text/csv"},
        )

    assert response.status_code == 200
    rows = response.json()["rows"]
    assert any("duplicate_property_owner_phone" in row["blocked_reasons"] for row in rows)


def test_lead_qa_scoring_works_and_shows_blocked_reasons():
    with TestClient(app) as client:
        response = client.get("/api/lead-qa")
        detail = client.get("/api/lead-qa/lead-import-001-row-003")

    assert response.status_code == 200
    assert response.json()["call_priority"]
    assert detail.status_code == 200
    assert "missing_property_address" in detail.json()["blocked_reasons"]
    assert detail.json()["live_outreach_allowed"] is False


def test_do_not_contact_blocks_outreach_eligibility():
    with TestClient(app) as client:
        response = client.post(
            "/api/call-outcomes",
            json={
                "lead_id": "lead-002",
                "contact_result": "do_not_contact",
                "motivation_notes": "Seller asked to not be contacted again.",
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["do_not_contact"] is True
    assert body["outreach_eligibility"]["eligible"] is False
    assert "do_not_contact_recorded" in body["outreach_eligibility"]["blocked_reasons"]
    assert body["live_outreach_allowed"] is False


def test_call_outcome_updates_contactability_and_motivation():
    with TestClient(app) as client:
        wrong = client.post(
            "/api/call-outcomes",
            json={"lead_id": "lead-003", "contact_result": "wrong_number"},
        )
        motivated = client.post(
            "/api/call-outcomes",
            json={
                "lead_id": "lead-004",
                "contact_result": "motivated",
                "motivation_notes": "Seller wants an as-is draft explanation.",
                "seller_temperature": 86,
            },
        )
        exceptions = client.get("/api/operator-mode/exceptions")

    assert wrong.status_code == 200
    assert wrong.json()["lead"]["contactability_score"] == 25
    assert motivated.status_code == 200
    assert motivated.json()["escalation_created"] is True
    assert motivated.json()["internal_task_created"] is True
    assert any(
        exception["source_record_id"] == motivated.json()["id"]
        for exception in exceptions.json()["exceptions"]
    )


def test_feedback_loop_compares_prediction_vs_actual_and_recommends_adjustment():
    with TestClient(app) as client:
        response = client.post(
            "/api/feedback-loop",
            json={
                "lead_id": "lead-006",
                "call_outcome_id": "call-outcome-002",
                "source_prediction_type": "predicted_contactability",
                "source_prediction_value": "high contactability",
                "actual_result": "wrong_number",
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["accuracy_score"] < 70
    assert "contactability" in body["recommended_scoring_adjustment"]
    assert body["scoring_adjustment"]["deterministic"] is True
    assert body["scoring_adjustment"]["owner_review_status"] == "pending_review"


def test_field_testing_blocks_unsafe_language_and_live_paths():
    with TestClient(app) as client:
        safety = client.post(
            "/api/field-testing/safety/validate",
            json={"content": "Send All now and guarantee profit with legal advice."},
        )
        dashboard = client.get("/api/field-testing")

    assert safety.status_code == 200
    assert safety.json()["allowed"] is False
    assert "bulk_outreach_language" in safety.json()["risk_flags"]
    assert "guaranteed_profit_language" in safety.json()["risk_flags"]
    assert dashboard.status_code == 200
    assert dashboard.json()["live_outreach_allowed"] is False
    assert dashboard.json()["bulk_outreach_allowed"] is False
    assert dashboard.json()["auto_portal_publish_allowed"] is False


def test_v19_backend_routes_render():
    routes = [
        "/api/lead-imports",
        "/api/lead-imports/lead-import-001",
        "/api/lead-imports/preview",
        "/api/lead-qa",
        "/api/lead-qa/lead-import-001-row-001",
        "/api/call-outcomes",
        "/api/call-outcomes/call-outcome-001",
        "/api/field-testing",
        "/api/field-briefing",
        "/api/feedback-loop",
        "/api/feedback-loop/feedback-001",
        "/api/scoring-adjustments",
    ]
    with TestClient(app) as client:
        for route in routes:
            response = client.get(route)
            assert response.status_code == 200, route
