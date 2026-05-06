from __future__ import annotations

from app.serializers import model_to_dict


def sanitize_memory_record(record, *, external: bool = False) -> dict[str, object]:
    data = model_to_dict(record)
    data["unsupported_claims_blocked"] = True
    data["portal_exposure_allowed"] = False
    if external:
        data.pop("internal_strategy", None)
        data.pop("source_record_id", None)
        data.pop("source_signal_ids", None)
        data["external_summary_only"] = True
    return data

