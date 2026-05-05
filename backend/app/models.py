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
    buyer_priorities: Mapped[list["BuyerDealPriority"]] = relationship(
        back_populates="deal"
    )
    distribution_preps: Mapped[list["DealDistributionPrep"]] = relationship(
        back_populates="deal"
    )
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
    unified_deal_rooms: Mapped[list["UnifiedDealRoom"]] = relationship(
        back_populates="deal"
    )
    evidence_packets: Mapped[list["DealEvidencePacket"]] = relationship(
        back_populates="deal"
    )
    assignment_fee_attributions: Mapped[list["AssignmentFeeAttribution"]] = relationship(
        back_populates="deal"
    )
    offer_positioning_records: Mapped[list["OfferPositioningRecord"]] = relationship(
        back_populates="deal"
    )
    negotiation_records: Mapped[list["NegotiationRecord"]] = relationship(
        back_populates="deal"
    )
    contract_ready_states: Mapped[list["ContractReadyState"]] = relationship(
        back_populates="deal"
    )
    title_review_coordinations: Mapped[list["TitleReviewCoordination"]] = relationship(
        back_populates="deal"
    )
    review_packet_preps: Mapped[list["ReviewPacketPrep"]] = relationship(
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
    demand_profile: Mapped["BuyerDemandProfile | None"] = relationship(
        back_populates="buyer", uselist=False
    )
    deal_priorities: Mapped[list["BuyerDealPriority"]] = relationship(
        back_populates="buyer"
    )
    distribution_preps: Mapped[list["DealDistributionPrep"]] = relationship(
        back_populates="buyer"
    )
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


class BuyerDemandProfile(TimestampMixin, Base):
    __tablename__ = "buyer_demand_profiles"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    buyer_id: Mapped[str] = mapped_column(ForeignKey("buyers.id"), unique=True, nullable=False)
    buyer_activity_score: Mapped[float] = mapped_column(Float, default=0)
    zip_code_demand_score: Mapped[float] = mapped_column(Float, default=0)
    property_type_demand_score: Mapped[float] = mapped_column(Float, default=0)
    price_band_fit_score: Mapped[float] = mapped_column(Float, default=0)
    closing_speed_score: Mapped[float] = mapped_column(Float, default=0)
    proof_of_funds_strength: Mapped[float] = mapped_column(Float, default=0)
    reliability_score: Mapped[float] = mapped_column(Float, default=0)
    last_engaged_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    preferred_spread_margin_notes: Mapped[str] = mapped_column(Text, default="")
    target_zip_codes: Mapped[list[str]] = mapped_column(JSON, default=list)
    property_type: Mapped[str] = mapped_column(String(80), default="any")
    price_band: Mapped[str] = mapped_column(String(80), default="")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)

    buyer: Mapped[Buyer] = relationship(back_populates="demand_profile")
    deal_priorities: Mapped[list["BuyerDealPriority"]] = relationship(
        back_populates="demand_profile"
    )


class BuyerDealPriority(TimestampMixin, Base):
    __tablename__ = "buyer_deal_priorities"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    buyer_id: Mapped[str] = mapped_column(ForeignKey("buyers.id"), nullable=False)
    buyer_demand_profile_id: Mapped[str | None] = mapped_column(
        ForeignKey("buyer_demand_profiles.id"), nullable=True
    )
    target_area_match: Mapped[float] = mapped_column(Float, default=0)
    max_price_fit: Mapped[float] = mapped_column(Float, default=0)
    proof_of_funds_score: Mapped[float] = mapped_column(Float, default=0)
    past_reliability_score: Mapped[float] = mapped_column(Float, default=0)
    closing_speed_score: Mapped[float] = mapped_column(Float, default=0)
    deal_type_fit: Mapped[float] = mapped_column(Float, default=0)
    buyer_margin_strength: Mapped[float] = mapped_column(Float, default=0)
    priority_score: Mapped[float] = mapped_column(Float, default=0)
    rank: Mapped[int] = mapped_column(Integer, default=0)
    ranking_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    risk_flags: Mapped[list[str]] = mapped_column(JSON, default=list)
    recommended_next_step: Mapped[str] = mapped_column(Text, default="")
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    live_contact_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    buyer_blast_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    internal_profit_logic_exposed: Mapped[bool] = mapped_column(Boolean, default=False)

    deal: Mapped[Deal] = relationship(back_populates="buyer_priorities")
    buyer: Mapped[Buyer] = relationship(back_populates="deal_priorities")
    demand_profile: Mapped[BuyerDemandProfile | None] = relationship(
        back_populates="deal_priorities"
    )
    distribution_preps: Mapped[list["DealDistributionPrep"]] = relationship(
        back_populates="buyer_priority"
    )


