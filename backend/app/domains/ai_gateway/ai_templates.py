from __future__ import annotations

from typing import Any


TEMPLATE_LIBRARY: dict[str, dict[str, object]] = {
    "seller_script_draft": {
        "template_name": "Seller script draft",
        "template_version": "v20.1",
        "template_sections": ["intro", "empathy", "property_question", "soft_close"],
        "template_body": (
            "Intro: identify the operator. Empathy: acknowledge seller context. "
            "Question: ask about property condition and timeline. Soft close: ask whether "
            "the owner may review a written as-is option."
        ),
    },
    "buyer_message_draft": {
        "template_name": "Buyer message draft",
        "template_version": "v20.1",
        "template_sections": ["deal_summary", "system_numbers", "cta"],
        "template_body": (
            "Deal summary from sanitized system data. Numbers must come from source_data. "
            "CTA asks for draft interest or proof-of-funds review only."
        ),
    },
    "objection_response": {
        "template_name": "Objection response draft",
        "template_version": "v20.1",
        "template_sections": ["acknowledge", "clarify", "evidence", "next_step"],
        "template_body": "Non-pressuring objection response with owner review required.",
    },
    "deal_summary": {
        "template_name": "Deal summary",
        "template_version": "v20.1",
        "template_sections": ["property", "numbers", "risks", "next_actions"],
        "template_body": "Internal summary using existing underwriting and gate data only.",
    },
    "daily_briefing": {
        "template_name": "Daily briefing",
        "template_version": "v20.1",
        "template_sections": ["hot_deals", "owner_approvals", "blockers", "safe_actions"],
        "template_body": "Prime 2 daily briefing with recommendations only.",
    },
    "negotiation_assist": {
        "template_name": "Negotiation assist",
        "template_version": "v20.1",
        "template_sections": ["seller_context", "safe_range", "objection", "next_move"],
        "template_body": "Negotiation support without pressure tactics or live automation.",
    },
    "field_testing_summary": {
        "template_name": "Field testing summary",
        "template_version": "v20.1",
        "template_sections": ["import_quality", "call_outcomes", "prediction_misses", "adjustments"],
        "template_body": "Summarize real lead QA and feedback loop results.",
    },
    "call_intelligence_extraction": {
        "template_name": "Call intelligence extraction",
        "template_version": "v23.1",
        "template_sections": ["seller_signals", "objections", "risk_flags", "next_action"],
        "template_body": "Extract seller conversation signals from provided transcript basis only. Do not invent prices, repairs, motivation, or commitments.",
    },
}


def template_for(request_type: str) -> dict[str, object]:
    return TEMPLATE_LIBRARY[request_type]


def build_template_response(request_type: str, source_data: dict[str, Any]) -> str:
    property_summary = str(source_data.get("property_summary") or source_data.get("address") or "property on file")
    next_action = str(source_data.get("next_best_action") or "owner review")
    arv_range = source_data.get("arv_range", "system ARV range on file")
    repair_range = source_data.get("repair_estimate_range", "system repair range on file")
    asking_price = source_data.get("asking_price", "system asking price on file")
    buyer_margin = source_data.get("buyer_margin", "system buyer margin on file")

    responses = {
        "seller_script_draft": (
            f"Draft for owner review: Hi, this is the operator following up about {property_summary}. "
            "I wanted to understand your timeline, the current condition, and whether an as-is option "
            f"would be useful. If it makes sense, the owner can review a written next step. Suggested next action: {next_action}."
        ),
        "buyer_message_draft": (
            f"Draft buyer note: {property_summary}. Asking price: {asking_price}. "
            f"ARV range: {arv_range}. Repair estimate range: {repair_range}. "
            f"Estimated buyer margin: {buyer_margin}. Reply with draft interest or proof-of-funds status for owner review."
        ),
        "objection_response": (
            f"Draft response: I hear the concern. The current numbers are based on the system record for {property_summary}, "
            f"including ARV range {arv_range} and repair range {repair_range}. The owner can review the issue and decide the next step."
        ),
        "deal_summary": (
            f"Internal deal summary: {property_summary}. Asking price: {asking_price}. ARV range: {arv_range}. "
            f"Repair range: {repair_range}. Buyer margin: {buyer_margin}. Recommended action: {next_action}."
        ),
        "daily_briefing": (
            "Prime 2 briefing draft: review hot opportunities, owner approvals, compliance blockers, buyer POF gaps, "
            f"and field-testing misses. Priority next action: {next_action}."
        ),
        "negotiation_assist": (
            f"Negotiation support draft: keep the conversation centered on {property_summary}, documented condition, "
            f"timeline, and the existing safe range. Recommended next move: {next_action}."
        ),
        "field_testing_summary": (
            "Field-testing summary draft: imported lead QA, call outcomes, do-not-contact records, and prediction misses "
            f"should be reviewed before scoring changes. Recommended next action: {next_action}."
        ),
        "call_intelligence_extraction": (
            "Call intelligence extraction draft: review transcript-based seller signals, objections, DNC status, "
            f"risk flags, and draft-only next action. Recommended next action: {next_action}."
        ),
    }
    return responses[request_type]
