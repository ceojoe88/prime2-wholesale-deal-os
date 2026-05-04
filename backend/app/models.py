from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def utcnow() -> datetime:
    return datetime.now(UTC)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utcnow, onupdate=utcnow
    )


class Division(TimestampMixin, Base):
    __tablename__ = "divisions"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    manager_name: Mapped[str] = mapped_column(String(120), nullable=False)
    responsibilities: Mapped[list[str]] = mapped_column(JSON, default=list)
    priority_queue: Mapped[list[str]] = mapped_column(JSON, default=list)
    workload: Mapped[int] = mapped_column(Integer, default=0)
    active_recommendations: Mapped[list[str]] = mapped_column(JSON, default=list)
    risk_flags: Mapped[list[str]] = mapped_column(JSON, default=list)
    performance_notes: Mapped[str] = mapped_column(Text, default="")
    next_best_action: Mapped[str] = mapped_column(Text, default="")

    agents: Mapped[list["Agent"]] = relationship(back_populates="division")


class Agent(TimestampMixin, Base):
    __tablename__ = "agents"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(140), nullable=False)
    division_id: Mapped[str] = mapped_column(ForeignKey("divisions.id"), nullable=False)
    allowed_actions: Mapped[list[str]] = mapped_column(JSON, default=list)
    denied_actions: Mapped[list[str]] = mapped_column(JSON, default=list)
    current_focus: Mapped[str] = mapped_column(Text, default="")
    recommendation: Mapped[str] = mapped_column(Text, default="")
    risk_flags: Mapped[list[str]] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(40), default="active")

    division: Mapped[Division] = relationship(back_populates="agents")


class Lead(TimestampMixin, Base):
    __tablename__ = "leads"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    seller_name: Mapped[str] = mapped_column(String(120), nullable=False)
    address: Mapped[str] = mapped_column(String(180), nullable=False)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    state: Mapped[str] = mapped_column(String(20), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(20), nullable=False)
    property_type: Mapped[str] = mapped_column(String(80), nullable=False)
    source_category: Mapped[str] = mapped_column(String(80), nullable=False)
    stage: Mapped[str] = mapped_column(String(40), default="new_lead")
    asking_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estimated_equity: Mapped[int] = mapped_column(Integer, default=0)
    motivation_score: Mapped[float] = mapped_column(Float, default=0)
    distress_score: Mapped[float] = mapped_column(Float, default=0)
    equity_score: Mapped[float] = mapped_column(Float, default=0)
    urgency_score: Mapped[float] = mapped_column(Float, default=0)
    contactability_score: Mapped[float] = mapped_column(Float, default=0)
    seller_temperature: Mapped[float] = mapped_column(Float, default=0)
    data_confidence: Mapped[float] = mapped_column(Float, default=0)
    market_demand: Mapped[float] = mapped_column(Float, default=0)
    opportunity_score: Mapped[float] = mapped_column(Float, default=0)
    compliance_risk: Mapped[float] = mapped_column(Float, default=0)
    notes: Mapped[list[str]] = mapped_column(JSON, default=list)
    next_best_action: Mapped[str] = mapped_column(Text, default="")

    deals: Mapped[list["Deal"]] = relationship(back_populates="lead")
    seller_interactions: Mapped[list["SellerInteraction"]] = relationship(back_populates="lead")
    contract_controls: Mapped[list["ContractControl"]] = relationship(back_populates="lead")
    seller_offer_publications: Mapped[list["SellerOfferPublication"]] = relationship(
        back_populates="lead"
    )