class DealDistributionPrep(TimestampMixin, Base):
    __tablename__ = "deal_distribution_preps"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    buyer_id: Mapped[str | None] = mapped_column(ForeignKey("buyers.id"), nullable=True)
    buyer_priority_id: Mapped[str | None] = mapped_column(
        ForeignKey("buyer_deal_priorities.id"), nullable=True
    )
    buyer_deal_publication_id: Mapped[str | None] = mapped_column(
        ForeignKey("buyer_deal_publications.id"), nullable=True
    )
    buyer_deal_email_draft: Mapped[str] = mapped_column(Text, default="")
    buyer_sms_draft: Mapped[str] = mapped_column(Text, default="")
    private_deal_sheet_draft: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    buyer_call_notes: Mapped[str] = mapped_column(Text, default="")
    buyer_response_tracker: Mapped[list[dict[str, object]]] = mapped_column(JSON, default=list)
    approval_status: Mapped[str] = mapped_column(String(80), default="owner_review_needed")
    draft_status: Mapped[str] = mapped_column(String(80), default="draft")
    safety_status: Mapped[str] = mapped_column(String(80), default="pending")
    blocked_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    live_send_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    bulk_blast_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    seller_private_data_exposed: Mapped[bool] = mapped_column(Boolean, default=False)
    assignment_fee_exposed: Mapped[bool] = mapped_column(Boolean, default=False)
    legal_closing_guarantee_allowed: Mapped[bool] = mapped_column(Boolean, default=False)

    deal: Mapped[Deal] = relationship(back_populates="distribution_preps")
    buyer: Mapped[Buyer | None] = relationship(back_populates="distribution_preps")
    buyer_priority: Mapped[BuyerDealPriority | None] = relationship(
        back_populates="distribution_preps"
    )
    buyer_deal_publication: Mapped[BuyerDealPublication | None] = relationship()


class OfferPositioningRecord(TimestampMixin, Base):
    __tablename__ = "offer_positioning_records"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    offer_packet_id: Mapped[str | None] = mapped_column(
        ForeignKey("offer_packets.id"), nullable=True
    )
    offer_strategy_type: Mapped[str] = mapped_column(String(80), default="as-is")
    seller_pain_alignment: Mapped[list[str]] = mapped_column(JSON, default=list)
    justification_summary: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    anchor_price: Mapped[int] = mapped_column(Integer, default=0)
    walk_away_price: Mapped[int] = mapped_column(Integer, default=0)
    ideal_contract_price: Mapped[int] = mapped_column(Integer, default=0)
    concession_range: Mapped[dict[str, int]] = mapped_column(JSON, default=dict)
    negotiation_notes: Mapped[str] = mapped_column(Text, default="")
    confidence_score: Mapped[float] = mapped_column(Float, default=0)
    owner_approval_recorded: Mapped[bool] = mapped_column(Boolean, default=False)
    safety_status: Mapped[str] = mapped_column(String(80), default="pending")
    blocked_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    pressure_tactics_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    legal_advice_allowed: Mapped[bool] = mapped_column(Boolean, default=False)

    deal: Mapped[Deal] = relationship(back_populates="offer_positioning_records")
    offer_packet: Mapped[OfferPacket | None] = relationship()
    negotiation_records: Mapped[list["NegotiationRecord"]] = relationship(
        back_populates="offer_positioning"
    )
    contract_ready_states: Mapped[list["ContractReadyState"]] = relationship(
        back_populates="offer_positioning"
    )


class NegotiationRecord(TimestampMixin, Base):
    __tablename__ = "negotiation_records"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    offer_positioning_id: Mapped[str | None] = mapped_column(
        ForeignKey("offer_positioning_records.id"), nullable=True
    )
    seller_interaction_id: Mapped[str | None] = mapped_column(
        ForeignKey("seller_interactions.id"), nullable=True
    )
    seller_last_response: Mapped[str] = mapped_column(Text, default="")
    seller_objections: Mapped[list[str]] = mapped_column(JSON, default=list)
    counter_offer: Mapped[int | None] = mapped_column(Integer, nullable=True)
    emotional_signals: Mapped[list[str]] = mapped_column(JSON, default=list)
    negotiation_stage: Mapped[str] = mapped_column(String(80), default="initial")
    next_move_recommendation: Mapped[str] = mapped_column(Text, default="")
    motivation_score: Mapped[float] = mapped_column(Float, default=0)
    price_alignment: Mapped[float] = mapped_column(Float, default=0)
    timeline_alignment: Mapped[float] = mapped_column(Float, default=0)
    trust_level: Mapped[float] = mapped_column(Float, default=0)
    objection_resolution: Mapped[float] = mapped_column(Float, default=0)
    contact_consistency: Mapped[float] = mapped_column(Float, default=0)
    readiness_score: Mapped[float] = mapped_column(Float, default=0)
    readiness_level: Mapped[str] = mapped_column(String(80), default="low_readiness")
    safety_status: Mapped[str] = mapped_column(String(80), default="pending")
    blocked_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    automatic_acceptance_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    live_negotiation_automation_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    pressure_tactics_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    legal_advice_allowed: Mapped[bool] = mapped_column(Boolean, default=False)

    deal: Mapped[Deal] = relationship(back_populates="negotiation_records")
    offer_positioning: Mapped[OfferPositioningRecord | None] = relationship(
        back_populates="negotiation_records"
    )
    seller_interaction: Mapped[SellerInteraction | None] = relationship()
    contract_ready_states: Mapped[list["ContractReadyState"]] = relationship(
        back_populates="negotiation_record"
    )


