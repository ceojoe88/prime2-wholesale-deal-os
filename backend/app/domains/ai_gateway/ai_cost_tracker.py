from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import AICostLedger


MODEL_COST_PER_1K_TOKENS = {
    "prime2-controlled-template": 0.0,
    "gpt-4.1-mini": 0.002,
    "gpt-4.1": 0.01,
}


def estimate_tokens(*parts: str) -> int:
    chars = sum(len(part or "") for part in parts)
    return max(1, int(chars / 4) + 24)


def estimate_cost(model: str, token_estimate: int) -> float:
    per_1k = MODEL_COST_PER_1K_TOKENS.get(model, 0.002)
    return round((token_estimate / 1000) * per_1k, 6)


def current_period() -> str:
    return datetime.now(UTC).strftime("%Y-%m")


def monthly_total(session: Session, period: str | None = None) -> float:
    target = period or current_period()
    return round(
        sum(
            ledger.cost_estimate
            for ledger in session.query(AICostLedger)
            .filter(AICostLedger.period == target)
            .all()
        ),
        6,
    )


def cost_gate(session: Session, model: str, token_estimate: int) -> dict[str, object]:
    cost = estimate_cost(model, token_estimate)
    total_after = round(monthly_total(session) + cost, 6)
    over_cap = total_after > settings.ai_monthly_cost_cap
    over_tokens = token_estimate > settings.ai_max_tokens_per_request
    flags = []
    if over_cap:
        flags.append("monthly_ai_cost_cap_exceeded")
    if over_tokens:
        flags.append("max_token_limit_exceeded")
    return {
        "allowed": not flags,
        "risk_flags": flags,
        "token_estimate": token_estimate,
        "cost_estimate": cost,
        "monthly_total_after_request": total_after,
        "monthly_cap": settings.ai_monthly_cost_cap,
        "cap_status": "blocked" if flags else "within_cap",
    }


def create_cost_ledger(
    session: Session,
    *,
    request_id: str,
    request_type: str,
    model: str,
    token_estimate: int,
    cost_estimate: float,
    monthly_total_after: float,
) -> AICostLedger:
    ledger = AICostLedger(
        id=f"ai-cost-{session.query(AICostLedger).count() + 1:03d}",
        request_id=request_id,
        period=current_period(),
        request_type=request_type,
        model=model,
        token_estimate=token_estimate,
        cost_estimate=cost_estimate,
        monthly_total_after=monthly_total_after,
        monthly_cap=settings.ai_monthly_cost_cap,
        cap_status=(
            "blocked" if monthly_total_after > settings.ai_monthly_cost_cap else "within_cap"
        ),
        provider_mode=settings.ai_provider_mode,
    )
    session.add(ledger)
    return ledger

