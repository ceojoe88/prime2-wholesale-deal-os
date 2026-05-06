from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.domains.cloud_readiness.service import (
    cloud_backups,
    cloud_env,
    cloud_monitoring,
    cloud_security,
    sync_cloud_readiness,
)


router = APIRouter(prefix="/api/v1/cloud-readiness", tags=["cloud-readiness"])


@router.get("/overview")
def overview(session: Session = Depends(get_session)) -> dict[str, object]:
    return sync_cloud_readiness(session)


@router.get("/env")
def env(session: Session = Depends(get_session)) -> dict[str, object]:
    return cloud_env(session)


@router.get("/security")
def security(session: Session = Depends(get_session)) -> dict[str, object]:
    return cloud_security(session)


@router.get("/backups")
def backups(session: Session = Depends(get_session)) -> dict[str, object]:
    return cloud_backups(session)


@router.get("/monitoring")
def monitoring(session: Session = Depends(get_session)) -> dict[str, object]:
    return cloud_monitoring(session)
