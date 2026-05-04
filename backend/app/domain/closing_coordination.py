from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.buyer_portal import portal_publish_gate, update_publication_gate
from app.domain.seller_portal import update_seller_visibility_gate
from app.models import (
    AssignmentReadinessRecord,
    ClosingCoordinationChecklist,
    CommunicationDraft,
    ContractControl,
    Deal,
    DealRoomBlocker,
    SellerInteraction,
    SellerOfferPublication,
    TitleHandoffPacket,
    UnifiedDealRoom,
)
from app.serializers import model_to_dict


NEXT_ACTION_BY_BLOCKER = {
    "missing_buyer_pof": "verify buyer POF",
    "missing_seller_document": "review seller response",
    "missing_compliance_review": "resolve compliance blocker",
    "missing_owner_approval": "update closing timeline",
    "weak_buyer_margin": "review assignment readiness",
    "high_risk_language": "resolve compliance blocker",
    "assignment_not_confirmed": "review assignment readiness",
    "title_handoff_incomplete": "prepare title handoff",
    "communication_draft_pending": "approve communication dry-run",
}

BLOCKER_DETAILS = {
    "missing_buyer_pof": ("high", "Buyer proof of funds must be verified before assignment readiness."),
    "missing_seller_document": ("medium", "Seller document or access item still needs operator review."),
    "missing_compliance_review": ("critical", "Compliance review must be complete before closing coordination can clear."),
    "missing_owner_approval": ("critical", "Owner approval is required for real-world coordination steps."),
    "weak_buyer_margin": ("critical", "Buyer margin is below the protected threshold."),
    "high_risk_language": ("critical", "Unsafe language is present in a seller or communication record."),
    "assignment_not_confirmed": ("high", "Assignment allowed status must be confirmed."),
    "title_handoff_incomplete": ("high", "Title handoff packet is missing or incomplete."),
    "communication_draft_pending": ("medium", "Communication draft still needs safety or dry-run review."),
}


def _latest_or_none(records):
    return records[0] if records else None


def _buyer_margin(deal: Deal) -> int:
    return deal.arv - deal.repairs - deal.buyer_costs - deal.buyer_purchase_price


def _seller_status(room: UnifiedDealRoom) -> str:
    publication = room.seller_offer_publication
    if publication is None:
        publication = _latest_or_none(room.deal.seller_offer_publications)
    if publication is None:
        return "missing"
    update_seller_visibility_gate(publication)
    return publication.visibility_status


def _buyer_status(room: UnifiedDealRoom) -> str:
    publication = room.buyer_deal_publication or room.deal.buyer_publication
    if publication is None:
        return "missing"
    update_publication_gate(publication, room.deal)
    return "visible" if portal_publish_gate(room.deal, publication)["can_publish"] else publication.availability_status


def _title_status(room: UnifiedDealRoom) -> str:
    packet = room.title_handoff_packet or _latest_or_none(room.deal.title_handoff_packets)
    if packet is None:
        return "missing"
    if packet.title_submission_allowed or packet.submitted_to_title:
        return "blocked_submission_enabled"
    return packet.packet_status


def _assignment_status(room: UnifiedDealRoom) -> str:
    record = room.assignment_readiness_record or _latest_or_none(room.deal.assignment_readiness_records)
    if record is None:
        return "blocked"
    return "assignment_ready" if record.assignment_ready else record.readiness_status


def _communication_drafts_for(session: Session, deal: Deal) -> list[CommunicationDraft]:
    seller_interaction_ids = [
        interaction.id
        for interaction in session.query(SellerInteraction)
        .filter(SellerInteraction.lead_id == deal.lead_id)
        .all()
    ]
    buyer_interest_ids = [interest.id for interest in deal.buyer_interests]
    title_packet_ids = [packet.id for packet in deal.title_handoff_packets]
    drafts = session.query(CommunicationDraft).all()
    return [
        draft
        for draft in drafts
        if draft.seller_interaction_id in seller_interaction_ids
        or draft.buyer_interest_id in buyer_interest_ids
        or draft.title_handoff_packet_id in title_packet_ids
    ]


def _communication_status(session: Session, room: UnifiedDealRoom) -> str:
    drafts = _communication_drafts_for(session, room.deal)
    if not drafts:
        return "missing"
    if any(draft.risk_status == "blocked" or (draft.safety_checked and not draft.safety_passed) for draft in drafts):
        return "blocked"
    if any(not draft.safety_checked for draft in drafts):
        return "pending"
    return "ready"


def _compliance_status(room: UnifiedDealRoom) -> str:
    contract = room.contract_control
    records = room.deal.compliance_records
    if contract.compliance_review_status != "approved":
        return "pending"
    if any(record.status == "needs_review" for record in records):
        return "pending"
    return "complete"


