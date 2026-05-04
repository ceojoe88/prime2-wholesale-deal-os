from __future__ import annotations

from collections import defaultdict
from sqlalchemy.orm import Session

from app.domain.buyer_demand import sync_buyer_deal_priority
from app.domain.seller_acquisition import offer_packet_gate
from app.models import (
    BuyerDealPriority,
    ContractReadyState,
    Deal,
    NegotiationRecord,
    OfferPacket,
    OfferPositioningRecord,
)
from app.serializers import model_to_dict


CONVERSION_LANGUAGE_PATTERNS = {
    "this will sell today": "false_urgency",
    "last chance": "pressure_tactics",
    "you must sign": "pressure_tactics",
    "sign now": "pressure_tactics",
    "take it or leave it": "pressure_tactics",
    "i have buyers lined up": "fake_buyer_claim",
    "we have buyers lined up": "fake_buyer_claim",
    "we already have a buyer": "fake_buyer_claim",
    "guaranteed buyer": "fake_buyer_claim",
    "guaranteed close": "guaranteed_close_language",
    "guaranteed closing": "guaranteed_close_language",
    "we guarantee close": "guaranteed_close_language",
    "legal advice": "legal_statement",
    "you are legally required": "legal_statement",
    "no attorney needed": "legal_statement",
    "hide the assignment": "misleading_assignment_language",
    "do not mention assignment": "misleading_assignment_language",
    "we are the end buyer no matter what": "misleading_assignment_language",
}

NEGOTIATION_STAGES = {
    "initial",
    "follow-up",
    "negotiating",
    "soft-accepted",
    "verbally accepted",
    "stalled",
}


def validate_conversion_language(content: str) -> dict[str, object]:
    lowered = content.lower()
    flags = sorted(
        {
            flag
            for pattern, flag in CONVERSION_LANGUAGE_PATTERNS.items()
            if pattern in lowered
        }
    )
    return {
        "allowed": not flags,
        "blocked": bool(flags),
        "risk_flags": flags,
        "false_urgency_blocked": "false_urgency" in flags,
        "fake_buyer_claim_blocked": "fake_buyer_claim" in flags,
        "guaranteed_close_blocked": "guaranteed_close_language" in flags,
        "legal_statement_blocked": "legal_statement" in flags,
        "pressure_tactics_blocked": "pressure_tactics" in flags,
        "misleading_assignment_language_blocked": "misleading_assignment_language" in flags,
    }


def readiness_score(record: NegotiationRecord) -> dict[str, object]:
    score = round(
        record.motivation_score * 0.22
        + record.price_alignment * 0.2
        + record.timeline_alignment * 0.16
        + record.trust_level * 0.16
        + record.objection_resolution * 0.14
        + record.contact_consistency * 0.12,
        2,
    )
    if score >= 85 and record.negotiation_stage in {"soft-accepted", "verbally accepted"}:
        level = "contract-ready"
    elif score >= 75:
        level = "high readiness"
    elif score >= 55:
        level = "medium readiness"
    else:
        level = "low readiness"
    return {
        "score": score,
        "readiness_level": level,
        "inputs": {
            "motivation_score": record.motivation_score,
            "price_alignment": record.price_alignment,
            "timeline_alignment": record.timeline_alignment,
            "trust_level": record.trust_level,
            "objection_resolution": record.objection_resolution,
            "contact_consistency": record.contact_consistency,
        },
    }


def sync_negotiation_record(record: NegotiationRecord) -> dict[str, object]:
    content = " ".join(
        [
            record.seller_last_response,
            " ".join(record.seller_objections),
            " ".join(record.emotional_signals),
            record.next_move_recommendation,
        ]
    )
    safety = validate_conversion_language(content)
    score = readiness_score(record)
    record.readiness_score = float(score["score"])
    record.readiness_level = str(score["readiness_level"])
    record.safety_status = "passed" if safety["allowed"] else "blocked"
    record.blocked_reasons = safety["risk_flags"]
    record.draft_only = True
    record.automatic_acceptance_allowed = False
    record.live_negotiation_automation_allowed = False
    record.pressure_tactics_allowed = False
    record.legal_advice_allowed = False
    return {"readiness": score, "safety": safety}


def _latest_offer_packet(deal: Deal) -> OfferPacket | None:
    return deal.offer_packets[0] if deal.offer_packets else None


def _top_buyer_priority(deal: Deal) -> BuyerDealPriority | None:
    priorities = list(deal.buyer_priorities)
    for priority in priorities:
        sync_buyer_deal_priority(priority)
    return sorted(priorities, key=lambda item: item.priority_score, reverse=True)[0] if priorities else None


def _buyer_demand_confirmed(deal: Deal) -> bool:
    priority = _top_buyer_priority(deal)
    return bool(
        priority
        and priority.priority_score >= 85
        and not priority.risk_flags
        and priority.buyer.proof_of_funds_status == "verified"
    )


