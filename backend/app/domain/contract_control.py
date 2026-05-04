from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import AssignmentReadinessRecord, ContractControl, TitleHandoffPacket
from app.serializers import model_to_dict


CONTRACT_UNSAFE_PATTERNS = {
    "executable_legal_contract_generation": [
        "generate executable contract",
        "create binding contract",
        "ready to sign contract",
        "final legal contract",
        "execute this contract",
    ],
    "legal_advice": [
        "this is legal advice",
        "no attorney needed",
        "you are legally required",
        "ignore title",
    ],
    "live_outreach": [
        "send sms",
        "send email",
        "call seller",
        "call buyer",
        "email title company",
    ],
    "title_company_submission": [
        "submit to title",
        "send to title company",
        "open escrow now",
        "wire earnest money now",
    ],
    "false_assignment_claims": [
        "assignment is guaranteed",
        "assignment is already approved",
        "buyer will definitely close",
        "assignment allowed no matter what",
    ],
    "hidden_disclosure_language": [
        "hide the assignment",
        "do not disclose assignment",
        "keep the fee hidden",
        "do not mention the spread",
    ],
    "misrepresentation": [
        "pretend to be the end buyer",
        "misrepresent",
        "say we own it already",
        "seller does not need to know",
    ],
    "automatic_contract_status_changes": [
        "automatically mark under contract",
        "auto execute",
        "auto status change",
        "mark assigned automatically",
    ],
}


def validate_contract_language(content: str) -> dict[str, object]:
    text = content.lower()
    flags = [
        category
        for category, phrases in CONTRACT_UNSAFE_PATTERNS.items()
        if any(phrase in text for phrase in phrases)
    ]
    return {
        "allowed": not flags,
        "risk_flags": flags,
        "reason": (
            "Contract-control language is draft-safe."
            if not flags
            else "Unsafe contract/title language blocked."
        ),
    }


def _buyer_margin(deal) -> int:
    return deal.arv - deal.repairs - deal.buyer_costs - deal.buyer_purchase_price


def contract_prep_gate(contract: ContractControl) -> dict[str, object]:
    reasons: list[str] = []
    deal = contract.deal
    packet = contract.offer_packet

    if packet is None:
        reasons.append("missing_offer_packet_record")
    elif not packet.packet_prep_allowed or packet.approval_status != "owner_approved_draft_ready":
        reasons.append("offer_packet_not_approved")

    if not contract.seller_accepted_terms:
        reasons.append("seller_accepted_terms_missing")
    if deal.arv <= 0:
        reasons.append("missing_arv")
    if deal.repairs <= 0:
        reasons.append("missing_repair_estimate")

    buyer_margin = _buyer_margin(deal)
    if buyer_margin < deal.buyer_desired_profit:
        reasons.append("buyer_margin_not_protected")
    if deal.projected_assignment_fee <= 0:
        reasons.append("assignment_spread_not_calculated")
    if contract.compliance_review_status != "approved" or (
        packet is not None and not packet.compliance_guard_passed
    ):
        reasons.append("compliance_guard_not_passed")
    if contract.owner_approval_status != "approved":
        reasons.append("owner_approval_not_recorded")

    return {
        "can_prepare": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "buyer_margin": buyer_margin,
        "projected_assignment_fee": deal.projected_assignment_fee,
        "draft_only": True,
        "contract_execution_allowed": False,
        "live_sending_allowed": False,
        "title_submission_allowed": False,
    }


def update_contract_prep_gate(contract: ContractControl) -> None:
    gate = contract_prep_gate(contract)
    contract.blocked_reasons = gate["blocked_reasons"]
    contract.contract_prep_allowed = gate["can_prepare"]


def title_handoff_summary(packet: TitleHandoffPacket) -> dict[str, object]:
    return {
        **model_to_dict(packet),
        "no_title_company_submission": True,
        "title_submission_allowed": False,
        "submitted_to_title": False,
        "legal_advice_provided": False,
    }


def assignment_readiness_gate(record: AssignmentReadinessRecord) -> dict[str, object]:
    reasons: list[str] = []
    contract = record.contract_control
    buyer = record.buyer

    if contract is None:
        reasons.append("missing_contract_control")
    elif not contract.contract_prep_allowed:
        reasons.append("contract_control_not_ready")

    if contract is None or not contract.assignment_allowed_flag or not record.assignment_allowed_confirmed:
        reasons.append("assignment_allowed_not_confirmed")
    if record.buyer_match is None:
        reasons.append("buyer_match_missing")
    if buyer is None or record.buyer_pof_status != "verified" or buyer.proof_of_funds_status != "verified":
        reasons.append("buyer_pof_not_verified")
    if record.buyer_interest is None:
        reasons.append("buyer_interest_missing")
    if (
        contract is None
        or contract.compliance_review_status != "approved"
        or not record.compliance_review_passed
    ):
        reasons.append("compliance_review_not_passed")
    if (
        contract is None
        or contract.owner_approval_status != "approved"
        or not record.owner_approval_recorded
    ):
        reasons.append("owner_approval_not_recorded")

    return {
        "assignment_ready": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "draft_only": True,
        "contract_execution_allowed": False,
        "title_submission_allowed": False,
    }


def update_assignment_readiness(record: AssignmentReadinessRecord) -> None:
    gate = assignment_readiness_gate(record)
    record.blocked_reasons = gate["blocked_reasons"]
    record.assignment_ready = gate["assignment_ready"]
    record.readiness_status = "assignment_ready" if gate["assignment_ready"] else "blocked"


def contract_title_dashboard(session: Session) -> dict[str, object]:
    contracts = session.query(ContractControl).all()
    title_packets = session.query(TitleHandoffPacket).all()
    readiness_records = session.query(AssignmentReadinessRecord).all()

    for contract in contracts:
        update_contract_prep_gate(contract)
    for record in readiness_records:
        update_assignment_readiness(record)

    blocked_contracts = [
        {"contract_id": contract.id, "deal_id": contract.deal_id, "blocked_reasons": contract.blocked_reasons}
        for contract in contracts
        if contract.blocked_reasons
    ]
    missing_items = []
    for contract in contracts:
        missing = []
        if contract.owner_approval_status != "approved":
            missing.append("owner_approval")
        if contract.compliance_review_status != "approved":
            missing.append("compliance_review")
        if not contract.title_company_preference:
            missing.append("title_company_preference")
        if contract.required_documents_checklist:
            missing.extend(
                item
                for item in contract.required_documents_checklist
                if item.lower().startswith("missing")
            )
        if missing:
            missing_items.append({"contract_id": contract.id, "missing_items": missing})

    return {
        "contracts_in_prep": [
            model_to_dict(contract)
            for contract in contracts
            if contract.contract_status in {"prep_review", "draft_prep_ready"}
        ],
        "title_handoff_packets": [title_handoff_summary(packet) for packet in title_packets],
        "assignment_ready_deals": [
            model_to_dict(record) for record in readiness_records if record.assignment_ready
        ],
        "blocked_contract_prep_reasons": blocked_contracts,
        "missing_approval_compliance_title_items": missing_items,
        "buyer_pof_gaps": [
            model_to_dict(record)
            for record in readiness_records
            if record.buyer_pof_status != "verified"
        ],
        "draft_only": True,
        "live_sending_allowed": False,
        "title_submission_allowed": False,
        "contract_execution_allowed": False,
    }
