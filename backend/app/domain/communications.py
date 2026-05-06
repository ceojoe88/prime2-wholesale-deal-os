from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from typing import Protocol

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import (
    BuyerInterest,
    CommunicationApproval,
    CommunicationDraft,
    CommunicationDryRunReceipt,
    CommunicationSendAttempt,
    ContractControl,
    SellerInteraction,
    TitleHandoffPacket,
)
from app.serializers import model_to_dict


COMMUNICATION_UNSAFE_PATTERNS = {
    "pressure_language": [
        "you must sign",
        "sign now",
        "take it or leave it",
        "last chance",
        "do not talk to anyone else",
    ],
    "legal_advice": [
        "this is legal advice",
        "no attorney needed",
        "you are legally required",
        "ignore title",
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
    "misleading_assignment_language": [
        "hide the assignment",
        "do not mention assignment",
        "we are the end buyer no matter what",
    ],
    "hidden_fee_deception_language": [
        "keep the fee hidden",
        "do not disclose the fee",
        "seller does not need to know",
        "buyer does not need to know",
    ],
    "unsupported_claims": [
        "best price guaranteed",
        "highest offer guaranteed",
        "risk free",
        "guaranteed profit",
    ],
    "bulk_or_campaign_language": [
        "send to all buyers",
        "blast",
        "campaign",
        "auto follow-up",
    ],
}

SMS_OPT_OUT_PATTERNS = ("reply stop", "text stop", "stop to opt out")
ALLOWED_DRAFT_TYPES = {
    "seller_follow_up",
    "buyer_interest_response",
    "title_handoff_email",
    "internal_owner_note",
}


class CommunicationAdapter(Protocol):
    provider_mode: str

    def send(self, draft: CommunicationDraft, recipient: str, idempotency_key: str) -> dict[str, object]:
        ...


class MockEmailAdapter:
    provider_mode = "mock/dry_run"

    def send(self, draft: CommunicationDraft, recipient: str, idempotency_key: str) -> dict[str, object]:
        return {
            "provider_mode": self.provider_mode,
            "provider_called": True,
            "mock_sent": True,
            "channel": "email",
            "recipient": recipient,
            "idempotency_key": idempotency_key,
        }


class MockSmsAdapter:
    provider_mode = "mock/dry_run"

    def send(self, draft: CommunicationDraft, recipient: str, idempotency_key: str) -> dict[str, object]:
        return {
            "provider_mode": self.provider_mode,
            "provider_called": True,
            "mock_sent": True,
            "channel": "sms",
            "recipient": recipient,
            "idempotency_key": idempotency_key,
        }


def communication_hash(subject: str, body: str) -> str:
    value = f"{subject.strip()}\n{body.strip()}".encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def idempotency_key_for(draft: CommunicationDraft, recipient: str, subject_body_hash: str) -> str:
    raw = "|".join(
        [
            draft.id,
            draft.source_record_type,
            draft.source_record_id,
            recipient,
            subject_body_hash,
        ]
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def draft_recipient(draft: CommunicationDraft) -> str:
    if draft.channel == "sms":
        return draft.recipient_phone_placeholder
    if draft.channel == "internal":
        return draft.recipient_email_placeholder or "owner"
    return draft.recipient_email_placeholder


def validate_communication_safety(draft: CommunicationDraft) -> dict[str, object]:
    text = f"{draft.subject} {draft.draft_body}".lower()
    flags = [
        category
        for category, phrases in COMMUNICATION_UNSAFE_PATTERNS.items()
        if any(phrase in text for phrase in phrases)
    ]
    if draft.channel == "sms" and not any(pattern in text for pattern in SMS_OPT_OUT_PATTERNS):
        flags.append("missing_sms_opt_out")
    if draft.draft_type not in ALLOWED_DRAFT_TYPES:
        flags.append("unsupported_draft_type")
    return {
        "allowed": not flags,
        "risk_flags": sorted(set(flags)),
        "reason": "Communication draft passed safety checks." if not flags else "Communication draft blocked by safety checks.",
    }


def update_draft_safety(draft: CommunicationDraft) -> dict[str, object]:
    result = validate_communication_safety(draft)
    draft.safety_checked = True
    draft.safety_passed = bool(result["allowed"])
    draft.safety_result = result
    draft.draft_hash = communication_hash(draft.subject, draft.draft_body)
    draft.risk_status = "clear" if result["allowed"] else "blocked"
    draft.status = "safety_passed" if result["allowed"] else "blocked_safety"
    return result


def source_record_is_tied(session: Session, draft: CommunicationDraft, recipient: str) -> bool:
    if draft.source_record_type == "seller_interaction":
        record = session.get(SellerInteraction, draft.source_record_id)
        return (
            record is not None
            and draft.seller_interaction_id == record.id
            and draft.recipient_type == "seller"
            and bool(recipient)
        )
    if draft.source_record_type == "buyer_interest":
        record = session.get(BuyerInterest, draft.source_record_id)
        if record is None or draft.buyer_interest_id != record.id:
            return False
        if draft.channel == "sms":
            return recipient == record.buyer.phone
        return recipient == record.buyer.email
    if draft.source_record_type == "title_handoff_packet":
        record = session.get(TitleHandoffPacket, draft.source_record_id)
        return (
            record is not None
            and draft.title_handoff_packet_id == record.id
            and draft.recipient_type == "title_company"
            and bool(recipient)
        )
    if draft.source_record_type == "contract_control":
        record = session.get(ContractControl, draft.source_record_id)
        return record is not None and draft.recipient_type == "owner"
    return False


def generate_dry_run_receipt(session: Session, draft: CommunicationDraft) -> CommunicationDryRunReceipt:
    safety = update_draft_safety(draft)
    recipient = draft_recipient(draft)
    subject_body_hash = communication_hash(draft.subject, draft.draft_body)
    idempotency_key = idempotency_key_for(draft, recipient, subject_body_hash)
    existing = (
        session.query(CommunicationDryRunReceipt)
        .filter(CommunicationDryRunReceipt.idempotency_key == idempotency_key)
        .first()
    )
    if existing is not None:
        draft.last_dry_run_receipt_id = existing.id
        draft.status = "dry_run_ready" if safety["allowed"] else "blocked_safety"
        session.flush()
        return existing

    count = session.query(CommunicationDryRunReceipt).count() + 1
    receipt = CommunicationDryRunReceipt(
        id=f"dryrun-{count:03d}",
        draft_id=draft.id,
        recipient=recipient,
        subject_body_hash=subject_body_hash,
        source_record_type=draft.source_record_type,
        source_record_id=draft.source_record_id,
        risk_status="clear" if safety["allowed"] else "blocked",
        safety_result=safety,
        provider_mode=settings.communication_provider_mode,
        idempotency_key=idempotency_key,
    )
    draft.last_dry_run_receipt_id = receipt.id
    draft.status = "dry_run_ready" if safety["allowed"] else "blocked_safety"
    session.add(receipt)
    session.flush()
    return receipt


def approval_gate(
    session: Session,
    draft: CommunicationDraft,
    receipt: CommunicationDryRunReceipt | None,
    approval: CommunicationApproval | None,
    recipient_count: int = 1,
) -> dict[str, object]:
    reasons: list[str] = []
    current_hash = communication_hash(draft.subject, draft.draft_body)
    recipient = draft_recipient(draft)

    if draft.draft_type == "title_handoff_email":
        reasons.append("title_company_submission_blocked")
    if recipient_count != 1:
        reasons.append("bulk_send_blocked")
    if not draft.safety_checked:
        reasons.append("safety_check_missing")
    if not draft.safety_passed:
        reasons.append("safety_not_passed")
    if receipt is None:
        reasons.append("dry_run_receipt_missing")
    elif current_hash != receipt.subject_body_hash:
        reasons.append("draft_changed_after_dry_run")
    if approval is None or not approval.owner_approval_recorded:
        reasons.append("owner_approval_not_recorded")
    if not settings.communication_global_live_enabled:
        reasons.append("global_live_flag_disabled")
    if not draft.communication_live_flag_enabled:
        reasons.append("communication_live_flag_disabled")
    if not draft.provider_readiness:
        reasons.append("provider_not_ready")
    if not source_record_is_tied(session, draft, recipient):
        reasons.append("recipient_not_tied_to_source_record")
    if draft.live_send_count > 0:
        reasons.append("draft_already_sent")
    if receipt is not None:
        prior = (
            session.query(CommunicationSendAttempt)
            .filter(
                CommunicationSendAttempt.idempotency_key == receipt.idempotency_key,
                CommunicationSendAttempt.attempt_status.in_(["mock_sent", "sent"]),
            )
            .first()
        )
        if prior is not None:
            reasons.append("idempotency_key_already_used")

    return {
        "can_send": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "current_hash": current_hash,
        "recipient": recipient,
        "provider_mode": settings.communication_provider_mode,
    }


def latest_approval_for(
    session: Session,
    draft: CommunicationDraft,
    receipt: CommunicationDryRunReceipt | None,
) -> CommunicationApproval | None:
    if receipt is None:
        return None
    return (
        session.query(CommunicationApproval)
        .filter(
            CommunicationApproval.draft_id == draft.id,
            CommunicationApproval.dry_run_receipt_id == receipt.id,
            CommunicationApproval.owner_approval_recorded.is_(True),
        )
        .order_by(CommunicationApproval.created_at.desc())
        .first()
    )


def record_send_attempt(
    session: Session,
    draft: CommunicationDraft,
    receipt: CommunicationDryRunReceipt | None,
    gate: dict[str, object],
    live_send_requested: bool = True,
    provider_called: bool = False,
    mock_sent: bool = False,
) -> CommunicationSendAttempt:
    count = session.query(CommunicationSendAttempt).count() + 1
    attempt = CommunicationSendAttempt(
        id=f"comm-attempt-{count:03d}",
        draft_id=draft.id,
        dry_run_receipt_id=receipt.id if receipt else None,
        recipient=str(gate.get("recipient") or draft_recipient(draft)),
        channel=draft.channel,
        provider_mode=str(gate.get("provider_mode") or settings.communication_provider_mode),
        attempt_status="mock_sent" if mock_sent else "blocked",
        blocked_reasons=list(gate.get("blocked_reasons") or []),
        safety_result=draft.safety_result,
        idempotency_key=receipt.idempotency_key if receipt else "",
        provider_called=provider_called,
        mock_sent=mock_sent,
        live_send_requested=live_send_requested,
        bulk_send_detected="bulk_send_blocked" in gate.get("blocked_reasons", []),
    )
    session.add(attempt)
    session.flush()
    return attempt


def send_with_gate(
    session: Session,
    draft: CommunicationDraft,
    receipt: CommunicationDryRunReceipt | None,
    approval: CommunicationApproval | None,
    recipient_count: int = 1,
) -> tuple[CommunicationSendAttempt, dict[str, object]]:
    gate = approval_gate(session, draft, receipt, approval, recipient_count)
    if not gate["can_send"]:
        attempt = record_send_attempt(session, draft, receipt, gate, provider_called=False)
        draft.status = "blocked_live_attempt"
        draft.blocked_reasons = gate["blocked_reasons"]
        return attempt, gate

    adapter: CommunicationAdapter = MockSmsAdapter() if draft.channel == "sms" else MockEmailAdapter()
    result = adapter.send(draft, str(gate["recipient"]), receipt.idempotency_key if receipt else "")
    attempt = record_send_attempt(
        session,
        draft,
        receipt,
        gate,
        provider_called=bool(result["provider_called"]),
        mock_sent=bool(result["mock_sent"]),
    )
    draft.live_send_count += 1
    draft.status = "mock_sent"
    return attempt, gate


def communication_dashboard(session: Session) -> dict[str, object]:
    drafts = session.query(CommunicationDraft).all()
    receipts = session.query(CommunicationDryRunReceipt).all()
    attempts = session.query(CommunicationSendAttempt).all()
    approvals = session.query(CommunicationApproval).all()

    return {
        "global_live_flag_enabled": settings.communication_global_live_enabled,
        "provider_mode": settings.communication_provider_mode,
        "drafts_needing_safety_check": [
            model_to_dict(draft) for draft in drafts if not draft.safety_checked
        ],
        "dry_runs_needing_owner_approval": [
            model_to_dict(receipt)
            for receipt in receipts
            if not any(
                approval.owner_approval_recorded
                and approval.dry_run_receipt_id == receipt.id
                for approval in approvals
            )
            and receipt.safety_result.get("allowed") is True
        ],
        "blocked_live_attempts": [
            model_to_dict(attempt)
            for attempt in attempts
            if attempt.attempt_status == "blocked"
        ],
        "sent_or_mock_sent_attempts": [
            model_to_dict(attempt)
            for attempt in attempts
            if attempt.attempt_status in {"mock_sent", "sent"}
        ],
        "communication_risk_queue": [
            model_to_dict(draft)
            for draft in drafts
            if draft.risk_status == "blocked" or draft.blocked_reasons
        ],
        "drafts": [model_to_dict(draft) for draft in drafts],
        "dry_runs": [model_to_dict(receipt) for receipt in receipts],
        "approvals": [model_to_dict(approval) for approval in approvals],
        "attempts": [model_to_dict(attempt) for attempt in attempts],
        "bulk_send_allowed": False,
        "campaigns_allowed": False,
        "buyer_blast_execution_allowed": False,
        "title_company_submission_allowed": False,
    }
