from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.domains.worker_runtime.job_ledger import record_job_log
from app.domains.worker_runtime.retry_manager import schedule_retry
from app.domains.worker_runtime.worker import worker_safety_guard
from app.models import WorkerJob
from app.serializers import model_to_dict


def run_worker_job(session: Session, job: WorkerJob) -> dict[str, object]:
    if job.status == "completed":
        return {
            **model_to_dict(job),
            "idempotent_replay": True,
            "duplicate_execution_prevented": True,
        }

    safety = worker_safety_guard(job.job_type)
    job.attempts += 1
    job.last_run = datetime.now(UTC)
    job.live_action_allowed = False
    job.contract_execution_allowed = False
    job.title_submission_allowed = False
    job.portal_publish_allowed = False
    job.payment_handling_allowed = False
    job.bulk_send_allowed = False
    if not safety["allowed"]:
        schedule_retry(job, ",".join(safety["blocked_reasons"]))
        record_job_log(
            session,
            job,
            event_type="job_failed",
            status=job.status,
            message=job.error_message,
            safety_result=safety,
        )
        session.commit()
        return {**model_to_dict(job), "safety_result": safety}

    job.status = "running"
    record_job_log(
        session,
        job,
        event_type="job_started",
        status="running",
        message="Internal prep job started. No provider or live action path invoked.",
        safety_result=safety,
    )
    job.status = "completed"
    job.next_run = None
    job.error_message = ""
    record_job_log(
        session,
        job,
        event_type="job_completed",
        status="completed",
        message="Internal prep job completed and routed to Prime 2 queues.",
        safety_result=safety,
    )
    session.commit()
    return {
        **model_to_dict(job),
        "safety_result": safety,
        "real_world_action_taken": False,
        "provider_called": False,
    }


def run_due_jobs(session: Session) -> dict[str, object]:
    now = datetime.now(UTC)
    jobs = (
        session.query(WorkerJob)
        .filter(WorkerJob.status == "pending")
        .filter(WorkerJob.next_run <= now)
        .order_by(WorkerJob.created_at.asc())
        .all()
    )
    results = [run_worker_job(session, job) for job in jobs]
    return {
        "ran_jobs": results,
        "completed_count": len([job for job in results if job["status"] == "completed"]),
        "failed_count": len([job for job in results if job["status"] == "failed"]),
        "live_action_triggered": False,
    }

