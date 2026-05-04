from app.domain.buyer_matching import score_buyer_match
from app.domain.profit_control import ProfitControlInput, calculate_mao, calculate_profit_control
from app.domain.scoring import calculate_lead_opportunity


def test_lead_scoring_uses_weighted_inputs():
    score = calculate_lead_opportunity(
        {
            "motivation": 90,
            "distress_signals": 80,
            "equity": 85,
            "urgency": 70,
            "contactability": 75,
            "seller_temperature": 85,
            "data_confidence": 80,
            "market_demand": 90,
        }
    )
    assert 82 <= score <= 84


def test_mao_calculation_matches_profit_control_formula():
    assert calculate_mao(200000, 30000, 10000, 35000, 10000) == 115000


def test_middle_man_profit_formulas_and_10k_flag():
    result = calculate_profit_control(
        ProfitControlInput(
            arv=275000,
            estimated_repairs=45000,
            buyer_desired_profit=45000,
            buyer_closing_costs=6000,
            buyer_holding_costs=6000,
            seller_contract_price=151000,
            buyer_purchase_price=166000,
        )
    )
    assert result["max_buyer_purchase_price"] == 173000
    assert result["max_seller_offer"] == 163000
    assert result["projected_assignment_fee"] == 15000
    assert result["is_10k_opportunity"] is True
    assert "buyer_margin_below_desired_profit" not in result["risk_flags"]


def test_buyer_margin_protection_flags_bad_spread():
    result = calculate_profit_control(
        ProfitControlInput(
            arv=260000,
            estimated_repairs=70000,
            buyer_desired_profit=40000,
            buyer_closing_costs=6000,
            buyer_holding_costs=6000,
            seller_contract_price=132000,
            buyer_purchase_price=140000,
        )
    )
    assert result["projected_assignment_fee"] == 8000
    assert result["is_10k_opportunity"] is False
    assert "projected_assignment_fee_below_target" in result["risk_flags"]
    assert "buyer_margin_below_desired_profit" in result["risk_flags"]
    assert "seller_offer_exceeds_margin_safe_max" in result["risk_flags"]


def test_buyer_matching_scores_area_price_type_and_reliability():
    deal = {
        "id": "deal-001",
        "zip_code": "75216",
        "property_type": "single_family",
        "buyer_purchase_price": 166000,
    }
    buyer = {
        "id": "buyer-001",
        "target_zip_codes": ["75216"],
        "max_purchase_price": 210000,
        "property_type": "single_family",
        "proof_of_funds_status": "verified",
        "closing_speed_days": 10,
        "reliability_score": 94,
    }
    match = score_buyer_match(deal, buyer)
    assert match["score"] >= 95
    assert match["draft_only"] is True
    assert "proof_of_funds_verified" in match["match_reasons"]
