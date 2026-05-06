from __future__ import annotations

from uuid import uuid4

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.domains.real_deal_execution.safety import (
    execution_safety_boundary,
    validate_execution_guidance_text,
)
from app.domains.real_deal_execution.sanitizer import sanitize_execution_record
from app.domains.real_deal_execution.schemas import (
    RealDealExecutionBatchCreate,
    RealDealExecutionBatchStatusUpdate,
)
from app.domains.real_deal_execution.scoring import (
    buyer_margin,
    buyer_validation_gate,
    contract_ready_gate,
    evidence_gate,
    offer_decision_status,
)
from app.domains.real_deal_execution.workflow import call_checklist, validate_batch_status
from app.models import (
    AssignmentFeeAttribution,
    Buyer,
    BuyerDealPriority,
    ContractReadyState,
    Deal,
    DealEvidencePacket,
    FieldCallOutcome,
    Lead,
    LeadImportBatch,
    LeadImportRow,
    LeadQualityReview,
    LearningSignal,
    OfferPacket,
    RealDealExecutionBatch,
    TitleReviewCoordination,
)
from app.serializers import model_to_dict


MOTIVATED_RESULTS = {"motivated", "offer_requested", "appointment_set"}
ACTIVE_STATUSES = {
    "draft",
    "active",
    "calling",
    "underwriting",
    "offer_decision",
    "buyer_validation",
    "contract_ready",
}


def active_execution_batch(session: Session) -> RealDealExecutionBatch:
    batch = (
        session.query(RealDealExecutionBatch)
        .filter(RealDealExecutionBatch.batch_status.in_(ACTIVE_STATUSES))
        .order_by(desc(RealDealExecutionBatch.created_at))
        .first()
    )
    if batch is not None:
        sync_execution_batch_counts(session, batch)
        return batch

    import_batch = session.query(LeadImportBatch).order_by(desc(LeadImportBatch.created_at)).first()
    batch = RealDealExecutionBatch(
        id=f"execution-batch-{uuid4().hex[:10]}",
        batch_name="First real deal batch",
        lead_import_batch_id=import_batch.id if import_batch else None,
        market_zip_focus=["75216"],
        batch_status="draft",
        owner_notes="Prime 2 created a guarded first-deal execution batch.",
        next_best_action="Review imported leads, QA rows, and call-priority sellers before any owner-run calls.",
        safety_notes=[
            "Prime 2 recommends and tracks only.",
            "Owner executes and approves real-world actions.",
        ],
    )
    session.add(batch)
    session.flush()
    sync_execution_batch_counts(session, batch)
    return batch


def create_execution_batch(
    session: Session,
    request: RealDealExecutionBatchCreate,
) -> dict[str, object]:
    batch = RealDealExecutionBatch(
        id=f"execution-batch-{uuid4().hex[:10]}",
        batch_name=request.batch_name,
        lead_import_batch_id=request.lead_import_batch_id,
        market_zip_focus=request.market_zip_focus,
        target_assignment_fee=request.target_assignment_fee,
        batch_status="draft",
        owner_notes=request.owner_notes,
        next_best_action="Run QA, call-priority review, and underwriting before offer decisions.",
        safety_notes=["No imported lead triggers live outreach automatically."],
    )
    session.add(batch)
    sync_execution_batch_counts(session, batch)
    session.commit()
    session.refresh(batch)
    return sanitize_execution_record(batch)


def update_batch_status(
    session: Session,
    batch_id: str,
    request: RealDealExecutionBatchStatusUpdate,
) -> dict[str, object]:
    batch = session.get(RealDealExecutionBatch, batch_id)
    if batch is None:
        raise ValueError(f"Execution batch not found: {batch_id}")
    batch.batch_status = validate_batch_status(request.batch_status)
    if request.owner_notes is not None:
        batch.owner_notes = request.owner_notes
    sync_execution_batch_counts(session, batch)
    session.commit()
    session.refresh(batch)
    return sanitize_execution_record(batch)


