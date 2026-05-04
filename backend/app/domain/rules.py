from __future__ import annotations

from dataclasses import dataclass, field


ANALYSIS_ONLY_ACTIONS = {
    "analyze",
    "score",
    "draft",
    "recommend",
    "escalate",
    "flag_risk",
    "prepare_checklist",
    "summarize",
}

BLOCKED_ACTIONS = {
    "send_sms": "Live SMS is blocked in v1.",
    "send_email": "Live email is blocked in v1.",
    "call_seller": "Live calling is blocked in v1.",
    "contact_buyer": "Live buyer contact is blocked in v1.",
    "execute_contract": "Contract execution is blocked in v1.",
    "buyer_blast_execute": "Buyer blasts are draft-only in v1.",
    "generate_executable_contract": "Executable legal contract generation is blocked; V4 prepares checklists and placeholders only.",
    "submit_to_title_company": "Title-company submission is blocked in V4.",
    "change_contract_status_automatically": "Automatic contract status changes are blocked; owner approval controls real-world status changes.",
    "bulk_send": "Bulk communication is blocked; V5 allows only one approved draft to one tied recipient.",
    "campaign_send": "Campaigns are blocked in V5.",
    "auto_followup_sequence": "Automatic follow-up sequences are blocked in V5.",
    "skip_trace_paid_api": "Paid skip tracing and external paid API calls are blocked in v1.",
    "public_signup": "Public signup is blocked; this is a single-owner private OS.",
    "create_public_buyer_portal": "Public buyer portals are blocked; V2 allows only an invite-gated controlled deal room.",
    "create_public_seller_portal": "Public seller portals are blocked; V6 allows only an invite-gated controlled offer room.",
    "create_client_portal": "Client portals are out of scope for v1.",
    "execute_seller_portal_acceptance": "Seller portal acceptance execution is blocked; responses are owner-reviewed intake only.",
    "auto_negotiate_seller_offer": "Live negotiation automation is blocked in V6.",
    "automatic_closing_submission": "Automatic closing or title submission is blocked in V7.",
    "handle_payment": "Payment handling is blocked in V7.",
    "generate_closing_contract": "Executable closing or contract generation is blocked in V7.",
    "make_fake_profit_claim": "Fake or unsupported profit claims are blocked in V8.",
    "make_unsupported_roi_claim": "Unsupported ROI claims are blocked in V8.",
    "invent_buyer_seller_numbers": "Invented buyer or seller numbers are blocked; attribution must use source records.",
    "publish_client_facing_proof": "Client-facing proof is blocked unless explicitly approved in a future controlled release.",
    "make_legal_closing_guarantee": "Legal or closing guarantees are blocked in V8.",
    "live_buyer_blast": "Live buyer blasts are blocked; V9 prepares one-buyer draft distribution only.",
    "prepare_bulk_buyer_distribution": "Bulk buyer distribution is blocked in V9.",
    "make_misleading_scarcity_claim": "Misleading scarcity is blocked in buyer distribution drafts.",
    "make_fake_buyer_competition_claim": "Fake buyer competition or fake offers are blocked in buyer distribution drafts.",
    "expose_seller_private_data": "Seller/private lead data must not be exposed in buyer distribution prep.",
    "expose_assignment_fee_without_approval": "Assignment fee logic is hidden from buyer distribution unless explicitly approved in a future gate.",
    "execute_offer_acceptance": "Automatic seller acceptance is blocked in V10.",
    "mark_contract_ready_without_gate": "Contract-ready state requires V10 underwriting, profit, buyer demand, compliance, risk, readiness, and owner gates.",
    "automate_live_negotiation": "Live negotiation automation is blocked in V10.",
    "generate_offer_contract": "Executable contract generation is blocked; V10 only marks readiness for external attorney/title drafting.",
    "use_pressure_tactics": "Pressure tactics are blocked in V10 offer conversion.",
    "make_fake_urgency_claim": "False urgency is blocked in V10 offer conversion.",
    "submit_review_packet_to_title": "Title/attorney review packets are draft-only in V11; document submission is blocked.",
    "send_title_company_email": "Title company email sending is blocked in V11 review coordination.",
    "claim_attorney_client_relationship": "Attorney-client relationship claims are blocked in V11.",
    "guarantee_closing": "Closing guarantees are blocked in V11 title/attorney review coordination.",
    "autonomous_send_sms": "V12 autonomy may not send SMS.",
    "autonomous_send_email": "V12 autonomy may not send email.",
    "autonomous_call_seller": "V12 autonomy may not call sellers.",
    "autonomous_contact_buyer": "V12 autonomy may not contact buyers.",
    "autonomous_buyer_blast": "V12 autonomy may not execute buyer blasts.",
    "autonomous_contract_execution": "V12 autonomy may not execute contracts.",
    "autonomous_title_submission": "V12 autonomy may not submit to title companies.",
    "autonomous_portal_publish": "V12 autonomy may not publish portal data.",
    "autonomous_payment_collection": "V12 autonomy may not collect or handle payments.",
    "autonomy_level_5": "V12 Level 5 autonomy is disabled and unavailable.",
    "give_legal_advice": "Legal advice is blocked; use attorney/title review reminders.",
    "guarantee_profit": "Guaranteed profit claims are blocked.",
}

