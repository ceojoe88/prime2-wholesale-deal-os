from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app.domains.campaign_brain.router import router as campaign_brain_v1_router
from app.domains.document_intelligence.router import router as document_intelligence_v1_router
from app.domains.market_enrichment.router import router as market_enrichment_v1_router
from app.domains.mobile_operator.router import router as mobile_operator_v1_router
from app.domains.prime_memory.router import router as prime_memory_v1_router
from app.domains.provider_readiness.router import router as provider_readiness_v1_router
from app.models import (
    AIRequestLog,
    AITemplate,
    AuditExportPacket,
    AssignmentFeeAttribution,
    AssignmentReadinessRecord,
    AutoExecutionRule,
    AutomationRule,
    BuyerAccelerationRecord,
    AutonomousDailyOperatingReport,
    CallIntelligenceSession,
    CampaignRuleRecord,
    BuyerDealPublication,
    BuyerDemandProfile,
    CommunicationDraft,
    ContractControl,
    ContractReadyState,
    DealProbabilityRecord,
    DocumentIntelligenceFile,
    Division,
    FieldCallOutcome,
    MarketProfile,
    MobileOperatorNote,
    LeadImportBatch,
    LeadQualityReview,
    ProviderSandboxReadinessCheck,
    ProviderRegistry,
    PrimeMemoryItem,
    LeadSpendPlan,
    MarketScalingScore,
    OfferPacket,
    OperatorModeSetting,
    OutcomeLearningRecord,
    PredictionFeedbackRecord,
    RevenueForecastRecord,
    ScoringAdjustmentSuggestion,
    TitleReviewCoordination,
    WorkerHeartbeat,
    WorkerJob,
    SellerInteraction,
    SellerOfferPublication,
    SystemTrustScore,
    TitleHandoffPacket,
    UnifiedDealRoom,
)
from app.seed_data import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    if settings.auto_seed:
        with SessionLocal() as session:
            if (
                session.query(Division).count() == 0
                or session.query(BuyerDealPublication).count() == 0
                or session.query(BuyerDemandProfile).count() == 0
                or session.query(SellerInteraction).count() == 0
                or session.query(OfferPacket).count() == 0
                or session.query(ContractControl).count() == 0
                or session.query(ContractReadyState).count() == 0
                or session.query(TitleReviewCoordination).count() == 0
                or session.query(AutomationRule).count() == 0
                or session.query(AutoExecutionRule).count() == 0
                or session.query(BuyerAccelerationRecord).count() == 0
                or session.query(OutcomeLearningRecord).count() == 0
                or session.query(RevenueForecastRecord).count() == 0
                or session.query(DealProbabilityRecord).count() == 0
                or session.query(MarketScalingScore).count() == 0
                or session.query(LeadSpendPlan).count() == 0
                or session.query(OperatorModeSetting).count() == 0
                or session.query(AutonomousDailyOperatingReport).count() == 0
                or session.query(SystemTrustScore).count() == 0
                or session.query(AuditExportPacket).count() == 0
                or session.query(ProviderSandboxReadinessCheck).count() == 0
                or session.query(ProviderRegistry).count() == 0
                or session.query(TitleHandoffPacket).count() == 0
                or session.query(AssignmentReadinessRecord).count() == 0
                or session.query(CommunicationDraft).count() == 0
                or session.query(SellerOfferPublication).count() == 0
                or session.query(UnifiedDealRoom).count() == 0
                or session.query(AssignmentFeeAttribution).count() == 0
                or session.query(LeadImportBatch).count() == 0
                or session.query(LeadQualityReview).count() == 0
                or session.query(FieldCallOutcome).count() == 0
                or session.query(PredictionFeedbackRecord).count() == 0
                or session.query(AITemplate).count() == 0
                or session.query(AIRequestLog).count() == 0
                or session.query(WorkerJob).count() == 0
                or session.query(WorkerHeartbeat).count() == 0
                or session.query(ScoringAdjustmentSuggestion).count() == 0
                or session.query(CallIntelligenceSession).count() == 0
                or session.query(DocumentIntelligenceFile).count() == 0
                or session.query(CampaignRuleRecord).count() == 0
                or session.query(MarketProfile).count() == 0
                or session.query(PrimeMemoryItem).count() == 0
                or session.query(MobileOperatorNote).count() == 0
            ):
                seed_database(session)
    yield


app = FastAPI(
    title=settings.app_name,
    description="Private operator-only acquisition-to-assignment command system.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(provider_readiness_v1_router)
app.include_router(document_intelligence_v1_router)
app.include_router(campaign_brain_v1_router)
app.include_router(market_enrichment_v1_router)
app.include_router(prime_memory_v1_router)
app.include_router(mobile_operator_v1_router)


@app.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "private_operator_only": settings.private_operator_only,
        "overseer": settings.overseer_name,
    }