def _compliance_passed(deal: Deal, packet: OfferPacket | None) -> bool:
    compliance_clear = all(record.status != "needs_review" for record in deal.compliance_records)
    return bool((packet is None or packet.compliance_guard_passed) and compliance_clear)


def _profit_control_validated(deal: Deal, packet: OfferPacket | None) -> bool:
    buyer_margin = deal.arv - deal.repairs - deal.buyer_costs - deal.buyer_purchase_price
    spread_valid = deal.projected_assignment_fee >= deal.target_assignment_fee
    margin_valid = buyer_margin >= deal.buyer_desired_profit
    packet_gate = offer_packet_gate(deal, packet) if packet else {"can_prepare": False}
    return bool(spread_valid and margin_valid and (packet_gate["can_prepare"] if packet else True))


def offer_conversion_gate(state: ContractReadyState) -> dict[str, object]:
    deal = state.deal
    packet = _latest_offer_packet(deal)
    negotiation = state.negotiation_record
    reasons: list[str] = []
    underwriting_complete = bool(
        deal.arv > 0
        and deal.repairs > 0
        and deal.max_seller_offer > 0
        and (packet.underwriting_complete if packet else True)
    )
    profit_validated = _profit_control_validated(deal, packet)
    buyer_demand = _buyer_demand_confirmed(deal)
    compliance_passed = _compliance_passed(deal, packet)
    no_risks = not deal.risk_flags
    seller_ready = bool(
        negotiation
        and negotiation.readiness_level in {"high readiness", "contract-ready"}
        and negotiation.safety_status != "blocked"
    )

    if not underwriting_complete:
        reasons.append("underwriting_not_complete")
    if not profit_validated:
        reasons.append("profit_control_not_validated")
    if not buyer_demand:
        reasons.append("buyer_demand_not_confirmed")
    if not compliance_passed:
        reasons.append("compliance_not_passed")
    if not no_risks:
        reasons.append("risk_flags_present")
    if not seller_ready:
        reasons.append("seller_readiness_not_high")
    if not state.owner_approval_recorded:
        reasons.append("owner_approval_not_recorded")
    if state.executable_contract_generated:
        reasons.append("executable_contract_generated")
    if state.contract_execution_allowed:
        reasons.append("contract_execution_enabled")
    if state.legal_advice_provided:
        reasons.append("legal_advice_provided")
    if state.automatic_acceptance_allowed:
        reasons.append("automatic_acceptance_enabled")
    if state.live_negotiation_automation_allowed:
        reasons.append("live_negotiation_automation_enabled")

    return {
        "can_mark_contract_ready": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "underwriting_complete": underwriting_complete,
        "profit_control_validated": profit_validated,
        "buyer_demand_confirmed": buyer_demand,
        "compliance_passed": compliance_passed,
        "no_risk_flags": no_risks,
        "seller_readiness_high": seller_ready,
        "owner_approval_recorded": state.owner_approval_recorded,
        "contract_execution_allowed": False,
        "executable_contract_generation_allowed": False,
        "legal_advice_allowed": False,
        "automatic_acceptance_allowed": False,
    }


def acceleration_recommendations(state: ContractReadyState) -> list[str]:
    gate = offer_conversion_gate(state)
    negotiation = state.negotiation_record
    if gate["can_mark_contract_ready"]:
        return ["move to verbal agreement", "prepare external attorney/title drafting request"]
    actions = []
    reasons = set(gate["blocked_reasons"])
    if "seller_readiness_not_high" in reasons and negotiation:
        if "price" in " ".join(negotiation.seller_objections).lower():
            actions.append("handle objection X")
            actions.append("adjust price within safe range")
        elif negotiation.negotiation_stage == "stalled":
            actions.append("send updated offer explanation")
        else:
            actions.append("hold position")
    if "buyer_demand_not_confirmed" in reasons:
        actions.append("confirm buyer demand before contract-ready state")
    if "profit_control_not_validated" in reasons or "risk_flags_present" in reasons:
        actions.append("disengage")
    if "compliance_not_passed" in reasons:
        actions.append("resolve compliance blocker")
    if "owner_approval_not_recorded" in reasons:
        actions.append("request owner approval review")
    return list(dict.fromkeys(actions or ["hold position"]))


