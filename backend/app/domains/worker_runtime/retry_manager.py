from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.core.config import settings
from app.models import WorkerJob


def retry_delay(attempts: int) -> timedelta:
    return timedelta(minutes=min(60, 2 ** max(0, attempts - 1)))


def schedule_retry(job: WorkerJob, error_message: str) -> None:
    job.error_message = error_message
    if job.attempts >= min(job.max_attempts, settings.worker_max_retry_attempts):
        job.status = "failed"
        job.next_run = None
        return
    job.status = "pending"
    job.next_run = datetime.now(UTC) + retry_delay(job.attempts)

