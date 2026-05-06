from __future__ import annotations

from pydantic import BaseModel


class CloudReadinessProfileRequest(BaseModel):
    profile_name: str = "production"
