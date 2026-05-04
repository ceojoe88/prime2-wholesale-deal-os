from __future__ import annotations

from datetime import datetime
from typing import Any


def model_to_dict(model: Any) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for column in model.__mapper__.columns:
        value = getattr(model, column.key)
        if isinstance(value, datetime):
            value = value.isoformat()
        data[column.key] = value
    return data
