from __future__ import annotations

from pydantic import BaseModel, Field


class ClientLeadScoreRequest(BaseModel):
    workspace_id: str | None = None
    refresh: bool = False


class ClientWorkspaceCreate(BaseModel):
    workspace_name: str
    client_name: str = ""
    market_focus: list[str] = Field(default_factory=list)
