from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "Virtual Wholesale Real Estate Deal OS"
    environment: str = os.getenv("APP_ENV", "local")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./wholesale_os.db")
    private_operator_only: bool = True
    owner_role: str = "Owner"
    overseer_name: str = "Wholesale Prime"
    target_assignment_fee: int = 10_000
    auto_seed: bool = os.getenv("AUTO_SEED", "true").lower() == "true"
    communication_global_live_enabled: bool = (
        os.getenv("COMMUNICATION_GLOBAL_LIVE_ENABLED", "false").lower() == "true"
    )
    communication_provider_mode: str = os.getenv(
        "COMMUNICATION_PROVIDER_MODE", "mock/dry_run"
    )


settings = Settings()
