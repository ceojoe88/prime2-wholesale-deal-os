from __future__ import annotations

import os
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.config import settings
from app.domains.cloud_readiness.sanitizer import sanitize_cloud_record
from app.models import (
    AICostLedger,
    AutoExecutionAttempt,
    CampaignActivationAttempt,
    CloudBackupReadinessRecord,
    CloudDeploymentProfile,
    CloudEnvironmentCheck,
    CloudMonitoringSnapshot,
    CommunicationSendAttempt,
    ProviderAttemptAudit,
    ProviderRegistry,
    WorkerHeartbeat,
    WorkerJob,
)
from app.serializers import model_to_dict


SECRET_ENV_REFERENCE_NAMES = {
    "OPENAI_API_KEY",
    "EMAIL_SANDBOX_API_KEY",
    "SMS_PROVIDER_API_KEY",
    "CRM_SANDBOX_KEY",
    "STORAGE_SANDBOX_KEY",
}


def _env_present(name: str) -> bool:
    return bool(os.getenv(name))


def _is_truthy_env(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def _allowed_origins() -> list[str]:
    raw = os.getenv("ALLOWED_ORIGINS", "")
    if not raw:
        return []
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


def evaluate_environment(profile_name: str = "production") -> list[CloudEnvironmentCheck]:
    database_url = os.getenv("DATABASE_URL", "")
    allowed_origins = _allowed_origins()
    provider_mode = os.getenv("PROVIDER_MODE", settings.communication_provider_mode)
    frontend_api = os.getenv("NEXT_PUBLIC_API_BASE_URL", "")
    backup_target = os.getenv("BACKUP_TARGET", "")
    auth_required = _is_truthy_env("PRIME2_AUTH_REQUIRED")
    debug_off = not _is_truthy_env("DEBUG")
    live_flags_off = (
        not settings.communication_global_live_enabled
        and not _is_truthy_env("COMMUNICATION_LIVE_ENABLED")
        and not _is_truthy_env("SMS_LIVE_ENABLED")
        and not _is_truthy_env("EMAIL_LIVE_ENABLED")
    )

    checks = [
        {
            "id": f"cloud-env-{profile_name}-auth",
            "category": "security",
            "check_name": "auth required",
            "passed": auth_required,
            "detail": "PRIME2_AUTH_REQUIRED env flag is present and true." if auth_required else "Private cloud exposure must require owner auth.",
            "remediation": "Set PRIME2_AUTH_REQUIRED=true and wire private authentication before production.",
        },
        {
            "id": f"cloud-env-{profile_name}-debug",
            "category": "security",
            "check_name": "debug mode off",
            "passed": debug_off,
            "detail": "DEBUG is not enabled.",
            "remediation": "Set DEBUG=false for staging/production.",
        },
        {
            "id": f"cloud-env-{profile_name}-database",
            "category": "env",
            "check_name": "database url configured",
            "passed": bool(database_url) and (profile_name != "production" or not database_url.startswith("sqlite")),
            "detail": "DATABASE_URL is configured without exposing its value." if database_url else "DATABASE_URL env var is missing.",
            "remediation": "Set DATABASE_URL to the private Postgres URL for cloud deployment.",
        },
        {
            "id": f"cloud-env-{profile_name}-cors",
            "category": "security",
            "check_name": "cors restricted",
            "passed": bool(allowed_origins) and "*" not in allowed_origins,
            "detail": f"{len(allowed_origins)} allowed origins configured.",
            "remediation": "Set ALLOWED_ORIGINS to exact private frontend origins.",
        },
        {
            "id": f"cloud-env-{profile_name}-frontend-api",
            "category": "env",
            "check_name": "frontend api base configured",
            "passed": bool(frontend_api),
            "detail": "NEXT_PUBLIC_API_BASE_URL reference exists." if frontend_api else "Frontend API base URL is missing.",
            "remediation": "Set NEXT_PUBLIC_API_BASE_URL for the private frontend deployment.",
        },
        {
            "id": f"cloud-env-{profile_name}-provider-mode",
            "category": "provider",
            "check_name": "provider mode safe",
            "passed": provider_mode in {"mock", "mock/dry_run", "sandbox"},
            "detail": f"Provider mode is {provider_mode}.",
            "remediation": "Keep provider mode mock or sandbox until V30 activation gates pass.",
        },
        {
            "id": f"cloud-env-{profile_name}-live-flags",
            "category": "provider",
            "check_name": "provider live flags default off",
            "passed": live_flags_off,
            "detail": "Live provider flags are off." if live_flags_off else "One or more live provider flags are enabled.",
            "remediation": "Disable live provider flags until owner-approved activation records exist.",
        },
        {
            "id": f"cloud-env-{profile_name}-worker-mode",
            "category": "worker",
            "check_name": "worker mode visible",
            "passed": bool(os.getenv("WORKER_MODE", "internal")),
            "detail": f"Worker mode is {os.getenv('WORKER_MODE', 'internal')}.",
            "remediation": "Set WORKER_MODE to disabled, internal, or worker.",
        },
        {
            "id": f"cloud-env-{profile_name}-backup-target",
            "category": "backup",
            "check_name": "backup path or bucket placeholder",
            "passed": bool(backup_target),
            "detail": "Backup target reference exists." if backup_target else "Backup target is not configured.",
            "remediation": "Set BACKUP_TARGET to a local path or private bucket placeholder.",
        },
        {
            "id": f"cloud-env-{profile_name}-openai-reference",
            "category": "secrets",
            "check_name": "openai key env reference only",
            "passed": True,
            "detail": "OPENAI_API_KEY is read from env only; value is never stored.",
            "remediation": "Keep API keys in environment or secret manager only.",
        },
    ]
    records: list[CloudEnvironmentCheck] = []
    for check in checks:
        passed = bool(check["passed"])
        records.append(
            CloudEnvironmentCheck(
                id=str(check["id"]),
                profile_name=profile_name,
                category=str(check["category"]),
                check_name=str(check["check_name"]),
                required=True,
                passed=passed,
                status="passed" if passed else "blocked",
                detail=str(check["detail"]),
                remediation=str(check["remediation"]),
                blocked_reasons=[] if passed else [str(check["check_name"]).replace(" ", "_")],
                secret_value_exposed=False,
                prevents_production=not passed,
            )
        )
    return records


def sync_deployment_profile(profile: CloudDeploymentProfile, checks: list[CloudEnvironmentCheck]) -> dict[str, object]:
    reasons = sorted({reason for check in checks for reason in check.blocked_reasons if check.required and not check.passed})
    profile.readiness_status = "ready" if not reasons else "blocked"
    profile.blocked_reasons = reasons
    return {
        "ready": not reasons,
        "blocked_reasons": reasons,
        "public_exposure_allowed": False,
        "live_provider_activation_allowed": False,
    }


def sync_backup_readiness(record: CloudBackupReadinessRecord) -> dict[str, object]:
    reasons: list[str] = []
    if not record.backup_target:
        reasons.append("backup_target_required")
    if record.raw_secrets_included:
        reasons.append("raw_secrets_blocked")
    if not record.database_backup_metadata:
        reasons.append("database_backup_metadata_required")
    if not record.export_manifest:
        reasons.append("export_manifest_required")
    if not record.restore_checklist:
        reasons.append("restore_checklist_required")
    record.safe_metadata_only = True
    record.status = "ready_for_restore_test" if not reasons else "blocked"
    record.blocked_reasons = sorted(set(reasons))
    return {
        "ready": not reasons,
        "blocked_reasons": record.blocked_reasons,
        "safe_metadata_only": True,
        "raw_secrets_included": False,
    }


def build_monitoring_snapshot(session: Session, profile_name: str = "production") -> CloudMonitoringSnapshot:
    heartbeat = session.query(WorkerHeartbeat).first()
    failed_jobs = session.query(WorkerJob).filter(WorkerJob.status == "failed").count()
    blocked_attempts = session.query(ProviderAttemptAudit).filter(ProviderAttemptAudit.attempt_status == "blocked").count()
    blocked_attempts += session.query(CommunicationSendAttempt).filter(CommunicationSendAttempt.attempt_status == "blocked").count()
    blocked_attempts += session.query(AutoExecutionAttempt).filter(AutoExecutionAttempt.attempt_status == "blocked").count()
    blocked_attempts += session.query(CampaignActivationAttempt).filter(CampaignActivationAttempt.attempt_status == "blocked").count()
    cost = session.query(AICostLedger).order_by(AICostLedger.created_at.desc()).first()
    providers = session.query(ProviderRegistry).all()
    provider_status = "blocked" if any(provider.readiness_status != "ready" for provider in providers) else "ready"
    reasons: list[str] = []
    if failed_jobs:
        reasons.append("failed_jobs_present")
    if provider_status != "ready":
        reasons.append("provider_readiness_blocked")
    if heartbeat is None or heartbeat.status != "healthy":
        reasons.append("worker_heartbeat_unhealthy")
    return CloudMonitoringSnapshot(
        id=f"cloud-monitoring-{profile_name}",
        profile_name=profile_name,
        health_status="ok",
        readiness_status="ready" if not reasons else "blocked",
        worker_heartbeat_status=heartbeat.status if heartbeat else "missing",
        provider_readiness_status=provider_status,
        ai_cost_cap_status=cost.cap_status if cost else "unknown",
        failed_job_count=failed_jobs,
        blocked_action_count=blocked_attempts,
        readiness_passed=not reasons,
        blocked_reasons=sorted(set(reasons)),
        secrets_exposed=False,
        live_provider_activation_allowed=False,
    )


def sync_cloud_readiness(session: Session, profile_name: str = "production") -> dict[str, object]:
    checks = evaluate_environment(profile_name)
    for check in checks:
        session.merge(check)

    profile = session.get(CloudDeploymentProfile, f"cloud-profile-{profile_name}")
    if profile is None:
        profile = CloudDeploymentProfile(id=f"cloud-profile-{profile_name}", profile_name=profile_name)
        session.add(profile)

    backup = session.get(CloudBackupReadinessRecord, f"cloud-backup-{profile_name}")
    if backup is None:
        backup = CloudBackupReadinessRecord(
            id=f"cloud-backup-{profile_name}",
            profile_name=profile_name,
            backup_target=os.getenv("BACKUP_TARGET", ""),
            database_backup_metadata={
                "database_url_present": bool(os.getenv("DATABASE_URL", "")),
                "database_url_value": "masked" if os.getenv("DATABASE_URL", "") else "",
                "generated_at": datetime.now(UTC).isoformat(),
            },
            export_manifest={
                "safe_metadata_only": True,
                "excluded": ["raw_secret_values", "private_contact_values"],
            },
            restore_checklist=[
                "verify encrypted storage target",
                "restore into isolated database",
                "run alembic upgrade head",
                "run seed consistency checks",
            ],
        )
        session.add(backup)

    backup.backup_target = os.getenv("BACKUP_TARGET", backup.backup_target)
    backup_gate = sync_backup_readiness(backup)
    monitoring = build_monitoring_snapshot(session, profile_name)
    session.merge(monitoring)
    profile_gate = sync_deployment_profile(profile, checks)
    session.commit()

    live_enabled_count = session.query(ProviderRegistry).filter(ProviderRegistry.live_enabled.is_(True)).count()
    production_ready = profile_gate["ready"] and backup_gate["ready"] and monitoring.readiness_passed
    return {
        "profile": sanitize_cloud_record(profile),
        "production_ready": production_ready,
        "blocked_reasons": sorted(
            set(profile.blocked_reasons + backup.blocked_reasons + monitoring.blocked_reasons)
        ),
        "environment_checks": [sanitize_cloud_record(check) for check in checks],
        "backup_readiness": sanitize_cloud_record(backup),
        "monitoring": sanitize_cloud_record(monitoring),
        "credential_posture": {
            "secret_values_exposed": False,
            "secret_reference_names": sorted(SECRET_ENV_REFERENCE_NAMES),
            "openai_key_present": _env_present("OPENAI_API_KEY"),
            "raw_secret_storage_allowed": False,
        },
        "provider_live_flags": {
            "live_enabled_count": live_enabled_count,
            "default_off": live_enabled_count == 0 and not settings.communication_global_live_enabled,
            "activation_allowed": False,
        },
        "deployment_profiles": [
            sanitize_cloud_record(item)
            for item in session.query(CloudDeploymentProfile).order_by(CloudDeploymentProfile.profile_name).all()
        ],
        "fail_closed": not production_ready,
        "no_deployment_automation": True,
    }


def cloud_env(session: Session) -> dict[str, object]:
    return {"environment_checks": sync_cloud_readiness(session)["environment_checks"]}


def cloud_security(session: Session) -> dict[str, object]:
    overview = sync_cloud_readiness(session)
    return {
        "production_ready": overview["production_ready"],
        "blocked_reasons": overview["blocked_reasons"],
        "credential_posture": overview["credential_posture"],
        "provider_live_flags": overview["provider_live_flags"],
        "public_exposure_allowed": False,
    }


def cloud_backups(session: Session) -> dict[str, object]:
    return {"backup_readiness": sync_cloud_readiness(session)["backup_readiness"]}


def cloud_monitoring(session: Session) -> dict[str, object]:
    return {"monitoring": sync_cloud_readiness(session)["monitoring"]}
