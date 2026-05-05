from app.seed_data import seed_payload


def test_seed_payload_counts_and_hot_deals():
    payload = seed_payload()
    assert len(payload["divisions"]) == 9
    assert len(payload["agents"]) == 51
    assert len(payload["leads"]) == 30
    assert len(payload["buyers"]) == 10
    assert len(payload["deals"]) == 8
    assert len([deal for deal in payload["deals"] if deal["is_hot_opportunity"]]) == 5
    assert len([deal for deal in payload["deals"] if deal["is_under_contract"]]) == 2
    assert len(payload["compliance_records"]) == 3
    assert len(payload["buyer_matches"]) == 3
    assert len(payload["buyer_deal_publications"]) == 8
    assert len(payload["buyer_interests"]) == 5
    assert len(payload["buyer_demand_profiles"]) == 10
    assert len(payload["buyer_deal_priorities"]) == 12
    assert len(payload["deal_distribution_preps"]) == 4
    assert len(payload["seller_interactions"]) == 6
    assert len(payload["offer_packets"]) == 5
    assert len(payload["offer_positioning_records"]) == 5
    assert len(payload["negotiation_records"]) == 5
    assert len(payload["contract_ready_states"]) == 5
    assert len(payload["title_review_coordinations"]) == 4
    assert len(payload["review_packet_preps"]) == 3
    assert len(payload["automation_rules"]) == 6
    assert len(payload["scheduler_runs"]) == 5
    assert len(payload["automation_attempts"]) == 10
    assert len(payload["autonomous_agent_tasks"]) == 8
    assert len(payload["automation_event_triggers"]) == 5
    assert len(payload["daily_command_briefings"]) == 1
    assert len(payload["autonomy_escalations"]) == 2
    assert len(payload["approved_templates"]) == 5
    assert len(payload["auto_execution_rules"]) == 4
    assert len(payload["auto_execution_dry_runs"]) == 2
    assert len(payload["auto_execution_attempts"]) == 3
    assert len(payload["auto_execution_audit_records"]) == 3
    assert len(payload["buyer_acceleration_records"]) == 3
    assert len(payload["buyer_sequence_preps"]) == 3
    assert len(payload["buyer_response_routes"]) == 4
    assert len(payload["buyer_velocity_profiles"]) == 4
    assert len(payload["outcome_learning_records"]) == 6
    assert len(payload["optimization_recommendations"]) == 4
    assert len(payload["agent_performance_scores"]) == 5
    assert len(payload["scoring_weight_changes"]) == 3
    assert len(payload["revenue_forecast_records"]) == 2
    assert len(payload["deal_probability_records"]) == 4
    assert len(payload["market_scaling_scores"]) == 3
    assert len(payload["lead_spend_plans"]) == 2
    assert len(payload["operator_mode_settings"]) == 2
    assert len(payload["semi_autonomous_command_loop_runs"]) == 1
    assert len(payload["owner_approval_items"]) == 9
    assert len(payload["operator_exception_records"]) == 4
    assert len(payload["autonomous_daily_operating_reports"]) == 1
    assert len(payload["system_trust_scores"]) == 1
    assert len(payload["contract_controls"]) == 5
    assert len(payload["seller_offer_publications"]) == 5
    assert len(payload["seller_portal_responses"]) == 4
    assert len(payload["unified_deal_rooms"]) == 4
    assert len(payload["closing_coordination_checklists"]) == 4
    assert len(payload["deal_room_blockers"]) == 3
    assert len(payload["deal_evidence_packets"]) == 4
    assert len(payload["assignment_fee_attributions"]) == 4
    assert len(payload["title_handoff_packets"]) == 3
    assert len(payload["assignment_readiness_records"]) == 4
    assert len(payload["communication_drafts"]) == 6
    assert len(payload["communication_dry_run_receipts"]) == 4
    assert len(payload["communication_approvals"]) == 2
    assert len(payload["communication_send_attempts"]) == 2


def test_seeded_agents_are_analysis_only():
    payload = seed_payload()
    for agent in payload["agents"]:
        assert "send_sms" in agent["denied_actions"]
        assert "execute_contract" in agent["denied_actions"]
        assert "recommend" in agent["allowed_actions"]