class Deal(TimestampMixin, Base):
    __tablename__ = "deals"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    lead_id: Mapped[str] = mapped_column(ForeignKey("leads.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="researching")
    arv: Mapped[int] = mapped_column(Integer, nullable=False)
    repairs: Mapped[int] = mapped_column(Integer, nullable=False)
    buyer_costs: Mapped[int] = mapped_column(Integer, nullable=False)
    buyer_desired_profit: Mapped[int] = mapped_column(Integer, nullable=False)
    target_assignment_fee: Mapped[int] = mapped_column(Integer, default=10_000)
    max_buyer_purchase_price: Mapped[int] = mapped_column(Integer, nullable=False)
    max_seller_offer: Mapped[int] = mapped_column(Integer, nullable=False)
    seller_contract_price: Mapped[int] = mapped_column(Integer, nullable=False)
    buyer_purchase_price: Mapped[int] = mapped_column(Integer, nullable=False)
    projected_assignment_fee: Mapped[int] = mapped_column(Integer, nullable=False)
    offer_reasonableness_score: Mapped[float] = mapped_column(Float, default=0)
    spread_confidence_score: Mapped[float] = mapped_column(Float, default=0)
    risk_score: Mapped[float] = mapped_column(Float, default=0)
    confidence_score: Mapped[float] = mapped_column(Float, default=0)
    deal_speed_score: Mapped[float] = mapped_column(Float, default=0)
    risk_flags: Mapped[list[str]] = mapped_column(JSON, default=list)
    underwriting_notes: Mapped[str] = mapped_column(Text, default="")
    seller_fairness_notes: Mapped[str] = mapped_column(Text, default="")
    buyer_margin_notes: Mapped[str] = mapped_column(Text, default="")
    conservative_offer: Mapped[int] = mapped_column(Integer, default=0)
    standard_offer: Mapped[int] = mapped_column(Integer, default=0)
    aggressive_offer: Mapped[int] = mapped_column(Integer, default=0)
    owner_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    compliance_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    is_hot_opportunity: Mapped[bool] = mapped_column(Boolean, default=False)
    is_under_contract: Mapped[bool] = mapped_column(Boolean, default=False)

    lead: Mapped[Lead] = relationship(back_populates="deals")
    matches: Mapped[list["BuyerMatch"]] = relationship(back_populates="deal")
    compliance_records: Mapped[list["ComplianceRecord"]] = relationship(back_populates="deal")
    buyer_publication: Mapped["BuyerDealPublication | None"] = relationship(
        back_populates="deal", uselist=False
    )
    buyer_interests: Mapped[list["BuyerInterest"]] = relationship(back_populates="deal")
    offer_packets: Mapped[list["OfferPacket"]] = relationship(back_populates="deal")
    contract_controls: Mapped[list["ContractControl"]] = relationship(back_populates="deal")
    title_handoff_packets: Mapped[list["TitleHandoffPacket"]] = relationship(back_populates="deal")
    assignment_readiness_records: Mapped[list["AssignmentReadinessRecord"]] = relationship(
        back_populates="deal"
    )
    seller_offer_publications: Mapped[list["SellerOfferPublication"]] = relationship(
        back_populates="deal"
    )


class Buyer(TimestampMixin, Base):
    __tablename__ = "buyers"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    company: Mapped[str] = mapped_column(String(140), nullable=False)
    email: Mapped[str] = mapped_column(String(160), nullable=False)
    phone: Mapped[str] = mapped_column(String(40), nullable=False)
    target_zip_codes: Mapped[list[str]] = mapped_column(JSON, default=list)
    max_purchase_price: Mapped[int] = mapped_column(Integer, nullable=False)
    property_type: Mapped[str] = mapped_column(String(80), nullable=False)
    proof_of_funds_status: Mapped[str] = mapped_column(String(60), default="unverified")
    closing_speed_days: Mapped[int] = mapped_column(Integer, default=21)
    reliability_score: Mapped[float] = mapped_column(Float, default=0)
    past_performance: Mapped[str] = mapped_column(Text, default="")
    preferred_deal_type: Mapped[str] = mapped_column(String(80), default="assignment")
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    matches: Mapped[list["BuyerMatch"]] = relationship(back_populates="buyer")
    interests: Mapped[list["BuyerInterest"]] = relationship(back_populates="buyer")
    assignment_readiness_records: Mapped[list["AssignmentReadinessRecord"]] = relationship(
        back_populates="buyer"
    )


class BuyerMatch(TimestampMixin, Base):
    __tablename__ = "buyer_matches"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    buyer_id: Mapped[str] = mapped_column(ForeignKey("buyers.id"), nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    match_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    risk_flags: Mapped[list[str]] = mapped_column(JSON, default=list)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[str] = mapped_column(String(60), default="draft_match")

    deal: Mapped[Deal] = relationship(back_populates="matches")
    buyer: Mapped[Buyer] = relationship(back_populates="matches")
    assignment_readiness_records: Mapped[list["AssignmentReadinessRecord"]] = relationship(
        back_populates="buyer_match"
    )


class ComplianceRecord(TimestampMixin, Base):
    __tablename__ = "compliance_records"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(140), nullable=False)
    status: Mapped[str] = mapped_column(String(60), default="needs_review")
    required_confirmations: Mapped[list[str]] = mapped_column(JSON, default=list)
    risk_warnings: Mapped[list[str]] = mapped_column(JSON, default=list)
    blocked_actions: Mapped[list[str]] = mapped_column(JSON, default=list)
    attorney_title_review_required: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[str] = mapped_column(Text, default="")

    deal: Mapped[Deal] = relationship(back_populates="compliance_records")


class BuyerDealPublication(TimestampMixin, Base):
    __tablename__ = "buyer_deal_publications"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), unique=True, nullable=False)
    operator_marked_visible: Mapped[bool] = mapped_column(Boolean, default=False)
    compliance_reviewed: Mapped[bool] = mapped_column(Boolean, default=False)
    seller_contract_controlled: Mapped[bool] = mapped_column(Boolean, default=False)
    risk_status: Mapped[str] = mapped_column(String(40), default="review")
    availability_status: Mapped[str] = mapped_column(String(60), default="draft")
    asking_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    beds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    baths: Mapped[float | None] = mapped_column(Float, nullable=True)
    sqft: Mapped[int | None] = mapped_column(Integer, nullable=True)
    arv_low: Mapped[int | None] = mapped_column(Integer, nullable=True)
    arv_high: Mapped[int | None] = mapped_column(Integer, nullable=True)
    repair_low: Mapped[int | None] = mapped_column(Integer, nullable=True)
    repair_high: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estimated_buyer_margin: Mapped[int | None] = mapped_column(Integer, nullable=True)
    buyer_margin_status: Mapped[str] = mapped_column(String(40), default="review")
    photos_placeholder: Mapped[list[str]] = mapped_column(JSON, default=list)
    access_instructions_placeholder: Mapped[str] = mapped_column(Text, default="")
    blocked_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    deal: Mapped[Deal] = relationship(back_populates="buyer_publication")