def _has_high_risk_language(session: Session, room: UnifiedDealRoom) -> bool:
    seller_publications = room.deal.seller_offer_publications
    if any(not publication.offer_language_safety_passed for publication in seller_publications):
        return True
    return any(
        draft.risk_status == "blocked" or (draft.safety_checked and not draft.safety_passed)
        for draft in _communication_drafts_for(session, room.deal)
    )


def update_deal_room_statuses(session: Session, room: UnifiedDealRoom) -> None:
    room.seller_portal_status = _seller_status(room)
    room.buyer_portal_status = _buyer_status(room)
    room.title_handoff_status = _title_status(room)
    room.assignment_readiness_status = _assignment_status(room)
    room.communication_status = _communication_status(session, room)
    room.compliance_status = _compliance_status(room)
    room.owner_approval_status = room.contract_control.owner_approval_status
    room.closing_timeline = room.contract_control.closing_timeline


def checklist_blocked_reasons(checklist: ClosingCoordinationChecklist) -> list[str]:
    checks = {
        "seller_accepted_offer": checklist.seller_accepted_offer,
        "contract_prep_ready": checklist.contract_prep_ready,
        "buyer_matched": checklist.buyer_matched,
        "buyer_pof_verified": checklist.buyer_pof_verified,
        "assignment_allowed_confirmed": checklist.assignment_allowed_confirmed,
        "title_handoff_prepared": checklist.title_handoff_prepared,
        "inspection_access_coordinated": checklist.inspection_access_coordinated,
        "seller_documents_requested": checklist.seller_documents_requested,
        "buyer_intent_recorded": checklist.buyer_intent_recorded,
        "compliance_review_complete": checklist.compliance_review_complete,
        "owner_approval_complete": checklist.owner_approval_complete,
    }
    return [key for key, value in checks.items() if not value]


def expected_blocker_types(session: Session, room: UnifiedDealRoom) -> list[str]:
    checklist = room.closing_checklist
    if checklist is None:
        return ["missing_seller_document", "missing_owner_approval"]

    blockers: list[str] = []
    if not checklist.buyer_pof_verified:
        blockers.append("missing_buyer_pof")
    if not checklist.seller_documents_requested:
        blockers.append("missing_seller_document")
    if not checklist.compliance_review_complete or room.compliance_status != "complete":
        blockers.append("missing_compliance_review")
    if not checklist.owner_approval_complete or room.owner_approval_status != "approved":
        blockers.append("missing_owner_approval")
    if _buyer_margin(room.deal) < room.deal.buyer_desired_profit:
        blockers.append("weak_buyer_margin")
    if _has_high_risk_language(session, room):
        blockers.append("high_risk_language")
    if not checklist.assignment_allowed_confirmed:
        blockers.append("assignment_not_confirmed")
    if not checklist.title_handoff_prepared or room.title_handoff_status in {"missing", "blocked_submission_enabled"}:
        blockers.append("title_handoff_incomplete")
    if room.communication_status in {"missing", "pending", "blocked"}:
        blockers.append("communication_draft_pending")
    return sorted(set(blockers))


def sync_blockers(session: Session, room: UnifiedDealRoom) -> list[DealRoomBlocker]:
    expected = expected_blocker_types(session, room)
    existing_by_type = {blocker.blocker_type: blocker for blocker in room.blocker_records}
    next_id = session.query(DealRoomBlocker).count() + 1

    for blocker_type in expected:
        severity, detail = BLOCKER_DETAILS[blocker_type]
        blocker = existing_by_type.get(blocker_type)
        if blocker is None:
            blocker = DealRoomBlocker(
                id=f"deal-blocker-{next_id:03d}",
                deal_room_id=room.id,
                deal_id=room.deal_id,
                blocker_type=blocker_type,
            )
            next_id += 1
            session.add(blocker)
            existing_by_type[blocker_type] = blocker
        blocker.severity = severity
        blocker.status = "open"
        blocker.source = "closing_coordination_gate"
        blocker.detail = detail
        blocker.recommendation = NEXT_ACTION_BY_BLOCKER[blocker_type]
        blocker.blocks_closing = True
        blocker.owner_action_required = blocker_type in {
            "missing_owner_approval",
            "missing_compliance_review",
            "weak_buyer_margin",
            "high_risk_language",
        }
        blocker.resolved = False
        blocker.draft_only = True

    for blocker_type, blocker in existing_by_type.items():
        if blocker_type not in expected:
            blocker.status = "resolved"
            blocker.resolved = True
            blocker.blocks_closing = False

    session.flush()
    return [blocker for blocker in room.blocker_records if not blocker.resolved]


def next_best_actions(room: UnifiedDealRoom) -> list[dict[str, object]]:
    actions = []
    seen: set[str] = set()
    for blocker in room.blocker_records:
        if blocker.resolved:
            continue
        action = NEXT_ACTION_BY_BLOCKER.get(blocker.blocker_type, "review assignment readiness")
        if action in seen:
            continue
        seen.add(action)
        actions.append(
            {
                "action": action,
                "source_blocker": blocker.blocker_type,
                "recommendation_only": True,
                "owner_approval_required": blocker.owner_action_required,
                "legal_execution_allowed": False,
                "title_submission_allowed": False,
                "payment_handling_allowed": False,
                "automatic_negotiation_allowed": False,
            }
        )
    return actions


