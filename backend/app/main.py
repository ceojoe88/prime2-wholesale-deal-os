from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app.models import (
    AssignmentFeeAttribution,
    AssignmentReadinessRecord,
    AutoExecutionRule,
    AutomationRule,
    BuyerAccelerationRecord,
    BuyerDealPublication,
    BuyerDemandProfile,
    CommunicationDraft,
    ContractControl,
    ContractReadyState,
    Division,
    OfferPacket,
    TitleReviewCoordination,
    SellerInteraction,
    SellerOfferPublication,
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
                or session.query(TitleHandoffPacket).count() == 0
                or session.query(AssignmentReadinessRecord).count() == 0
                or session.query(CommunicationDraft).count() == 0
                or session.query(SellerOfferPublication).count() == 0
                or session.query(UnifiedDealRoom).count() == 0
                or session.query(AssignmentFeeAttribution).count() == 0
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


@app.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "private_operator_only": settings.private_operator_only,
        "overseer": settings.overseer_name,
    }
