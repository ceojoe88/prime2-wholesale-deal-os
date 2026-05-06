from __future__ import annotations

from app.serializers import model_to_dict


def sanitize_market_record(record) -> dict[str, object]:
    data = model_to_dict(record)
    data["estimate_only"] = True
    data["guaranteed_roi_allowed"] = False
    data["guaranteed_profit_allowed"] = False
    data["paid_external_api_used"] = False
    return data