class BuyerInterest(TimestampMixin, Base):
    __tablename__ = "buyer_interests"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    buyer_id: Mapped[str] = mapped_column(ForeignKey("buyers.id"), nullable=False)
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    interest_status: Mapped[str] = mapped_column(String(60), default="intent_draft")
    intended_offer_amount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    proof_of_funds_status: Mapped[str] = mapped_column(String(60), default="unverified")
    notes: Mapped[str] = mapped_column(Text, default="")
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    contract_execution_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    buyer: Mapped[Buyer] = relationship(back_populates="interests")
    deal: Mapped[Deal] = relationship(back_populates="buyer_interests")
    assignment_readiness_records: Mapped[list["AssignmentReadinessRecord"]] = relationship(
        back_populates="buyer_interest"
    )


class SellerInteraction(TimestampMixin, Base):
    __tablename__ = "seller_interactions"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    lead_id: Mapped[str] = mapped_column(ForeignKey("leads.id"), nullable=False)
    call_notes: Mapped[str] = mapped_column(Text, default="")
    motivation_answers: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)
    asking_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    timeline: Mapped[str] = mapped_column(String(120), default="")
    property_condition: Mapped[str] = mapped_column(Text, default="")
    pain_points: Mapped[list[str]] = mapped_column(JSON, default=list)
    objections: Mapped[list[str]] = mapped_column(JSON, default=list)
    next_follow_up_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    seller_temperature_score: Mapped[float] = mapped_column(Float, default=0)
    objection_status: Mapped[str] = mapped_column(String(80), default="unknown")
    follow_up_urgency: Mapped[str] = mapped_column(String(60), default="normal")
    next_best_seller_action: Mapped[str] = mapped_column(Text, default="")
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    live_outreach_allowed: Mapped[bool] = mapped_column(Boolean, default=False)

    lead: Mapped[Lead] = relationship(back_populates="seller_interactions")
    communication_drafts: Mapped[list["CommunicationDraft"]] = relationship(
        back_populates="seller_interaction"
    )


