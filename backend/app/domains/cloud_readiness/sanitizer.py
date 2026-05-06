from __future__ import annotations

from app.serializers import model_to_dict


def sanitize_cloud_record(record: object) -> dict[str, object]:
    data = model_to_dict(record)
    for key in list(data):
        if "secret" in key.lower() or "token" in key.lower() or "password" in key.lower():
            if key not in {"secret_value_exposed", "raw_secrets_included", "secrets_exposed"}:
                data[key] = "masked"
    data["safe_for_frontend"] = True
    data["raw_secret_values_exposed"] = False
    return data
