from fastapi.testclient import TestClient

from app.main import app
from app.seed_data import seed_payload


def test_prime_2_identity_is_consistent_in_internal_surfaces():
    payload = seed_payload()
    assert "Wholesale Prime" not in str(payload)
    assert any(
        briefing["generated_by"] == "Prime 2"
        for briefing in payload["daily_command_briefings"]
    )
    assert any(
        report["generated_by"] == "Prime 2"
        for report in payload["autonomous_daily_operating_reports"]
    )

    with TestClient(app) as client:
        health = client.get("/health")
        hierarchy = client.get("/api/hierarchy")
        command = client.get("/api/command-center")
        autonomy_briefing = client.get("/api/autonomy/daily-briefing")

    assert health.json()["overseer"] == "Prime 2"
    assert hierarchy.json()["overseer"]["name"] == "Prime 2"
    assert command.json()["overseer"] == "Prime 2"
    assert autonomy_briefing.json()["generated_by"] == "Prime 2"


def test_seed_relationships_reference_existing_source_records():
    payload = seed_payload()
    lead_ids = {row["id"] for row in payload["leads"]}
    deal_ids = {row["id"] for row in payload["deals"]}
    buyer_ids = {row["id"] for row in payload["buyers"]}
    buyer_match_ids = {row["id"] for row in payload["buyer_matches"]}
    buyer_interest_ids = {row["id"] for row in payload["buyer_interests"]}
    buyer_priority_ids = {row["id"] for row in payload["buyer_deal_priorities"]}
    buyer_publication_ids = {row["id"] for row in payload["buyer_deal_publications"]}
    seller_interaction_ids = {row["id"] for row in payload["seller_interactions"]}
    offer_packet_ids = {row["id"] for row in payload["offer_packets"]}
    contract_control_ids = {row["id"] for row in payload["contract_controls"]}
    title_handoff_ids = {row["id"] for row in payload["title_handoff_packets"]}
    seller_offer_ids = {row["id"] for row in payload["seller_offer_publications"]}
    assignment_readiness_ids = {
        row["id"] for row in payload["assignment_readiness_records"]
    }
    deal_room_ids = {row["id"] for row in payload["unified_deal_rooms"]}
    evidence_packet_ids = {row["id"] for row in payload["deal_evidence_packets"]}
    offer_positioning_ids = {row["id"] for row in payload["offer_positioning_records"]}
    negotiation_ids = {row["id"] for row in payload["negotiation_records"]}
    contract_ready_ids = {row["id"] for row in payload["contract_ready_states"]}
    title_review_ids = {row["id"] for row in payload["title_review_coordinations"]}
    automation_rule_ids = {row["id"] for row in payload["automation_rules"]}
    scheduler_run_ids = {row["id"] for row in payload["scheduler_runs"]}
    auto_rule_ids = {row["id"] for row in payload["auto_execution_rules"]}
    auto_dry_run_ids = {row["id"] for row in payload["auto_execution_dry_runs"]}
    lead_import_batch_ids = {row["id"] for row in payload["lead_import_batches"]}
    lead_import_row_ids = {row["id"] for row in payload["lead_import_rows"]}
    call_outcome_ids = {row["id"] for row in payload["field_call_outcomes"]}
    feedback_ids = {row["id"] for row in payload["prediction_feedback_records"]}

    for deal in payload["deals"]:
        assert deal["lead_id"] in lead_ids
    for match in payload["buyer_matches"]:
        assert match["deal_id"] in deal_ids
        assert match["buyer_id"] in buyer_ids
    for publication in payload["buyer_deal_publications"]:
        assert publication["deal_id"] in deal_ids
    for interest in payload["buyer_interests"]:
        assert interest["deal_id"] in deal_ids
        assert interest["buyer_id"] in buyer_ids
    for interaction in payload["seller_interactions"]:
        assert interaction["lead_id"] in lead_ids
    for packet in payload["offer_packets"]:
        assert packet["deal_id"] in deal_ids
    for contract in payload["contract_controls"]:
        assert contract["lead_id"] in lead_ids
        assert contract["deal_id"] in deal_ids
        assert contract["offer_packet_id"] in offer_packet_ids
    for packet in payload["title_handoff_packets"]:
        assert packet["contract_control_id"] in contract_control_ids
        assert packet["deal_id"] in deal_ids
    for readiness in payload["assignment_readiness_records"]:
        assert readiness["contract_control_id"] in contract_control_ids
        assert readiness["deal_id"] in deal_ids
        assert readiness["buyer_id"] in buyer_ids
        if readiness.get("buyer_match_id"):
            assert readiness["buyer_match_id"] in buyer_match_ids
        if readiness.get("buyer_interest_id"):
            assert readiness["buyer_interest_id"] in buyer_interest_ids
    for draft in payload["communication_drafts"]:
        if draft.get("seller_interaction_id"):
            assert draft["seller_interaction_id"] in seller_interaction_ids
        if draft.get("buyer_interest_id"):
            assert draft["buyer_interest_id"] in buyer_interest_ids
        if draft.get("title_handoff_packet_id"):
            assert draft["title_handoff_packet_id"] in title_handoff_ids
    for publication in payload["seller_offer_publications"]:
        assert publication["lead_id"] in lead_ids
        assert publication["deal_id"] in deal_ids
        assert publication["offer_packet_id"] in offer_packet_ids
        assert publication["contract_control_id"] in contract_control_ids
    for room in payload["unified_deal_rooms"]:
        assert room["deal_id"] in deal_ids
        assert room["contract_control_id"] in contract_control_ids
        assert room["seller_offer_publication_id"] in seller_offer_ids
        assert room["buyer_deal_publication_id"] in buyer_publication_ids
        if room.get("title_handoff_packet_id"):
            assert room["title_handoff_packet_id"] in title_handoff_ids
        if room.get("assignment_readiness_record_id"):
            assert room["assignment_readiness_record_id"] in assignment_readiness_ids
    for checklist in payload["closing_coordination_checklists"]:
        assert checklist["deal_room_id"] in deal_room_ids
    for blocker in payload["deal_room_blockers"]:
        assert blocker["deal_room_id"] in deal_room_ids
        assert blocker["deal_id"] in deal_ids
    for packet in payload["deal_evidence_packets"]:
        assert packet["deal_room_id"] in deal_room_ids
        assert packet["deal_id"] in deal_ids
    for fee in payload["assignment_fee_attributions"]:
        assert fee["deal_room_id"] in deal_room_ids
        assert fee["deal_id"] in deal_ids
        assert fee["evidence_packet_id"] in evidence_packet_ids
    for priority in payload["buyer_deal_priorities"]:
        assert priority["deal_id"] in deal_ids
        assert priority["buyer_id"] in buyer_ids
    for prep in payload["deal_distribution_preps"]:
        assert prep["deal_id"] in deal_ids
        assert prep["buyer_id"] in buyer_ids
        assert prep["buyer_priority_id"] in buyer_priority_ids
        assert prep["buyer_deal_publication_id"] in buyer_publication_ids
    for positioning in payload["offer_positioning_records"]:
        assert positioning["deal_id"] in deal_ids
        assert positioning["offer_packet_id"] in offer_packet_ids
    for negotiation in payload["negotiation_records"]:
        assert negotiation["deal_id"] in deal_ids
        assert negotiation["offer_positioning_id"] in offer_positioning_ids
        assert negotiation["seller_interaction_id"] in seller_interaction_ids
    for state in payload["contract_ready_states"]:
        assert state["deal_id"] in deal_ids
        assert state["offer_positioning_id"] in offer_positioning_ids
        assert state["negotiation_record_id"] in negotiation_ids
    for review in payload["title_review_coordinations"]:
        assert review["deal_id"] in deal_ids
        assert review["contract_ready_state_id"] in contract_ready_ids
    for packet in payload["review_packet_preps"]:
        assert packet["title_review_coordination_id"] in title_review_ids
        assert packet["deal_id"] in deal_ids
    for run in payload["scheduler_runs"]:
        assert run["rule_id"] in automation_rule_ids
    for attempt in payload["automation_attempts"]:
        assert attempt["run_id"] in scheduler_run_ids
    for task in payload["autonomous_agent_tasks"]:
        assert task["rule_id"] in automation_rule_ids
        assert task["run_id"] in scheduler_run_ids
    for attempt in payload["auto_execution_attempts"]:
        assert attempt["rule_id"] in auto_rule_ids
        if attempt.get("dry_run_id"):
            assert attempt["dry_run_id"] in auto_dry_run_ids
    for row in payload["lead_import_rows"]:
        assert row["batch_id"] in lead_import_batch_ids
        if row.get("committed_lead_id"):
            assert row["committed_lead_id"] in lead_ids
    for review in payload["lead_quality_reviews"]:
        assert review["batch_id"] in lead_import_batch_ids
        assert review["import_row_id"] in lead_import_row_ids
        if review.get("lead_id"):
            assert review["lead_id"] in lead_ids
    for outcome in payload["field_call_outcomes"]:
        assert outcome["lead_id"] in lead_ids
        assert outcome["live_outreach_allowed"] is False
    for feedback in payload["prediction_feedback_records"]:
        if feedback.get("lead_id"):
            assert feedback["lead_id"] in lead_ids
        if feedback.get("deal_id"):
            assert feedback["deal_id"] in deal_ids
        if feedback.get("call_outcome_id"):
            assert feedback["call_outcome_id"] in call_outcome_ids
    for suggestion in payload["scoring_adjustment_suggestions"]:
        assert suggestion["feedback_id"] in feedback_ids
        assert suggestion["deterministic"] is True