class OfferPacket(TimestampMixin, Base):
    __tablename__ = "offer_packets"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    packet_status: Mapped[str] = mapped_column(String(80), default="draft")
    owner_approval_recorded: Mapped[bool] = mapped_column(Boolean, default=False)
    compliance_guard_passed: Mapped[bool] = mapped_column(Boolean, default=False)
    buyer_margin_protected: Mapped[bool] = mapped_column(Boolean, default=False)
    target_assignment_fee_checked: Mapped[bool] = mapped_column(Boolean, default=False)
    underwriting_complete: Mapped[bool] = mapped_column(Boolean, default=False)
    packet_prep_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    blocked_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    approval_status: Mapped[str] = mapped_column(String(80), default="owner_review_required")
    draft_summary: Mapped[str] = mapped_column(Text, default="")
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    real_world_action_taken: Mapped[bool] = mapped_column(Boolean, default=False)

    deal: Mapped[Deal] = relationship(back_populates="offer_packets")
    contract_controls: Mapped[list["ContractControl"]] = relationship(back_populates="offer_packet")
    seller_offer_publications: Mapped[list["SellerOfferPublication"]] = relationship(
        back_populates="offer_packet"
    )


class ContractControl(TimestampMixin, Base):
    __tablename__ = "contract_controls"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    lead_id: Mapped[str] = mapped_column(ForeignKey("leads.id"), nullable=False)
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    offer_packet_id: Mapped[str] = mapped_column(ForeignKey("offer_packets.id"), nullable=False)
    seller_accepted_terms: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    contract_status: Mapped[str] = mapped_column(String(80), default="prep_review")
    assignment_allowed_flag: Mapped[bool] = mapped_column(Boolean, default=False)
    inspection_access_notes: Mapped[str] = mapped_column(Text, default="")
    earnest_money_notes: Mapped[str] = mapped_column(Text, default="")
    closing_timeline: Mapped[str] = mapped_column(String(120), default="")
    title_company_preference: Mapped[str] = mapped_column(String(160), default="")
    required_documents_checklist: Mapped[list[str]] = mapped_column(JSON, default=list)
    owner_approval_status: Mapped[str] = mapped_column(String(80), default="pending")
    compliance_review_status: Mapped[str] = mapped_column(String(80), default="pending")
    contract_prep_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    blocked_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    executable_contract_generated: Mapped[bool] = mapped_column(Boolean, default=False)
    live_sending_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    title_submission_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    automatic_status_change_allowed: Mapped[bool] = mapped_column(Boolean, default=False)

    lead: Mapped[Lead] = relationship(back_populates="contract_controls")
    deal: Mapped[Deal] = relationship(back_populates="contract_controls")
    offer_packet: Mapped[OfferPacket] = relationship(back_populates="contract_controls")
    title_handoff_packets: Mapped[list["TitleHandoffPacket"]] = relationship(
        back_populates="contract_control"
    )
    assignment_readiness_records: Mapped[list["AssignmentReadinessRecord"]] = relationship(
        back_populates="contract_control"
    )
    seller_offer_publications: Mapped[list["SellerOfferPublication"]] = relationship(
        back_populates="contract_control"
    )