class ContractReadyState(TimestampMixin, Base):
    __tablename__ = "contract_ready_states"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    offer_positioning_id: Mapped[str | None] = mapped_column(
        ForeignKey("offer_positioning_records.id"), nullable=True
    )
    negotiation_record_id: Mapped[str | None] = mapped_column(
        ForeignKey("negotiation_records.id"), nullable=True
    )
    readiness_status: Mapped[str] = mapped_column(String(80), default="blocked")
    contract_ready: Mapped[bool] = mapped_column(Boolean, default=False)
    ready_for_external_drafting: Mapped[bool] = mapped_column(Boolean, default=False)
    seller_likely_to_sign: Mapped[bool] = mapped_column(Boolean, default=False)
    numbers_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    negotiation_stabilized: Mapped[bool] = mapped_column(Boolean, default=False)
    underwriting_complete: Mapped[bool] = mapped_column(Boolean, default=False)
    profit_control_validated: Mapped[bool] = mapped_column(Boolean, default=False)
    buyer_demand_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    compliance_passed: Mapped[bool] = mapped_column(Boolean, default=False)
    no_risk_flags: Mapped[bool] = mapped_column(Boolean, default=False)
    seller_readiness_high: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_approval_recorded: Mapped[bool] = mapped_column(Boolean, default=False)
    blocked_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    fastest_path_to_contract: Mapped[list[str]] = mapped_column(JSON, default=list)
    projected_assignment_fee: Mapped[int] = mapped_column(Integer, default=0)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    external_attorney_title_drafting_required: Mapped[bool] = mapped_column(
        Boolean, default=True
    )
    executable_contract_generated: Mapped[bool] = mapped_column(Boolean, default=False)
    contract_execution_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    legal_advice_provided: Mapped[bool] = mapped_column(Boolean, default=False)
    automatic_acceptance_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    live_negotiation_automation_allowed: Mapped[bool] = mapped_column(Boolean, default=False)

    deal: Mapped[Deal] = relationship(back_populates="contract_ready_states")
    offer_positioning: Mapped[OfferPositioningRecord | None] = relationship(
        back_populates="contract_ready_states"
    )
    negotiation_record: Mapped[NegotiationRecord | None] = relationship(
        back_populates="contract_ready_states"
    )
    title_review_coordinations: Mapped[list["TitleReviewCoordination"]] = relationship(
        back_populates="contract_ready_state"
    )


class TitleReviewCoordination(TimestampMixin, Base):
    __tablename__ = "title_review_coordinations"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    contract_ready_state_id: Mapped[str | None] = mapped_column(
        ForeignKey("contract_ready_states.id"), nullable=True
    )
    selected_title_company_placeholder: Mapped[str] = mapped_column(Text, default="")
    attorney_title_review_status: Mapped[str] = mapped_column(
        String(80), default="not_started"
    )
    required_documents: Mapped[list[str]] = mapped_column(JSON, default=list)
    missing_items: Mapped[list[str]] = mapped_column(JSON, default=list)
    review_notes: Mapped[str] = mapped_column(Text, default="")
    owner_approval_status: Mapped[str] = mapped_column(String(80), default="pending")
    packet_prep_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    blocked_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    legal_advice_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    contract_execution_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    document_submission_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    title_company_email_send_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    attorney_client_relationship_claimed: Mapped[bool] = mapped_column(
        Boolean, default=False
    )
    closing_guarantee_allowed: Mapped[bool] = mapped_column(Boolean, default=False)

    deal: Mapped[Deal] = relationship(back_populates="title_review_coordinations")
    contract_ready_state: Mapped[ContractReadyState | None] = relationship(
        back_populates="title_review_coordinations"
    )
    review_packets: Mapped[list["ReviewPacketPrep"]] = relationship(
        back_populates="title_review_coordination"
    )


class ReviewPacketPrep(TimestampMixin, Base):
    __tablename__ = "review_packet_preps"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    title_review_coordination_id: Mapped[str] = mapped_column(
        ForeignKey("title_review_coordinations.id"), nullable=False
    )
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    property_summary: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    seller_terms: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    buyer_assignment_readiness_summary: Mapped[dict[str, object]] = mapped_column(
        JSON, default=dict
    )
    closing_timeline: Mapped[str] = mapped_column(String(120), default="")
    access_notes: Mapped[str] = mapped_column(Text, default="")
    compliance_checklist: Mapped[list[str]] = mapped_column(JSON, default=list)
    document_checklist: Mapped[list[str]] = mapped_column(JSON, default=list)
    packet_status: Mapped[str] = mapped_column(String(80), default="draft")
    prep_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    blocked_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    legal_advice_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    contract_execution_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    document_submission_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    title_company_email_send_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    submitted_to_title: Mapped[bool] = mapped_column(Boolean, default=False)
    attorney_client_relationship_claimed: Mapped[bool] = mapped_column(
        Boolean, default=False
    )
    closing_guarantee_allowed: Mapped[bool] = mapped_column(Boolean, default=False)

    title_review_coordination: Mapped[TitleReviewCoordination] = relationship(
        back_populates="review_packets"
    )
    deal: Mapped[Deal] = relationship(back_populates="review_packet_preps")


