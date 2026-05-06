from __future__ import annotations

from fastapi.testclient import TestClient

from app.domains.cloud_readiness.service import evaluate_environment, sync_backup_readiness
from app.main import app
from app.models import CloudBackupReadinessRecord


def test_production_readiness_fails_when_critical_env_missing(monkeypatch):
    for name in [
        "PRIME2_AUTH_REQUIRED",
        "DATABASE_URL",
        "ALLOWED_ORIGINS",
        "NEXT_PUBLIC_API_BASE_URL",
        "BACKUP_TARGET",
    ]:
        monkeypatch.delenv(name, raising=False)

    checks = evaluate_environment("production")
    failed = {check.check_name for check in checks if check.required and not check.passed}

    assert "auth required" in failed
    assert "database url configured" in failed
    assert "cors restricted" in failed
    assert "frontend api base configured" in failed


def test_cloud_readiness_overview_fails_closed_and_live_flags_default_off():
    with TestClient(app) as client:
        response = client.get("/api/v1/cloud-readiness/overview")

    assert response.status_code == 200
    body = response.json()
    assert body["production_ready"] is False
    assert body["fail_closed"] is True
    assert body["provider_live_flags"]["default_off"] is True
    assert body["provider_live_flags"]["activation_allowed"] is False
    assert body["no_deployment_automation"] is True


def test_cloud_readiness_masks_secret_posture():
    with TestClient(app) as client:
        response = client.get("/api/v1/cloud-readiness/security")

    assert response.status_code == 200
    body = response.json()
    assert body["credential_posture"]["secret_values_exposed"] is False
    assert body["credential_posture"]["raw_secret_storage_allowed"] is False
    assert "OPENAI_API_KEY" in body["credential_posture"]["secret_reference_names"]
    assert "sk-" not in str(body)


def test_cloud_backup_metadata_is_safe():
    record = CloudBackupReadinessRecord(
        id="cloud-backup-test",
        profile_name="production",
        backup_target="private_bucket_placeholder",
        database_backup_metadata={"database_url_value": "masked"},
        export_manifest={"excluded": ["raw_secret_values"]},
        restore_checklist=["restore into isolated database"],
        raw_secrets_included=False,
    )
    gate = sync_backup_readiness(record)
    assert gate["ready"] is True
    assert gate["safe_metadata_only"] is True
    assert gate["raw_secrets_included"] is False
    assert record.status == "ready_for_restore_test"


def test_cloud_monitoring_endpoint_returns_health_summary():
    with TestClient(app) as client:
        response = client.get("/api/v1/cloud-readiness/monitoring")

    assert response.status_code == 200
    monitoring = response.json()["monitoring"]
    assert monitoring["health_status"] == "ok"
    assert "worker_heartbeat_status" in monitoring
    assert monitoring["live_provider_activation_allowed"] is False
    assert monitoring["secrets_exposed"] is False


def test_cloud_readiness_routes_render():
    with TestClient(app) as client:
        overview = client.get("/api/v1/cloud-readiness/overview")
        env = client.get("/api/v1/cloud-readiness/env")
        security = client.get("/api/v1/cloud-readiness/security")
        backups = client.get("/api/v1/cloud-readiness/backups")
        monitoring = client.get("/api/v1/cloud-readiness/monitoring")

    assert overview.status_code == 200
    assert env.status_code == 200
    assert security.status_code == 200
    assert backups.status_code == 200
    assert monitoring.status_code == 200