LEGAL_ADVICE_PATTERNS = (
    "you are legally required",
    "this is legal advice",
    "guaranteed profit",
    "you can ignore title",
    "no attorney needed",
    "hide the assignment fee",
    "misrepresent",
    "submit to title",
    "generate executable contract",
    "hide the assignment",
    "guaranteed roi",
    "risk-free return",
    "guaranteed close",
    "guaranteed closing",
    "invented buyer price",
    "invented seller price",
        "buyer blast",
        "send to all buyers",
        "autonomous blast",
        "autonomous title submission",
        "autonomous contract execution",
        "level 5 autonomy",
        "fake buyer competition",
    "fake offer",
    "misleading scarcity",
    "only buyer getting this",
    "we already have offers",
    "this will sell today",
    "i have buyers lined up",
    "we have buyers lined up",
    "attorney-client relationship",
    "we are your attorney",
    "send documents to title",
    "send to title company",
    "email title company",
    "will definitely close",
)


@dataclass(frozen=True)
class ValidationResult:
    allowed: bool
    action: str
    actor: str
    reason: str
    required_approvals: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, object]:
        return {
            "allowed": self.allowed,
            "action": self.action,
            "actor": self.actor,
            "reason": self.reason,
            "required_approvals": self.required_approvals,
            "risk_flags": self.risk_flags,
        }


def validate_action(
    actor: str,
    action: str,
    content: str = "",
    owner_approved: bool = False,
    compliance_reviewed: bool = False,
) -> ValidationResult:
    normalized_action = action.strip().lower()
    normalized_content = content.lower()
    risk_flags: list[str] = []

    if normalized_action in BLOCKED_ACTIONS:
        return ValidationResult(
            allowed=False,
            action=normalized_action,
            actor=actor,
            reason=BLOCKED_ACTIONS[normalized_action],
            risk_flags=[normalized_action],
        )

    matched_patterns = [
        phrase for phrase in LEGAL_ADVICE_PATTERNS if phrase in normalized_content
    ]
    if matched_patterns:
        return ValidationResult(
            allowed=False,
            action=normalized_action,
            actor=actor,
            reason="Unsafe, deceptive, guarantee, or legal-advice language detected.",
            risk_flags=matched_patterns,
        )

    if actor.lower() == "wholesale prime" and normalized_action not in ANALYSIS_ONLY_ACTIONS:
        return ValidationResult(
            allowed=False,
            action=normalized_action,
            actor=actor,
            reason="Wholesale Prime may only recommend, escalate, summarize, score, draft, or flag risk.",
            risk_flags=["overseer_execution_attempt"],
        )

    if normalized_action in {"prepare_offer_packet", "prepare_assignment_packet"}:
        required_approvals = []
        if not owner_approved:
            required_approvals.append("owner_approval")
        if normalized_action == "prepare_assignment_packet" and not compliance_reviewed:
            required_approvals.append("compliance_review")
        if required_approvals:
            return ValidationResult(
                allowed=False,
                action=normalized_action,
                actor=actor,
                reason="Required approval gate has not been satisfied.",
                required_approvals=required_approvals,
                risk_flags=["approval_gate"],
            )
        return ValidationResult(
            allowed=True,
            action=normalized_action,
            actor=actor,
            reason="Allowed gated packet-preparation action after required approval.",
            required_approvals=[],
            risk_flags=[],
        )

    if normalized_action in ANALYSIS_ONLY_ACTIONS:
        return ValidationResult(
            allowed=True,
            action=normalized_action,
            actor=actor,
            reason="Allowed analysis-only system action.",
            risk_flags=risk_flags,
        )

    return ValidationResult(
        allowed=False,
        action=normalized_action,
        actor=actor,
        reason="Unknown or execution-like action is blocked by default in v1.",
        risk_flags=["default_block"],
    )


def system_rules() -> dict[str, object]:
    return {
        "mode": "private_operator_only",
        "owner_final_approval": True,
        "public_signup": False,
        "portals": {
            "client": False,
            "buyer": "invite_gated_controlled",
            "seller": "invite_gated_controlled_offer_review",
        },
        "live_outreach": {"sms": False, "email": False, "calls": False, "buyer_blasts": False},
        "autonomy": {
            "level_2_internal_prep": True,
            "level_3_draft_creation_scheduling": True,
            "level_4_owner_approval_required": True,
            "level_5_available": False,
            "autonomous_live_outreach": False,
            "autonomous_contract_execution": False,
            "autonomous_title_submission": False,
            "autonomous_portal_publishing": False,
            "autonomous_payment_collection": False,
        },
        "blocked_actions": BLOCKED_ACTIONS,
        "agent_allowed_actions": sorted(ANALYSIS_ONLY_ACTIONS),
    }