class SellerOfferPublication(TimestampMixin, Base):
    __tablename__ = "seller_offer_publications"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    lead_id: Mapped[str] = mapped_column(ForeignKey("leads.id"), nullable=False)
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    offer_packet_id: Mapped[str] = mapped_column(ForeignKey("offer_packets.id"), nullable=False)
    contract_control_id: Mapped[str] = mapped_column(
        ForeignKey("contract_controls.id"), nullable=False
    )
    portal_visibility_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    offer_status: Mapped[str] = mapped_column(String(80), default="owner_review")
    offer_amount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    closing_timeline_estimate: Mapped[str] = mapped_column(String(120), default="")
    inspection_access_next_step: Mapped[str] = mapped_column(Text, default="")
    title_company_review_status: Mapped[str] = mapped_column(String(120), default="")
    document_checklist: Mapped[list[str]] = mapped_column(JSON, default=list)
    operator_contact_placeholder: Mapped[str] = mapped_column(Text, default="")
    offer_language: Mapped[str] = mapped_column(Text, default="")
    offer_language_safety_passed: Mapped[bool] = mapped_column(Boolean, default=False)
    offer_language_safety_result: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    compliance_check_passed: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_approval_recorded: Mapped[bool] = mapped_column(Boolean, default=False)
    visibility_status: Mapped[str] = mapped_column(String(80), default="draft")
    blocked_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    visible_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    contract_execution_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    live_negotiation_automation_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    legal_advice_provided: Mapped[bool] = mapped_column(Boolean, default=False)
    buyer_data_exposed: Mapped[bool] = mapped_column(Boolean, default=False)
    internal_profit_logic_exposed: Mapped[bool] = mapped_column(Boolean, default=False)

    lead: Mapped[Lead] = relationship(back_populates="seller_offer_publications")
    deal: Mapped[Deal] = relationship(back_populates="seller_offer_publications")
    offer_packet: Mapped[OfferPacket] = relationship(
        back_populates="seller_offer_publications"
    )
    contract_control: Mapped[ContractControl] = relationship(
        back_populates="seller_offer_publications"
    )
    seller_responses: Mapped[list["SellerPortalResponse"]] = relationship(
        back_populates="seller_offer_publication"
    )


class SellerPortalResponse(TimestampMixin, Base):
    __tablename__ = "seller_portal_responses"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    seller_offer_publication_id: Mapped[str] = mapped_column(
        ForeignKey("seller_offer_publications.id"), nullable=False
    )
    response_type: Mapped[str] = mapped_column(String(80), nullable=False)
    seller_portal_note: Mapped[str] = mapped_column(Text, default="")
    offer_question: Mapped[str] = mapped_column(Text, default="")
    appointment_access_preference: Mapped[str] = mapped_column(Text, default="")
    document_upload_placeholder: Mapped[str] = mapped_column(Text, default="")
    response_status: Mapped[str] = mapped_column(String(80), default="received")
    operator_review_status: Mapped[str] = mapped_column(String(80), default="pending_review")
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    negotiation_execution_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    contract_execution_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    automatic_acceptance_allowed: Mapped[bool] = mapped_column(Boolean, default=False)

    seller_offer_publication: Mapped[SellerOfferPublication] = relationship(
        back_populates="seller_responses"
    )


class TitleHandoffPacket(TimestampMixin, Base):
    __tablename__ = "title_handoff_packets"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    contract_control_id: Mapped[str] = mapped_column(
        ForeignKey("contract_controls.id"), nullable=False
    )
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    property_details: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    seller_info_placeholder: Mapped[str] = mapped_column(Text, default="")
    buyer_entity_info_placeholder: Mapped[str] = mapped_column(Text, default="")
    agreed_price: Mapped[int] = mapped_column(Integer, nullable=False)
    closing_timeline: Mapped[str] = mapped_column(String(120), default="")
    access_notes: Mapped[str] = mapped_column(Text, default="")
    assignment_status: Mapped[str] = mapped_column(String(80), default="assignment_review")
    required_document_checklist: Mapped[list[str]] = mapped_column(JSON, default=list)
    attorney_title_review_reminder: Mapped[str] = mapped_column(Text, default="")
    packet_status: Mapped[str] = mapped_column(String(80), default="draft")
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    title_submission_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    submitted_to_title: Mapped[bool] = mapped_column(Boolean, default=False)
    legal_advice_provided: Mapped[bool] = mapped_column(Boolean, default=False)

    contract_control: Mapped[ContractControl] = relationship(
        back_populates="title_handoff_packets"
    )
    deal: Mapped[Deal] = relationship(back_populates="title_handoff_packets")
    communication_drafts: Mapped[list["CommunicationDraft"]] = relationship(
        back_populates="title_handoff_packet"
    )