def sync_execution_batch_counts(session: Session, batch: RealDealExecutionBatch) -> RealDealExecutionBatch:
    rows = _import_rows_for_batch(session, batch)
    deals = _deals_for_batch(session, batch)
    call_outcomes = session.query(FieldCallOutcome).all()
    motivated = [outcome for outcome in call_outcomes if outcome.contact_result in MOTIVATED_RESULTS]
    offers = session.query(OfferPacket).all()
    accepted = session.query(ContractReadyState).filter(ContractReadyState.seller_likely_to_sign.is_(True)).all()
    assignment_fees = session.query(AssignmentFeeAttribution).all()

    batch.leads_reviewed = len(rows) or session.query(LeadQualityReview).count()
    batch.calls_completed = len(call_outcomes)
    batch.motivated_sellers = len(motivated)
    batch.offers_prepared = len(offers)
    batch.offers_accepted = len(accepted)
    batch.buyer_matches = sum(len(deal.buyer_priorities) or len(deal.matches) for deal in deals)
    contract_states = [_contract_state_for_deal(session, deal.id) for deal in deals]
    batch.contract_ready_count = len([state for state in contract_states if state and state.contract_ready])
    batch.projected_assignment_fees = sum(max(deal.projected_assignment_fee, 0) for deal in deals)
    batch.verified_assignment_fees = sum(
        item.projected_assignment_fee for item in assignment_fees if item.verification_status == "verified"
    )
    batch.blockers = _cockpit_blockers(session, batch, deals)
    batch.next_best_action = _next_best_action(batch)
    return batch


def cockpit_dashboard(session: Session) -> dict[str, object]:
    batch = active_execution_batch(session)
    session.commit()
    top_imported = top_imported_leads(session, batch)
    call_priority = [item for item in top_imported if item.get("recommended_next_action") == "call_priority"][:3]
    offers = offer_decision_board(session)
    buyer_validation = buyer_validation_board(session)
    contract_ready = contract_ready_board(session)
    evidence = evidence_tracker(session)
    return {
        "current_execution_batch": sanitize_execution_record(batch),
        "top_10_imported_leads": top_imported[:10],
        "top_3_call_priority_leads": call_priority,
        "seller_calls_completed": batch.calls_completed,
        "motivated_sellers_found": batch.motivated_sellers,
        "deals_needing_underwriting": [item for item in offers["offers"] if item["decision_status"] == "needs_data"],
        "offers_ready_for_owner_decision": [
            item for item in offers["offers"] if item["decision_status"] == "ready_for_owner_review"
        ],
        "buyer_validation_needed": [
            item for item in buyer_validation["buyer_validations"] if not item["gate"]["validated"]
        ],
        "contract_ready_candidates": [
            item for item in contract_ready["contract_ready_candidates"] if item["gate"]["contract_ready"]
        ],
        "title_attorney_handoff_needed": [
            item for item in contract_ready["contract_ready_candidates"] if item["title_review_status"] != "ready"
        ],
        "projected_10k_assignment_fee_candidates": [
            item for item in evidence["evidence_records"] if item["projected_assignment_fee"] >= batch.target_assignment_fee
        ],
        "blockers": batch.blockers,
        "next_best_action": batch.next_best_action,
        "prime_2_execution_coach": execution_coach(session),
        "safety_boundary": execution_safety_boundary(),
    }


def top_imported_leads(session: Session, batch: RealDealExecutionBatch | None = None) -> list[dict[str, object]]:
    batch = batch or active_execution_batch(session)
    rows = _import_rows_for_batch(session, batch)
    qa_by_row = {
        review.import_row_id: review
        for review in session.query(LeadQualityReview).filter(LeadQualityReview.import_row_id.is_not(None)).all()
    }
    cards: list[dict[str, object]] = []
    for row in rows:
        review = qa_by_row.get(row.id)
        cards.append(
            {
                "id": row.id,
                "owner_name": row.owner_name,
                "property": _row_property(row),
                "lead_source": row.lead_source,
                "lead_type": row.lead_type,
                "row_status": row.row_status,
                "approved_for_commit": row.approved_for_commit,
                "data_confidence": row.data_confidence,
                "qa_score": review.data_quality_score if review else 0,
                "contactability_score": review.contactability_score if review else 0,
                "recommended_next_action": review.recommended_next_action if review else "research_more",
                "blocked_reasons": sorted(set((row.blocked_reasons or []) + (review.blocked_reasons if review else []))),
                "live_outreach_allowed": False,
            }
        )
    cards.sort(key=lambda item: (item["recommended_next_action"] == "call_priority", item["qa_score"]), reverse=True)
    return cards


