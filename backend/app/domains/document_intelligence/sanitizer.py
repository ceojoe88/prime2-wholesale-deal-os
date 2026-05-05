from __future__ import annotations

from app.serializers import model_to_dict


def sanitize_document(record) -> dict[str, object]:
    data = model_to_dict(record)
    data.pop("full_text_internal", None)
    data["full_text_hidden"] = True
    data["portal_publish_allowed"] = False
    data["legal_advice_provided"] = False
    data["executable_contract_generated"] = False
    return data


def sanitize_record(record) -> dict[str, object]:
    data = model_to_dict(record)
    data["portal_publish_allowed"] = bool(data.get("portal_publish_allowed", False)) and False
    return data