class AutomationRule(TimestampMixin, Base):
    __tablename__ = "automation_rules"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    workflow_type: Mapped[str] = mapped_column(String(80), nullable=False)
    autonomy_level: Mapped[int] = mapped_column(Integer, default=2)
    trigger_event: Mapped[str] = mapped_column(String(120), default="")
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    allowed_actions: Mapped[list[str]] = mapped_column(JSON, default=list)
    blocked_actions: Mapped[list[str]] = mapped_column(JSON, default=list)
    schedule_label: Mapped[str] = mapped_column(String(120), default="")
    owner_approval_required: Mapped[bool] = mapped_column(Boolean, default=False)
    safety_status: Mapped[str] = mapped_column(String(80), default="guarded")
    last_run_status: Mapped[str] = mapped_column(String(80), default="not_run")
    idempotency_key: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    live_action_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    level_5_disabled: Mapped[bool] = mapped_column(Boolean, default=True)
    portal_publish_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    contract_execution_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    title_submission_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    payment_collection_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str] = mapped_column(Text, default="")

    runs: Mapped[list["SchedulerRun"]] = relationship(back_populates="rule")
    tasks: Mapped[list["AutonomousAgentTask"]] = relationship(back_populates="rule")
    event_triggers: Mapped[list["AutomationEventTrigger"]] = relationship(
        back_populates="rule"
    )


class SchedulerRun(TimestampMixin, Base):
    __tablename__ = "scheduler_runs"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    rule_id: Mapped[str | None] = mapped_column(
        ForeignKey("automation_rules.id"), nullable=True
    )
    workflow_type: Mapped[str] = mapped_column(String(80), nullable=False)
    run_status: Mapped[str] = mapped_column(String(80), default="queued")
    scheduled_for: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    idempotency_key: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    created_tasks: Mapped[int] = mapped_column(Integer, default=0)
    created_attempts: Mapped[int] = mapped_column(Integer, default=0)
    escalation_created: Mapped[bool] = mapped_column(Boolean, default=False)
    daily_briefing_created: Mapped[bool] = mapped_column(Boolean, default=False)
    summary: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    owner_approval_required: Mapped[bool] = mapped_column(Boolean, default=False)
    autonomy_level: Mapped[int] = mapped_column(Integer, default=2)
    idempotent_replay: Mapped[bool] = mapped_column(Boolean, default=False)
    real_world_action_taken: Mapped[bool] = mapped_column(Boolean, default=False)

    rule: Mapped[AutomationRule | None] = relationship(back_populates="runs")
    attempts: Mapped[list["AutomationAttempt"]] = relationship(back_populates="run")
    tasks: Mapped[list["AutonomousAgentTask"]] = relationship(back_populates="run")
    briefings: Mapped[list["DailyCommandBriefing"]] = relationship(back_populates="run")
    escalations: Mapped[list["AutonomyEscalation"]] = relationship(back_populates="run")


class AutomationAttempt(TimestampMixin, Base):
    __tablename__ = "automation_attempts"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    run_id: Mapped[str | None] = mapped_column(ForeignKey("scheduler_runs.id"), nullable=True)
    action_type: Mapped[str] = mapped_column(String(100), nullable=False)
    source_record_type: Mapped[str] = mapped_column(String(100), default="")
    source_record_id: Mapped[str] = mapped_column(String(100), default="")
    attempt_status: Mapped[str] = mapped_column(String(80), default="blocked")
    autonomy_level: Mapped[int] = mapped_column(Integer, default=2)
    safety_result: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    blocked_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    owner_approval_required: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_approval_recorded: Mapped[bool] = mapped_column(Boolean, default=False)
    provider_called: Mapped[bool] = mapped_column(Boolean, default=False)
    real_world_action_taken: Mapped[bool] = mapped_column(Boolean, default=False)
    idempotency_key: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)

    run: Mapped[SchedulerRun | None] = relationship(back_populates="attempts")


class AutonomousAgentTask(TimestampMixin, Base):
    __tablename__ = "autonomous_agent_tasks"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    rule_id: Mapped[str | None] = mapped_column(
        ForeignKey("automation_rules.id"), nullable=True
    )
    run_id: Mapped[str | None] = mapped_column(ForeignKey("scheduler_runs.id"), nullable=True)
    agent_name: Mapped[str] = mapped_column(String(140), nullable=False)
    division: Mapped[str] = mapped_column(String(140), nullable=False)
    task_type: Mapped[str] = mapped_column(String(100), nullable=False)
    source_record_type: Mapped[str] = mapped_column(String(100), default="")
    source_record_id: Mapped[str] = mapped_column(String(100), default="")
    priority: Mapped[str] = mapped_column(String(40), default="normal")
    status: Mapped[str] = mapped_column(String(80), default="queued")
    recommendation: Mapped[str] = mapped_column(Text, default="")
    due_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    idempotency_key: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    owner_approval_required: Mapped[bool] = mapped_column(Boolean, default=False)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    live_action_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    readiness_marked: Mapped[bool] = mapped_column(Boolean, default=False)

    rule: Mapped[AutomationRule | None] = relationship(back_populates="tasks")
    run: Mapped[SchedulerRun | None] = relationship(back_populates="tasks")