def closing_readiness_gate(room: UnifiedDealRoom) -> dict[str, object]:
    checklist = room.closing_checklist
    reasons = checklist_blocked_reasons(checklist) if checklist else ["missing_checklist"]
    open_blockers = [blocker.blocker_type for blocker in room.blocker_records if not blocker.resolved]
    if open_blockers:
        reasons.extend(f"blocker:{blocker}" for blocker in open_blockers)
    if room.owner_approval_status != "approved":
        reasons.append("owner_approval_not_recorded")
    if room.legal_execution_allowed or room.executable_contract_generated:
        reasons.append("legal_execution_enabled")
    if room.title_submission_allowed:
        reasons.append("title_submission_enabled")
    if room.payment_handling_allowed:
        reasons.append("payment_handling_enabled")
    if room.automatic_negotiation_allowed:
        reasons.append("automatic_negotiation_enabled")
    return {
        "closing_ready": not reasons,
        "blocked_reasons": sorted(set(reasons)),
        "recommendation_only": True,
        "legal_execution_allowed": False,
        "title_submission_allowed": False,
        "payment_handling_allowed": False,
        "automatic_negotiation_allowed": False,
    }


def sync_deal_room(session: Session, room: UnifiedDealRoom) -> dict[str, object]:
    update_deal_room_statuses(session, room)
    if room.closing_checklist is not None:
        room.closing_checklist.blocked_reasons = checklist_blocked_reasons(room.closing_checklist)
        room.closing_checklist.readiness_status = (
            "checklist_complete" if not room.closing_checklist.blocked_reasons else "blocked"
        )
    open_blockers = sync_blockers(session, room)
    room.blockers = [blocker.blocker_type for blocker in open_blockers]
    room.next_required_actions = [item["action"] for item in next_best_actions(room)]
    room.projected_assignment_fee_at_risk = room.deal.projected_assignment_fee if open_blockers else 0
    gate = closing_readiness_gate(room)
    room.coordination_status = "closing_ready" if gate["closing_ready"] else "blocked"
    return gate


def unified_deal_room_summary(room: UnifiedDealRoom) -> dict[str, object]:
    return {
        **model_to_dict(room),
        "deal": model_to_dict(room.deal),
        "contract_control": model_to_dict(room.contract_control),
        "closing_checklist": model_to_dict(room.closing_checklist) if room.closing_checklist else None,
        "blocker_records": [
            model_to_dict(blocker) for blocker in room.blocker_records if not blocker.resolved
        ],
        "next_best_actions": next_best_actions(room),
        "readiness_gate": closing_readiness_gate(room),
        "recommendation_only": True,
        "legal_execution_allowed": False,
        "title_submission_allowed": False,
        "payment_handling_allowed": False,
        "automatic_negotiation_allowed": False,
    }


def closing_coordination_dashboard(session: Session) -> dict[str, object]:
    rooms = session.query(UnifiedDealRoom).all()
    for room in rooms:
        sync_deal_room(session, room)

    active = [room for room in rooms if room.coordination_status in {"blocked", "closing_ready"}]
    closing_ready = [room for room in rooms if closing_readiness_gate(room)["closing_ready"]]
    blocked = [room for room in rooms if not closing_readiness_gate(room)["closing_ready"]]
    blockers = [
        blocker
        for room in rooms
        for blocker in room.blocker_records
        if not blocker.resolved
    ]
    return {
        "active_deal_rooms": [unified_deal_room_summary(room) for room in active],
        "closing_ready_deals": [unified_deal_room_summary(room) for room in closing_ready],
        "blocked_deals": [unified_deal_room_summary(room) for room in blocked],
        "assignment_ready_deals": [
            unified_deal_room_summary(room)
            for room in rooms
            if room.assignment_readiness_status == "assignment_ready"
        ],
        "portal_statuses": [
            {
                "deal_room_id": room.id,
                "seller_portal_status": room.seller_portal_status,
                "buyer_portal_status": room.buyer_portal_status,
                "title_handoff_status": room.title_handoff_status,
            }
            for room in rooms
        ],
        "next_best_actions": [
            {"deal_room_id": room.id, **action}
            for room in rooms
            for action in next_best_actions(room)
        ],
        "projected_assignment_fees_at_risk": sum(room.projected_assignment_fee_at_risk for room in rooms),
        "blockers": [model_to_dict(blocker) for blocker in blockers],
        "recommendation_only": True,
        "legal_execution_allowed": False,
        "title_submission_allowed": False,
        "payment_handling_allowed": False,
        "automatic_negotiation_allowed": False,
    }
