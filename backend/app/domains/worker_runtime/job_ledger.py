from __future__ import annotations

from uuid import uuid4

from sqlalchemy.orm import Session

from app.models import WorkerJob, WorkerJobLog


def record_job_log(
    session: Session,
    job: WorkerJob | None,
    *,
    event_type: str,
    status: str,
    message: str,
    safety_result: dict[str, object] | None = None,
) -> WorkerJobLog:
    log = WorkerJobLog(
        id=f"worker-log-{uuid4().hex[:10]}",
        job_id=job.job_id if job else None,
        job_type=job.job_type if job else "",
        event_type=event_type,
        status=status,
        message=message,
        attempt_number=job.attempts if job else 0,
        idempotency_key=job.idempotency_key if job else "",
        safety_result=safety_result or {},
        provider_called=False,
        real_world_action_taken=False,
    )
    session.add(log)
    return log