def test_seeded_automation_and_provider_paths_remain_guarded():
    payload = seed_payload()

    for rule in payload["automation_rules"]:
        assert rule["autonomy_level"] <= 4
        assert rule["level_5_disabled"] is True
        assert rule["live_action_allowed"] is False
        assert rule["portal_publish_allowed"] is False
        assert rule["contract_execution_allowed"] is False
        assert rule["title_submission_allowed"] is False
        assert rule["payment_collection_allowed"] is False

    for run in payload["scheduler_runs"]:
        assert run["autonomy_level"] <= 4
        assert run["real_world_action_taken"] is False

    for attempt in payload["automation_attempts"]:
        assert attempt["real_world_action_taken"] is False
        if attempt["attempt_status"] == "blocked":
            assert attempt["provider_called"] is False

    for rule in payload["auto_execution_rules"]:
        assert rule["autonomy_level"] <= 4
        assert rule["bulk_send_allowed"] is False
        assert rule["buyer_blast_allowed"] is False
        assert rule["legal_contract_message_allowed"] is False
        assert rule["cold_sms_allowed"] is False

    for item in payload["owner_approval_items"]:
        assert item["owner_required"] is True
        assert item["executed"] is False


def test_all_documented_core_get_routes_are_registered():
    routes = [
        "/api/system/rules",
        "/api/command-center",
        "/api/hierarchy",
        "/api/divisions",
        "/api/divisions/market-intelligence",
        "/api/managers",
        "/api/agents",
        "/api/agents/zip-code-demand-agent",
        "/api/leads",
        "/api/leads/lead-001",
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
        "/api/deals",
        "/api/deals/deal-001",
        "/api/underwriting",
        "/api/profit-control",
        "/api/seller-acquisition",
        "/api/seller-acquisition/lead-001",
        "/api/follow-up-control",
        "/api/offer-packets",
        "/api/offer-packets/packet-001",
        "/api/contract-control",
        "/api/contract-control/contract-001",
        "/api/title-handoff",
        "/api/title-handoff/title-001",
        "/api/assignment-readiness",
        "/api/deal-room",
        "/api/deal-room/deal-room-001",
        "/api/closing-coordination",
        "/api/closing-coordination/blockers",
        "/api/closing-coordination/readiness",
        "/api/deal-evidence",
        "/api/deal-evidence/evidence-001",
        "/api/assignment-fees",
        "/api/assignment-fees/fee-001",
        "/api/buyer-demand",
        "/api/buyer-demand/buyer-001",
        "/api/buyer-priority",
        "/api/deal-distribution",
        "/api/deal-distribution/distribution-001",
        "/api/buyer-acceleration",
        "/api/buyer-acceleration/deal-001",
        "/api/buyer-sequences",
        "/api/buyer-response-router",
        "/api/buyer-velocity",
        "/api/optimization",
        "/api/optimization/patterns",
        "/api/optimization/recommendations",
        "/api/optimization/agent-performance",
        "/api/optimization/lost-deals",
        "/api/optimization/source-quality",
        "/api/revenue-forecast",
        "/api/revenue-forecast/forecast-2026-05",
        "/api/market-scaling",
        "/api/lead-spend-planner",
        "/api/pipeline-value",
        "/api/operator-mode",
        "/api/operator-mode/approvals",
        "/api/operator-mode/exceptions",
        "/api/operator-mode/daily-report",
        "/api/operator-mode/system-trust",
        "/api/operator-mode/settings",
        "/api/production-readiness",
        "/api/audit-exports",
        "/api/audit-exports/audit-export-001",
        "/api/evidence-attachments",
        "/api/provider-readiness",
        "/api/backups",
        "/api/offer-conversion",
        "/api/offer-conversion/deal-001",
        "/api/negotiations",
        "/api/negotiations/negotiation-001",
        "/api/contract-ready",
        "/api/title-review",
        "/api/title-review/title-review-001",
        "/api/review-packets",
        "/api/review-packets/review-packet-001",
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
        "/api/communications",
        "/api/communications/dry-runs",
        "/api/communications/attempts",
        "/api/communications/approvals",
        "/api/communications/comm-draft-001",
        "/api/buyers",
        "/api/buyers/buyer-001",
        "/api/buyer-matches",
        "/api/compliance",
        "/api/daily-briefing",
    ]

    with TestClient(app) as client:
        for route in routes:
            response = client.get(route)
            assert response.status_code == 200, route
