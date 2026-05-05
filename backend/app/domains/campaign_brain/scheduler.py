from __future__ import annotations

from datetime import UTC, datetime, timedelta


def next_campaign_review_time(cooldown_hours: int) -> datetime:
    return datetime.now(UTC) + timedelta(hours=max(cooldown_hours, 1))