def seller_call_workflow(session: Session) -> dict[str, object]:
    batch = active_execution_batch(session)
    outcomes = (
        session.query(FieldCallOutcome)
        .order_by(desc(FieldCallOutcome.call_datetime))
        .all()
    )
    return {
        "current_execution_batch": sanitize_execution_record(batch),
        "guided_call_checklist": call_checklist(),
        "call_queue": top_imported_leads(session, batch)[:10],
        "recent_call_outcomes": [model_to_dict(outcome) for outcome in outcomes],
        "mobile_call_queue_path": "/mobile/calls",
        "system_calling_enabled": False,
    }


def offer_decision_board(session: Session) -> dict[str, object]:
    batch = active_execution_batch(session)
    offers: list[dict[str, object]] = []
    for deal in _deals_for_batch(session, batch):
        packet = _offer_packet_for_deal(session, deal.id)
        status, reasons = offer_decision_status(deal, packet)
        offers.append(
            {
                "deal_id": deal.id,
                "arv": deal.arv,
                "repairs": deal.repairs,
                "buyer_costs": deal.buyer_costs,
                "buyer_desired_profit": deal.buyer_desired_profit,
                "buyer_max_price": deal.max_buyer_purchase_price,
                "target_assignment_fee": deal.target_assignment_fee,
                "max_seller_offer": deal.max_seller_offer,
                "seller_asking_price": _lead_for_deal(session, deal).asking_price if _lead_for_deal(session, deal) else None,
                "recommended_offer_range": {
                    "conservative": deal.conservative_offer,
                    "standard": deal.standard_offer,
                    "aggressive": deal.aggressive_offer,
                },
                "buyer_margin_impact": buyer_margin(deal),
                "seller_reasonableness_notes": deal.seller_fairness_notes,
                "prime_2_recommendation": _offer_recommendation(status, reasons),
                "owner_approval_status": packet.approval_status if packet else "owner_review_required",
                "decision_status": status,
                "blocked_reasons": reasons,
            }
        )
    offers.sort(key=lambda item: item["buyer_margin_impact"], reverse=True)
    return {"offers": offers, "safety_boundary": execution_safety_boundary()}


def buyer_validation_board(session: Session) -> dict[str, object]:
    batch = active_execution_batch(session)
    rows: list[dict[str, object]] = []
    for deal in _deals_for_batch(session, batch):
        priority = _top_buyer_priority_for_deal(session, deal.id)
        buyer = session.get(Buyer, priority.buyer_id) if priority else None
        gate = buyer_validation_gate(deal, priority, buyer)
        rows.append(
            {
                "deal_id": deal.id,
                "top_buyer_match": buyer.name if buyer else "No buyer validated",
                "buyer_pof_status": buyer.proof_of_funds_status if buyer else "missing",
                "buyer_max_price_fit": priority.max_price_fit if priority else 0,
                "buyer_response_velocity": priority.closing_speed_score if priority else 0,
                "buyer_reliability_score": buyer.reliability_score if buyer else 0,
                "buyer_margin_strength": priority.buyer_margin_strength if priority else 0,
                "buyer_interest_status": _buyer_interest_status(deal),
                "access_showing_requirement": "Coordinate access only after owner-approved next step.",
                "buyer_objection_notes": priority.risk_flags if priority else ["buyer_validation_missing"],
                "gate": gate,
            }
        )
    return {"buyer_validations": rows, "safety_boundary": execution_safety_boundary()}