class AssignmentReadinessRecord(TimestampMixin, Base):
    __tablename__ = "assignment_readiness_records"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    contract_control_id: Mapped[str] = mapped_column(
        ForeignKey("contract_controls.id"), nullable=False
    )
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    buyer_id: Mapped[str | None] = mapped_column(ForeignKey("buyers.id"), nullable=True)
    buyer_match_id: Mapped[str | None] = mapped_column(
        ForeignKey("buyer_matches.id"), nullable=True
    )
    buyer_interest_id: Mapped[str | None] = mapped_column(
        ForeignKey("buyer_interests.id"), nullable=True
    )
    readiness_status: Mapped[str] = mapped_column(String(80), default="blocked")
    assignment_ready: Mapped[bool] = mapped_column(Boolean, default=False)
    blocked_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    assignment_allowed_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    buyer_pof_status: Mapped[str] = mapped_column(String(80), default="unverified")
    compliance_review_passed: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_approval_recorded: Mapped[bool] = mapped_column(Boolean, default=False)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    contract_execution_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    title_submission_allowed: Mapped[bool] = mapped_column(Boolean, default=False)

    contract_control: Mapped[ContractControl] = relationship(
        back_populates="assignment_readiness_records"
    )
    deal: Mapped[Deal] = relationship(back_populates="assignment_readiness_records")
    buyer: Mapped[Buyer | None] = relationship(back_populates="assignment_readiness_records")
    buyer_match: Mapped[BuyerMatch | None] = relationship(
        back_populates="assignment_readiness_records"
    )
    buyer_interest: Mapped[BuyerInterest | None] = relationship(
        back_populates="assignment_readiness_records"
    )


class CommunicationDraft(TimestampMixin, Base):
    __tablename__ = "communication_drafts"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    draft_type: Mapped[str] = mapped_column(String(80), nullable=False)
    channel: Mapped[str] = mapped_column(String(40), nullable=False)
    recipient_type: Mapped[str] = mapped_column(String(80), nullable=False)
    recipient_email_placeholder: Mapped[str] = mapped_column(String(180), default="")
    recipient_phone_placeholder: Mapped[str] = mapped_column(String(80), default="")
    source_record_type: Mapped[str] = mapped_column(String(80), nullable=False)
    source_record_id: Mapped[str] = mapped_column(String(80), nullable=False)
    seller_interaction_id: Mapped[str | None] = mapped_column(
        ForeignKey("seller_interactions.id"), nullable=True
    )
    buyer_interest_id: Mapped[str | None] = mapped_column(
        ForeignKey("buyer_interests.id"), nullable=True
    )
    title_handoff_packet_id: Mapped[str | None] = mapped_column(
        ForeignKey("title_handoff_packets.id"), nullable=True
    )
    subject: Mapped[str] = mapped_column(String(200), default="")
    draft_body: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(80), default="draft")
    safety_checked: Mapped[bool] = mapped_column(Boolean, default=False)
    safety_passed: Mapped[bool] = mapped_column(Boolean, default=False)
    safety_result: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    owner_approval_recorded: Mapped[bool] = mapped_column(Boolean, default=False)
    communication_live_flag_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    provider_readiness: Mapped[bool] = mapped_column(Boolean, default=False)
    last_dry_run_receipt_id: Mapped[str | None] = mapped_column(String(80), nullable=True)
    approved_dry_run_receipt_id: Mapped[str | None] = mapped_column(String(80), nullable=True)
    draft_hash: Mapped[str] = mapped_column(String(128), default="")
    risk_status: Mapped[str] = mapped_column(String(80), default="unchecked")
    blocked_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    live_send_count: Mapped[int] = mapped_column(Integer, default=0)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    bulk_send_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    campaign_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    auto_followup_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    buyer_blast_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    title_submission_allowed: Mapped[bool] = mapped_column(Boolean, default=False)

    seller_interaction: Mapped[SellerInteraction | None] = relationship(
        back_populates="communication_drafts"
    )
    buyer_interest: Mapped[BuyerInterest | None] = relationship()
    title_handoff_packet: Mapped[TitleHandoffPacket | None] = relationship(
        back_populates="communication_drafts"
    )
    dry_run_receipts: Mapped[list["CommunicationDryRunReceipt"]] = relationship(
        back_populates="draft"
    )
    approvals: Mapped[list["CommunicationApproval"]] = relationship(back_populates="draft")
    send_attempts: Mapped[list["CommunicationSendAttempt"]] = relationship(
        back_populates="draft"
    )


