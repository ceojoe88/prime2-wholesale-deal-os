from __future__ import annotations

from app.serializers import model_to_dict


def sanitize_live_activation_record(record: object) -> dict[str, object]:
    data = model_to_dict(record)
    for key in list(data):
        if "secret" in key.lower() or "token" in key.lower() or "password" in key.lower():
            data[key] = "masked" if data[key] else data[key]
    data["secret_values_exposed"] = False
    data["response_sanitized"] = True
    return data