class AutomationEventTrigger(TimestampMixin, Base):
    __tablename__ = "automation_event_triggers"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    rule_id: Mapped[str | None] = mapped_column(
        ForeignKey("automation_rules.id"), nullable=True
    )
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    source_record_type: Mapped[str] = mapped_column(String(100), default="")
    source_record_id: Mapped[str] = mapped_column(String(100), default="")
    workflow_type: Mapped[str] = mapped_column(String(80), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(80), default="queued")
    idempotency_key: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    processed: Mapped[bool] = mapped_column(Boolean, default=False)

    rule: Mapped[AutomationRule | None] = relationship(back_populates="event_triggers")


class DailyCommandBriefing(TimestampMixin, Base):
    __tablename__ = "daily_command_briefings"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    run_id: Mapped[str | None] = mapped_column(ForeignKey("scheduler_runs.id"), nullable=True)
    briefing_date: Mapped[str] = mapped_column(String(40), nullable=False)
    generated_by: Mapped[str] = mapped_column(String(120), default="Wholesale Prime")
    hot_deals: Mapped[list[dict[str, object]]] = mapped_column(JSON, default=list)
    priority_actions: Mapped[list[str]] = mapped_column(JSON, default=list)
    manager_queue: Mapped[list[dict[str, object]]] = mapped_column(JSON, default=list)
    escalations: Mapped[list[dict[str, object]]] = mapped_column(JSON, default=list)
    safety_summary: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    owner_review_items: Mapped[list[str]] = mapped_column(JSON, default=list)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    legal_advice_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    live_outreach_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    portal_publish_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    title_submission_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    contract_execution_allowed: Mapped[bool] = mapped_column(Boolean, default=False)

    run: Mapped[SchedulerRun | None] = relationship(back_populates="briefings")


class AutonomyEscalation(TimestampMixin, Base):
    __tablename__ = "autonomy_escalations"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    run_id: Mapped[str | None] = mapped_column(ForeignKey("scheduler_runs.id"), nullable=True)
    deal_id: Mapped[str | None] = mapped_column(ForeignKey("deals.id"), nullable=True)
    lead_id: Mapped[str | None] = mapped_column(ForeignKey("leads.id"), nullable=True)
    escalation_type: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(40), default="medium")
    reason: Mapped[str] = mapped_column(Text, default="")
    recommended_action: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(80), default="open")
    owner_action_required: Mapped[bool] = mapped_column(Boolean, default=True)
    autonomy_level: Mapped[int] = mapped_column(Integer, default=3)
    real_world_action_blocked: Mapped[bool] = mapped_column(Boolean, default=True)
    idempotency_key: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)

    run: Mapped[SchedulerRun | None] = relationship(back_populates="escalations")


class AutoExecutionRule(TimestampMixin, Base):
    __tablename__ = "auto_execution_rules"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    rule_name: Mapped[str] = mapped_column(String(160), nullable=False)
    action_type: Mapped[str] = mapped_column(String(100), nullable=False)
    source_type: Mapped[str] = mapped_column(String(100), default="")
    allowed_recipient_type: Mapped[str] = mapped_column(String(100), default="")
    trigger: Mapped[str] = mapped_column(String(140), default="")
    required_conditions: Mapped[list[str]] = mapped_column(JSON, default=list)
    approved_template_id: Mapped[str | None] = mapped_column(
        ForeignKey("approved_templates.id"), nullable=True
    )
    autonomy_level: Mapped[int] = mapped_column(Integer, default=3)
    live_flag_required: Mapped[bool] = mapped_column(Boolean, default=True)
    risk_score: Mapped[float] = mapped_column(Float, default=0)
    owner_approval_status: Mapped[str] = mapped_column(String(80), default="pending")
    status: Mapped[str] = mapped_column(String(80), default="draft")
    blocked_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    bulk_send_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    buyer_blast_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    legal_contract_message_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    cold_sms_allowed: Mapped[bool] = mapped_column(Boolean, default=False)

    approved_template: Mapped["ApprovedTemplate | None"] = relationship(
        back_populates="rules"
    )
    dry_runs: Mapped[list["AutoExecutionDryRun"]] = relationship(back_populates="rule")
    attempts: Mapped[list["AutoExecutionAttempt"]] = relationship(back_populates="rule")
    audit_records: Mapped[list["AutoExecutionAuditRecord"]] = relationship(
        back_populates="rule"
    )


