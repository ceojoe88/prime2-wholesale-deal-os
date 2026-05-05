from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.config import settings
from app.domains.worker_runtime.job_ledger import record_job_log
from app.domains.worker_runtime.worker import worker_safety_guard
from app.models import WorkerJob
from app.serializers import model_to_dict


def enqueue_job(
    session: Session,
    *,
    job_type: str,
    source_record: str = "",
    idempotency_key: str | None = None,
    next_run: datetime | None = None,
    priority: str = "normal",
) -> dict[str, object]:
    key = idempotency_key or f"{job_type}:{source_record or 'global'}"
    existing = (
        session.query(WorkerJob).filter(WorkerJob.idempotency_key == key).one_or_none()
    )
    if existing is not None:
        return {
            **model_to_dict(existing),
            "idempotent_replay": True,
            "duplicate_job_created": False,
        }

    safety = worker_safety_guard(job_type)
    status = "pending" if safety["allowed"] else "failed"
    job = WorkerJob(
        id=f"worker-job-{uuid4().hex[:10]}",
        job_id=f"job-{session.query(WorkerJob).count() + 1:03d}",
        job_type=job_type,
        source_record=source_record,
        status=status,
        attempts=0,
        next_run=next_run or datetime.now(UTC),
        idempotency_key=key,
        error_message="" if safety["allowed"] else ",".join(safety["blocked_reasons"]),
        priority=priority,
        max_attempts=settings.worker_max_retry_attempts,
        live_action_allowed=False,
        contract_execution_allowed=False,
        title_submission_allowed=False,
        portal_publish_allowed=False,
        payment_handling_allowed=False,
        bulk_send_allowed=False,
    )
    session.add(job)
    session.flush()
    record_job_log(
        session,
        job,
        event_type="job_enqueued" if safety["allowed"] else "job_blocked",
        status=status,
        message="Worker job queued for internal prep only." if safety["allowed"] else job.error_message,
        safety_result=safety,
    )
    session.commit()
    return {
        **model_to_dict(job),
        "idempotent_replay": False,
        "duplicate_job_created": False,
        "safety_result": safety,
    }

