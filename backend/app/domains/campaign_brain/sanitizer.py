from __future__ import annotations

from app.serializers import model_to_dict


def sanitize_campaign_record(record) -> dict[str, object]:
    data = model_to_dict(record)
    data["bulk_blast_allowed"] = False
    if "live_send_allowed" in data:
        data["live_send_allowed"] = False
    return data

