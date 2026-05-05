from __future__ import annotations

import os
from dataclasses import dataclass


def _int_env(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


def _float_env(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    app_name: str = "Virtual Wholesale Real Estate Deal OS"
    environment: str = os.getenv("APP_ENV", "local")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./wholesale_os.db")
    private_operator_only: bool = True
    owner_role: str = "Owner"
    overseer_name: str = "Prime 2"
    target_assignment_fee: int = 10_000
    auto_seed: bool = os.getenv("AUTO_SEED", "true").lower() == "true"
    communication_global_live_enabled: bool = (
        os.getenv("COMMUNICATION_GLOBAL_LIVE_ENABLED", "false").lower() == "true"
    )
    communication_provider_mode: str = os.getenv(
        "COMMUNICATION_PROVIDER_MODE", "mock/dry_run"
    )
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    ai_provider_mode: str = os.getenv("AI_PROVIDER_MODE", "mock/dry_run")
    ai_default_model: str = os.getenv("AI_DEFAULT_MODEL", "prime2-controlled-template")
    ai_max_tokens_per_request: int = _int_env("AI_MAX_TOKENS_PER_REQUEST", 1200)
    ai_monthly_cost_cap: float = _float_env("AI_MONTHLY_COST_CAP", 25.0)
    worker_max_retry_attempts: int = _int_env("WORKER_MAX_RETRY_ATTEMPTS", 3)
    worker_stuck_job_minutes: int = _int_env("WORKER_STUCK_JOB_MINUTES", 15)


settings = Settings()
