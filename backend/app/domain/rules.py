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
    "create_seller_portal": "Seller portals are out of scope for v1.",
    "create_client_portal": "Client portals are out of scope for v1.",
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
        "portals": {"client": False, "buyer": "invite_gated_controlled", "seller": False},
        "live_outreach": {"sms": False, "email": False, "calls": False, "buyer_blasts": False},
        "blocked_actions": BLOCKED_ACTIONS,
        "agent_allowed_actions": sorted(ANALYSIS_ONLY_ACTIONS),
    }
