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
    assert len(payload["seller_interactions"]) == 6
    assert len(payload["offer_packets"]) == 5
    assert len(payload["contract_controls"]) == 5
    assert len(payload["seller_offer_publications"]) == 5
    assert len(payload["seller_portal_responses"]) == 4
    assert len(payload["unified_deal_rooms"]) == 4
    assert len(payload["closing_coordination_checklists"]) == 4
    assert len(payload["deal_room_blockers"]) == 3
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
