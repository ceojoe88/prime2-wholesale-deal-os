from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models import SellerOfferPublication, SellerPortalResponse
from app.serializers import model_to_dict


SANITIZED_SELLER_OFFER_FIELDS = {
    "offer_id",
    "property_address_summary",
    "offer_status",
    "offer_amount",
    "closing_timeline_estimate",
    "inspection_access_next_step",
    "title_company_review_status",
    "document_checklist",
    "owner_operator_contact_placeholder",
    "seller_questions_notes_action",
    "portal_visibility_status",
}

FORBIDDEN_SELLER_PORTAL_KEYS = {
    "buyer",
    "buyer_id",
    "buyer_name",
    "buyer_email",
    "buyer_phone",
    "buyer_list",
    "buyer_data",
    "buyer_purchase_price",
    "buyer_price",
    "assignment_fee",
    "target_assignment_fee",
    "projected_assignment_fee",
    "internal_spread",
    "spread_confidence_score",
    "max_seller_offer",
    "max_buyer_purchase_price",
    "mao",
    "mao_logic",
    "motivation_score",
    "seller_temperature",
    "seller_temperature_score",
    "source_category",
    "lead_source",
    "internal_notes",
    "notes",
    "wholesale_prime_recommendations",
    "compliance_risk",
    "compliance_risk_details",
    "risk_flags",
    "agent_queues",
    "manager_queues",
}

SELLER_PORTAL_UNSAFE_PATTERNS = {
    "pressure_language": [
        "you must sign",
        "sign now",
        "take it or leave it",
        "last chance",
        "do not talk to anyone else",
    ],
    "fake_urgency": [
        "offer expires in minutes",
        "title closes today no matter what",
        "you will lose the house if you wait",
    ],
    "fake_buyer_claim": [
        "we already have a buyer",
        "cash buyer is guaranteed",
        "my buyer will definitely close",
    ],
    "guaranteed_close": [
        "guaranteed closing",
        "we guarantee close",
        "guaranteed cash closing",
    ],
    "legal_advice": [
        "this is legal advice",
        "no attorney needed",
        "you are legally required",
        "ignore title",
    ],
    "misleading_assignment_language": [
        "hide the assignment",
        "do not mention assignment",
        "we are the end buyer no matter what",
        "seller does not need to know",
    ],
    "contract_execution": [
        "click to accept contract",
        "accept this binding agreement",
        "sign the contract now",
        "execute this contract",
    ],
    "live_negotiation_automation": [
        "auto negotiate",
        "automatic counteroffer",
        "automatically accept",
        "auto accept",
    ],
}

VALID_CONTRACT_STATUSES = {
    "prep_review",
    "draft_prep_ready",
    "controlled_review",
    "seller_terms_recorded",
}

ALLOWED_RESPONSE_TYPES = {
    "seller_portal_note",
    "offer_question",
    "appointment_access_preference",
    "document_upload_placeholder",
}


def validate_seller_portal_language(content: str) -> dict[str, object]:
    text = content.lower()
    flags = [
        category
        for category, phrases in SELLER_PORTAL_UNSAFE_PATTERNS.items()
        if any(phrase in text for phrase in phrases)
    ]
    return {
        "allowed": not flags,
        "risk_flags": sorted(set(flags)),
        "reason": (
            "Seller portal language is review-safe."
            if not flags
            else "Unsafe seller portal language blocked."
        ),
    }


def seller_visibility_gate(publication: SellerOfferPublication | None) -> dict[str, object]:
    reasons: list[str] = []
    if publication is None:
        return {"can_show": False, "blocked_reasons": ["missing_seller_offer_publication"]}

    packet = publication.offer_packet
    contract = publication.contract_control

    if not publication.portal_visibility_enabled:
        reasons.append("portal_visibility_not_enabled")
    if packet is None or not packet.packet_prep_allowed or packet.approval_status != "owner_approved_draft_ready":
        reasons.append("offer_packet_not_approved")
    if (
        not publication.compliance_check_passed
        or packet is None
        or not packet.compliance_guard_passed
        or contract is None
        or contract.compliance_review_status != "approved"
    ):
        reasons.append("compliance_check_not_passed")
    if (
        not publication.owner_approval_recorded
        or packet is None
        or not packet.owner_approval_recorded
        or contract is None
        or contract.owner_approval_status != "approved"
    ):
        reasons.append("owner_approval_not_recorded")
    if contract is None or contract.contract_status not in VALID_CONTRACT_STATUSES or not contract.contract_prep_allowed:
        reasons.append("contract_control_status_not_valid")

    safety = validate_seller_portal_language(publication.offer_language)
    publication.offer_language_safety_result = safety
    if not publication.offer_language_safety_passed or not safety["allowed"]:
        reasons.append("offer_language_safety_not_passed")
    if publication.contract_execution_allowed:
        reasons.append("contract_execution_enabled")
    if publication.live_negotiation_automation_allowed:
        reasons.append("live_negotiation_automation_enabled")
    if publication.legal_advice_provided:
        reasons.append("legal_advice_flagged")
    if publication.buyer_data_exposed:
        reasons.append("buyer_data_exposed")
    if publication.internal_profit_logic_exposed:
        reasons.append("internal_profit_logic_exposed")

    return {"can_show": not reasons, "blocked_reasons": sorted(set(reasons))}