class ApprovedTemplate(TimestampMixin, Base):
    __tablename__ = "approved_templates"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    template_name: Mapped[str] = mapped_column(String(160), nullable=False)
    template_type: Mapped[str] = mapped_column(String(100), nullable=False)
    channel: Mapped[str] = mapped_column(String(60), default="internal")
    recipient_type: Mapped[str] = mapped_column(String(100), default="")
    subject: Mapped[str] = mapped_column(String(180), default="")
    body: Mapped[str] = mapped_column(Text, default="")
    approved: Mapped[bool] = mapped_column(Boolean, default=False)
    safety_status: Mapped[str] = mapped_column(String(80), default="unchecked")
    risk_flags: Mapped[list[str]] = mapped_column(JSON, default=list)
    requires_opt_out: Mapped[bool] = mapped_column(Boolean, default=False)
    includes_opt_out: Mapped[bool] = mapped_column(Boolean, default=False)
    legal_advice_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    pressure_language_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    fake_urgency_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    fake_buyer_claim_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    draft_only_default: Mapped[bool] = mapped_column(Boolean, default=True)

    rules: Mapped[list[AutoExecutionRule]] = relationship(
        back_populates="approved_template"
    )
    dry_runs: Mapped[list["AutoExecutionDryRun"]] = relationship(
        back_populates="template"
    )
    attempts: Mapped[list["AutoExecutionAttempt"]] = relationship(
        back_populates="template"
    )


class AutoExecutionDryRun(TimestampMixin, Base):
    __tablename__ = "auto_execution_dry_runs"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    rule_id: Mapped[str] = mapped_column(ForeignKey("auto_execution_rules.id"))
    template_id: Mapped[str] = mapped_column(ForeignKey("approved_templates.id"))
    source_record_type: Mapped[str] = mapped_column(String(100), default="")
    source_record_id: Mapped[str] = mapped_column(String(100), default="")
    recipient_type: Mapped[str] = mapped_column(String(100), default="")
    recipient_placeholder: Mapped[str] = mapped_column(String(180), default="")
    subject_body_hash: Mapped[str] = mapped_column(String(160), default="")
    safety_passed: Mapped[bool] = mapped_column(Boolean, default=False)
    safety_result: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    risk_status: Mapped[str] = mapped_column(String(80), default="unchecked")
    provider_mode: Mapped[str] = mapped_column(String(80), default="mock/dry_run")
    idempotency_key: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(80), default="created")

    rule: Mapped[AutoExecutionRule] = relationship(back_populates="dry_runs")
    template: Mapped[ApprovedTemplate] = relationship(back_populates="dry_runs")


class AutoExecutionAttempt(TimestampMixin, Base):
    __tablename__ = "auto_execution_attempts"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    rule_id: Mapped[str | None] = mapped_column(
        ForeignKey("auto_execution_rules.id"), nullable=True
    )
    template_id: Mapped[str | None] = mapped_column(
        ForeignKey("approved_templates.id"), nullable=True
    )
    dry_run_id: Mapped[str | None] = mapped_column(
        ForeignKey("auto_execution_dry_runs.id"), nullable=True
    )
    action_type: Mapped[str] = mapped_column(String(100), nullable=False)
    source_record_type: Mapped[str] = mapped_column(String(100), default="")
    source_record_id: Mapped[str] = mapped_column(String(100), default="")
    recipient_type: Mapped[str] = mapped_column(String(100), default="")
    recipient_count: Mapped[int] = mapped_column(Integer, default=1)
    attempt_status: Mapped[str] = mapped_column(String(80), default="blocked")
    blocked_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    safety_result: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    owner_approval_recorded: Mapped[bool] = mapped_column(Boolean, default=False)
    v5_safety_passed: Mapped[bool] = mapped_column(Boolean, default=False)
    v5_dry_run_receipt_exists: Mapped[bool] = mapped_column(Boolean, default=False)
    v5_approval_recorded: Mapped[bool] = mapped_column(Boolean, default=False)
    live_flags_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    provider_ready: Mapped[bool] = mapped_column(Boolean, default=False)
    provider_called: Mapped[bool] = mapped_column(Boolean, default=False)
    provider_mode: Mapped[str] = mapped_column(String(80), default="mock/dry_run")
    idempotency_key: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    audit_record_created: Mapped[bool] = mapped_column(Boolean, default=False)

    rule: Mapped[AutoExecutionRule | None] = relationship(back_populates="attempts")
    template: Mapped[ApprovedTemplate | None] = relationship(back_populates="attempts")
    dry_run: Mapped[AutoExecutionDryRun | None] = relationship()