def sync_contract_ready_state(state: ContractReadyState) -> dict[str, object]:
    if state.negotiation_record:
        sync_negotiation_record(state.negotiation_record)
    gate = offer_conversion_gate(state)
    state.underwriting_complete = bool(gate["underwriting_complete"])
    state.profit_control_validated = bool(gate["profit_control_validated"])
    state.buyer_demand_confirmed = bool(gate["buyer_demand_confirmed"])
    state.compliance_passed = bool(gate["compliance_passed"])
    state.no_risk_flags = bool(gate["no_risk_flags"])
    state.seller_readiness_high = bool(gate["seller_readiness_high"])
    state.blocked_reasons = gate["blocked_reasons"]
    state.projected_assignment_fee = state.deal.projected_assignment_fee
    state.fastest_path_to_contract = acceleration_recommendations(state)
    state.contract_ready = bool(gate["can_mark_contract_ready"])
    state.ready_for_external_drafting = state.contract_ready
    state.seller_likely_to_sign = state.contract_ready or state.seller_readiness_high
    state.numbers_locked = state.contract_ready or (
        state.profit_control_validated and state.offer_positioning is not None
    )
    state.negotiation_stabilized = bool(
        state.negotiation_record
        and state.negotiation_record.negotiation_stage
        in {"soft-accepted", "verbally accepted"}
    )
    state.readiness_status = "contract_ready" if state.contract_ready else "blocked"
    state.draft_only = True
    state.external_attorney_title_drafting_required = True
    state.executable_contract_generated = False
    state.contract_execution_allowed = False
    state.legal_advice_provided = False
    state.automatic_acceptance_allowed = False
    state.live_negotiation_automation_allowed = False
    return gate


def offer_positioning_summary(positioning: OfferPositioningRecord) -> dict[str, object]:
    safety = validate_conversion_language(
        " ".join(
            [
                positioning.negotiation_notes,
                str(positioning.justification_summary),
                " ".join(positioning.seller_pain_alignment),
            ]
        )
    )
    positioning.safety_status = "passed" if safety["allowed"] else "blocked"
    positioning.blocked_reasons = safety["risk_flags"]
    positioning.draft_only = True
    positioning.pressure_tactics_allowed = False
    positioning.legal_advice_allowed = False
    return {
        **model_to_dict(positioning),
        "safety_result": safety,
        "contract_execution_allowed": False,
        "legal_advice_allowed": False,
    }


def negotiation_summary(record: NegotiationRecord) -> dict[str, object]:
    sync_negotiation_record(record)
    return {
        **model_to_dict(record),
        "readiness": readiness_score(record),
        "contract_execution_allowed": False,
        "automatic_acceptance_allowed": False,
        "live_negotiation_automation_allowed": False,
    }


def contract_ready_summary(state: ContractReadyState) -> dict[str, object]:
    gate = sync_contract_ready_state(state)
    return {
        **model_to_dict(state),
        "conversion_gate": gate,
        "contract_ready_state_note": "Ready for external attorney/title drafting only; no contract is generated or executed.",
        "contract_execution_allowed": False,
        "executable_contract_generated": False,
        "legal_advice_provided": False,
        "automatic_acceptance_allowed": False,
    }


def offer_conversion_dashboard(session: Session) -> dict[str, object]:
    positionings = session.query(OfferPositioningRecord).all()
    negotiations = session.query(NegotiationRecord).all()
    states = session.query(ContractReadyState).all()
    for record in negotiations:
        sync_negotiation_record(record)
    for state in states:
        sync_contract_ready_state(state)

    contract_ready = [state for state in states if state.contract_ready]
    high_readiness = [
        record
        for record in negotiations
        if record.readiness_level in {"high readiness", "contract-ready"}
    ]
    stalled = [record for record in negotiations if record.negotiation_stage == "stalled"]
    price_adjustment = [
        record
        for record in negotiations
        if any("price" in objection.lower() for objection in record.seller_objections)
        and record.counter_offer
    ]
    at_risk = [state for state in states if state.blocked_reasons]
    by_deal: dict[str, list[ContractReadyState]] = defaultdict(list)
    for state in states:
        by_deal[state.deal_id].append(state)

    return {
        "offer_positioning_records": [
            offer_positioning_summary(positioning) for positioning in positionings
        ],
        "negotiation_records": [negotiation_summary(record) for record in negotiations],
        "contract_ready_states": [contract_ready_summary(state) for state in states],
        "contract_ready_deals": [contract_ready_summary(state) for state in contract_ready],
        "high_readiness_sellers": [negotiation_summary(record) for record in high_readiness],
        "stalled_negotiations": [negotiation_summary(record) for record in stalled],
        "deals_needing_price_adjustment": [
            negotiation_summary(record) for record in price_adjustment
        ],
        "deals_at_risk": [contract_ready_summary(state) for state in at_risk],
        "fastest_path_to_contract": [
            {
                "deal_id": deal_id,
                "state_id": sorted(states, key=lambda item: len(item.blocked_reasons))[0].id,
                "actions": sorted(states, key=lambda item: len(item.blocked_reasons))[0].fastest_path_to_contract,
            }
            for deal_id, states in by_deal.items()
        ],
        "projected_10k_contracts_ready": [
            contract_ready_summary(state)
            for state in contract_ready
            if state.projected_assignment_fee >= state.deal.target_assignment_fee
        ],
        "contract_execution_allowed": False,
        "executable_contract_generation_allowed": False,
        "legal_advice_allowed": False,
        "automatic_acceptance_allowed": False,
    }