class CommunicationDryRunReceipt(TimestampMixin, Base):
    __tablename__ = "communication_dry_run_receipts"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    draft_id: Mapped[str] = mapped_column(
        ForeignKey("communication_drafts.id"), nullable=False
    )
    recipient: Mapped[str] = mapped_column(String(180), nullable=False)
    subject_body_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    source_record_type: Mapped[str] = mapped_column(String(80), nullable=False)
    source_record_id: Mapped[str] = mapped_column(String(80), nullable=False)
    risk_status: Mapped[str] = mapped_column(String(80), default="review")
    safety_result: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    provider_mode: Mapped[str] = mapped_column(String(80), default="mock/dry_run")
    idempotency_key: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)

    draft: Mapped[CommunicationDraft] = relationship(back_populates="dry_run_receipts")
    approvals: Mapped[list["CommunicationApproval"]] = relationship(back_populates="dry_run_receipt")
    send_attempts: Mapped[list["CommunicationSendAttempt"]] = relationship(
        back_populates="dry_run_receipt"
    )


class CommunicationApproval(TimestampMixin, Base):
    __tablename__ = "communication_approvals"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    draft_id: Mapped[str] = mapped_column(
        ForeignKey("communication_drafts.id"), nullable=False
    )
    dry_run_receipt_id: Mapped[str] = mapped_column(
        ForeignKey("communication_dry_run_receipts.id"), nullable=False
    )
    owner_approval_recorded: Mapped[bool] = mapped_column(Boolean, default=False)
    approval_status: Mapped[str] = mapped_column(String(80), default="pending")
    approval_notes: Mapped[str] = mapped_column(Text, default="")
    approved_by: Mapped[str] = mapped_column(String(80), default="Owner")
    draft_hash_at_approval: Mapped[str] = mapped_column(String(128), default="")

    draft: Mapped[CommunicationDraft] = relationship(back_populates="approvals")
    dry_run_receipt: Mapped[CommunicationDryRunReceipt] = relationship(
        back_populates="approvals"
    )


class CommunicationSendAttempt(TimestampMixin, Base):
    __tablename__ = "communication_send_attempts"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    draft_id: Mapped[str] = mapped_column(
        ForeignKey("communication_drafts.id"), nullable=False
    )
    dry_run_receipt_id: Mapped[str | None] = mapped_column(
        ForeignKey("communication_dry_run_receipts.id"), nullable=True
    )
    recipient: Mapped[str] = mapped_column(String(180), default="")
    channel: Mapped[str] = mapped_column(String(40), default="")
    provider_mode: Mapped[str] = mapped_column(String(80), default="mock/dry_run")
    attempt_status: Mapped[str] = mapped_column(String(80), default="blocked")
    blocked_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    safety_result: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    idempotency_key: Mapped[str] = mapped_column(String(160), default="")
    provider_called: Mapped[bool] = mapped_column(Boolean, default=False)
    mock_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    live_send_requested: Mapped[bool] = mapped_column(Boolean, default=False)
    bulk_send_detected: Mapped[bool] = mapped_column(Boolean, default=False)

    draft: Mapped[CommunicationDraft] = relationship(back_populates="send_attempts")
    dry_run_receipt: Mapped[CommunicationDryRunReceipt | None] = relationship(
        back_populates="send_attempts"
    )
