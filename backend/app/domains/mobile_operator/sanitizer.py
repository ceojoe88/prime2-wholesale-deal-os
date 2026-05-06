from __future__ import annotations

from app.serializers import model_to_dict


def sanitize_mobile_record(record: object) -> dict[str, object]:
    data = model_to_dict(record)
    data["real_world_action_taken"] = False
    data["mobile_capture_only"] = True
    return data