def contract_ready_board(session: Session) -> dict[str, object]:
    batch = active_execution_batch(session)
    rows: list[dict[str, object]] = []
    for deal in _deals_for_batch(session, batch):
        state = _contract_state_for_deal(session, deal.id)
        title = _title_review_for_deal(session, deal.id)
        gate = contract_ready_gate(state)
        rows.append(
            {
                "deal_id": deal.id,
                "checklist": {
                    "seller_motivation_confirmed": bool(state and state.seller_readiness_high),
                    "seller_terms_soft_accepted": bool(state and state.seller_likely_to_sign),
                    "underwriting_complete": bool(state and state.underwriting_complete),
                    "buyer_demand_validated": bool(state and state.buyer_demand_confirmed),
                    "offer_approved": bool(state and state.owner_approval_recorded),
                    "compliance_passed": bool(state and state.compliance_passed),
                    "assignment_readiness_checked": bool(state and state.profit_control_validated),
                    "title_attorney_review_prep_available": bool(state and state.ready_for_external_drafting),
                    "owner_approval_complete": bool(state and state.owner_approval_recorded),
                },
                "title_review_status": "ready" if title and title.packet_prep_allowed else "needed",
                "gate": gate,
                "contract_document_created": False,
                "external_drafting_required": True,
            }
        )
    return {"contract_ready_candidates": rows, "safety_boundary": execution_safety_boundary()}


def evidence_tracker(session: Session) -> dict[str, object]:
    batch = active_execution_batch(session)
    rows: list[dict[str, object]] = []
    for deal in _deals_for_batch(session, batch):
        attribution = _assignment_fee_for_deal(session, deal.id)
        packet = _evidence_packet_for_deal(session, deal.id)
        gate = evidence_gate(deal, attribution, packet)
        rows.append(
            {
                "deal_id": deal.id,
                "seller_target_price": _lead_for_deal(session, deal).asking_price if _lead_for_deal(session, deal) else None,
                "approved_offer_price": deal.seller_contract_price,
                "buyer_projected_price": attribution.buyer_purchase_price if attribution else deal.buyer_purchase_price,
                "projected_assignment_fee": attribution.projected_assignment_fee if attribution else deal.projected_assignment_fee,
                "buyer_margin": attribution.buyer_margin if attribution else buyer_margin(deal),
                "evidence_source_records": attribution.attribution_basis if attribution else [],
                "confidence_score": attribution.confidence_score if attribution else deal.confidence_score,
                "missing_proof": gate["blocked_reasons"],
                "risk_flags": deal.risk_flags,
                "gate": gate,
            }
        )
    return {"evidence_records": rows, "safety_boundary": execution_safety_boundary()}


def field_test_report(session: Session) -> dict[str, object]:
    batch = active_execution_batch(session)
    report = {
        "batch": sanitize_execution_record(batch),
        "leads_imported": len(_import_rows_for_batch(session, batch)),
        "leads_qa_passed": len(
            [review for review in session.query(LeadQualityReview).all() if not review.blocked_reasons]
        ),
        "calls_attempted": batch.calls_completed,
        "sellers_reached": session.query(FieldCallOutcome).filter(
            FieldCallOutcome.contact_result.in_(["spoke_to_owner", "motivated", "offer_requested", "appointment_set"])
        ).count(),
        "motivated_sellers": batch.motivated_sellers,
        "offers_prepared": batch.offers_prepared,
        "offers_presented": len([item for item in offer_decision_board(session)["offers"] if item["decision_status"] != "needs_data"]),
        "buyer_matches": batch.buyer_matches,
        "contract_ready_candidates": batch.contract_ready_count,
        "projected_assignment_fees": batch.projected_assignment_fees,
        "prediction_misses": _prediction_misses(session),
        "scoring_lessons": [
            "Keep call-priority high only when QA and contactability both support it.",
            "Require buyer validation before moving a seller opportunity toward contract-ready.",
        ],
        "next_batch_recommendations": [
            "Run a 10-lead QA batch in the strongest zip focus.",
            "Log every call outcome before changing scoring weights.",
            "Move only evidence-supported opportunities into owner decision review.",
        ],
        "learning_signal": _sync_report_learning_signal(session, batch),
        "safety_boundary": execution_safety_boundary(),
    }
    session.commit()
    return report