class AutoExecutionAuditRecord(TimestampMixin, Base):
    __tablename__ = "auto_execution_audit_records"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    attempt_id: Mapped[str | None] = mapped_column(
        ForeignKey("auto_execution_attempts.id"), nullable=True
    )
    rule_id: Mapped[str | None] = mapped_column(
        ForeignKey("auto_execution_rules.id"), nullable=True
    )
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    source_record_type: Mapped[str] = mapped_column(String(100), default="")
    source_record_id: Mapped[str] = mapped_column(String(100), default="")
    outcome: Mapped[str] = mapped_column(String(100), default="blocked")
    blocked_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    safety_snapshot: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    provider_called: Mapped[bool] = mapped_column(Boolean, default=False)
    idempotency_key: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)

    rule: Mapped[AutoExecutionRule | None] = relationship(back_populates="audit_records")
    attempt: Mapped[AutoExecutionAttempt | None] = relationship()


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
    unified_deal_rooms: Mapped[list["UnifiedDealRoom"]] = relationship(
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


class UnifiedDealRoom(TimestampMixin, Base):
    __tablename__ = "unified_deal_rooms"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    contract_control_id: Mapped[str] = mapped_column(
        ForeignKey("contract_controls.id"), nullable=False
    )
    seller_offer_publication_id: Mapped[str | None] = mapped_column(
        ForeignKey("seller_offer_publications.id"), nullable=True
    )
    buyer_deal_publication_id: Mapped[str | None] = mapped_column(
        ForeignKey("buyer_deal_publications.id"), nullable=True
    )
    title_handoff_packet_id: Mapped[str | None] = mapped_column(
        ForeignKey("title_handoff_packets.id"), nullable=True
    )
    assignment_readiness_record_id: Mapped[str | None] = mapped_column(
        ForeignKey("assignment_readiness_records.id"), nullable=True
    )
    seller_portal_status: Mapped[str] = mapped_column(String(80), default="missing")
    buyer_portal_status: Mapped[str] = mapped_column(String(80), default="missing")
    title_handoff_status: Mapped[str] = mapped_column(String(80), default="missing")
    assignment_readiness_status: Mapped[str] = mapped_column(String(80), default="blocked")
    communication_status: Mapped[str] = mapped_column(String(80), default="pending")
    compliance_status: Mapped[str] = mapped_column(String(80), default="pending")
    closing_timeline: Mapped[str] = mapped_column(String(120), default="")
    blockers: Mapped[list[str]] = mapped_column(JSON, default=list)
    next_required_actions: Mapped[list[str]] = mapped_column(JSON, default=list)
    owner_approval_status: Mapped[str] = mapped_column(String(80), default="pending")
    coordination_status: Mapped[str] = mapped_column(String(80), default="blocked")
    projected_assignment_fee_at_risk: Mapped[int] = mapped_column(Integer, default=0)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    legal_execution_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    executable_contract_generated: Mapped[bool] = mapped_column(Boolean, default=False)
    title_submission_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    payment_handling_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    automatic_negotiation_allowed: Mapped[bool] = mapped_column(Boolean, default=False)

    deal: Mapped[Deal] = relationship(back_populates="unified_deal_rooms")
    contract_control: Mapped[ContractControl] = relationship(
        back_populates="unified_deal_rooms"
    )
    seller_offer_publication: Mapped[SellerOfferPublication | None] = relationship()
    buyer_deal_publication: Mapped[BuyerDealPublication | None] = relationship()
    title_handoff_packet: Mapped[TitleHandoffPacket | None] = relationship()
    assignment_readiness_record: Mapped[AssignmentReadinessRecord | None] = relationship()
    closing_checklist: Mapped["ClosingCoordinationChecklist | None"] = relationship(
        back_populates="deal_room",
        uselist=False,
    )
    blocker_records: Mapped[list["DealRoomBlocker"]] = relationship(
        back_populates="deal_room"
    )
    evidence_packets: Mapped[list["DealEvidencePacket"]] = relationship(
        back_populates="deal_room"
    )
    assignment_fee_attributions: Mapped[list["AssignmentFeeAttribution"]] = relationship(
        back_populates="deal_room"
    )


class ClosingCoordinationChecklist(TimestampMixin, Base):
    __tablename__ = "closing_coordination_checklists"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    deal_room_id: Mapped[str] = mapped_column(
        ForeignKey("unified_deal_rooms.id"), unique=True, nullable=False
    )
    seller_accepted_offer: Mapped[bool] = mapped_column(Boolean, default=False)
    contract_prep_ready: Mapped[bool] = mapped_column(Boolean, default=False)
    buyer_matched: Mapped[bool] = mapped_column(Boolean, default=False)
    buyer_pof_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    assignment_allowed_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    title_handoff_prepared: Mapped[bool] = mapped_column(Boolean, default=False)
    inspection_access_coordinated: Mapped[bool] = mapped_column(Boolean, default=False)
    seller_documents_requested: Mapped[bool] = mapped_column(Boolean, default=False)
    buyer_intent_recorded: Mapped[bool] = mapped_column(Boolean, default=False)
    compliance_review_complete: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_approval_complete: Mapped[bool] = mapped_column(Boolean, default=False)
    readiness_status: Mapped[str] = mapped_column(String(80), default="blocked")
    blocked_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    legal_execution_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    title_submission_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    payment_handling_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    automatic_negotiation_allowed: Mapped[bool] = mapped_column(Boolean, default=False)

    deal_room: Mapped[UnifiedDealRoom] = relationship(back_populates="closing_checklist")


class DealRoomBlocker(TimestampMixin, Base):
    __tablename__ = "deal_room_blockers"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    deal_room_id: Mapped[str] = mapped_column(
        ForeignKey("unified_deal_rooms.id"), nullable=False
    )
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    blocker_type: Mapped[str] = mapped_column(String(80), nullable=False)
    severity: Mapped[str] = mapped_column(String(40), default="medium")
    status: Mapped[str] = mapped_column(String(80), default="open")
    source: Mapped[str] = mapped_column(String(100), default="")
    detail: Mapped[str] = mapped_column(Text, default="")
    recommendation: Mapped[str] = mapped_column(Text, default="")
    blocks_closing: Mapped[bool] = mapped_column(Boolean, default=True)
    owner_action_required: Mapped[bool] = mapped_column(Boolean, default=True)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)

    deal_room: Mapped[UnifiedDealRoom] = relationship(back_populates="blocker_records")
    deal: Mapped[Deal] = relationship()