def update_seller_visibility_gate(publication: SellerOfferPublication) -> dict[str, object]:
    gate = seller_visibility_gate(publication)
    publication.blocked_reasons = gate["blocked_reasons"]
    if gate["can_show"]:
        publication.visibility_status = "visible"
        publication.visible_at = publication.visible_at or datetime.now(UTC)
    else:
        publication.visibility_status = "blocked"
        publication.visible_at = None
    return gate


def assert_no_seller_portal_leaks(payload: dict[str, object]) -> None:
    leaked_keys = FORBIDDEN_SELLER_PORTAL_KEYS.intersection(payload.keys())
    if leaked_keys:
        raise ValueError(f"Seller portal sanitizer leaked forbidden fields: {sorted(leaked_keys)}")
    if not set(payload.keys()).issubset(SANITIZED_SELLER_OFFER_FIELDS):
        extras = sorted(set(payload.keys()) - SANITIZED_SELLER_OFFER_FIELDS)
        raise ValueError(f"Seller portal sanitizer emitted unexpected fields: {extras}")


def sanitize_seller_offer(publication: SellerOfferPublication) -> dict[str, object]:
    gate = seller_visibility_gate(publication)
    if not gate["can_show"]:
        raise ValueError("Offer is not seller-visible.")

    lead = publication.lead
    sanitized = {
        "offer_id": publication.id,
        "property_address_summary": (
            f"{lead.address}, {lead.city}, {lead.state} {lead.zip_code}"
        ),
        "offer_status": publication.offer_status,
        "offer_amount": publication.offer_amount,
        "closing_timeline_estimate": publication.closing_timeline_estimate,
        "inspection_access_next_step": publication.inspection_access_next_step,
        "title_company_review_status": publication.title_company_review_status,
        "document_checklist": publication.document_checklist,
        "owner_operator_contact_placeholder": publication.operator_contact_placeholder,
        "seller_questions_notes_action": {
            "type": "draft_intake_only",
            "operator_review_required": True,
            "automatic_negotiation_allowed": False,
            "offer_acceptance_execution_allowed": False,
            "document_upload_is_placeholder": True,
        },
        "portal_visibility_status": publication.visibility_status,
    }
    assert_no_seller_portal_leaks(sanitized)
    return sanitized


def response_content(payload: dict[str, object]) -> str:
    return " ".join(
        str(payload.get(key, ""))
        for key in [
            "seller_portal_note",
            "offer_question",
            "appointment_access_preference",
            "document_upload_placeholder",
        ]
    )


def seller_response_is_review_only(response: SellerPortalResponse) -> bool:
    return (
        response.draft_only
        and not response.negotiation_execution_allowed
        and not response.contract_execution_allowed
        and not response.automatic_acceptance_allowed
    )


def seller_portal_rules() -> dict[str, object]:
    return {
        "source_of_truth": "private_operator_system",
        "invite_gated_only": True,
        "public_signup": False,
        "contract_execution": False,
        "live_negotiation_automation": False,
        "legal_advice": False,
        "buyer_data_exposure": False,
        "internal_profit_spread_exposure": False,
        "sanitized_fields": sorted(SANITIZED_SELLER_OFFER_FIELDS),
        "forbidden_fields": sorted(FORBIDDEN_SELLER_PORTAL_KEYS),
    }


def seller_portal_dashboard(session: Session) -> dict[str, object]:
    publications = session.query(SellerOfferPublication).all()
    responses = session.query(SellerPortalResponse).all()
    visible_offers = []
    blocked_offers = []

    for publication in publications:
        gate = update_seller_visibility_gate(publication)
        item = {
            "offer_id": publication.id,
            "deal_id": publication.deal_id,
            "lead_id": publication.lead_id,
            "offer_status": publication.offer_status,
            "portal_visibility_enabled": publication.portal_visibility_enabled,
            "visibility_status": publication.visibility_status,
            "blocked_reasons": gate["blocked_reasons"],
        }
        if gate["can_show"]:
            visible_offers.append(item)
        else:
            blocked_offers.append(item)

    return {
        "seller_visible_offers": visible_offers,
        "seller_portal_questions": [
            model_to_dict(response)
            for response in responses
            if response.response_type == "offer_question"
        ],
        "seller_document_checklist_queue": [
            {
                "offer_id": publication.id,
                "document_checklist": publication.document_checklist,
                "visibility_status": publication.visibility_status,
            }
            for publication in publications
            if publication.document_checklist
        ],
        "seller_response_queue": [
            model_to_dict(response)
            for response in responses
            if response.operator_review_status != "reviewed"
        ],
        "blocked_seller_visibility_reasons": blocked_offers,
        "contract_execution_allowed": False,
        "live_negotiation_automation_allowed": False,
        "buyer_data_exposure_allowed": False,
        "internal_profit_logic_exposure_allowed": False,
    }