def execution_coach(session: Session) -> list[dict[str, object]]:
    batch = active_execution_batch(session)
    offers = offer_decision_board(session)["offers"]
    buyer_rows = buyer_validation_board(session)["buyer_validations"]
    evidence_rows = evidence_tracker(session)["evidence_records"]
    guidance = [
        ("call_next_seller", "Call this seller next", "Use the call-priority row with the highest QA score."),
        ("research_before_call", "Research this deal before calling", "Rows with missing contactability or valuation should stay in research."),
    ]
    for offer in offers[:3]:
        if offer["decision_status"] == "needs_data":
            guidance.append(("weak_or_missing_numbers", "Do not pursue: weak spread", f"{offer['deal_id']} needs data before offer review."))
        elif offer["decision_status"] == "ready_for_owner_review":
            guidance.append(("owner_decision", "Ready for owner decision", f"{offer['deal_id']} is ready for owner offer review."))
    for row in buyer_rows[:3]:
        if not row["gate"]["validated"]:
            guidance.append(("buyer_validation", "Need buyer validation before offer", f"{row['deal_id']} has buyer validation blockers."))
    for row in evidence_rows[:3]:
        if row["projected_assignment_fee"] >= batch.target_assignment_fee and not row["gate"]["evidence_supported"]:
            guidance.append(("evidence_gap", "Potential 10K spread but missing proof", f"{row['deal_id']} needs evidence cleanup."))
    return [
        {
            "id": key,
            "title": title,
            "recommendation": body,
            "safe_text": validate_execution_guidance_text(f"{title}. {body}"),
            "internal_recommendation_only": True,
        }
        for key, title, body in guidance
    ]


def _import_rows_for_batch(session: Session, batch: RealDealExecutionBatch) -> list[LeadImportRow]:
    query = session.query(LeadImportRow)
    if batch.lead_import_batch_id:
        query = query.filter(LeadImportRow.batch_id == batch.lead_import_batch_id)
    return query.order_by(LeadImportRow.row_number).all()


def _deals_for_batch(session: Session, batch: RealDealExecutionBatch) -> list[Deal]:
    deals = session.query(Deal).order_by(desc(Deal.projected_assignment_fee)).all()
    if not batch.market_zip_focus:
        return deals
    focused = [
        deal
        for deal in deals
        if (lead := _lead_for_deal(session, deal)) and lead.zip_code in batch.market_zip_focus
    ]
    other_deals = [deal for deal in deals if deal not in focused]
    return focused + other_deals


def _lead_for_deal(session: Session, deal: Deal) -> Lead | None:
    return session.get(Lead, deal.lead_id)


def _row_property(row: LeadImportRow) -> str:
    return f"{row.property_address}, {row.property_city}, {row.property_state} {row.property_zip}".strip(", ")


def _offer_packet_for_deal(session: Session, deal_id: str) -> OfferPacket | None:
    return (
        session.query(OfferPacket)
        .filter(OfferPacket.deal_id == deal_id)
        .order_by(desc(OfferPacket.created_at))
        .first()
    )


def _top_buyer_priority_for_deal(session: Session, deal_id: str) -> BuyerDealPriority | None:
    return (
        session.query(BuyerDealPriority)
        .filter(BuyerDealPriority.deal_id == deal_id)
        .order_by(desc(BuyerDealPriority.priority_score))
        .first()
    )


def _buyer_interest_status(deal: Deal) -> str:
    if not deal.buyer_interests:
        return "missing"
    return deal.buyer_interests[0].interest_status


def _contract_state_for_deal(session: Session, deal_id: str) -> ContractReadyState | None:
    return (
        session.query(ContractReadyState)
        .filter(ContractReadyState.deal_id == deal_id)
        .order_by(desc(ContractReadyState.created_at))
        .first()
    )


def _title_review_for_deal(session: Session, deal_id: str) -> TitleReviewCoordination | None:
    return (
        session.query(TitleReviewCoordination)
        .filter(TitleReviewCoordination.deal_id == deal_id)
        .order_by(desc(TitleReviewCoordination.created_at))
        .first()
    )


