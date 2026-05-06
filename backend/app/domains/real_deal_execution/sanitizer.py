from __future__ import annotations

from typing import Any

from app.serializers import model_to_dict


INTERNAL_KEYS = {
    "seller_contact",
    "internal_notes",
    "raw_strategy",
    "private_profit_logic",
}


def sanitize_execution_record(record: Any) -> dict[str, Any]:
    data = model_to_dict(record) if hasattr(record, "__mapper__") else dict(record)
    for key in INTERNAL_KEYS:
        data.pop(key, None)
    data["sanitized"] = True
    return data

