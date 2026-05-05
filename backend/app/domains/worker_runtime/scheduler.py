from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.domains.worker_runtime.job_queue import enqueue_job


def recurring_job_specs(now: datetime | None = None) -> list[dict[str, object]]:
    moment = now or datetime.now(UTC)
    day_key = moment.strftime("%Y%m%d")
    hour_key = moment.strftime("%Y%m%d%H")
    five_minute_bucket = int(moment.timestamp() // 300)
    return [
        {
            "job_type": "automation_rule_evaluation",
            "source_record": "automation_rules",
            "idempotency_key": f"worker:automation:{five_minute_bucket}",
            "next_run": moment,
            "schedule": "every_5_min",
        },
        {
            "job_type": "lead_scoring_refresh",
            "source_record": "leads",
            "idempotency_key": f"worker:lead-scoring:{hour_key}",
            "next_run": moment + timedelta(seconds=1),
            "schedule": "hourly",
        },
        {
            "job_type": "daily_briefing_generation",
            "source_record": "daily_command_briefing",
            "idempotency_key": f"worker:daily-briefing:{day_key}",
            "next_run": moment + timedelta(seconds=2),
            "schedule": "daily",
        },
        {
            "job_type": "forecast_refresh",
            "source_record": "revenue_forecast",
            "idempotency_key": f"worker:forecast:{day_key}",
            "next_run": moment + timedelta(seconds=3),
            "schedule": "daily",
        },
    ]


def schedule_recurring_jobs(session: Session, now: datetime | None = None) -> dict[str, object]:
    jobs = [
        enqueue_job(
            session,
            job_type=str(spec["job_type"]),
            source_record=str(spec["source_record"]),
            idempotency_key=str(spec["idempotency_key"]),
            next_run=spec["next_run"],  # type: ignore[arg-type]
        )
        for spec in recurring_job_specs(now)
    ]
    return {
        "scheduled_jobs": jobs,
        "created_count": len([job for job in jobs if not job.get("idempotent_replay")]),
        "duplicate_count": len([job for job in jobs if job.get("idempotent_replay")]),
        "live_action_allowed": False,
    }