class DealEvidencePacket(TimestampMixin, Base):
    __tablename__ = "deal_evidence_packets"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    deal_room_id: Mapped[str] = mapped_column(
        ForeignKey("unified_deal_rooms.id"), nullable=False
    )
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    lead_source: Mapped[str] = mapped_column(String(120), default="")
    seller_interaction_proof: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    underwriting_snapshot: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    buyer_interest_proof: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    pof_proof_status: Mapped[str] = mapped_column(String(80), default="missing")
    contract_control_status: Mapped[str] = mapped_column(String(80), default="missing")
    title_handoff_status: Mapped[str] = mapped_column(String(80), default="missing")
    communication_receipts: Mapped[list[dict[str, object]]] = mapped_column(JSON, default=list)
    blocker_history: Mapped[list[dict[str, object]]] = mapped_column(JSON, default=list)
    compliance_review_status: Mapped[str] = mapped_column(String(80), default="pending")
    source_records_present: Mapped[bool] = mapped_column(Boolean, default=False)
    unsupported_profit_claims: Mapped[list[str]] = mapped_column(JSON, default=list)
    evidence_status: Mapped[str] = mapped_column(String(80), default="needs_review")
    owner_review_status: Mapped[str] = mapped_column(String(80), default="pending_review")
    approved: Mapped[bool] = mapped_column(Boolean, default=False)
    sanitized_summary: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    internal_notes_sanitized: Mapped[bool] = mapped_column(Boolean, default=True)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    client_facing_proof_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    legal_closing_guarantee_allowed: Mapped[bool] = mapped_column(Boolean, default=False)

    deal_room: Mapped[UnifiedDealRoom] = relationship(back_populates="evidence_packets")
    deal: Mapped[Deal] = relationship(back_populates="evidence_packets")
    assignment_fee_attributions: Mapped[list["AssignmentFeeAttribution"]] = relationship(
        back_populates="evidence_packet"
    )


class AssignmentFeeAttribution(TimestampMixin, Base):
    __tablename__ = "assignment_fee_attributions"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    deal_room_id: Mapped[str] = mapped_column(
        ForeignKey("unified_deal_rooms.id"), nullable=False
    )
    deal_id: Mapped[str] = mapped_column(ForeignKey("deals.id"), nullable=False)
    evidence_packet_id: Mapped[str | None] = mapped_column(
        ForeignKey("deal_evidence_packets.id"), nullable=True
    )
    projected_assignment_fee: Mapped[int] = mapped_column(Integer, default=0)
    target_assignment_fee: Mapped[int] = mapped_column(Integer, default=10_000)
    seller_contract_price: Mapped[int] = mapped_column(Integer, default=0)
    buyer_purchase_price: Mapped[int] = mapped_column(Integer, default=0)
    buyer_margin: Mapped[int] = mapped_column(Integer, default=0)
    attribution_basis: Mapped[list[str]] = mapped_column(JSON, default=list)
    confidence_score: Mapped[float] = mapped_column(Float, default=0)
    verification_status: Mapped[str] = mapped_column(String(80), default="needs_review")
    owner_review_status: Mapped[str] = mapped_column(String(80), default="pending_review")
    source_records_present: Mapped[bool] = mapped_column(Boolean, default=False)
    unsupported_profit_claims: Mapped[list[str]] = mapped_column(JSON, default=list)
    verified_10k_opportunity: Mapped[bool] = mapped_column(Boolean, default=False)
    draft_only: Mapped[bool] = mapped_column(Boolean, default=True)
    client_facing_proof_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    legal_closing_guarantee_allowed: Mapped[bool] = mapped_column(Boolean, default=False)

    deal_room: Mapped[UnifiedDealRoom] = relationship(
        back_populates="assignment_fee_attributions"
    )
    deal: Mapped[Deal] = relationship(back_populates="assignment_fee_attributions")
    evidence_packet: Mapped[DealEvidencePacket | None] = relationship(
        back_populates="assignment_fee_attributions"
    )