def _assignment_fee_for_deal(session: Session, deal_id: str) -> AssignmentFeeAttribution | None:
    return (
        session.query(AssignmentFeeAttribution)
        .filter(AssignmentFeeAttribution.deal_id == deal_id)
        .order_by(desc(AssignmentFeeAttribution.confidence_score))
        .first()
    )


def _evidence_packet_for_deal(session: Session, deal_id: str) -> DealEvidencePacket | None:
    return (
        session.query(DealEvidencePacket)
        .filter(DealEvidencePacket.deal_id == deal_id)
        .order_by(desc(DealEvidencePacket.created_at))
        .first()
    )


def _offer_recommendation(status: str, reasons: list[str]) -> str:
    if status == "ready_for_owner_review":
        return "Prime 2 recommends owner review of the standard offer option before any seller-facing action."
    if "buyer_margin_not_protected" in reasons:
        return "Offer is too aggressive for buyer margin; revise numbers before owner review."
    if "target_assignment_fee_not_met" in reasons:
        return "Spread is below target; hold or research a safer price path."
    if "compliance_review_needed" in reasons:
        return "Compliance review needed before offer decisioning."
    return "Research missing data before preparing an offer decision."


def _cockpit_blockers(
    session: Session,
    batch: RealDealExecutionBatch,
    deals: list[Deal],
) -> list[str]:
    blockers: set[str] = set()
    if not _import_rows_for_batch(session, batch):
        blockers.add("no_import_batch_rows")
    if batch.calls_completed == 0:
        blockers.add("seller_calls_not_logged")
    if not any(deal.projected_assignment_fee >= batch.target_assignment_fee for deal in deals):
        blockers.add("no_10k_candidate")
    for deal in deals[:3]:
        priority = _top_buyer_priority_for_deal(session, deal.id)
        buyer = session.get(Buyer, priority.buyer_id) if priority else None
        if not buyer_validation_gate(deal, priority, buyer)["validated"]:
            blockers.add("buyer_validation_needed")
        if not evidence_gate(
            deal,
            _assignment_fee_for_deal(session, deal.id),
            _evidence_packet_for_deal(session, deal.id),
        )["evidence_supported"]:
            blockers.add("assignment_fee_evidence_needed")
    return sorted(blockers)


def _next_best_action(batch: RealDealExecutionBatch) -> str:
    if "seller_calls_not_logged" in batch.blockers:
        return "Run the call checklist on the top call-priority lead and log the outcome."
    if "buyer_validation_needed" in batch.blockers:
        return "Validate buyer POF, price fit, and reliability before contract-ready review."
    if "assignment_fee_evidence_needed" in batch.blockers:
        return "Attach source-backed evidence before treating any spread as supported."
    return "Move the strongest evidence-backed opportunity to owner decision review."


def _prediction_misses(session: Session) -> list[str]:
    signals = (
        session.query(LearningSignal)
        .filter(LearningSignal.variance > 20)
        .order_by(desc(LearningSignal.variance))
        .limit(5)
        .all()
    )
    return [signal.explanation for signal in signals]


def _sync_report_learning_signal(
    session: Session,
    batch: RealDealExecutionBatch,
) -> dict[str, object]:
    signal = session.get(LearningSignal, "learning-signal-v31-first-batch")
    if signal is None:
        signal = LearningSignal(
            signal_id="learning-signal-v31-first-batch",
            signal_type="first_deal_batch_execution",
            source_domain="real_deal_execution",
            source_record_id=batch.id,
            predicted_value="10-lead batch can surface one owner-review candidate",
            actual_value=f"{batch.motivated_sellers} motivated sellers, {batch.contract_ready_count} contract-ready candidates",
            variance=max(0, 1 - batch.contract_ready_count) * 25,
            confidence=72,
            explanation="Prime 2 generated an advisory first-batch learning signal from execution counts.",
            recommended_adjustment="Review call QA and buyer validation before changing scoring weights.",
            owner_review_status="pending_review",
            evidence_basis=[batch.id, batch.lead_import_batch_id or "", "field_call_outcomes"],
            auto_applied=False,
            unsupported_claims_blocked=True,
        )
        session.add(signal)
        session.flush()
    return model_to_dict(signal)
