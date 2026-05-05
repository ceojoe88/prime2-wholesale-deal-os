from __future__ import annotations

from sqlalchemy.orm import Session

from app.domains.worker_runtime.heartbeat import worker_health
from app.models import WorkerJob, WorkerJobLog
from app.serializers import model_to_dict


def worker_dashboard(session: Session) -> dict[str, object]:
    jobs = session.query(WorkerJob).order_by(WorkerJob.created_at.desc()).all()
    logs = session.query(WorkerJobLog).order_by(WorkerJobLog.created_at.desc()).limit(50).all()
    return {
        "worker_health": worker_health(session),
        "jobs": [model_to_dict(job) for job in jobs],
        "logs": [model_to_dict(log) for log in logs],
        "pending_jobs": [model_to_dict(job) for job in jobs if job.status == "pending"],
        "failed_jobs": [model_to_dict(job) for job in jobs if job.status == "failed"],
        "feeds": [
            "autonomy panel",
            "daily briefing",
            "escalation queue",
            "next-best-action engine",
        ],
        "live_outreach_allowed": False,
        "bulk_send_allowed": False,
        "contract_execution_allowed": False,
        "title_submission_allowed": False,
        "portal_publish_allowed": False,
        "payment_handling_allowed": False,
    }

