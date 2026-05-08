from __future__ import annotations

from pydantic import BaseModel, Field


class ClientLeadScoreRequest(BaseModel):
    workspace_id: str | None = None
    refresh: bool = False


class ClientWorkspaceCreate(BaseModel):
    workspace_name: str
    client_name: str = ""
    market_focus: list[str] = Field(default_factory=list)


class ClientBuyerProfileCreate(BaseModel):
    buyer_name: str = "Manual Buyer"
    buyer_company: str | None = None
    buyer_type: str = "unknown"
    primary_market: str = ""
    target_zip_codes: list[str] = Field(default_factory=list)
    preferred_property_types: list[str] = Field(default_factory=list)
    min_price: int | None = None
    max_price: int | None = None
    rehab_tolerance: str = "unknown"
    close_speed: str = "unknown"
    funding_status: str = "unknown"
    proof_of_funds_status: str = "missing"
    communication_preference: str = "unknown"
    active_status: str = "needs_review"
    notes_summary: str = ""


class ClientBuyerBuyBoxCreate(BaseModel):
    market: str = ""
    zip_codes: list[str] = Field(default_factory=list)
    property_types: list[str] = Field(default_factory=list)
    min_beds: int | None = None
    min_baths: float | None = None
    min_sqft: int | None = None
    max_purchase_price: int | None = None
    min_purchase_price: int | None = None
    rehab_level: str = "unknown"
    occupancy_preference: str = "unknown"
    deal_type_preference: str = "unknown"
    notes_summary: str = ""


class ClientBuyerDemandEvidenceCreate(BaseModel):
    buyer_id: str | None = None
    evidence_type: str = "manual_client_note"
    evidence_summary: str = ""
    source_type: str = "manual"
    confidence_level: str = "medium"


class ClientBuyerOutreachDraftCreate(BaseModel):
    buyer_id: str | None = None
    draft_type: str = "deal_preview"
    purpose: str = "manual buyer preview"


class ClientContactConsentRecordCreate(BaseModel):
    contact_type: str = "unknown"
    lead_id: str | None = None
    buyer_id: str | None = None
    contact_name: str | None = None
    phone: str | None = None
    email: str | None = None
    consent_channel: str = "unknown"
    consent_status: str = "unknown"
    consent_source: str = "manual_entry"
    consent_summary: str = ""
    consent_captured_at: str | None = None
    expires_at: str | None = None
    requires_human_review: bool = False


class ClientContactOptOutRecordCreate(BaseModel):
    contact_type: str = "unknown"
    lead_id: str | None = None
    buyer_id: str | None = None
    phone: str | None = None
    email: str | None = None
    channel: str = "unknown"
    opt_out_status: str = "unknown"
    opt_out_source: str = "manual_entry"
    opt_out_summary: str = ""
    recorded_at: str = ""
    requires_human_review: bool = True


class ClientMessageRiskReviewCreate(BaseModel):
    workspace_id: str
    lead_id: str | None = None
    buyer_id: str | None = None
    source_draft_type: str = "unknown"
    source_draft_id: str | None = None
    channel: str = "unknown"
    draft_body: str | None = None


class ClientCommunicationApprovalGateCreate(BaseModel):
    workspace_id: str
    lead_id: str | None = None
    buyer_id: str | None = None
    source_draft_type: str = "unknown"
    source_draft_id: str | None = None
    contact_status_id: str | None = None
    message_risk_review_id: str | None = None


class ClientComplianceReadinessPlaceholderCreate(BaseModel):
    placeholder_type: str = "dnc_check"
    readiness_status: str = "placeholder_only"
    summary: str = ""
    required_before_live: bool = True


class ClientWeeklyCommandReportCreate(BaseModel):
    report_week_start: str = ""
    report_week_end: str = ""


class ClientBusinessProfileCreate(BaseModel):
    business_name: str = "Client Business"
    operator_name: str | None = None
    business_type: str = "unknown"
    experience_level: str = "unknown"
    primary_market: str = ""
    secondary_markets: list[str] = Field(default_factory=list)
    monthly_lead_goal: int | None = None
    monthly_contract_goal: int | None = None
    preferred_strategy: str = "unknown"
    current_tools_summary: str | None = None
    biggest_bottleneck: str = "unknown"


class ClientStrategyProfileCreate(BaseModel):
    strategy_type: str = "unknown"
    acquisition_channels: list[str] = Field(default_factory=list)
    disposition_channels: list[str] = Field(default_factory=list)
    target_property_types: list[str] = Field(default_factory=list)
    target_seller_situations: list[str] = Field(default_factory=list)
    target_price_band_min: int | None = None
    target_price_band_max: int | None = None
    assignment_fee_target: int | None = None
    risk_tolerance: str = "unknown"
    operating_mode: str = "unknown"
    strategy_summary: str = ""
    requires_human_review: bool = False


class ClientMarketSetupCreate(BaseModel):
    market_name: str = ""
    state: str = ""
    counties: list[str] = Field(default_factory=list)
    cities: list[str] = Field(default_factory=list)
    zip_codes: list[str] = Field(default_factory=list)
    market_priority: str = "primary"
    market_status: str = "draft"
    market_notes_summary: str = ""


class ClientPipelineSetupCreate(BaseModel):
    pipeline_name: str = "Prime2 Full Deal Loop"
    pipeline_type: str = "full_deal_loop"
    setup_status: str = "draft"


class ClientLeadSourceSetupCreate(BaseModel):
    source_name: str = "Manual lead source"
    source_type: str = "manual_entry"
    source_status: str = "planned"
    expected_monthly_leads: int | None = None
    cost_tracking_enabled: bool = False
    provider_connected: bool = False
    notes_summary: str = ""


class ClientBuyerListSetupCreate(BaseModel):
    setup_status: str | None = None
    recommended_next_step: str = ""


class ClientTeamSetupChecklistCreate(BaseModel):
    owner_added: bool | None = None
    acquisition_role_added: bool | None = None
    underwriting_role_added: bool | None = None
    disposition_role_added: bool | None = None
    compliance_owner_added: bool | None = None
    client_success_owner_added: bool | None = None
    recommended_next_step: str = ""


class ClientComplianceSetupChecklistCreate(BaseModel):
    consent_policy_documented: bool | None = None
    opt_out_process_documented: bool | None = None
    dnc_placeholder_created: bool | None = None
    ten_dlc_placeholder_created: bool | None = None
    email_unsubscribe_placeholder_created: bool | None = None
    call_recording_notice_placeholder_created: bool | None = None
    compliance_owner_assigned: bool | None = None
    recommended_next_step: str = ""


class ClientFirstLeadImportChecklistCreate(BaseModel):
    first_10_leads_target: int = 10
    recommended_next_step: str = ""


class ClientOnboardingTaskCreate(BaseModel):
    task_title: str = "Review onboarding blocker"
    task_description: str = ""
    task_category: str = "review"
    task_status: str = "todo"
    priority: str = "medium"
    owner_role: str = "onboarding_manager"
    due_window: str = "this_week"
    related_blocker_id: str | None = None
