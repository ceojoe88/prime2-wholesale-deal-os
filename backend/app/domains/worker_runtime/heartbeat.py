from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import WorkerHeartbeat, WorkerJob
from app.serializers import model_to_dict


def detect_stuck_jobs(session: Session) -> list[WorkerJob]:
    cutoff = datetime.now(UTC) - timedelta(minutes=settings.worker_stuck_job_minutes)
    return (
        session.query(WorkerJob)
        .filter(WorkerJob.status == "running")
        .filter(WorkerJob.last_run <= cutoff)
        .all()
    )


def record_heartbeat(session: Session, worker_name: str = "prime2-worker") -> WorkerHeartbeat:
    stuck_jobs = detect_stuck_jobs(session)
    heartbeat = (
        session.query(WorkerHeartbeat)
        .filter(WorkerHeartbeat.worker_name == worker_name)
        .first()
    )
    if heartbeat is None:
        heartbeat = WorkerHeartbeat(id="worker-heartbeat-001", worker_name=worker_name)
        session.add(heartbeat)
    heartbeat.status = "degraded" if stuck_jobs else "healthy"
    heartbeat.last_seen_at = datetime.now(UTC)
    heartbeat.active = True
    heartbeat.stuck_jobs_detected = len(stuck_jobs)
    heartbeat.recovery_recommended = bool(stuck_jobs)
    heartbeat.health_summary = {
        "pending_jobs": session.query(WorkerJob).filter(WorkerJob.status == "pending").count(),
        "running_jobs": session.query(WorkerJob).filter(WorkerJob.status == "running").count(),
        "completed_jobs": session.query(WorkerJob).filter(WorkerJob.status == "completed").count(),
        "failed_jobs": session.query(WorkerJob).filter(WorkerJob.status == "failed").count(),
        "stuck_job_ids": [job.job_id for job in stuck_jobs],
        "live_action_allowed": False,
    }
    heartbeat.live_action_allowed = False
    session.commit()
    return heartbeat


def worker_health(session: Session) -> dict[str, object]:
    heartbeat = record_heartbeat(session)
    return {
        "heartbeat": model_to_dict(heartbeat),
        "status": heartbeat.status,
        "stuck_jobs_detected": heartbeat.stuck_jobs_detected,
        "recovery_mechanism": "stuck jobs are detected and routed for retry/escalation review",
        "live_actions_allowed": False,
        "contract_execution_allowed": False,
        "title_submission_allowed": False,
        "portal_publish_allowed": False,
        "payment_handling_allowed": False,
    }

