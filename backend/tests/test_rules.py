from app.domain.rules import system_rules, validate_action


def test_private_operator_only_mode_and_no_portals():
    rules = system_rules()
    assert rules["mode"] == "private_operator_only"
    assert rules["public_signup"] is False
    assert rules["portals"] == {
        "client": False,
        "buyer": "invite_gated_controlled",
        "seller": "invite_gated_controlled_offer_review",
    }
    assert rules["live_outreach"] == {
        "sms": False,
        "email": False,
        "calls": False,
        "buyer_blasts": False,
    }


def test_live_actions_and_buyer_blast_execution_are_blocked():
    for action in ["send_sms", "send_email", "call_seller", "contact_buyer", "buyer_blast_execute"]:
        result = validate_action("Seller Script Agent", action)
        assert result.allowed is False
        assert action in result.risk_flags


def test_legal_advice_and_guarantee_language_is_blocked():
    result = validate_action(
        "Offer Explanation Agent",
        "draft",
        "This is legal advice and a guaranteed profit for everyone.",
    )
    assert result.allowed is False
    assert "legal-advice" in result.reason


def test_agents_and_wholesale_prime_cannot_execute_real_world_actions():
    agent_result = validate_action("MAO Agent", "execute_contract")
    prime_result = validate_action("Wholesale Prime", "prepare_offer_packet", owner_approved=True)
    assert agent_result.allowed is False
    assert prime_result.allowed is False
    assert "Wholesale Prime" in prime_result.reason


def test_owner_approval_and_compliance_review_are_required_for_packet_prep():
    blocked_offer = validate_action("Owner", "prepare_offer_packet")
    allowed_offer = validate_action("Owner", "prepare_offer_packet", owner_approved=True)
    blocked_assignment = validate_action(
        "Owner", "prepare_assignment_packet", owner_approved=True, compliance_reviewed=False
    )
    allowed_assignment = validate_action(
        "Owner", "prepare_assignment_packet", owner_approved=True, compliance_reviewed=True
    )
    assert blocked_offer.allowed is False
    assert blocked_offer.required_approvals == ["owner_approval"]
    assert allowed_offer.allowed is True
    assert blocked_assignment.allowed is False
    assert blocked_assignment.required_approvals == ["compliance_review"]
    assert allowed_assignment.allowed is True
